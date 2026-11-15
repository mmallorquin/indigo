**Objetivo:** sumar a la fábrica un Reel en video, una revisión automática de calidad y, cuando se pueda, la vista "así queda puesto" del probador.

**Depende de:** "Fábrica 1" ya mergeada. Misma interfaz de línea de comandos; no tocar `.github/`.

**Qué hacer**

- **Reel** `reel.mp4` (1080×1920, 15 a 25 s, H.264 + AAC silencioso o sin audio) armado con FFmpeg a partir de las fotos y clips del CSV: movimiento suave en las fotos, textos del guion encima y cierre con la marca y "Pedí por WhatsApp". Claude (Sonnet) escribe el guion (gancho, 3 a 5 textos cortos, cierre) y lo guarda en `textos.json`. Si FFmpeg no está, saltear el Reel y anotarlo.
- **Revisión** `revision.json` por SKU: Claude mira cada PNG y un fotograma del Reel y responde en JSON si el precio se lee, si la prenda coincide con la foto original, si hay errores de texto o datos inventados, y un puntaje de 1 a 10 con el motivo. Si algo falla, regenerar esa pieza una sola vez; si vuelve a fallar, dejarla marcada "revisar" en el resumen.
- **Vista del probador** (opcional por SKU): si la fila tiene `prenda_probador` y existe la variable `FABRICA_APP_URL`, pedir `POST {FABRICA_APP_URL}/probador/probar` con esa prenda y la modelo de ejemplo (sin foto de clienta), vista `frente`. Ese pedido respeta los topes de la app y queda en caché. Usar la imagen como lámina extra del carrusel con la leyenda "Imagen generada con IA". Si el tope del día está lleno, seguir sin ella.
- Sumar al resumen el puntaje de revisión por pieza.

**Listo cuando**

- Tests: con FFmpeg presente genera un MP4 válido (se puede saltear el test si no hay FFmpeg); la revisión con Claude falso marca una pieza mala y la regenera una vez; sin `FABRICA_APP_URL` no se llama al probador.
- `pytest -q` pasa completo.
