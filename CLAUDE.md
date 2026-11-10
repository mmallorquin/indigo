# Indigo — contexto para Claude Code

App web de la tienda de ropa Indigo (Ciudad del Este, Paraguay). Hoy hace una cosa:
subís la foto de una prenda y un agente de IA arma la ficha de producto.
El dueño del repo está aprendiendo orquestación de agentes e infraestructura: cuando hagas
un cambio, explicá en 2–3 líneas qué concepto aplica (sin tutoriales largos).

## Cómo está armado

- `agente_catalogo.py` — el agente (Microsoft Agent Framework + Claude). `crear_cliente()` es el único lugar que cambia según el modelo.
- `esquemas.py` — la salida estructurada (Pydantic). Reglas: `extra="forbid"`, sin valores por defecto, opcionales como `X | None`.
- `app/main.py` — FastAPI. Contraseña con HTTP Basic (`APP_PASSWORD`). Sin contraseña quedan solo `/salud`, `/static`, `/probador` y `/probador/prenda/<id>.png`.
- `secretos.py` — en Azure trae ANTHROPIC_API_KEY y APP_PASSWORD de Key Vault al arrancar (el entorno es *express*: no soporta Key Vault references).
- `almacen.py` — Blob Storage (Azure) o memoria (local). Las fichas van en la raíz del contenedor; todo lo del probador, bajo `probador/`.
- `probador.py` — probador virtual con IA: llama a FLUX.2 [pro] en el recurso de IA de Azure (`FLUX_ENDPOINT`) con la identidad administrada, sin API key. También el catálogo de prendas y los topes de gasto.
- `app/static/probador.js` — la página del probador. La foto de la clienta se envía solo si acepta el aviso.
- `app/plantillas/` — HTML con Jinja2. Tiene que verse bien en el celular.
- `app/static/` — `indigo.css`, logo y tipografías (Inter y Cormorant Garamond, licencia OFL). Se sirve sin contraseña.
- `catalogo.py` — versión de línea de comandos para procesar una carpeta de fotos.
- `marca.toml` — datos de la marca que leen los agentes. También define los colores de la app (`[identidad]`) y es lo que muestra la página `/marca`.

## Reglas del probador (no romper)

- La foto de una clienta y su resultado no se guardan nunca: ni en Blob, ni en disco, ni en logs. Hay un test que lo comprueba.
- Cada imagen generada cuesta plata y la página es pública: todo camino que genere tiene que pasar por `Topes.reservar`.
- Los resultados de la modelo de ejemplo sí se guardan (`probador/cache/`) para no pagarlos dos veces.
- Apagarlo sin desplegar: `PROBADOR_IA=0` en la Container App.

## Reglas

- Todo lo que ve el usuario va en español de Paraguay, con voseo.
- Correr `pytest -q` antes de dar un cambio por terminado. Los tests usan un Claude falso: no gastan API.
- Nunca escribir API keys ni contraseñas en el código ni en archivos del repo. Viven en Key Vault (`infra/conectar_secretos.sh`).
- Cambios chicos y enfocados. No agregar dependencias sin decir por qué.
- Si una dependencia nueva hace falta, agregarla con versión en `requirements.txt`.

## Despliegue

Cada push a `main` corre `.github/workflows/deploy.yml`: tests → imagen Docker en
`ghcr.io/mmallorquin/indigo` → `az containerapp update` en `ca-indigo` (rg-indigo, Brazil South).
Si los tests fallan, no se despliega nada.

## Correr local

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
APP_PASSWORD=prueba uvicorn app.main:app --reload --port 8080   # usa ANTHROPIC_API_KEY del entorno o .env
# o con Docker:
docker build -t indigo . && docker run --rm -p 8080:8080 --env-file .env -e APP_PASSWORD=prueba indigo
```
