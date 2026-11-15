# Progreso del Productor de contenido

## 2026-11-15 (domingo)
- Entradas: no hay `docs/estrategia/plan-semana.md` en main. Usé `docs/campanas/estrategia.md` (borrador) y el respaldo de las "3 prendas con mejores fotos".
- **Bloqueo, el mismo que en el ciclo 1 de PROGRESO.md:** las 4 prendas de /probador tienen `ejemplo: true` y no son de la tienda. La modelo es una persona real sin autorización confirmada. catalogo.csv solo tiene DEMO-JEAN.
- Producido: ninguna pieza de prenda. No llamé a /probador/probar (gasto en la API: 0).
- Paquete del día: `docs/campanas/hoy/2026-11-15.md`. Hoy no hay nada programado y el día 1 (16/11) queda bloqueado.
- `whatsapp.md` ya existía: no lo toqué.
- Sigue: cuando haya al menos 1 prenda real con foto propia, producir la prenda A (jean) en este orden: S1 (día 1), R1 (día 2), C1–C5 (día 3), y guardar el método en `.claude/skills/carrusel` y `.claude/skills/reel`.

## 2026-11-15 (domingo, 2.ª corrida)
- El plan de la semana existe en la rama `operador/estrategia-2026-11-15` (sin mergear). Lo usé como guía porque sus piezas 1 y 4 no necesitan prenda.
- Las 3 prendas "de mejores fotos" siguen siendo de ejemplo (`ejemplo: true`): no hice piezas de prenda. Gasto en /probador/probar: 0 (0 de 10 esta semana).
- Producido: `docs/campanas/2026-W47/marca/` story_01..03 ("Cómo pedir", lun 16) y story_04 (talle, jue 19), con textos.json y whatsapp.json (IND-MARCA-S1..S4).
- Paquetes: `hoy/2026-11-15.md` (no se sube nada) y `hoy/2026-11-16.md` (las 3 stories, 20:30).
- Skill nueva: `.claude/skills/story-marca`.
- Sigue: piezas 2, 3, 5, 6 y 7 del plan (jean A, blusa B, pantalón C, Reel) cuando Marco cargue prendas reales.

## 2026-11-15 (domingo, 3.ª corrida)
- El plan ya está en main (#18, #19). Mergeé main en esta rama (sin conflictos): el PR #14 ahora solo toca `docs/campanas/`, `.claude/skills/` y `APRENDIZAJES.md`.
- Las 4 prendas de /probador siguen con `ejemplo: true` y `catalogo.csv` solo tiene DEMO-JEAN: piezas 2, 3, 5, 6 y 7 bloqueadas. Gasto en /probador/probar: 0 (0 de 10 esta semana).
- Ajustes por el plan nuevo: story_01 dice "una persona de Ciudad del Este" (§9); S1–S4 van también al estado de WhatsApp (§12), con su texto en `textos.json` y en los paquetes. Mismo código por story; en el registro, otra fila con red `whatsapp`.
- Guardé `marca/piezas.json`: regenera las 4 stories idénticas con la skill.
- Paquetes: `hoy/2026-11-15.md` (no se sube nada) y `hoy/2026-11-16.md` (Instagram + estado, 20:30). S3 espera la confirmación de Marco (pregunta 4).
- Sigue: cuando haya jean A real, carrusel C1 (portada "Así queda puesto") y C1B (precio y talles del CSV, primera línea con el rango de talles).

## 2026-11-15 (domingo, 4.ª corrida, 12:00)
- Revisé de nuevo: /probador y /tienda siguen con las 4 prendas de ejemplo (`ejemplo: true`), `catalogo.csv` solo tiene DEMO-JEAN, no hay archivos subidos y Marco no respondió en el #3. Piezas 2, 3, 5, 6 y 7 siguen bloqueadas.
- No produje piezas nuevas ni toqué las existentes. Gasto en /probador/probar: 0 (0 de 10 esta semana).
- Paquetes: `hoy/2026-11-15.md` (no se sube nada) y `hoy/2026-11-16.md` siguen vigentes, sin cambios.
- Para la carrusel no hace falta skill nueva: la fábrica (`fabrica/LEEME.md`) ya hace carrusel_01..05, stories, textos.json y whatsapp.json desde `catalogo.csv`. Con jean A real: correr la fábrica para ese SKU y revisar contra el plan (primera línea con rango de talles, portada C1 sin precio; C1B depende del #16).
- Sigue: lo mismo. Si el jean A no está cargado el lunes 16 a la noche, la prueba A/B pasa al 24 y 25 (plan §3).
