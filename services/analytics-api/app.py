import os
from typing import Any

import psycopg
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://la_user:la_secret_change_me@postgres:5432/learning_analytics",
)

app = FastAPI(title="Learning Analytics API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_conn():
    return psycopg.connect(DATABASE_URL)


@app.get("/health")
def health():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return {"status": "ok", "service": "analytics-api"}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/overview")
def overview():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM statements")
            statements = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM learner_analytics")
            learners = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM learner_analytics WHERE risk_level = 'high'")
            at_risk = cur.fetchone()[0]
            cur.execute("SELECT AVG(engagement_score), AVG(risk_score) FROM learner_analytics")
            avg_eng, avg_risk = cur.fetchone()
            cur.execute(
                """
                SELECT risk_level, COUNT(*)
                FROM learner_analytics
                GROUP BY risk_level
                """
            )
            by_risk = {row[0]: row[1] for row in cur.fetchall()}
    return {
        "statements": statements,
        "learners": learners,
        "at_risk": at_risk,
        "avg_engagement": round(float(avg_eng or 0), 3),
        "avg_risk": round(float(avg_risk or 0), 3),
        "risk_distribution": by_risk,
    }


@app.get("/api/learners")
def learners(
    risk_level: str | None = None,
    limit: int = Query(50, ge=1, le=500),
):
    clauses = []
    params: list[Any] = []
    if risk_level:
        clauses.append("risk_level = %s")
        params.append(risk_level)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    params.append(limit)
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT actor_mbox, actor_name, total_statements, quiz_attempts,
                       quiz_avg_score, video_views, forum_posts, active_days,
                       last_activity, engagement_score, risk_score, risk_level,
                       remediation, updated_at
                FROM learner_analytics
                {where}
                ORDER BY risk_score DESC NULLS LAST
                LIMIT %s
                """,
                params,
            )
            cols = [d[0] for d in cur.description]
            rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    for row in rows:
        for key in ("quiz_avg_score", "engagement_score", "risk_score"):
            if row.get(key) is not None:
                row[key] = round(float(row[key]), 3)
        if row.get("last_activity"):
            row["last_activity"] = row["last_activity"].isoformat()
        if row.get("updated_at"):
            row["updated_at"] = row["updated_at"].isoformat()
    return {"learners": rows}


@app.get("/api/courses")
def courses():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT course_id, learners, statements, avg_quiz_score,
                       at_risk_learners, updated_at
                FROM course_kpis
                ORDER BY statements DESC
                """
            )
            cols = [d[0] for d in cur.description]
            rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    for row in rows:
        if row.get("avg_quiz_score") is not None:
            row["avg_quiz_score"] = round(float(row["avg_quiz_score"]), 3)
        if row.get("updated_at"):
            row["updated_at"] = row["updated_at"].isoformat()
    return {"courses": rows}


@app.get("/api/remediations")
def remediations(limit: int = Query(20, ge=1, le=100)):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT actor_name, actor_mbox, risk_level, risk_score, remediation
                FROM learner_analytics
                WHERE risk_level IN ('high', 'medium')
                ORDER BY risk_score DESC
                LIMIT %s
                """,
                (limit,),
            )
            cols = [d[0] for d in cur.description]
            rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    for row in rows:
        if row.get("risk_score") is not None:
            row["risk_score"] = round(float(row["risk_score"]), 3)
    return {"remediations": rows}
