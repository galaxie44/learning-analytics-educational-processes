# Livrables prêts à rendre

Dossier généré automatiquement pour Moodle / soutenance.

| Fichier | Usage |
|---------|--------|
| `Presentation-Learning-Analytics.pptx` | Slides soutenance (ouvrir dans PowerPoint / Google Slides) |
| `Rapport-Learning-Analytics.docx` | Rapport à coller / adapter au template Moodle |

Sources texte :
- `docs/rapport/presentation-complet.md`
- `docs/rapport/rapport-projet-complet.md`
- `docs/SCRIPT-ORAL-2MIN.md`
- `docs/EXPLICATION-SIMPLE.md`

Captures techniques : `docs/captures/`

Régénérer :

```powershell
python scripts\generate-pptx.py
python scripts\generate-docx.py
python scripts\export-demo-artifacts.py
```
