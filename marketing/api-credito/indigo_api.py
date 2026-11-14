#!/usr/bin/env python3
"""Indigo PY - trabajos masivos con la API de Anthropic (solo biblioteca estandar).

Flujo:  plan -> enviar (lote Batch, mitad de precio) -> estado -> bajar -> juez
        ahora = lo mismo en tiempo real (sin esperar al lote)
Tareas: catalogo | contenido | dms | juez
La API key NO va en este archivo: variable ANTHROPIC_API_KEY o ~/.config/indigo/api_key
"""
import argparse, base64, concurrent.futures as cf, json, os, pathlib, re, sys, time
import urllib.error, urllib.request

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent                      # carpeta indigo-py-marketing
OUT = AQUI / "salida"
API = "https://api.anthropic.com/v1"
MODELOS = {"haiku": "claude-haiku-5-5", "sonnet": "claude-sonnet-5-5", "opus": "claude-opus-5-5"}
# USD por millon de tokens (entrada, salida), precio estandar. Batch = 50 %.
# Fuente: platform.claude.com/docs/en/about-claude/pricing (14-nov-2026). Haiku: prompts <100k.
PRECIO = {"haiku": (0.10, 0.50), "sonnet": (2.0, 10.0), "opus": (4.0, 20.0)}
CARPETAS_FOTOS = [
    "videos-v6-olivo/work/fuentes-nuevas", "videos-v6-olivo/work/fuentes-nuevas-ui",
    "videos-v6-olivo/work/inventario", "videos-v6-olivo/work/brand",
    "coleccion-v8-editorial/portadas",
]
MT = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}

REGLAS = """Sos el equipo de contenido de Indigo PY (@indigopy_), tienda de ropa femenina de Ciudad del Este, Paraguay.
Escribis en espanol paraguayo cercano, con voseo (vos, escribime, mira), calido y concreto. Sin emojis en exceso.
REGLAS DURAS:
1. NUNCA inventes precio, talle, color exacto, composicion de tela, stock, plazo, costo de envio, condiciones de pago ni fechas. Si el dato falta, escribi [FALTA: nombre del dato] y listalo en datos_pendientes.
2. Nada de escasez ni urgencia falsa ("ultimas unidades", "solo hoy") salvo que el dato real figure en los datos recibidos.
3. No prometas devoluciones, cambios ni garantias: la politica esta pendiente. Marcalo como [FALTA: politica].
4. Indigo compra local y revende; no digas que fabrica ni que tiene taller propio.
5. No uses IA generativa como argumento ni inventes testimonios, resenas o numeros de ventas.
6. Cierres siempre por mensaje directo de Instagram o WhatsApp; pago por transferencia.
Responde SOLO con JSON valido, sin texto antes ni despues."""


# ---------------------------------------------------------------- utilidades
def leer(ruta):
    p = RAIZ / ruta
    return p.read_text(encoding="utf-8") if p.exists() else ""


def contexto():
    partes = [REGLAS, "\n=== CONTEXTO DEL NEGOCIO ===\n" + leer("CONTEXTO-NEGOCIO.md"),
              "\n=== IDENTIDAD VISUAL ===\n" + leer("videos-v6-olivo/IDENTIDAD-VISUAL.md"),
              "\n=== DATOS CONOCIDOS (null = falta) ===\n" + leer("videos-v9-zocalos/motor/datos.json")]
    return "\n".join(partes)


def clave():
    k = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not k:
        p = pathlib.Path.home() / ".config/indigo/api_key"
        if p.exists():
            k = p.read_text().strip()
    if not k:
        sys.exit("Falta la API key. Guardala con el comando del README (no la pegues en el chat).")
    return k


