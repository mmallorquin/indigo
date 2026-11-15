# Estrategia de lanzamiento — Índigo Py

> Estado: borrador para que Marco apruebe. Fuentes: `marca.toml`, `marketing/CONTEXTO-NEGOCIO.md`, `MEGAPROMPT-MARKETING-INDIGO-PY.md`, `MOTION-BLUEPRINT-APLICADO-INDIGO-PY.md`.
> Regla de oro: no hay precio, talle, stock, plazo ni condiciones de cambio confirmados. Donde falte, se dice "Consultá precio y talle por WhatsApp" o "te confirmo enseguida".

## 1. Público, propuesta de valor y mensajes clave

### Público
Mujeres de Ciudad del Este y del resto de Paraguay que buscan jeans, blusas y pantalones fáciles de combinar para la oficina y las salidas, y que quieren resolver sus dudas de talle y calce **antes** de comprar por WhatsApp. No hay datos de edad ni de ingresos: no se asumen.

Segmento para la primera prueba: **mujeres de CDE que buscan jeans y básicas para el día a día**. Por qué: los dueños dicen que los jeans son lo más vendido, y es donde más pesa la duda de talle (hipótesis, sin validar con clientas nuevas).

### Propuesta de valor
> En Índigo ves la prenda puesta, resolvés tu talle por WhatsApp con una persona y pedís sin salir de casa.

Se apoya en tres cosas reales: pedidos y asesoría por WhatsApp, cobro por transferencia, envíos a todo Paraguay por transportadora (todavía sin un envío lejano hecho: no prometer plazos) y el probador virtual de la tienda.

### Tres mensajes clave
1. **"Así queda puesto."** Mostramos la prenda puesta y cómo combinarla, no solo colgada. (Si la imagen es del probador: leyenda "Imagen generada con IA".)
2. **"Tu talle, sin vueltas."** Preguntanos por WhatsApp y te ayudamos con el talle. Nunca se afirma un talle ni una medida que no figure en la tienda.
3. **"Pedí por WhatsApp."** Una sola llamada a la acción por pieza, con un código para saber de qué pieza vino la consulta.

Prohibido (de `marca.toml`): "elevá tu estilo", "descubrí tu mejor versión", "el must-have perfecto", urgencia o escasez inventada, testimonios inventados.

## 2. Embudo

| Etapa | Qué pasa | Métrica | Cómo se mide |
|---|---|---|---|
| 1. Atraer | Reel, carrusel o story en Instagram/TikTok | Vistas, guardados, compartidos, visitas al perfil | Estadísticas nativas de cada red, por pieza (anotar el código `IND-<sku>-<pieza>`) |
| 2. Consulta por WhatsApp | La persona toca el enlace y escribe | **Consultas por pieza** | El enlace `wa.me` trae el texto "Hola, vengo por IND-<sku>-<pieza>". Se cuenta cada chat que arranca con ese código |
| 3. Consulta calificada | Quiere comprar y encaja (producto, talle, zona) | Consultas calificadas / consultas | Etiqueta en WhatsApp Business: *Calificada* |
| 4. Cierre | Cotización completa → transferencia → pedido pagado | Pedidos pagados / consultas calificadas | Etiquetas *Cotizada* y *Pagada*, más planilla de pedidos |
| 5. Entrega y posventa | Despacho o entrega, mensaje a las 24 h | Entregados, cambios, motivo de pérdida | Etiqueta *Entregada*; planilla |
| 6. Recompra y recomendación | Se le pide que recomiende y vuelva | Clientas que recompran o recomiendan | Etiqueta *Recompra* y pregunta "¿cómo nos conociste?" |

Reglas de medición (del megaprompt): una venta cuenta solo si está **pagada**; separar conocidos de personas nuevas; con pocas ventas no se declara ganador; si el denominador es cero, "no calculable".

