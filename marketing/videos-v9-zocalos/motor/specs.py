#!/usr/bin/env python3
"""Los 30 videos de Indigo PY. Uso: python3 specs.py all | 01 09 ... | still 01 0.5 3.0"""
import sys, os, time, json, re, math, subprocess
from engine import *

# ---------------------------------------------------------------------------
# DATOS VARIABLES. Todo precio, talle, color, nombre, fecha, costo o medida sale de motor/datos.json
# (o del archivo pasado con --datos). Un dato en null = falta: el video queda pendiente, NO se
# renderiza como final y nunca se inventa ni se rellena el valor.
# ---------------------------------------------------------------------------
COMPLETAR = "[COMPLETAR]"
RUTA_DATOS = os.path.join(HERE, "datos.json")
DATOS = {"videos": {}, "confirmaciones": {}}

# ruta -> (que hay que completar, ejemplo del formato, largo maximo recomendado en pantalla)
CAMPOS = {
    "07.altura": ("Altura de la modelo", "1,68 m", 12),
    "07.talle": ("Talle que usa la modelo en el jean wide leg", "38", 12),
    "08.composicion_tela": ("Composición de la tela del pantalón sastrero beige", "98% algodón, 2% elastano", 30),
    "10.persona_a.altura": ("Altura de la persona A", "1,60 m", 12),
    "10.persona_a.talle": ("Talle de la persona A con ese jean", "36", 8),
    "10.persona_b.altura": ("Altura de la persona B", "1,75 m", 12),
    "10.persona_b.talle": ("Talle de la persona B con ese jean", "42", 8),
    "12.medida_tiro_cm": ("Medida del tiro del pantalón sastrero, en centímetros (solo el número)", "30", 5),
    "12.talles_sastrero_camel": ("Talles disponibles del pantalón sastrero camel", "36, 38, 40", 16),
    "18.costo_envio": ("Costo del envío", "Gs. 25.000", 16),
    "18.plazo_envio": ("Plazo de entrega del envío", "2 a 4 días", 16),
    "20.costo_envio": ("Costo del envío (respuesta a '¿Hacen envíos?')", "Gs. 25.000", 22),
    "20.condiciones_pago": ("Condiciones de pago (respuesta a '¿Cómo pago?'; una línea corta, por ejemplo si se pide seña)", "Seña del 50%, resto al recibir", 28),
    "22.nombre": ("Nombre de quien responde los mensajes y habla a cámara", "Ana", 16),
    "27.jean_negro.precio": ("Precio del jean negro (solo el número; el video agrega 'Gs.')", "189.000", 12),
    "27.jean_negro.talles": ("Talles del jean negro", "36 al 42", 16),
    "27.jean_azul.precio": ("Precio del jean azul (solo el número; el video agrega 'Gs.')", "179.000", 12),
    "27.jean_azul.talles": ("Talles del jean azul", "36 al 42", 16),
    "28.prenda": ("Prenda de la que quedan últimas unidades", "Jean negro", 24),
    "28.unidades": ("Cantidad de unidades que quedan (contadas el día de publicar)", "3", 4),
    "28.talles": ("Talles que quedan", "38 y 40", 16),
    "29.precio": ("Precio del conjunto marrón (solo el número; el video agrega 'Gs.')", "320.000", 12),
    "29.talles": ("Talles del conjunto marrón", "36 al 42", 16),
    "29.colores": ("Colores en que viene el conjunto marrón", "Marrón y beige", 28),
    "30.fecha_disponibilidad": ("Fecha desde la que están disponibles los colores de temporada", "1 de diciembre", 18),
}
# confirmaciones: nombre mostrado en pantalla. Si 'confirmado' no es true, se avisa (no bloquea).
CONF_TEXTO = {
    "jean_negro": ("¿El jean negro es Flare o Mom?", ["09", "27"]),
    "jean_azul": ("¿El jean azul es Mom o Flare?", ["09", "27"]),
    "color_terracota": ("¿La polera canelada se llama 'terracota' como color?", ["30"]),
    "color_camel": ("¿El pantalón sastrero se llama 'camel' como color?", ["12"]),
}
SUBJEAN = {"Flare": "se abre desde la rodilla", "Mom": "tiro alto y pierna recta"}
PLANTILLAS = ("07", "10", "11", "12", "19", "21", "22", "24", "28")  # tienen tomas por grabar (carteles FALTA GRABAR)
NOMBRES = {
    "01": "Un jean, cinco looks", "02": "Sumale un blazer", "03": "Outfit en 3 segundos", "04": "Adiviná la prenda", "05": "De gris a color",
    "06": "Tres looks, una pantalla", "07": "Altura y talle", "08": "La tela de cerca", "09": "¿Mom o Flare?", "10": "Mismo jean, dos cuerpos",
    "11": "Caminar, sentarse, agacharse", "12": "Tiro alto de verdad", "13": "Un jean, tres ocasiones", "14": "Regla del color fuerte",
    "15": "Cuatro prendas, tres looks", "16": "Oficina de lunes a viernes", "17": "Una capa cambia todo", "18": "Cómo comprar en tres pasos",
    "19": "Así preparamos tu pedido", "20": "Tres dudas de siempre", "21": "Elegimos prenda por prenda", "22": "Quién te responde",
    "23": "Primero el resultado", "24": "La pila entera primero", "25": "Esperando que me elogien", "26": "Cuenta regresiva a las fiestas",
    "27": "Nuevos ingresos: Mom y Flare", "28": "Últimas unidades", "29": "Ficha con precio y talles", "30": "Colores de temporada",
}
PRUEBA = os.path.abspath(os.path.join(HERE, "..", "work", "prueba"))
# --- tomas reales: la duena deja clips NN_tomaK.mp4/.mov en tomas/ (o en la carpeta de --tomas) ---
BASE = os.path.abspath(os.path.join(HERE, ".."))
TOMAS_DEFECTO = os.path.join(BASE, "tomas")
RUTA_TOMAS = TOMAS_DEFECTO
EXT_TOMAS = (".mp4", ".mov")
_probe, _huecos = {}, {}


