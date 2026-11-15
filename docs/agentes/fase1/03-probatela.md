**Objetivo:** que desde la tienda se pueda probar una prenda con un toque.

**Depende de:** la tienda pública (`/tienda`) ya mergeada.

**Qué hacer**
- Botón "Probátela" en cada prenda de `/tienda` que abre `/probador?prenda=<id>`.
- En `probador.js`, si viene `?prenda=<id>` y la prenda existe, la rueda arranca en esa prenda y la deja fijada. Si no existe, el probador abre normal.
- No cambia nada de los topes ni de la privacidad: fijar una prenda no genera imagen; la imagen se genera recién cuando la persona lo pide, como hoy.

**Listo cuando**
- Probado con una prenda existente y con un id inexistente.
- `pytest -q` pasa completo (agregar test si se toca algo del servidor).
