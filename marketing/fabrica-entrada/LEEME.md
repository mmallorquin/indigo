# Entrada de la fábrica de piezas

1. Copiá acá las fotos (y clips cortos, si tenés) de cada prenda.
2. Agregá una fila por prenda en `catalogo.csv` (se abre con Excel o Numbers; guardalo como CSV):

| Columna | Qué va | Ejemplo |
|---|---|---|
| sku | Código corto, sin espacios | JEAN-MOM-01 |
| nombre | Cómo se llama la prenda | Jean mom tiro alto |
| categoria | jean, blusa, pantalón, vestido, conjunto… | jean |
| precio_gs | Precio en guaraníes, solo números. Vacío = "Consultá precio" | 189000 |
| talles | Separados por `/` | 36/38/40 |
| stock | Unidades disponibles. Vacío = no se menciona | 6 |
| medidas | Medidas útiles para elegir talle | Cintura 70 cm (talle 38) |
| entrega | Cómo se entrega | Envío a todo Paraguay por transportadora |
| fotos | Archivos separados por `\|` | jean-mom-1.jpg\|jean-mom-2.jpg |
| clips | Videos cortos separados por `\|` (opcional) | jean-mom.mp4 |
| prenda_probador | Id de la prenda en /probador/prendas (opcional) | |
| estado | `listo` para que la fábrica la procese | listo |

3. Subilo a Azure: `bash ~/vibe_coding/indigo/marketing/sincronizar-medios.sh subir`
4. Corré la fábrica: GitHub → Actions → **fabrica** → Run workflow.

La fila `DEMO-JEAN` es solo para probar: sus piezas salen con marca de agua "DEMO". Borrala cuando cargues prendas reales.
Nunca se inventan precios, talles ni stock: lo que falte sale como "Consultá por WhatsApp".
