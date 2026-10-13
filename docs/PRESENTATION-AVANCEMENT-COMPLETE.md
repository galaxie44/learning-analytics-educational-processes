# Présentation d’avancement COMPLÈTE — 13/14 octobre

**Durée cible** : 15–20 min + 10 min questions  
**Message** : l’avancement = **on a terminé la PoC technique**  
**Fichier slides** : `docs/livrables/Presentation-Avancement-COMPLETE.pptx`

---

## Script oral (à lire / apprendre)

### Slide 1 — Titre (~30 s)

Bonjour,

Nous sommes l’équipe 1 : Bastien, Edouard, Titoan, Jiale et Yoan.

Notre sujet : **Learning Analytics of Educational Processes**.

Aujourd’hui c’est la présentation d’**avancement**. On va être directs :  
**notre avancement, c’est que la preuve de concept Docker est déjà terminée et fonctionnelle.**

---

### Slide 2 — Message d’avancement (~45 s)

Le minimum demandé pour cette séance était :
- avoir défini le problème,
- proposé une idée de solution,
- commencé Docker.

De notre côté, on a déjà :
- une **stack complète** qui tourne,
- un **dashboard** avec KPIs, risque et remédiations,
- des **tests automatisés** verts,
- un déploiement **documenté sur EVA**.

Donc on vous montre aujourd’hui le **résultat technique**, pas seulement une intention.

---

### Slide 3 — Problématique (~1 min)

Dans un enseignement digitalisé, les élèves font des quiz, regardent des vidéos, se connectent…

Le problème : ces traces sont **dispersées**.  
L’enseignant voit mal :
- qui décroche,
- qui est en difficulté,
- quoi proposer concrètement.

On veut détecter le risque **tôt**, et proposer des **actions**.

---

### Slide 4 — Solution (~1 min)

On propose un service cloud de type **SaaS** :
1. **Collecter** les événements au format **xAPI**
2. **Stocker** dans un entrepôt
3. **Analyser** (engagement + score de risque)
4. **Recommander** des remédiations
5. **Communiquer** via un dashboard et une API

Les données de démo sont **synthétiques** (pas de vrais étudiants).

---

### Slide 5 — Cloud NIST (~45 s)

- **SaaS** : l’enseignant utilise le dashboard, sans gérer l’infra
- **Private cloud** : VM EVA UPPA
- Machine : `m1-siglis-cc-03`, IP `10.3.16.179`
- Accès derrière **OpenVPN**

---

### Slide 6 — Architecture Docker (~1 min 30)

La chaîne Docker Compose :

`générateur xAPI → LRS → Postgres → worker analytics → API → dashboard`

Chaque boîte = un conteneur.
- Le générateur simule des apprenants
- Le LRS reçoit les statements xAPI
- Postgres stocke
- Le worker calcule engagement / risque / remédiations
- L’API et le dashboard exposent le résultat

Grafana / Portainer = optionnels.

---

### Slide 7 — Réutilisé vs développé (~45 s)

On a respecté la consigne du cours :
- **Réutilisé** : Postgres, nginx, Grafana, Portainer
- **Développé** : le glue métier Learning Analytics (LRS, générateur, ML, API, UI)

Ni tout from scratch, ni simple collage d’images.

---

### Slide 8 — Ce qui tourne (~1 min)

Aujourd’hui, en démo :
- Compose multi-services UP
- des milliers de statements xAPI
- 25 apprenants simulés
- liste triée par risque + remédiations
- smoke test `PASSED`
- images poussées sur Docker Hub

---

### Slide 9 — DÉMO (~2–3 min) ★

*(Ouvrir le navigateur)*

1. Dashboard : **http://localhost:8300**  
   → montrer KPIs, élève HIGH risk, remédiation urgente
2. API : **http://localhost:8210/api/overview**  
   → même info en JSON (preuve serveur)
3. Si VPN : **http://10.3.16.179:8300**

Phrase :  
« Ce que vous voyez, c’est le produit déjà utilisable par un enseignant. »

---

### Slide 10 — Ops EVA (~45 s)

Contraintes prises en compte :
- 2 Go RAM → stack légère
- proxy UPPA + `NO_PROXY` pour les services internes
- `restart: on-failure:3` (pas de redémarrage illimité, conforme au mail Proxmox)

---

### Slide 11 — Roadmap (~45 s)

- ✓ Problème / solution / PoC Docker
- ✓ Démo locale + EVA
- → Soutenance finale : Business Model Canvas, ArchiMate, cookbook, slides finales
- Perspectives : brancher un vrai LMS, RGPD, orchestration Swarm/K8s

---

### Slide 12 — Merci / questions (~20 s)

Merci.  
Repo : `github.com/galaxie44/learning-analytics-educational-processes`

On est prêts pour vos questions.

---

## Checklist avant 8h

- [ ] Ouvrir Docker Desktop
- [ ] `docker compose up -d` dans le dossier Projet
- [ ] Tester http://localhost:8300
- [ ] Ouvrir le PPTX
- [ ] Avoir le script sous les yeux (téléphone OK)

Commandes express :

```powershell
cd "c:\Users\edoua\Desktop\Master SIGLIS\Cloud computing\Projet"
docker compose up -d
start http://localhost:8300
start docs\livrables\Presentation-Avancement-COMPLETE.pptx
```

---

## Réponses rapides aux questions probables

**Pourquoi Docker ?**  
Isoler chaque service, reproduire local → EVA, aligné au cours.

**Pourquoi xAPI ?**  
Standard d’interopérabilité des traces éducatives.

**C’est du vrai ML ?**  
Oui, score d’engagement + Isolation Forest pour le risque, sur données simulées.

**Et la suite ?**  
Finaliser les livrables de soutenance (BMC, ArchiMate, cookbook), pas reconstruire le code.
