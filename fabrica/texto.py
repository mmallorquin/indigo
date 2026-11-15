"""Textos con Claude (Sonnet) por HTTP, con tope de gasto. Los datos duros (precio, talles...) NO los escribe Claude."""

import json
import os
import re
from datetime import datetime

import httpx

API = "https://api.anthropic.com/v1/messages"
MODELO = "claude-sonnet-5-5"
PRECIO_USD_POR_MILLON = (2.0, 10.0)  # entrada, salida (igual que marketing/api-credito/indigo_api.py)
MAX_SALIDA = 2000

REGLAS = """Sos el equipo de contenido de Indigo (@indigopy_), tienda de ropa femenina de Ciudad del Este, Paraguay.
Escribís en español de Paraguay con voseo, cercano y concreto, sin exagerar.
REGLAS DURAS: no inventes precio, talle, color exacto, tela, stock, plazo, envío ni condiciones de cambio.
No escribas cifras de dinero. Nada de escasez ni urgencia ("últimas unidades", "solo hoy"). Sin testimonios.
Una sola llamada a la acción: pedir por WhatsApp. Respondé SOLO con JSON válido."""

PEDIDO = """Prenda: {nombre} (categoría: {categoria}). Cantidad de fotos: {n_fotos}.
Devolvé un JSON con estas claves exactas:
"gancho_puesto": frase corta (máx 7 palabras) para el gancho "Así queda puesto",
"gancho_precio": frase corta (máx 7 palabras) para el gancho "Precio y talles disponibles",
"detalle": una frase (máx 14 palabras) sobre lo que se VE en la prenda,
"combinar": lista de 3 ideas cortas (máx 8 palabras cada una) de con qué combinarla,
"caption_instagram": 2 a 4 líneas, termina con una sola llamada a pedir por WhatsApp,
"caption_tiktok": 1 a 2 líneas,
"hashtags": lista de 10 hashtags en minúscula con #,
"alt": lista de 8 textos alternativos de imágenes (portada, detalle, combinar, talles, cierre, story 1, 2 y 3), cada uno describe lo que se ve."""

PROHIBIDO = re.compile(r"(últim[ao]s?\s+unidades|solo\s+hoy|quedan\s+\d|stock\s+limitado|[₲$]|\bgs\b|guaran[ií]es|\d{2,3}[.,]\d{3})", re.I)


class TopeSuperado(Exception):
    pass


class Gasto:
    def __init__(self, tope_usd: float):
        self.tope, self.total, self.llamadas = tope_usd, 0.0, []

    @staticmethod
    def estimar(chars_entrada: int, max_salida: int) -> float:
        tokens_in = chars_entrada // 3 + 1
        return (tokens_in * PRECIO_USD_POR_MILLON[0] + max_salida * PRECIO_USD_POR_MILLON[1]) / 1e6

    def reservar(self, chars_entrada: int, max_salida: int) -> None:
        """Antes de cada llamada: si el peor caso pasa el tope, no se llama."""
        if self.total + self.estimar(chars_entrada, max_salida) > self.tope:
            raise TopeSuperado(f"Se llegó al tope de US$ {self.tope:.2f}")
        corte = os.environ.get("FABRICA_CORTE")
        if corte and datetime.now().astimezone() >= datetime.fromisoformat(corte):
            raise TopeSuperado(f"Pasó la hora de corte ({corte})")

    def anotar(self, sku: str, tokens_in: int, tokens_out: int) -> None:
        usd = (tokens_in * PRECIO_USD_POR_MILLON[0] + tokens_out * PRECIO_USD_POR_MILLON[1]) / 1e6
        self.total += usd
        self.llamadas.append({"sku": sku, "tokens_in": tokens_in, "tokens_out": tokens_out, "usd": round(usd, 5)})


def llamar_claude(sistema: str, pedido: str) -> tuple[str, int, int]:
    """Devuelve (texto, tokens_entrada, tokens_salida). La key llega en ANTHROPIC_API_KEY."""
    r = httpx.post(API, timeout=120, headers={
        "x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"},
        json={"model": MODELO, "max_tokens": MAX_SALIDA, "system": sistema,
              "messages": [{"role": "user", "content": pedido}]})
    r.raise_for_status()
    d = r.json()
    return d["content"][0]["text"], d["usage"]["input_tokens"], d["usage"]["output_tokens"]


def _validar(d: dict) -> dict:
    claves = {"gancho_puesto": str, "gancho_precio": str, "detalle": str, "combinar": list,
              "caption_instagram": str, "caption_tiktok": str, "hashtags": list, "alt": list}
    for k, tipo in claves.items():
        if not isinstance(d.get(k), tipo):
            raise ValueError(f"falta o es inválido: {k}")
    if len(d["combinar"]) < 3 or len(d["hashtags"]) < 10 or len(d["alt"]) < 8:
        raise ValueError("faltan elementos en las listas")
    d["combinar"], d["hashtags"], d["alt"] = d["combinar"][:3], d["hashtags"][:10], d["alt"][:8]
    if PROHIBIDO.search(json.dumps(d, ensure_ascii=False)):
        raise ValueError("el texto trae precio, cifra o escasez que no está en los datos")
    return d


def escribir_textos(prenda, gasto: Gasto, llamar=llamar_claude) -> dict:
    """Un solo pedido por prenda. Si Claude devuelve algo inválido, se reintenta una vez."""
    pedido = PEDIDO.format(nombre=prenda.nombre, categoria=prenda.categoria or "sin dato", n_fotos=len(prenda.fotos))
    ultimo = None
    for _ in range(2):
        gasto.reservar(len(REGLAS) + len(pedido), MAX_SALIDA)
        texto, t_in, t_out = llamar(REGLAS, pedido)
        gasto.anotar(prenda.sku, t_in, t_out)
        try:
            crudo = texto[texto.index("{"): texto.rindex("}") + 1]
            return _validar(json.loads(crudo))
        except ValueError as e:  # incluye JSONDecodeError
            ultimo = e
    raise ValueError(f"Claude no devolvió textos válidos: {ultimo}")
