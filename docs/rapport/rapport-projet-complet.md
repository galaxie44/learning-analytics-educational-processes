# Rapport projet — Learning Analytics of Educational Processes

**À copier dans le template Moodle « Cloud Computing I — Project report »** (sections ci-dessous alignées sur le template).

**Cours** : SIGLIS M1 · Cloud Computing I — Docker & containers  
**Équipe 1** : Bastien Bruey, Edouard Clemenceau, Titoan Lalanne, Jiale Li, Yoan Minbielle  
**Service** : Learning analytics of educational processes (UNITA / GEMINAE)  
**Déploiement** : Private cloud EVA — `m1-siglis-cc-03` (`10.3.16.179`)

---

## Project summary

Nous proposons une plateforme **SaaS** de **Learning Analytics** déployée en **conteneurs Docker** sur le cloud pédagogique UPPA (EVA). Elle ingère des traces d’apprentissage au standard **xAPI** via un **Learning Record Store (LRS)** minimal, les persiste dans **PostgreSQL**, exécute un pipeline **ETL + machine learning** (score d’engagement, détection d’apprenants à risque, recommandations de remédiation), et expose les résultats via une **API REST** et un **dashboard** pour enseignants et coordinateurs de programme.

Le proof-of-concept utilise un **générateur de statements synthétiques** (25 apprenants fictifs) afin de respecter la confidentialité tout en démontrant la chaîne bout-en-bout. La stack est reproductible en local (Docker Desktop) et en production pédagogique sur EVA (2 Go RAM, proxy HTTP UPPA).

---

## Evaluation of Learning Outcomes

| Attente du service Learning Analytics | Réalisation dans notre PoC |
|---------------------------------------|----------------------------|
| Intégration / interopérabilité (xAPI, LRS) | `lrs-api` : POST/GET `/xAPI/statements`, auth Basic ; générateur simulant activités LMS |
| BI / analytics sur données éducatives | `analytics-api` : overview, liste learners, KPIs engagement |
| Entrepôt + mining / ML | Postgres + `analytics-worker` : agrégations, IsolationForest, `risk_score` |
| Stratégies data-driven de remédiation | Table/API `remediations` liée au niveau de risque |
| Communication aux stakeholders | Dashboard web `:8300` + JSON API pour intégrations futures |

---

## Business Model Canvas

| Bloc | Contenu |
|------|---------|
| **Customer segments** | Enseignants, coordinateurs de filière, établissements partenaires UNITA |
| **Value proposition** | Détection précoce du décrochage, vue cohorte, remédiations suggérées, déploiement cloud maîtrisé |
| **Channels** | Dashboard web, API REST, (option) Grafana pour équipes data |
| **Customer relationships** | Self-service SaaS, support selon tier SLA |
| **Revenue streams** | Modèle freemium : FREE / GOLD / PLATINUM (voir SLA) |
| **Key resources** | Stack Docker, LRS, entrepôt Postgres, modèles ML, VM EVA |
| **Key activities** | Ingestion xAPI, calcul périodique analytics, exploitation dashboard |
| **Key partners** | UPPA (EVA, proxy), écosystème xAPI/ADL, LMS sources de traces |
| **Cost structure** | VM dédiée ~200 €/mois (hypothèse cours), coût marginal faible par tenant containerisé |

---

## ArchiMate

Trois couches documentées dans `docs/archimate/README.md` (diagrammes Mermaid) :

- **Business** : enseignant / coordinateur → service LA → processus de remédiation → décision data-driven
- **Application** : generator, LRS, worker, API, dashboard, Grafana
- **Technology** : Docker Engine sur LXC EVA, Compose, réseau bridge, accès VPN, proxy UPPA

*Joindre au rapport : exports PNG des trois diagrammes.*

---

## 1. Fundamental concepts (NIST cloud)

