#!/usr/bin/env python3
"""Un comando para armar un lote de videos de Indigo PY desde motor/datos.json.

  python3 motor/lote.py --dias 7                 # valida, renderiza los videos completos y arma calendario.md
  python3 motor/lote.py --dias 15
  python3 motor/lote.py --dias 7 --plan          # solo validacion + calendario + datos-faltantes (no renderiza)
  python3 motor/lote.py --solo 27,29             # solo esos videos (los que esten completos)
  python3 motor/lote.py --datos otro.json ...    # otro archivo de datos
  python3 motor/lote.py --tomas otra/carpeta ... # otra carpeta de tomas (por defecto tomas/ junto a LEEME.md)
  python3 motor/lote.py --dias 7 --salida lotes/2026-11-10_7dias   # retoma un lote: salta los MP4 ya hechos
Opciones: --inicio AAAA-MM-DD (primer dia del calendario, por defecto manana), --max N (renderiza como mucho N videos nuevos y sale).
Regla: nunca se inventa un dato. Video con datos en null = pendiente: no se renderiza y se avisa por video y campo.
Plantillas (07, 10, 11, 12, 19, 21, 22, 24): se arman como finales solo con TODAS sus tomas (tomas/NN_tomaK.mp4 o .mov) y todos sus datos."""
import sys, os, shutil, tempfile, time, datetime, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import specs as S  # noqa: E402

BASE = os.path.abspath(os.path.join(HERE, ".."))
DIAS_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def parse_solo(txt):
    ids = []
    for p in txt.split(","):
        p = p.strip()
        if not p:
            continue
        if not p.isdigit() or f"{int(p):02d}" not in S.ALL:
            raise SystemExit(f"--solo: '{p}' no es un video válido (01 a 30).")
        ids.append(f"{int(p):02d}")
    return sorted(set(ids))


def carpeta_nueva(base_dir, nombre):
    os.makedirs(base_dir, exist_ok=True)
    p = os.path.join(base_dir, nombre); k = 2
    while os.path.exists(p):
        p = os.path.join(base_dir, f"{nombre}_{k}"); k += 1
    os.makedirs(p); return p


def seg(x):
    """Segundos con coma decimal: 2,5 s."""
    return f"{x:.1f}".replace(".", ",") + " s"


def md_faltantes(ejemplo):
    L = ["# Datos y tomas que faltan para los videos de Índigo PY", ""]
    if ejemplo:
        L += ["> ATENCIÓN: este informe se generó con datos o tomas de EJEMPLO (ficticios). No es el informe real.", ""]
    ids = sorted(S.ALL)
    listos = [i for i in ids if S.estado(i) == "listo"]
    pend = [i for i in ids if S.estado(i) == "pendiente"]
    plan = [i for i in ids if S.estado(i) == "plantilla"]
    L += [f"Generado el {datetime.date.today().isoformat()} a partir de `{os.path.basename(S.RUTA_DATOS)}`. Completá lo que falta y avisá: los videos se vuelven a armar con un solo comando.", "",
          f"- Videos listos para publicar: {len(listos)} ({', '.join(listos)})",
          f"- Videos que solo esperan un dato: {len(pend)} ({', '.join(pend) or 'ninguno'})",
          f"- Plantillas con tomas por grabar: {len(plan)} ({', '.join(plan) or 'ninguna'})", "",
          "Regla: no se inventa ningún precio, talle, color, nombre ni fecha. Si falta el dato, el video no se arma.", "",
          "## 1. Datos que faltan, video por video", "",
          "Escribí la respuesta después de la flecha. Los precios, solo el número (el video agrega \"Gs.\").", ""]
    hay = False
    for i in ids:
        f = S.faltantes(i)
        if not f:
            continue
        hay = True
        L.append(f"### Video {i} · {S.NOMBRES[i]}" + (" (además necesita tomas, ver punto 3)" if S.tomas_faltantes(i) else ""))
        for r in f:
            preg, ej, mx = S.CAMPOS[r]
            L.append(f"- [ ] {preg}. Ejemplo de cómo escribirlo: _{ej}_ (máximo {mx} caracteres) → ________")
        L.append("")
    if not hay:
        L += ["No falta ningún dato.", ""]
    L += ["## 2. Confirmaciones pendientes", "",
          "No frenan el armado, pero hay que confirmarlas antes de publicar.", ""]
    pc = S.confirmaciones_pendientes()
    for k, preg, nombre, vids in pc:
        L.append(f"- [ ] {preg} Hoy los videos dicen \"{nombre}\" (videos {', '.join(vids)}). → ________")
    if not pc:
        L.append("Todo confirmado.")
    L += ["", "## 3. Tomas por grabar (plantillas)", "",
          f"Estos videos son plantillas: los carteles \"FALTA GRABAR\" marcan cada toma. Dejá cada clip en `{os.path.relpath(S.RUTA_TOMAS, BASE) if S.tomas_oficiales() else S.RUTA_TOMAS}/` con el nombre exacto de abajo "
          "(`.mp4` o `.mov`, da igual si va en mayúsculas). Grabá en vertical. La duración mínima es la del tramo real dentro del video "
          "(redondeada hacia arriba a medio segundo) y puede ser menor que la que dice el cartel. Una plantilla se arma como final solo con todas sus tomas y todos sus datos.", ""]
    for i in S.PLANTILLAS:
        hs = S.huecos(i)
        if not hs:
            continue
        hay = sum(1 for h in hs if h["archivo"])
        L.append(f"### Video {i} · {S.NOMBRES[i]} (tomas: {hay} de {len(hs)})")
        for h in hs:
            que = " ".join(h["titulo"]) + (" - " + "; ".join(h["detalles"]) if h["detalles"] else "")
            que = que.replace(S.COMPLETAR, "(dato pendiente, ver punto 1)")
            if h["archivo"]:
                L.append(f"- [x] `{os.path.basename(h['archivo'])}` ya está (dura {seg(h['clip'])}). Qué era: {que}."
                         + (f" **Corta: faltan {seg(h['faltan'])} (se sostiene el último cuadro).**" if h["faltan"] else ""))
            else:
                L.append(f"- [ ] `{S.nombre_toma(h)}` (o `.mov`) · qué grabar: {que} · duración mínima: {seg(h['dur_min'])} (tramo real {seg(h['dur'])})"
                         + (f" · el subtítulo `{' '.join(h['titulo']).replace(S.COMPLETAR, '(dato pendiente)')}` lo agrega el video solo" if [d.strip().lower() for d in h["detalles"]] == [S.SUBTITULO] else ""))
        L.append("")
    if not any(S.huecos(i) for i in S.PLANTILLAS):
        L.append("No hay plantillas con tomas.")
        L.append("")
    return "\n".join(L)


