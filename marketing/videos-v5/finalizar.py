from pathlib import Path
import subprocess
r=Path(__file__).resolve().parent
for n in ['lanzamiento-negro','lanzamiento-blanco']:
 subprocess.run(['ffmpeg','-v','error','-i',str(r/(n+'-sin-musica.mp4')),'-i',str(r/(n+'-musica.wav')),
  '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',
  '-af','loudnorm=I=-16:TP=-3:LRA=9','-t','20','-movflags','+faststart','-y',str(r/(n+'.mp4'))],check=True)
