# yPBL Cookbook — Learning Analytics of Educational Processes

## Challenge / Problem
Comment fournir un service cloud d’analytics pédagogique capable d’intégrer des traces hétérogènes, d’analyser les parcours et de recommander des remédiations aux enseignants et coordinateurs ?

## Learning outcomes (service expectations)
1. Expliquer intégration / interopérabilité (xAPI, LRS)
2. Appliquer outils BI/analytics sur données éducatives
3. Utiliser entrepôt + mining/ML pour patterns et prédiction
4. Mettre en œuvre des stratégies data-driven de remédiation
5. Communiquer les insights aux stakeholders

## Proposed solution
Plateforme Docker multi-conteneurs : LRS xAPI + Postgres + worker ML + API + dashboard (+ Grafana/Portainer).

## Cloud mapping
- Service model : SaaS
- Deployment : private cloud EVA
- IaC : Dockerfiles + Compose

## Runbook (étudiant)
1. Copier `.env.local.example` → `.env` (local) ou `.env.example` (EVA)
2. `docker compose up --build -d`
3. Attendre seed generator (~1–2 min)
4. Ouvrir dashboard `:8300`
5. Vérifier `python scripts/seed-and-verify.py`

## EVA specifics
- VPN OpenVPN
- `ssh root@10.3.16.179`
- Proxy `cache.univ-pau.fr:3128` via `.env`
- Ressources limitées (1 vCPU / 2 Go) → éviter profils lourds sauf besoin

## Success criteria
- [x] Statements xAPI stockés (~1000+ en PoC)
- [x] Learners + risk_score calculés (25 apprenants simulés)
- [x] Dashboard accessible (`:8300`)
- [x] Smoke test vert (`python scripts/seed-and-verify.py`)
- [x] Documentation (rapport complet, ArchiMate, guide test)
- [x] Démo EVA documentée (`docs/eva-deploy.md`, VM `10.3.16.179`)

## Assessment rubric (auto-évaluation équipe)

| Critère | Preuve |
|---------|--------|
| Compréhension cloud NIST | Rapport § SaaS + private cloud EVA |
| Docker / Compose | `docker compose ps`, healthchecks |
| xAPI | LRS + générateur + curl statements |
| Analytics / ML | `/api/overview`, worker IsolationForest |
| Stakeholder UX | Dashboard + remédiations |
| Ops EVA | Proxy, NO_PROXY, 2 Go RAM |

## Team workflow
Répartir : infra Compose / LRS / analytics-ML / dashboard / documentation-soutenance.

## Liens repo
- Guide test : `docs/GUIDE-PROJET-ET-TESTS.md`
- Rapport Word-ready : `docs/rapport/rapport-projet-complet.md`
- Template Google Doc yPBL : https://bit.ly/ypbl-cookbook-template (copier les sections ci-dessus)
