#!/usr/bin/env python3
"""Motor de video Indigo PY: zocalos, titulos y transiciones sobre material real.
Sin IA generativa: solo recorte, composicion y texto. Requiere Python 3, Pillow, NumPy y FFmpeg.
INDIGO_ROOT = carpeta indigo-py-marketing; INDIGO_OUT = carpeta de salida."""
import os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("INDIGO_ROOT", os.path.abspath(os.path.join(HERE, "..", "..")))
OUT = os.environ.get("INDIGO_OUT", os.path.join(HERE, "..", "finales"))
W, H, FPS = 1080, 1920, 30
THREADS = os.environ.get("INDIGO_THREADS", "2")  # hilos de FFmpeg (la maquina se comparte)
OLIVE = (79, 85, 51); DARK = (48, 55, 31); PAPER = (244, 240, 230); INK = (32, 37, 27)
SAGE = (203, 208, 178); SAND = (196, 171, 121)
FONTS = ROOT + "/coleccion-v8-editorial/editor/public/fonts/"
FILES = {"serif": "cormorant-normal.ttf", "italic": "cormorant-italic.ttf", "sans": "inter-500.ttf", "bold": "inter-700.ttf"}
AUDIO = ROOT + "/videos-v6-olivo/editor/public/audio/%02d.wav"
BPM = {1: 100, 2: 102, 3: 104, 4: 106, 5: 108, 6: 110, 7: 112, 8: 103, 9: 105, 10: 109}
_fc = {}


def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        f = ImageFont.truetype(FONTS + FILES[kind], size)
        if kind in ("serif", "italic"):
            try:
                f.set_variation_by_axes([600])
            except Exception:
                pass
        _fc[k] = f
    return _fc[k]


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def eo(p):
    p = clamp(p); return 1 - (1 - p) ** 3


def eio(p):
    p = clamp(p); return p * p * (3 - 2 * p)


def text_sprite(txt, kind, size, color, tracking=0, shadow=0):
    f = font(kind, size); asc, desc = f.getmetrics()
    w = int(sum(f.getlength(c) for c in txt) + tracking * max(len(txt) - 1, 0)) if tracking else int(f.getlength(txt))
    pad = shadow * 3
    img = Image.new("RGBA", (w + 2 * pad + 8, asc + desc + 2 * pad), (0, 0, 0, 0))

    def put(d, ox, oy, fill):
        if tracking:
            x = ox
            for c in txt:
                d.text((x, oy), c, font=f, fill=fill); x += f.getlength(c) + tracking
        else:
            d.text((ox, oy), txt, font=f, fill=fill)
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); put(ImageDraw.Draw(sh), pad, pad + 4, (0, 0, 0, 190))
        img = sh.filter(ImageFilter.GaussianBlur(shadow))
    put(ImageDraw.Draw(img), pad, pad, tuple(color) + (255,))
    return img


def paste(cv, sp, x, y, alpha=1.0, clip=None):
    if alpha <= 0.01:
        return
    if clip:
        l, t, r, b = [int(v) for v in clip]
        l = max(l, 0); t = max(t, 0); r = min(r, sp.width); b = min(b, sp.height)
        if r <= l or b <= t:
            return
        sp = sp.crop((l, t, r, b)); x += l; y += t
    m = sp.getchannel("A")
    if alpha < 0.995:
        m = m.point(lambda v: int(v * alpha))
    cv.paste(sp, (int(x), int(y)), m)


def anim_io(t, t0, t1, din=0.4, dout=0.22):
    return eo((t - t0) / din), clamp((t1 - t) / dout)


