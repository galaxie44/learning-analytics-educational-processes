# Outline rapport final (template Moodle)

À reporter dans le fichier DOCX « Cloud Computing II - Project Template ».

## Project summary
Plateforme SaaS de Learning Analytics basée Docker : collecte xAPI, entrepôt Postgres, analytics/ML, dashboard de remédiation pour enseignants et coordinateurs UNITA/GEMINAE.

## Evaluation of Learning Outcomes
Mapper les 5 attentes du service Learning Analytics (intégration, BI, mining/ML, stratégies data-driven, communication).

## Business Model Canvas
- Value proposition : détection précoce + remédiation
- Customer segments : enseignants, coordinateurs, établissements UNITA
- Channels : dashboard web / API
- Revenue : FREE / GOLD / PLATINUM (voir SLA)
- Cost structure : ~200 €/mois serveur dédié (hypothèse cours) amorti sur N containers

## ArchiMate
Voir `docs/archimate/`.

## 1. Fundamental concepts (NIST)
- SaaS offert aux consumers éducatifs
- Private cloud EVA
- Caractéristiques : on-demand, network access, resource pooling, measured service ; elasticity via Swarm en perspective

## 2. Cloud Service usage / competitors
Comparer à Learning Locker, Ralph LRS, solutions LMS analytics Moodle — différenciation : stack pédagogique légère, remédiation intégrée, déploiement cours Docker.

## 3. Design & Development
- Services Compose, healthchecks, restart policies
- Auth Basic LRS, secrets env
- SLA mapping :
  - Availability : healthchecks + restart
  - Performance : memory limits / KPIs
  - Security/privacy : auth + données synthétiques

## Architecture Diagram
Reprendre le schéma README / ArchiMate technology layer.

## Captures
- `docker compose ps`
- Dashboard http://...:8300
- `/api/overview`
- (EVA) `ssh root@10.3.16.179` + URLs 10.3.16.179
