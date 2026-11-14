from pathlib import Path
import subprocess
root=Path('/home/user/indigo-v2/clips');root.mkdir(exist_ok=True)
cuts=[(10.7,3.5),(1,1.5),(4.15,1.45),(6,2.8),(14.2,3.35),(18,2),(21,3.6),(25.5,1.8),(10.7,6.85)]
for start,duration in cuts:
 p=root/('clip-'+str(start)+'-'+str(duration)+'.mp4')
 subprocess.run(['ffmpeg','-y','-v','error','-i','/home/user/indigo/source.mp4','-ss',str(start),'-t',str(duration),'-vf','setpts=PTS-STARTPTS','-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-g','1','-keyint_min','1','-bf','0','-r','30',str(p)],check=True)
print('Decoded clean clips ready')

