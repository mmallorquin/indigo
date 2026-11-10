"""Probador virtual con IA: genera una foto de la persona con la prenda puesta.

Usa FLUX.2 [pro] desplegado en el recurso de IA de Azure (se paga del crédito de Azure).
La app entra con su identidad administrada: no hay API key.

Qué se guarda y qué no:
- Prendas de la tienda, la foto de la modelo de ejemplo y los resultados de la modelo: en Blob Storage.
- La foto de una clienta y sus resultados: NUNCA. Viven en memoria mientras dura el pedido.
"""

import base64
import hashlib
import io
import json
import logging
import os

import httpx
from PIL import Image, ImageOps

log = logging.getLogger("indigo.probador")

TIPOS = {"arriba": "Parte de arriba", "abajo": "Parte de abajo", "entera": "Prenda entera"}
EN_INGLES = {"arriba": "a top", "abajo": "bottoms", "entera": "a full outfit"}
CARPETA = "probador/"
LADO_PERSONA = 1024  # px del lado más largo de la foto que se manda a la IA
LADO_PRENDA = 768


class ProbadorError(Exception):
    """Error que se le puede mostrar a la clienta. `tipo` le dice a la página qué hacer."""

    def __init__(self, mensaje: str, tipo: str, estado: int):
        super().__init__(mensaje)
        self.tipo, self.estado = tipo, estado


def preparar_imagen(datos: bytes, lado: int, multiplo: int = 1) -> bytes:
    """Lee la imagen, la endereza, la achica y la devuelve como JPEG sin metadatos (sin EXIF ni GPS)."""
    try:
        with Image.open(io.BytesIO(datos)) as original:
            img = ImageOps.exif_transpose(original)
            if img.mode in ("RGBA", "LA", "P"):  # fondo transparente -> blanco
                img = img.convert("RGBA")
                fondo = Image.new("RGBA", img.size, "white")
                img = Image.alpha_composite(fondo, img)
            img = img.convert("RGB")
            img.thumbnail((lado, lado))
            if multiplo > 1:  # el modelo pide medidas múltiplo de 16
                ancho, alto = (max(multiplo, d - d % multiplo) for d in img.size)
                img = img.resize((ancho, alto))
            salida = io.BytesIO()
            img.save(salida, format="JPEG", quality=90)
            return salida.getvalue()
    except Exception as e:
        raise ValueError("El archivo no es una imagen que se pueda leer") from e


def instruccion(tipos: list[str]) -> str:
    """El pedido al modelo. En inglés porque así sigue mejor las instrucciones."""
    refs = " and ".join(f"the garment from image {i} ({EN_INGLES[t]})" for i, t in enumerate(tipos, start=2))
    return (
        f"Virtual clothing try-on. Show the same person from image 1 now wearing {refs}, fitted naturally to "
        "their body. Keep the person's face, hair, skin tone, body shape, pose, framing and the background "
        "exactly the same as in image 1. Change only the clothes that the new garments replace; keep every "
        "other piece of clothing as it is. Reproduce the garment's real color, fabric and details. "
        "Photorealistic, natural fabric folds and lighting. Fully clothed."
    )


class ProbadorFlux:
    """FLUX.2 [pro] en Microsoft Foundry: una foto de la persona + hasta dos prendas -> una foto nueva."""

    def __init__(self, endpoint: str):
        from azure.identity import DefaultAzureCredential

        self._url = endpoint.rstrip("/") + "/providers/blackforestlabs/v1/flux-2-pro?api-version=preview"
        self._credencial = DefaultAzureCredential()

    def generar(self, persona: bytes, prendas: list[bytes], tipos: list[str]) -> tuple[bytes, dict]:
        with Image.open(io.BytesIO(persona)) as img:
            ancho, alto = img.size
        pedido = {"model": "FLUX.2-pro", "prompt": instruccion(tipos), "output_format": "jpeg",
                  "width": ancho, "height": alto, "input_image": base64.b64encode(persona).decode()}
        for i, prenda in enumerate(prendas, start=2):
            pedido[f"input_image_{i}"] = base64.b64encode(prenda).decode()

        token = self._credencial.get_token("https://cognitiveservices.azure.com/.default").token
        try:
            r = httpx.post(self._url, json=pedido, headers={"Authorization": f"Bearer {token}"}, timeout=150)
        except httpx.HTTPError as e:
            log.error("FLUX no respondió: %s", type(e).__name__)
            raise ProbadorError("El probador tardó demasiado. Probá de nuevo en un rato.", "falla", 502) from e

        if r.status_code == 400 and "content_safety" in r.text:
            raise ProbadorError("No pudimos usar esa imagen. Probá con otra foto, de cuerpo entero y con buena luz.",
                                "rechazada", 422)
        if r.status_code == 429:
            raise ProbadorError("Hay muchas pruebas al mismo tiempo. Esperá un minuto y probá de nuevo.", "falla", 503)
        if r.status_code != 200:
            log.error("FLUX respondió %s: %s", r.status_code, r.text[:300])
            raise ProbadorError("El probador no está respondiendo. Probá de nuevo en un rato.", "falla", 502)

        cuerpo = r.json()
        meta = cuerpo.get("request_meta") or {}
        if isinstance(meta, str):
            meta = json.loads(meta)
        return base64.b64decode(cuerpo["data"][0]["b64_json"]), meta


