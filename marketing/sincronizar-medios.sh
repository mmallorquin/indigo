#!/bin/bash
# Sincroniza videos y fotos de Indigo con Azure Storage (cuenta stindigo5dvav, contenedor "medios").
# Los medios no van a GitHub (pesan GB); viven en tu Mac y en Azure.
#
#   bash sincronizar-medios.sh subir   # Mac -> Azure (nunca borra nada en Azure)
#   bash sincronizar-medios.sh bajar   # Azure -> Mac (no pisa archivos que ya tenes)
#
# Requiere Azure CLI en la Mac (brew install azure-cli). La primera vez abre el navegador para az login.
set -euo pipefail
ST=stindigo5dvav; RG=rg-indigo; C=medios
# Carpeta con los videos y fotos (ignorados por git).
DIR="${INDIGO_MEDIOS:-$HOME/vibe_coding/indigo/marketing}"

command -v az >/dev/null || { echo "Falta Azure CLI. Instalala con: brew install azure-cli"; exit 1; }
az account show -o none 2>/dev/null || az login -o none
KEY=$(az storage account keys list -n "$ST" -g "$RG" --query '[0].value' -o tsv)
az storage container create --account-name "$ST" --account-key "$KEY" -n "$C" -o none

# Carpetas que no se suben: dependencias y herramientas que se pueden volver a instalar
EXCL_PATH=$(cd "$DIR" && find . \( -name node_modules -o -name .git -o -name .cache -o -name python -path '*/work/python' \) -type d -prune -print | sed 's|^\./||' | paste -sd ';' -)

case "${1:-}" in
  subir)
    az storage blob sync --account-name "$ST" --account-key "$KEY" -c "$C" -s "$DIR" \
      --delete-destination false --exclude-pattern '.DS_Store;*.pyc' --exclude-path "$EXCL_PATH"
    ;;
  bajar)
    az storage blob download-batch --account-name "$ST" --account-key "$KEY" -s "$C" -d "$DIR" \
      --overwrite false -o none
    ;;
  *) echo "Uso: bash $0 subir|bajar"; exit 1 ;;
esac
echo "Listo ($1): $DIR <-> $ST/$C"
