"""Dibuja las láminas con Pillow: colores de marca.toml, Inter (fabrica/fuentes) y Cormorant Garamond (app/static/fuentes)."""

from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageDraw, ImageFont, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
SIN_DATO = "Consultá precio y talle por WhatsApp"
W, H_C, H_S = 1080, 1350, 1920


def colores(marca: dict) -> dict:
    return {c["clave"]: c["hex"] for c in marca["identidad"]["colores"]}


def fuente(nombre: str, tam: int) -> ImageFont.FreeTypeFont:
    ruta = {"sans": RAIZ / "fabrica/fuentes/Inter-Medium.otf", "negrita": RAIZ / "fabrica/fuentes/Inter-Bold.otf",
            "serif": RAIZ / "app/static/fuentes/cormorant-normal.ttf"}[nombre]
    return ImageFont.truetype(str(ruta), tam)


def cubrir(img: Image.Image, ancho: int, alto: int, zoom: float = 1.0) -> Image.Image:
    img = ImageOps.exif_transpose(img).convert("RGB")
    if zoom > 1:
        w, h = img.size
        cw, ch = int(w / zoom), int(h / zoom)
        img = img.crop(((w - cw) // 2, (h - ch) // 2, (w + cw) // 2, (h + ch) // 2))
    return ImageOps.fit(img, (ancho, alto), Image.LANCZOS, centering=(0.5, 0.4))


def contener(img: Image.Image, ancho: int, alto: int, fondo: str) -> Image.Image:
    """La prenda entera, sin recortar, centrada sobre un fondo liso."""
    img = ImageOps.exif_transpose(img).convert("RGB")
    img.thumbnail((ancho, alto), Image.LANCZOS)
    lienzo = Image.new("RGB", (ancho, alto), fondo)
    lienzo.paste(img, ((ancho - img.width) // 2, (alto - img.height) // 2))
    return lienzo


def partir(d: ImageDraw.ImageDraw, texto: str, f, ancho: int) -> list[str]:
    lineas, actual = [], ""
    for palabra in texto.split():
        prueba = f"{actual} {palabra}".strip()
        if d.textlength(prueba, font=f) <= ancho or not actual:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra
    return lineas + ([actual] if actual else [])


def texto(d, xy, t, f, color, ancho, centrado=False, interlineado=1.25) -> int:
    """Escribe texto en varias líneas. Devuelve la y donde terminó."""
    x, y = xy
    for linea in partir(d, t, f, ancho):
        px = x + (ancho - d.textlength(linea, font=f)) / 2 if centrado else x
        d.text((px, y), linea, font=f, fill=color)
        y += int(f.size * interlineado)
    return y


def marca_demo(img: Image.Image) -> Image.Image:
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    f = fuente("negrita", img.width // 5)
    d.text((img.width // 2, img.height // 2), "DEMO", font=f, fill=(255, 255, 255, 110), anchor="mm",
           stroke_width=3, stroke_fill=(0, 0, 0, 110))
    capa = capa.rotate(25, resample=Image.BICUBIC)
    return Image.alpha_composite(img.convert("RGBA"), capa).convert("RGB")


def linea_datos(p) -> dict:
    """Solo lo que está en el CSV. Lo que falta no se muestra como dato: se manda a WhatsApp."""
    return {
        "precio": f"Gs. {p.precio_gs:,}".replace(",", ".") if p.precio_gs is not None else None,
        "talles": "Talles: " + " · ".join(p.talles) if p.talles else None,
        "medidas": p.medidas, "entrega": p.entrega,
        "stock": f"Disponibles: {p.stock}" if p.stock else None,
    }


def enlace_whatsapp(marca: dict, codigo: str, nombre: str) -> str:
    msg = f"Hola, vengo por {codigo}. Me interesa: {nombre}."
    return f"{marca['contacto']['whatsapp_url']}?text={quote(msg)}"


class Fabricante:
    def __init__(self, marca: dict, prenda, fotos: list[Image.Image], textos: dict):
        self.m, self.p, self.fotos, self.t = marca, prenda, fotos, textos
        self.c = colores(marca)
        self.datos = linea_datos(prenda)
        self.logo = Image.open(RAIZ / "app/static" / marca["identidad"]["logo"]).convert("RGB")

    def _foto(self, i: int) -> Image.Image:
        return self.fotos[i % len(self.fotos)]

    def _lienzo(self, alto: int, fondo: str):
        img = Image.new("RGB", (W, alto), self.c[fondo])
        return img, ImageDraw.Draw(img)

    def _firma(self, img, d, alto, claro=True):
        """Logo chico y @ abajo, en todas las láminas."""
        color = self.c["marfil"] if claro else self.c["olivo"]
        logo = self.logo.resize((72, 72))
        img.paste(logo, (64, alto - 130))
        d.text((152, alto - 112), "@indigopy_", font=fuente("sans", 32), fill=color)

    def _terminar(self, img):
        return marca_demo(img) if self.p.demo else img

    # ---- carrusel 1080x1350
    def c1_portada(self):
        img = cubrir(self._foto(0), W, H_C)
        d = ImageDraw.Draw(img)
        d.rectangle((0, H_C - 400, W, H_C), fill=self.c["olivo-profundo"])
        d.rectangle((64, H_C - 400, 184, H_C - 394), fill=self.c["arena"])
        texto(d, (64, H_C - 360), self.p.nombre, fuente("serif", 84), self.c["marfil"], W - 128, interlineado=1.0)
        texto(d, (64, H_C - 190), self.t["gancho_puesto"], fuente("sans", 40), self.c["salvia"], W - 128)
        self._firma(img, d, H_C)
        return self._terminar(img)

    def c2_detalle(self):
        img = cubrir(self._foto(1), W, H_C, zoom=1.8)
        d = ImageDraw.Draw(img)
        d.rectangle((0, H_C - 330, W, H_C), fill=self.c["olivo-profundo"])
        texto(d, (64, H_C - 290), self.t["detalle"], fuente("serif", 62), self.c["marfil"], W - 128, interlineado=1.1)
        self._firma(img, d, H_C)
        return self._terminar(img)

    def c3_combinar(self):
        img, d = self._lienzo(H_C, "marfil")
        img.paste(contener(self._foto(2), W - 128, 640, self.c["marfil"]), (64, 64))
        d.text((64, 750), "Cómo combinarla", font=fuente("serif", 76), fill=self.c["olivo"])
        y = 870
        for idea in self.t["combinar"]:
            d.ellipse((64, y + 16, 80, y + 32), fill=self.c["arena"])
            y = texto(d, (104, y), idea, fuente("sans", 42), self.c["tinta"], W - 170) + 18
        self._firma(img, d, H_C, claro=False)
        return self._terminar(img)

    def c4_talles(self):
        img, d = self._lienzo(H_C, "olivo")
        d.text((64, 90), "Talles y medidas", font=fuente("serif", 84), fill=self.c["marfil"])
        d.rectangle((64, 210, 184, 216), fill=self.c["arena"])
        filas = [self.datos["precio"], self.datos["talles"], self.datos["medidas"], self.datos["entrega"], self.datos["stock"]]
        y = 270
        for fila in filas:
            if fila:
                y = texto(d, (64, y), fila, fuente("negrita", 52), self.c["marfil"], W - 128) + 30
        if None in filas[:3]:  # falta precio, talle o medidas: se manda a WhatsApp, no se inventa
            y = texto(d, (64, y + 20), SIN_DATO, fuente("sans", 44), self.c["salvia"], W - 128)
        self._firma(img, d, H_C)
        return self._terminar(img)

    def c5_cierre(self):
        img, d = self._lienzo(H_C, "olivo-profundo")
        img.paste(self.logo.resize((220, 220)), ((W - 220) // 2, 230))
        texto(d, (64, 520), "Pedí por WhatsApp", fuente("serif", 100), self.c["marfil"], W - 128, centrado=True)
        texto(d, (64, 700), self.m["nombre"] + " · " + self.m["ciudad"], fuente("sans", 38), self.c["salvia"], W - 128, centrado=True)
        d.rounded_rectangle((200, 840, W - 200, 970), 20, fill=self.c["arena"])
        d.text((W // 2, 905), self.m["contacto"]["whatsapp"], font=fuente("negrita", 52), fill=self.c["tinta"], anchor="mm")
        d.text((W // 2, 1060), f"Código: IND-{self.p.sku}-C5", font=fuente("sans", 34), fill=self.c["salvia"], anchor="mm")
        return self._terminar(img)

    # ---- stories 1080x1920
    def s1_producto(self):
        img = cubrir(self._foto(0), W, H_S)
        d = ImageDraw.Draw(img)
        d.rectangle((0, H_S - 560, W, H_S), fill=self.c["olivo-profundo"])
        texto(d, (64, H_S - 520), self.p.nombre, fuente("serif", 96), self.c["marfil"], W - 128, interlineado=1.0)
        texto(d, (64, H_S - 330), self.datos["precio"] or SIN_DATO, fuente("negrita", 56), self.c["arena"], W - 128)
        self._firma(img, d, H_S)
        return self._terminar(img)

    def s2_combinar(self):
        img, d = self._lienzo(H_S, "marfil")
        img.paste(contener(self._foto(2), W - 128, 900, self.c["marfil"]), (64, 180))
        d.text((64, 1130), "Cómo combinarla", font=fuente("serif", 88), fill=self.c["olivo"])
        y = 1270
        for idea in self.t["combinar"]:
            d.ellipse((64, y + 16, 80, y + 32), fill=self.c["arena"])
            y = texto(d, (104, y), idea, fuente("sans", 44), self.c["tinta"], W - 170) + 20
        return self._terminar(img)

    def s3_comprar(self):
        img, d = self._lienzo(H_S, "olivo")
        d.text((64, 200), "Cómo pedir", font=fuente("serif", 120), fill=self.c["marfil"])
        pasos = ["Escribinos por WhatsApp", "Te ayudamos con el talle", "Confirmamos y pagás por transferencia"]
        y = 520
        for i, paso in enumerate(pasos, 1):
            d.ellipse((64, y, 164, y + 100), fill=self.c["arena"])
            d.text((114, y + 50), str(i), font=fuente("negrita", 56), fill=self.c["tinta"], anchor="mm")
            y = max(texto(d, (204, y + 10), paso, fuente("sans", 50), self.c["marfil"], W - 270), y + 120) + 70
        d.rounded_rectangle((120, 1420, W - 120, 1560), 24, fill=self.c["arena"])
        d.text((W // 2, 1490), self.m["contacto"]["whatsapp"], font=fuente("negrita", 56), fill=self.c["tinta"], anchor="mm")
        d.text((W // 2, 1640), f"Código: IND-{self.p.sku}-S3", font=fuente("sans", 34), fill=self.c["salvia"], anchor="mm")
        return self._terminar(img)

    def todas(self) -> dict[str, Image.Image]:
        return {
            "carrusel_01": self.c1_portada(), "carrusel_02": self.c2_detalle(), "carrusel_03": self.c3_combinar(),
            "carrusel_04": self.c4_talles(), "carrusel_05": self.c5_cierre(),
            "story_01": self.s1_producto(), "story_02": self.s2_combinar(), "story_03": self.s3_comprar(),
        }
