# Slides d’avancement — Learning Analytics (13/14 octobre)

Structure recommandée (20 min + 10 Q&A). À copier dans PowerPoint / Google Slides.

## Slide 1 — Titre
- Learning Analytics of Educational Processes
- Team 1 · Cloud Computing I · SIGLIS
- Membres : Bastien, Edouard, Titoan, Jiale, Yoan

## Slide 2 — Problématique
- Traces éducatives dispersées
- Besoin de détection précoce du décrochage
- Décision pédagogique peu outillée par la donnée

## Slide 3 — Acteurs & besoins
- Enseignants, coordinateurs, apprenants
- Intégration xAPI, BI, ML, remédiation, communication

## Slide 4 — Positionnement cloud (NIST)
- Service model : **SaaS**
- Deployment : **Private cloud** (EVA UPPA)
- Provider / Consumer / (Auditor)

## Slide 5 — Architecture Docker
Schéma :
`generator → LRS → Postgres → worker ML → API → dashboard`
(+ Grafana/Portainer optionnels)

## Slide 6 — Ce qui est déjà implémenté
- Compose multi-conteneurs
- Ingestion xAPI + auth
- Analytics risque + remédiations
- Dashboard stakeholders
- Smoke tests

## Slide 7 — Démo / résultats attendus
- KPIs : statements, learners, at-risk
- Table apprenants triée par risque
- Remédiations actionnables

## Slide 8 — Roadmap
- 12 oct : rapport initial
- 13/14 oct : avancement + quiz
- 21/22 oct : soutenance finale (BMC, ArchiMate, EVA)

## Slide 9 — Risques & mitigation
- 2 Go RAM EVA → stack légère + profils optionnels
- Proxy UPPA → `.env` / `env_file`
- Données réelles sensibles → synthétiques en PoC
