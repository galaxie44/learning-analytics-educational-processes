# Guide captures d’écran — rapport & slides

Prendre ces captures **en local** et **sur EVA (VPN)** pour le rapport final.

## 1. Infrastructure

**Commande** (PowerShell ou SSH) :

```powershell
docker compose ps
```

**Attendu** : `la-postgres`, `la-lrs-api`, `la-xapi-generator`, `la-analytics-worker`, `la-analytics-api`, `la-dashboard` — statut Up / healthy.

**Légende rapport** : « Stack Docker Compose — Learning Analytics PoC »

---

## 2. Dashboard enseignant

**URL local** : http://localhost:8300  
**URL EVA** : http://10.3.16.179:8300 (VPN connecté)

**Attendu** : cartes KPI (statements, learners, at-risk, engagement) + tableau apprenants.

**Légende** : « Interface stakeholders — vue risque et engagement »

---

## 3. API overview (JSON)

Navigateur ou curl :

```powershell
curl http://localhost:8210/api/overview
```

**Attendu** : JSON avec `statements`, `learners`, `at_risk`, `avg_engagement`, `risk_distribution`.

**Légende** : « API BI — indicateurs agrégés »

---

## 4. Smoke test

```powershell
python scripts\seed-and-verify.py
```

Capture de la fin avec `SMOKE TEST PASSED` et ligne `Overview: {...}`.

**Légende** : « Validation automatisée bout-en-bout »

---

## 5. (Option) Statement xAPI

Avec auth Basic (`lrs` / mot de passe `.env`) :

```powershell
curl -u lrs:VOTRE_MOT_DE_PASSE "http://localhost:8200/xAPI/statements?limit=1"
```

**Légende** : « Interopérabilité xAPI — échantillon de statement stocké »

---

## Export ArchiMate

1. Ouvrir https://mermaid.live
2. Coller chaque bloc Mermaid de `docs/archimate/README.md`
3. Export PNG → insérer dans Word sous « ArchiMate »
