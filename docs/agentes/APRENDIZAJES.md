# Aprendizajes del operador

Memoria entre corridas. Máximo 5 líneas por corrida, con fecha. Si pasa las 150 líneas, condensar.
Nada de acá puede aflojar las "Reglas que no se rompen" del prompt ni de `CLAUDE.md`.

## 2026-11-14 (noche)
- `pip` suelto instala en el Python del sistema y pytest no ve los módulos: usar `python3 -m pip` y `python3 -m pytest` (42 tests pasan en main).
- No había `gh` ni `GH_TOKEN`: `gh` sale de apt; sin token, el estado se lee de las páginas públicas (`estado_sin_gh.py`) y git push igual funciona. La API sin token se queda sin cupo enseguida: no depender de ella.
- PR #12 (tienda) y #13 (fábrica 1) pasan sus tests pero chocan en `docs/campanas/PROGRESO.md`: no tocar archivos compartidos en PR de tareas; poner la novedad en la descripción.
- Con #12 y #13 sin mergear, ningún issue queda desbloqueado (#6, #7 dependen de /tienda; #8 de #6; #9 de fábrica 1; #10 es fase 2). Corrida dedicada a revisión y auto-mejora, sin apilar ramas.

## 2026-11-15 (productor)
- Antes de producir, revisá `ejemplo` en el JSON `#datos` de /probador (la API /probador/prendas pide contraseña). Si todas las prendas son de ejemplo, no hay producto real: no se hacen piezas.
- /probador/modelo.jpg es una persona real: no se usa en piezas hasta que Marco lo autorice por escrito.

## 2026-11-15 (productor, 2.ª corrida)
- Si el plan no está en main, buscalo en las ramas `operador/estrategia-*` (`git fetch origin`): ahí estaba.
- Aunque no haya prendas reales, las piezas "sin prenda" del plan (cómo pedir, talle) sí se pueden hacer: no dejar la corrida en cero.
- En stories con sticker, dejá el espacio vacío: un aviso dibujado ("acá va el sticker") se termina publicando.

## 2026-11-15 (productor, 3.ª corrida)
- Si tu rama vieja quedó atrás de main, mergeá `origin/main` (después de `git fetch origin main`: `origin/main` local puede estar viejo) antes de evaluar qué toca el PR.
- Guardá el JSON de entrada de cada pieza junto a los PNG: sin él, corregir una palabra obliga a reconstruir todo el texto.
- El estado de WhatsApp no tiene sticker de enlace ni de preguntas: misma imagen, texto "Respondé este estado" y mismo código; en el registro va otra fila con red `whatsapp`.

## 2026-11-15 (productor, 4.ª corrida)
- Antes de producir, mirá también los comentarios del issue #3 (API con `GH_TOKEN` vía fetch): ahí aparecen las respuestas de Marco. Si no cambió nada (prendas, catálogo, respuestas), cerrá en corto: progreso y aviso, sin rehacer piezas.
- Para carruseles de prenda real, primero la fábrica (`python3 -m fabrica --skus <sku>`): no dupliques su trabajo con Pillow a mano.
