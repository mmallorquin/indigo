# Progreso de la maratón

## Ciclo 1 (14/11/2026)
- Hecho: A1–A4 (estrategia, embudo, calendario de 14 días, guiones de WhatsApp).
- **Bloqueo de B (piezas):** las 4 prendas de /probador (`ejblusa`, `ejchaleco`, `ejjean`, `ejpantalon`) tienen `ejemplo: true`: son imágenes de ejemplo, no prendas reales de la tienda. Y `/probador/modelo.jpg` es una foto de una persona real. Hacer flyers y reels de prendas que no existen sería inventar producto, así que B queda en pausa hasta que Marco suba prendas reales en /probador/prendas (o confirme que se pueden usar las de ejemplo) y autorice usar la modelo.
- Sigue: C (issues #5, #6, #7, #8) — #4 y #5 ya los trabaja el agente de Actions.

## Ciclo 2 (14/11/2026)
- A1–A4 mergeado (#11).
- Issue #5: /tienda pública (PR abierto, toca app/: lo aprueba Marco).
- Entorno: los tests corren con `/usr/local/bin/python3 -m pytest -q` (44 pasan).
- Sigue: #6 (botón WhatsApp) cuando se mergee #5 — depende de él.
