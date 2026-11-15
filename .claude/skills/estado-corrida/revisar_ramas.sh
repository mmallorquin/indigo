#!/usr/bin/env bash
# Corre los tests en cada rama operador/* abierta y avisa qué pares chocan al mergear.
# Uso: bash .claude/skills/estado-corrida/revisar_ramas.sh   (desde la raíz del repo)
set -u
cd "$(git rev-parse --show-toplevel)"
git fetch -q --prune origin '+refs/heads/*:refs/remotes/origin/*'
ramas=$(git for-each-ref --format='%(refname:short)' 'refs/remotes/origin/operador/*' | while read -r r; do
  [ -n "$(git log --oneline origin/main.."$r" | head -1)" ] && echo "$r"; done)
[ -z "$ramas" ] && { echo "No hay ramas operador/* sin mergear."; exit 0; }

dir=$(mktemp -d)
for r in $ramas; do
  git worktree add -q --detach "$dir/wt" "$r" >/dev/null 2>&1
  res=$(cd "$dir/wt" && python3 -m pytest -q 2>&1 | tail -1)
  echo "$r -> $res | archivos: $(git diff --name-only origin/main..."$r" | tr '\n' ' ')"
  git worktree remove --force "$dir/wt"
done

echo "--- Choques entre ramas (si se mergea una, la otra queda en conflicto)"
set -- $ramas
while [ $# -gt 1 ]; do
  a=$1; shift
  for b in "$@"; do
    base=$(git merge-base "$a" "$b")
    if git merge-tree "$base" "$a" "$b" | grep -q '^<<<<<<<\|^+<<<<<<<'; then
      echo "CHOCAN: $a y $b -> $(git diff --name-only "$base" "$a" | sort | comm -12 - <(git diff --name-only "$base" "$b" | sort) | tr '\n' ' ')"
    fi
  done
done
rm -rf "$dir"
