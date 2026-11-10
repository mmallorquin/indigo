"""Prueba el agente sin gastar API: reemplaza a Claude por un cliente falso.

Verifica que la foto viaje como imagen, que se pida salida estructurada
y que la respuesta se convierta en FichaProducto.
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from agent_framework.anthropic import AnthropicClient
from anthropic.types.beta import BetaMessage
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from agente_catalogo import cargar_marca, crear_agente, fichar  # noqa: E402

FICHA_EJEMPLO = {
    "nombre_sugerido": "Blusa Lino Celeste",
    "categoria": "blusa",
    "descripcion": "Blusa manga corta en tono celeste con botones al frente.",
    "colores": ["celeste"],
    "material_aparente": "lino",
    "detalles": ["botones al frente", "manga corta"],
    "estilo": ["casual"],
    "ocasiones": ["oficina", "salida de día"],
    "temporada": "verano",
    "combina_con": ["jean claro", "sandalias"],
    "palabras_clave": ["blusa celeste", "blusa de lino"],
    "calidad_foto": "buena",
    "problemas_foto": [],
    "confianza": "alta",
    "preguntas_para_la_tienda": ["¿Qué talles hay?", "¿Precio?"],
}


class AnthropicFalso:
    """Imita anthropic_client.beta.messages.create y guarda lo que se le mandó."""

    base_url = "https://falso.local"

    def __init__(self):
        self.pedidos = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    async def _create(self, **kwargs):
        self.pedidos.append(kwargs)
        return BetaMessage.model_validate({
            "id": "msg_test",
            "type": "message",
            "role": "assistant",
            "model": kwargs["model"],
            "content": [{"type": "text", "text": json.dumps(FICHA_EJEMPLO)}],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {"input_tokens": 1234, "output_tokens": 321},
        })


@pytest.fixture
def foto(tmp_path):
    ruta = tmp_path / "blusa.png"
    Image.new("RGB", (4000, 3000), "skyblue").save(ruta)  # foto grande, a propósito
    return ruta


@pytest.mark.asyncio
async def test_fichar_con_cliente_falso(foto):
    falso = AnthropicFalso()
    client = AnthropicClient(api_key="test", model="claude-haiku-4-5", anthropic_client=falso)
    agente = crear_agente(cargar_marca(RAIZ / "marca.toml"), client=client)

    ficha, uso = await fichar(agente, foto)

    # La respuesta se convirtió en una ficha válida
    assert ficha.nombre_sugerido == "Blusa Lino Celeste"
    assert ficha.categoria == "blusa"
    assert uso.get("input_token_count") == 1234

    pedido = falso.pedidos[0]
    # Se pidió salida estructurada con nuestro esquema
    esquema = pedido["output_config"]["format"]["schema"]
    assert esquema["additionalProperties"] is False
    assert "preguntas_para_la_tienda" in esquema["required"]
    # Las instrucciones llevan el nombre de la marca
    assert "Índigo Py" in str(pedido["system"])
    # La foto viajó como imagen JPEG
    bloques = pedido["messages"][-1]["content"]
    imagen = next(b for b in bloques if b["type"] == "image")
    assert imagen["source"]["media_type"] == "image/jpeg"


def test_foto_se_achica(foto):
    import io

    from agente_catalogo import LADO_MAXIMO, preparar_foto

    with Image.open(io.BytesIO(preparar_foto(foto))) as img:
        assert max(img.size) <= LADO_MAXIMO
        assert img.format == "JPEG"
