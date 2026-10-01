#!/usr/bin/env python3
"""Capture des écrans démo (API + dashboard) pour le rapport."""

from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "captures"
OUT.mkdir(parents=True, exist_ok=True)

URLS = {
    "01-api-overview.json": "http://localhost:8210/api/overview",
    "02-api-learners.json": "http://localhost:8210/api/learners?limit=5",
    "03-api-remediations.json": "http://localhost:8210/api/remediations?limit=5",
    "04-lrs-health.json": "http://localhost:8200/health",
    "05-dashboard.html": "http://localhost:8300/",
}


def main() -> None:
    for name, url in URLS.items():
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = resp.read()
            (OUT / name).write_bytes(data)
            print(f"OK {name} ({len(data)} bytes)")
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {name}: {exc}")
    legend = OUT / "LEGENDE-CAPTURES.md"
    legend.write_text(
        """# Légendes captures (rapport)

1. **01-api-overview.json** — Résumé brut serveur (`/api/overview`).
2. **05-dashboard.html** — Page enseignant (à ouvrir aussi en screenshot navigateur).
3. Terminal : coller aussi une capture de `SMOKE TEST PASSED`.

> Les fichiers JSON/HTML ici sont des preuves techniques.
> Pour le Word Moodle, préférer aussi des **screenshots PNG** du navigateur (API + dashboard).
""",
        encoding="utf-8",
    )
    print(f"Legend: {legend}")


if __name__ == "__main__":
    main()