def http(metodo, ruta, cuerpo=None, crudo=False, intentos=5):
    url = ruta if ruta.startswith("http") else API + ruta
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    for i in range(intentos):
        req = urllib.request.Request(url, data=datos, method=metodo, headers={
            "x-api-key": clave(), "anthropic-version": "2023-06-01", "content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                b = r.read()
                return b.decode() if crudo else json.loads(b)
        except urllib.error.HTTPError as e:
            txt = e.read().decode(errors="replace")
            if e.code in (429, 500, 502, 503, 529) and i < intentos - 1:
                time.sleep(2 ** i * 3)
                continue
            sys.exit(f"Error HTTP {e.code}: {txt[:600]}")
        except (urllib.error.URLError, TimeoutError) as e:
            if i < intentos - 1:
                time.sleep(2 ** i * 3)
                continue
            sys.exit(f"Sin conexion con la API: {e}")


def cid(s):
    return re.sub(r"[^a-zA-Z0-9_-]", "-", s)[:64]


def sacar_json(txt):
    t = txt.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    try:
        return json.loads(t)
    except Exception:
        m = re.search(r"\{.*\}", t, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
    return None


# ---------------------------------------------------------------- tareas
def t_catalogo(modelo):
    prompt = ("Mira la imagen y describi SOLO lo que se ve. Devolve JSON con: archivo_tipo (foto de producto / captura de Instagram / "
              "fotograma de video / logo / otro), prendas (lista de {categoria, subtipo, color_visible, estampado, largo, calce_visible, "
              "detalles}), combinaciones_sugeridas (lista de 3 a 5 looks usando lo que se ve), ocasiones_posibles, calidad_para_video (1 a 5 y por que), "
              "problemas (texto incrustado, baja resolucion, recorte), datos_pendientes (todo lo que NO se puede saber mirando: precio, talle, tela, stock).")
    reqs = []
    for c in CARPETAS_FOTOS:
        for f in sorted((RAIZ / c).glob("*")) if (RAIZ / c).exists() else []:
            mt = MT.get(f.suffix.lower())
            if not mt or f.stat().st_size > 4_500_000:
                continue
            b64 = base64.b64encode(f.read_bytes()).decode()
            reqs.append((cid(f"{f.parent.name}__{f.stem}"), {
                "max_tokens": 1500, "system": contexto(),
                "messages": [{"role": "user", "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": mt, "data": b64}},
                    {"type": "text", "text": f"Archivo: {f.name}\n{prompt}"}]}]}, 1700))
    return reqs


def t_contenido(modelo):
    videos = sorted(p.stem for p in (RAIZ / "videos-v9-zocalos/finales").glob("*.mp4"))
    prompt = ("Video de Reels/TikTok titulado \"{t}\" (numero {n}). Generá material de publicacion con variedad real de enfoque. "
              "JSON: {{video, ganchos (8 variantes, maximo 8 palabras cada una), textos_en_pantalla (4), captions (5 variantes de 2 a 4 lineas), "
              "ctas (5, cierre por DM o WhatsApp), hashtags (10 mixtos locales y de moda), guion_voz_en_off (opcional, 40 a 60 palabras), "
              "mejor_horario_sugerido (solo si hay razon; si no, null), datos_pendientes}}")
    reqs = []
    for v in videos:
        n, _, t = v.partition("-")
        reqs.append((cid(f"video-{n}"), {
            "max_tokens": 3500, "system": contexto(),
            "messages": [{"role": "user", "content": prompt.format(t=t.replace("-", " "), n=n)}]}, 600))
    return reqs


SITUACIONES = [
    ("atraer", "Primer mensaje de alguien que vio un reel y escribe 'info' o 'precio'"),
    ("atraer", "Alguien reacciona a una historia con un emoji"),
    ("atraer", "Pregunta '¿tenes este jean en mi talle?' sin decir el talle"),
    ("confianza", "'¿Es real la tienda? ¿Como se que no me estafan?'"),
    ("confianza", "Pide fotos reales o video de la prenda puesta"),
    ("confianza", "Dice que le da miedo comprar sin probar"),
    ("confianza", "Pregunta de donde son las prendas / si son originales"),
    ("talle", "No sabe que talle pedir y da su altura y peso"),
    ("talle", "Entre dos talles, duda cual elegir"),
    ("talle", "Pregunta por la tela y si estira"),
    ("conversion", "Pregunta cuanto sale el envio a Asuncion"),
    ("conversion", "Pregunta cuanto sale el envio al interior (Encarnacion, Pedro Juan Caballero, Concepcion)"),
    ("conversion", "Pregunta como se paga y si piden sena"),
    ("conversion", "Quiere pagar en cuotas o con tarjeta"),
    ("conversion", "Pide descuento"),
    ("conversion", "Dice 'lo pienso' y desaparece (seguimiento a las 24 h)"),
    ("conversion", "Seguimiento a las 72 h a alguien que cotizo y no pago"),
    ("postventa", "Pasar datos de transferencia y confirmar el pedido"),
    ("postventa", "Avisar que el pedido salio con la transportadora"),
    ("postventa", "Pedir una resena/foto despues de la entrega sin presionar"),
    ("postventa", "La prenda no le calza y pide cambio"),
    ("recompra", "Clienta que compro hace un mes: avisar de nuevos ingresos"),
    ("recompra", "Invitar a clienta a traer una amiga"),
    ("fuera_horario", "Mensaje automatico cuando no estan disponibles (sin prometer plazo)"),
    ("fuera_horario", "Alguien escribe un domingo a la noche pidiendo todo urgente"),
    ("local", "Quiere probarse en Ciudad del Este antes de comprar"),
]