def vacio(x):
    if x is None:
        return True
    if isinstance(x, str):
        return (not x.strip()) or "[COMPLETAR" in x
    if isinstance(x, (list, tuple)):
        return not [e for e in x if not vacio(e)]
    return not isinstance(x, (int, float)) or isinstance(x, bool)


def _txt(x):
    if isinstance(x, (list, tuple)):
        return ", ".join(str(e).strip() for e in x)
    return str(x).strip()


def _buscar(ruta):
    """Valor de 'NN.campo.sub' en DATOS['videos'], o None si falta."""
    vid, *ks = ruta.split(".")
    x = DATOS.get("videos", {}).get(vid)
    for k in ks:
        if not isinstance(x, dict) or k not in x:
            return None
        x = x[k]
    return x


def cargar_datos(ruta=None):
    """Carga datos.json (o 'ruta'). Devuelve la lista de avisos de estructura."""
    global DATOS, RUTA_DATOS
    RUTA_DATOS = os.path.abspath(ruta) if ruta else RUTA_DATOS
    with open(RUTA_DATOS, encoding="utf-8") as f:
        DATOS = json.load(f)
    DATOS.setdefault("videos", {}); DATOS.setdefault("confirmaciones", {})
    avisos = []
    for k in CONF_TEXTO:
        c = DATOS["confirmaciones"].get(k)
        if not isinstance(c, dict) or vacio(c.get("nombre")):
            raise SystemExit(f"datos: falta confirmaciones.{k}.nombre en {RUTA_DATOS} (tiene que tener el nombre que hoy se muestra).")
    for vid, campos in DATOS["videos"].items():
        if vid not in NOMBRES:
            avisos.append(f"datos: el video '{vid}' no existe (se ignora).")
    return avisos


def es_ejemplo():
    return bool(DATOS.get("_ejemplo"))


def cargar_tomas(ruta=None):
    """Define la carpeta de tomas (por defecto motor/../tomas)."""
    global RUTA_TOMAS
    RUTA_TOMAS = os.path.abspath(ruta) if ruta else TOMAS_DEFECTO
    if ruta and not os.path.isdir(RUTA_TOMAS):
        raise SystemExit(f"--tomas: no existe la carpeta {RUTA_TOMAS}")
    _huecos.clear()
    return RUTA_TOMAS


def tomas_oficiales():
    return RUTA_TOMAS == TOMAS_DEFECTO


def tomas_ficticias():
    """Una carpeta de tomas con un archivo EJEMPLO.txt contiene clips de prueba (sinteticos)."""
    return os.path.exists(os.path.join(RUTA_TOMAS, "EJEMPLO.txt"))


def es_prueba():
    """Datos o tomas de ejemplo: lo que se arme NO es publicable."""
    return es_ejemplo() or tomas_ficticias()


def buscar_toma(base):
    """Ruta del archivo base.mp4 / base.mov (sin distinguir mayusculas) o None. Devuelve (ruta, otras_rutas)."""
    try:
        mapa = {}
        for a in sorted(os.listdir(RUTA_TOMAS)):
            mapa.setdefault(a.lower(), a)
    except OSError:
        return None, []
    ok = [os.path.join(RUTA_TOMAS, mapa[base + e]) for e in EXT_TOMAS if base + e in mapa]
    return (ok[0] if ok else None), ok[1:]


def duracion_toma(path):
    """Segundos del clip segun ffmpeg -i, o None si no se puede leer como video."""
    if path not in _probe:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path], capture_output=True, text=True)
        m = re.search(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)", r.stderr)
        _probe[path] = (int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))) if (m and "Video:" in r.stderr) else None
    return _probe[path]


def g(vid, *ks):
    """Dato del video para ponerlo en pantalla. Si falta, devuelve [COMPLETAR] (el video queda pendiente y no se renderiza)."""
    x = _buscar(".".join((vid,) + ks))
    return COMPLETAR if vacio(x) else _txt(x)


def conf(k):
    return str(DATOS["confirmaciones"][k]["nombre"]).strip()


def confirmaciones_pendientes(vid=None):
    out = []
    for k, (preg, vids) in CONF_TEXTO.items():
        if vid is not None and vid not in vids:
            continue
        if DATOS["confirmaciones"][k].get("confirmado") is not True:
            out.append((k, preg, conf(k), vids))
    return out


def faltantes(vid):
    return [r for r in CAMPOS if r.split(".")[0] == vid and vacio(_buscar(r))]


def largos_excedidos(vid):
    out = []
    for r, (_, _, mx) in CAMPOS.items():
        if r.split(".")[0] == vid and not vacio(_buscar(r)) and len(g(vid, *r.split(".")[1:])) > mx:
            out.append((r, len(g(vid, *r.split(".")[1:])), mx))
    return out


def estado(vid):
    """'listo' | 'pendiente' (falta algún dato) | 'plantilla' (falta alguna toma; además puede faltar algún dato).
    Listo = todas las tomas del video (si es plantilla) y todos sus datos."""
    if tomas_faltantes(vid):
        return "plantilla"
    return "pendiente" if faltantes(vid) else "listo"


_slate0 = Video.slate
SUBTITULO = "subtítulo en pantalla"  # detalle de los carteles VOZ: el titulo del cartel ES el texto del subtitulo


