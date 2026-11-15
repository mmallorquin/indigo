---
name: estado-corrida
description: Usala al empezar cada corrida del operador (paso 1 "Mirá el estado") para ver issues, PR, Actions y avisos, correr los tests de las ramas operador/* y detectar PR que chocan entre sí. Funciona con gh autenticado y también sin GH_TOKEN (lee las páginas públicas).
---

# Estado de la corrida

## 1. Herramientas
- Python: usá siempre `python3 -m pip` y `python3 -m pytest`. El `pip` suelto apunta al Python del sistema y deja los módulos donde pytest no los ve.
- `gh`: si falta, `apt-get install -y -q gh` (si no lo encuentra, antes `apt-get update -q`).
- Auth: `[ -n "$GH_TOKEN" ] && echo hay-token` (nunca imprimas el valor). Sin token, `gh` no sirve y la API pública suele estar sin cupo (60 pedidos/hora por IP compartida).

## 2. Con gh autenticado
```bash
gh issue list --state open -L 50
gh pr list --state open --json number,title,headRefName,statusCheckRollup \
  --jq '.[] | "#\(.number) \(.headRefName) \(.title) checks=\(.statusCheckRollup|map(.conclusion // .status)|join(","))"'
gh run list -L 15
gh issue view 3 --comments --json comments --jq '.comments[-10:][] | "--- \(.author.login) \(.createdAt)\n\(.body)"'
```

## 3. Sin GH_TOKEN (solo lectura)
```bash
python3 .claude/skills/estado-corrida/estado_sin_gh.py   # issues, PR, Actions y comentarios del #3
```
Sin token NO podés: abrir PR, comentar, mergear ni disparar workflows. Sí podés hacer push (git usa su propio helper). Dejá el informe en `/mnt/session/outputs/` y en la respuesta final, con los links `https://github.com/<repo>/pull/new/<rama>`.

## 4. Ramas y choques (siempre)
```bash
bash .claude/skills/estado-corrida/revisar_ramas.sh
```
Corre `pytest` en cada rama `operador/*` sin mergear (en un worktree aparte, no toca tu copia) y lista los pares que chocan. Si dos PR chocan, decile a Marco en qué orden mergear; después del primer merge, rebaseá el otro en su misma rama.

## 5. Decidir la tarea
- Issue elegible = abierto, sin PR, y con todo su "Depende de:" ya en `main` (`git log origin/main --oneline | grep` o mirar que el archivo/ruta exista en main).
- Si ninguno es elegible: no apiles ramas sobre PR sin mergear. Revisá los PR abiertos contra su issue (`docs/agentes/fase1/`) y dedicá la corrida a la auto-mejora.
