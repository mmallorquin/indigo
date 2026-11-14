# Control de calidad — Índigo Py · Colección Olivo

Revisión realizada el 13 de octubre de 2026 sobre los diez MP4 finales. Archivos preparados para revisión humana y publicación manual.

## Verificación técnica de principio a fin

Los diez exports se decodificaron completos con FFmpeg, incluyendo video y audio. Resultado: cero errores de decodificación y cero segmentos negros con detector de 98 % de píxeles oscuros y duración mínima de 0,05 s.

- Todos: 1080 × 1920, 9:16, 30 fps, H.264, yuv420p, audio AAC de 48 kHz y dos canales.
- Duraciones de video: 18, 19 o 20 s. El contenedor AAC añade entre 0,005 y 0,011 s; no agrega imágenes negras.
- Audio final: aproximadamente −18 LUFS-I. True peaks entre −4,40 y −3,16 dBTP, sin saturación digital.
- Música instrumental original, sin voz ni dependencia del sonido para entender el mensaje. Se aplican envolventes de entrada y salida.

Los valores por archivo, dimensiones, cantidad de fotogramas, tamaños y SHA256 están en `datos-tecnicos.json`.

## Revisión visual de la secuencia completa

Se inspeccionaron las diez hojas de contacto de los MP4 finales, con un fotograma por segundo a lo largo de toda su duración, más el fotograma inicial y el último. También se inspeccionaron previews de cada escena a mayor resolución. Las hojas finales están en `qa/*-completo.jpg`.

Se verificaron ortografía, cierres, contacto, proporciones de personas y prendas, contraste, lectura de los mensajes una vez terminada su entrada, composición, colores de origen y ausencia de rótulos históricos de precios o promociones dentro de los recortes usados.

| Video | Resultado visual |
|---|---|
| 01 Consulta | Collage, dos datos, ejemplo de mensaje y cierre legibles. El ejemplo es texto sugerido, no una conversación ni testimonio. |
| 02 Chalecos | Imágenes limpias, sin icono de reproducción; foco en distintos diseños de la misma referencia. |
| 03 Básicas | Básica y look de inspiración diferenciados; texto modular completo. |
| 04 Mangas largas | Toma verde recortada antes del cambio a remera negra; referencia lila y cierre completos. |
| 05 Sastrero | Vista completa y acercamiento real de cintura; no se modifica la silueta. |
| 06 Blusa | Vista completa y acercamiento al fruncido; máscaras sin textos cortados en su estado final. |
| 07 Conjuntos | Tres combinaciones reales, prendas reconocibles y fotos sin estirar; se retiraron etiquetas que se superponían durante la entrada. |
| 08 Cuellos | Verde y chocolate, notas de inspiración y composición de tres líneas completas. |
| 09 Azul + crema | Look completo y tonos gráficos aproximados; prendas conservan el color de la foto. |
| 10 Jeans | Tramo estable de percha; costura, preguntas y CTA completos. |

Las máscaras y letras escalonadas muestran fragmentos durante su entrada intencional; los mensajes completos permanecen visibles antes del corte siguiente. El gancho queda claro dentro de los primeros dos segundos. El contacto se sostiene en el cierre de cuatro segundos.

## Correcciones aplicadas

1. Se normalizaron los saltos de línea para evitar que apareciera la secuencia literal `\n` y que se desbordaran frases.
2. Se sustituyeron portadas públicas recortadas por originales completos para conjuntos, sastrero, blusa y azul con crema.
3. Se descartaron imágenes con botón de reproducción y la referencia de remeronas cuya fidelidad no quedó verificada.
4. Se ajustaron los acercamientos de cintura y fruncido y el encuadre de las fotos de conjuntos.
5. Se evitó la disolvencia heredada del clip de jeans.
6. Se recortó la toma verde antes del cambio de prenda y se volvió a exportar y comprobar el video 04.

## Galería y paquete

La galería fue abierta en el navegador: se cargan los diez videos con dimensiones correctas, las portadas y los captions. Se comprobó reproducción de un MP4 final. Todos los enlaces locales fueron comprobados contra los archivos entregados. El ZIP incluye los MP4, portadas, captions, editables, fuentes, recursos utilizados y evidencias de control, sin node_modules.

No se afirma disponibilidad actual a partir de las publicaciones históricas. La revisión humana final y la publicación manual corresponden a la tienda.
