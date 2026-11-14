from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
for name in ['looks', 'consulta']:
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(root / (name + '-sin-musica.mp4')),
                    '-i', str(root / (name + '-musica-original.wav')), '-map', '0:v:0', '-map', '1:a:0',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
                    '-af', 'loudnorm=I=-16:TP=-1.5:LRA=9', '-t', '20', '-movflags', '+faststart',
                    '-y', str(root / (name + '.mp4'))], check=True)

