---
name: preparar-pr
description: Usala cada vez que vayas a abrir un PR del operador (tarea de un issue o auto-mejora): nombre de rama, tests, descripción, y si lo podés mergear vos o lo tiene que aprobar Marco.
---

# Preparar un PR

1. Rama desde `main` actualizado:
   `git fetch -q origin main && git switch -c operador/<numero>-<slug> origin/main` (auto-mejora: `operador/auto-mejora-AAAA-MM-DD`).
2. Antes de commitear, revisá la zona prohibida (tiene que salir vacío):
   `git diff --name-only origin/main | grep -E '^(secretos\.py|infra/|\.github/|\.env)'`
3. Tests: `python3 -m pip install -q -r requirements-dev.txt && python3 -m pytest -q` hasta que pase. Nunca borres ni aflojes tests (privacidad del probador, `Topes`).
4. Si tocás `docs/campanas/PROGRESO.md` u otro archivo compartido, mirá con `revisar_ramas.sh` (skill estado-corrida) si choca con otro PR abierto; si choca, mejor no tocarlo y poner la novedad en la descripción del PR.
5. Commit y push: `git push -u origin <rama>`. Si falla por red, reintentá hasta 4 veces (2, 4, 8, 16 s).
6. PR: `gh pr create --base main --title "..." --body-file /tmp/pr.md`. Cuerpo:
   ```
   ## Qué cambió
   ## Cómo probarlo
   ## Concepto (2–3 líneas)
   Closes #<numero>
   ```
7. ¿Lo mergeo yo? Solo si es mío, los checks están en verde y TODOS los archivos están en `marketing/`, `docs/` o `.claude/skills/`:
   `git diff --name-only origin/main...HEAD | grep -vE '^(marketing/|docs/|\.claude/skills/)'` tiene que salir vacío.
   Entonces `gh pr checks <n> --watch` y `gh pr merge <n> --squash --delete-branch`. Si no, queda para Marco y va en el informe.
8. Sin GH_TOKEN: hacé push igual y poné en el informe el link `https://github.com/mmallorquin/indigo/pull/new/<rama>`.
