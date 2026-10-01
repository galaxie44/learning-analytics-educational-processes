$ErrorActionPreference = "Stop"
# Copy project to EVA and deploy. Requires OpenVPN connected.
$Project = Resolve-Path (Join-Path $PSScriptRoot "..")
$HostIp = "10.3.16.179"
$Remote = "root@${HostIp}"
$RemoteDir = "/opt/learning-analytics"

Write-Host "Testing SSH to $Remote ..."
ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new $Remote "echo OK; hostname; free -h"

Write-Host "Creating remote directory..."
ssh $Remote "mkdir -p $RemoteDir"

Write-Host "Syncing project (tar over ssh)..."
$exclude = @('.git', '__pycache__', '.venv', 'postgres-data')
# Use tar for portability
Push-Location $Project
tar -czf "$env:TEMP\la-project.tgz" --exclude=.git --exclude=__pycache__ --exclude=.venv *
Pop-Location
scp "$env:TEMP\la-project.tgz" "${Remote}:/tmp/la-project.tgz"
ssh $Remote "mkdir -p $RemoteDir && tar -xzf /tmp/la-project.tgz -C $RemoteDir && cd $RemoteDir && cp -n .env.example .env && bash scripts/deploy-eva.sh"

Write-Host "Done. Open http://${HostIp}:8300 (VPN required)"
