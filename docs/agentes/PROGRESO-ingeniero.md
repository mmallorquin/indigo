# Progreso del Ingeniero

## Corrida del 15/11/2026 (mañana)

**Qué encontré**
- Conexión bien: `gh` con token, permiso de push, deploy en verde y `/salud` con el sha de `main`.
- PR #12 (tienda pública, issue #5): tests en verde, pero en conflicto con `main` por `docs/campanas/PROGRESO.md`. Durante la corrida el Revisor dejó ⚠️ con tres pedidos: el conflicto, la categoría pegada al precio y el botón pegado a la grilla.
- Durante la corrida aparecieron los issues #15 y #16 con la etiqueta `ingeniero`. Los dos se programan en `fabrica/`.

**Qué hice**
- PR #12: traje `main` a la rama (merge, sin forzar el push) y dejé `PROGRESO.md` igual que en `main`. Corregí los dos detalles de CSS que pidió el Revisor. Checks en verde, 50 tests.
- Mergeé el #12 (primer merge del día en hora de Paraguay). Deploy en verde y `/salud` con el sha `bfb3ef4` al primer intento. En producción: `/tienda` responde 200 sin contraseña, 4 prendas, sin desborde a 375 px; `/`, `/marca` y `/probador/prendas` siguen pidiendo clave. El issue #5 quedó cerrado.
- Issue #6: PR abierto en la rama `operador/ing-6-pedir-whatsapp`. Ruta `GET /ir/whatsapp/<id>` (anota el clic sin datos de la persona y redirige), botón en `/tienda` y en el probador, y el parámetro `pieza` que pidió el estratega. 57 tests pasan (7 nuevos). Revisado a 375 px, en claro y en oscuro.
- Cerré el PR #17 (solo traía este archivo): ahora viaja en el PR del #6, para no pasar de un PR nuevo por corrida.

**Qué quedó pendiente**
- Revisor: revisar el PR del #6. Hoy `main` ya tuvo tres merges (#12, #18 y #19), así que no se mergea hasta mañana.
- Marco: decidir si `fabrica/` es zona del Ingeniero. Mi lista es `app/`, `tests/`, los `.py` de la raíz y `.claude/skills/`. Los issues #15, #16 y #9 se programan en `fabrica/`, así que no los tomé. El #16 (variante B) hace falta para la prueba del miércoles 18.
- `CLAUDE.md` dice que sin contraseña quedan solo `/salud`, `/static` y el probador. Ya no es cierto: también `/tienda` y, con el #6, `/ir/whatsapp`. No lo toqué porque no está en mi zona.

**Para la próxima corrida**
1. Si el PR del #6 tiene ✅ o ⚠️ sin bloqueantes y checks en verde: mergear, esperar el deploy y verificar el sha en `/salud`. Después probar en producción `/ir/whatsapp/<id de una prenda>` (tiene que dar 302 a wa.me) y un id inventado (404).
2. Después, el #7 (Probátela): ya está destrabado y es de `app/`.
3. Si Marco confirma que `fabrica/` es mía: primero el #16, después el #15.
4. El #8 puede pedir una dependencia en `requirements.txt` (zona protegida): si la pide, ese PR queda abierto para Marco.

**Aprendizajes de esta corrida** (pendientes de pasar a `docs/agentes/APRENDIZAJES.md`: ese archivo no está en `main` y ya lo crean el PR #14 y la rama `operador/auto-mejora-2026-11-14`; crearlo acá sumaría un tercer choque)
- 2026-11-15 · `gh`: si apt no lo encuentra, primero `apt-get update -q`. `gh pr edit` falla en la versión 2.45 (error de Projects classic): usar `gh api -X PATCH repos/<repo>/pulls/<n> -F body=@archivo.md`.
- 2026-11-15 · Un PR que choca en un archivo compartido se arregla con `git merge origin/main` en la rama y `git checkout --theirs <archivo>`: queda como en `main`, sin forzar el push.
- 2026-11-15 · Capturas a 375 px: Playwright ya tiene Chromium (`/opt/pw-browsers`). Levantar la app con `APP_PASSWORD=prueba`, cargar prendas con `POST /probador/prendas` y medir `scrollWidth - clientWidth` (tiene que dar 0). Contra producción hace falta `ignore_https_errors=True`. Los tests de texto no ven dos `<span>` pegados: mirar la captura.
- 2026-11-15 · Otros agentes escriben mientras corrés (revisión, issues y merges nuevos): volvé a leer PR e issues antes de mergear y antes de elegir tarea. Los merges del día se cuentan en hora de Paraguay y entre todos.
- 2026-11-15 · Las prendas de ejemplo no se nombran en ningún mensaje de WhatsApp ni llevan botón de pedido: esa regla ya estaba en `probador.js` y vale para toda ruta nueva.
