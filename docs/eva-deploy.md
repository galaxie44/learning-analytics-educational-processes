# EVA deployment notes

## Target

- Host: `m1-siglis-cc-03`
- IP: `10.3.16.179`
- SSH: `ssh root@10.3.16.179`
- Resources: 1 vCPU / 2 GB RAM / 30 GB
- Project path on VM: `/opt/learning-analytics`

## Checklist

1. OpenVPN Connect UPPA connected
2. `ssh root@10.3.16.179`
3. Docker Engine + Compose available
4. Copy project (`scripts/deploy-eva.ps1` or tar/scp)
5. `cp .env.example .env` (proxy UPPA + **NO_PROXY** including Docker service names)
6. Configure Docker daemon proxy (`/etc/systemd/system/docker.service.d/http-proxy.conf`) then `systemctl restart docker`
7. `docker compose up --build -d`
8. Verify:
   - `curl -s http://127.0.0.1:8210/api/overview`
   - Dashboard: http://10.3.16.179:8300

## Critical: NO_PROXY for internal Docker DNS

Without service names in `NO_PROXY`, HTTP_PROXY sends traffic to `lrs-api` via the university cache and seeding fails. `.env.example` already includes:

`postgres,lrs-api,analytics-api,analytics-worker,xapi-generator,dashboard,...`

## Optional profiles

```bash
docker compose --profile full up -d   # Grafana :3000
docker compose --profile ops up -d    # Portainer :9000
```

Prefer core stack on EVA to stay within 2 GB RAM.

## Verified status (deployment)

- Core stack healthy on EVA
- ~1000 xAPI statements seeded
- 25 learners with risk scores / remediations
- Memory footprint ~350 MiB used on 2 GiB VM
- Dashboard HTTP 200 on port 8300
