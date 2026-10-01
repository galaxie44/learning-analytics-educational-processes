# Rapport initial — Learning Analytics of Educational Processes

**Cours** : SIGLIS M1 · Cloud Computing I — Docker & containers  
**Équipe 1** : Bastien Bruey, Edouard Clemenceau, Titoan Lalanne, Jiale Li, Yoan Minbielle  
**Jalon** : 12 octobre (rapport initial — pas de PoC obligatoire)  
**Contexte** : UNITA / GEMINAE — Cloud Environment for Education of the Future

## 1. Problématique identifiée

Dans un environnement d’enseignement digitalisé (LMS, quiz, vidéos, forums), les traces d’apprentissage sont **fragmentées**. Les enseignants et coordinateurs manquent d’une vue intégrée pour :

- détecter tôt les apprenants en difficulté ;
- comprendre les patterns d’engagement ;
- proposer des **remédiations** data-driven ;
- communiquer des insights clairs aux parties prenantes.

Le problème n’est pas seulement le stockage de logs, mais l’**interopérabilité** (standard xAPI), l’**analyse** (BI + ML) et l’**action** pédagogique.

## 2. Acteurs principaux

| Acteur NIST / métier | Rôle |
|----------------------|------|
| Cloud Consumer — Enseignant | Consulte KPIs, alertes risque, remédiations |
| Cloud Consumer — Coordinateur de programme | Suit cohortes / cours, qualité pédagogique |
| Cloud Consumer — Étudiant (indirect) | Bénéficie de parcours remédiés |
| Cloud Provider — Équipe projet / UPPA EVA | Déploie et opère la plateforme Docker |
| Cloud Auditor (perspective) | Conformité traces / confidentialité (données synthétiques en PoC) |

## 3. Besoins

1. Intégrer des événements d’apprentissage via un standard interopérable (**xAPI**).
2. Stocker durablement les statements dans un entrepôt.
3. Calculer des indicateurs (engagement, scores, activité).
4. Estimer un **risque de désengagement / échec** et proposer des remédiations.
5. Exposer les résultats via API + dashboard compréhensible.
6. Déployer la solution en **containers Docker** sur le cloud pédagogique EVA.

## 4. Solution proposée (esquisse Docker)

Service cloud de type **SaaS** sur **private cloud** EVA :

1. **lrs-api** — mini Learning Record Store (POST/GET `/xAPI/statements`)
2. **postgres** — data warehouse des statements + tables analytics
3. **xapi-generator** — simulation de traces multi-apprenants (démonstration)
4. **analytics-worker** — ETL + ML (IsolationForest + score d’engagement)
5. **analytics-api** — API BI (`/api/overview`, `/api/learners`, `/api/remediations`)
6. **dashboard** — interface stakeholders
7. **grafana** / **portainer** — briques existantes optionnelles (profils Compose)

Choix volontaire : **réutiliser** Postgres/Grafana/Portainer et **développer** le glue métier Learning Analytics (conforme à la consigne : ni tout from scratch, ni simple collage d’images).

## 5. Pourquoi Docker répond au problème

- Isolation et reproductibilité de la chaîne analytics
- Composition multi-services (Compose) alignée labs du cours
- Déploiement portable local → EVA
- Caractéristiques cloud : on-demand self-service, measured service (KPIs), rapid elasticity (perspective Swarm)

## 6. Prochaines étapes

- Finaliser PoC déployée sur EVA (`10.3.16.179`)
- Compléter Business Model Canvas + ArchiMate (séances ultérieures)
- Préparer soutenance d’avancement (13/14 octobre) puis soutenance finale (21/22 octobre)

## Références

- Project Context and Requirements (elearn)
- NIST SP 800-145 / Cloud Computing Reference Architecture
- xAPI / ADL LRS specification
