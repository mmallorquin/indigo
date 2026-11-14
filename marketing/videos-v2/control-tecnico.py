from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess,json
root=Path('/home/user/indigo-v2')
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
probes={}
for name in ['looks','consulta','looks-sin-musica','consulta-sin-musica']:
 p=root/(name+'.mp4')
 probes[name]=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,r_frame_rate,nb_frames,bit_rate,sample_rate,channels,duration:format=duration,size,bit_rate','-of','json',str(p)]))
 subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
 if '-sin-musica' in name: continue
 d=root/('qa-'+name);d.mkdir(exist_ok=True)
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(p),'-vf','fps=2,scale=162:288',str(d/'%02d.jpg')],check=True)
 sheet=Image.new('RGB',(1296,1872),'#F7F4EC');draw=ImageDraw.Draw(sheet)
 for k,path in enumerate(sorted(d.glob('*.jpg'))):
  x=(k%8)*162;y=(k//8)*312
  sheet.paste(Image.open(path),(x,y+24));draw.text((x+7,y+2),f'{k/2:.1f}s',font=f,fill='#475139')
 sheet.save(root/(name+'-qa.jpg'),quality=82)
(root/'datos-tecnicos.json').write_text(json.dumps(probes,indent=2))
print(json.dumps(probes,indent=2))

