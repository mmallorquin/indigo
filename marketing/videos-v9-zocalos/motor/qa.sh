#!/bin/bash
# uso: qa.sh salida.jpg video1.mp4 ... (hasta 5 por hoja)
out=$1; shift; i=0; ins=""
for f in "$@"; do D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"); ffmpeg -v error -y -i "$f" -vf "fps=6/$D,scale=270:480,tile=6x1" -frames:v 1 /tmp/qa_row_$i.png; ins="$ins -i /tmp/qa_row_$i.png"; i=$((i+1)); done
ffmpeg -v error -y $ins -filter_complex "vstack=inputs=$i" -q:v 3 "$out"
