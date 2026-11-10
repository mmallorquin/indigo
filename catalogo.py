"""Uso: python catalogo.py fotos/

Arma una ficha por cada foto de la carpeta y las guarda en salida/:
- salida/<foto>.json  -> la ficha completa
- salida/catalogo.csv -> resumen para abrir en Excel
"""

import asyncio
import csv
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

from agente_catalogo import cargar_marca, crear_agente, fichar

EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp", ".heic"}
SALIDA = Path("salida")


async def main(carpeta: Path) -> None:
    fotos = sorted(p for p in carpeta.iterdir() if p.suffix.lower() in EXTENSIONES)
    if not fotos:
        sys.exit(f"No encontré fotos en {carpeta}")

    SALIDA.mkdir(exist_ok=True)
    agente = crear_agente(cargar_marca())
    filas, total_in, total_out = [], 0, 0

    for i, foto in enumerate(fotos, 1):
        print(f"[{i}/{len(fotos)}] {foto.name} ... ", end="", flush=True)
        try:
            ficha, uso = await fichar(agente, foto)
        except Exception as e:  # una foto mala no frena el lote
            print(f"ERROR: {e}")
            continue

        (SALIDA / f"{foto.stem}.json").write_text(
            ficha.model_dump_json(indent=2), encoding="utf-8"
        )
        tokens_in, tokens_out = uso.get("input_token_count", 0), uso.get("output_token_count", 0)
        total_in, total_out = total_in + tokens_in, total_out + tokens_out
        print(f"{ficha.nombre_sugerido} ({ficha.categoria}, confianza {ficha.confianza}) "
              f"· {tokens_in}+{tokens_out} tokens")

        filas.append({
            "foto": foto.name,
            "nombre": ficha.nombre_sugerido,
            "categoria": ficha.categoria,
            "colores": ", ".join(ficha.colores),
            "temporada": ficha.temporada,
            "estilo": ", ".join(ficha.estilo),
            "calidad_foto": ficha.calidad_foto,
            "confianza": ficha.confianza,
            "preguntas": " | ".join(ficha.preguntas_para_la_tienda),
        })

    if filas:
        with open(SALIDA / "catalogo.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=filas[0].keys())
            writer.writeheader()
            writer.writerows(filas)

    print(f"\nListo: {len(filas)}/{len(fotos)} fichas en {SALIDA}/ "
          f"· tokens totales {total_in} entrada + {total_out} salida")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    load_dotenv()
    asyncio.run(main(Path(sys.argv[1])))
