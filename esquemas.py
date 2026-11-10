"""Qué devuelve cada agente. Hoy: la ficha de producto del agente de catálogo.

Reglas para que el esquema funcione con las salidas estructuradas de Claude:
- extra="forbid" en cada modelo (Claude exige additionalProperties: false).
- Sin valores por defecto ni límites de largo: todo campo es obligatorio;
  lo opcional se expresa como `X | None`.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Categoria = Literal[
    "remera", "blusa", "camisa", "top", "vestido", "pollera", "short",
    "pantalon", "jean", "campera", "abrigo", "buzo", "conjunto",
    "enterito", "traje_de_bano", "accesorio", "calzado", "otro",
]


class FichaProducto(BaseModel):
    """Ficha de una prenda, armada solo a partir de lo que se ve en la foto."""

    model_config = ConfigDict(extra="forbid")

    nombre_sugerido: str = Field(description="Nombre comercial corto y atractivo, 2 a 5 palabras")
    categoria: Categoria
    descripcion: str = Field(description="2 o 3 oraciones describiendo la prenda tal como se ve")
    colores: list[str] = Field(description="Colores principales, del más al menos presente")
    material_aparente: str | None = Field(description="Material que parece ser, o null si no se distingue")
    detalles: list[str] = Field(description="Estampados, cortes, botones, volados, escote, largo, etc.")
    estilo: list[str] = Field(description="Ej.: casual, elegante, deportivo, boho, urbano")
    ocasiones: list[str] = Field(description="Dónde se usaría: oficina, salida nocturna, playa, cumpleaños...")
    temporada: Literal["verano", "invierno", "media_estacion", "todo_el_anio"]
    combina_con: list[str] = Field(description="Prendas o accesorios que combinan, para armar looks")
    palabras_clave: list[str] = Field(description="Términos de búsqueda y hashtags sin el #, en español")
    calidad_foto: Literal["buena", "aceptable", "mala"]
    problemas_foto: list[str] = Field(description="Qué mejorar de la foto (luz, fondo, encuadre); vacío si está bien")
    confianza: Literal["alta", "media", "baja"] = Field(
        description="Qué tan seguro estás de la ficha en general"
    )
    preguntas_para_la_tienda: list[str] = Field(
        description="Datos que la foto no muestra y la tienda debe completar (talles, precio, tela real...)"
    )
