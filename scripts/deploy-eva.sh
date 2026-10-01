#!/usr/bin/env bash
# Deploy Learning Analytics stack to EVA (run ON the VM after SSH)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example (UPPA proxy enabled)"
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker missing. Installing Docker Engine..."
  curl -fsSL https://get.docker.com | sh
  systemctl enable --now docker
fi

docker compose down --remove-orphans || true
docker compose up --build -d

echo "Waiting for health..."
sleep 40
python3 scripts/seed-and-verify.py || python scripts/seed-and-verify.py || true

echo
echo "Deployed on EVA."
echo "  Dashboard:     http://$(hostname -I | awk '{print $1}'):8300"
echo "  LRS:           http://$(hostname -I | awk '{print $1}'):8200"
echo "  Analytics API: http://$(hostname -I | awk '{print $1}'):8210"
docker compose ps
