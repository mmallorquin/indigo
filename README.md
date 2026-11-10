# Indigo

App web de la tienda: subís la foto de una prenda y un agente de IA arma la ficha de producto.
Corre en Docker sobre Azure Container Apps y se actualiza sola con cada `git push`.

```
 Tu Mac                     GitHub                         Azure (Brazil South, rg-indigo)
┌──────────────┐  push   ┌──────────────────────┐ deploy  ┌─────────────────────────────────┐
│ Claude Code  │ ──────> │ repo privado (backup) │ ──────> │ ca-indigo  (tu app en Docker)    │
│ edita código │         │ Actions: test→imagen  │  OIDC   │   ├─ Key Vault: API key, clave   │
│ con prompts  │         │ ghcr.io: imágenes     │         │   └─ Storage: fotos y fichas     │
└──────────────┘         └──────────────────────┘         └─────────────────────────────────┘
```

## Primera vez (unos 15 minutos)

**1. Subir el código a GitHub** (desde tu Mac, en esta carpeta):

```bash
brew install gh && gh auth login        # si no tenés gh
git init -b main && git add . && git commit -m "Indigo: primera versión"
gh repo create mmallorquin/indigo --private --source . --push
```

Eso dispara el primer despliegue. Miralo en la pestaña **Actions** del repo.
Va a fallar en el último paso: es normal, faltan los pasos 2 y 3.

**2. Hacer pública la imagen** (no el código): en GitHub → tu perfil → **Packages** → `indigo` →
**Package settings** → **Change visibility** → Public.
Así Azure la puede descargar sin contraseña. La imagen no tiene secretos: las claves viven en Key Vault.

**3. Cargar los secretos** — ✅ ya hecho (API key y clave guardadas en Key Vault).
Para cambiarlos más adelante: subí `infra/conectar_secretos.sh` a [Cloud Shell](https://shell.azure.com)
(*Manage files → Upload*) y corré `bash conectar_secretos.sh`. La app los lee al arrancar (`secretos.py`).

**4. Volver a desplegar:** en GitHub → **Actions** → *deploy* → **Run workflow**.
Al terminar, el resumen muestra la URL. Entrás con cualquier usuario y la contraseña del paso 3.

## El día a día: cambiar la app con prompts

```bash
cd indigo
claude                                   # abrís Claude Code en la carpeta
> "Agregá un botón para copiar las palabras clave como hashtags"
pytest -q                                # Claude Code ya lo corre, pero revisalo
git add . && git commit -m "Copiar hashtags" && git push
```

En 3–4 minutos está en Azure. Si los tests fallan, no se despliega nada.
`CLAUDE.md` le explica a Claude Code cómo está armado el proyecto, así no tenés que repetirlo.

**Volver atrás** si algo salió mal: `git revert HEAD && git push` (despliega la versión anterior).

## Respaldo

- **GitHub** guarda todo el historial. Tu Mac tiene una copia completa.
- Copia extra en un disco o en iCloud, en un solo archivo:
  `git bundle create ~/Backups/indigo-$(date +%F).bundle --all`
  (para recuperar: `git clone indigo-AAAA-MM-DD.bundle indigo`).
- Las fotos y fichas están en el Storage de Azure (`stindigo5dvav`, contenedor `fotos`).

## Probar en tu Mac

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env                     # pegá tu ANTHROPIC_API_KEY y poné una APP_PASSWORD
uvicorn app.main:app --reload --port 8080   # abrí http://localhost:8080
```

Con Docker (Docker Desktop u OrbStack): `docker build -t indigo . && docker run --rm -p 8080:8080 --env-file .env indigo`

Procesar una carpeta de fotos sin la web: `python catalogo.py fotos/`

## Qué vas aprendiendo en cada pieza

| Pieza | Concepto |
|---|---|
| `Dockerfile` | Empaquetar la app con todo lo que necesita; capas y caché |
| `deploy.yml` | CI/CD: probar, construir y desplegar en cada cambio |
| OIDC (`azure/login`) | GitHub entra a Azure sin contraseñas guardadas |
| Identidad administrada | La app lee Key Vault y Storage sin claves en el código |
| Container Apps | Escala a cero cuando nadie la usa (no gasta) |
| `/salud` | Cómo la plataforma sabe si tu app está viva |
| `esquemas.py` | Salida estructurada: la base para encadenar agentes |

## Costos

Azure: casi cero (Container Apps escala a cero; Storage centavos). La alerta de presupuesto avisa al 50/80/100% de USD 8/mes.
Claude: menos de 1 centavo por ficha con Haiku.
Detalle de toda la infraestructura en `infra/README.md`.
