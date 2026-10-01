# Guide du projet — en quoi ça consiste et comment tester (5–10 min)

Document pour **comprendre le sujet**, **l’expliquer à l’oral** et **valider que tout marche**, sans être expert DevOps.

---

## 1. En une phrase

Vous avez construit une **plateforme cloud type SaaS** (conteneurs Docker) qui **collecte des traces d’apprentissage** au format **xAPI**, les **stocke**, les **analyse** (KPIs + détection de risque par ML), puis les **montre** aux enseignants via un **dashboard** et une **API**.

---

## 2. Contexte pédagogique (pourquoi ce projet existe)

- **Cours** : Cloud Computing I (Docker & conteneurs), SIGLIS M1 UPPA.
- **Thème UNITA/GEMINAE** : *Learning analytics of educational processes*.
- **Consigne enseignant** : ne pas tout coder from scratch ; réutiliser des briques (Postgres, Grafana, Portainer…) et **ajouter la valeur métier** : xAPI, analytics, ML, remédiation, dashboard.
- **Livrables** : rapport (initial + final), slides, cookbook yPBL, démo sur **EVA** (VM privée UPPA derrière VPN).

---

## 3. Le problème métier (storytelling soutenance)

Aujourd’hui, les activités d’un cours sont éparpillées (LMS, quiz, vidéos…). Les enseignants voient mal :

- qui **décroche** avant l’échec ;
- qui est **engagé** mais en difficulté ;
- quelle **action** proposer (relance, ressource, tutorat).

Votre solution **centralise les événements** (xAPI), **calcule des indicateurs**, **score le risque**, et **suggère des remédiations** dans une interface simple.

---

## 4. Architecture (ce qui tourne dans Docker)

Flux de données :

```text
xapi-generator  →  lrs-api  →  postgres
                      ↑
analytics-worker  ----+----→  tables analytics (learners, KPIs)
analytics-api     ←---+
dashboard (nginx) → proxy /api → analytics-api
```

| Conteneur | Rôle concret |
|-----------|----------------|
| **postgres** | Base : statements xAPI bruts + tables `learner_analytics`, KPIs cours |
| **lrs-api** | Mini-LRS : reçoit et sert les statements (`/xAPI/statements`), auth Basic |
| **xapi-generator** | Simule ~25 apprenants qui font des actions (login, quiz, vidéo…) et envoie des statements au LRS |
| **analytics-worker** | Boucle ETL : lit Postgres, calcule engagement, **IsolationForest** pour anomalie/risque, remédiations |
| **analytics-api** | REST BI : `/api/overview`, `/api/learners`, `/api/remediations` |
| **dashboard** | Page web pour enseignants (tableau risque, KPIs) |
| **grafana** / **portainer** | Optionnels (`--profile full` / `ops`) — souvent désactivés sur EVA (2 Go RAM) |

**Modèle cloud NIST** : vous **consommez** le service comme enseignant (SaaS) ; l’**équipe / UPPA** **fournit** l’infra sur **private cloud** EVA (`m1-siglis-cc-03`, `10.3.16.179`).

---

## 5. Ce que vous avez « inventé » vs réutilisé

| Réutilisé | Développé par l’équipe |
|-----------|-------------------------|
| Postgres, nginx, Grafana, Portainer | LRS xAPI minimal, générateur, worker ML, API BI, dashboard métier, Compose + scripts test/déploiement |

C’est exactement ce que Daniel Sanchez attend : **glue métier** autour de briques existantes.

---

## 6. Test simple — local (recommandé avant soutenance)

**Prérequis** : Docker Desktop démarré, Python 3.

```powershell
cd "c:\Users\edoua\Desktop\Master SIGLIS\Cloud computing\Projet"
copy .env.local.example .env
docker compose up --build -d
```

Attendre **1–2 minutes** (le générateur envoie les traces). Puis :

```powershell
python scripts\seed-and-verify.py
```

**Succès** : dernière ligne `SMOKE TEST PASSED` + chiffres du type ~1000+ statements, 25 learners, quelques `at_risk`.