def t_dms(modelo):
    prompt = ("Etapa del embudo: {e}. Situacion: {s}.\nEscribi respuestas listas para copiar en DM/WhatsApp. JSON: {{etapa, situacion, "
              "respuestas (3 variantes: breve, calida, con pregunta que avanza la venta), siguiente_paso_sugerido, datos_pendientes}}. "
              "Si la respuesta depende de un dato que falta, dejá [FALTA: ...] en el texto.")
    return [(cid(f"dm-{i:02d}-{e}"), {"max_tokens": 2000, "system": contexto(),
             "messages": [{"role": "user", "content": prompt.format(e=e, s=s)}]}, 300)
            for i, (e, s) in enumerate(SITUACIONES, 1)]


def t_juez(modelo):
    reqs = []
    for tarea in ("contenido", "dms"):
        for f in sorted((OUT / tarea).glob("*.json")) if (OUT / tarea).exists() else []:
            if f.name in ("batch.json", "gasto.json"):
                continue
            cuerpo = f.read_text(encoding="utf-8")
            prompt = ("Sos editor/a senior. Abajo hay candidatos generados para Indigo PY. Evalualos contra las reglas duras y contra la identidad de marca "
                      "(claridad, voseo natural, nada de relleno, ningun dato inventado). JSON: {{archivo, descartar (lista de {{item, motivo}}), "
                      "elegidos (los 3 mejores por categoria con puntaje 1-10 y una linea de por que), version_final_recomendada (texto listo para publicar), "
                      "alertas (datos pendientes o riesgos de promesa)}}.\nARCHIVO: {a}\nCANDIDATOS:\n{c}")
            reqs.append((cid(f"juez-{tarea}-{f.stem}"), {"max_tokens": 3000, "system": contexto(),
                         "messages": [{"role": "user", "content": prompt.format(a=f.name, c=cuerpo)}]}, len(cuerpo) // 3))
    return reqs


TAREAS = {"catalogo": t_catalogo, "contenido": t_contenido, "dms": t_dms, "juez": t_juez}


# ---------------------------------------------------------------- comandos
def construir(tarea, modelo):
    reqs = TAREAS[tarea](modelo)
    return [(c, {"model": MODELOS[modelo], **p}, extra) for c, p, extra in reqs]


def costo_max(reqs, modelo, batch=True):
    pin, pout = PRECIO[modelo]
    f = 0.5 if batch else 1.0
    ent = sum((len(json.dumps(p.get("system", ""))) + 200) / 3.5 + extra for _, p, extra in reqs)
    sal = sum(p["max_tokens"] for _, p, _ in reqs)
    return ent, sal, (ent * pin + sal * pout) / 1e6 * f


def cmd_plan(a):
    tot = 0
    for t in (list(TAREAS) if a.tarea == "todas" else [a.tarea]):
        r = construir(t, a.modelo)
        e, s, c = costo_max(r, a.modelo, not a.ahora)
        tot += c
        print(f"{t:10} {len(r):4} pedidos | entrada ~{e/1e3:7.0f}k tok | salida max {s/1e3:7.0f}k tok | costo maximo ~US$ {c:6.2f} ({a.modelo})")
    print(f"TOTAL costo maximo ~US$ {tot:.2f}  (el real suele ser bastante menor)")


def cmd_enviar(a):
    r = construir(a.tarea, a.modelo)
    if not r:
        sys.exit("No hay pedidos (carpeta vacia o falta la salida previa).")
    _, _, c = costo_max(r, a.modelo)
    if c > a.tope:
        sys.exit(f"Costo maximo US$ {c:.2f} supera el tope US$ {a.tope:.2f}. Subi --tope o reduci la tarea.")
    d = OUT / a.tarea
    d.mkdir(parents=True, exist_ok=True)
    res = http("POST", "/messages/batches", {"requests": [{"custom_id": c, "params": p} for c, p, _ in r]})
    (d / "batch.json").write_text(json.dumps({"id": res["id"], "modelo": a.modelo, "n": len(r), "enviado": time.strftime("%F %T")}))
    print(f"Lote enviado: {res['id']} ({len(r)} pedidos, costo maximo US$ {c:.2f}). Revisa con: estado {a.tarea}")


def _batch(tarea):
    p = OUT / tarea / "batch.json"
    if not p.exists():
        sys.exit(f"No hay lote enviado para {tarea}.")
    return json.loads(p.read_text())


def cmd_estado(a):
    for t in (list(TAREAS) if a.tarea == "todas" else [a.tarea]):
        if not (OUT / t / "batch.json").exists():
            continue
        b = _batch(t)
        r = http("GET", f"/messages/batches/{b['id']}")
        print(f"{t:10} {r['processing_status']:12} {r['request_counts']}")


def guardar(tarea, modelo, items, batch):
    d = OUT / tarea
    d.mkdir(parents=True, exist_ok=True)
    pin, pout = PRECIO[modelo]
    f = 0.5 if batch else 1.0
    ent = sal = ok = mal = 0
    for it in items:
        c, res = it["custom_id"], it["result"]
        if res["type"] != "succeeded":
            mal += 1
            (d / f"{c}.error.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
            continue
        ok += 1
        m = res["message"]
        u = m.get("usage", {})
        ent += u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
        sal += u.get("output_tokens", 0)
        txt = "".join(b.get("text", "") for b in m["content"] if b["type"] == "text")
        j = sacar_json(txt)
        if j is None:
            (d / f"{c}.txt").write_text(txt, encoding="utf-8")
        else:
            (d / f"{c}.json").write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
    usd = (ent * pin + sal * pout) / 1e6 * f
    reg = {"tarea": tarea, "modelo": modelo, "ok": ok, "errores": mal, "tok_entrada": ent, "tok_salida": sal, "usd": round(usd, 4),
           "batch": batch, "fecha": time.strftime("%F %T")}
    with open(OUT / "gasto.jsonl", "a") as g:
        g.write(json.dumps(reg) + "\n")
    print(f"{tarea}: {ok} bien, {mal} con error | entrada {ent:,} tok, salida {sal:,} tok | gasto ~US$ {usd:.3f}")


def cmd_bajar(a):
    b = _batch(a.tarea)
    r = http("GET", f"/messages/batches/{b['id']}")
    if r["processing_status"] != "ended":
        sys.exit(f"Todavia en proceso: {r['request_counts']}")
    txt = http("GET", r["results_url"], crudo=True)
    items = [json.loads(l) for l in txt.splitlines() if l.strip()]
    guardar(a.tarea, b["modelo"], items, True)


def cmd_ahora(a):
    r = construir(a.tarea, a.modelo)[: a.max]
    _, _, c = costo_max(r, a.modelo, False)
    if c > a.tope:
        sys.exit(f"Costo maximo US$ {c:.2f} supera el tope US$ {a.tope:.2f}.")

    def uno(x):
        cidx, p, _ = x
        p = dict(p)
        p["system"] = [{"type": "text", "text": p["system"], "cache_control": {"type": "ephemeral"}}]
        m = http("POST", "/messages", p)
        return {"custom_id": cidx, "result": {"type": "succeeded", "message": m}}

    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        items = list(ex.map(uno, r))
    guardar(a.tarea, a.modelo, items, False)


def cmd_gasto(a):
    p = OUT / "gasto.jsonl"
    if not p.exists():
        return print("Sin gasto registrado todavia.")
    filas = [json.loads(l) for l in p.read_text().splitlines()]
    for f in filas:
        print(f"{f['fecha']}  {f['tarea']:10} {f['modelo']:7} US$ {f['usd']:.3f}")
    print(f"TOTAL registrado: US$ {sum(f['usd'] for f in filas):.3f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nombre, fn in (("plan", cmd_plan), ("enviar", cmd_enviar), ("ahora", cmd_ahora)):
        s = sub.add_parser(nombre)
        s.add_argument("tarea", choices=list(TAREAS) + (["todas"] if nombre == "plan" else []))
        s.add_argument("--modelo", choices=list(MODELOS), default="sonnet")
        s.add_argument("--tope", type=float, default=15.0, help="tope de costo maximo en USD")
        if nombre == "plan":
            s.add_argument("--ahora", action="store_true", help="calcular precio sin descuento Batch")
        if nombre == "ahora":
            s.add_argument("--max", type=int, default=1000)
        s.set_defaults(fn=fn)
    for nombre, fn in (("estado", cmd_estado), ("bajar", cmd_bajar)):
        s = sub.add_parser(nombre)
        s.add_argument("tarea", choices=list(TAREAS) + (["todas"] if nombre == "estado" else []))
        s.set_defaults(fn=fn)
    sub.add_parser("gasto").set_defaults(fn=cmd_gasto)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
