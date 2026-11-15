# Progreso del estratega

## Corrida del 15/11/2026 (primera)

**Qué encontré**
- No existían `docs/estrategia/`, `docs/resultados/registro.csv` ni `PROGRESO-estratega.md`. El plan anterior es `docs/campanas/estrategia.md` (calendario de 14 días, del 14/11).
- Sin resultados: no se publicó ninguna pieza con código.
- La tienda (/probador) muestra 4 prendas, todas de ejemplo. El catálogo de la fábrica solo tiene `DEMO-JEAN`.
- En el issue de avisos (#3), hasta donde deja ver la página pública, no hay pedidos nuevos de Marco. El último comentario es el informe del operador del 14/11, que ya pedía prendas reales.
- Sin token de GitHub: no pude crear issues, comentar ni abrir el PR.

**Qué hice**
- `plan-semana.md` para el 16 al 22/11, con hipótesis declaradas y una prueba A/B de portada ("Así queda puesto" contra "Precio y talles") sobre el jean A.
- `mercado.md` con 7 hallazgos y sus links (usé las 10 búsquedas).
- `issues-ingeniero.md` con 2 issues listos para pegar y un comentario para el #6.
- `docs/resultados/README.md` con el formato de `registro.csv`.

**Qué quedó pendiente**
- Marco: abrir el PR de la rama `operador/estrategia-2026-11-15`, crear los 2 issues con la etiqueta `ingeniero` y responder la lista de la sección 6 del plan.
- El informe no se pudo dejar en el issue #3: está en la respuesta de la corrida, para que Marco lo pegue.

**Para la próxima corrida**
1. Mirar si existe `registro.csv` y si tiene filas. Si tiene, calcular por pieza y por prenda antes de tocar el plan.
2. Resolver la prueba A/B con el criterio de la sección 3 del plan. Si no se corrió (faltaban precio y talles), no cambiarla: sigue siendo la primera prueba.
3. Revisar si la tienda ya tiene prendas reales y reemplazar los lugares A, B, C y D por sus nombres y SKU.
4. Revisar si los issues de `issues-ingeniero.md` ya están creados, para no duplicarlos.
5. No repetir las búsquedas de mercado de esta corrida. Falta mirar: publicaciones reales de boutiques de CDE (las bios no alcanzan) y precios de jeans de la competencia.

**Aprendizajes de esta corrida** (pendientes de pasar a `docs/agentes/APRENDIZAJES.md`: ese archivo todavía no está en `main`, vive en la rama `operador/auto-mejora-2026-11-14`, y crearlo acá haría chocar los dos PR)
- 2026-11-15 · El estratega no puede nombrar prendas si la tienda solo tiene ejemplos: se definen lugares (A, B, C) con criterio de elección y Marco pone el modelo.
- 2026-11-15 · Instagram no se puede abrir con la herramienta de lectura: de la competencia solo sale la bio del buscador. Para ver publicaciones hace falta que Marco mande capturas.
- 2026-11-15 · Para una prueba A/B hacen falta códigos distintos por variante; la fábrica hoy da un solo código por portada (pedido en `issues-ingeniero.md`).
- 2026-11-15 · Sin `GH_TOKEN` no hay issues ni informe en el #3: dejar todo en `docs/estrategia/` y en la respuesta.
- 2026-11-15 · El plan entra en 3 minutos solo con tablas y unas 800 palabras; la primera versión tenía 1.200.