# ---------- sprites ----------
def make_zocalo(kicker, title, sub=None, maxw=760):
    k = text_sprite(kicker, "bold", 25, OLIVE, tracking=5)
    size = 78
    while True:
        tt = text_sprite(title, "serif", size, INK)
        if tt.width <= maxw - 96 or size <= 44:
            break
        size -= 4
    s = text_sprite(sub, "sans", 30, INK) if sub else None
    w = max(k.width, tt.width, s.width if s else 0) + 96
    h = 26 + k.height + tt.height - 6 + ((s.height + 6) if s else 0) + 28
    img = Image.new("RGBA", (w, h), tuple(PAPER) + (255,))
    ImageDraw.Draw(img).rectangle((0, 0, 11, h), fill=tuple(OLIVE) + (255,))
    y = 26; img.alpha_composite(k, (44, y)); y += k.height - 8
    img.alpha_composite(tt, (44, y)); y += tt.height - 2
    if s:
        img.alpha_composite(s, (44, y))
    return img


def make_zocalo_lineas(lines, maxw=760):
    """Zocalo del mismo estilo que make_zocalo pero sin sobretitulo: solo el texto (una o mas lineas)."""
    size = 78
    while True:
        sps = [text_sprite(l, "serif", size, INK) for l in lines]
        if max(sp.width for sp in sps) <= maxw - 96 or size <= 44:
            break
        size -= 4
    w = max(sp.width for sp in sps) + 96
    h = 26 + sum(sp.height - 6 for sp in sps) + 34
    img = Image.new("RGBA", (w, h), tuple(PAPER) + (255,))
    ImageDraw.Draw(img).rectangle((0, 0, 11, h), fill=tuple(OLIVE) + (255,))
    y = 26
    for sp in sps:
        img.alpha_composite(sp, (44, y)); y += sp.height - 6
    return img


def make_pill(text, bg=PAPER, fg=INK, size=30, padx=28, pady=12, tracking=3):
    ts = text_sprite(text, "bold", size, fg, tracking=tracking)
    w = ts.width + 2 * padx; h = ts.height + 2 * pady
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=tuple(bg) + (255,))
    img.alpha_composite(ts, (padx, pady)); return img


def make_bubble(lines, side):
    bg, fg = (PAPER, INK) if side == "L" else (OLIVE, PAPER)
    sps = [text_sprite(l, "sans", 48, fg) for l in lines]
    w = max(s.width for s in sps) + 76; h = sum(s.height for s in sps) + 50
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, w - 1, h - 1), radius=38, fill=tuple(bg) + (255,))
    y = 25
    for s in sps:
        img.alpha_composite(s, (38, y)); y += s.height
    return img


def make_logo(d=300):
    im = Image.open(ROOT + "/coleccion-v8-editorial/editor/public/brand/logo.jpg").convert("RGB").resize((d, d), Image.LANCZOS)
    m = Image.new("L", (d * 2, d * 2), 0); ImageDraw.Draw(m).ellipse((4, 4, d * 2 - 4, d * 2 - 4), fill=255)
    im.putalpha(m.resize((d, d), Image.LANCZOS)); return im


# ---------- overlays: (t0, t1, fn(cv, t)) ----------
def ov_zocalo(t0, t1, kicker, title, sub=None, x=65, yb=1240, maxw=760, side="L"):
    sp = make_zocalo(kicker, title, sub, maxw)
    if side == "R":
        x = 1015 - sp.width

    def fn(cv, t):
        pin, pout = anim_io(t, t0, t1)
        vis = pin * eo(pout)
        paste(cv, sp, x - int(26 * (1 - pin)), yb - sp.height, 1.0, clip=(0, 0, int(sp.width * vis), sp.height))
    return (t0, t1, fn)


def ov_zocalo_sp(t0, t1, sp, x=65, yb=1240):
    """Mismo movimiento de entrada/salida que ov_zocalo, con un sprite ya hecho."""
    def fn(cv, t):
        pin, pout = anim_io(t, t0, t1)
        vis = pin * eo(pout)
        paste(cv, sp, x - int(26 * (1 - pin)), yb - sp.height, 1.0, clip=(0, 0, int(sp.width * vis), sp.height))
    return (t0, t1, fn)