def _slate(s, title, details, beats, tr="cut", tag="FALTA GRABAR"):
    """Cartel de plantilla. Cartel de DATOS (FALTA COMPLETAR): se quita si los datos del video estan completos.
    Cartel de TOMA: se reemplaza por el clip NN_tomaK si existe; si no, queda el cartel. Registra cada hueco en s.huecos."""
    vid = s.slug[:2]
    if tag == "FALTA COMPLETAR":
        if not faltantes(vid):
            return (s.t, s.t)
        return _slate0(s, title, details, beats, tr, tag)
    if not hasattr(s, "huecos"):
        s.huecos = []
    k = len(s.huecos) + 1
    base = f"{vid}_toma{k}"
    ruta, otras = buscar_toma(base)
    dclip = duracion_toma(ruta) if ruta else None
    h = dict(k=k, base=base, tag=tag, titulo=list(title), detalles=list(details), archivo=None, otras=otras, ilegible=None, clip=None, faltan=0.0, subtitulo=None)
    if ruta and dclip is None:
        h["ilegible"] = ruta; ruta = None
    if ruta:
        a, b = s.toma(ruta, beats, tr)
    else:
        a, b = _slate0(s, title, details, beats, tr, tag)
    dur = s.sc[-1].n / FPS
    h["dur"] = dur; h["dur_min"] = math.ceil(dur * 2 - 1e-9) / 2
    if ruta:
        h["archivo"] = ruta; h["clip"] = dclip
        h["faltan"] = max(0.0, dur - dclip) if dur - dclip > 1.0 / FPS else 0.0
        if [d.strip().lower() for d in details] == [SUBTITULO]:
            h["subtitulo"] = list(title)
            s.ov.append(ov_zocalo_sp(a + 0.22, b - 0.12, make_zocalo_lineas(list(title))))
    s.huecos.append(h)
    s.tomas = getattr(s, "tomas", []) + [(tag, list(title), list(details))]
    return a, b


Video.slate = _slate

PHX = {"marron": 0.44, "beige": 0.52, "uva": 0.59, "azul": 0.58, "sastrero": 0.6}
_ph = {}
PM = 430  # ancho maximo del zocalo junto a una persona


def ph(k):
    if k not in _ph:
        _ph[k] = Image.open(PH[k]).convert("RGB")
    return _ph[k]


def kb(k, z=1.08):
    return dict(k0=(PHX[k], 0.5, 1.0), k1=(PHX[k], 0.46, z))


def strips(items, gap=12, d0=0.1, dd=0.26):
    n = len(items); w = (W - gap * (n - 1)) // n; out = []
    for k, it in enumerate(items):
        im = cover(ph(it), w, H, cx=PHX[it]) if isinstance(it, str) else cover(it[0], w, H, cx=it[1])
        out.append((im, k * (w + gap), 0, d0 + k * dd))
    return out


def panel(v, a, b, kicker, lines, sub=None, size=66):
    y = 1294
    v.ov.append(ov_sprite(a + 0.15, b, text_sprite(kicker, "bold", 23, OLIVE, tracking=4), 44, y, dout=0.01)); y += 46
    for l in lines:
        v.ov.append(ov_sprite(a + 0.25, b, text_sprite(l, "serif", size, INK), 44, y, dout=0.01)); y += int(size * 1.04)
    if sub:
        v.ov.append(ov_sprite(a + 0.4, b, text_sprite(sub, "sans", 28, INK), 44, y + 10, dout=0.01))


def bubble(v, t0, t1, lines, side, y):
    sp = make_bubble(lines, side)
    v.ov.append(ov_sprite(t0, t1, sp, 65 if side == "L" else 1015 - sp.width, y))


LK = dict(focus=(0.55, 0.5))


def v01():
    v = Video("01-un-jean-cinco-looks", 1)
    a, b = v.clip("looks", 0.95, 3, speed=0.5, **LK); v.title(a, b, ["Un jean.", "Cinco looks."], y=380, size=112)
    for k, (name, t0, bt) in enumerate([("Remera negra", 2.05, 3), ("Manga larga lila", 6.3, 4), ("Blazer fucsia", 10.0, 4), ("Verde lima", 18.35, 3), ("Tapado crema", 21.0, 4)]):
        a, b = v.clip("looks", t0, bt, tr="curtain" if k == 4 else "cut", **LK)
        v.zoc(a, b, f"LOOK 0{k + 1} / 05", name, "con jean wide leg", maxw=PM)
    v.end(["¿Cuál es", "el tuyo?"], "JEAN"); return v


def v02():
    v = Video("02-sumale-un-blazer", 2)
    a, b = v.clip("looks", 6.3, 3, **LK); v.title(a, b, ["El mismo look.", "Una prenda más."], y=380, size=84); v.tag(a, b, "ANTES", y=590)
    a, b = v.clip("looks", 12.7, 6, speed=0.8, tr="flash", **LK); v.tag(a, a + 1.5, "DESPUÉS", y=400)
    a2, b2 = v.clip("looks", 15.7, 2, **LK); v.zoc(a + 0.5, b2, "LA PRENDA QUE SUMA", "Blazer fucsia", "sobre básico lila", maxw=PM)
    v.end(["¿Lo sumás?"], "BLAZER", beats=4); return v


def v03():
    v = Video("03-outfit-en-3-segundos", 7)
    a, b = v.clip("looks", 18.75, 10, **LK); v.title(a, a + 1.6, ["Lista en", "3 segundos."], y=380, size=112)
    v.zoc(a + 2.3, b, "EL LOOK", "Tapado crema", "con jean wide leg", maxw=PM)
    v.end(["De entrecasa", "a lista."], "TAPADO", beats=4); return v


def v04():
    v = Video("04-adivina-la-prenda", 6); bt = v.b
    a, b = v.clip("tonos", 16.2, 5, zoom=(2.5, 2.0), focus=(0.6, 0.75), punch=False); v.title(a, b, ["¿Qué prenda", "es?"], y=330)
    for k, n in enumerate("321"):
        v.big(a + (2 + k) * bt, a + (3 + k) * bt, n, y=780, size=300)
    a, b = v.clip("tonos", 18.93, 5, zoom=(1.25, 1.0), tr="flash"); v.zoc(a, b, "ERA ESTA", "Polera canelada", "cuello alto")
    v.end(["¿La", "adivinaste?"], "TELA"); return v


