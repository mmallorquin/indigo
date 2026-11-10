#!/usr/bin/env bash
# Se corre UNA vez en Cloud Shell (o cuando quieras cambiar la key o la clave).
# Guarda la API key de Anthropic y la clave de la app en Key Vault.
# La app las lee sola al arrancar (secretos.py), con su identidad administrada.
#
# Por qué no usamos "Key Vault references" de Container Apps: el entorno cae-indigo
# es de tipo "express" y no las soporta. Leerlas desde el código funciona en cualquier entorno.
set -euo pipefail

RG=rg-indigo
KV=kv-indigo-5dvav
APP=ca-indigo

read -r -s -p "API key de Anthropic (no se ve al escribir): " KEY; echo
read -r -s -p "Clave para entrar a la app (no se ve al escribir): " PASS; echo
az keyvault secret set --vault-name $KV -n anthropic-api-key --value "$KEY" -o none
az keyvault secret set --vault-name $KV -n app-password --value "$PASS" -o none
unset KEY PASS
echo "Secretos guardados en Key Vault."

# Le decimos a la app dónde está el Key Vault (esto no es un secreto)
az containerapp update -n $APP -g $RG -o none --set-env-vars \
  KEY_VAULT_URL=https://$KV.vault.azure.net/ ANTHROPIC_CHAT_MODEL=claude-haiku-4-5
echo "Listo. Si cambiás la key o la clave, reiniciá la app para que las vuelva a leer:"
echo "  az containerapp revision restart -n $APP -g $RG --revision \$(az containerapp show -n $APP -g $RG --query properties.latestRevisionName -o tsv)"
