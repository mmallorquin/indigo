**Objetivo:** que cada prenda tenga un botón para pedirla por WhatsApp, y saber cuántas veces se toca.

**Depende de:** la tienda pública (`/tienda`) ya mergeada.

**Qué hacer**
- Botón "Pedir por WhatsApp" en cada prenda de `/tienda` y en el probador.
- El botón apunta a una ruta propia, `GET /ir/whatsapp/<id_prenda>`, que anota el clic y redirige (302) a `[contacto].whatsapp_url` de `marca.toml` con un mensaje prellenado: "Hola Indigo, me interesa <nombre de la prenda>. ¿Tienen en mi talle?" (codificado para URL).
- Por ahora el clic se anota en el log (`logging`) con la prenda y la fecha, sin datos de la persona (sin IP, sin teléfono). La medición formal llega en otro issue.

**Listo cuando**
- Tests de la redirección: id existente → 302 al wa.me con el mensaje; id inexistente → 404.
- `pytest -q` pasa completo.
