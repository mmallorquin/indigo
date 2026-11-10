#!/usr/bin/env bash
# Infraestructura de Indigo en Azure (Azure for Students, Brazil South).
# Es el mismo script que se corrió en Cloud Shell el 2026-11-08.
# Para recrear todo desde cero: borrá rg-indigo y corré esto en Cloud Shell (Bash).
set -euo pipefail

LOC=brazilsouth          # regiones permitidas: canadacentral, mexicocentral, brazilsouth, spaincentral, northcentralus
RG=rg-indigo
SUF=$(tr -dc a-z0-9 </dev/urandom | head -c5)   # sufijo único: storage y key vault son nombres globales
ST=stindigo$SUF
KV=kv-indigo-$SUF
PG=psql-indigo-$SUF

az config set extension.use_dynamic_install=yes_without_prompt -o none
for p in Microsoft.App Microsoft.Storage Microsoft.KeyVault Microsoft.Insights \
         Microsoft.OperationalInsights Microsoft.DBforPostgreSQL Microsoft.CostManagement Microsoft.Consumption; do
  az provider register -n "$p" -o none
done

# 1. Grupo de recursos: todo Indigo vive acá; borrarlo borra todo.
az group create -n $RG -l $LOC --tags proyecto=indigo -o none

# 2. Storage: fotos y videos. Sin acceso público.
az storage account create -n $ST -g $RG -l $LOC --sku Standard_LRS --kind StorageV2 \
  --access-tier Hot --min-tls-version TLS1_2 --allow-blob-public-access false -o none
az storage container create --account-name $ST -n fotos --auth-mode key -o none

# 3. Key Vault: API keys (Anthropic, Telegram...). Permisos por RBAC.
az keyvault create -n $KV -g $RG -l $LOC --enable-rbac-authorization true --retention-days 7 -o none
ME=$(az ad signed-in-user show --query id -o tsv)
az role assignment create --assignee-object-id "$ME" --assignee-principal-type User \
  --role "Key Vault Secrets Officer" --scope "$(az keyvault show -n $KV --query id -o tsv)" -o none

# 4. Observabilidad: logs con tope de 0,15 GB/día (queda dentro de lo gratuito) + App Insights.
az monitor log-analytics workspace create -g $RG -n log-indigo -l $LOC --retention-time 30 --quota 0.15 -o none
az monitor app-insights component create -a appi-indigo -g $RG -l $LOC --workspace log-indigo \
  --kind web --application-type web -o none

# 5. Entorno de Container Apps (plan de consumo: sin apps corriendo no cobra).
LAW_ID=$(az monitor log-analytics workspace show -g $RG -n log-indigo --query customerId -o tsv)
LAW_KEY=$(az monitor log-analytics workspace get-shared-keys -g $RG -n log-indigo --query primarySharedKey -o tsv)
az containerapp env create -n cae-indigo -g $RG -l $LOC \
  --logs-workspace-id "$LAW_ID" --logs-workspace-key "$LAW_KEY" -o none

# 6. PostgreSQL B1MS (gratis 12 meses: 750 h/mes, 32 GB). Sin contraseña: solo login con tu cuenta (Entra ID).
az postgres flexible-server create -g $RG -n $PG -l $LOC --tier Burstable --sku-name Standard_B1ms \
  --storage-size 32 --storage-auto-grow Disabled --version 16 --zonal-resiliency Disabled \
  --backup-retention 7 --public-access None --microsoft-entra-auth Enabled --password-auth Disabled -y -o none
az postgres flexible-server microsoft-entra-admin create -g $RG -s $PG \
  -u "$(az ad signed-in-user show --query userPrincipalName -o tsv)" -i "$ME" -t User -o none
az postgres flexible-server db create -g $RG -s $PG -n indigo -o none

# 7. Presupuesto: USD 8/mes (≈ los USD 100 del año) con avisos por correo.
SUB=$(az account show --query id -o tsv)
EMAIL=$(az account show --query user.name -o tsv)
n(){ printf '"%s":{"enabled":true,"operator":"GreaterThan","threshold":%s,"thresholdType":"%s","contactEmails":["%s"]}' "$1" "$2" "$3" "$EMAIL"; }
cat > /tmp/budget.json <<EOF
{"properties":{"category":"Cost","amount":8,"timeGrain":"Monthly",
 "timePeriod":{"startDate":"$(date -u +%Y-%m-01)T00:00:00Z"},
 "notifications":{$(n real50 50 Actual),$(n real80 80 Actual),$(n real100 100 Actual),$(n pronostico100 100 Forecasted)}}}
EOF
az rest --method put --body @/tmp/budget.json -o none \
  --url "https://management.azure.com/subscriptions/$SUB/providers/Microsoft.Consumption/budgets/indigo-mensual?api-version=2023-05-01"

# 8. App: identidades, permisos y la Container App (con imagen de relleno hasta el primer deploy).
GH_REPO=${GH_REPO:-mmallorquin/indigo}
az identity create -n id-indigo-app -g $RG -l $LOC -o none
az identity create -n id-indigo-github -g $RG -l $LOC -o none
APP_PID=$(az identity show -n id-indigo-app -g $RG --query principalId -o tsv)
GH_PID=$(az identity show -n id-indigo-github -g $RG --query principalId -o tsv)
sleep 20  # las identidades nuevas tardan en propagarse
az role assignment create --assignee-object-id $APP_PID --assignee-principal-type ServicePrincipal \
  --role "Key Vault Secrets User" --scope "$(az keyvault show -n $KV --query id -o tsv)" -o none
az role assignment create --assignee-object-id $APP_PID --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" --scope "$(az storage account show -n $ST -g $RG --query id -o tsv)" -o none
az role assignment create --assignee-object-id $GH_PID --assignee-principal-type ServicePrincipal \
  --role Contributor --scope "$(az group show -n $RG --query id -o tsv)" -o none
az identity federated-credential create --identity-name id-indigo-github -g $RG -n github-main \
  --issuer https://token.actions.githubusercontent.com --subject "repo:$GH_REPO:ref:refs/heads/main" \
  --audiences api://AzureADTokenExchange -o none

APP_CID=$(az identity show -n id-indigo-app -g $RG --query clientId -o tsv)
az containerapp create -n ca-indigo -g $RG --environment cae-indigo \
  --image mcr.microsoft.com/k8se/quickstart:latest --target-port 8080 --ingress external \
  --min-replicas 0 --max-replicas 1 --cpu 0.5 --memory 1.0Gi \
  --env-vars AZURE_CLIENT_ID=$APP_CID AZURE_STORAGE_ACCOUNT=$ST -o none
sleep 60  # si falla con "managed identity bootstrap failed", esperá un minuto y repetí la línea siguiente
az containerapp identity assign -n ca-indigo -g $RG \
  --user-assigned "$(az identity show -n id-indigo-app -g $RG --query id -o tsv)" -o none
echo "Client ID para GitHub Actions: $(az identity show -n id-indigo-github -g $RG --query clientId -o tsv)"

echo "Listo: RG=$RG ST=$ST KV=$KV PG=$PG"
