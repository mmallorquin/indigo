# Índigo Py — entrega v4

Mirar `editorial.mp4` y `energia.mp4` para elegir qué subir. Ambos duran 20 s, muestran ropa real y cierran con “Escribinos JEANS por WhatsApp”. Editorial utiliza serif y movimiento suave; Energía utiliza tipografía de impacto y más percusión. Los archivos `*-sin-musica.mp4` conservan la misma imagen sin audio.

Planificación: `PREPRODUCCION.md`. Guiones, captions y prompts por tramo: `GUIONES-Y-PROMPTS.md`. Prompt reutilizable: `PROMPT-MAESTRO.md`. Fuentes y referencias: `FICHAS-Y-FUENTES.md`. Las verificaciones de la entrega se documentan en `CONTROL-DE-CALIDAD.md`.

Portadas: `editorial-portada.jpg` y `energia-portada.jpg`, también en PNG. Fotogramas de diseño: `*-gancho`, `*-demostracion` y `*-cierre`. Láminas de persona y producto: `referencias/`. Los proyectos nativos editables están en `editorial/` y `energia/` con medios y tipografías.

La fuente es 720×1280; el recorte 590×1048 retira el título incrustado. Los masters son 1080×1920, pero no recuperan el detalle del jean perdido en el archivo comprimido. Para primeros planos con más detalle, usar originales o una grabación nueva del mismo SKU.

## Reconstrucción

Se requieren FFmpeg, Python con NumPy y Pillow, y Higgsedit compatible con motion por palabra y revelados de frame. Los MP4 terminados se pueden usar directamente. No se requiere generar personas o ropa.

1. Ejecutar `python3 preparar-montaje.py`: crea `beats.json`, `timeline.json` y `montaje-base.mp4` desde `source.mp4`.
2. Conservar los proyectos y fuentes incluidas: Editorial tiene Playfair Display 400 y DM Sans 400/700; Energía tiene Anton 400 y DM Sans 400/700.
3. Ejecutar `INDIGO_ROOT="/ruta/absoluta/a/videos-v4" higgsedit build editar.jsx`. Este build reemplaza la timeline: guardar copia si hubo cambios manuales.
4. Renderizar cada proyecto en su archivo `*-sin-musica.mp4`, con salida absoluta, H.264 de 8 bits, 30 fps y bitrate 10M. Por ejemplo: `higgsedit render /ruta/absoluta/a/videos-v4/editorial --out /ruta/absoluta/a/videos-v4/editorial-sin-musica.mp4 --depth 8 --bitrate 10M --workers 2`.
5. Ejecutar `python3 crear-sonido.py` y `python3 finalizar.py`.
6. Ejecutar `python3 control-tecnico.py` y revisar los exports y las hojas de cuadros. Los controles técnicos automáticos no sustituyen esa revisión visual.

Se utiliza un montaje continuo para evitar saltos de búsqueda entre clips en el renderer. Las selecciones originales quedan editables por cuadro en el script y JSON; textos y animaciones quedan editables en los proyectos nativos.

La música instrumental se sintetizó sin muestras externas. No se agregó voz, canción de redes, precio, urgencia, stock, plazo nacional ni financiación. No se publicaron los videos ni se activaron anuncios.