def ov_title(t0, t1, lines, size=124, kind="serif", color=PAPER, x=65, y=300, align="left", lh=0.98, shadow=10, stagger=0.09, din=0.5):
    sps = [text_sprite(l, kind, size, color, shadow=shadow) for l in lines]
    step = int(size * lh * 1.04); pad = shadow * 3

    def fn(cv, t):
        _, pout = anim_io(t, t0, t1, dout=0.2)
        for k, sp in enumerate(sps):
            p = eo((t - t0 - k * stagger) / din)
            if p <= 0:
                continue
            xx = x - pad if align == "left" else (W - sp.width) // 2
            hv = int(sp.height * p)
            paste(cv, sp, xx, y - pad + k * step + (sp.height - hv), alpha=min(1, pout) * min(1, p * 2), clip=(0, 0, sp.width, hv))
    return (t0, t1, fn)


def ov_sprite(t0, t1, sp, x=0, y=0, din=0.3, dout=0.2, rise=26, center=False, pop=False):
    def fn(cv, t):
        pin, pout = anim_io(t, t0, t1, din, dout)
        a = min(1, pin * 1.6) * min(1, pout); s = sp
        if pop and pin < 1:
            sc = 1.3 - 0.3 * pin
            s = sp.resize((max(1, int(sp.width * sc)), max(1, int(sp.height * sc))), Image.BILINEAR)
        xx = (W - s.width) // 2 if center else x - (s.width - sp.width) // 2
        yy = y - (s.height - sp.height) // 2 + (0 if pop else int(rise * (1 - pin)))
        paste(cv, s, xx, yy, a)
    return (t0, t1, fn)


def ov_line(t0, t1, y, x0=65, x1=1015, color=SAND, th=6):
    def fn(cv, t):
        pin, pout = anim_io(t, t0, t1, 0.5, 0.2)
        if pout < 0.5:
            return
        ImageDraw.Draw(cv).rectangle((x0, y, x0 + int((x1 - x0) * pin), y + th), fill=color)
    return (t0, t1, fn)


def ov_strips(t0, t1, colors):
    n = len(colors); sw = W // n + 1

    def fn(cv, t):
        d = ImageDraw.Draw(cv)
        for k, c in enumerate(colors):
            p = eio((t - t0 - 0.35 - k * 0.12) / 0.55)
            top = int(H * p)
            if top < H:
                d.rectangle((k * sw, 0, (k + 1) * sw, H - top), fill=c)
    return (t0, t1, fn)