def crear_probador():
    """None = probador en pausa (sin endpoint, o apagado con PROBADOR_IA=0)."""
    endpoint = os.environ.get("FLUX_ENDPOINT")
    if not endpoint or os.environ.get("PROBADOR_IA", "1") == "0":
        return None
    return ProbadorFlux(endpoint)


# --- Catálogo de prendas (sobre el almacén: probador/prendas/<id>.json y .jpg) ---

def prendas(almacen) -> list[dict]:
    nombres = [n for n in almacen.listar(CARPETA + "prendas/") if n.endswith(".json")]
    return sorted((json.loads(almacen.leer(n)) for n in nombres), key=lambda p: p["creado"])


def prendas_visibles(almacen) -> list[dict]:
    """Lo que ven las clientas: las prendas de la tienda; si todavía no hay, las de ejemplo."""
    todas = prendas(almacen)
    return [p for p in todas if not p.get("ejemplo")] or todas


def guardar_prenda(almacen, prenda: dict, foto: bytes) -> None:
    almacen.escribir(f"{CARPETA}prendas/{prenda['id']}.jpg", preparar_imagen(foto, LADO_PRENDA), "image/jpeg")
    almacen.escribir(f"{CARPETA}prendas/{prenda['id']}.json", json.dumps(prenda, ensure_ascii=False).encode(),
                     "application/json")


def borrar_prenda(almacen, id_: str) -> None:
    for extension in (".jpg", ".json"):
        almacen.borrar(f"{CARPETA}prendas/{id_}{extension}")


def foto_prenda(almacen, id_: str) -> bytes | None:
    return almacen.leer(f"{CARPETA}prendas/{id_}.jpg") if id_.isalnum() else None


# --- Topes de uso: cada imagen generada cuesta plata y la página es pública ---

class Topes:
    """Cuenta las imágenes generadas por día (total y por IP) y las guarda en el almacén.

    Se guarda en Blob porque la app escala a cero: en memoria el contador se perdería al dormirse.
    La app corre con una sola réplica, así que alcanza con leer-sumar-escribir.
    """

    def __init__(self, almacen):
        self._almacen = almacen

    def _archivo(self, dia: str) -> str:
        return f"{CARPETA}uso/{dia}.json"

    def leer(self, dia: str) -> dict:
        datos = self._almacen.leer(self._archivo(dia))
        return json.loads(datos) if datos else {"total": 0, "ips": {}, "costo": 0}

    def reservar(self, dia: str, ip: str) -> None:
        """Suma una prueba ANTES de generar. Si ya se llegó al tope, corta con un mensaje."""
        uso = self.leer(dia)
        quien = hashlib.sha256(f"{dia}:{ip}".encode()).hexdigest()[:16]  # no guardamos la IP, solo su huella
        if uso["total"] >= int(os.environ.get("PROBADOR_TOPE_DIA", "40")):
            raise ProbadorError("El probador llegó a su límite por hoy. Mañana vuelve a estar disponible.",
                                "limite", 429)
        if uso["ips"].get(quien, 0) >= int(os.environ.get("PROBADOR_TOPE_IP", "8")):
            raise ProbadorError("Ya hiciste todas las pruebas de hoy. Mañana podés seguir.", "limite", 429)
        uso["total"] += 1
        uso["ips"][quien] = uso["ips"].get(quien, 0) + 1
        self._guardar(dia, uso)

    def devolver(self, dia: str, ip: str) -> None:
        """Si la generación falló, esa prueba no cuenta."""
        uso = self.leer(dia)
        quien = hashlib.sha256(f"{dia}:{ip}".encode()).hexdigest()[:16]
        uso["total"] = max(0, uso["total"] - 1)
        uso["ips"][quien] = max(0, uso["ips"].get(quien, 0) - 1)
        self._guardar(dia, uso)

    def anotar_costo(self, dia: str, costo: float) -> None:
        uso = self.leer(dia)
        uso["costo"] = round(uso.get("costo", 0) + costo, 2)
        self._guardar(dia, uso)

    def _guardar(self, dia: str, uso: dict) -> None:
        self._almacen.escribir(self._archivo(dia), json.dumps(uso).encode(), "application/json")
