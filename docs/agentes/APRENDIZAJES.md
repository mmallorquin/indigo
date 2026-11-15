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