def v05():
    v = Video("05-de-gris-a-color", 3)
    a, b = v.clip("looks", 18.3, 3, speed=0.6, bw=(0, 99), **LK); v.title(a, b, ["Así cambia", "un color."], y=380, size=112)
    a, b = v.clip("looks", 18.3, 4, speed=0.88, tr="flash", zoom=(1.0, 1.08), **LK); v.zoc(a, b, "COLOR 01", "Verde lima", "manga larga", maxw=PM)
    a, b = v.clip("looks", 10.0, 3, zoom=(1.0, 1.08), **LK); v.zoc(a, b, "COLOR 02", "Fucsia", "blazer", maxw=PM)
    v.end(["¿Qué color", "te falta?"], "COLOR", beats=4); return v


def v06():
    v = Video("06-tres-looks-una-pantalla", 5); keys = ["marron", "beige", "uva"]; names = ["Conjunto marrón", "Beige con negro", "Bordó con violeta"]
    a, b = v.tiles(strips(keys), 4, bg=PAPER)
    for k in range(3):
        v.big(a + 0.3 + k * 0.26, b, str(k + 1), y=320, size=210, cx=176 + 364 * k)
    v.tag(a + 1.1, b, "¿1, 2 O 3?", y=1130, center=True, size=46)
    for k, key in enumerate(keys):
        a, b = v.photo(key, 4, tr="slide_l", **kb(key)); v.big(a + 0.2, b, str(k + 1), y=300, size=230, cx=150 if key != "marron" else 930)
        v.zoc(a, b, f"LOOK {k + 1}", names[k], maxw=PM, side="R" if key == "marron" else "L")
    v.end(["¿Cuál es", "más vos?"], "LOOK + NÚMERO"); return v


def v07():
    v = Video("07-altura-y-talle", 8)
    a, b = v.clip("looks", 6.2, 3, **LK); v.title(a, b, [f"Mido {g('07', 'altura')}", f"Talle {g('07', 'talle')}"], y=380, size=78)
    a, b = v.clip("looks", 7.95, 3, speed=0.69, **LK); v.tag(a, b, "PERFIL", y=400)
    a, b = v.clip("looks", 12.9, 4, **LK); v.tag(a, b, "ESPALDA", y=400); v.zoc(a, b, "JEAN WIDE LEG", "Tiro alto", "pierna ancha", maxw=PM)
    v.slate(["Plano de perfil:", "cintura y cadera"], ["Plano medio, 3 s, luz de costado", "Y una caminata hacia cámara, 2 s", "Completar altura y talle reales"], 4)
    v.end(["¿Cuál es", "tu talle?"], "CALCE", beats=4); return v


def v08():
    v = Video("08-la-tela-de-cerca", 4)
    a, b = v.clip("tonos", 3.2, 4, zoom=(1.5, 1.3), focus=(0.5, 0.45)); v.title(a, b, ["Mirá cómo", "cae."], y=330)
    a, b = v.clip("tonos", 6.3, 4); v.tag(a, b, "CINTURA", y=330)
    a, b = v.clip("tonos", 11.6, 3); a2, b2 = v.clip("tonos", 13.6, 3)
    v.zoc(a, b2, "LA TELA DE CERCA", "Pantalón sastrero", f"beige · composición {g('08', 'composicion_tela')}")
    v.end(["¿Lo querés", "ver puesto?"], "SASTRERO", beats=4); return v


def v09():
    v = Video("09-mom-o-flare", 9)
    a, b = v.clip("jeans", 0.1, 4); v.title(a, a + 1.5, ["¿Mom", "o Flare?"], y=330, size=150); jn = conf("jean_negro"); v.zoc(a + 1.2, b, "JEAN NEGRO", jn, SUBJEAN.get(jn))
    a, b = v.clip("jeans", 3.4, 7, tr="curtain"); ja = conf("jean_azul"); v.zoc(a, b, "JEAN AZUL", ja, SUBJEAN.get(ja))
    v.end(["¿Cuál sos?"], "MOM o FLARE"); return v


def v10():
    v = Video("10-mismo-jean-dos-cuerpos", 10)
    v.slate(["Mismo jean,", "dos cuerpos"], ["Una segunda persona con el mismo jean", "Mismo encuadre fijo, frente y perfil", "2 tomas cada una y 1 juntas"], 5)
    T = [(cover(still("looks", 3.0), 534, H, cx=0.55), 0, 0, 0.1), (cover(still("looks", 7.5), 534, H, cx=0.55), 546, 0, 0.35)]
    a, b = v.tiles(T, 7, tr="curtain"); v.tag(a, b, "EJEMPLO DE ENCUADRE", y=300, center=True, bg=SAND)
    v.tag(a + 0.4, b, "PERSONA A", x=65, y=420); v.tag(a + 0.7, b, "PERSONA B", x=611, y=420)
    v.tag(a + 1.0, b, f"MIDE {g('10', 'persona_a', 'altura')} · TALLE {g('10', 'persona_a', 'talle')}", x=65, y=1150, size=26)
    v.tag(a + 1.0, b, f"MIDE {g('10', 'persona_b', 'altura')} · TALLE {g('10', 'persona_b', 'talle')}", x=611, y=1150, size=26)
    v.end(["¿Dudás de", "tu talle?"], "TALLE", beats=4); return v


