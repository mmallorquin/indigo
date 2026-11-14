# Índigo Py · tres videos editoriales finales

Entrega del 13 de octubre de 2026. Tres MP4 terminados, verticales de 1080 × 1920 a 30 fps, con fotografías reales de la marca, tipografía animada, diagramas y música instrumental. No necesitan grabación nueva. No tienen locución ni presentador artificial.

Abrir `index.html` para revisar las piezas, descargar MP4 y portadas y copiar los captions. `INDICE.md` registra conceptos, fuentes y CTA; `beat-sheet.json` contiene los tiempos en segundos y fotogramas. `CONTROL-DE-CALIDAD.md` y `datos-tecnicos.json` contienen la verificación de los archivos finales.

## Archivos

- `finales/`: 11-combinaciones, 12-detalles y 13-capas en MP4.
- `portadas/`: una imagen de 1080 × 1920 por pieza.
- `captions/`: texto breve listo para copiar.
- `subtitulos/`: SRT del texto principal en pantalla. Es un recurso de accesibilidad/editorial, no una transcripción de voz. Los MP4 ya contienen sus textos animados.
- `CAPITULOS-YOUTUBE.txt`: capítulos opcionales para un video convencional; no son necesarios en Reels o Shorts.
- `editor/`: fuentes Remotion, dependencias fijadas, imágenes, logo, fuentes tipográficas, WAV y scripts de producción.
- `qa/`: hojas de 40 fotogramas de cada export y mediciones del master.

Las prendas provienen de publicaciones anteriores. Las imágenes sirven como referencias de combinación y diseño; no prometen stock, precios, promociones ni disponibilidad actual. El diagrama de camisa del video 13 es una idea genérica, rotulada como tal, y no una fotografía de un producto en venta. No se agregaron datos de contacto no verificados.

## Editar y reproducir

Requisitos: Node.js, Python 3, NumPy, Pillow, FFmpeg y FFprobe en PATH. Instalar dependencias JS desde `editor`:

```sh
cd editor
npm ci
npm run dev
```

Las composiciones son `11-Combinaciones`, `12-Detalles` y `13-Capas`. Editar `src/Root.tsx` para contenido y tiempos, y `src/Design.tsx` para paleta, tipografía, tarjetas y animaciones. Todos los medios se resuelven desde `public/`; no se consultan redes durante el render.

Para generar otra exportación, desde `editor`:

```sh
mkdir -p ../work ../finales ../portadas ../qa
node scripts/render.mjs render
python3 scripts/master.py
python3 scripts/control.py
```

`render.mjs` escribe mezclas intermedias en `work/` y portadas. `master.py` hace normalización de dos pasadas y escribe los MP4 entregables en `finales/`. `control.py` decodifica todo el archivo, mide audio y formato y genera hojas de contacto. `python3 scripts/sfx.py` regenera los efectos locales. `musica.py` permite regenerar las pistas instrumentales originales; los WAV utilizados ya están incluidos. `entrega.py` regenera el índice, los textos y la galería; si cambia el montaje, actualizar también sus cues.

El ZIP no incluye `node_modules` ni mezclas intermedias. Instalar con `npm ci` antes de editar. Los hashes del manifiesto permiten comprobar los archivos del paquete.

## Adaptación de la guía

Se conservan la estructura gancho–título–desarrollo–cierre, los gráficos explicativos, revelados, comparación y lista, animación determinista, transición musical de cuatro segundos y master de −14 LUFS. La paleta y las familias tipográficas siguen Índigo.

Al elegir una entrega sin grabación ni voz, no corresponden transcripción, eliminación de muletillas, cortes de palabras, seguimiento facial de un video hablado, procesamiento vocal ni pruebas ASR. Las fotografías de personas se encuadran manteniendo sus rostros visibles. La entrega queda lista para revisión humana y publicación manual. No fue publicada.
