import os
import secrets
import uuid
from datetime import datetime, timezone
from typing import Any

import psycopg
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://la_user:la_secret_change_me@postgres:5432/learning_analytics",
)
LRS_USER = os.getenv("LRS_BASIC_USER", "lrs")
LRS_PASS = os.getenv("LRS_BASIC_PASS", "lrs_secret_change_me")

app = FastAPI(title="Learning Analytics LRS", version="1.0.0")
security = HTTPBasic()


class Actor(BaseModel):
    mbox: str | None = None
    name: str | None = None
    objectType: str | None = "Agent"


class Verb(BaseModel):
    id: str
    display: dict[str, str] | None = None


class ActivityDefinition(BaseModel):
    name: dict[str, str] | None = None
    type: str | None = None


class ObjectModel(BaseModel):
    id: str
    objectType: str | None = "Activity"
    definition: ActivityDefinition | None = None


class ResultModel(BaseModel):
    score: dict[str, float] | None = None
    success: bool | None = None
    duration: str | None = None
    response: str | None = None


class ContextModel(BaseModel):
    contextActivities: dict[str, Any] | None = None
    extensions: dict[str, Any] | None = None


class Statement(BaseModel):
    id: str | None = None
    actor: Actor
    verb: Verb
    object: ObjectModel
    result: ResultModel | None = None
    context: ContextModel | None = None
    timestamp: str | None = None


def require_auth(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    user_ok = secrets.compare_digest(credentials.username, LRS_USER)
    pass_ok = secrets.compare_digest(credentials.password, LRS_PASS)
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid LRS credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def get_conn():
    return psycopg.connect(DATABASE_URL)


def parse_duration_seconds(duration: str | None) -> float | None:
    if not duration or not duration.startswith("PT"):
        return None
    value = duration[2:]
    seconds = 0.0
    num = ""
    for ch in value:
        if ch.isdigit() or ch == ".":
            num += ch
        elif ch == "H" and num:
            seconds += float(num) * 3600
            num = ""
        elif ch == "M" and num:
            seconds += float(num) * 60
            num = ""
        elif ch == "S" and num:
            seconds += float(num)
            num = ""
    return seconds or None


def extract_course(context: ContextModel | None) -> str | None:
    if not context or not context.contextActivities:
        return None
    parents = context.contextActivities.get("parent") or []
    if parents and isinstance(parents, list):
        first = parents[0]
        if isinstance(first, dict):
            return first.get("id")
    return None


def store_statement(stmt: Statement) -> str:
    statement_id = stmt.id or str(uuid.uuid4())
    actor_mbox = stmt.actor.mbox
    actor_name = stmt.actor.name
    object_name = None
    if stmt.object.definition and stmt.object.definition.name:
        object_name = stmt.object.definition.name.get("en-US") or next(
            iter(stmt.object.definition.name.values()), None
        )
    score = None
    if stmt.result and stmt.result.score:
        score = stmt.result.score.get("scaled")
        if score is None and "raw" in stmt.result.score:
            raw = stmt.result.score["raw"]
            maximum = stmt.result.score.get("max", 100) or 100
            score = raw / maximum
    success = stmt.result.success if stmt.result else None
    duration = parse_duration_seconds(stmt.result.duration if stmt.result else None)
    course = extract_course(stmt.context)
    payload = stmt.model_dump()
    payload["id"] = statement_id
    if not payload.get("timestamp"):
        payload["timestamp"] = datetime.now(timezone.utc).isoformat()

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO statements (
                    id, actor_mbox, actor_name, verb_id, object_id, object_name,
                    result_score, result_success, result_duration_seconds,
                    context_course, statement, stored_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, NOW()
                )
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    statement_id,
                    actor_mbox,
                    actor_name,
                    stmt.verb.id,
                    stmt.object.id,
                    object_name,
                    score,
                    success,
                    duration,
                    course,
                    psycopg.types.json.Json(payload),
                ),
            )
        conn.commit()
    return statement_id


@app.get("/health")
def health():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return {"status": "ok", "service": "lrs-api"}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/xAPI/statements")
def post_statements(
    payload: Statement | list[Statement],
    _: str = Depends(require_auth),
):
    statements = payload if isinstance(payload, list) else [payload]
    if not statements:
        raise HTTPException(status_code=400, detail="Empty statement payload")
    ids = [store_statement(s) for s in statements]
    return ids


@app.get("/xAPI/statements")
def get_statements(
    limit: int = Query(50, ge=1, le=500),
    actor: str | None = None,
    verb: str | None = None,
    _: str = Depends(require_auth),
):
    clauses = []
    params: list[Any] = []
    if actor:
        clauses.append("actor_mbox = %s")
        params.append(actor if actor.startswith("mailto:") else f"mailto:{actor}")
    if verb:
        clauses.append("verb_id = %s")
        params.append(verb)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    params.append(limit)
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT statement
                FROM statements
                {where}
                ORDER BY stored_at DESC
                LIMIT %s
                """,
                params,
            )
            rows = [row[0] for row in cur.fetchall()]
    return {"statements": rows, "more": ""}
