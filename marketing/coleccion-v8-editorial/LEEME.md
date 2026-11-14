# Índigo · Estudios de prendas

Se entrega el prompt ejecutado, dos Reels de 22 segundos en 1080 × 1920 a 30 fps y dos carruseles de cinco placas en 1080 × 1350. Las fotos son reales del proyecto. No se utilizó grabación nueva, locución ni modelos generadas.

Abrir `index.html` para revisar y descargar las piezas. Los enlaces definitivos de Canva y Figma están en `ENLACES-EDITABLES.json` y en la galería. Ambos carruseles están guardados en Canva con cinco páginas y dimensiones 1080 × 1350. En Figma hay diez frames nativos, cinco componentes fotográficos, diez variables de identidad y estilos tipográficos. Los textos y las fotografías se pueden editar. Las fuentes y referencias están en `INDICE.md`.

## Archivos locales

- `reels/`: MP4 H.264, AAC, BT.709 y faststart, con música instrumental.
- `carruseles/`: diez PNG finales.
- `portadas/` y `captions/`: portadas y textos breves para cada tema.
- `editables/svg/`: diez SVG con fotografías incorporadas y texto vectorial.
- `editables/*-canva.html`: versión paginada con recursos incorporados; es la fuente de las versiones finales guardadas en Canva.
- `editables/*-canva.pdf`: respaldo paginado con texto nativo. Para continuar en Canva, usar sus enlaces finales o el HTML, que conserva mejor los bloques de composición.
- `editor/`: proyecto Remotion y datos de composición, recursos y scripts.
- `qa/`: hojas de contacto de los MP4 y de los diseños revisados.

Las versiones preliminares importadas desde PDF en Canva no son la entrega final: la conversión movía algunos textos. Los diseños entregados llevan «Final» o «Entrega» en el título y fueron importados desde HTML. Los enlaces de la galería apuntan exclusivamente a esas versiones.

## Editar el video

Desde `editor`, ejecutar `npm ci` y `npm run dev`. Las composiciones principales son `14-Neutros` y `15-Pantalones`. Cada escena tiene su propia composición editable. El contenido, posiciones y colores están en `src/contenido.json`, generado por `scripts/contenido.py`; el movimiento se controla en `src/Artwork.tsx`. Las animaciones se calculan por fotograma, sin aleatoriedad.

Para exportar: `node scripts/render.mjs render`, seguido de `python3 scripts/master.py` y `python3 scripts/control.py`. Requiere Node.js, Python 3 con Pillow y NumPy, FFmpeg y FFprobe. Los scripts de exportación de PDF usan además ReportLab, FontTools y Brotli. Los TTF convertidos ya están incluidos junto a sus licencias OFL. No se entregan `node_modules` ni mezclas intermedias.

La música reutiliza las pistas instrumentales 03 y 07 de la colección v6, sintetizadas localmente sin samples externos. La procedencia y el generador se incluyen en `licencia/` y `editor/scripts/musica.py`. El master final se midió después de AAC. Ver `CONTROL-DE-CALIDAD.md`.

Las prendas de publicaciones anteriores sirven como referencias; su disponibilidad, colores y talles se confirman por consulta. No se incorporaron precios, medidas, promociones ni beneficios no verificados. No se publicó ni programó contenido.
