from pathlib import Path
import subprocess, json, hashlib
from PIL import Image, ImageDraw

r=Path(__file__).resolve().parent
names=['lanzamiento-negro','lanzamiento-blanco']
data={'videos':{},'hashes_video':{},'fuentes':{}}
for base in names:
 for suffix in ['', '-sin-musica']:
  n=base+suffix;file=r/(n+'.mp4')
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
   'stream=codec_name,width,height,r_frame_rate,nb_frames,bit_rate,sample_rate,channels,duration:format=duration,size,bit_rate','-of','json',str(file)]))
  video=next(s for s in probe['streams'] if s['codec_name']=='h264')
  assert video['width']==1080 and video['height']==1920
  assert video['r_frame_rate']=='30/1' and int(video['nb_frames'])==600
  assert abs(float(probe['format']['duration'])-20)<.05
  audio=[s for s in probe['streams'] if s['codec_name']=='aac']
  assert bool(audio)==(suffix=='')
  if audio: assert audio[0]['channels']==2 and audio[0]['sample_rate']=='48000'
  subprocess.run(['ffmpeg','-v','error','-i',str(file),'-f','null','-'],check=True)
  data['videos'][n]=probe
  data['hashes_video'][n]=subprocess.check_output(['ffmpeg','-v','error','-i',str(file),'-map','0:v:0',
    '-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
 assert data['hashes_video'][base]==data['hashes_video'][base+'-sin-musica']
 folder=r/('qa-'+base);folder.mkdir(exist_ok=True)
 subprocess.run(['ffmpeg','-v','error','-i',str(r/(base+'.mp4')),'-vf','fps=4,scale=144:256','-y',str(folder/'%03d.jpg')],check=True)
 frames=sorted(folder.glob('*.jpg'));assert len(frames)==80
 sheet=Image.new('RGB',(1152,2800),'#252525');d=ImageDraw.Draw(sheet)
 for i,file in enumerate(frames):
  x,y=i%8*144,i//8*280
  sheet.paste(Image.open(file),(x,y+24));d.text((x+4,y+4),f'{i/4:.2f}s',fill='white')
 sheet.save(r/(base+'-qa.jpg'),quality=74)
 for tag,time in [('portada',1.3),('producto',6.2),('look',9.1),('cierre',17.4)]:
  subprocess.run(['ffmpeg','-v','error','-i',str(r/(base+'.mp4')),'-ss',str(time),'-frames:v','1',
   '-vf','scale=360:640','-y',str(r/(base+'-final-'+tag+'.jpg'))],check=True)
 with open(r/(base+'-audio-control.txt'),'w') as f:
  subprocess.run(['ffmpeg','-v','info','-i',str(r/(base+'.mp4')),'-af',
   'loudnorm=I=-16:TP=-3:LRA=9:print_format=json','-f','null','-'],stderr=f,check=True)
 for tag in ['portada','producto','look','cierre']:
  Image.open(r/(base+'-'+tag+'.png')).convert('RGB').save(r/(base+'-'+tag+'.jpg'),quality=95)
for file in sorted((r/'fuentes').glob('*.mp4')):
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
  'stream=codec_name,width,height,r_frame_rate:format=duration,size','-of','json',str(file)]))
 data['fuentes'][file.name]={'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'probe':probe}
(r/'datos-tecnicos.json').write_text(json.dumps(data,indent=2))
print(json.dumps(data['videos'],indent=2))
