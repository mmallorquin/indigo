# Revisión visual — colección C (08, 09 y 10)

Estado: previews regenerados revisados; revisión de MP4 completos pendiente de exportación final.

## Previews inspeccionados

Se abrió individualmente cada JPG en resolución original:

- 08-cuellos: 1,5; 6,5; 11,5 y 16,5 segundos.
- 09-azul-crema: 1,5; 6,5; 11,5 y 16,5 segundos.
- 10-jeans: 1,5; 6,5; 11,5 y 18,5 segundos.

Resultado de los doce previews actuales: ortografía correcta, contraste adecuado, proporciones conservadas, CTA y contacto legibles, sin clipping ni solapamiento de texto con prendas o notas. Los textos principales conservan márgenes respecto del borde inferior y de los controles laterales habituales. Esta comprobación visual no sustituye una prueba de la interfaz de cada plataforma.

## Hallazgo corregido y vuelto a verificar

Los primeros previews mostraban la secuencia literal `\n` en texto y, en 08 a 11,5 s, recortaban el final de «Presencia». Afectaba también frases de 09 y 10. El coordinador corrigió `Brand.tsx`, línea 25, para normalizar la secuencia antes de separar líneas. Los doce previews regenerados muestran ahora los saltos reales; «Cuello. / Textura. / Presencia.» y las otras frases están completos.

Los tamaños y posiciones de `Type` en estos stills exportados coinciden con la composición. No se observa en estos exports el comportamiento de valores por defecto que el coordinador describió al mirar Studio. No se modificó código en esta revisión.

## Ajuste visual sugerido

10-jeans, 6,5 s, escena «Jean en percha» (4–8 s): la fuente contiene una disolvencia, con silueta y pantalón semitransparentes superpuestos. La prenda conserva proporción, pero el momento reduce la claridad del producto. Conviene usar un tramo estable de la fuente o una imagen fija real. Referencia: `CollectionC.tsx`, `JeansLook`, línea 15; `Clip` utiliza `start={.3}`. Pendiente de decisión del coordinador y de comprobación en el MP4.

## Pendiente para completar

- Escena «Preguntas útiles» de 10-jeans, 12–16 s, no incluida en los cuatro previews recibidos.
- 08 y 10: extraer e inspeccionar hoja de contacto cada segundo, incluyendo frame 0 y último frame del MP4 definitivo.
- Comprobar que las correcciones observadas en stills aparecen en los MP4 finales y que el contacto permanece legible en el cierre.

Las diez pistas WAV ya fueron medidas por separado. El coordinador aplica la envolvente de entrada/salida correspondiente a la duración de cada video mediante `Music`.
