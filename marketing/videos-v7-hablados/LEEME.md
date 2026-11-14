# Índigo · tres videos hablados · preparación

Formato seleccionado: vertical 9:16, 25–35 segundos, con una persona real hablando a cámara. Identidad de Índigo: olivo #4F5533, oscuro #30371F, marfil #F4F0E6 y dorado suave #C4AB79. Inter y Cormorant Garamond.

## Estado

Los tres guiones, los planes de gráficas y las maquetas editables están preparados. Las imágenes de `previews/` se renderizaron y revisaron: textos completos y regiones de cámara y gráficas separadas. Son pruebas visuales, no videos finales.

Falta la grabación real. El prompt original contenía `<path/to/raw.mp4>`, que es un marcador de posición, y todavía no se recibió una ruta válida ni un archivo hablado. Una toma larga puede servir para las tres piezas, o pueden usarse tres tomas separadas.

`GUIONES-PARA-GRABAR.md` contiene propuestas para grabar en español natural de Paraguay. Si la grabación está en portugués u otro idioma, la edición conservará ese idioma y la voz original; no se impondrá una traducción ni se fingirá que los guiones son transcripciones.

`brief-y-beats-provisionales.json` enumera los cues por frase, las fuentes públicas y las gráficas. Los índices de palabras y los tiempos del corte se mantienen nulos hasta analizar la voz real.

## Edición que depende del material

1. Verificar archivo, voz, idioma, resolución y cualquier dato privado visible. Ocultar referencias de domicilio antes del montaje.
2. Transcribir por palabras con Scribe si hay acceso disponible. Si se usa Whisper, ajustar cada extremo con la energía del audio real.
3. Elegir rangos de palabras, eliminar muletillas y repeticiones, preservar significado y redondear cortes a fotogramas de 30 fps. Medir ruido y silencios con RMS cada 10 ms; no aplicar −38 dBFS sin medir el material.
4. Seguir el rostro cada 0,2 s y suavizar sólo dentro de cada segmento. Validar recorte y espacio de gráficas con la cara real. El placeholder actual no simula un seguimiento facial realizado.
5. Cuar cada gráfica al inicio de las palabras reales, ajustar el formato vertical y mantener la cara libre. Diagramas y rótulos describen sólo prendas verificables.
6. Limpiar y comprimir voz, incorporar música y acentos discretos, realizar ducking y loudnorm de dos pasadas a −14 LUFS y −1,5 dBTP.
7. Re-transcribir la voz cortada y el mix, comparar palabras, reparar fragmentos o ataques cortados y verificar legibilidad, privacidad, duración y sincronía.
8. Entregar MP4 H.264 CRF 16, AAC 320k, BT.709 y faststart; SRT con 42 caracteres por línea y hasta dos líneas. Los capítulos se adaptan sólo si el formato/plataforma los necesita.

## Editables

Proyecto Remotion en `editor/`, con recursos locales y versiones fijadas. Desde esa carpeta: `npm ci`, luego `npm run dev`. Las composiciones 11–13 llevan el sufijo Maqueta y el atributo cameraSrc vacío intencionalmente. No exportar para publicación hasta integrar, revisar y sincronizar la grabación.

No se publicó contenido ni se generó una persona o una voz artificial.
