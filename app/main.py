"""App web de Indigo: subís la foto de una prenda y el agente de catálogo arma la ficha.

Variables de entorno:
- APP_PASSWORD (obligatoria): contraseña para entrar. Sin ella la app no procesa nada.
- ANTHROPIC_API_KEY / ANTHROPIC_CHAT_MODEL: el modelo que usa el agente.
- KEY_VAULT_URL (en Azure): de ahí salen ANTHROPIC_API_KEY y APP_PASSWORD (ver secretos.py).
- AZURE_STORAGE_ACCOUNT (opcional): si está, guarda fotos y fichas en Blob Storage.
  Si no, las guarda en memoria (se pierden al reiniciar; sirve para probar en tu Mac).
"""

import json
import os
import secrets
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(RAIZ / ".env")  # en tu Mac; en Azure no hay .env y las variables vienen de la Container App

from secretos import cargar_desde_key_vault  # noqa: E402

cargar_desde_key_vault()  # en Azure: API key y clave desde Key Vault con la identidad administrada

from agente_catalogo import cargar_marca, crear_agente, fichar  # noqa: E402
from almacen import crear_almacen  # noqa: E402

app = FastAPI(title="Indigo")
plantillas = Jinja2Templates(directory=RAIZ / "app" / "plantillas")
seguridad = HTTPBasic(realm="Indigo")
almacen = crear_almacen()
_agente = None
MAX_BYTES = 15 * 1024 * 1024


def agente():
    """El agente se crea la primera vez que se usa (así la app arranca aunque falte la API key)."""
    global _agente
    if _agente is None:
        _agente = crear_agente(cargar_marca(RAIZ / "marca.toml"), os.environ.get("MODEL_PROVIDER", "claude"))
    return _agente


def con_contrasena(cred: HTTPBasicCredentials = Depends(seguridad)) -> None:
    esperada = os.environ.get("APP_PASSWORD", "")
    if not esperada:
        raise HTTPException(503, "Falta configurar APP_PASSWORD")
    if not secrets.compare_digest(cred.password.encode(), esperada.encode()):
        raise HTTPException(401, "Contraseña incorrecta", headers={"WWW-Authenticate": "Basic"})


@app.get("/salud")
def salud():
    """Para que Azure sepa que la app está viva. Sin contraseña a propósito."""
    return {"estado": "ok", "version": os.environ.get("APP_VERSION", "local")}


@app.get("/", response_class=HTMLResponse, dependencies=[Depends(con_contrasena)])
async def inicio(request: Request):
    recientes = await run_in_threadpool(almacen.recientes, 12)
    return plantillas.TemplateResponse(request, "inicio.html", {"recientes": recientes})


@app.post("/fichar", response_class=HTMLResponse, dependencies=[Depends(con_contrasena)])
async def nueva_ficha(request: Request, foto: UploadFile = File(...)):
    datos = await foto.read()
    if not datos:
        raise HTTPException(400, "No llegó ninguna foto")
    if len(datos) > MAX_BYTES:
        raise HTTPException(413, "La foto pesa más de 15 MB")

    try:
        ficha, uso = await fichar(agente(), datos, foto.filename)
    except Exception as e:  # mostramos el error en la página en vez de un 500 mudo
        return plantillas.TemplateResponse(
            request, "inicio.html", {"recientes": [], "error": str(e)}, status_code=502
        )

    registro = {
        "id": uuid.uuid4().hex[:12],
        "creado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "archivo": foto.filename,
        "tokens": uso,
        "ficha": ficha.model_dump(),
    }
    await run_in_threadpool(almacen.guardar, registro, datos)
    return plantillas.TemplateResponse(request, "ficha.html", {"r": registro})


@app.get("/ficha/{id_}", response_class=HTMLResponse, dependencies=[Depends(con_contrasena)])
async def ver_ficha(request: Request, id_: str):
    registro = await run_in_threadpool(almacen.ficha, id_)
    if registro is None:
        raise HTTPException(404, "No existe esa ficha")
    return plantillas.TemplateResponse(request, "ficha.html", {"r": registro})


@app.get("/ficha/{id_}/json", dependencies=[Depends(con_contrasena)])
async def ficha_json(id_: str):
    registro = await run_in_threadpool(almacen.ficha, id_)
    if registro is None:
        raise HTTPException(404, "No existe esa ficha")
    return Response(json.dumps(registro, ensure_ascii=False, indent=2), media_type="application/json")


@app.get("/foto/{id_}", dependencies=[Depends(con_contrasena)])
async def ver_foto(id_: str):
    datos = await run_in_threadpool(almacen.foto, id_)
    if datos is None:
        raise HTTPException(404, "No existe esa foto")
    return Response(datos, media_type="image/jpeg")
