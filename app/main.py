"""App web de Indigo: subís la foto de una prenda y el agente de catálogo arma la ficha.

Variables de entorno:
- APP_PASSWORD (obligatoria): contraseña para entrar. Sin ella la app no procesa nada.
- ANTHROPIC_API_KEY / ANTHROPIC_CHAT_MODEL: el modelo que usa el agente.
- KEY_VAULT_URL (en Azure): de ahí salen ANTHROPIC_API_KEY y APP_PASSWORD (ver secretos.py).
- Rutas sin contraseña: /salud, /static y el probador público (/probador, /probador/probar y sus imágenes).
- FLUX_ENDPOINT: recurso de IA de Azure que genera las fotos del probador. Sin esto, el probador queda en pausa.
- PROBADOR_IA=0 lo apaga sin desplegar. PROBADOR_TOPE_DIA y PROBADOR_TOPE_IP limitan el gasto (40 y 8).
- AZURE_STORAGE_ACCOUNT (opcional): si está, guarda fotos y fichas en Blob Storage.
  Si no, las guarda en memoria (se pierden al reiniciar; sirve para probar en tu Mac).
"""

import asyncio
import hashlib
import json
import os
import secrets
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
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
import probador as pb  # noqa: E402

MARCA = cargar_marca(RAIZ / "marca.toml")  # una sola lectura: la usan el agente y las plantillas

app = FastAPI(title=MARCA["nombre"])
# Logo, tipografías y CSS. Sin contraseña: son públicos y el navegador los guarda en caché.
app.mount("/static", StaticFiles(directory=RAIZ / "app" / "static"), name="static")
plantillas = Jinja2Templates(directory=RAIZ / "app" / "plantillas")
plantillas.env.globals.update(marca=MARCA, version=os.environ.get("APP_VERSION", "local"))
seguridad = HTTPBasic(realm="Indigo")
almacen = crear_almacen()
_agente = None
MAX_BYTES = 15 * 1024 * 1024


def agente():
    """El agente se crea la primera vez que se usa (así la app arranca aunque falte la API key)."""
    global _agente
    if _agente is None:
        _agente = crear_agente(MARCA, os.environ.get("MODEL_PROVIDER", "claude"))
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


@app.get("/marca", response_class=HTMLResponse, dependencies=[Depends(con_contrasena)])
async def ver_marca(request: Request):
    """La identidad de la marca tal como la leen los agentes (marca.toml)."""
    return plantillas.TemplateResponse(request, "marca.html")


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


# ---------------------------------------------------------------------------
# Probador virtual con IA
# Público: /probador, /probador/probar y las imágenes. Privado: /probador/prendas y /probador/modelo.
# ---------------------------------------------------------------------------

MAX_BYTES_PROBADOR = 10 * 1024 * 1024
MODELO = pb.CARPETA + "modelo.jpg"
probador_ia = pb.crear_probador()  # None = en pausa
_candado = asyncio.Lock()  # para que dos pedidos a la vez no se salteen el tope


def _hoy() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _ip(request: Request) -> str:
    """La IP que vio Azure. Va última en X-Forwarded-For; lo anterior lo puede inventar quien llama."""
    reenviado = request.headers.get("x-forwarded-for", "")
    return reenviado.split(",")[-1].strip() or (request.client.host if request.client else "desconocida")


@app.get("/probador", response_class=HTMLResponse)
async def probador(request: Request):
    prendas = await run_in_threadpool(pb.prendas_visibles, almacen)
    hay_modelo = await run_in_threadpool(almacen.leer, MODELO) is not None
    return plantillas.TemplateResponse(
        request, "probador.html",
        {"prendas": prendas, "pestanas": pb.PESTANAS, "activo": probador_ia is not None, "hay_modelo": hay_modelo},
    )


