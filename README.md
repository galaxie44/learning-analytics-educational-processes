# Learning Analytics of Educational Processes

Plateforme cloud Docker (SaaS éducatif) pour l’équipe 1 — **Cloud Computing I · SIGLIS M1**.

Service : intégration de traces d’apprentissage **xAPI**, entrepôt PostgreSQL, analytics / ML de risque, API BI et dashboard stakeholders.

## Architecture

```text
xapi-generator -> lrs-api -> postgres
                     ^
analytics-worker ----+----> learner_analytics / course_kpis
analytics-api  <-----+
dashboard (nginx) -> analytics-api
grafana (profile full)
portainer (profile ops)
```

NIST : **SaaS**, déploiement **private cloud** (EVA UPPA).

## Prérequis

- Docker + Docker Compose
- Python 3 (pour le smoke test hôte)
- Sur EVA : OpenVPN Connect + proxy UPPA

## Démarrage local (Docker Desktop)

```powershell
cd "Projet"
copy .env.local.example .env
docker compose up --build -d
python scripts\seed-and-verify.py
```

Ou :

```powershell
.\scripts\test-stack.ps1
```

### URLs locales

| Service | URL |
|---------|-----|
| LRS (xAPI) | http://localhost:8200/xAPI/statements |
| Analytics API | http://localhost:8210/api/overview |
| Dashboard | http://localhost:8300 |
| Grafana (optionnel) | `docker compose --profile full up -d` → http://localhost:3000 |
| Portainer (optionnel) | `docker compose --profile ops up -d` → http://localhost:9000 |

Auth LRS (Basic) : `lrs` / `lrs_secret_change_me` (modifiable via `.env`).

## Déploiement EVA (2 Go RAM)

Machine attribuée :

- Host : `m1-siglis-cc-03`
- IP : `10.3.16.179`
- SSH : `ssh root@10.3.16.179`

Étapes :

1. Connecter **OpenVPN Connect**
2. `ssh root@10.3.16.179`
3. Copier le projet (git clone ou `scp`)
4. Créer `.env` depuis `.env.example` (proxy UPPA inclus)
5. Lancer la stack **légère** (sans Grafana/Portainer) :

```bash
cp .env.example .env
# adapter les mots de passe si besoin
docker compose up --build -d
# optionnel BI :
# docker compose --profile full up -d
```

6. Accès (depuis le VPN) :
   - Dashboard : http://10.3.16.179:8300
   - LRS : http://10.3.16.179:8200
   - Analytics API : http://10.3.16.179:8210

Les limites mémoire Compose sont calibrées pour ~2 Go RAM.

## Smoke test

```bash
python scripts/seed-and-verify.py
```

Vérifie healthchecks, présence de statements xAPI, calcul d’analytics (learners / risk), dashboard.

## Documentation projet

- **[docs/EXPLICATION-SIMPLE.md](docs/EXPLICATION-SIMPLE.md)** — explication sans jargon + légende capture API
- **[docs/SCRIPT-ORAL-2MIN.md](docs/SCRIPT-ORAL-2MIN.md)** — script oral 2 min (avec / sans jargon)
- **[docs/livrables/](docs/livrables/)** — PowerPoint + Word générés
- **[docs/GUIDE-PROJET-ET-TESTS.md](docs/GUIDE-PROJET-ET-TESTS.md)** — en quoi consiste le projet + test simple (5–10 min)
- [docs/LIVRABLES-MOODLE.md](docs/LIVRABLES-MOODLE.md) — checklist rendu elearn
- [docs/CAPTURES-DEMO.md](docs/CAPTURES-DEMO.md) — screenshots rapport / slides
- [docs/rapport/rapport-initial.md](docs/rapport/rapport-initial.md) — jalon 12 octobre
- [docs/rapport/rapport-projet-complet.md](docs/rapport/rapport-projet-complet.md) — rapport final (contenu Word)
- [docs/rapport/presentation-complet.md](docs/rapport/presentation-complet.md) — slides + notes orateur
- [docs/rapport/slides-avancement.md](docs/rapport/slides-avancement.md) — version courte
- [docs/cookbook-ypbl.md](docs/cookbook-ypbl.md)
- [docs/archimate/README.md](docs/archimate/README.md)
- [docs/eva-deploy.md](docs/eva-deploy.md)

## Équipe

BRUEY Bastien · CLEMENCEAU Edouard · LALANNE Titoan · LI Jiale · MINBIELLE Yoan

## SLA (aperçu)

| Classe | Disponibilité | Rétention | Support analytics |
|--------|---------------|-----------|-------------------|
| FREE | best effort | 7 jours | KPIs de base |
| GOLD | healthchecks + restart | 30 jours | remédiations |
| PLATINUM | monitoring + quotas | 90 jours | ML + alerting |

Implémenté techniquement : healthchecks, `restart: unless-stopped`, auth Basic LRS, secrets via env, données synthétiques pseudonymisées.
