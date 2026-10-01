#!/usr/bin/env python3
"""Smoke test for the Learning Analytics stack."""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from base64 import b64encode

LRS_URL = os.getenv("LRS_URL", "http://localhost:8200").rstrip("/")
API_URL = os.getenv("ANALYTICS_API_URL", "http://localhost:8210").rstrip("/")
DASH_URL = os.getenv("DASHBOARD_URL", "http://localhost:8300").rstrip("/")
LRS_USER = os.getenv("LRS_BASIC_USER", "lrs")
LRS_PASS = os.getenv("LRS_BASIC_PASS", "lrs_secret_change_me")


def http_json(url: str, method: str = "GET", data: dict | list | None = None, auth: tuple[str, str] | None = None):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if auth:
        token = b64encode(f"{auth[0]}:{auth[1]}".encode()).decode()
        headers["Authorization"] = f"Basic {token}"
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode()
        return resp.status, json.loads(raw) if raw else {}


def wait(url: str, auth: tuple[str, str] | None = None, timeout: int = 180) -> None:
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        try:
            status, payload = http_json(url, auth=auth)
            if status == 200:
                print(f"OK {url}")
                return
            last = f"status={status} payload={payload}"
        except Exception as exc:  # noqa: BLE001
            last = str(exc)
        time.sleep(3)
    raise RuntimeError(f"Timeout waiting for {url}: {last}")


def main() -> int:
    print("== Learning Analytics smoke test ==")
    wait(f"{LRS_URL}/health")
    wait(f"{API_URL}/health")
    wait(f"{DASH_URL}/health")

    # Ensure at least some statements exist (generator should already seed)
    status, payload = http_json(
        f"{LRS_URL}/xAPI/statements?limit=5",
        auth=(LRS_USER, LRS_PASS),
    )
    assert status == 200, payload
    statements = payload.get("statements") or []
    print(f"LRS statements sample: {len(statements)}")
    if not statements:
        demo = {
            "actor": {"mbox": "mailto:smoke@univ-pau.fr", "name": "Smoke Tester"},
            "verb": {"id": "http://adlnet.gov/expapi/verbs/experienced"},
            "object": {
                "id": "http://example.org/activities/smoke",
                "definition": {"name": {"en-US": "Smoke activity"}},
            },
            "result": {"score": {"scaled": 0.8}},
        }
        status, ids = http_json(
            f"{LRS_URL}/xAPI/statements",
            method="POST",
            data=demo,
            auth=(LRS_USER, LRS_PASS),
        )
        assert status == 200, ids
        print(f"Posted smoke statement: {ids}")
        time.sleep(5)

    # Wait for analytics worker to populate learner_analytics
    deadline = time.time() + 180
    overview = {}
    while time.time() < deadline:
        _, overview = http_json(f"{API_URL}/api/overview")
        if overview.get("learners", 0) > 0 and overview.get("statements", 0) > 0:
            break
        time.sleep(5)
    print("Overview:", overview)
    assert overview.get("statements", 0) > 0, "No statements in analytics overview"
    assert overview.get("learners", 0) > 0, "No learners computed yet"

    _, learners = http_json(f"{API_URL}/api/learners?limit=5")
    assert learners.get("learners"), "Empty learners list"
    print(f"Learners returned: {len(learners['learners'])}")

    _, rem = http_json(f"{API_URL}/api/remediations?limit=5")
    print(f"Remediations returned: {len(rem.get('remediations') or [])}")

    # Dashboard HTML reachable
    req = urllib.request.Request(DASH_URL)
    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode()
        assert "Learning Analytics" in html
    print("Dashboard HTML OK")
    print("SMOKE TEST PASSED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"SMOKE TEST FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