def v11():
    v = Video("11-caminar-sentarse-agacharse", 10)
    v.slate(["Gancho: cuclillas", "de golpe"], ["Plano de perfil, 2 s, 2 tomas"], 3)
    a, b = v.clip("calle", 0.4, 8, tr="flash"); panel(v, a, b, "PRUEBA DE MOVIMIENTO", ["Caminar:", "pasa."], "Jean wide leg azul", size=66)
    v.slate(["Faltan: sentada", "y escalón"], ["Sentada en plano medio, cruza la pierna", "Sube un escalón, 2 s cada una"], 3)
    v.end(["Cómodo", "de verdad."], "CÓMODO", beats=4); return v


def v12():
    v = Video("12-tiro-alto-de-verdad", 1)
    a, b = v.photo("sastrero", 5, k0=(0.6, 0.2, 1.9), k1=(0.6, 0.22, 1.6)); v.title(a, b, ["Tiro alto", "de verdad."], y=330)
    v.zoc(a + 0.9, b, "PANTALÓN SASTRERO", "Tiro alto", f"medida de tiro: {g('12', 'medida_tiro_cm')} cm")
    v.slate(["Dedo marcando", "la pretina"], ["Detalle de cintura, frente y perfil", "2 tomas de 3 s"], 3)
    a, b = v.photo("sastrero", 5, k0=(0.6, 0.5, 1.0), k1=(0.6, 0.45, 1.12), tr="flash"); v.zoc(a, b, "PANTALÓN SASTRERO", conf("color_camel"), f"talles {g('12', 'talles_sastrero_camel')}", maxw=PM)
    v.end(["Alto", "es alto."], "CINTURA"); return v


def v13():
    v = Video("13-un-jean-tres-ocasiones", 2)
    for t0, wd in [(10.4, "Trabajo."), (22.0, "Salida."), (2.4, "Diario.")]:
        a, b = v.clip("looks", t0, 1, **LK); v.big(a, b, wd, y=400, size=150)
    for k, (t0, t1, kick, name, sub) in enumerate([(10.0, 13.0, "PARA EL TRABAJO", "Con blazer fucsia", None), (21.0, 25.7, "PARA SALIR", "Con tapado crema", "lentes y cartera"), (2.05, 4.4, "PARA TODOS LOS DÍAS", "Con remera negra", None)]):
        a, b = v.clip("looks", t0, 4 if k < 2 else 3, tr="slide_l", **LK); a2, b2 = v.clip("looks", t1, 2, **LK)
        v.zoc(a, b2, kick, name, sub, maxw=PM)
    v.end(["¿Cuál", "necesitás?"], "PLAN"); return v


def v14():
    v = Video("14-regla-del-color-fuerte", 3)
    a, b = v.clip("looks", 10.0, 3, zoom=(1.9, 1.7), focus=(0.56, 0.3)); v.title(a, b, ["¿Miedo al", "fucsia?"], y=380)
    a, b = v.card(DARK, 4, tr="curtain"); v.title(a + 0.2, b, ["Un solo color", "fuerte por look."], size=108, y=600, align="center", shadow=0)
    v.tag(a + 0.9, b, "EL RESTO ACOMPAÑA", y=880, center=True, bg=SAND)
    a, b = v.clip("looks", 15.5, 4, tr="curtain", **LK); v.zoc(a, b, "EJEMPLO 01", "Fucsia + jean", maxw=PM)
    a, b = v.clip("looks", 18.4, 3, **LK); v.zoc(a, b, "EJEMPLO 02", "Verde lima + jean", maxw=PM)
    a, b = v.photo("uva", 3, **kb("uva")); v.zoc(a, b, "EJEMPLO 03", "Violeta + bordó", maxw=PM)
    v.end(["Guardalo para", "cuando dudes."], "FUCSIA"); return v


def v15():
    v = Video("15-cuatro-prendas-tres-looks", 4)
    st = {k: still("tonos", t) for k, t in [("pant", 4.5), ("top", 9.5), ("pol", 17.5), ("gris", 24.0)]}
    T = [(cover(st[k], 534, 954), x, y, 0.1 + i * 0.16) for i, (k, x, y) in enumerate([("pant", 0, 0), ("top", 546, 0), ("pol", 0, 966), ("gris", 546, 966)])]
    a, b = v.tiles(T, 3, bg=PAPER); v.title(a + 0.5, b, ["4 prendas.", "3 looks."], y=760, size=150, align="center", shadow=14)
    for k, (t0, nm) in enumerate([(3.3, "SASTRERO BEIGE"), (8.8, "TOP DRAPEADO"), (16.6, "POLERA CANELADA"), (23.0, "PANTALÓN GRIS")]):
        a, b = v.clip("tonos", t0, 2, tr="curtain" if k == 0 else "cut"); v.tag(a, b, f"{k + 1} · {nm}", y=320)
    a, b = v.clip("tonos", 11.6, 4, tr="curtain"); v.zoc(a, b, "LOOK 01", "Sastrero + top", "beige con beige")
    a, b = v.clip("tonos", 20.6, 4, tr="curtain"); v.zoc(a, b, "LOOK 02", "Gris + polera")
    T2 = [(cover(st["pant"], 534, H), 0, 0, 0.1), (cover(st["pol"], 534, H), 546, 0, 0.3)]
    a, b = v.tiles(T2, 4, tr="curtain", bg=PAPER); v.zoc(a + 0.5, b, "LOOK 03", "Sastrero + polera")
    v.end(["La base de", "tu placard."], "NEUTROS"); return v


