# Índigo Py — 10 videos · Colección Olivo

Entrega del 13 de octubre de 2026, lista para revisión humana y publicación manual.

## Revisar y publicar

Abrir `index.html` con un navegador. La galería funciona localmente, sin conexión, con los MP4 y portadas de esta carpeta. Reproducir cada video, copiar su caption y descargar los archivos individuales. No se publicó contenido en ninguna red.

- `finales/`: 10 MP4 H.264, 1080 × 1920, 30 fps, audio AAC estéreo, 18–20 segundos.
- `portadas/`: 10 portadas JPG, 1080 × 1920, extraídas de un fotograma con el gancho legible.
- `captions/` y `CAPTIONS.md`: un caption breve por pieza.
- `INDICE.md`, `indice.json` y `fuentes.csv`: conceptos, prendas, fuentes públicas y CTA.
- `IDENTIDAD-VISUAL.md`: paleta HEX, tipografía, logo y contacto.
- `CONTROL-DE-CALIDAD.md`, `datos-tecnicos.json` y `qa/*-completo.jpg`: controles y revisión de los exports.

## Editar

El proyecto Remotion está en `editor/`. Los textos, tiempos, encuadres y animaciones se pueden editar en `src/CollectionA.tsx`, `CollectionB.tsx`, `CollectionC.tsx` y `Brand.tsx`. `Root.tsx` registra cada video por separado. Los recursos usados están en `public/`; los originales recuperados y su procedencia se conservan en `work/`.

Desde `editor/`:

```sh
npm ci
npm run dev
node scripts/render.mjs final
```

Para exportar una pieza: `node scripts/render.mjs final 06`. Para obtener previews: `node scripts/render.mjs preview 06`. Las dependencias están fijadas en package-lock.json. No es necesario volver a descargar las prendas o el logo.

La música se entrega en diez WAV. Su generador reproducible y mediciones están en `editor/scripts/musica.py` y `licencia/origen.md`. El render aplica una entrada y una salida suaves. Las fuentes Inter y Cormorant Garamond incluyen sus licencias OFL.

`editor/scripts/empaquetar.py` reconstruye el índice, los captions, la galería y el manifiesto de recursos. `editor/scripts/control.py` realiza la decodificación y medición completas, y genera las hojas de contacto; requiere Python con Pillow y FFmpeg/FFprobe.

## Material y decisiones

La colección usa fotografías y clips reales del proyecto y de publicaciones oficiales. Ocho piezas amplían el contenido con prendas y fotografías distintas de los tres clips de v5. Las piezas 04 y 10 usan extractos reales anteriores con otros enfoques; los recortes eliminan los rótulos comerciales históricos de las fuentes. Las fotos están animadas con motion design: no son nuevas grabaciones de las prendas.

La referencia de remeronas mostraba una señal histórica de contenido con IA y su fidelidad no quedó comprobada. Se reemplazó esa idea por una pieza útil sobre cómo consultar. Las demás categorías se distribuyen entre chalecos, básicas, mangas largas, pantalones de vestir, blusas, conjuntos, cuellos, combinaciones y jeans.

Las publicaciones marcadas vendidas se usan como inspiración de publicaciones anteriores, con esa condición indicada. No se afirman precios, stock actual, promociones ni características no verificadas. Para la publicación manual, la tienda puede confirmar las opciones actuales por el WhatsApp público incluido.
