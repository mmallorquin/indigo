**Objetivo:** que al cargar una prenda en el catálogo salgan, en una sola corrida, sus textos, un carrusel y stories listos para revisar y publicar.

Es la base de la "fábrica de piezas". La corre `.github/workflows/fabrica.yml` (ya existe; no lo toques: `.github/` es zona prohibida). Esa corrida baja las entradas del Storage, ejecuta el comando de abajo y sube lo que quede en la carpeta de salida.

**Interfaz que espera el workflow (respetala tal cual)**

```
python -m fabrica --entrada marketing/fabrica-entrada --salida salida/piezas [--skus A,B] [--tope-usd 8]
```

- Lee `catalogo.csv` de la carpeta de entrada. Columnas: `sku,nombre,categoria,precio_gs,talles,stock,medidas,entrega,fotos,clips,prenda_probador,estado`. `fotos` y `clips` son nombres de archivo separados por `|`, relativos a la carpeta de entrada.
- Procesa las filas con `estado` = `listo` (o las de `--skus`). Las filas `DEMO` solo se usan si no hay ninguna `listo`, y sus piezas llevan una marca de agua "DEMO" visible.
- Por cada SKU escribe en `salida/piezas/<sku>/`:
  - `carrusel_01.png` … `carrusel_05.png` (1080×1350): portada, detalle, combinaciones, talles y medidas, y cierre con WhatsApp.
  - `story_01.png` … `story_03.png` (1080×1920): producto, cómo combinarlo y cómo comprar.
  - `textos.json`: caption de Instagram, caption de TikTok, 10 hashtags, texto alternativo de cada imagen y 2 ganchos distintos para la misma prenda ("Así queda puesto" contra "Precio y talles disponibles").
  - `whatsapp.json`: un enlace `wa.me` por pieza, con el número de `[contacto]` de `marca.toml` y un mensaje prellenado con código de pieza (`IND-<sku>-C1`, `IND-<sku>-S2`, …), para saber qué pieza trajo cada consulta.
  - `listo.json` al terminar ese SKU. Si existe, el SKU se saltea (la corrida se puede reanudar).
- Escribe `salida/piezas/resumen.md` (tabla: SKU, piezas generadas, datos faltantes, costo) y `salida/piezas/gasto.json` (tokens y USD por llamada y totales).
- Sale con código 0 aunque falle un SKU (lo anota en el resumen y sigue). Sale con código distinto de 0 solo si falla la autenticación con la API o no puede escribir la salida.

**Reglas**

- Claude (Sonnet) escribe los textos y elige qué foto va en cada lámina. Llamarlo por HTTP con `httpx`, como `marketing/api-credito/indigo_api.py`; la key llega en `ANTHROPIC_API_KEY`. Sin dependencias nuevas si se puede (Pillow y httpx ya están).
- **Tope de gasto:** antes de cada llamada, estimar su costo máximo; si la suma superaría `--tope-usd`, no llamar y cortar con el motivo en el resumen. Si existe la variable `FABRICA_CORTE` (fecha y hora ISO) y ya pasó, no iniciar llamadas nuevas.
- Precio, talle, stock y entrega: solo los del CSV. Si falta, la pieza dice "Consultá precio y talle por WhatsApp" (es la política de `marca.toml`). Nunca inventar.
- Identidad: colores de `[identidad]` en `marca.toml` y tipografías de `app/static/fuentes` (Inter y Cormorant Garamond). El precio tiene que leerse bien en un celular.
- Español de Paraguay con voseo. Sin escasez falsa ("últimas unidades") salvo que el CSV lo diga.
- Agregar `fabrica/LEEME.md` corto: cómo cargar una prenda y cómo correrlo local.

**Listo cuando**

- Tests con un Claude falso y fotos chicas generadas en el test: genera todas las piezas de un SKU, respeta el tope, saltea un SKU con `listo.json` y no inventa precio cuando falta.
- `pytest -q` pasa completo.