def v16():
    v = Video("16-oficina-lunes-a-viernes", 5)
    bz = still("looks", 11.0)
    a, b = v.tiles(strips(["marron", "beige", (bz, 0.55), "uva", "azul"], gap=10, dd=0.16), 3, bg=PAPER)
    for k, d in enumerate("LMMJV"):
        v.big(a + 0.2 + k * 0.16, b, d, y=310, size=130, cx=104 + 218 * k)
    v.title(a + 0.9, b, ["La semana", "resuelta."], y=820, size=120, align="center", shadow=14)
    for day, src, name in [("LUNES", "marron", "Conjunto marrón"), ("MARTES", "beige", "Beige con negro"), ("MIÉRCOLES", None, "Blazer fucsia y jean"), ("JUEVES", "uva", "Bordó con violeta"), ("VIERNES", "azul", "Tapado crema y jean")]:
        if src:
            a, b = v.photo(src, 4, tr="slide_u", **kb(src))
        else:
            a, b = v.clip("looks", 10.0, 4, tr="slide_u", **LK)
        v.tag(a, b, day, y=360 if not src else 300, size=40, x=65 if src != "marron" else 700)
        v.zoc(a, b, "LOOK DEL DÍA", name, maxw=PM, side="R" if src == "marron" else "L")
    v.end(["¿Te armamos", "la tuya?"], "OFICINA"); return v


def v17():
    v = Video("17-una-capa-cambia-todo", 6)
    T = [(cover(still("looks", 7.5), 534, H, cx=0.55), 0, 0, 0.1), (cover(still("looks", 11.0), 534, H, cx=0.55), 546, 0, 0.4)]
    a, b = v.tiles(T, 3); v.big(a + 0.2, b, "Sin", y=330, size=170, cx=267); v.big(a + 0.5, b, "Con", y=330, size=170, cx=813)
    a, b = v.clip("looks", 6.3, 3, tr="curtain", **LK); v.tag(a, b, "SIN CAPA", y=400)
    a, b = v.clip("looks", 9.9, 4, tr="flash", **LK); v.tag(a, b, "CON CAPA", y=400); v.zoc(a, b, "LA CAPA", "Blazer fucsia", maxw=PM)
    a, b = v.clip("looks", 21.0, 4, tr="curtain", **LK); a2, b2 = v.photo("azul", 3, **kb("azul"))
    v.zoc(a, b, "OTRA CAPA", "Tapado crema", maxw=PM); v.zoc(a2, b2, "OTRA CAPA", "Tapado crema", "sobre remera y jean", maxw=PM)
    v.end(["Una capa", "y listo."], "CAPA"); return v


def v18():
    v = Video("18-como-comprar-en-tres-pasos", 7)
    a, b = v.photo("marron", 3, dim=0.42, blur=6, **kb("marron")); v.big(a, b, "3", y=330, size=440)
    v.title(a + 0.5, b, ["Comprar son", "3 pasos."], y=900, size=100, align="center")
    for n, lines, key in [("1", ["Mandanos la foto", "y tu talle."], "beige"), ("2", ["Te confirmamos", "disponibilidad", "y precio."], "uva"), ("3", ["Transferencia", "y envío a todo", "el país."], "azul")]:
        a, b = v.photo(key, 6, tr="slide_l", dim=0.42, blur=6, **kb(key)); v.big(a + 0.1, b, n, y=300, size=320, cx=170)
        v.title(a + 0.3, b, lines, y=700, size=96)
        if n == "3":
            v.tag(a + 1.2, b, f"COSTO Y PLAZO: {g('18', 'costo_envio')} · {g('18', 'plazo_envio')}", y=1060, bg=SAND, size=28)
    v.end(["Así de", "simple."], "QUIERO"); return v


def v19():
    v = Video("19-asi-preparamos-tu-pedido", 8)
    v.slate(["Así preparamos", "tu pedido"], ["Cenital sobre una mesa, luz de ventana", "5 planos de 3 s con sonido real", "Sin datos personales a la vista"], 5)
    for k, (w, d) in enumerate([("Doblamos", "Manos doblan la prenda"), ("Envolvemos", "Papel o bolsa, a 1,5×"), ("Tu nombre", "Nota a mano, sin dirección"), ("Listo para enviar", "Paquete cerrado en la mano")]):
        v.slate([w], [d], 4, tr="slide_l", tag=f"TOMA {k + 1} · 3 s")
    v.end(["El próximo puede", "ser el tuyo."], "PEDIDO", beats=4); return v


def v20():
    v = Video("20-tres-dudas-de-siempre", 9)
    a, b = v.photo(still("tonos", 14.0), 24, k0=(0.5, 0.5, 1.0), k1=(0.5, 0.5, 1.15), dim=0.5, blur=7)
    for q, ans, t0, t1 in [("¿Hacen envíos?", ["Sí, a todo el país.", f"Costo: {g('20', 'costo_envio')}"], 0.2, 4.5), ("¿Qué talle me va?", ["Decinos tu altura y tu talle", "habitual y te orientamos."], 4.75, 9.0), ("¿Cómo pago?", ["Por transferencia.", g("20", "condiciones_pago")], 9.25, 13.6)]:
        bubble(v, t0, t1, [q], "L", 430); bubble(v, t0 + 1.25, t1, ans, "R", 610)
    v.end(["¿Otra duda?"], "DUDA"); return v


def v21():
    v = Video("21-elegimos-prenda-por-prenda", 10)
    v.slate(["Mano recorriendo", "perchas"], ["Punto de vista, 2 s, a 1,5×", "Es el gancho del video"], 3)
    a, b = v.clip("jeans", 0.2, 4, tr="flash"); v.title(a, b, ["Así elegimos", "lo que te llega."], y=330, size=96)
    a, b = v.clip("tonos", 22.6, 4); v.tag(a, b, "REVISAMOS COSTURAS", y=330)
    a, b = v.clip("tonos", 13.6, 3); v.tag(a, b, "SOLO LO QUE USARÍAMOS", y=330)
    v.end(["Cada prenda,", "una por una."], "NUEVO"); return v


