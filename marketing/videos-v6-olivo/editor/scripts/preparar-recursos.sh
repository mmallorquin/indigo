#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
ffmpeg -hide_banner -loglevel error -y -ss 1.0 -t 0.75 -i ../work/originales/IG04-looks-original.mp4 -vf 'crop=600:980:80:260,setpts=4*(PTS-STARTPTS),fps=30,tpad=stop_mode=clone:stop_duration=2.4' -an -c:v libx264 -crf 18 public/media/manga-verde.mp4
ffmpeg -hide_banner -loglevel error -y -ss 6.7 -t 2.1 -i ../work/originales/IG04-looks-original.mp4 -vf 'crop=600:980:80:260,setpts=2.4*(PTS-STARTPTS),fps=30' -an -c:v libx264 -crf 18 public/media/manga-lila.mp4
ffmpeg -hide_banner -loglevel error -y -i ../work/originales/IG06-jeans-original.mp4 -vf 'crop=720:1000:0:0' -an -c:v libx264 -crf 18 public/media/jean-percha.mp4
