import os
import time
from datetime import datetime, timezone

import numpy as np
import psycopg
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://la_user:la_secret_change_me@postgres:5432/learning_analytics",
)
LOOP_SECONDS = int(os.getenv("LOOP_SECONDS", "60"))


def get_conn():
    return psycopg.connect(DATABASE_URL)


def wait_db(timeout: int = 180) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
            print("Database ready", flush=True)
            return
        except Exception as exc:  # noqa: BLE001
            print(f"Waiting DB: {exc}", flush=True)
            time.sleep(2)
    raise RuntimeError("Database not ready")


def remediation_for(risk: float, quiz_avg: float | None, forum_posts: int) -> str:
    if risk >= 0.7:
        if (quiz_avg or 0) < 0.5:
            return "Urgent: assign remedial quiz path and tutoring session."
        if forum_posts == 0:
            return "Encourage forum participation and peer study group."
        return "Schedule academic advisor check-in and weekly progress plan."
    if risk >= 0.4:
        return "Send personalized resource pack and monitor next quiz results."
    return "Maintain engagement with advanced optional challenges."


def compute_analytics() -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    actor_mbox,
                    MAX(actor_name) AS actor_name,
                    COUNT(*) AS total_statements,
                    COUNT(*) FILTER (WHERE verb_id LIKE '%answered%' OR verb_id LIKE '%scored%') AS quiz_attempts,
                    AVG(result_score) FILTER (WHERE result_score IS NOT NULL) AS quiz_avg_score,
                    COUNT(*) FILTER (WHERE object_id LIKE '%/video-%') AS video_views,
                    COUNT(*) FILTER (WHERE verb_id LIKE '%commented%') AS forum_posts,
                    COUNT(DISTINCT DATE(stored_at)) AS active_days,
                    MAX(stored_at) AS last_activity
                FROM statements
                WHERE actor_mbox IS NOT NULL
                GROUP BY actor_mbox
                """
            )
            rows = cur.fetchall()

        if not rows:
            print("No statements yet", flush=True)
            return

        features = []
        meta = []
        for row in rows:
            (
                actor_mbox,
                actor_name,
                total,
                quiz_attempts,
                quiz_avg,
                video_views,
                forum_posts,
                active_days,
                last_activity,
            ) = row
            quiz_avg = float(quiz_avg) if quiz_avg is not None else 0.0
            feat = [
                float(total),
                float(quiz_attempts),
                quiz_avg,
                float(video_views),
                float(forum_posts),
                float(active_days),
            ]
            features.append(feat)
            meta.append(
                {
                    "actor_mbox": actor_mbox,
                    "actor_name": actor_name,
                    "total": int(total),
                    "quiz_attempts": int(quiz_attempts),
                    "quiz_avg": quiz_avg,
                    "video_views": int(video_views),
                    "forum_posts": int(forum_posts),
                    "active_days": int(active_days),
                    "last_activity": last_activity,
                }
            )

        x = np.array(features, dtype=float)
        scaler = MinMaxScaler()
        x_scaled = scaler.fit_transform(x)

        # Engagement: weighted normalized activity
        weights = np.array([0.15, 0.2, 0.3, 0.15, 0.1, 0.1])
        engagement = np.clip((x_scaled * weights).sum(axis=1), 0, 1)

        # Risk via isolation forest anomaly + inverse engagement
        if len(x_scaled) >= 5:
            model = IsolationForest(contamination=0.2, random_state=42)
            model.fit(x_scaled)
            anomaly = -model.decision_function(x_scaled)
            anomaly = (anomaly - anomaly.min()) / (anomaly.max() - anomaly.min() + 1e-9)
        else:
            anomaly = 1 - engagement

        risk = np.clip(0.65 * (1 - engagement) + 0.35 * anomaly, 0, 1)

        with conn.cursor() as cur:
            for i, m in enumerate(meta):
                risk_score = float(risk[i])
                if risk_score >= 0.7:
                    level = "high"
                elif risk_score >= 0.4:
                    level = "medium"
                else:
                    level = "low"
                rem = remediation_for(risk_score, m["quiz_avg"], m["forum_posts"])
                cur.execute(
                    """
                    INSERT INTO learner_analytics (
                        actor_mbox, actor_name, total_statements, quiz_attempts,
                        quiz_avg_score, video_views, forum_posts, active_days,
                        last_activity, engagement_score, risk_score, risk_level,
                        remediation, updated_at
                    ) VALUES (
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW()
                    )
                    ON CONFLICT (actor_mbox) DO UPDATE SET
                        actor_name = EXCLUDED.actor_name,
                        total_statements = EXCLUDED.total_statements,
                        quiz_attempts = EXCLUDED.quiz_attempts,
                        quiz_avg_score = EXCLUDED.quiz_avg_score,
                        video_views = EXCLUDED.video_views,
                        forum_posts = EXCLUDED.forum_posts,
                        active_days = EXCLUDED.active_days,
                        last_activity = EXCLUDED.last_activity,
                        engagement_score = EXCLUDED.engagement_score,
                        risk_score = EXCLUDED.risk_score,
                        risk_level = EXCLUDED.risk_level,
                        remediation = EXCLUDED.remediation,
                        updated_at = NOW()
                    """,
                    (
                        m["actor_mbox"],
                        m["actor_name"],
                        m["total"],
                        m["quiz_attempts"],
                        m["quiz_avg"],
                        m["video_views"],
                        m["forum_posts"],
                        m["active_days"],
                        m["last_activity"],
                        float(engagement[i]),
                        risk_score,
                        level,
                        rem,
                    ),
                )

            cur.execute(
                """
                INSERT INTO course_kpis (course_id, learners, statements, avg_quiz_score, at_risk_learners, updated_at)
                SELECT
                    s.course_id,
                    s.learners,
                    s.statements,
                    s.avg_quiz_score,
                    COALESCE(r.at_risk_learners, 0) AS at_risk_learners,
                    NOW()
                FROM (
                    SELECT
                        COALESCE(context_course, 'unknown') AS course_id,
                        COUNT(DISTINCT actor_mbox) AS learners,
                        COUNT(*) AS statements,
                        AVG(result_score) FILTER (WHERE result_score IS NOT NULL) AS avg_quiz_score
                    FROM statements
                    GROUP BY COALESCE(context_course, 'unknown')
                ) s
                LEFT JOIN (
                    SELECT
                        COALESCE(st.context_course, 'unknown') AS course_id,
                        COUNT(DISTINCT la.actor_mbox) AS at_risk_learners
                    FROM learner_analytics la
                    JOIN statements st ON st.actor_mbox = la.actor_mbox
                    WHERE la.risk_level = 'high'
                    GROUP BY COALESCE(st.context_course, 'unknown')
                ) r ON r.course_id = s.course_id
                ON CONFLICT (course_id) DO UPDATE SET
                    learners = EXCLUDED.learners,
                    statements = EXCLUDED.statements,
                    avg_quiz_score = EXCLUDED.avg_quiz_score,
                    at_risk_learners = EXCLUDED.at_risk_learners,
                    updated_at = NOW()
                """
            )
        conn.commit()
        print(
            f"[{datetime.now(timezone.utc).isoformat()}] Updated analytics for {len(meta)} learners",
            flush=True,
        )


def main() -> None:
    wait_db()
    while True:
        try:
            compute_analytics()
        except Exception as exc:  # noqa: BLE001
            print(f"Worker error: {exc}", flush=True)
        time.sleep(LOOP_SECONDS)


if __name__ == "__main__":
    main()
