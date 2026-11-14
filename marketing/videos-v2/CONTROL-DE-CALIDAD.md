# Control de calidad — Índigo Py v2

## Imagen y contenido

La revisión identificó transiciones incrustadas en el reel fuente que desplazaban la vista del cuerpo. Se ajustaron los rangos de entrada y salida. Además apareció un salto de imagen al exportar la última toma en el compositor: `finalizar.py` recompone ese tramo con el clip real decodificado por separado y conserva los títulos nativos. Las timelines finales están en el guion y en `editar.jsx`.

Control realizado sobre los archivos finales: decodificación completa de los cuatro MP4 y revisión visual de fotogramas cada 0,5 segundos en ambas piezas con música, además de portadas, fichas y tarjeta de cierre. Se revisaron texto, encuadre, cambios de outfit, color del producto y coherencia de cada toma con la fuente. Las hojas de revisión son `looks-qa.jpg` y `consulta-qa.jpg`. La revisión por fotogramas no equivale a una prueba de publicación dentro de Instagram o TikTok en un teléfono físico; no se hizo esa publicación.

Textos principales colocados en una banda superior sin cubrir el jean. Tarjeta de cierre durante 4 segundos, con número y mensaje en el área central. La forma animada de los títulos se revisó en los fotogramas exportados. No hay subtítulos de voz porque la fuente no tiene diálogo. El texto incrustado del video original se cubre con la banda gráfica.

La persona, el cuerpo y el jean proceden íntegramente del video real. No se generaron nuevas poses ni detalles, ni se modificaron color o calce. Las fichas son recortes identificados del mismo material. La identidad comercial del modelo de jean sigue pendiente de confirmación; las piezas invitan a consultar disponibilidad.

## Datos técnicos

Los valores medidos de cada archivo se incluyen en `datos-tecnicos.json`: duración, dimensiones, fps, número de cuadros, códecs, bitrate y pistas de audio. Cada pieza tiene 24 segundos y 720 cuadros, a 1080×1920 y 30 fps, H.264. Los masters sin música no contienen pista de audio; las versiones principales incorporan AAC estéreo a 48 kHz. El objetivo de codificación fue 10 Mbps; el bitrate medido puede diferir por el contenido.

El audio es la instrumental original incluida en el paquete. Se normalizó con objetivo −18 LUFS y techo de pico verdadero −1,5 dBTP durante la mezcla; son parámetros de procesamiento, no una medición posterior de loudness. No hay sincronización labial ni voz clonada. La imagen de las versiones con música se conserva mediante copia del flujo de video del master.

Fuente verificada: 27,7 segundos, 720×1280, H.264, 30 fps y sin audio. La fuente limita la nitidez: el export 1080p no inventa detalle ni se presenta como 4K.

## Datos comerciales

WhatsApp revisado antes de exportar: +595 973 434 868, coincidente con el enlace público de la bio. CTA único: «Escribinos JEANS por WhatsApp». No se publicaron precios, descuentos, medidas, talles ni stock no confirmados. No se prometen entrega gratuita, prueba a domicilio general ni crédito.

Las dos piezas son enfoques distintos; no se presentan como prueba controlada del gancho. No se publicaron, no se enviaron mensajes y no se activaron anuncios.
