# Música instrumental original — Índigo Py v6 olivo

Las diez pistas se sintetizaron íntegramente con el generador local `editor/scripts/musica.py`. No contienen voz, grabaciones de personas, loops, samples, melodías importadas ni archivos de audio externos. Los timbres de teclas, bajo, kick, hi-hat y caja suave se construyen con osciladores, envolventes y ruido pseudoaleatorio de semilla fija. Las progresiones y patrones están definidos en el script.

## Uso

Audio creado por encargo para estas piezas de Índigo Py. Se entrega para usar, editar, recortar y distribuir en el contenido de la marca, sin pago adicional ni atribución obligatoria. No se incorpora material musical de terceros. Python, NumPy y FFmpeg son herramientas de síntesis y procesamiento; sus archivos o grabaciones no se incluyen como samples.

## Reproducción

Requisitos: Python 3 con NumPy y FFmpeg/FFprobe en PATH. Ejecutar `python3 editor/scripts/musica.py` desde la raíz de `videos-v6-olivo`, o ejecutar el script por ruta absoluta. Las semillas son fijas. La síntesis es reproducible; pequeñas diferencias de normalización pueden depender de la versión de FFmpeg.

Formato: WAV PCM de 16 bits, 48.000 Hz, estéreo, 24 segundos por pista. Entrada de 0,8 s y salida de 2 s con curva suave. Pulsos entre 100 y 112 BPM. Normalización EBU R128 hacia −18 LUFS-I con techo de −3,2 dBTP.

Al recortar una pista para un video de menos de 24 s, aplicar una nueva salida suave durante el último segundo del video; la salida incluida termina al segundo 24.

## Mediciones de los WAV finales

| Archivo | Referencia | BPM | Duración s | Pico dBFS | LUFS-I | Pico dBTP | LRA LU |
|---|---|---:|---:|---:|---:|---:|---:|
| 01.wav | Estampa | 100 | 24.000 | -3.200 | -18.04 | -3.20 | 2.30 |
| 02.wav | Capas | 102 | 24.000 | -3.200 | -18.04 | -3.20 | 2.40 |
| 03.wav | Base | 104 | 24.000 | -4.364 | -18.00 | -4.36 | 3.10 |
| 04.wav | Lineas | 106 | 24.000 | -3.216 | -18.00 | -3.22 | 3.80 |
| 05.wav | Tres ideas | 108 | 24.000 | -3.200 | -18.04 | -3.20 | 3.10 |
| 06.wav | Detalle | 110 | 24.000 | -3.311 | -18.00 | -3.31 | 2.90 |
| 07.wav | Diptico | 112 | 24.000 | -3.200 | -18.07 | -3.20 | 2.90 |
| 08.wav | Cuello | 103 | 24.000 | -4.155 | -17.99 | -4.15 | 2.10 |
| 09.wav | Azul y crema | 105 | 24.000 | -3.200 | -18.19 | -3.20 | 4.40 |
| 10.wav | Referencias | 109 | 24.000 | -3.202 | -18.10 | -3.20 | 2.40 |

Mediciones realizadas sobre cada WAV exportado, con FFmpeg/loudnorm para LUFS-I y true peak, y muestras PCM para el pico dBFS. El generador verifica duración, frecuencia, canales, techo de picos y tolerancia de ±1 LU antes de escribir este informe.
