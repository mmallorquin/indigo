"""Stories de marca (sin prenda) para Índigo Py: 1080x1920, colores de marca.toml, Inter + Cormorant.

Uso: python3 .claude/skills/story-marca/hacer_stories.py <carpeta_salida> <piezas.json>
piezas.json: lista de {"archivo", "etiqueta", "titulo", "cuerpo", "codigo", "hueco_sticker"(opcional)}.
"""
import json
import sys
import tomllib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parents[3]
W, H = 1080, 1920
MARCA = tomllib.loads((RAIZ / "marca.toml").read_text(encoding="utf-8"))
C = {c["clave"]: c["hex"] for c in MARCA["identidad"]["colores"]}
WA = MARCA["contacto"]["whatsapp"]


def f(nombre, tam):
    ruta = {"sans": "fabrica/fuentes/Inter-Medium.otf", "negrita": "fabrica/fuentes/Inter-Bold.otf",
            "serif": "app/static/fuentes/cormorant-normal.ttf"}[nombre]
    return ImageFont.truetype(str(RAIZ / ruta), tam)


def partir(d, t, fuente, ancho):
    lineas, actual = [], ""
    for p in t.split():
        prueba = (actual + " " + p).strip()
        if d.textlength(prueba, font=fuente) <= ancho or not actual:
            actual = prueba
        else:
            lineas.append(actual)
            actual = p
    return lineas + ([actual] if actual else [])


def bloque(d, y, t, fuente, color, ancho=880, inter=1.22):
    for parrafo in t.split("\n"):
        for linea in partir(d, parrafo, fuente, ancho):
            d.text(((W - d.textlength(linea, font=fuente)) / 2, y), linea, font=fuente, fill=color)
            y += int(fuente.size * inter)
        y += int(fuente.size * 0.35)
    return y


def logo(tam):
    img = Image.open(RAIZ / "app/static/marca/logo.jpg").convert("RGB").resize((tam, tam), Image.LANCZOS)
    mascara = Image.new("L", (tam, tam), 0)
    ImageDraw.Draw(mascara).ellipse((0, 0, tam - 1, tam - 1), fill=255)
    return img, mascara


def story(p, salida):
    im = Image.new("RGB", (W, H), C["olivo-profundo"])
    d = ImageDraw.Draw(im)
    lg, m = logo(190)
    im.paste(lg, ((W - 190) // 2, 230), m)
    y = 470
    d.line((440, y, 640, y), fill=C["arena"], width=3)
    y = bloque(d, y + 40, p["etiqueta"].upper(), f("negrita", 38), C["arena"])
    y = bloque(d, y + 40, p["titulo"], f("serif", 112), C["marfil"], inter=1.05)
    y = bloque(d, y + 40, p["cuerpo"], f("sans", 50), C["salvia"], ancho=860, inter=1.32)
    # si p["hueco_sticker"]: el espacio libre entre el texto y el botón (~y 1000-1440) queda para el
    # sticker de preguntas que se pone en la app de Instagram. Nunca escribir un aviso ahí: se publicaría.
    # botón
    by = 1470
    d.rounded_rectangle((140, by, 940, by + 130), radius=65, fill=C["marfil"])
    t = "Pedí por WhatsApp"
    fb = f("negrita", 54)
    d.text(((W - d.textlength(t, font=fb)) / 2, by + 32), t, font=fb, fill=C["olivo-profundo"])
    bloque(d, by + 160, WA, f("negrita", 44), C["marfil"])
    bloque(d, by + 225, "Código " + p["codigo"], f("sans", 30), C["arena"])
    im.save(salida / p["archivo"], optimize=True)


if __name__ == "__main__":
    salida = Path(sys.argv[1])
    salida.mkdir(parents=True, exist_ok=True)
    for pieza in json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")):
        story(pieza, salida)
        print("ok", pieza["archivo"])