def archivo(i):
    """Nombre del MP4 del video (mismo nombre que los de finales/)."""
    import glob
    h = sorted(glob.glob(os.path.join(BASE, "finales", f"{i}-*.mp4")))
    return os.path.basename(h[0]) if h else f"{i}-*.mp4"


def md_calendario(prog, listos_fuera, pedidos, inicio, ejemplo, solo, no_listos):
    L = ["# Calendario del lote", ""]
    if ejemplo:
        L += ["> ATENCIÓN: lote hecho con datos o tomas de EJEMPLO (ficticios). NO PUBLICAR estos videos.", ""]
    L += [f"Días pedidos: {pedidos}. Videos listos programados: {len(prog)}." + (f" Solo estos videos: {', '.join(solo)}." if solo else ""), ""]
    if len(prog) < pedidos:
        L += [f"**No alcanzan los videos listos para {pedidos} días: hay {len(prog)}.** Los días {len(prog) + 1} a {pedidos} quedan sin video "
              "(no se repite ninguno). Completá los datos de `datos-faltantes.md` para sumar más.", ""]
    L += ["| Día | Fecha | Video | Archivo | Antes de publicar |", "|---|---|---|---|---|"]
    for k, i in enumerate(prog):
        d = inicio + datetime.timedelta(days=k)
        notas = [f"confirmar «{n}»" for _, _, n, _ in S.confirmaciones_pendientes(i)] + S.notas_tomas(i)
        L.append(f"| {k + 1} | {DIAS_ES[d.weekday()]} {d.strftime('%d/%m')} | {i} · {S.NOMBRES[i]} | `{archivo(i)}` | {'; '.join(notas) or '-'} |")
    for k in range(len(prog), pedidos):
        d = inicio + datetime.timedelta(days=k)
        L.append(f"| {k + 1} | {DIAS_ES[d.weekday()]} {d.strftime('%d/%m')} | (sin video listo) | - | - |")
    if listos_fuera:
        L += ["", f"Listos pero fuera de este calendario (sobran): {', '.join(listos_fuera)}."]
    if no_listos:
        L += ["", "No incluidos por estar incompletos: " + "; ".join(f"{i} ({e})" for i, e in no_listos) + ". Ver `datos-faltantes.md`."]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Arma un lote de videos desde datos.json")
    ap.add_argument("--dias", type=int); ap.add_argument("--solo"); ap.add_argument("--datos")
    ap.add_argument("--plan", action="store_true"); ap.add_argument("--salida"); ap.add_argument("--inicio"); ap.add_argument("--max", type=int)
    ap.add_argument("--tomas", help="carpeta con las tomas NN_tomaK.mp4/.mov (por defecto tomas/)")
    a = ap.parse_args()
    for m in S.cargar_datos(a.datos):
        print(m)
    S.cargar_tomas(a.tomas)
    ejemplo = S.es_prueba()
    solo = parse_solo(a.solo) if a.solo else None
    if a.dias is not None and a.dias < 1:
        raise SystemExit("--dias tiene que ser 1 o más.")
    inicio = datetime.date.fromisoformat(a.inicio) if a.inicio else datetime.date.today() + datetime.timedelta(days=1)
    print(f"Datos: {S.RUTA_DATOS}" + ("  [EJEMPLO: datos ficticios]" if S.es_ejemplo() else ""))
    print(f"Tomas: {S.RUTA_TOMAS}" + ("  [EJEMPLO: tomas ficticias]" if S.tomas_ficticias() else ""))

    # validar
    cand = solo or sorted(S.ALL)
    listos, no_listos = [], []
    for i in cand:
        e = S.estado(i)
        if e == "listo":
            listos.append(i)
        else:
            for m in S.aviso_no_listo(i):
                print(m)
            partes = []
            if e == "plantilla":
                partes.append("plantilla con tomas por grabar: " + ", ".join(S.nombre_toma(h) for h in S.tomas_faltantes(i)))
            if S.faltantes(i):
                partes.append("falta " + ", ".join(r.split(".", 1)[1] for r in S.faltantes(i)))
            no_listos.append((i, " y ".join(partes)))
        for m in S.avisos_tomas(i):
            print(m)
        for r, n, mx in S.largos_excedidos(i):
            print(f"AVISO video {i}: '{r.split('.', 1)[1]}' tiene {n} caracteres (recomendado hasta {mx}); revisá que entre en pantalla.")
    for i in cand:
        for k, preg, nombre, vids in S.confirmaciones_pendientes(i):
            if S.estado(i) == "listo":
                print(f"AVISO video {i}: sin confirmar «{preg}» (hoy dice {nombre}); confirmar antes de publicar.")
    pedidos = a.dias if a.dias is not None else len(listos)
    prog = listos[:pedidos]
    fuera = listos[pedidos:]

    nombre = (f"{datetime.date.today().isoformat()}_{a.dias}dias" if a.dias else f"{datetime.date.today().isoformat()}_solo-{'-'.join(solo or ['todos'])}")
    if ejemplo:
        nombre += "_EJEMPLO"
    if a.plan:
        nombre += "_plan"
    out = os.path.abspath(a.salida) if a.salida else carpeta_nueva(os.path.join(BASE, "lotes"), nombre)
    os.makedirs(out, exist_ok=True)

    falt = md_faltantes(ejemplo)
    # el informe real vive junto a LEEME.md; con datos de ejemplo solo va dentro del lote
    destinos = [os.path.join(out, "datos-faltantes.md")] + ([] if (ejemplo or not S.tomas_oficiales()) else [os.path.join(BASE, "datos-faltantes.md")])
    for p in destinos:
        open(p, "w", encoding="utf-8").write(falt)
    open(os.path.join(out, "calendario.md"), "w", encoding="utf-8").write(md_calendario(prog, fuera, pedidos, inicio, ejemplo, solo, no_listos))
    if ejemplo:
        open(os.path.join(out, "LEEME-EJEMPLO.txt"), "w", encoding="utf-8").write("Videos hechos con datos o tomas ficticios (datos.ejemplo.json o una carpeta de tomas con EJEMPLO.txt). Solo para pruebas. NO PUBLICAR.\n")
    print(f"Salida: {out}\nCalendario: {len(prog)} de {pedidos} días con video listo" + (f" (sobran {len(fuera)})" if fuera else "")
          + (" (NO ALCANZAN los videos listos)" if len(prog) < pedidos else ""))
    print("Informe: " + ", ".join(destinos))

    if a.plan:
        print("Modo --plan: no se renderizó nada."); return
    hechos = 0
    for i in prog:
        v = S.ALL[i](); slug = v.slug; fin = os.path.join(out, slug + ".mp4")
        if os.path.exists(fin):
            print(f"{i} ya existe, se salta ({slug}.mp4)", flush=True); continue
        if a.max is not None and hechos >= a.max:
            print(f"Corte por --max {a.max}: faltan videos. Retomá con: python3 motor/lote.py {' '.join(sys.argv[1:] if not a.salida else sys.argv[1:])} --salida {out}")
            return
        tmp = tempfile.mkdtemp(prefix="indigo_")  # se renderiza fuera de la carpeta del repo y se copia el MP4 final
        try:
            t = time.time(); f, D = v.render(tmp)
            shutil.copyfile(f, fin); hechos += 1
            print(f"{i} {slug}.mp4 {D:.1f}s render={time.time() - t:.0f}s", flush=True)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print(f"Listo: {hechos} videos nuevos en {out}")


if __name__ == "__main__":
    main()
