**Objetivo:** que cualquier persona vea las prendas de Indigo en una página pública, cómoda en el celular.

**Qué hacer**
- Nueva ruta pública `GET /tienda` (sin contraseña) con una grilla de las prendas visibles (`pb.prendas_visibles`), con su foto (`/probador/prenda/<id>.jpg`), nombre y categoría.
- Pestañas o filtro por categoría, reutilizando `pb.PESTANAS`.
- Usar la identidad de `marca.toml` y `base.html` (colores, tipografías, modo claro y oscuro).
- Precio, talle y stock: mostrar solo lo que ya exista en los datos de la prenda. Si no está, mostrar "Consultanos por WhatsApp". Nunca inventar.
- Agregar un enlace a `/tienda` desde `/probador` y desde el inicio.

**Listo cuando**
- `/tienda` carga sin contraseña y se ve bien en un celular de 375 px de ancho.
- Hay tests nuevos para la ruta (con y sin prendas) y `pytest -q` pasa completo.
