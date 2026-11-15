# Plan de la semana — 16 al 22 de noviembre de 2026

**Datos:** `docs/resultados/registro.csv` no existe todavía: no hay resultados para calcular. Todo es **hipótesis**; la meta de la semana es conseguir los primeros números.

**Bloqueo:** la tienda solo tiene 4 prendas de ejemplo. Sin prendas reales, solo salen las piezas "sin prenda".

## 1. Prendas a empujar

Defino el lugar; Marco elige el modelo real.

| Lugar | Prenda | Motivo |
|---|---|---|
| **A** (ancla) | Un jean en stock, el que tenga más talles. Si hay, pierna ancha o recto de tiro alto | Los dueños dicen que es lo más vendido (muestra chica). Tendencia: mercado §5 |
| **B** | Una blusa que combine con el jean A | Las ventas fueron de 2–3 prendas juntas. Hipótesis: el look suma prendas por pedido |
| **C** | Un pantalón de tono neutro | Hipótesis: trae a la que busca ropa de oficina y no jean |
| **D** (opcional) | Un chaleco, si hay stock | Completa el look del sábado |

## 2. Tres mensajes clave

1. **"Así queda puesto."** Frente, espalda y detalle. Motivo: es lo que más se pregunta al comprar ropa por chat (mercado §4).
2. **"Tu talle, sin vueltas."** Decinos qué talle usás y te pasamos las medidas. Motivo: el talle es la duda n.º 1 (mercado §4).
3. **"Preguntá todo antes de transferir."** Te atiende una persona de CDE, sin apuro. Motivo: en semana de Black Friday todos apuran; a la clienta nueva le falta confianza (hipótesis).

Una sola llamada a la acción: **Pedí por WhatsApp**, con el código de la pieza.

## 3. Prueba A/B (una sola)

- **Hipótesis:** precio y talles en la portada traen más consultas que solo mostrar cómo queda.
- **Variantes:** mismo jean A, mismas fotos, Instagram, 20:30. Solo cambian la portada y la primera línea. Cada carrusel va también a stories con su enlace.
  - **A · "Así queda puesto"** — martes 17 — `IND-<sku>-C1`
  - **B · "Precio y talles"** — miércoles 18 — `IND-<sku>-C1B`
- **Condición:** precio y talles reales del jean A. Si faltan, B no se publica y la prueba pasa a la otra semana.
- **Métrica:** consultas con ese código por cada 1.000 cuentas alcanzadas, hasta 72 horas después de publicar.
- **Criterio** (domingo 22):
  - **Gana** la que tenga 5 consultas o más y al menos el doble que la otra → su gancho va en las portadas de la semana que viene.
  - **Inconcluso** si entre las dos no llegan a 5 → falta alcance, no gancho: se repite con la blusa B y un Reel.
  - **Empate** en otro caso → queda "Así queda puesto" y se prueba Reel contra carrusel.
- **Límite:** dos días distintos y poca gente: es una pista, no una prueba.

## 4. Calendario

| Día | Red | Hora | Pieza | Prenda | Gancho |
|---|---|---|---|---|---|
| Lun 16 | Instagram | 20:30 | 3 stories | Sin prenda | "Preguntá todo antes de transferir" |
| Mar 17 | Instagram | 20:30 | Carrusel + story (A) | Jean A | "Así queda puesto" |
| Mié 18 | Instagram | 20:30 | Carrusel + story (B) | Jean A | "Precio y talles" |
| Jue 19 | Instagram | 20:30 | Story con caja de preguntas | Sin prenda | "Tu talle, sin vueltas" |
| Vie 20 | Instagram + TikTok | 20:30 | Carrusel | Blusa B con jean A | "Así queda con el jean" |
| Sáb 21 | TikTok + Instagram | 11:00 | Reel de 15–25 s | Jean A + blusa B (+ D) | "Un jean, tres looks" |
| Dom 22 | Instagram | 20:30 | Carrusel + story | Pantalón C | El que venga ganando |

- **20:30:** Marco responde desde las 20:00 y contestar rápido pesa más que la hora pico (hipótesis; mercado §3 y §6).
- **Martes y miércoles:** mejores días de Instagram y antes del Black Friday de CDE (19 al 22). Sin descuento aprobado, no se nombran ofertas.
- **Sábado:** sin clips no hay Reel; se adelanta el pantalón C.

## 5. Piezas para el Productor (por prioridad)

| # | Pieza | Día | Código | Nota |
|---|---|---|---|---|
| 1 | 3 stories "Cómo pedir" | Lun | `IND-MARCA-S1` a `S3` | Escribinos, te ayudamos con el talle, pagás por transferencia |
| 2 | Jean A: carrusel, portada A | Mar | `IND-<sku>-C1` | Foto puesta, sin precio en la portada |
| 3 | Jean A: portada B | Mié | `IND-<sku>-C1B` | Misma foto + precio y talles del catálogo |
| 4 | Story de talle | Jue | `IND-MARCA-S4` | "¿Qué talle de jean usás?" |
| 5 | Blusa B: carrusel | Vie | `IND-<sku>-C1` | Una lámina con el jean A |
| 6 | Pantalón C: carrusel | Dom | `IND-<sku>-C1` | Portada con el gancho ganador |
| 7 | Reel "Un jean, tres looks" | Sáb | `IND-<sku>-R1` | Opcional: solo con clips de Marco |

En todas: código en el texto y en el enlace de WhatsApp. Si falta un dato, "Consultá precio y talle por WhatsApp". Sin escasez inventada, sin prendas de ejemplo.

## 6. Lo que solo Marco puede dar

1. Prendas reales A, B y C: fotos de frente, espalda y detalle, y su fila en `catalogo.csv`.
2. Precio y talles del jean A (sin eso no hay prueba).
3. ¿Hay oferta real para el Black Friday? Si no, no se nombra.
4. Desde qué hora respondés WhatsApp entre semana (asumí las 20:00).
5. Seguidores de hoy en Instagram y TikTok.
6. El domingo 22: cargar `registro.csv` (ver `docs/resultados/README.md`).

Mercado: `mercado.md`. Tareas de código: `issues-ingeniero.md`.
