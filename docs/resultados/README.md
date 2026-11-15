# Resultados

Acá va `registro.csv`, el archivo que carga Marco con lo que pasó con cada pieza publicada. El estratega lo lee cada semana para decidir qué repetir y qué cambiar.

**Estado al 15/11/2026:** el archivo todavía no existe. Para empezar, creá `docs/resultados/registro.csv` con esta primera línea:

```
fecha,codigo,red,alcance,consultas,ventas,monto_gs
```

## Qué va en cada columna

| Columna | Qué va | Formato |
|---|---|---|
| `fecha` | El día que se publicó la pieza | AAAA-MM-DD |
| `codigo` | El código de la pieza | `IND-<sku>-<pieza>` |
| `red` | Dónde se publicó | `instagram` o `tiktok` |
| `alcance` | Cuentas alcanzadas, según las estadísticas de la red | Número, sin puntos |
| `consultas` | Chats de WhatsApp que llegaron por esa pieza | Número |
| `ventas` | Pedidos **pagados** que salieron de esas consultas | Número |
| `monto_gs` | Total cobrado por esas ventas, en guaraníes | Número, sin puntos |

Forma de una fila (los valores entre < > se reemplazan por los reales):

```
<fecha>,IND-<sku>-C1,instagram,<alcance>,<consultas>,<ventas>,<monto_gs>
```

## Reglas para cargar

- Una fila por pieza y por red. Si el mismo carrusel salió en Instagram y en TikTok, son dos filas.
- El alcance y las consultas se anotan 72 horas después de publicar. Si más tarde entra una venta, se corrige esa fila; no se agrega otra.
- Una consulta cuenta para la pieza cuyo código trae el primer mensaje ("Hola, vengo por IND-…"). Si no trae código, preguntá "¿qué publicación viste?". Si no se sabe, anotala con el código `IND-SINCODIGO-X`.
- Una venta cuenta solo si está pagada.
- Si un dato no se sabe, dejá la celda vacía. No pongas cero ni un número estimado: cero quiere decir "miré y no hubo".
- No van nombres, teléfonos ni ningún dato de las clientas.

## Códigos de pieza

- `C1` a `C5`: láminas del carrusel (el carrusel entero se anota como `C1`). `C1B`: carrusel con la portada B de la prueba.
- `S1` a `S4`: stories. `R1`: Reel. `FLY`: flyer.
- `<sku>` es el de `catalogo.csv`. Las piezas que no son de una prenda usan `MARCA` (por ejemplo `IND-MARCA-S1`).

## Qué calcula el estratega

Por pieza y por prenda: consultas, ventas, ventas por consulta y consultas por cada 1.000 de alcance. Si el denominador es cero, se informa "no calculable".
