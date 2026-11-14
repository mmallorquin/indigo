# Revisión de la colección

Verificación del 26 de octubre de 2026 sobre las exportaciones finales.

| Reel | Imagen | Duración | LUFS-I final | Pico verdadero final |
|---|---|---:|---:|---:|
| 14 · Neutros | 1080 × 1920, 30 fps | 22 s | −14,12 | −1,80 dBTP |
| 15 · Pantalones | 1080 × 1920, 30 fps | 22 s | −14,23 | −1,79 dBTP |

Los dos MP4 se decodificaron completos sin errores. H.264 CRF 16, yuv420p, BT.709, AAC estéreo 48 kHz y faststart. Normalización de dos pasadas; los valores de la tabla corresponden a AAC final. No se encontraron segmentos negros. Cada hoja de contacto contiene 40 fotogramas desde el primero hasta el último; se revisaron ambos recorridos completos y escenas clave a resolución de exportación.

Los fotogramas consecutivos decodificados son distintos, con racha máxima idéntica de un frame. `freezedetect` registra alertas en planos fotográficos con movimiento suave y texto sostenido; se conservan en `datos-tecnicos.json`, sin presentarlo como una prueba sin alertas. Las piezas usan fotos, revelados y acercamientos editoriales; no pretenden mostrar movimiento real de una modelo.

Se revisaron las diez placas locales, las páginas PDF renderizadas, capturas de Figma y miniaturas de las versiones finales de Canva. Se corrigió un recorte en etiquetas pequeñas antes de exportar. La importación inicial de PDF a Canva alteraba agrupación y posición de texto; se sustituyó por HTML paginado, comprobando después el contenido textual y las dimensiones 1080 × 1350 de sus cinco páginas por diseño. Las versiones PDF iniciales de Canva no son los enlaces entregados.

En Figma se validaron los diez frames, sin textos fuera del lienzo, con variables de color y fotos como instancias de componentes. La comparación del sastrero usa un recorte de la foto original. El esquema de medidas es genérico, sin cifras inventadas. Ningún texto cubre los rostros de las modelos; no se alteraron colores de prendas ni proporciones del logo.

TypeScript compiló sin emitir archivos. El empaquetado valida cantidades, hashes de recursos, CRC del ZIP y enlaces locales de la galería. La disponibilidad de productos requiere consulta; la revisión comercial y publicación quedan a cargo de la tienda.