# ---------- escenas ----------
class Reader:
    def __init__(s, path, t0, n, speed):
        s.path, s.t0, s.n, s.speed = path, t0, n, speed; s.p = None; s.cur = -1; s.fr = None

    def get(s, j):
        j = max(0, min(j, s.n - 1))
        if s.p is None:
            dur = (s.n + 2) / FPS * s.speed
            s.p = subprocess.Popen(["ffmpeg", "-v", "error", "-threads", THREADS, "-ss", f"{s.t0:.3f}", "-t", f"{dur:.3f}", "-i", s.path,
                                    "-vf", f"setpts=PTS/{s.speed},fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                   stdout=subprocess.PIPE)
        while s.cur < j:
            b = s.p.stdout.read(720 * 1280 * 3)
            if len(b) < 720 * 1280 * 3:
                break
            s.fr = np.frombuffer(b, np.uint8).reshape(1280, 720, 3); s.cur += 1
        return s.fr

    def close(s):
        if s.p:
            s.p.stdout.close(); s.p.kill(); s.p.wait(); s.p = None


def band_bg(bands):
    cv = Image.new("RGB", (W, H), DARK)
    wm = text_sprite("ÍNDIGO PY", "bold", 24, SAGE, tracking=7)
    for (y0, y1, wy) in bands:
        paste(cv, wm, (W - wm.width) // 2, wy)
        ImageDraw.Draw(cv).rectangle((W // 2 - 44, wy + wm.height + 6, W // 2 + 44, wy + wm.height + 8), fill=SAND)
    return cv


PRE = {
    "looks": dict(src=(0, 226, 720, 1280), dst=(0, 336, 1080, 1581), bands=[(0, 336, 272)]),
    "jeans": dict(src=(0, 0, 720, 1030), dst=(0, 0, 1080, 1545), bands=[(1545, 1920, 1610)]),
    "tonos": dict(src=(0, 0, 720, 1090), dst=(0, 0, 1080, 1635), bands=[(1635, 1920, 1700)]),
    "calle": dict(src=(0, 0, 720, 1280), dst=(0, 0, 1080, 1920), bands=[], cover=(0, 1262, 612, 1730)),
}
SRC = {
    "looks": ROOT + "/videos-v2/source.mp4",
    "jeans": ROOT + "/videos-v5/fuentes/jeans-percha.mp4",
    "tonos": ROOT + "/videos-v5/fuentes/prendas-tonos.mp4",
    "calle": ROOT + "/videos-v5/fuentes/outfit-calle.mp4",
}
PH = {
    "marron": ROOT + "/videos-v7-editorial/editor/public/media/conjunto-marron.jpg",
    "beige": ROOT + "/videos-v7-editorial/editor/public/media/conjunto-beige.jpg",
    "uva": ROOT + "/videos-v7-editorial/editor/public/media/conjunto-uva.jpg",
    "azul": ROOT + "/videos-v7-editorial/editor/public/media/azul-crema.jpg",
    "sastrero": ROOT + "/coleccion-v8-editorial/editor/public/media/sastrero.jpg",
}
for _k, _p in PRE.items():
    _p["bg"] = band_bg(_p["bands"])


class Clip:
    def __init__(s, key, t0, n, speed=1.0, zoom=(1.0, 1.045), focus=(0.5, 0.5), bw=None, punch=True):
        s.pre = PRE[key]; s.n = n; s.zoom = zoom; s.focus = focus; s.bw = bw; s.punch = punch
        s.rd = Reader(SRC[key], t0, n, speed)

    def base(s, j):
        j = max(0, min(j, s.n - 1)); im = Image.fromarray(s.rd.get(j))
        sx0, sy0, sx1, sy1 = s.pre["src"]; dx, dy, dw, dh = s.pre["dst"]
        z = s.zoom[0] + (s.zoom[1] - s.zoom[0]) * (j / max(1, s.n - 1))
        if s.punch and j < 8:
            z *= 1 + 0.07 * (1 - eo(j / 8))
        cw = (sx1 - sx0) / z; ch = (sy1 - sy0) / z
        cx = sx0 + (sx1 - sx0) * s.focus[0]; cy = sy0 + (sy1 - sy0) * s.focus[1]
        l = min(max(cx - cw / 2, sx0), sx1 - cw); t = min(max(cy - ch / 2, sy0), sy1 - ch)
        im = im.resize((dw, dh), Image.LANCZOS, box=(l, t, l + cw, t + ch))
        if s.bw and s.bw[0] <= j / FPS < s.bw[1]:
            im = ImageOps.grayscale(im).convert("RGB")
        im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
        cv = s.pre["bg"].copy(); cv.paste(im, (dx, dy))
        if s.pre.get("cover"):
            x0, y0, x1, y1 = s.pre["cover"]; d = ImageDraw.Draw(cv)
            d.rectangle((x0, y0, x1, y1), fill=PAPER); d.rectangle((x0, y0, x0 + 11, y1), fill=OLIVE)
        return cv

    def close(s):
        s.rd.close()


def cover_box(iw, ih, w, h, cx=0.5, cy=0.5, sc=1.0):
    bw_ = min(iw, ih * w / h); bh_ = bw_ * h / w
    cw = bw_ / sc; ch = bh_ / sc
    l = min(max(iw * cx - cw / 2, 0), iw - cw); t = min(max(ih * cy - ch / 2, 0), ih - ch)
    return (l, t, l + cw, t + ch)


def cover(im, w, h, cx=0.5, cy=0.5, sc=1.0):
    return im.resize((w, h), Image.LANCZOS, box=cover_box(im.width, im.height, w, h, cx, cy, sc))


def still(key, t):
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", SRC[key], "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    im = Image.fromarray(np.frombuffer(b, np.uint8).reshape(1280, 720, 3))
    return im.crop(PRE[key]["src"])


class Photo:
    def __init__(s, src, n, k0=(0.5, 0.5, 1.0), k1=(0.5, 0.5, 1.08), dim=None, blur=0):
        im = Image.open(PH[src]).convert("RGB") if isinstance(src, str) else src
        if blur:
            im = im.filter(ImageFilter.GaussianBlur(blur))
        if dim:
            im = ImageEnhance.Brightness(im).enhance(dim)
        s.im = im; s.n = n; s.k0 = k0; s.k1 = k1

    def base(s, j):
        p = eio(max(0, min(j, s.n - 1)) / max(1, s.n - 1))
        cx, cy, sc = [a + (b - a) * p for a, b in zip(s.k0, s.k1)]
        return s.im.resize((W, H), Image.BICUBIC, box=cover_box(s.im.width, s.im.height, W, H, cx, cy, sc))

    def close(s):
        pass


class Static:
    def __init__(s, img, n):
        s.img = img; s.n = n

    def base(s, j):
        return s.img.copy()

    def close(s):
        pass


class Tiles:
    def __init__(s, n, tiles, bg=DARK, rev=0.45):
        s.n = n; s.tiles = tiles; s.bg = bg; s.rev = rev

    def base(s, j):
        t = max(0, j) / FPS; cv = Image.new("RGB", (W, H), s.bg)
        for im, x, y, dl in s.tiles:
            hv = int(im.height * eo((t - dl) / s.rev))
            if hv > 0:
                cv.paste(im.crop((0, 0, im.width, hv)), (x, y))
        return cv

    def close(s):
        pass


class TomaClip:
    """Toma real grabada por la duena: recorte al centro a 9:16, 1080x1920, 30 fps, sin su audio, recortada
    a la duracion del tramo (n cuadros). Si la toma es mas corta se usa entera y se sostiene el ultimo cuadro."""
    def __init__(s, path, n):
        s.path = path; s.n = n; s.p = None; s.cur = -1; s.fr = None; s.fin = False

    def _abrir(s):
        vf = f"crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS}"
        s.p = subprocess.Popen(["ffmpeg", "-v", "error", "-threads", THREADS, "-i", s.path, "-an", "-vf", vf, "-frames:v", str(s.n),
                                "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)

    def get(s, j):
        j = max(0, min(j, s.n - 1))
        if s.p is None and not s.fin:
            s._abrir()
        while s.cur < j and not s.fin:
            b = s.p.stdout.read(W * H * 3)
            if len(b) < W * H * 3:
                s.fin = True; s.close(); break
            s.fr = np.frombuffer(b, np.uint8).reshape(H, W, 3); s.cur += 1
            if s.cur >= s.n - 1:
                s.fin = True; s.close()
        return s.fr

    def base(s, j):
        fr = s.get(j)
        return Image.fromarray(fr).copy() if fr is not None else Image.new("RGB", (W, H), DARK)

    def close(s):
        if s.p:
            s.p.stdout.close(); s.p.kill(); s.p.wait(); s.p = None


def slate_img(title, details, tag="FALTA GRABAR"):
    cv = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(cv)
    x0, y0, x1, y1 = 65, 290, 1015, 1250
    for x in range(x0, x1, 44):
        d.rectangle((x, y0, min(x + 24, x1), y0 + 4), fill=SAND); d.rectangle((x, y1 - 4, min(x + 24, x1), y1), fill=SAND)
    for y in range(y0, y1, 44):
        d.rectangle((x0, y, x0 + 4, min(y + 24, y1)), fill=SAND); d.rectangle((x1 - 4, y, x1, min(y + 24, y1)), fill=SAND)
    paste(cv, make_pill(tag, bg=SAND, fg=INK, size=30), 120, 360)
    y = 470
    for l in title:
        sp = text_sprite(l, "serif", 92, PAPER); paste(cv, sp, 120, y); y += 96
    y += 34
    for l in details:
        sp = text_sprite(l, "sans", 36, SAGE); paste(cv, sp, 120, y); y += 56
    return cv


# ---------- video ----------
class Video:
    def __init__(s, slug, track):
        s.slug = slug; s.track = track; s.b = 60.0 / BPM[track]; s.sc = []; s.ov = []; s.t = 0.0

    def _add(s, make, beats, tr, T):
        a = s.t; s.t += beats * s.b
        f0 = round(a * FPS); n = round(s.t * FPS) - f0
        sc = make(n); sc.start = f0; sc.tr = tr
        sc.T = T if T is not None else {"cut": 0, "curtain": 14, "flash": 8, "slide_l": 10, "slide_u": 10}[tr]
        s.sc.append(sc); return a, s.t

    def clip(s, key, t0, beats, tr="cut", T=None, **kw):
        return s._add(lambda n: Clip(key, t0, n, **kw), beats, tr, T)

    def photo(s, src, beats, tr="cut", T=None, **kw):
        return s._add(lambda n: Photo(src, n, **kw), beats, tr, T)

    def card(s, color, beats, tr="cut", T=None):
        return s._add(lambda n: Static(Image.new("RGB", (W, H), color), n), beats, tr, T)

    def static(s, img, beats, tr="cut", T=None):
        return s._add(lambda n: Static(img, n), beats, tr, T)

    def tiles(s, tiles, beats, tr="cut", T=None, **kw):
        return s._add(lambda n: Tiles(n, tiles, **kw), beats, tr, T)

    def slate(s, title, details, beats, tr="cut", tag="FALTA GRABAR"):
        return s.static(slate_img(title, details, tag), beats, tr)

    def toma(s, path, beats, tr="cut", T=None):
        """Escena con una toma real (archivo de video) en lugar de un cartel."""
        return s._add(lambda n: TomaClip(path, n), beats, tr, T)

    def zoc(s, a, b, kicker, title, sub=None, **kw):
        s.ov.append(ov_zocalo(a + 0.22, b - 0.12, kicker, title, sub, **kw))

    def title(s, a, b, lines, **kw):
        s.ov.append(ov_title(a + 0.08, b - 0.08, lines, **kw))

    def tag(s, a, b, text, x=65, y=300, center=False, pop=False, **kw):
        s.ov.append(ov_sprite(a + 0.1, b - 0.08, make_pill(text, **kw), x, y, center=center, pop=pop))

    def big(s, a, b, text, y=560, size=300, color=PAPER, cx=None):
        sp = text_sprite(text, "bold" if text.strip().isdigit() else "serif", int(size * 0.8) if text.strip().isdigit() else size, color, shadow=12)
        s.ov.append(ov_sprite(a + 0.04, b - 0.05, sp, int(cx - sp.width / 2) if cx is not None else 0, y, center=cx is None, pop=True, din=0.22))

    def end(s, question, kw, beats=5, tr="curtain", verb="Escribinos"):
        a, b = s.card(OLIVE, beats, tr)
        s.ov.append(ov_sprite(a + 0.25, b, make_logo(250), 0, 330, center=True, pop=True, dout=0.01))
        s.ov.append(ov_title(a + 0.4, b + 1, question, size=112, y=640, align="center", shadow=0, lh=0.98))
        y = 640 + len(question) * 114 + 46
        s.ov.append(ov_sprite(a + 0.75, b + 1, text_sprite(verb, "sans", 38, SAGE), 0, y, center=True))
        s.ov.append(ov_sprite(a + 0.9, b + 1, make_pill(kw, bg=PAPER, fg=INK, size=46, padx=40, pady=14, tracking=5), 0, y + 64, center=True, pop=True))
        s.ov.append(ov_sprite(a + 1.05, b + 1, text_sprite("por mensaje · @indigopy_", "sans", 36, SAGE), 0, y + 176, center=True))
        return a, b

    # ----- render -----
    def frame(s, i):
        k = max(n for n, sc in enumerate(s.sc) if sc.start <= i)
        act = None
        for m in range(1, len(s.sc)):
            T = s.sc[m].T; b0 = s.sc[m].start - T // 2
            if T and b0 <= i < b0 + T:
                act = (m, (i - b0) / T)
        if act is None:
            cv = s.sc[k].base(i - s.sc[k].start); post = None
        else:
            m, p = act; out, inn = s.sc[m - 1], s.sc[m]; tr = inn.tr; post = (tr, p)
            if tr in ("curtain", "flash"):
                src = out if p < 0.5 else inn; cv = src.base(i - src.start)
            else:
                A = out.base(i - out.start); B = inn.base(i - inn.start); cv = Image.new("RGB", (W, H), DARK)
                if tr == "slide_l":
                    off = int(eio(p) * W); cv.paste(A, (-off, 0)); cv.paste(B, (W - off, 0))
                else:
                    off = int(eio(p) * H); cv.paste(A, (0, -off)); cv.paste(B, (0, H - off))
                post = None
        t = i / FPS
        for (t0, t1, fn) in s.ov:
            if t0 <= t < t1:
                fn(cv, t)
        if post:
            tr, p = post; d = ImageDraw.Draw(cv)
            if tr == "curtain":
                if p < 0.5:
                    x1 = int(eio(p * 2) * (W + 60)); d.rectangle((0, 0, x1, H), fill=OLIVE); d.rectangle((x1 - 26, 0, x1, H), fill=SAND)
                else:
                    x0 = int(eio((p - 0.5) * 2) * (W + 60)); d.rectangle((x0, 0, W, H), fill=OLIVE); d.rectangle((x0, 0, x0 + 26, H), fill=SAND)
            else:
                a = (1 - abs(2 * p - 1)) ** 1.2 * 0.92
                cv = Image.blend(cv, Image.new("RGB", (W, H), PAPER), a)
        return cv

    def total(s):
        return round(s.t * FPS)

    def render(s, outdir=None):
        outdir = outdir or OUT; os.makedirs(outdir, exist_ok=True)
        tmp = os.path.join(outdir, s.slug + ".video.mp4"); fin = os.path.join(outdir, s.slug + ".mp4")
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                "-threads", THREADS, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                                "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", tmp], stdin=subprocess.PIPE)
        N = s.total()
        for i in range(N):
            enc.stdin.write(s.frame(i).tobytes())
        enc.stdin.close(); enc.wait()
        for sc in s.sc:
            sc.close()
        D = N / FPS
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-i", AUDIO % s.track,
                            "-filter:a", f"atrim=0:{D:.3f},afade=t=out:st={D - 1.0:.3f}:d=1.0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
                            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", fin])
        if r.returncode == 0:
            try:
                os.remove(tmp)
            except OSError:  # carpetas donde no se puede borrar: queda el .video.mp4 intermedio
                pass
        return fin, D

    def stills(s, times, outdir):
        os.makedirs(outdir, exist_ok=True); res = []
        for t in times:
            i = min(s.total() - 1, max(0, round(t * FPS)))
            p = os.path.join(outdir, f"{s.slug}_{t:05.2f}.jpg"); s.frame(i).save(p, quality=88); res.append(p)
        for sc in s.sc:
            sc.close()
        return res
