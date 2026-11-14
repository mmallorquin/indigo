#!/usr/bin/env python3
"""Un comando para armar un lote de videos de Indigo PY desde motor/datos.json.

  python3 motor/lote.py --dias 7                 # valida, renderiza los videos completos y arma calendario.md
  python3 motor/lote.py --dias 15
  python3 motor/lote.py --dias 7 --plan          # solo validacion + calendario + datos-faltantes (no renderiza)
  python3 motor/lote.py --solo 27,29             # solo esos videos (los que esten completos)
  python3 motor/lote.py --datos otro.json ...    # otro archivo de datos
  python3 motor/lote.py --dias 7 --salida lotes/2026-11-10_7dias   # retoma un lote: salta los MP4 ya hechos
Opciones: --inicio AAAA-MM-DD (primer dia del calendario, por defecto manana), --max N (renderiza como mucho N videos nuevos y sale).
Regla: nunca se inventa un dato. Video con datos en null = pendiente: no se renderiza y se avisa por video y campo."""
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


def md_faltantes(ejemplo):
    L = ["# Datos que faltan para los videos de Índigo PY", ""]
    if ejemplo:
        L += ["> ATENCIÓN: este informe se generó con datos de EJEMPLO (ficticios). No es el informe real.", ""]
    ids = sorted(S.ALL)
    listos = [i for i in ids if S.estado(i) == "listo"]
    pend = [i for i in ids if S.estado(i) == "pendiente"]
    plan = [i for i in ids if S.estado(i) == "plantilla"]
    L += [f"Generado el {datetime.date.today().isoformat()} a partir de `{os.path.basename(S.RUTA_DATOS)}`. Completá lo que falta y avisá: los videos se vuelven a armar con un solo comando.", "",
          f"- Videos listos para publicar: {len(listos)} ({', '.join(listos)})",
          f"- Videos que solo esperan un dato: {len(pend)} ({', '.join(pend) or 'ninguno'})",
          f"- Plantillas con tomas por grabar: {len(plan)} ({', '.join(plan)})", "",
          "Regla: no se inventa ningún precio, talle, color, nombre ni fecha. Si falta el dato, el video no se arma.", "",
          "## 1. Datos que faltan, video por video", "",
          "Escribí la respuesta después de la flecha. Los precios, solo el número (el video agrega \"Gs.\").", ""]
    hay = False
    for i in ids:
        f = S.faltantes(i)
        if not f:
            continue
        hay = True
        L.append(f"### Video {i} · {S.NOMBRES[i]}" + (" (además necesita tomas, ver punto 3)" if i in S.PLANTILLAS else ""))
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
          "Estos videos son plantillas: los carteles \"FALTA GRABAR\" marcan lo que hay que filmar. Hasta que esas tomas se graben e incorporen, no son videos finales.", ""]
    for i in S.PLANTILLAS:
        L.append(f"### Video {i} · {S.NOMBRES[i]}")
        for tag, titulo, det in S.tomas(i):
            L.append(f"- [ ] {' '.join(titulo)} ({tag}): " + "; ".join(det))
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
        L += ["> ATENCIÓN: lote hecho con datos de EJEMPLO (ficticios). NO PUBLICAR estos videos.", ""]
    L += [f"Días pedidos: {pedidos}. Videos listos programados: {len(prog)}." + (f" Solo estos videos: {', '.join(solo)}." if solo else ""), ""]
    if len(prog) < pedidos:
        L += [f"**No alcanzan los videos listos para {pedidos} días: hay {len(prog)}.** Los días {len(prog) + 1} a {pedidos} quedan sin video "
              "(no se repite ninguno). Completá los datos de `datos-faltantes.md` para sumar más.", ""]
    L += ["| Día | Fecha | Video | Archivo | Antes de publicar |", "|---|---|---|---|---|"]
    for k, i in enumerate(prog):
        d = inicio + datetime.timedelta(days=k)
        notas = [f"confirmar «{n}»" for _, _, n, _ in S.confirmaciones_pendientes(i)]
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
    a = ap.parse_args()
    for m in S.cargar_datos(a.datos):
        print(m)
    ejemplo = S.es_ejemplo()
    solo = parse_solo(a.solo) if a.solo else None
    if a.dias is not None and a.dias < 1:
        raise SystemExit("--dias tiene que ser 1 o más.")
    inicio = datetime.date.fromisoformat(a.inicio) if a.inicio else datetime.date.today() + datetime.timedelta(days=1)
    print(f"Datos: {S.RUTA_DATOS}" + ("  [EJEMPLO: datos ficticios]" if ejemplo else ""))

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
            no_listos.append((i, "plantilla con tomas por grabar" if e == "plantilla" else "falta " + ", ".join(r.split(".", 1)[1] for r in S.faltantes(i))))
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
    destinos = [os.path.join(out, "datos-faltantes.md")] + ([] if ejemplo else [os.path.join(BASE, "datos-faltantes.md")])
    for p in destinos:
        open(p, "w", encoding="utf-8").write(falt)
    open(os.path.join(out, "calendario.md"), "w", encoding="utf-8").write(md_calendario(prog, fuera, pedidos, inicio, ejemplo, solo, no_listos))
    if ejemplo:
        open(os.path.join(out, "LEEME-EJEMPLO.txt"), "w", encoding="utf-8").write("Videos hechos con datos ficticios (datos.ejemplo.json). Solo para pruebas. NO PUBLICAR.\n")
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
