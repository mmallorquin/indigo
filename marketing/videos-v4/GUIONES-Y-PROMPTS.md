# Índigo Py — dos reels v4

Dos videos verticales de 20 segundos para mirar y elegir. El montaje utiliza la misma persona y el mismo jean del reel de combinaciones. La dirección de arte cambia entre versiones; no se presenta esta comparación como una prueba que aísle una sola variable.

## Editorial

Playfair Display y DM Sans; oliva y crema como propuesta gráfica. Revelados desde abajo, movimiento suave de palabras, línea fina y salida discreta. Música instrumental propia con percusión suave. El tema es combinar un jean.

| Tiempo del título | Texto | Imagen y propósito |
|---|---|---|
| 0,10–1,80 | Un jean. | Outfit fucsia completo, identificar la prenda |
| 2,00–4,10 | Varios looks. | Lila y giro real, mostrar otra combinación |
| 6,00–7,90 | Cambiá el look. | Fucsia en movimiento, sostener la idea de combinación |
| 14,00–15,65 | ¿Cuál va con vos? | Abrigo beige, invitar a elegir |
| 16,00–20,00 | ÍNDIGO PY / Escribinos / JEANS / por WhatsApp | Producto en movimiento, acción final única |

Entrada: máscara de 0,50 s y movimiento por palabra de 0,42 s con solapamiento. Salida: 0,20 s de desplazamiento y opacidad. Entre títulos quedan intervalos de imagen limpia. El CTA entra en 0,38 s; JEANS se revela con un retraso de 0,10 s durante 0,35 s y queda estable.

**Caption para copiar:**

Un jean, varias ideas para combinarlo. ¿Cuál look va con vos? Escribinos JEANS por WhatsApp y contanos qué modelo y talle buscás, y tu ciudad.

Gancho alternativo para una edición futura: «Tu jean. / Tu estilo.». No está incorporado al MP4 actual.

## Energía

Anton y DM Sans, misma paleta propuesta. Máscara lateral, palabras con entrada horizontal, trazo más ancho y salidas rápidas. La pista propia tiene percusión más marcada. El tema es orientar la consulta por jeans.

| Tiempo del título | Texto | Imagen y propósito |
|---|---|---|
| 0,10–1,80 | ¿BUSCÁS JEANS? | Outfit fucsia completo, identificar intención |
| 2,00–3,80 | TU ESTILO | Lila y giro, abrir elección |
| 6,00–7,80 | TU MODELO | Fucsia, orientar necesidad |
| 9,00–10,80 | TU TALLE | Continúa el giro real, orientar consulta sin prometer talles disponibles |
| 13,00–14,80 | TU CIUDAD | Abrigo beige, dato para evaluar entrega |
| 16,00–20,00 | ÍNDIGO PY / Escribinos / JEANS / por WhatsApp | Imagen real, acción final única |

Entrada: máscara lateral de 0,35 s y movimiento por palabra de 0,30 s con solapamiento. Salida: 0,18 s. El CTA tiene la misma duración y estructura que la otra versión; usa la tipografía de impacto.

**Caption para copiar:**

¿Buscás jeans? Contanos qué modelo querés, tu talle y en qué ciudad estás. Escribinos JEANS por WhatsApp para consultar las opciones.

Gancho alternativo para una edición futura: «Elegí tu look.». No está incorporado al MP4 actual.

## Montaje y sonido

La selección por cuadros y el origen de cada tramo están en `timeline.json` y `preparar-montaje.py`. Ambos MP4 usan el mismo montaje: fucsia, lila, negro, fucsia con giro, verde claro, abrigo beige y negro. La fuente fucsia tiene una reutilización de 0,3 s; no son nuevas tomas.

Pulso: 120 BPM, cada 0,5 s. Cortes a 2, 4,5, 6, 11, 13, 16,5 y 18,5 s. Los cues gráficos y los acentos están en `beats.json`. La música se sintetizó sin muestras externas; no hay voz ni canción tomada de una red social. La mezcla conserva la imagen del render silencioso sin volver a comprimirla.

## Prompt de edición por tramo

Usar únicamente `source.mp4`, CREADORA-REF-01 y JEAN-REF-01. Tomar los cuadros exactos de `timeline.json`; recortar x=100, y=232, 590×1048 y escalar a 1080×1920. Conservar persona, prenda, color y movimiento grabados. No generar ángulos, cuerpo, tela, cintura o etiqueta. No usar efectos para simular una prueba de calce.

Abrir directamente con el outfit completo. Resolver el cambio de combinación con cortes reales sobre el pulso. Superponer los títulos según la tabla de la versión elegida, con entrada, lectura y salida. Mantener rostro, cintura y piernas libres. Dejar respirar la imagen entre intervenciones. El abrigo oculta parte del jean: mostrarlo como combinación, sin atribuirle una demostración de detalles del pantalón. Mantener el CTA desde 16 hasta 20 s sobre la persona en movimiento, sin pantalla final estática.

No agregar precio, urgencia, stock, financiación, visitas gratuitas ni plazos de envío: no están confirmados. Las palabras modelo, talle y ciudad piden información a la persona interesada; no anuncian disponibilidad.

## Uso y medición

Elegir la pieza que mejor represente a la tienda. Antes de subir, comprobar el contacto a WhatsApp del perfil y la vista previa de portada/textos en Instagram o TikTok. El video no publica el número en pantalla. Los MP4 silenciosos permiten usar audio de la biblioteca del destino según los permisos de la cuenta.

Registrar de forma simple consultas nuevas, consultas con modelo/necesidad, talle y ciudad, cotizaciones, pedidos pagados y entregados. Preguntar qué publicación motivó la consulta cuando no pueda identificarse. No atribuir ventas solo por vistas o likes. Estos archivos no activan anuncios ni fijan presupuesto.

