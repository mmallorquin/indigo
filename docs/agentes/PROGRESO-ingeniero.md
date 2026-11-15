# Progreso del Ingeniero

## Corrida del 15/11/2026 (mañana)

**Qué encontré**
- Conexión bien: `gh` con token, permiso de push, último deploy en verde y `/salud` con el sha de `main` (`5b00591`).
- No existe la etiqueta `ingeniero` ni hay issues con ella. Los dos que pidió el estratega siguen solo en `docs/estrategia/issues-ingeniero.md` (rama `operador/estrategia-2026-11-15`, sin PR).
- PR #12 (tienda pública, issue #5): tests en verde, pero en conflicto con `main` por `docs/campanas/PROGRESO.md`. Sin comentarios de Marco ni del Revisor.
- #6, #7 y #8 dependen de que `/tienda` esté en `main`. #9 no tiene dependencias pendientes, pero vive en `fabrica/`.

**Qué hice**
- PR #12: traje `main` a la rama (merge, sin forzar el push) y dejé `PROGRESO.md` igual que en `main`; el PR ya no toca `docs/campanas/`. Quedó sin conflicto y con checks en verde (50 tests).
- PR #12: revisé `/tienda` a 375 px con capturas (claro y oscuro). Corregí dos detalles con 3 líneas de CSS: categoría y precio salían en el mismo renglón, y el botón de WhatsApp quedaba pegado a la grilla.
- No mergeé nada: falta la revisión del Revisor. No abrí PR de issue nuevo: no hay ninguno desbloqueado en mi zona.

**Qué quedó pendiente**
- Revisor o Marco: revisar el PR #12. Es lo que destraba #6, #7 y #8.
- Marco: decidir si `fabrica/` es zona del Ingeniero. Hoy mi lista es `app/`, `tests/`, los `.py` de la raíz y `.claude/skills/`; el #9 y los dos pedidos del estratega (variante B `C1B` y resumen de `registro.csv`) están en `fabrica/`.
- Marco: crear los dos issues del estratega con la etiqueta `ingeniero` (la variante B hace falta para la prueba del martes 17 y miércoles 18).

**Para la próxima corrida**
1. Si el PR #12 tiene ✅ o ⚠️ sin bloqueantes y checks en verde: mergear, esperar el deploy y verificar el sha en `/salud`. Después, abrir `/tienda` en producción.
2. Con `/tienda` en `main`: tomar el #6 (botón de WhatsApp) e incluir el parámetro opcional `pieza` que pidió el estratega. Después el #7.
3. El #8 necesita una dependencia en `requirements.txt` (zona protegida): ese PR queda abierto para Marco.
4. Contar los merges del día en hora de Paraguay: #11 y #13 figuran con fecha 15/11 en UTC, pero fueron el 14/11 a la noche.

**Aprendizajes de esta corrida** (pendientes de pasar a `docs/agentes/APRENDIZAJES.md`: ese archivo no está en `main` y ya lo crean dos ramas sin mergear; crearlo acá sumaría un tercer choque)
- 2026-11-15 · `gh`: si apt no lo encuentra, primero `apt-get update -q`. `gh pr edit` falla en la versión 2.45 (error de Projects classic): usar `gh api -X PATCH repos/<repo>/pulls/<n> -F body=@archivo.md`.
- 2026-11-15 · Un PR que choca en un archivo compartido se arregla con `git merge origin/main` en la rama y `git checkout --theirs <archivo>`: queda como en `main`, sin forzar el push.
- 2026-11-15 · Capturas a 375 px: Playwright ya tiene Chromium (`/opt/pw-browsers`). Levantar `uvicorn` con `APP_PASSWORD=prueba PROBADOR_IA=0`, cargar prendas con `POST /probador/prendas` y medir `scrollWidth - clientWidth` (tiene que dar 0).
- 2026-11-15 · En `.grilla`, dos `<span>` seguidos salen en el mismo renglón: mirar siempre la captura, los tests de texto no lo detectan.
- 2026-11-15 · Antes de elegir issue, comparar su carpeta con mi zona: `fabrica/` no está en la lista y hoy los pedidos nuevos caen ahí.