def v22():
    v = Video("22-quien-te-responde", 1)
    v.slate(["Quién te responde", "los mensajes"], ["Hablado a cámara, plano medio", "Ventana de frente, perchero de fondo", "18 s con el guion del documento"], 5)
    for tg, lines in [("VOZ · 0 a 2 s", ["Hola, soy", f"{g('22', 'nombre')}."]), ("VOZ · 2 a 7 s", ["Soy la que te", "responde."]), ("VOZ · 7 a 13 s", ["Elegimos, te", "asesoramos", "y enviamos."]), ("VOZ · 13 a 18 s", ["Escribime.", "Te respondo yo."])]:
        v.slate(lines, ["Subtítulo en pantalla"], 4, tr="slide_l", tag=tg)
    v.end(["Escribime.", "Te respondo yo."], "HOLA", beats=4); return v


def v23():
    v = Video("23-primero-el-resultado", 2)
    a, b = v.clip("looks", 25.8, 3, **LK); v.title(a, b, ["Así termina."], y=400, size=112)
    a, b = v.clip("looks", 18.4, 3, tr="flash", **LK); v.title(a, b, ["Así empieza."], y=400, size=112); v.zoc(a + 0.4, b, "PASO 1", "El jean", "y un básico", maxw=PM)
    a, b = v.clip("looks", 20.3, 4, **LK); v.zoc(a + 0.5, b, "PASO 2", "La capa", "tapado crema", maxw=PM)
    a, b = v.clip("looks", 22.7, 4, **LK); v.zoc(a, b, "PASO 3", "Los detalles", "lentes y cartera", maxw=PM)
    v.clip("looks", 26.3, 2, tr="flash", **LK)
    v.end(["Tres pasos", "y el look está."], "ARMAR"); return v


def v24():
    v = Video("24-la-pila-entera-primero", 3)
    v.slate(["La pila entera", "primero"], ["Plano medio con la pila en brazos", "6 prendas, 1,5 s cada una", "Cada una tapa el lente al desplegarse"], 4)
    a, b = v.clip("jeans", 0.2, 4, tr="flash"); v.tag(a, b, "1 / 2", y=330, x=65); v.zoc(a, b, "NUEVOS INGRESOS", "Jean negro")
    a, b = v.clip("jeans", 3.5, 7, tr="curtain"); v.tag(a, b, "2 / 2", y=330, x=65); v.zoc(a, b, "NUEVOS INGRESOS", "Jean azul")
    v.end(["¿Cuál te", "llamó?"], "INGRESOS"); return v


def v25():
    v = Video("25-esperando-que-me-elogien", 4)
    a, b = v.clip("calle", 0.2, 5, speed=0.8); panel(v, a, b, "ÍNDIGO PY", ["Esperando que me", "elogien el outfit…"])
    a, b = v.clip("calle", 2.46, 4, punch=False); panel(v, a, b, "ÍNDIGO PY", ["…para decir que", "lo vendo yo."], "Jean wide leg · polera negra")
    v.end(["Sí, lo", "vendo yo."], "OUTFIT", beats=4); return v


def v26():
    v = Video("26-cuenta-regresiva-fiestas", 5)
    a, b = v.photo("azul", 3, dim=0.45, blur=5, **kb("azul")); v.title(a, b, ["Se vienen", "las fiestas."], y=560, size=124, align="center")
    v.tag(a + 0.8, b, "¿YA SABÉS QUÉ TE PONÉS?", y=880, center=True, bg=SAND)
    for occ, key, name in [("CENA DEL TRABAJO", "beige", "Beige con negro"), ("NAVIDAD EN FAMILIA", "marron", "Conjunto marrón"), ("AÑO NUEVO", "uva", "Bordó con violeta")]:
        a, b = v.photo(key, 4, tr="curtain", **kb(key)); v.tag(a, b, occ, y=300, size=36, x=65 if key != "marron" else 560)
        v.zoc(a, b, "EL LOOK", name, maxw=PM, side="R" if key == "marron" else "L")
    v.end(["Pedí con", "tiempo."], "FIESTAS"); return v


def v27():
    v = Video("27-nuevos-ingresos-mom-y-flare", 6); 
    def sub(k):
        return f"Gs. {g('27', k, 'precio')} · Talles {g('27', k, 'talles')}"
    a, b = v.clip("jeans", 0.2, 4); v.big(a, a + 1.2, "Nuevo", y=330, size=220); v.zoc(a + 0.9, b, "NUEVO INGRESO", f"Jean {conf('jean_negro')} negro", sub("jean_negro"))
    a, b = v.clip("jeans", 3.4, 8, tr="curtain"); v.zoc(a, b, "NUEVO INGRESO", f"Jean {conf('jean_azul')} azul", sub("jean_azul"))
    v.end(["Reservá", "el tuyo."], "NUEVOS"); return v


def v28():
    v = Video("28-ultimas-unidades", 7)
    a, b = v.photo(still("jeans", 7.0), 5, k0=(0.55, 0.5, 1.0), k1=(0.55, 0.5, 1.12), dim=0.45, blur=4)
    v.title(a, b, ["Últimas."], y=520, size=190, align="center"); v.tag(a + 0.7, b, f"QUEDAN {g('28', 'unidades')} UNIDADES", y=840, center=True, bg=SAND)
    v.tag(a + 0.9, b, f"{g('28', 'prenda')}", y=760, center=True, bg=PAPER)
    v.tag(a + 1.1, b, f"TALLES: {g('28', 'talles')}", y=930, center=True, bg=PAPER)
    v.slate(["Faltan los datos", "reales"], ["Prenda, unidades y talles", "contados el día de publicar"], 4, tr="curtain", tag="FALTA COMPLETAR")
    v.end(["Cuando se va,", "se va."], "ÚLTIMA", beats=4); return v


def v29():
    v = Video("29-ficha-con-precio-y-talles", 8)
    a, b = v.photo("marron", 8, k0=(0.44, 0.5, 1.0), k1=(0.44, 0.45, 1.14)); v.zoc(a + 0.1, b, "CONJUNTO MARRÓN", f"Gs. {g('29', 'precio')}", f"Talles {g('29', 'talles')}", maxw=PM, side="R")
    a, b = v.photo("marron", 4, k0=(0.42, 0.3, 1.9), k1=(0.42, 0.34, 1.7), tr="flash"); v.tag(a, b, f"COLORES: {g('29', 'colores')}", y=320, bg=SAND)
    v.end(["¿Te mandamos", "más fotos?"], "FICHA"); return v


