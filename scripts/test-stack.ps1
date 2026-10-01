$ErrorActionPreference = "Stop"
Write-Host "== Building and starting Learning Analytics stack =="
Set-Location $PSScriptRoot\..

if (-not (Test-Path .env)) {
  Copy-Item .env.local.example .env
}

docker compose up --build -d
Write-Host "Waiting for services..."
Start-Sleep -Seconds 20

python "$PSScriptRoot\seed-and-verify.py"
if ($LASTEXITCODE -ne 0) {
  Write-Host "Smoke test failed. Recent logs:"
  docker compose logs --tail=80
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Stack is up:"
Write-Host "  LRS API:        http://localhost:8200/health"
Write-Host "  Analytics API:  http://localhost:8210/health"
Write-Host "  Dashboard:      http://localhost:8300"
Write-Host "  Grafana (full): docker compose --profile full up -d"
Write-Host "  Portainer(ops): docker compose --profile ops up -d"
