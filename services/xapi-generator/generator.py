import os
import random
import time
import uuid
from datetime import datetime, timezone

import requests

# Ensure Docker service DNS bypasses UPPA HTTP proxy
os.environ.setdefault(
    "NO_PROXY",
    "127.0.0.1,localhost,postgres,lrs-api,analytics-api,analytics-worker,xapi-generator,dashboard",
)
os.environ["no_proxy"] = os.environ.get("NO_PROXY", "")

LRS_URL = os.getenv("LRS_URL", "http://lrs-api:8000").rstrip("/")
USER = os.getenv("LRS_BASIC_USER", "lrs")
PASS = os.getenv("LRS_BASIC_PASS", "lrs_secret_change_me")
STUDENT_COUNT = int(os.getenv("STUDENT_COUNT", "25"))
STATEMENTS_PER_STUDENT = int(os.getenv("STATEMENTS_PER_STUDENT", "40"))
LOOP_SECONDS = int(os.getenv("LOOP_SECONDS", "120"))

COURSES = [
    ("http://example.org/course/cloud-computing", "Cloud Computing I"),
    ("http://example.org/course/devops", "DevOps Fundamentals"),
    ("http://example.org/course/networks", "Computer Networks"),
]

VERBS = {
    "initialized": "http://adlnet.gov/expapi/verbs/initialized",
    "experienced": "http://adlnet.gov/expapi/verbs/experienced",
    "completed": "http://adlnet.gov/expapi/verbs/completed",
    "answered": "http://adlnet.gov/expapi/verbs/answered",
    "scored": "http://adlnet.gov/expapi/verbs/scored",
    "commented": "http://adlnet.gov/expapi/verbs/commented",
}

ACTIVITIES = [
    ("video", "http://example.org/activities/video-{i}", "Lecture video {i}"),
    ("quiz", "http://example.org/activities/quiz-{i}", "Quiz {i}"),
    ("forum", "http://example.org/activities/forum-{i}", "Forum topic {i}"),
    ("reading", "http://example.org/activities/reading-{i}", "Reading {i}"),
]


def wait_for_lrs(timeout: int = 600) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(f"{LRS_URL}/health", timeout=3)
            if r.status_code == 200:
                print("LRS is ready", flush=True)
                return
        except requests.RequestException:
            pass
        time.sleep(2)
    raise RuntimeError("LRS not ready")


def student_profile(i: int) -> dict:
    # Mix of engaged / average / at-risk learners
    if i % 5 == 0:
        return {"name": f"Learner AtRisk {i}", "engagement": 0.25}
    if i % 3 == 0:
        return {"name": f"Learner Average {i}", "engagement": 0.55}
    return {"name": f"Learner Engaged {i}", "engagement": 0.85}


def build_statement(student_idx: int, activity_idx: int) -> dict:
    profile = student_profile(student_idx)
    course_id, course_name = random.choice(COURSES)
    kind, id_tpl, name_tpl = random.choice(ACTIVITIES)
    act_id = id_tpl.format(i=activity_idx % 8 + 1)
    act_name = name_tpl.format(i=activity_idx % 8 + 1)
    mbox = f"mailto:learner{student_idx:02d}@univ-pau.fr"

    if kind == "quiz":
        verb = VERBS["answered"]
        score = max(0.0, min(1.0, random.gauss(profile["engagement"], 0.15)))
        result = {
            "score": {"scaled": round(score, 2), "raw": round(score * 100), "max": 100},
            "success": score >= 0.5,
            "duration": f"PT{random.randint(3, 20)}M{random.randint(0, 59)}S",
        }
    elif kind == "video":
        verb = VERBS["experienced"]
        result = {"duration": f"PT{random.randint(2, 25)}M{random.randint(0, 59)}S"}
    elif kind == "forum":
        verb = VERBS["commented"]
        result = {"response": "Synthetic forum contribution for learning analytics."}
    else:
        verb = random.choice([VERBS["initialized"], VERBS["completed"], VERBS["experienced"]])
        result = {"success": random.random() < profile["engagement"]}

    return {
        "id": str(uuid.uuid4()),
        "actor": {"objectType": "Agent", "name": profile["name"], "mbox": mbox},
        "verb": {"id": verb, "display": {"en-US": verb.split("/")[-1]}},
        "object": {
            "id": act_id,
            "objectType": "Activity",
            "definition": {
                "name": {"en-US": act_name},
                "type": f"http://adlnet.gov/expapi/activities/{kind}",
            },
        },
        "result": result,
        "context": {
            "contextActivities": {
                "parent": [
                    {
                        "id": course_id,
                        "objectType": "Activity",
                        "definition": {"name": {"en-US": course_name}},
                    }
                ]
            }
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def post_batch(statements: list[dict]) -> None:
    r = requests.post(
        f"{LRS_URL}/xAPI/statements",
        json=statements,
        auth=(USER, PASS),
        timeout=30,
    )
    r.raise_for_status()
    print(f"Posted {len(statements)} statements -> {r.status_code}", flush=True)


def seed_once() -> None:
    batch: list[dict] = []
    for s in range(1, STUDENT_COUNT + 1):
        for a in range(STATEMENTS_PER_STUDENT):
            batch.append(build_statement(s, a))
            if len(batch) >= 50:
                post_batch(batch)
                batch = []
    if batch:
        post_batch(batch)


def main() -> None:
    wait_for_lrs()
    print("Initial seed...", flush=True)
    seed_once()
    while True:
        print(f"Sleeping {LOOP_SECONDS}s before incremental generation...", flush=True)
        time.sleep(LOOP_SECONDS)
        # Incremental light traffic
        batch = [build_statement(random.randint(1, STUDENT_COUNT), random.randint(1, 20)) for _ in range(20)]
        try:
            post_batch(batch)
        except requests.RequestException as exc:
            print(f"Generator error: {exc}", flush=True)


if __name__ == "__main__":
    main()
