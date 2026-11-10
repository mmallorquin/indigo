"""Agente de catálogo: recibe la foto de una prenda y devuelve su ficha."""

import io
import os
import tomllib
from pathlib import Path

from agent_framework import Agent, Content, Message
from PIL import Image, ImageOps

from esquemas import FichaProducto

try:  # fotos HEIC del iPhone, si está instalado pillow-heif
    from pillow_heif import register_heif_opener

    register_heif_opener()
except ImportError:
    pass

LADO_MAXIMO = 1568  # px; más grande no mejora la lectura y cuesta más tokens
PROVEEDORES = ("claude", "azure")

INSTRUCCIONES = """\
Sos el agente de catálogo de {nombre}, una {rubro} de {ciudad}.
Recibís la foto de UNA prenda y armás su ficha de producto.

Reglas:
- Describí solo lo que se ve. Si algo no se distingue (tela, largo exacto), decilo o dejalo en null.
- Nunca inventes precio, talles, stock ni composición de la tela: eso va en preguntas_para_la_tienda.
- Escribí en español de Paraguay, claro y natural, sin exagerar.
- Si en la foto hay varias prendas, la ficha es de la principal y lo mencionás en la descripción.
- Las palabras clave son las que usaría una clienta para buscar esa prenda.

Contexto de la marca (puede estar incompleto):
- Público: {publico}
- Tono: {tono}
- Estilos principales: {estilos}
- Evitar: {evitar}
- Notas: {notas}
"""


def cargar_marca(ruta: Path = Path("marca.toml")) -> dict:
    with open(ruta, "rb") as f:
        return tomllib.load(f)


def crear_cliente(proveedor: str):
    """El único lugar donde cambia algo según el modelo. El resto del agente es igual."""
    if proveedor == "claude":
        from agent_framework.anthropic import AnthropicClient

        # Lee ANTHROPIC_API_KEY del entorno; el modelo, de ANTHROPIC_CHAT_MODEL o Haiku por defecto
        modelo = os.environ.get("ANTHROPIC_CHAT_MODEL") or "claude-haiku-4-5"
        return AnthropicClient(model=modelo), {"max_tokens": 2000}

    if proveedor == "azure":
        from agent_framework.openai import OpenAIChatClient
        from azure.identity import DefaultAzureCredential

        # Sin API key: usa tu sesión de `az login` (y en la nube, la identidad administrada)
        cliente = OpenAIChatClient(
            model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-5-mini"),
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            credential=DefaultAzureCredential(),
        )
        # gpt-5-mini razona antes de responder: esos tokens también cuentan en el máximo
        return cliente, {"max_tokens": 6000, "reasoning": {"effort": "low"}}

    raise ValueError(f"Proveedor desconocido: {proveedor}. Opciones: {', '.join(PROVEEDORES)}")


def crear_agente(marca: dict, proveedor: str = "claude", client=None) -> Agent:
    vacio = "(sin definir)"
    instrucciones = INSTRUCCIONES.format(
        nombre=marca["nombre"],
        rubro=marca["rubro"],
        ciudad=marca["ciudad"],
        publico=marca.get("publico") or vacio,
        tono=marca.get("tono") or vacio,
        estilos=", ".join(marca.get("estilos_principales", [])) or vacio,
        evitar=", ".join(marca.get("evitar", [])) or vacio,
        notas=marca.get("notas") or vacio,
    )
    if client is None:
        client, opciones = crear_cliente(proveedor)
    else:
        opciones = {"max_tokens": 2000}
    return Agent(
        client=client,
        name=f"catalogo-{proveedor}",
        instructions=instrucciones,
        default_options={"response_format": FichaProducto, **opciones},
    )


def preparar_foto(origen: Path | bytes) -> bytes:
    """Endereza, achica y convierte a JPEG para mandarla al modelo."""
    if isinstance(origen, bytes):
        origen = io.BytesIO(origen)
    with Image.open(origen) as img:
        img = ImageOps.exif_transpose(img).convert("RGB")
        img.thumbnail((LADO_MAXIMO, LADO_MAXIMO))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        return buffer.getvalue()


async def fichar(agente: Agent, foto: Path | bytes, nombre: str | None = None) -> tuple[FichaProducto, dict]:
    """Devuelve la ficha y el uso de tokens de esa foto (ruta o bytes)."""
    nombre = nombre or (foto.name if isinstance(foto, Path) else "foto")
    mensaje = Message(
        role="user",
        contents=[
            Content.from_text(text=f"Armá la ficha de esta prenda (archivo: {nombre})."),
            Content.from_data(data=preparar_foto(foto), media_type="image/jpeg"),
        ],
    )
    respuesta = await agente.run(mensaje)
    if respuesta.value is None:
        raise ValueError(f"El modelo no devolvió una ficha válida: {respuesta.text[:200]}")
    return respuesta.value, dict(getattr(respuesta, "usage_details", None) or {})
