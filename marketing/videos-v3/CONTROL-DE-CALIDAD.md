# Índigo Py — control de calidad v3

## Verificación técnica

Los cuatro MP4 se decodificaron completos con FFmpeg sin errores. Cada video tiene 600 cuadros, 20,000 s, 1080×1920 y 30 fps. H.264 a aproximadamente 10 Mbit/s. Los dos masters con música incluyen AAC estéreo a 48 kHz, aproximadamente 195 kbit/s, y metadatos al inicio para reproducción progresiva.

Se comparó el SHA-256 del flujo de video comprimido de cada pareja con/sin música: ambos coinciden. El audio no modifica la imagen ni su duración. El original no contiene voz ni audio. La música y los acentos se sintetizaron sin muestras externas.

Mediciones del master AAC: looks −16,37 LUFS integrados y −1,22 dBTP; consulta −16,38 LUFS y −1,24 dBTP. No hay picos por encima de 0 dBTP. Las cifras medidas están en los archivos `*-audio-control.txt`; no equivalen a una escucha subjetiva en todos los dispositivos.

## Revisión visual y motion

Se inspeccionó una prueba exportada de tres segundos, la secuencia completa de cada master por muestreo a cuatro cuadros por segundo y los cierres finales a 360×640. Las hojas `*-qa.jpg` conservan ese muestreo; sus tiempos son etiquetas aproximadas de cada intervalo de un cuarto de segundo. También se abrió cada master en Chrome: el reproductor avanzó hasta 20 s y terminó mostrando el CTA sobre la modelo; se verificó el estado final y el cuadro visible de ambos.

Se comprobó producto visible desde el inicio, revelado y salida de títulos, cambio real de outfit al resolver el primer gancho, pasajes con la ropa sin texto, secuencia modelo/talle/ciudad y CTA final legible sobre la modelo en movimiento. Se corrigió el tamaño y la posición del CTA después de la primera prueba para apartarlo del rostro. No hay cabecera sólida permanente, tarjetas, botones falsos ni placa de cierre que sustituya cuatro segundos de imagen real.

El recorte mantiene cabeza, cintura, largo del jean y zapatos en las tomas seleccionadas. Se compararon las combinaciones con la fuente y fichas reales. No se observó un salto a piso vacío o transición vertical de la fuente en las hojas de los masters. No se aplicaron recoloraciones, personas nuevas, ropa generada, detalles o perspectivas artificiales.

La lectura del cierre se revisó mediante una imagen reducida a 360×640; no se afirma una prueba en un teléfono físico ni una publicación en Instagram o TikTok. No se dispone del original limpio en mayor resolución. La fuente 720p y el recorte limitan el detalle de la ropa; exportar a 1080p no lo recupera.

## Estado de entrega

Dos piezas para revisión, con música y sin música, portadas, tres fotogramas de dirección por pieza, fichas, guiones, mapa de motion, prompts, fuentes y proyectos editables. Se delegó únicamente una propuesta breve de textos/captions a gpt-6-luna. La selección de tomas, animación y control final permanecieron en el agente principal.

No se publicaron videos, no se enviaron mensajes y no se activaron anuncios. No se afirman ventas, conversiones, metas o rentabilidad futura. No se usaron modelos de generación de imagen o video.
