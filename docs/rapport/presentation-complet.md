# Présentation orale — texte complet des slides

**Durée** : ~20 min + 10 min questions  
**Usage** : copier chaque bloc dans une slide PowerPoint / Google Slides  
**Notes orateur** : en italique sous chaque slide

---

## Slide 1 — Titre

**Learning Analytics of Educational Processes**

Équipe 1 — Cloud Computing I — SIGLIS M1 UPPA

Bastien Bruey · Edouard Clemenceau · Titoan Lalanne · Jiale Li · Yoan Minbielle

*Notes : annoncer le service UNITA/GEMINAE et l’objectif : cloud Docker + analytics pédagogique.*

---

## Slide 2 — Problématique

- Traces d’apprentissage **dispersées** (LMS, quiz, vidéos)
- **Décrochage** souvent détecté trop tard
- Peu d’**actions** guidées par la donnée pour les enseignants

*Notes : 1 exemple concret — un étudiant qui stoppe les quiz 3 semaines avant l’examen.*

---

## Slide 3 — Objectif du service

Fournir un **SaaS** qui :

1. **Collecte** (xAPI / LRS)
2. **Analyse** (KPIs + ML)
3. **Recommande** (remédiations)
4. **Communique** (dashboard + API)

*Notes : rappeler les 5 learning outcomes du sujet.*

---

## Slide 4 — Acteurs

| Acteur | Besoin |
|--------|--------|
| Enseignant | Vue risque + actions |
| Coordinateur | Vue cohorte / cours |
| Apprenant | Parcours adapté (indirect) |
| Provider (UPPA/EVA) | Hébergement sécurisé |

*Notes : placer sur schéma NIST Consumer / Provider.*

---

## Slide 5 — Positionnement cloud (NIST)

- **Service model** : SaaS
- **Deployment** : Private cloud EVA
- VM : `m1-siglis-cc-03` — `10.3.16.179`
- Accès : VPN + SSH

*Notes : insister : enseignant ne gère pas Docker, il utilise le dashboard.*

---

## Slide 6 — Architecture Docker

```
xapi-generator → lrs-api → postgres
                      ↑
analytics-worker ─────┴──→ analytics tables
analytics-api ←────────────
dashboard (nginx) → API
```

Optionnel : Grafana, Portainer (profils Compose)

*Notes : montrer `docker compose ps` en capture.*

---

## Slide 7 — Briques réutilisées vs développées

**Réutilisé** : PostgreSQL, nginx, Grafana, Portainer

**Développé** : LRS xAPI, générateur, worker ML, API BI, dashboard métier, scripts test

*Notes : réponse directe à la consigne « ni from scratch ni collage d’images ».*

---

## Slide 8 — xAPI en 20 secondes

- Standard **JSON** : acteur + verbe + objet + résultat
- **LRS** = entrepôt normé de statements
- Interopérabilité entre outils éducatifs

*Notes : option demo curl `/xAPI/statements?limit=1` avec auth Basic.*

---

## Slide 9 — Analytics & ML

- **Engagement** : agrégats d’activité, scores quiz simulés
- **Risque** : IsolationForest sur features comportementales
- **Remédiation** : règles + textes actionnables par niveau de risque

*Notes : ne pas entrer dans les hyperparamètres — rester sur l’intention pédagogique.*

---

## Slide 10 — API & Dashboard

- `GET /api/overview` — KPIs globaux
- `GET /api/learners` — tri par risque
- `GET /api/remediations` — suggestions

Dashboard : http://…:8300

*Notes : live demo 2 min si réseau OK.*

---

## Slide 11 — Résultats PoC

- ~1000+ statements
- 25 apprenants simulés
- Apprenants **at risk** identifiés
- Smoke test automatisé **PASSED**

*Notes : chiffres exacts du jour de la démo.*

---

## Slide 12 — SLA & sécurité

| Tier | Idée |
|------|------|
| FREE / GOLD / PLATINUM | rétention + profondeur analytics |

PoC : healthchecks, restart policies, auth LRS, **données synthétiques**

*Notes : mentionner RGPD si passage en production réelle.*

---

## Slide 13 — Contraintes EVA

- 1 vCPU, **2 Go RAM** → stack allégée
- Proxy UPPA → `.env` + **NO_PROXY** inter-services
- OpenVPN obligatoire

*Notes : anecdote 0 statements avant fix NO_PROXY — montre maîtrise ops.*

---

## Slide 14 — Business Model Canvas (synthèse)

- **Valeur** : détection précoce + remédiation
- **Clients** : enseignants UNITA / établissements
- **Canal** : dashboard + API
- **Revenus** : tiers FREE/GOLD/PLATINUM

*Notes : renvoyer au rapport pour le canvas complet.*

---

## Slide 15 — ArchiMate

Trois couches : Business / Application / Technology

*Notes : afficher les 3 PNG exportés depuis Mermaid.*

---

## Slide 16 — Roadmap & conclusion

- Rapport initial ✓
- PoC Docker local + EVA ✓
- Soutenance finale : BMC, ArchiMate, perspectives Swarm/K8s, LMS réel

**Merci — questions ?**

*Notes : distribuer le runbook : `docs/GUIDE-PROJET-ET-TESTS.md`.*