@app.get("/probador/modelo.jpg")
async def foto_modelo():
    datos = await run_in_threadpool(almacen.leer, MODELO)
    if datos is None:
        raise HTTPException(404, "Todavía no hay modelo de ejemplo")
    return Response(datos, media_type="image/jpeg", headers={"Cache-Control": "public, max-age=300"})


@app.get("/probador/prenda/{id_}.jpg")
async def foto_prenda(id_: str):
    datos = await run_in_threadpool(pb.foto_prenda, almacen, id_)
    if datos is None:
        raise HTTPException(404, "No existe esa prenda")
    return Response(datos, media_type="image/jpeg", headers={"Cache-Control": "public, max-age=86400"})


@app.post("/probador/probar")
async def probar(request: Request, prendas: str = Form(...), vista: str = Form("frente"), acepto: str = Form(""),
                 foto: UploadFile | None = File(None)):
    """Devuelve la foto de la persona con el conjunto puesto (JPEG), o un error en JSON.

    Siempre se parte de la foto original de la persona más todas las prendas: una sola generación por foto.
    Sin `foto` usa la modelo de ejemplo, y ese resultado se guarda para no pagarlo dos veces.
    Con `foto` (la de la clienta) no se guarda nada: ni la foto ni el resultado, en ninguna vista.
    """
    try:
        if probador_ia is None:
            raise pb.ProbadorError("El probador está en pausa por ahora. Escribinos y te ayudamos a elegir.",
                                   "pausado", 503)
        catalogo = {p["id"]: p for p in await run_in_threadpool(pb.prendas, almacen)}
        pedidas = list(dict.fromkeys(i for i in prendas.split(",") if i))
        elegidas = sorted((catalogo[i] for i in pedidas if i in catalogo), key=lambda p: pb.ORDEN[p["tipo"]])
        tipos = [p["tipo"] for p in elegidas]
        if len(elegidas) != len(pedidas) or not pb.conjunto_valido(tipos) or vista not in pb.VISTAS:
            raise pb.ProbadorError("Elegí una prenda por categoría. Un vestido reemplaza a la de arriba y a la de abajo.",
                                   "pedido", 400)

        guardado = None
        if foto is not None:
            if acepto != "si":
                raise pb.ProbadorError("Para usar tu foto tenés que aceptar el aviso.", "pedido", 400)
            datos = await foto.read()
            if len(datos) > MAX_BYTES_PROBADOR:
                raise pb.ProbadorError("La foto pesa más de 10 MB.", "pedido", 413)
        else:
            datos = await run_in_threadpool(almacen.leer, MODELO)
            if datos is None:
                raise pb.ProbadorError("Todavía no hay modelo de ejemplo. Probá con tu foto.", "pedido", 503)
            huella = hashlib.sha1(datos + f"{','.join(p['id'] for p in elegidas)}|{vista}".encode()).hexdigest()[:20]
            guardado = f"{pb.CARPETA}cache/{huella}.jpg"
            ya_hecha = await run_in_threadpool(almacen.leer, guardado)
            if ya_hecha:
                return Response(ya_hecha, media_type="image/jpeg")
        try:
            persona = await run_in_threadpool(pb.preparar_imagen, datos, pb.LADO_PERSONA, 16)
        except ValueError as e:
            raise pb.ProbadorError(str(e), "pedido", 400) from e
        # En la vista de espalda, si la tienda cargó la foto de atrás de una prenda, se manda esa.
        espaldas = [vista == "espalda" and bool(p.get("espalda")) for p in elegidas]
        fotos = [await run_in_threadpool(pb.foto_prenda, almacen, p["id"], atras) for p, atras in zip(elegidas, espaldas)]

        topes, dia, ip = pb.Topes(almacen), _hoy(), _ip(request)
        async with _candado:
            await run_in_threadpool(topes.reservar, dia, ip)
        try:
            imagen, meta = await run_in_threadpool(probador_ia.generar, persona, fotos, tipos, vista, espaldas)
        except Exception as e:
            async with _candado:
                await run_in_threadpool(topes.devolver, dia, ip)  # si falló, no cuenta
            if isinstance(e, pb.ProbadorError):
                raise
            pb.log.exception("Falló el probador")
            raise pb.ProbadorError("El probador no está respondiendo. Probá de nuevo en un rato.", "falla", 502) from e

        async with _candado:
            await run_in_threadpool(topes.anotar_costo, dia, float(meta.get("cost", 0) or 0))
        if guardado:
            await run_in_threadpool(almacen.escribir, guardado, imagen, "image/jpeg")
        return Response(imagen, media_type="image/jpeg", headers={"Cache-Control": "no-store"})
    except pb.ProbadorError as e:
        return JSONResponse({"error": str(e), "tipo": e.tipo}, status_code=e.estado)


