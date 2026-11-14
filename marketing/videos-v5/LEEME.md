# Índigo Py — dos videos de lanzamiento v5

La nueva dirección usa negro/blanco, Inter de gran peso, revelados de texto, producto que cambia de posición y escala, y música propia sincronizada con los cambios. Combina tres reels adicionales del perfil.

## Para mirar y elegir

- `lanzamiento-negro.mp4`: jeans, “ELEGÍ EL TUYO”, consulta con la palabra JEANS.
- `lanzamiento-blanco.mp4`: prendas y looks, “TU PRÓXIMO LOOK”, consulta con la palabra LOOK.
- `*-sin-musica.mp4`: misma imagen, sin audio, para usar música elegida en la aplicación.
- `*-portada.jpg` y `*-portada.png`: portada de cada propuesta.
- `GUIONES-Y-CAPTIONS.md`: escenas, captions listas y respuesta inicial para WhatsApp.
- `PROMPT-MAESTRO.md`: dirección actualizada para próximas piezas.

Export 9:16, 1080×1920, 30 fps, 20 s. La imagen original procede de copias 720×1280; los gráficos son nativos a 1080p. El negro/blanco es una dirección de campaña propuesta, no un cambio confirmado del logo o identidad general de la tienda.

## Proyecto editable

Las carpetas `lanzamiento-negro/` y `lanzamiento-blanco/` contienen los proyectos nativos de Higgsedit, medios usados y fuentes Inter. Pueden renderizarse directamente desde su `project.json`, con Higgsedit instalado. La música está mezclada en el MP4 final por separado; el proyecto gráfico produce la versión sin música.

Para reconstruir desde las fuentes en un entorno con Python/Pillow, FFmpeg y Higgsedit:

```sh
python3 preparar.py
INDIGO_ROOT="$PWD" higgsedit build editar.jsx
higgsedit render lanzamiento-negro --quality final --depth 8 --bitrate 10M --workers 2 --out "$PWD/lanzamiento-negro-sin-musica.mp4"
higgsedit render lanzamiento-blanco --quality final --depth 8 --bitrate 10M --workers 2 --out "$PWD/lanzamiento-blanco-sin-musica.mp4"
python3 sonido.py
python3 finalizar.py
python3 control-tecnico.py
```

Los recursos se incluyen para conservar la edición; no se reemplazaron instalaciones del equipo. El archivo `INDIGO-V5-LANZAMIENTO-COMPLETO.zip` reúne fuentes, bases, proyectos, música, export y documentación. Su contenido interno comienza en `videos-v5/`.

Antes de subir, revisar en la vista previa de la red social que los controles no tapen texto o producto. La publicación queda a elección del usuario. Las versiones anteriores se conservan en sus carpetas.