**Vérification manuelle (navigateur)** :

| URL | Ce que vous devez voir |
|-----|-------------------------|
| http://localhost:8300 | Dashboard avec KPIs et liste apprenants |
| http://localhost:8210/api/overview | JSON : `statements`, `learners`, `at_risk`, `avg_engagement` |
| http://localhost:8200/health | `{"status":"ok"}` |

**Une commande tout-en-un** :

```powershell
.\scripts\test-stack.ps1
```

(démarre Compose si besoin + smoke test)

---

## 7. Test simple — EVA (démo officielle)

1. **OpenVPN Connect** avec le profil UPPA (réseau `10.3.x.x`).
2. SSH : `ssh root@10.3.16.179`
3. Sur la VM : `cd /opt/learning-analytics` (ou le chemin où le projet est copié)
4. `.env` depuis `.env.example` (proxy UPPA + **NO_PROXY** incluant `lrs-api`, `postgres`, etc.)
5. `docker compose up --build -d`
6. Depuis votre PC (toujours VPN) :
   - Dashboard : http://10.3.16.179:8300
   - API : http://10.3.16.179:8210/api/overview

**Smoke test depuis votre PC** (API joignables en local port-forward ou curl sur la VM) :

```bash
# sur la VM
python3 scripts/seed-and-verify.py
# ou avec URLs EVA depuis le PC si ports exposés :
# set ANALYTICS_API_URL=http://10.3.16.179:8210 etc.
```

**Piège connu** : sans `NO_PROXY` pour les noms de services Docker, le générateur passe par le proxy universitaire et **n’atteint pas** le LRS → 0 statements. Corrigé dans `.env.example`.

---

## 8. Comment expliquer le flux xAPI (30 secondes)

1. Un **statement xAPI** = « qui a fait quoi, quand, sur quelle ressource » (JSON standard ADL).
2. Le **LRS** est la boîte aux lettres normée qui **accepte** ces JSON.
3. Le **worker** transforme l’historique en **features** (fréquence, scores quiz…) → **risk_score** + texte de **remédiation**.
4. Le **dashboard** ne parle pas xAPI : il consomme l’**API analytics** (plus simple pour l’UI).

---

## 9. SLA (FREE / GOLD / PLATINUM) — lien avec le code

Ce n’est pas facturé en PoC, mais le **rapport** doit montrer la **traduction technique** :

| Promesse | Implémentation actuelle |
|----------|-------------------------|
| Disponibilité | `restart: unless-stopped`, healthchecks |
| Sécurité LRS | Auth HTTP Basic (user/pass dans `.env`) |
| Données | Synthétiques / pseudonymisées (pas de vrais étudiants) |
| Rétention | Postgres (durée configurable ; pas de purge auto en PoC) |

---

## 10. Checklist « projet terminé »

- [x] Stack Docker Compose fonctionnelle (local + EVA documenté)
- [x] Smoke test automatisé
- [x] Rapport initial + contenu rapport final (`docs/rapport/rapport-projet-complet.md`)
- [x] Slides texte complet (`docs/rapport/presentation-complet.md`)
- [x] Cookbook yPBL (`docs/cookbook-ypbl.md`)
- [x] ArchiMate Mermaid (`docs/archimate/README.md`) → exporter PNG pour Word
- [ ] **À faire par l’équipe** : coller le Markdown dans le **DOCX Moodle**, faire les **captures** (`docs/CAPTURES-DEMO.md`), soumettre sur elearn

---

## 11. Fichiers utiles

| Fichier | Usage |
|---------|--------|
| `README.md` | Vue d’ensemble technique |
| `docs/eva-deploy.md` | Déploiement pas à pas EVA |
| `docs/rapport/rapport-projet-complet.md` | Rapport final prêt à transférer dans le template Word |
| `docs/LIVRABLES-MOODLE.md` | Liste de rendu Moodle + dates |

---

## Équipe

BRUEY Bastien · CLEMENCEAU Edouard · LALANNE Titoan · LI Jiale · MINBIELLE Yoan
