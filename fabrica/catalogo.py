"""Lee catalogo.csv. Lo que está vacío queda en None: nunca se completa con valores inventados."""

import csv
from dataclasses import dataclass, field
from pathlib import Path

COLUMNAS = ["sku", "nombre", "categoria", "precio_gs", "talles", "stock", "medidas", "entrega",
            "fotos", "clips", "prenda_probador", "estado"]


@dataclass
class Prenda:
    sku: str
    nombre: str
    categoria: str
    precio_gs: int | None
    talles: list[str]
    stock: int | None
    medidas: str | None
    entrega: str | None
    fotos: list[str] = field(default_factory=list)
    clips: list[str] = field(default_factory=list)
    prenda_probador: str | None = None
    estado: str = ""

    @property
    def demo(self) -> bool:
        return self.estado.upper() == "DEMO"

    def faltantes(self) -> list[str]:
        falta = []
        if self.precio_gs is None:
            falta.append("precio")
        if not self.talles:
            falta.append("talles")
        if not self.medidas:
            falta.append("medidas")
        if not self.entrega:
            falta.append("entrega")
        return falta


def _vacio(valor: str | None) -> str | None:
    valor = (valor or "").strip()
    return valor or None


def _entero(valor: str | None) -> int | None:
    limpio = "".join(c for c in (valor or "") if c.isdigit())
    return int(limpio) if limpio else None


def _lista(valor: str | None, sep: str) -> list[str]:
    return [x.strip() for x in (valor or "").split(sep) if x.strip()]


def leer_catalogo(entrada: Path) -> list[Prenda]:
    with open(entrada / "catalogo.csv", newline="", encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f))
    prendas = []
    for fila in filas:
        sku = (fila.get("sku") or "").strip()
        if not sku:
            continue
        prendas.append(Prenda(
            sku=sku, nombre=(fila.get("nombre") or sku).strip(), categoria=(fila.get("categoria") or "").strip(),
            precio_gs=_entero(fila.get("precio_gs")), talles=_lista(fila.get("talles"), "/"),
            stock=_entero(fila.get("stock")), medidas=_vacio(fila.get("medidas")), entrega=_vacio(fila.get("entrega")),
            fotos=_lista(fila.get("fotos"), "|"), clips=_lista(fila.get("clips"), "|"),
            prenda_probador=_vacio(fila.get("prenda_probador")), estado=(fila.get("estado") or "").strip(),
        ))
    return prendas


def elegir(prendas: list[Prenda], skus: list[str]) -> list[Prenda]:
    """--skus manda; si no, las 'listo'; las DEMO solo si no hay ninguna 'listo'."""
    if skus:
        return [p for p in prendas if p.sku in skus]
    listas = [p for p in prendas if p.estado.lower() == "listo"]
    return listas or [p for p in prendas if p.demo]
