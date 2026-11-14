# Índigo Py — producción de video v2

Dos reels de 24 segundos con material real: `looks.mp4` muestra combinaciones; `consulta.mp4` orienta la consulta por WhatsApp. Ambos incluyen música instrumental propia. Los archivos `*-sin-musica.mp4` conservan exactamente la misma imagen sin música; la fuente no contiene diálogo ni sonido útil.

Las portadas son `looks-portada.png` y `consulta-portada.png`. Las láminas de persona y producto están en `referencias/`. `GUIONES-Y-PROMPTS.md` contiene las timelines, textos, captions y prompts por toma; `FICHAS-Y-FUENTES.md` registra referencias y grabaciones faltantes. `CONTROL-DE-CALIDAD.md` documenta los controles realizados.

La fuente disponible es 720×1280. El montaje se exporta a 1080×1920 y 30 fps, con H.264 y AAC estéreo a 48 kHz en las versiones con música. La exportación mejora la presentación gráfica; no recupera detalle de la ropa.

## Proyecto editable

Se incluyen el video fuente, la música, `editar.jsx`, el script de láminas y los proyectos nativos `looks/` y `consulta/` con sus archivos de medios y tipografías. Para reconstruir se requiere Higgsedit compatible; los MP4 se pueden usar directamente sin ese programa.

Los scripts conservan las rutas absolutas del entorno que produjo los archivos. En otra máquina hay que ajustar `root`, la ruta de `source.mp4` y las entradas del script de láminas. Se incluyen `preparar-clips.py` y la carpeta `clips/`: son recortes reales decodificados desde el archivo original, con tiempo de inicio restablecido, para que el editor abra cada toma desde su primer cuadro. Ejecutar primero ese script si necesitan reconstruir los recortes, y luego `higgsedit build editar.jsx`. Los medios importados de los proyectos se conservan en sus carpetas. `higgsedit build` reemplaza la timeline: usar una copia si modificaron manualmente el proyecto.

Para reconstruir la entrega: renderizar cada proyecto a H.264 y 30 fps en `looks-composicion.mp4` y `consulta-composicion.mp4`; después ejecutar `finalizar.py`. Este paso conserva la composición nativa y decodifica la última toma real por separado: evita un salto de imagen observado al exportar ese clip desde el compositor. También mezcla `instrumental-original.wav`, codifica AAC estéreo a 48 kHz y prepara los archivos para reproducción progresiva. Los archivos intermedios de composición se regeneran desde los proyectos y no forman parte del paquete; los masters finales sí se incluyen. No hace falta generar personas o prendas para reconstruir estas piezas.

## Uso y comparación

Las dos piezas cambian el enfoque y la selección de tomas. Compararlas no aísla el efecto del gancho. Los ganchos alternativos del guion se pueden probar en futuras versiones manteniendo igual el resto del video y el CTA.

Registrar por pieza consultas nuevas, consultas con modelo/necesidad, talle y ciudad; cotizaciones y pedidos pagados y entregados. No se fijaron metas de ventas ni presupuesto publicitario. Estos archivos se prepararon para revisión; no se publicaron ni se activaron anuncios.
