# Plan de la semana — 16 al 22 de noviembre de 2026

Actualizado el domingo 15/11. Los § remiten a `mercado.md`.

## 0. Resultados: todavía no hay

- `docs/resultados/registro.csv` **no existe**: 0 piezas publicadas, 0 consultas, 0 ventas. Nada para calcular; todo es **hipótesis**.
- La tienda sigue con 4 prendas de ejemplo: sin prendas reales solo salen las piezas del lunes y del jueves.
- **Cambió hoy:** motivo del mensaje 3 (§9), más TikTok (§10), estado de WhatsApp (§12) y fecha de reserva para la prueba.

## 1. Prendas a empujar

Defino el lugar; Marco elige el modelo real.

| Lugar | Prenda | Motivo |
|---|---|---|
| **A** (ancla) | El jean en stock con más talles; si hay, pierna ancha o recto de tiro alto | Lo más vendido según los dueños (muestra chica). Tendencia: §5 |
| **B** | Blusa o camisa liviana que combine con el jean A | Se vendieron 2–3 prendas juntas. Hipótesis: el look suma prendas por pedido (§13) |
| **C** | Pantalón amplio de tono neutro | Hipótesis: trae a la que busca ropa de oficina |
| **D** (opcional) | Chaleco, si hay stock | Completa el look del sábado |

## 2. Tres mensajes clave

1. **"Así queda puesto."** Frente, espalda, detalle y qué talle usa quien la tiene puesta. Motivo: es lo que más se pregunta por chat (§4, §12).
2. **"Tu talle, sin vueltas."** Decinos qué talle usás y te pasamos las medidas. Motivo: el talle es la duda n.º 1 (§4).
3. **"Preguntá todo antes de transferir."** Te atiende una persona de CDE, sin apuro. Motivo: la Policía pide desconfiar de perfiles nuevos que cobran por adelantado, e Índigo es una cuenta nueva que cobra por transferencia (§9).

Una sola llamada a la acción: **Pedí por WhatsApp**, con el código de la pieza.

## 3. Prueba A/B (la misma: todavía no se corrió)

- **Hipótesis:** precio y talles en la portada traen más consultas que solo mostrar cómo queda (la competencia los muestra: §8).
- **Variantes:** mismo jean A, mismas fotos, Instagram, 20:30. Solo cambia la portada.
  - **A · "Así queda puesto"** — martes 17 — `IND-<sku>-C1`
  - **B · "Precio y talles"** — miércoles 18 — `IND-<sku>-C1B` (issue #16)
- **Condición:** jean A real, con precio y talles, cargado antes del martes. Si no, la prueba pasa entera al 24 y 25.
- **Métrica:** consultas con ese código por cada 1.000 cuentas alcanzadas, a las 72 horas de publicar.
- **Criterio** (domingo 22):
  - **Gana** la que tenga 5 consultas o más y al menos el doble que la otra → su gancho va en las portadas siguientes.
  - **Inconcluso** si entre las dos no llegan a 5 → falta alcance: se repite con la blusa B y un Reel.
  - **Empate** en otro caso → queda "Así queda puesto" y se prueba Reel contra carrusel.
- **Límite:** dos días distintos y poca gente: es una pista, no una prueba.

## 4. Calendario

| Día | Red | Hora | Pieza | Prenda | Gancho |
|---|---|---|---|---|---|
| Lun 16 | Instagram + estado de WhatsApp | 20:30 | 3 stories | Sin prenda | "Preguntá todo antes de transferir" |
| Mar 17 | Instagram | 20:30 | Carrusel + story (A) | Jean A | "Así queda puesto" |
| Mié 18 | Instagram | 20:30 | Carrusel + story (B) | Jean A | "Precio y talles" |
| Jue 19 | Instagram + estado de WhatsApp | 20:30 | Story con caja de preguntas | Sin prenda | "Tu talle, sin vueltas" |
| Vie 20 | Instagram + TikTok | 20:30 | Carrusel | Blusa B con jean A | "Así queda con el jean" |
| Sáb 21 | TikTok + Instagram | 11:00 | Reel de 15–25 s | Jean A + blusa B (+ D) | "Un jean, tres looks" |
| Dom 22 | Instagram + TikTok | 20:30 | Carrusel + story | Pantalón C | El gancho que venga ganando |

- **20:30:** Marco responde desde las 20:00, y contestar rápido pesa más que la hora pico (hipótesis; §6).
- **Martes y miércoles:** antes del Black Friday de CDE (19 al 22). Sin descuento aprobado, no se nombran ofertas.
- **TikTok y estado:** TikTok tiene más público adulto en Paraguay que Instagram (§10); el estado llega a los conocidos, que ya compraron (§12). La prueba no va a ninguno.
- **Sábado:** sin clips no hay Reel; se adelanta el pantalón C.

## 5. Piezas para el Productor (por prioridad; los días están en el calendario)

| # | Pieza | Código | Nota |
|---|---|---|---|
| 1 | 3 stories "Cómo pedir" | `IND-MARCA-S1` a `S3` | Hechas (PR #14). S3 dice que se transfiere con todo confirmado: Marco lo confirma antes de publicar (pregunta 4) |
| 2 | Jean A: carrusel, portada A | `IND-<sku>-C1` | Foto puesta, sin precio en la portada |
| 3 | Jean A: portada B | `IND-<sku>-C1B` | Misma foto + precio y talles del catálogo |
| 4 | Story de talle | `IND-MARCA-S4` | Hecha (PR #14) |
| 5 | Blusa B: carrusel | `IND-<sku>-C1` | Una lámina con el jean A |
| 6 | Pantalón C: carrusel | `IND-<sku>-C1` | Sin ganador: "Así queda puesto" |
| 7 | Reel "Un jean, tres looks" | `IND-<sku>-R1` | Solo con clips de Marco, sin marca de agua de otra app (§11) |

En todas: código en el texto y en el enlace. Dato que falta: "Consultá por WhatsApp". Sin escasez inventada, sin prendas de ejemplo y sin la modelo del probador hasta que Marco la autorice por escrito.

## 6. Lo que solo Marco puede dar

1. Prendas reales A, B y C: fotos de frente, espalda y detalle, y su fila en `catalogo.csv`.
2. Precio y talles del jean A (sin eso no hay prueba).
3. Fotos "puesta": ¿propias, o autorizás la modelo del probador? ¿Qué talle usa?
4. Clienta nueva: ¿transfiere recién con prenda, talle y total confirmados (así lo dice la story S3)?, ¿en CDE puede ver la prenda antes de pagar?, ¿hay cambio de talle?
5. ¿Hay oferta real para el Black Friday? Si no, no se nombra.
6. Desde qué hora respondés WhatsApp (asumí las 20:00) y seguidores de hoy.
7. El domingo 22: cargar `registro.csv` (ver `docs/resultados/README.md`).

Código pedido (etiqueta `ingeniero`): #15, resumen de resultados; #16, portada B. Medir clics por pieza: comentado en el #6.
