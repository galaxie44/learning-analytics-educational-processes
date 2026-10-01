# Explication ultra-simple du projet

Document pour quelqu’un qui **n’est pas** dans l’informatique.

---

## En une phrase

On a construit une **petite usine automatique** qui :

1. **collecte** des actions d’élèves fictifs (quiz, vidéos, connexions…),
2. **les range**,
3. **calcule** qui est en difficulté,
4. **affiche** tout ça sur une page web pour l’enseignant.

---

## Le problème (pourquoi on a fait ça)

Les élèves font plein d’activités en ligne, mais les infos sont **éparpillées**.  
L’enseignant ne voit pas clairement :

- qui décroche,
- qui risque d’échouer,
- quoi proposer pour aider.

---

## La solution (notre projet)

Une plateforme type **service en ligne** (SaaS) qui tourne dans des **boîtes Docker** (comme des petits appareils logiciels qui travaillent ensemble).

Les « élèves » sont **fictifs** (simulation) : pas de vraies données personnelles.

---

## Comment ça marche (histoire simple)

Imagine une chaîne :

1. Un **robot** invente des actions d’élèves (le générateur).
2. Une **boîte aux lettres** reçoit ces actions au format standard xAPI (le LRS).
3. Une **armoire** stocke tout (la base Postgres).
4. Un **analyste** calcule engagement + risque + conseils (le worker).
5. Une **fenêtre web** montre le résultat à l’enseignant (le dashboard).

```text
Robot → Boîte aux lettres → Armoire → Analyste → Page web enseignant
```

---

## Ce que montrent les écrans / le terminal

### Dashboard (`http://localhost:8300`)

C’est **l’écran pour l’enseignant** :

- chiffres clés en haut (combien d’actions, combien d’élèves, combien à risque…),
- liste des élèves **triés du plus à risque au moins à risque**,
- **conseils** (remédiations) à droite.

→ C’est la démo principale pour la soutenance.

### API (`http://localhost:8210/api/overview`)

C’est **la même information**, mais en texte brut (JSON).

→ Ça prouve que le « cerveau » calcule bien, même sans jolie interface.

### Terminal (`SMOKE TEST PASSED`)

C’est un **contrôle automatique** :

- les services répondent,
- il y a des données,
- le dashboard est accessible.

→ Si tu vois `SMOKE TEST PASSED`, **tout est bon**.

### Pourquoi les chiffres bougent (2300, 2400…) ?

Parce que le robot **continue d’envoyer** des actions.  
Ce n’est pas un bug.

---

## Phrase pour la soutenance (à apprendre)

> « On a bâti un service cloud en conteneurs qui collecte des traces d’apprentissage, détecte les élèves à risque, et affiche des recommandations pour l’enseignant. »

## Scripts oraux complets (2 minutes)

Voir **[SCRIPT-ORAL-2MIN.md](SCRIPT-ORAL-2MIN.md)** :

- Version A — sans jargon
- Version B — avec jargon technique

---

## Comment retester en 1 minute

1. Docker Desktop ouvert.
2. Dans le dossier du projet :

```powershell
copy .env.local.example .env
docker compose up --build -d
python scripts\seed-and-verify.py
```

3. Ouvrir :
   - http://localhost:8300 → dashboard
   - http://localhost:8210/api/overview → chiffres bruts

---

## Captures à garder pour le rapport

1. **API overview** — preuve que le calcul serveur marche  
2. **Dashboard** — preuve que l’enseignant voit les résultats  
3. **Terminal** avec `SMOKE TEST PASSED` — preuve du test auto  
4. (Plus tard) même chose sur EVA si possible

Explication détaillée de la capture 1 : section suivante.

---

## Capture 1 — expliquer `localhost:8210/api/overview`

### Qu’est-ce que c’est ?

Pas une jolie page. C’est une **réponse machine** : une ligne de texte avec des chiffres.

Adresse : `localhost:8210/api/overview`

- `localhost` = sur **ton** PC (pas Internet public)
- `8210` = la « porte » du service analytics
- `/api/overview` = « donne-moi le **résumé global** »

### À quoi ça sert ?

Le dashboard joli lit **ces mêmes chiffres** pour afficher les cartes en haut.  
Cette page = **preuve technique** que le calcul fonctionne.

### Lire la ligne (exemple)

```text
{"statements":2300,"learners":25,"at_risk":2,"avg_engagement":0.472,"avg_risk":0.517,"risk_distribution":{"medium":17,"high":2,"low":6}}
```

| Mot technique | Traduction simple |
|---------------|-------------------|
| `statements: 2300` | 2300 actions enregistrées (quiz, vidéo, etc.) |
| `learners: 25` | 25 élèves suivis |
| `at_risk: 2` | 2 élèves jugés **très à risque** |
| `avg_engagement: 0.472` | engagement moyen ≈ **47 %** |
| `avg_risk: 0.517` | risque moyen ≈ **52 %** |
| `risk_distribution` | répartition : 6 faible / 17 moyen / 2 élevé |

### Phrase pour coller sous la capture (légende rapport)

> « Vue API `/api/overview` : résumé calculé par le serveur (2300 statements, 25 apprenants, 2 à risque). Preuve que le pipeline analytics fonctionne avant affichage dashboard. »

### En 10 secondes à l’oral

> « Cette page n’est pas pour l’enseignant. C’est le résumé brut produit par le serveur. Le dashboard lit exactement ces chiffres pour les afficher proprement. »
