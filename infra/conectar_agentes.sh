#!/usr/bin/env bash
# Se corre UNA vez desde la Terminal de tu Mac, después de:
#   1) hacer push de .github/workflows/agente.yml
#   2) instalar la app de Claude en el repo: https://github.com/apps/claude
#
# Qué hace:
#   - Le da a id-indigo-github permiso de LEER secretos del Key Vault, para que los
#     agentes traigan la API key de Anthropic sin guardarla en GitHub.
#   - Crea la etiqueta "agente", el issue de avisos y los issues del plan.
#   - Salen con la etiqueta (arrancan solos, uno detrás del otro): la tienda pública
#     y la Fábrica 1. Los demás dependen de esos; los etiquetás vos al mergear el anterior.
set -euo pipefail
cd "$(dirname "$0")/.."

RG=rg-indigo
KV=kv-indigo-5dvav
ID=id-indigo-github
REPO=mmallorquin/indigo
DIR=docs/agentes/fase1

command -v az >/dev/null || { echo "Falta Azure CLI: brew install azure-cli"; exit 1; }
command -v gh >/dev/null || { echo "Falta GitHub CLI: brew install gh && gh auth login"; exit 1; }
az account show -o none 2>/dev/null || az login -o none
gh auth status >/dev/null 2>&1 || gh auth login

# 1. Permiso de lectura de secretos para la identidad de GitHub
PID=$(az identity show -n "$ID" -g "$RG" --query principalId -o tsv)
KVID=$(az keyvault show -n "$KV" --query id -o tsv)
az role assignment create --assignee-object-id "$PID" --assignee-principal-type ServicePrincipal \
  --role "Key Vault Secrets User" --scope "$KVID" -o none 2>/dev/null || echo "(el permiso ya existía)"
echo "OK: $ID puede leer secretos de $KV (puede tardar unos minutos en aplicarse)"

# 2. Etiqueta e issues (no duplica si ya existen)
gh label create agente -R "$REPO" --color 5319E7 --description "Lo programa el agente y abre un PR" --force >/dev/null
crear() {  # titulo archivo [etiqueta]
  if [ "$(gh issue list -R "$REPO" --state all --search "\"$1\" in:title" --json number -q length)" != "0" ]; then
    echo "Ya existe: $1"; return
  fi
  gh issue create -R "$REPO" --title "$1" --body-file "$DIR/$2" ${3:+--label "$3"}
}
crear "Fábrica: avisos y mejoras" ../avisos.md
crear "Fábrica 1: textos, carrusel y stories por prenda" 06-fabrica-1-carrusel-stories.md agente
crear "Tienda pública: catálogo de prendas en /tienda" 01-tienda-publica.md agente
crear "Botón Pedir por WhatsApp en cada prenda" 02-pedir-whatsapp.md
crear "Probátela: abrir el probador con la prenda fijada" 03-probatela.md
crear "Medición del embudo en App Insights" 04-medicion.md
crear "Fábrica 2: Reel, revisión automática y vista del probador" 07-fabrica-2-reel-revision.md
crear "Agente de contenido semanal (fase 2)" 05-agente-contenido.md

echo
echo "Listo. El agente arrancó con la Fábrica 1 y después sigue con la tienda pública."
echo "Miralo en la pestaña Actions del repo. Cuando abra cada PR, revisalo y mergealo."
echo "Después: etiquetá 'Fábrica 2' y el botón de WhatsApp con 'agente', y corré Actions → fabrica."
