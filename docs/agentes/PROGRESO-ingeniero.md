# Progreso del Ingeniero

## Corrida del 15/11/2026 (mañana, 2.ª)

**Qué encontré**
- Conexión bien: `gh` con token (hubo que instalarlo de apt), permiso de push, deploy en verde y `/salud` con el sha de `main` (`461ebae`).
- Nada roto. PR #20 (issue #6): checks en verde, todavía sin revisión. `main` ya tuvo tres merges hoy (#12, #18 y #19).
- Marco todavía no contestó si `fabrica/` es zona del Ingeniero: el #15 y el #16 siguen sin tomar.

**Qué hice**
- Issue #7 (Probátela): PR #21 en la rama `operador/ing-7-probatela`, salida de `main`. Botón "Probátela" en cada prenda de `/tienda` que abre `/probador?prenda=<id>`; el probador arranca con esa prenda al centro. 55 tests pasan (5 nuevos). Probado en Chromium a 375 px, en claro y en oscuro, con id existente, inexistente y raro.
- Decisión que quedó para Marco en el PR #21: el issue pide "dejarla fijada" y también "fijar no genera imagen". Hoy fijar es lo que pide la foto, así que la prenda queda al centro y la foto se genera recién con el toque en "Fijar esta prenda" (dos toques). Fijarla sola al llegar es una línea, pero el enlace gastaría con solo abrirlo.
- No mergeé nada: hoy ya hubo tres merges y falta el Revisor en los dos PR.

**Qué quedó pendiente**
- Revisor: PR #20 y PR #21.
- Marco: (1) ¿`fabrica/` es zona del Ingeniero? El #16 hace falta para la prueba del miércoles 18. (2) En el #21, ¿un toque o dos?
- Los PR #20 y #21 chocan en `tienda.html` e `indigo.css` (los dos arman la tarjeta con un botón debajo).

**Para la próxima corrida**
1. Mergear el #20 si tiene ✅ o ⚠️ sin bloqueantes y checks en verde. Verificar el sha en `/salud` y probar en producción `/ir/whatsapp/<id>` (302 a wa.me) y un id inventado (404).
2. Traer `main` a `operador/ing-7-probatela` (`git merge origin/main`, sin forzar el push) y resolver el choque: la tarjeta queda con "Probátela" (`boton secundario`) y debajo "Pedir por WhatsApp" (`boton`). En el CSS, `margin-top: auto` va solo en el primer botón (`.grilla a:first-child + .boton`) y `.grilla .secundario` conserva su color. Mirar la captura a 375 px antes de mergear.
3. Si Marco pide un solo toque en el #21: después de acomodar la rueda, `$("fijar").click()` al final de `probador.js`, y decirlo en el PR.
4. Si Marco confirma que `fabrica/` es mía: primero el #16, después el #15.
5. El #8 (medición) se destraba cuando entre el #20. Puede pedir una dependencia en `requirements.txt` (zona protegida): ese PR queda abierto para Marco.

**Aprendizajes de esta corrida** (pendientes de pasar a `docs/agentes/APRENDIZAJES.md`, que todavía no está en `main`)
- 2026-11-15 · En `probador.js`, "Fijar" es lo que pide la foto generada. Si un issue supone otra cosa, leelo contra el código, elegí lo que no gasta y dejá la decisión a Marco en el PR.
- 2026-11-15 · Un id que viene de la dirección se busca con `Array.find`, no en un objeto usado como diccionario: `objeto["constructor"]` devuelve algo y rompe la página.
- 2026-11-15 · Probar el JS sin sumar dependencias: `node` con el Playwright global (`require('/opt/npm-tools/node_modules/playwright')`, `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`) y un lanzador en `/tmp` que cambia `main.probador_ia` por uno falso. Los pedidos se cuentan con `page.on('request')`.
- 2026-11-15 · `.grilla a` le gana a `.secundario`: un botón dentro de la grilla necesita su propia regla de color.
- 2026-11-15 · Una rama creada desde `origin/main` queda siguiendo a `main`: `git branch --unset-upstream` y después `git push -u origin <rama>`.

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
