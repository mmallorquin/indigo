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

# Nombre largo (para cargar la prenda) y pestaña corta (para la clienta). El orden es el de las pestañas.
TIPOS = {"arriba": "Parte de arriba", "abajo": "Parte de abajo", "entera": "Prenda entera (vestido, enterito)",
         "cinto": "Cinto", "accesorio": "Accesorio"}
PESTANAS = {"arriba": "Arriba", "abajo": "Abajo", "entera": "Enteras", "cinto": "Cintos", "accesorio": "Accesorios"}
EN_INGLES = {"arriba": "a top", "abajo": "bottoms", "entera": "a full outfit", "cinto": "a belt",
             "accesorio": "an accessory"}
ORDEN = {"arriba": 0, "entera": 1, "abajo": 2, "cinto": 3, "accesorio": 4}  # orden fijo en el pedido a la IA
VISTAS = ("frente", "perfil", "espalda")
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


def conjunto_valido(tipos: list[str]) -> bool:
    """Una prenda por categoría; una prenda entera no va junto con una de arriba o una de abajo."""
    return (0 < len(tipos) == len(set(tipos))
            and not ("entera" in tipos and {"arriba", "abajo"} & set(tipos)))


def instruccion(tipos: list[str], vista: str = "frente", espaldas: list[bool] | None = None) -> str:
    """El pedido al modelo. En inglés porque así sigue mejor las instrucciones."""
    espaldas = espaldas or [False] * len(tipos)
    refs = " and ".join(
        f"the garment from image {i} ({EN_INGLES[t]}{', photographed from the back' if atras else ''})"
        for i, (t, atras) in enumerate(zip(tipos, espaldas), start=2)
    )
    comun = (
        f"Virtual clothing try-on. Show the same person from image 1 now wearing {refs}, fitted naturally to "
        "their body. Keep the person's face, hair, skin tone and body shape, and the same background and "
        "lighting as in image 1. Change only the clothes that the new garments replace; keep every other piece "
        "of clothing as it is. Reproduce each garment's real color, fabric and details. Photorealistic, natural "
        "fabric folds. Fully clothed."
    )
    encuadre = {
        "frente": " Keep the pose and framing exactly as in image 1.",
        "perfil": " Show the person turned 90 degrees in a full-body side profile view, standing straight, "
                  "head to feet visible, at the same distance from the camera.",
        "espalda": " Show the person from behind in a full-body back view, standing straight, head to feet "
                   "visible, at the same distance from the camera.",
    }
    return comun + encuadre[vista]


class ProbadorFlux:
    """FLUX.2 [pro] en Microsoft Foundry: la foto de la persona + las prendas del conjunto -> una foto nueva.

    Acepta hasta 8 imágenes por pedido; acá van como mucho 5 (la persona y 4 prendas).
    """

    def __init__(self, endpoint: str):
        from azure.identity import DefaultAzureCredential

        self._url = endpoint.rstrip("/") + "/providers/blackforestlabs/v1/flux-2-pro?api-version=preview"
        self._credencial = DefaultAzureCredential()

    def generar(self, persona: bytes, prendas: list[bytes], tipos: list[str], vista: str = "frente",
                espaldas: list[bool] | None = None) -> tuple[bytes, dict]:
        with Image.open(io.BytesIO(persona)) as img:
            ancho, alto = img.size
        pedido = {"model": "FLUX.2-pro", "prompt": instruccion(tipos, vista, espaldas), "output_format": "jpeg",
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


def guardar_prenda(almacen, prenda: dict, foto: bytes, espalda: bytes | None = None) -> None:
    base = f"{CARPETA}prendas/{prenda['id']}"
    almacen.escribir(f"{base}.jpg", preparar_imagen(foto, LADO_PRENDA), "image/jpeg")
    if espalda:  # foto de atrás de la prenda: se usa solo para la vista "Espalda"
        almacen.escribir(f"{base}_espalda.jpg", preparar_imagen(espalda, LADO_PRENDA), "image/jpeg")
        prenda = {**prenda, "espalda": True}
    almacen.escribir(f"{base}.json", json.dumps(prenda, ensure_ascii=False).encode(), "application/json")


def borrar_prenda(almacen, id_: str) -> None:
    for final in (".jpg", "_espalda.jpg", ".json"):
        almacen.borrar(f"{CARPETA}prendas/{id_}{final}")


def foto_prenda(almacen, id_: str, espalda: bool = False) -> bytes | None:
    if not id_.isalnum():
        return None
    return almacen.leer(f"{CARPETA}prendas/{id_}{'_espalda' if espalda else ''}.jpg")


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
