# Progreso del estratega

## Corrida del 15/11/2026 (tercera, a la par de la segunda)

- Arrancó con el mismo pedido mientras la segunda todavía trabajaba. Mismo diagnóstico: sin `registro.csv`, sin prendas reales, sin comentarios nuevos de Marco.
- No reescribí el plan. Sobre el de la segunda corrida sumé tres líneas: rango de talles en la primera línea de los textos (§14), qué mirar si la portada B trae consultas y no ventas, y la nota en "Cambió hoy".
- `mercado.md`: §14 a §16 (9 búsquedas propias; el resto repetía lo de la segunda) y un link más en §1. Revisé con `curl` los links de §1 a §6 y los números de §10: coinciden.
- Issues: al ir a crearlos ya existían el #15 y el #16. No dupliqué. Mi comentario en el #6 salió repetido y lo borré.
- Aprendizajes para pasar a `docs/agentes/APRENDIZAJES.md` junto con los de abajo (sección `## 2026-11-15 (estratega, 3.ª corrida)`):
  - Puede haber dos corridas del mismo agente a la vez: `git fetch` antes de escribir y antes del push; si la rama se movió, sumar encima solo lo que falta, sin forzar.
  - Listar los issues justo antes de crear o comentar (no al principio): entre una cosa y la otra aparecieron el #15 y el #16.
  - La herramienta de lectura web solo abre links que salieron de una búsqueda de la misma corrida; para revisar links de otra corrida, `curl` desde la terminal.
  - Instagram no abre, pero las páginas "discover" de TikTok y las tiendas web de la competencia sí muestran textos, talles, precios y condiciones.

## Corrida del 15/11/2026 (segunda)

**Qué encontré**
- `docs/resultados/registro.csv` sigue sin existir (ni en `main` ni en ninguna rama): no hay resultados. No se publicó ninguna pieza.
- La tienda (/probador) sigue con las 4 prendas de ejemplo.
- En el issue #3 no hay comentarios nuevos de Marco. El único es el informe del operador del 14/11.
- Esta vez sí había token de GitHub.

**Qué hice**
- `plan-semana.md`: misma semana (16 al 22/11) y misma prueba A/B, porque no se corrió. Cambios por el mercado: motivo del mensaje 3 (confianza), TikTok también el domingo, stories al estado de WhatsApp, fecha de reserva de la prueba (24 y 25/11) y más preguntas para Marco.
- `mercado.md`: 6 hallazgos nuevos (§8 a §13) con 9 búsquedas. Fechas del Black Friday confirmadas otra vez.
- Issues con la etiqueta `ingeniero` (la etiqueta no existía, la creé): **#15** resumen de resultados y **#16** portada B de la prueba. Comentario en el **#6** para medir clics por pieza. Borré `issues-ingeniero.md`: ya no hace falta.
- `docs/resultados/README.md`: la columna `red` acepta `whatsapp`.
- `docs/agentes/APRENDIZAJES.md`: **no lo toqué.** Todavía no está en `main` y el PR #14 del Productor (las stories del lunes) lo crea: si lo creaba acá, ese PR quedaba con conflicto justo antes de publicar. Las 5 líneas están abajo, para pasarlas cuando el archivo esté en `main`.

**Qué quedó pendiente**
- El Productor ya hizo las stories del lunes y del jueves con el plan de la mañana (PR #14). La story S3 dice que se transfiere "con prenda, talle y total confirmados": los dueños no confirmaron el momento del pago para clientas nuevas. Marco lo tiene que confirmar antes de publicarla (pregunta 4 del plan).
- Marco: responder la lista de la sección 6 del plan. Sin prendas reales, la semana se queda en las stories del lunes y del jueves.
- Nadie tomó todavía los issues #15 y #16 (no llevan la etiqueta `agente`, así que no disparan el agente de Actions).

**Para la próxima corrida**
1. Mirar si existe `registro.csv` y si tiene filas. Si tiene, calcular por pieza y por prenda antes de tocar el plan (si el #15 está mergeado, usar su comando).
2. Resolver la prueba A/B con el criterio de la sección 3. Si no se corrió, no cambiarla: mover las fechas y nada más.
3. Si la tienda ya tiene prendas reales, reemplazar los lugares A, B, C y D por sus nombres y SKU.
4. Antes de crear issues, listar los que ya tienen la etiqueta `ingeniero` (#15 y #16).
5. Mercado: no repetir los temas de `mercado.md`. Falta ver publicaciones reales de boutiques de CDE (pedir capturas a Marco) y el precio de un jean en una tienda de CDE.
6. Si corrés dos veces el mismo día y nada cambió (ni datos, ni prendas, ni comentarios), no reescribas el plan: alcanza con decirlo en el informe.
7. Si `docs/agentes/APRENDIZAJES.md` ya está en `main`, pasar ahí las 5 líneas de abajo y borrarlas de acá.

**Aprendizajes pendientes de pasar a `docs/agentes/APRENDIZAJES.md`** (sección `## 2026-11-15 (estratega)`)
- Si la tienda solo tiene prendas de ejemplo, el plan define lugares (A, B, C) con criterio de elección y Marco pone el modelo; no se nombran prendas.
- Una prueba A/B necesita un código por variante (`C1` y `C1B`) y una fecha de reserva por si falta la prenda; si no se corrió, no se rediseña.
- Sin `gh`, la API de GitHub anda con `curl` o Python y `GH_TOKEN` (sin imprimirlo). Nunca escribir la mención al agente en un comentario: `agente.yml` la toma como un pedido y gasta una corrida.
- Antes de crear un archivo compartido que no está en `main`, mirar los PR abiertos: si otro ya lo crea, no duplicarlo (choca) y dejar la nota en el PROGRESO propio.
- Antes de cambiar una pieza del plan, mirar si el Productor ya la hizo (PR abiertos y `docs/campanas/`): si está hecha, se marca qué revisar en vez de pedirla de nuevo.

## Corrida del 15/11/2026 (primera)

- No existían `docs/estrategia/`, `docs/resultados/` ni este archivo. El plan anterior era `docs/campanas/estrategia.md` (calendario de 14 días, del 14/11).
- Hice el primer `plan-semana.md` (hipótesis y prueba A/B de portada sobre el jean A), `mercado.md` con 7 hallazgos (10 búsquedas) y el formato de `registro.csv`.
- Sin token de GitHub: los issues y el informe quedaron para la segunda corrida.
