# Indigo — contexto para Claude Code

App web de la tienda de ropa Indigo (Ciudad del Este, Paraguay). Hoy hace una cosa:
subís la foto de una prenda y un agente de IA arma la ficha de producto.
El dueño del repo está aprendiendo orquestación de agentes e infraestructura: cuando hagas
un cambio, explicá en 2–3 líneas qué concepto aplica (sin tutoriales largos).

## Cómo está armado

- `agente_catalogo.py` — el agente (Microsoft Agent Framework + Claude). `crear_cliente()` es el único lugar que cambia según el modelo.
- `esquemas.py` — la salida estructurada (Pydantic). Reglas: `extra="forbid"`, sin valores por defecto, opcionales como `X | None`.
- `app/main.py` — FastAPI. Contraseña con HTTP Basic (`APP_PASSWORD`). `/salud` queda sin contraseña.
- `secretos.py` — en Azure trae ANTHROPIC_API_KEY y APP_PASSWORD de Key Vault al arrancar (el entorno es *express*: no soporta Key Vault references).
- `almacen.py` — fotos y fichas en Blob Storage (Azure) o en memoria (local).
- `app/plantillas/` — HTML con Jinja2. Tiene que verse bien en el celular.
- `catalogo.py` — versión de línea de comandos para procesar una carpeta de fotos.
- `marca.toml` — datos de la marca que leen los agentes.

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
