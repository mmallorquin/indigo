# Tareas de código pedidas por el estratega — 15/11/2026

En esta corrida no había token de GitHub, así que **no pude crear los issues**. Quedan acá listos para copiar y pegar. Etiqueta: `ingeniero`. Revisé los issues abiertos (#5 a #10) y ninguno cubre esto.

---

## Issue 1 — Resultados: registro.csv con encabezado y resumen por pieza y por prenda

**Etiqueta:** `ingeniero`

**Objetivo:** que Marco cargue los resultados en un solo archivo y que cualquier agente pueda sacar el resumen con un comando, sin calcular a mano.

**Qué hacer**
- Crear `docs/resultados/registro.csv` solo con el encabezado: `fecha,codigo,red,alcance,consultas,ventas,monto_gs` (formato en `docs/resultados/README.md`).
- Un comando (por ejemplo `python -m fabrica.resultados docs/resultados/registro.csv`) que imprima dos tablas en Markdown, por pieza y por prenda (el SKU sale del código `IND-<sku>-<pieza>`): alcance, consultas, ventas, monto, consultas por cada 1.000 de alcance y ventas por consulta.
- Si el denominador es cero, escribir "no calculable". No redondear para arriba ni completar filas que falten.
- Las filas con código mal escrito o números inválidos se listan aparte como "filas para revisar"; no frenan el resumen.

**Listo cuando**
- Con el archivo vacío (solo encabezado) el comando responde "Todavía no hay resultados cargados" y termina bien.
- Tests con un CSV de ejemplo: suma varias filas de la misma pieza, agrupa por prenda, muestra "no calculable" con cero consultas y separa las filas inválidas.
- `pytest -q` pasa completo.

---

## Issue 2 — Fábrica: variante B de portada para la prueba A/B (código C1B)

**Etiqueta:** `ingeniero`

**Objetivo:** que la fábrica entregue las dos portadas de la prueba de ganchos con códigos distintos, para saber de cuál vino cada consulta.

**Contexto:** hoy `carrusel_01` usa el gancho "Así queda puesto" (código `C1`). El gancho "Precio y talles disponibles" ya se escribe en `textos.json`, pero no hay lámina ni código para él.

**Qué hacer**
- Generar `carrusel_01b.png`: la misma foto y el mismo diseño de la portada, con el gancho de precio y, debajo, el precio y los talles tal como están en `catalogo.csv`.
- Sumar `C1B` a `whatsapp.json`, con el código `IND-<sku>-C1B` y su enlace.
- Si a la prenda le falta precio o talles, **no** generar la variante B y decirlo en `resumen.md` ("sin variante B: falta precio" o "falta talles"). Nunca completar con un dato inventado ni con "Consultá precio".
- En `textos.json`, guardar la primera línea del texto para cada variante.

**Listo cuando**
- Test: una prenda con precio y talles produce `carrusel_01b.png` y `whatsapp.json` trae `C1` y `C1B` con enlaces distintos.
- Test: una prenda sin precio no produce la variante B y el resumen lo dice.
- Las piezas DEMO siguen saliendo con marca de agua.
- `pytest -q` pasa completo.

---

## Comentario sugerido para el issue #6 (Botón Pedir por WhatsApp)

No hace falta un issue nuevo. Pedido: que `GET /ir/whatsapp/<id_prenda>` acepte un parámetro opcional `pieza` (por ejemplo `?pieza=IND-JEAN01-C1B`), lo anote junto con el clic y lo ponga en el mensaje prellenado. Así los clics de cada pieza se cuentan solos, aunque la clienta borre el texto. **Listo cuando:** hay un test con `pieza` válida (302 con el código en el mensaje) y otro con `pieza` mal formada (se ignora y redirige igual).
