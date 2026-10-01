# Scripts oraux — 2 minutes

Deux versions pour la soutenance. Chronomètre : **~2 minutes**.

---

## Version A — SANS jargon (grand public)

Bonjour,

Nous avons travaillé sur un problème simple : en cours en ligne, les élèves font des quiz, regardent des vidéos, se connectent… mais l’enseignant **ne voit pas clairement** qui décroche.

Notre projet, c’est une **petite usine automatique**. Elle collecte ces actions, les range, calcule qui est en difficulté, et propose des **conseils** pour aider.

Concrètement, on a plusieurs « boîtes » qui travaillent ensemble sur l’ordinateur et aussi sur le cloud de l’université. Un robot simule des élèves fictifs. Une boîte aux lettres reçoit leurs actions. Une armoire stocke tout. Un analyseur calcule le risque. Et une **page web** montre le résultat à l’enseignant.

Sur le tableau de bord, on voit par exemple vingt-cinq élèves, deux très à risque, et des recommandations du type « proposer du tutorat » ou « envoyer des ressources ».

Ce n’est pas des vraies données personnelles : tout est **simulé** pour la démonstration.

En résumé : on a bâti un service qui aide l’enseignant à **détecter tôt** les élèves en difficulté et à **agir** grâce aux données.

Merci, nous sommes prêts pour vos questions.

---

## Version B — AVEC jargon (enseignants / jury technique)

Bonjour,

Notre service UNITA/GEMINAE s’appelle **Learning Analytics of Educational Processes**.

Le problème : les traces d’apprentissage sont fragmentées. Nous proposons un **SaaS** déployé en **private cloud** sur EVA (`m1-siglis-cc-03`), modèle NIST Provider / Consumer.

L’architecture Docker Compose enchaîne : **xAPI generator** → **LRS** → **PostgreSQL** → **analytics worker** (ETL + Isolation Forest) → **API BI** → **dashboard** stakeholders. Grafana et Portainer restent optionnels.

Nous réutilisons des briques existantes (Postgres, nginx) et développons le glue métier : LRS xAPI, scoring d’engagement, `risk_score`, remédiations, API REST et UI.

Résultat PoC : ~2300 statements, 25 learners, distribution low/medium/high, smoke test `PASSED`. Accès démo : dashboard `:8300`, overview `/api/overview`.

SLA FREE/GOLD/PLATINUM mappé sur healthchecks, restart policies et profondeur analytics. Données synthétiques pour la confidentialité.

Perspectives : LMS réel, RGPD renforcé, orchestration Swarm/Kubernetes.

Merci, questions ?

---

## Astuces orales

- Version A si le jury est mixte / peu technique.
- Version B si on insiste sur Docker, NIST, xAPI.
- Après le script : **30 secondes de démo** (ouvrir le dashboard).
- Si stress : lire la Version A une fois à voix haute avant d’entrer.
