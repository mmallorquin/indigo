# Índigo PY · v9 · 30 videos con zócalos y transiciones

30 videos verticales 1080 × 1920 a 30 fps, H.264 + AAC, armados el 9 de noviembre de 2026 solo con material real de esta carpeta. No se usó IA generativa: recorte, composición, texto animado y las pistas instrumentales propias de `videos-v6-olivo`.

Los guiones, la tabla resumen y el calendario están en el documento "Índigo PY · 30 guiones de video para Reels y TikTok".

## Estado de cada video

**Listos para publicar (15):** 01, 02, 03, 04, 05, 06, 09, 13, 14, 15, 16, 17, 23, 25, 26.

**Falta completar un dato en pantalla (6):** 08 (composición de la tela), 18 (costo y plazo de envío), 20 (costo de envío y condiciones de pago), 27 (precio y talles), 29 (precio y talles), 30 (fecha de disponibilidad). El texto dice [COMPLETAR] donde va el dato.

**Plantillas con tomas por grabar (9):** 07, 10, 11, 12, 19, 21, 22, 24, 28. Los carteles "FALTA GRABAR" indican el plano, la duración y el lugar de cada toma.

## Antes de publicar

- Confirmar qué jean es Mom y cuál es Flare (videos 09 y 27).
- Confirmar los nombres de color: "terracota" en la polera canelada y "camel" en el sastrero.
- El material de origen es 720p bajado de Instagram con texto incrustado. Se recortó para sacar ese texto y se escaló; con los originales del celular la nitidez mejora.
- La música es instrumental propia. En Edits se puede cambiar por un audio de la biblioteca.

## Carpetas

- `finales/`: los 30 MP4.
- `qa/`: seis hojas de contacto, cinco videos por hoja.
- `motor/`: el código que los genera.

## Volver a renderizar

Requiere Python 3 con Pillow y NumPy, y FFmpeg en el PATH.

```
python3 videos-v9-zocalos/motor/specs.py 27        # un video
python3 videos-v9-zocalos/motor/specs.py all       # los 30
python3 videos-v9-zocalos/motor/specs.py still 27 1.5 4.0   # cuadros de prueba
```

Los textos, tiempos y fuentes de cada video están en `motor/specs.py`: para cargar un precio se reemplaza `[COMPLETAR]` en la función del video (`v27`, `v29`...) y se vuelve a renderizar. Colores, tipografías, zócalo y transiciones están en `motor/engine.py`.

## Uso nuevo (v9.1): un comando y un archivo de datos

Todos los datos variables (precios, talles, colores, envío, pago, alturas, nombres, fechas y confirmaciones) están en `motor/datos.json`. Lo que falta está en `null`. La regla es dura: nunca se inventa ni se rellena un dato. Un video con algún dato en `null` queda pendiente, no se renderiza como final y se imprime un aviso con el número de video y el campo.

```
python3 motor/lote.py --dias 7              # valida, renderiza los videos completos y arma el calendario
python3 motor/lote.py --dias 15
python3 motor/lote.py --dias 7 --plan       # solo validación + calendario + datos-faltantes.md (no renderiza)
python3 motor/lote.py --solo 27,29          # solo esos videos
python3 motor/lote.py --dias 7 --datos motor/datos.ejemplo.json   # otro archivo de datos
python3 motor/lote.py --dias 15 --max 7 --salida lotes/2026-11-10_15dias   # tandas: renderiza hasta 7 y, con --salida, retoma saltando los MP4 ya hechos
```

