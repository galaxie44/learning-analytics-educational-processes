# Checklist livrables Moodle — équipe 1

## Code & démo (terminé dans le dépôt)

- [x] `docker-compose.yml` + services (LRS, worker, API, dashboard, …)
- [x] `.env.example` (EVA + proxy + NO_PROXY)
- [x] `.env.local.example` (local)
- [x] `scripts/seed-and-verify.py`, `test-stack.ps1`, `deploy-eva.*`
- [x] README + `docs/eva-deploy.md`
- [x] Smoke test validé en local

## Documents à **soumettre** sur elearn (action équipe)

| Livrable | Source dans le repo | Action |
|----------|---------------------|--------|
| Rapport Word | `docs/livrables/Rapport-Learning-Analytics.docx` | Adapter au template Moodle si demandé |
| Slides PPTX | `docs/livrables/Presentation-Learning-Analytics.pptx` | Utiliser tel quel ou importer dans Google Slides |
| Scripts oraux | `docs/SCRIPT-ORAL-2MIN.md` | Version A (simple) / B (technique) |
| Rapport Markdown | `docs/rapport/rapport-projet-complet.md` | Source texte |
| Cookbook yPBL | `docs/cookbook-ypbl.md` | Copier dans [template officiel](https://bit.ly/ypbl-cookbook-template) |
| ArchiMate | `docs/archimate/README.md` | Exporter 3 PNG (Mermaid Live) → rapport |
| Captures | `docs/captures/` + screenshots navigateur | Voir `docs/CAPTURES-DEMO.md` |

## Captures minimales (5)

1. `docker compose ps` (tous healthy / up)
2. Dashboard `:8300` (KPIs visibles)
3. JSON `/api/overview`
4. (EVA) même dashboard via `10.3.16.179:8300`
5. Terminal `SMOKE TEST PASSED`

## Jalons dates (rappel)

- 12 oct. — rapport initial
- 13/14 oct. — présentation + quiz
- 21/22 oct. — soutenance finale

## Sécurité

- Ne pas committer `.env` avec vrais mots de passe
- Changer les secrets par défaut sur EVA si exposé au-delà du cours
