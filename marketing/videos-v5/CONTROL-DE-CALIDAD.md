# Revisión de export — v5

Dos MP4 de 20 segundos, 1080×1920, 30 fps, H.264 de 8 bits, 600 cuadros. Audio AAC estéreo a 48 kHz, aproximadamente 192 kbit/s. Bitrate total medido: 10,59 Mbit/s negro y 10,52 Mbit/s blanco. Cada archivo con música pesa aproximadamente 26 MB.

## Evidencia técnica

- Render nativo de ambos proyectos: diagnóstico vacío, sin fallbacks, 600 cuadros por archivo.
- Decodificación completa de los cuatro MP4 con FFmpeg, sin errores.
- Comparación SHA-256 del flujo de video: imagen idéntica en versión con música y sin música.
- Sonido final medido: negro −16,68 LUFS integrados y −2,67 dBTP; blanco −16,44 LUFS y −2,64 dBTP. Los valores corresponden al audio codificado, no a la medición del WAV anterior.
- Archivos fuente, resolución, duración y hashes registrados en `datos-tecnicos.json`.
- Reproducción en Chrome de ambas piezas: el reproductor llegó a 20/20 s con `ended=true`, sin error de reproducción. Se observaron encuadre y cierre.

## Revisión visual realizada

Se revisaron 80 muestras de cada export a intervalos de 0,25 s; cuadros decodificados de producto, look, mensaje lateral y cierre; y los cierres a 360×640. Las hojas `*-qa.jpg`, `export-verificacion.jpg` y `cierres-telefono.jpg` guardan esa evidencia.

La prueba nativa de cinco segundos cubrió la expansión y contracción de imagen y entrada de TU ESTILO. Se revisaron 24 cuadros consecutivos de esa transición. También se revisaron 24 cuadros del cambio al CTA blanco, desde 15,73 a 16,50 s. La geometría cambia suavemente, el texto se revela y la imagen mantiene proporción. No se observaron destellos fuertes ni transformaciones de la prenda en esos cambios.

Correcciones realizadas antes del master:

1. Un rango del reel de percha mostraba una placa oliva vieja: se cambiaron los cuadros para terminar antes de esa placa.
2. MANERA se recortaba: se redujo el tamaño lateral y retiró el punto final. La palabra completa está visible.
3. MIRÁ/ELEGÍ se ajustó para caber en su columna sin invadir la prenda.
4. El recorte de calle se ajustó para quitar texto incrustado en el borde superior, conservando rostro, torso y cintura.

No se detectaron letras cortadas en los textos estables revisados. Las letras parcialmente visibles durante una entrada o salida son el revelado diseñado. El CTA se mantiene hasta el final, con la imagen todavía en movimiento.

## Límites prácticos

Las fuentes son 720p y algunas tomas se repiten. La toma de calle es un plano medio; no muestra el largo completo del jean. La persona y las prendas conservan el material original. La revisión en teléfono no sustituye la vista previa dentro de Instagram/TikTok antes de subir: allí hay que comprobar el solapamiento con controles y caption del destino. No se publicó ningún archivo.

Estas verificaciones comprueban el archivo y la composición, no predicen consultas ni ventas.
