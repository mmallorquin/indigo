# Infra de Indigo en Azure

Suscripción **Azure for Students** · región **Brazil South** · todo en el grupo `rg-indigo`.

| Recurso | Nombre | Para qué | Costo esperado |
|---|---|---|---|
| Grupo de recursos | `rg-indigo` | Contiene todo. Borrarlo borra todo. | 0 |
| Storage + contenedor `fotos` | `stindigo5dvav` | Fotos de prendas y videos | Centavos (5 GB gratis 12 meses) |
| Key Vault | `kv-indigo-5dvav` | API keys (Anthropic, Telegram) | Centavos |
| Log Analytics | `log-indigo` | Logs, con tope de 0,15 GB/día | 0 dentro de los 5 GB/mes gratis |
| Application Insights | `appi-indigo` | Trazas de cada agente (etapa 4) | 0 dentro de lo gratuito |
| Entorno Container Apps | `cae-indigo` | Donde van a correr los agentes | 0 sin apps; luego cuota gratuita mensual |
| PostgreSQL B1MS + base `indigo` | `psql-indigo-5dvav` | Productos, posts, aprobaciones | Gratis 12 meses (750 h, 32 GB); verificá en Cost Management |
| Identidad `id-indigo-app` | — | La app entra a Key Vault y Storage sin claves | 0 |
| Identidad `id-indigo-github` | — | GitHub Actions despliega sin contraseñas (OIDC) | 0 |
| Container App | `ca-indigo` | La app web en Docker; escala a cero | 0 dentro de la cuota gratuita |
| AI Services | `ai-indigo-5dvav` | Para gpt-5-mini (despliegue bloqueado por Azure, ver abajo) | 0 sin uso |
| Presupuesto | `indigo-mensual` | Aviso por correo al 50/80/100% de USD 8/mes | 0 |

## gpt-5-mini bloqueado

Al desplegarlo, Azure respondió *715-123420: unusual activity for your account*. Se resuelve con un ticket de soporte
(portal → Help + support → Create a support request) o reintentando más adelante:
`az cognitiveservices account deployment create -n ai-indigo-5dvav -g rg-indigo --deployment-name gpt-5-mini --model-name gpt-5-mini --model-version 2025-08-07 --model-format OpenAI --sku-name GlobalStandard --sku-capacity 50`

## Cosas que hacés vos (no las puede hacer Claude)

**Cargar tu API key de Anthropic en Key Vault** (desde Cloud Shell, así no queda en ningún archivo):

```bash
read -s -p "API key: " K; az keyvault secret set --vault-name kv-indigo-5dvav -n anthropic-api-key --value "$K" -o none; unset K
```

**Conectarte a PostgreSQL** (no tiene contraseña; entrás con tu cuenta):

```bash
# 1. Permitir tu IP actual
az postgres flexible-server firewall-rule create -g rg-indigo -n psql-indigo-5dvav -r mi-ip \
  --start-ip-address $(curl -s ifconfig.me) --end-ip-address $(curl -s ifconfig.me)
# 2. Entrar con un token de Entra como contraseña
export PGPASSWORD=$(az account get-access-token --resource-type oss-rdbms --query accessToken -o tsv)
psql "host=psql-indigo-5dvav.postgres.database.azure.com dbname=indigo user=marco.mallorquin@fpune.edu.py sslmode=require"
```

## Para ahorrar crédito

- PostgreSQL no se usa hasta la etapa 3: podés apagarlo con
  `az postgres flexible-server stop -g rg-indigo -n psql-indigo-5dvav` (Azure lo vuelve a prender solo a los 7 días).
- Crédito restante: https://www.microsoftazuresponsorships.com/
- Recrear todo desde cero: `crear_infra.sh`.