### Código de pieza
`IND-<sku>-<pieza>`, por ejemplo `IND-JEAN01-R1`. Piezas: `FLY` flyer, `C1..C5` carrusel, `S1..S3` stories, `R1` reel. El código va en el enlace de WhatsApp y en el texto de cada publicación, para que cuando alguien escriba se sepa de dónde vino. Si la clienta no manda el código, se le pregunta de dónde nos conoció.

### Planilla mínima de pedidos
Fecha, código de pieza, persona nueva o conocida, prenda y talle, estado (consulta / cotizada / pagada / entregada / cancelada), total, motivo de pérdida.

## 3. Calendario de 14 días

Supuestos a confirmar con Marco: se produce y se programa el fin de semana; entre semana solo hay ventana de respuesta después de las 20:00. Por eso se publica **a las 12:30 y a las 20:30**: la segunda cae justo cuando pueden contestar. Día 1 = lunes 16/11/2026. Las piezas se reemplazan por las de una prenda **real** (ver `docs/campanas/PROGRESO.md`).

Prueba de ganchos sobre la **misma prenda** (prenda A, idealmente un jean, el producto más vendido):
- Gancho A: **"Así queda puesto"** (días 3 y 4).
- Gancho B: **"Precio y talles"** (días 5 y 6), solo con precio y talles que figuren en la tienda; si no, "Consultá precio y talle por WhatsApp".
- Se comparan **consultas por pieza** y guardados. Con tan pocos datos el resultado es una pista, no una prueba.

| Día | Red | Hora | Pieza | Gancho |
|---|---|---|---|---|
| 1 lun | Instagram | 20:30 | Story: "Ya estamos en Índigo, pedí por WhatsApp" (S1 de la prenda A) | "Abrimos pedidos por WhatsApp" |
| 2 mar | TikTok + IG | 20:30 | Reel de la prenda A (R1) | "Una prenda, tres looks" |
| 3 mié | Instagram | 12:30 | Carrusel A (C1–C5) gancho **Así queda puesto** | "Así queda puesto" |
| 4 jue | Instagram | 20:30 | Story con encuesta: "¿Con qué la combinarías?" | "Así queda puesto" |
| 5 vie | Instagram | 12:30 | Carrusel A gancho **Precio y talles** (variante de portada y de C4) | "Precio y talles" |
| 6 sáb | TikTok | 12:30 | Reel de la prenda A con texto "Precio y talles" | "Precio y talles" |
| 7 dom | Instagram | 20:30 | Story: respuesta a dudas de talle + enlace a WhatsApp | "Tu talle, sin vueltas" |
| 8 lun | Instagram | 12:30 | Flyer de la prenda B | "Nueva en Índigo" (solo si hay stock confirmado) |
| 9 mar | TikTok + IG | 20:30 | Reel de la prenda B | "Cómo combinarla" |
| 10 mié | Instagram | 12:30 | Carrusel B | "Así queda puesto" |
| 11 jue | Instagram | 20:30 | Story: cómo pedir en 3 pasos (WhatsApp, talle, transferencia) | "Pedir es fácil" |
| 12 vie | Instagram | 12:30 | Flyer de la prenda C | "Nueva en Índigo" |
| 13 sáb | TikTok | 12:30 | Reel de la prenda C | "Cómo combinarla" |
| 14 dom | Instagram | 20:30 | Story de balance + pedido de recomendación (sin testimonios inventados) | "Contanos qué te gustaría ver" |

Cada día, después de publicar: anotar el código de pieza, vistas, guardados y consultas recibidas. El domingo del día 7 y del 14: mirar la tabla y decidir qué gancho repetir.

## 4. Lo que falta de los dueños (bloquea publicar)
1. Qué prendas reales hay, con foto real, precio, talles y stock.
2. Condiciones para clientas nuevas: momento de la transferencia, cambios, reserva.
3. Transportadora, tarifa y quién paga el envío.
4. Horario de respuesta que pueden cumplir.
