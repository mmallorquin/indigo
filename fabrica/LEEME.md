# Fábrica de piezas

Convierte cada prenda del catálogo en 5 láminas de carrusel (1080×1350), 3 stories (1080×1920), `textos.json` y `whatsapp.json`.

## Cargar una prenda
1. Fotos en `marketing/fabrica-entrada/` y una fila en `catalogo.csv` (columnas en `marketing/fabrica-entrada/LEEME.md`) con `estado` = `listo`.
2. Lo que dejes vacío (precio, talles, medidas) sale como "Consultá precio y talle por WhatsApp". No se inventa.
3. Las filas `DEMO` solo se usan si no hay ninguna `listo`, y llevan marca de agua.

## Correr local
```bash
ANTHROPIC_API_KEY=... python -m fabrica --entrada marketing/fabrica-entrada --salida salida/piezas --tope-usd 3
```
Opciones: `--skus A,B` (solo esos), `--tope-usd` (si el peor caso de la próxima llamada pasa el tope, no se hace). `FABRICA_CORTE` (fecha ISO) frena llamadas nuevas después de esa hora.

En Actions: Actions → fabrica → Run workflow.

## Salida
`salida/piezas/<sku>/`: `carrusel_01..05.png`, `story_01..03.png`, `textos.json`, `whatsapp.json` (códigos `IND-<sku>-C1`…), `listo.json` (si existe, el SKU se saltea). Más `resumen.md` y `gasto.json`.
Claude escribe solo los textos creativos; precio, talles y medidas salen del CSV. Las láminas se asignan por orden de fotos (Claude no ve las imágenes).