- Salida: `lotes/AAAA-MM-DD_Ndias/` (carpeta nueva por corrida) con los MP4 completos y `calendario.md` (un video por día, sin repetir; si los listos no alcanzan, lo dice). `finales/` y `qa/` no se tocan.
- `datos-faltantes.md` (junto a este LEEME, y copia dentro de cada lote) se regenera en cada corrida: lista por video cada dato que falta, las confirmaciones pendientes y las tomas por grabar de las plantillas. Está escrito para que la dueña de la tienda lo complete sin leer código; después se cargan las respuestas en `motor/datos.json` (reemplazar `null` por el texto entre comillas; los precios van solo con el número, el video agrega "Gs.").
- Confirmaciones (`confirmaciones` en `datos.json`): nombre que se muestra para jean negro y jean azul (hoy Flare y Mom), "Terracota" y "Camel". Con `"confirmado": false` solo se avisa antes de publicar; si el nombre es otro, se cambia `nombre` y se pone `true`.
- Plantillas (07, 10, 11, 12, 19, 21, 22, 24, 28): tienen carteles FALTA GRABAR, así que el comando no las arma como finales aunque tengan todos los datos; sus tomas figuran en `datos-faltantes.md`.
- `motor/datos.ejemplo.json` tiene valores ficticios ("EJEMPLO ...") solo para pruebas. Las carpetas de lote hechas con él terminan en `_EJEMPLO` y llevan un aviso: NO PUBLICAR.
- `python3 motor/specs.py 27 [--datos ruta]` y `specs.py still 27 1.5 4.0` siguen funcionando; los cuadros de prueba van a `work/prueba/stills/` y los videos pendientes se saltan con aviso.
- FFmpeg usa 2 hilos por defecto (variable `INDIGO_THREADS`). En este equipo: `$HOME/venvs/indigo/bin/python` con `PATH=$HOME/bin:$PATH` (FFmpeg de imageio-ffmpeg).
- Respaldo de los originales de engine.py y specs.py: `motor/_respaldo-2026-11-09/`.
- Nota: la sección "Volver a renderizar" de arriba sigue válida, pero el `[COMPLETAR]` ya no se reemplaza en `specs.py`: se carga el dato en `datos.json`.

## Tomas nuevas en las plantillas (v9.2)

Las plantillas (07, 10, 11, 12, 19, 21, 22, 24) tienen carteles "FALTA GRABAR". Ahora cada cartel de toma se reemplaza por el clip real cuando el archivo existe.

- Los clips van en `tomas/` con nombre fijo por hueco: `NN_tomaK.mp4` o `.mov` (sin distinguir mayúsculas). El número y el orden salen de los carteles de cada plantilla; la lista exacta, qué grabar y la duración mínima están en `tomas/LEEME.md` y en la sección 3 de `datos-faltantes.md`.
- El clip se recorta al centro a 9:16, se escala a 1080 × 1920 a 30 fps, se corta a la duración del tramo y se le quita su audio (el video conserva la música). Zócalos, textos y transiciones son los que la plantilla ya definía.
- Si el clip es más corto que el tramo: se usa entero, se sostiene el último cuadro y el comando AVISA cuántos segundos faltan (también en `calendario.md`).
- Video 22, tomas 2 a 5 (carteles VOZ): el cartel trae el texto exacto del subtítulo y se muestra como zócalo sobre el clip. Los carteles que solo describen qué decir no llevan texto (queda anotado en `tomas/LEEME.md`).
- Video 28: su cartel "FALTA COMPLETAR" es de datos, no de toma. Con prenda, unidades y talles cargados en `datos.json` el cartel se quita y el video queda listo sin tomas (dura 4 tiempos menos que la plantilla).
- Una plantilla pasa a "lista" solo con todas sus tomas y todos sus datos. Con tomas parciales sigue como plantilla y el aviso nombra los archivos exactos que faltan.
- `--tomas ruta` (en `lote.py` y `specs.py`) apunta a otra carpeta de tomas. Si esa carpeta tiene un archivo `EJEMPLO.txt` (clips de prueba), todo lo armado sale en carpetas `_EJEMPLO` y no se toca el `datos-faltantes.md` real.

```
python3 motor/lote.py --dias 7 --plan                                  # qué tomas faltan y qué videos hay
python3 motor/lote.py --solo 19 --tomas otra/carpeta                    # armar la 19 con tomas de otra carpeta
python3 motor/specs.py 07 --tomas otra/carpeta                          # un video
```

- Respaldo de los originales de engine.py, specs.py y lote.py antes de este cambio: `motor/_respaldo-2026-11-10/`.
- Nunca se dejan clips de prueba en `tomas/`: ahí solo van las tomas reales.