- **Service model** : **SaaS** — l’utilisateur final (enseignant) consomme le dashboard sans gérer l’infra.
- **Deployment model** : **Private cloud** — ressources EVA réservées au projet, accès VPN.
- **Rôles NIST** : Cloud **Provider** (UPPA / équipe ops) ; Cloud **Consumer** (enseignants, coordinateurs) ; perspective **Auditor** (conformité RGPD sur données réelles — hors scope PoC synthétique).
- **Caractéristiques essentielles** :
  - *On-demand self-service* : `docker compose up` provisionne la stack
  - *Broad network access* : HTTP depuis VPN / localhost
  - *Resource pooling* : conteneurs partagent la VM (limites mémoire Compose)
  - *Rapid elasticity* : perspective scale-out Swarm/K8s (non implémenté en PoC)
  - *Measured service* : KPIs exposés (`statements`, `at_risk`, engagement)

---

## 2. Cloud service usage and competitors

**Concurrents / références** : Learning Locker, SQL LRS, analytics natifs Moodle/Canvas, solutions BI génériques.

**Différenciation** :

- Stack **légère** et **pédagogique** (alignée cours Docker)
- **Remédiation** intégrée dans l’API/dashboard (pas seulement des graphiques)
- Déploiement **reproductible** local ↔ EVA via Compose et `.env`

**Usage typique** : un établissement connecte ses LMS/outils xAPI au LRS ; le worker recalcule les scores toutes les N minutes ; les enseignants consultent le dashboard en début de semaine.

---

## 3. Design and development

### 3.1 Architecture technique

Services : `postgres`, `lrs-api`, `xapi-generator`, `analytics-worker`, `analytics-api`, `dashboard` ; optionnels `grafana`, `portainer`.

Communication interne : réseau Docker `la-net`. Le dashboard proxifie `/api/` vers `analytics-api`.

### 3.2 Sécurité et confidentialité

- Auth **HTTP Basic** sur le LRS (identifiants via variables d’environnement, non commités)
- Données **synthétiques** en démonstration
- Proxy UPPA sur EVA : configuration `HTTP_PROXY` / `HTTPS_PROXY` + `NO_PROXY` pour le trafic inter-conteneurs

### 3.3 SLA (FREE / GOLD / PLATINUM)

| Tier | Disponibilité | Rétention | Analytics |
|------|---------------|-----------|-----------|
| FREE | Best effort | 7 jours | KPIs de base |
| GOLD | Healthchecks + restart | 30 jours | Remédiations |
| PLATINUM | Monitoring + alerting (perspective) | 90 jours | ML + alerting |

**Implémentation PoC** : healthchecks Docker, `restart: unless-stopped`, limites mémoire pour stabilité EVA.

### 3.4 Tests

Script `scripts/seed-and-verify.py` : health LRS/API/dashboard, présence statements, overview cohérent, HTML dashboard.

---

## Architecture diagram

Reprendre le schéma du README ou la couche Technology ArchiMate.

```text
xapi-generator → lrs-api → postgres
                    ↑
analytics-worker ───┴──→ learner_analytics
analytics-api ←──────────
dashboard → analytics-api
```

---

## Results and demo

Indicateurs observés (local / EVA) :

- ~1000–1300 statements xAPI
- 25 apprenants simulés
- Distribution de risque (low / medium / high) et liste `at_risk`
- Remédiations textuelles par profil

**URLs démo** :

- Local : http://localhost:8300 , http://localhost:8210/api/overview
- EVA (VPN) : http://10.3.16.179:8300 , http://10.3.16.179:8210/api/overview

---

## Conclusion and perspectives

Le PoC prouve la faisabilité d’un service Learning Analytics **containerisé** sur EVA avec interopérabilité **xAPI**, analytics **ML** et **UX** enseignant. Perspectives : connecter un vrai LMS, renforcer RGPD (pseudonymisation, rétention), orchestration Swarm/K8s, alerting PLATINUM, SSO.

---

## References

- NIST SP 800-145 — Definition of Cloud Computing
- NIST Cloud Computing Reference Architecture
- xAPI Specification (ADL)
- Documentation projet : README.md, docs/GUIDE-PROJET-ET-TESTS.md

---

## Annex — Captures à insérer

Voir `docs/CAPTURES-DEMO.md` (liste des screenshots pour le rapport et les slides).
