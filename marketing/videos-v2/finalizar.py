from pathlib import Path
import subprocess
root=Path('/home/user/indigo-v2')
for name in ['looks','consulta']:
 native=root/(name+'-composicion.mp4')
 master=root/(name+'-sin-musica.mp4')
 if not native.exists(): master.rename(native)
 # Preserve the native titles; decode the final real shot independently.
 filt='[0:v]split=3[v0][vh][vt];[v0]trim=end=18.2,setpts=PTS-STARTPTS[a];[vh]trim=start=18.2:end=20,setpts=PTS-STARTPTS,crop=1080:416:0:0[head];[1:v]scale=1080:1920,setpts=PTS-STARTPTS[real];[real][head]overlay=0:0:shortest=1,trim=duration=1.8,setpts=PTS-STARTPTS[b];[vt]trim=start=20:end=24,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[out]'
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(native),'-i',str(root/'clips/clip-25.5-1.8.mp4'),'-filter_complex',filt,'-map','[out]','-an','-c:v','libx264','-preset','fast','-b:v','10M','-pix_fmt','yuv420p','-r','30','-t','24','-movflags','+faststart',str(master)],check=True)
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(master),'-i',str(root/'instrumental-original.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-ar','48000','-b:a','192k','-af','loudnorm=I=-18:TP=-1.5:LRA=7','-movflags','+faststart','-shortest',str(root/(name+'.mp4'))],check=True)
print('Final exports completed')

