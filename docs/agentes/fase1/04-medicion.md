**Objetivo:** medir el embudo de venta: visitas a la tienda, pruebas en el probador y clics a WhatsApp.

**Depende de:** el botón de WhatsApp ya mergeado.

**Qué hacer**
- Enviar eventos a Application Insights (`appi-indigo`): `vista_tienda`, `vista_prenda`, `prueba_probador` (cuando se genera una imagen) y `clic_whatsapp`.
- Si hace falta una dependencia (por ejemplo `azure-monitor-opentelemetry`), agregarla con versión en `requirements.txt` y explicar por qué en el PR. La conexión se toma de la variable `APPLICATIONINSIGHTS_CONNECTION_STRING`; si no está (local o tests), la app funciona igual sin enviar nada.
- Ningún evento lleva datos personales: ni IP, ni foto, ni teléfono. Solo el nombre del evento, la prenda y la categoría.
- En la descripción del PR, dejar la consulta KQL para ver el embudo de los últimos 7 días.

**Listo cuando**
- Tests verifican que, sin la variable de conexión, no se envía nada y nada falla.
- `pytest -q` pasa completo.
- El PR dice qué variable de entorno hay que cargar en `ca-indigo` (la carga Marco).
