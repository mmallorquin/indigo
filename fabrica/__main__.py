"""python -m fabrica --entrada marketing/fabrica-entrada --salida salida/piezas [--skus A,B] [--tope-usd 8]"""

import argparse
import json
import sys
import tomllib
from pathlib import Path

import httpx
from PIL import Image

from fabrica import laminas, texto
from fabrica.catalogo import elegir, leer_catalogo

RAIZ = Path(__file__).resolve().parent.parent
# código de pieza por archivo
CODIGOS = {"carrusel_01": "C1", "carrusel_02": "C2", "carrusel_03": "C3", "carrusel_04": "C4", "carrusel_05": "C5",
           "story_01": "S1", "story_02": "S2", "story_03": "S3"}
GANCHO_PRECIO = "Precio y talles disponibles"


def fabricar_prenda(prenda, entrada: Path, salida: Path, marca: dict, gasto, llamar) -> list[str]:
    """Genera las piezas de un SKU. Devuelve la lista de datos que faltaban."""
    fotos = [Image.open(entrada / f) for f in prenda.fotos if (entrada / f).exists()]
    if not fotos:
        raise ValueError("no hay fotos de la prenda en la carpeta de entrada")
    textos = texto.escribir_textos(prenda, gasto, llamar)
    carpeta = salida / prenda.sku
    carpeta.mkdir(parents=True, exist_ok=True)
    piezas = laminas.Fabricante(marca, prenda, fotos, textos).todas()
    for nombre, img in piezas.items():
        img.save(carpeta / f"{nombre}.png", optimize=True)
    claves = list(piezas)
    json.dump({
        "instagram": textos["caption_instagram"], "tiktok": textos["caption_tiktok"], "hashtags": textos["hashtags"],
        "alt": {k: textos["alt"][i] for i, k in enumerate(claves)},
        "ganchos": [{"nombre": "Así queda puesto", "texto": textos["gancho_puesto"]},
                    {"nombre": GANCHO_PRECIO, "texto": textos["gancho_precio"]}],
        "datos_faltantes": prenda.faltantes(),
    }, open(carpeta / "textos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump({CODIGOS[k]: {"codigo": f"IND-{prenda.sku}-{CODIGOS[k]}",
                            "enlace": laminas.enlace_whatsapp(marca, f"IND-{prenda.sku}-{CODIGOS[k]}", prenda.nombre)}
               for k in claves},
              open(carpeta / "whatsapp.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    (carpeta / "listo.json").write_text(json.dumps({"piezas": len(piezas)}), encoding="utf-8")
    return prenda.faltantes()


def correr(entrada: Path, salida: Path, skus: list[str], tope_usd: float, llamar=texto.llamar_claude) -> int:
    marca = tomllib.loads((RAIZ / "marca.toml").read_text(encoding="utf-8"))
    gasto = texto.Gasto(tope_usd)
    try:
        salida.mkdir(parents=True, exist_ok=True)
        prendas = elegir(leer_catalogo(entrada), skus)
    except OSError as e:
        print(f"No se puede leer la entrada o escribir la salida: {e}", file=sys.stderr)
        return 1
    filas, corte = [], None
    for p in prendas:
        if (salida / p.sku / "listo.json").exists():
            filas.append((p.sku, "ya estaba lista", "-"))
            continue
        if corte:
            filas.append((p.sku, f"no se hizo: {corte}", "-"))
            continue
        antes = gasto.total
        try:
            falta = fabricar_prenda(p, entrada, salida, marca, gasto, llamar)
            filas.append((p.sku, "8 piezas" + (" (DEMO)" if p.demo else ""), ", ".join(falta) or "ninguno", gasto.total - antes))
        except texto.TopeSuperado as e:
            corte = str(e)
            filas.append((p.sku, f"no se hizo: {corte}", "-"))
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (401, 403):  # la key no sirve: no tiene sentido seguir
                print("Falló la autenticación con la API de Anthropic.", file=sys.stderr)
                return 1
            filas.append((p.sku, f"falló: {e}", "-"))
        except Exception as e:  # un SKU roto no frena a los demás
            filas.append((p.sku, f"falló: {e}", "-"))
    lineas = ["## Resumen de la fábrica", "", "| SKU | Piezas | Datos faltantes | Costo US$ |", "|---|---|---|---|"]
    for f in filas:
        costo = f"{f[3]:.3f}" if len(f) > 3 else "-"
        lineas.append(f"| {f[0]} | {f[1]} | {f[2] if len(f) > 2 else '-'} | {costo} |")
    lineas += ["", f"Gasto total: US$ {gasto.total:.3f} de un tope de US$ {gasto.tope:.2f}."]
    if not prendas:
        lineas.append("No había prendas con estado `listo`.")
    (salida / "resumen.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    (salida / "gasto.json").write_text(json.dumps({"total_usd": round(gasto.total, 5), "tope_usd": gasto.tope,
                                                   "llamadas": gasto.llamadas}, indent=2), encoding="utf-8")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Fábrica de piezas de Indigo")
    ap.add_argument("--entrada", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--skus", default="")
    ap.add_argument("--tope-usd", type=float, default=8.0)
    a = ap.parse_args(argv)
    return correr(a.entrada, a.salida, [s.strip() for s in a.skus.split(",") if s.strip()], a.tope_usd)


if __name__ == "__main__":
    sys.exit(main())
