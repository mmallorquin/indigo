# Controles de entrega — v4

Revisión realizada el 9 de octubre de 2026, hora de Paraguay (10 de octubre UTC). Estos controles verifican los archivos entregados; no demuestran resultados de venta.

## Antes del master

Se revisaron gancho, demostración y cierre de ambas direcciones en fotogramas nativos. Se exportó una prueba de Energía de 4,5 s y se inspeccionaron 12 cuadros consecutivos entre 1,80 y 2,17 s: salida del gancho, corte real y revelado del título siguiente. No se observó arrastre de la prenda ni una transformación generada.

Se aumentaron los tamaños de “Escribinos”, “JEANS” y “por WhatsApp”, y se volvió a construir y revisar el cierre antes de los renders completos. La prueba breve inicial conserva los títulos del gancho; el cierre actualizado se verifica en los masters.

## Masters

| Archivo | Duración | Imagen | Audio | Tamaño |
|---|---|---|---|---|
| editorial.mp4 | 20,000 s | H.264, 1080×1920, 30 fps, 600 cuadros | AAC estéreo, 48 kHz | 25.673.989 bytes |
| energia.mp4 | 20,000 s | H.264, 1080×1920, 30 fps, 600 cuadros | AAC estéreo, 48 kHz | 25.620.252 bytes |
| editorial-sin-musica.mp4 | 20,000 s | Misma imagen del master con música | Sin audio | 25.168.126 bytes |
| energia-sin-musica.mp4 | 20,000 s | Misma imagen del master con música | Sin audio | 25.120.304 bytes |

FFmpeg decodificó los cuatro archivos completos sin errores. El hash SHA-256 del flujo de video comprimido coincide entre cada versión con música y su master silencioso: la mezcla de audio no alteró la imagen. Probes y hashes están en `datos-tecnicos.json`.

Se revisaron las dos hojas completas a 4 cuadros por segundo, 80 muestras por pieza (`*-qa.jpg`). No se observaron los desplazamientos verticales del original en los tramos seleccionados, recortes del cuerpo, deformaciones ni texto sobre cintura o piernas. Las pausas dejan la prenda visible. Este muestreo no equivale a inspeccionar individualmente los 600 cuadros.

Se inspeccionaron además 6 cuadros consecutivos por pieza alrededor del cambio final a 18,5 s (`cambio-final-cuadros.jpg`): el CTA permanece estable sobre el corte al outfit negro. Los cierres reales de ambos masters se revisaron reducidos a 360×640 (`*-final-cierre.jpg`). El texto no cubre el rostro y la acción a WhatsApp se lee.

Los dos MP4 se reprodujeron en Chrome hasta su final. El elemento de video informó duración 20 s, tiempo actual 20 s, `ended=true` y dimensiones 1080×1920, sin error de reproducción. Se verificó el cuadro final visible. No se hizo una escucha crítica en distintos dispositivos ni una vista previa dentro del compositor de Instagram/TikTok.

## Audio

Medición sobre AAC final con loudnorm: Editorial, −16,19 LUFS integrados y −4,02 dBTP; Energía, −16,92 LUFS y −1,38 dBTP. No se midieron picos por encima de 0 dBTP. La normalización de producción apuntó a −16 LUFS y −2 dBTP; el master energético tiene un pico mayor que ese objetivo después de la codificación AAC, todavía bajo 0. Los registros están en `*-audio-control.txt`.

## Límites y siguiente revisión

La fuente comprimida de 720×1280 se recorta y escala; 1080p no agrega detalle de tela. El abrigo oculta parte del jean. No hay macro nuevo, espalda completa estable, etiqueta legible, voz ni SKU confirmado. La identidad se conserva con el video real.

Las tipografías están registradas y los medios usan rutas relativas dentro de cada proyecto. Antes de subir, revisar el recorte de portada y superposiciones de la interfaz en el destino, y comprobar el enlace de WhatsApp del perfil. Los archivos no se publicaron. Tampoco se contactaron clientes ni se activaron anuncios.