async def _pagina_prendas(request: Request, error: str | None = None, estado: int = 200):
    prendas = await run_in_threadpool(pb.prendas, almacen)
    uso = await run_in_threadpool(pb.Topes(almacen).leer, _hoy())
    contexto = {
        "prendas": prendas, "tipos": pb.TIPOS, "error": error, "activo": probador_ia is not None,
        "hay_modelo": await run_in_threadpool(almacen.leer, MODELO) is not None,
        "uso": uso, "tope": int(os.environ.get("PROBADOR_TOPE_DIA", "40")),
    }
    return plantillas.TemplateResponse(request, "probador_prendas.html", contexto, status_code=estado)


@app.get("/probador/prendas", response_class=HTMLResponse, dependencies=[Depends(con_contrasena)])
async def prendas_admin(request: Request):
    return await _pagina_prendas(request)


@app.post("/probador/prendas", response_class=HTMLResponse, dependencies=[Depends(con_contrasena)])
async def subir_prenda(request: Request, nombre: str = Form(...), tipo: str = Form(...), foto: UploadFile = File(...),
                       espalda: UploadFile | None = File(None)):
    nombre = " ".join(nombre.split())[:60]
    datos = await foto.read()
    atras = (await espalda.read()) if espalda is not None else b""  # sin archivo elegido llega vacío
    prenda = {
        "id": uuid.uuid4().hex[:12],
        "nombre": nombre,
        "tipo": tipo,
        "creado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    try:
        if not nombre:
            raise ValueError("Falta el nombre de la prenda")
        if tipo not in pb.TIPOS:
            raise ValueError("Elegí la categoría de la prenda")
        if not datos:
            raise ValueError("No llegó ninguna foto")
        if max(len(datos), len(atras)) > MAX_BYTES_PROBADOR:
            raise ValueError("La foto pesa más de 10 MB")
        await run_in_threadpool(pb.guardar_prenda, almacen, prenda, datos, atras or None)
    except ValueError as e:
        return await _pagina_prendas(request, error=str(e), estado=400)
    return RedirectResponse("/probador/prendas", status_code=303)


@app.post("/probador/prendas/{id_}/borrar", dependencies=[Depends(con_contrasena)])
async def borrar_prenda(id_: str):
    if id_.isalnum():
        await run_in_threadpool(pb.borrar_prenda, almacen, id_)
    return RedirectResponse("/probador/prendas", status_code=303)


@app.post("/probador/modelo", response_class=HTMLResponse, dependencies=[Depends(con_contrasena)])
async def cambiar_modelo(request: Request, foto: UploadFile = File(...)):
    """Cambia la foto de la modelo de ejemplo que ven todas las clientas."""
    datos = await foto.read()
    try:
        if not datos or len(datos) > MAX_BYTES_PROBADOR:
            raise ValueError("Subí una foto de hasta 10 MB")
        imagen = await run_in_threadpool(pb.preparar_imagen, datos, pb.LADO_PERSONA, 16)
    except ValueError as e:
        return await _pagina_prendas(request, error=str(e), estado=400)
    await run_in_threadpool(almacen.escribir, MODELO, imagen, "image/jpeg")
    return RedirectResponse("/probador/prendas", status_code=303)
