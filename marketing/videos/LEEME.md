# Videos de jeans — Índigo Py

Dos ediciones de 24 segundos a partir del reel real de Instagram [DadS-vpOk4k](https://www.instagram.com/indigopy_/reel/DadS-vpOk4k/). No se generó una modelo ni se alteró la prenda. La paleta crema/oliva es una propuesta gráfica para estas piezas.

## Archivos

- `jeans-looks.mp4`: versatilidad, con base instrumental creada para estas piezas.
- `jeans-whatsapp.mp4`: consulta guiada, con la misma base.
- `jeans-looks-sin-musica.mp4` y `jeans-whatsapp-sin-musica.mp4`: masters para elegir otro audio.
- `portada-looks.png` y `portada-whatsapp.png`: fotogramas reales con título.
- `proyecto-videos.zip`: material recuperado, proyectos Higgsedit, portadas, script y base instrumental.

La música de la publicación original no se incorporó. La base se sintetizó con notas y percusión desde el script `crear-musica.py`, sin samples externos.

## Calidad y alcance

Fuente: H.264, 720 × 1280, 30 fps, 27,7 s. Salida: H.264, 1080 × 1920, 30 fps, 24 s; objetivo de codificación 10 Mbps. El aumento de resolución no recupera detalle que el original no contiene. Para una siguiente edición con mayor nitidez conviene usar los archivos originales del teléfono.

Se conserva la proporción y la imagen real de la prenda. Una banda superior sustituye el título incrustado de la fuente; rostro y calce quedan visibles. El cierre invita a consultar modelos, talles y disponibilidad al WhatsApp público del perfil. No incluye precios, descuentos, crédito, entrega gratuita ni prueba a domicilio.

Verificación: ambos masters se renderizaron sin errores, 720 cuadros cada uno. Se inspeccionaron fotogramas de las combinaciones y del cierre; las versiones con audio se decodificaron completas sin errores. Bitrate de video medido: aproximadamente 8,26 Mbps para looks y 8,29 Mbps para WhatsApp. Audio final: AAC estéreo, 48 kHz, aproximadamente 192 kbps. No se midió aún el rendimiento comercial de las piezas.

## Texto para publicar

**Video de looks:** Un jean y varias formas de combinarlo 💙 ¿Cuál va más con vos? Escribinos **JEANS** por WhatsApp al +595 973 434 868 para consultar opciones, talles y disponibilidad. #IndigoPy #Jeans #CiudadDelEste

**Video de consulta:** ¿Buscás jeans? Contanos qué modelo te gusta, tu talle y tu ciudad. Escribinos **JEANS** por WhatsApp al +595 973 434 868 y te confirmamos las opciones disponibles. #IndigoPy #Jeans #CiudadDelEste

Estos archivos están preparados para revisar y publicar manualmente. No se publicaron ni se activaron anuncios. Confirmar el stock actual del modelo mostrado antes de usar una oferta específica.

## Timeline: looks

| Salida | Segmento fuente | Imagen / texto |
|---|---|---|
| 0–3 s | 0–3 s | Combinación verde: «Un jean. Más de un look.» |
| 3–6 s | 3–6 s | Remera negra, mismo gancho |
| 6–9 s | 6–9 s | Remera lila: «Cambiá la combinación. Elegí tu estilo.» |
| 9–13 s | 9–13 s | Blazer fucsia, mismo texto |
| 13–16 s | 18–21 s | Combinación verde claro: «¿Cuál usarías vos?» |
| 16–20 s | 21–25 s | Abrigo claro, mismo texto |
| 20–24 s | Gráfico | «Escribinos JEANS por WhatsApp», número y consulta de disponibilidad |

## Timeline: WhatsApp

| Salida | Segmento fuente | Imagen / texto |
|---|---|---|
| 0–4 s | 9–13 s | Blazer fucsia: «¿Buscás jeans? Mirá cómo se combinan.» |
| 4–8 s | 0–4 s | Combinación verde/negra: «Contanos qué buscás. Modelo, talle y ciudad.» |
| 8–12 s | 6–10 s | Combinación lila/fucsia, mismo texto |
| 12–16 s | 18–22 s | Verde claro/abrigo: «Consultá las opciones. Te confirmamos disponibilidad.» |
| 16–20 s | 21–25 s | Abrigo claro, mismo texto |
| 20–24 s | Gráfico | Mismo CTA a WhatsApp |

## Reutilización

El [prompt de producción](../PROMPT-PRODUCCION-VIDEOS.md) sirve para nuevas piezas. El script de montaje usa Higgsedit y rutas de su entorno de producción; para ejecutarlo en otra máquina, ajustar `/home/user/indigo/` a la carpeta extraída y registrar las fuentes DM Sans 400/700 con `higgsedit fonts add`.
