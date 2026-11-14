# Índigo Py — producción v3

Dos reels de 20 segundos con ropa y persona reales, títulos animados y cierre sobre la modelo en movimiento. `looks.mp4` presenta combinaciones; `consulta.mp4` pide modelo, talle y ciudad. Incluyen instrumental propio. `*-sin-musica.mp4` contiene la misma imagen sin audio.

Portadas: `*-portada.png`. Fotogramas de dirección: `*-gancho.png`, `*-demostracion.png`, `*-cierre.png`. Fichas visuales: `referencias/`. Guiones, captions, prompts por toma y mapa de motion: `GUIONES-Y-PROMPTS.md`. Fuentes y referencias pendientes: `FICHAS-Y-FUENTES.md`. Controles efectivamente realizados: `CONTROL-DE-CALIDAD.md`.

La fuente es 720×1280. El recorte de 590×1048 retira el título incrustado sin cortar el cuerpo en las tomas seleccionadas. La exportación 1080×1920 permite gráficos nítidos; no recupera detalle de la prenda. Para una producción con primeros planos más nítidos hace falta el original o una nueva grabación.

## Reconstrucción

Se incluyen fuente, montajes base, música, scripts y proyectos nativos Higgsedit con sus medios y fuentes. No requieren generar personas o ropa. Las versiones MP4 se pueden usar directamente.

Con Higgsedit compatible y FFmpeg, ejecutar `python3 preparar-montaje.py`, registrar Bebas Neue 400 y DM Sans 400/700 en cada proyecto, y ejecutar `INDIGO_ROOT="/ruta/absoluta/a/esta/carpeta" higgsedit build editar.jsx`. El build reemplaza la timeline; conservar una copia si hubo cambios manuales. Renderizar cada proyecto a 1080×1920, 30 fps, H.264, 10M en `looks-sin-musica.mp4` y `consulta-sin-musica.mp4`. Luego ejecutar `python3 crear-sonido.py` y `python3 finalizar.py`. `control-tecnico.py` genera verificaciones técnicas y hojas de cuadros para revisión visual.

El proyecto usa un único video base por reel para evitar saltos al buscar entre múltiples clips importados. Las selecciones originales siguen editables en `preparar-montaje.py` y los JSON; los textos y animaciones quedan editables en los proyectos nativos. No se usó captura de navegador para producir los gráficos.

No se publicaron las piezas, no se enviaron mensajes y no se activaron anuncios. No se consumieron modelos de generación de video o imagen. No se incluyen precios, promesas de stock, visitas, envío gratuito ni financiación.

