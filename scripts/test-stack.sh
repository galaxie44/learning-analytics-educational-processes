#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env ]]; then
  cp .env.local.example .env
fi

docker compose up --build -d
echo "Waiting for services..."
sleep 25
python3 scripts/seed-and-verify.py

echo
echo "Stack is up:"
echo "  LRS API:        http://localhost:8200/health"
echo "  Analytics API:  http://localhost:8210/health"
echo "  Dashboard:      http://localhost:8300"
echo "  Grafana (full): docker compose --profile full up -d"
echo "  Portainer(ops): docker compose --profile ops up -d"
