# Control de la entrega editorial

Verificación realizada sobre los tres MP4 de `finales/`, el 13 de octubre de 2026. El script `editor/scripts/control.py` decodificó audio y video completos, leyó los metadatos, analizó negros y movimiento, midió el audio final y extrajo 40 fotogramas distribuidos desde el primero hasta el último de cada archivo.

| MP4 | Video | Duración de imagen | LUFS-I medidos | Pico verdadero medido |
|---|---|---:|---:|---:|
| 11-combinaciones | 1080 × 1920 · 30 fps | 30,50 s | −13,99 | −1,80 dBTP |
| 12-detalles | 1080 × 1920 · 30 fps | 30,50 s | −13,91 | −1,80 dBTP |
| 13-capas | 1080 × 1920 · 30 fps | 31,50 s | −14,02 | −1,79 dBTP |

Los contenedores duran 30,60 / 30,60 / 31,60 segundos por la cola de audio/codificación. Todos quedan dentro de los 35 segundos. H.264, yuv420p, BT.709, AAC estéreo de 48 kHz, objetivo 320 kb/s y `moov` antes de `mdat` para inicio rápido. Export inicial CRF 16 y posterior copia del video durante el master, sin otra pérdida visual.

## Revisión visual y de contenido

Se revisaron las tres hojas de contacto completas de 40 imágenes y las escenas clave de títulos, fotografías, listas, diagramas y cierres. Los mensajes principales se leen completos después de sus revelados y permanecen dentro del área de composición. Las letras que aparecen parcialmente durante una entrada corresponden a la animación por máscara. Los CTA se mantienen legibles durante el cierre.

Las fotografías tienen sus colores originales. Los encuadres de personas dejan los rostros visibles; las tarjetas pequeñas y las anotaciones no se colocan sobre ellos. No se incorporan direcciones, vistas residenciales identificables ni referencias al domicilio del usuario. El logo mantiene sus proporciones. No quedaron campos de grabación, instrucciones de cámara ni rótulos de maqueta.

Cada video tiene un gancho dentro de sus dos primeros segundos, título de 1,5 segundos, desarrollo propio y un solo CTA. Los contadores describen el número de referencias mostradas; no son estadísticas comerciales. Se conservaron los nombres y las prendas visibles en las fuentes de `INDICE.md`, sin promociones, precios ni promesas de stock.

## Movimiento, audio e integridad

La decodificación completa no produjo errores y el detector de negro no encontró segmentos negros. Los hashes de todos los fotogramas decodificados son consecutivamente distintos: la racha máxima de imágenes idénticas fue de un fotograma (0,033 s) en las tres piezas.

El detector perceptual `freezedetect` a −60 dB y 0,3 s sí genera alertas en composiciones con movimiento muy suave y texto sostenido. Se conservan esos registros en `datos-tecnicos.json`; no se los presenta como un control sin alertas. Las escenas señaladas son fotografías con acercamientos suaves o cierres gráficos con movimiento sutil, revisadas en las hojas de contacto y en los fotogramas clave. No hay secuencias de fotogramas idénticos de más de 0,3 segundos.

Música instrumental y efectos generados localmente, sin voz, con entradas/salidas suaves y cambio de pista mediante crossfade de cuatro segundos. Master de dos pasadas hacia −14 LUFS, techo previo de −1,8 dBTP para mantener margen en AAC. Las cifras de la tabla son las mediciones de la mezcla AAC final, no las del WAV ni las cifras objetivo. No se aplica control de claridad de voz por retranscripción porque no hay voz.

Los SRT de apoyo contienen el texto editorial principal: máximo 42 caracteres por línea y dos líneas. El proyecto pasa la compilación TypeScript sin emitir archivos. La galería carga los tres MP4 con dimensiones correctas y sin errores de medios. Los hashes SHA-256 y la validación CRC del ZIP completan la comprobación de la entrega.

La revisión humana final se realiza en `index.html`; la publicación es manual.