def v30():
    v = Video("30-colores-de-temporada", 9)
    a, b = v.clip("tonos", 3.2, 4); v.ov.append(ov_strips(a, a + 1.7, [(214, 203, 180), (150, 104, 88), (118, 118, 122)]))
    v.title(a + 1.0, b, ["Llegó la", "temporada."], y=330)
    for k, (t0, nm) in enumerate([(6.3, "Beige"), (16.5, conf("color_terracota")), (22.6, "Gris")]):
        a, b = v.clip("tonos", t0, 4, tr="curtain"); v.zoc(a, b, f"COLOR 0{k + 1}", nm)
    a, b = v.clip("tonos", 13.6, 3); v.zoc(a, b, "DISPONIBLE DESDE", g("30", "fecha_disponibilidad"))
    v.end(["¿Te avisamos", "primero?"], "TEMPORADA"); return v


ALL = {f"{i:02d}": globals()[f"v{i:02d}"] for i in range(1, 31)}

def huecos(vid):
    """Huecos de toma de una plantilla, en orden: dicts con k, base (NN_tomaK), tag, titulo, detalles, dur, dur_min,
    archivo (ruta o None), clip (seg), faltan (seg que hay que sostener), subtitulo, ilegible, otras."""
    if vid not in PLANTILLAS:
        return []
    if vid not in _huecos:
        _huecos[vid] = getattr(ALL[vid](), "huecos", [])
    return _huecos[vid]


def tomas_faltantes(vid):
    return [h for h in huecos(vid) if not h["archivo"]]


def tomas(vid):
    """Tomas de una plantilla: lista de (etiqueta, titulo, detalles)."""
    return [(h["tag"], h["titulo"], h["detalles"]) for h in huecos(vid)]


def nombre_toma(h):
    return f"{h['base']}.mp4"


def avisos_tomas(vid):
    """Avisos sobre los archivos de toma que SI existen: clip mas corto que el tramo, ilegible o duplicado."""
    out = []
    for h in huecos(vid):
        if h["ilegible"]:
            out.append(f"AVISO video {vid}: {os.path.basename(h['ilegible'])} no se pudo leer como video: se ignora y el hueco sigue como cartel.")
        if h["archivo"] and h["faltan"] > 0:
            out.append(f"AVISO video {vid}: {os.path.basename(h['archivo'])} dura {h['clip']:.1f} s y el tramo pide {h['dur']:.1f} s: se usa entera y se sostiene el último cuadro {h['faltan']:.1f} s. "
                       f"Faltan {h['faltan']:.1f} s (grabar al menos {h['dur_min']:g} s).")
        if h["archivo"] and h["otras"]:
            out.append(f"AVISO video {vid}: hay más de un archivo para {h['base']}; se usa {os.path.basename(h['archivo'])} y se ignoran {', '.join(os.path.basename(o) for o in h['otras'])}.")
    return out


def notas_tomas(vid):
    """Notas cortas para el calendario ('Antes de publicar') sobre tomas cortas."""
    return [f"{h['base']} dura {h['clip']:.1f} s: faltan {h['faltan']:.1f} s (último cuadro sostenido)" for h in huecos(vid) if h["archivo"] and h["faltan"] > 0]


def aviso_no_listo(vid):
    e = estado(vid)
    msgs = [f"AVISO video {vid} ({NOMBRES[vid]}): falta el dato '{r.split('.', 1)[1]}' ({CAMPOS[r][0]})" for r in faltantes(vid)]
    if e == "plantilla":
        fal = tomas_faltantes(vid); hay = [h for h in huecos(vid) if h["archivo"]]
        msgs.append(f"AVISO video {vid} ({NOMBRES[vid]}): es plantilla, faltan {len(fal)} de {len(huecos(vid))} tomas en {RUTA_TOMAS}: "
                    + ", ".join(f"{nombre_toma(h)} (o .mov)" for h in fal)
                    + (f". Ya están: {', '.join(os.path.basename(h['archivo']) for h in hay)}" if hay else ""))
    return msgs


if __name__ == "__main__":
    args = sys.argv[1:]
    ruta = None; rtomas = None
    if "--datos" in args:
        k = args.index("--datos"); ruta = args[k + 1]; del args[k:k + 2]
    if "--tomas" in args:
        k = args.index("--tomas"); rtomas = args[k + 1]; del args[k:k + 2]
    for a in cargar_datos(ruta):
        print(a)
    cargar_tomas(rtomas)
    if args and args[0] == "still":
        # los cuadros de prueba van a work/prueba/stills, nunca a finales/
        v = ALL[args[1]]()
        for m in aviso_no_listo(args[1]):
            print(m, "(cuadro de BORRADOR)")
        print("\n".join(v.stills([float(x) for x in args[2:]], os.environ.get("INDIGO_OUT") and os.path.join(OUT, "stills") or os.path.join(PRUEBA, "stills_EJEMPLO" if es_prueba() else "stills"))))
    else:
        ids = sorted(ALL) if (not args or args[0] == "all") else args
        for i in ids:
            if estado(i) != "listo":
                print("\n".join(aviso_no_listo(i)), "-> NO se renderiza como final", flush=True)
                continue
            t = time.time()
            print("\n".join(avisos_tomas(i)), flush=True) if avisos_tomas(i) else None
            fin, D = ALL[i]().render(os.path.join(PRUEBA, "render_EJEMPLO") if es_prueba() else None); print(f"{i} {os.path.basename(fin)} {D:.1f}s render={time.time() - t:.0f}s", flush=True)
