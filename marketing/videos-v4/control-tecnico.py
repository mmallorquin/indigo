from pathlib import Path
import subprocess
import json
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
probes, hashes = {}, {}
for name in ['editorial','energia','editorial-sin-musica','energia-sin-musica']:
    path = root/(name+'.mp4')
    probes[name] = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'stream=codec_name,width,height,r_frame_rate,nb_frames,bit_rate,sample_rate,channels,duration:format=duration,size,bit_rate',
        '-of','json',str(path)]))
    subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],check=True)
    hashes[name] = subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0',
        '-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
    if name.endswith('-sin-musica'):
        continue
    folder = root/('qa-'+name); folder.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vf','fps=4,scale=144:256',
        '-y',str(folder/'%03d.jpg')],check=True)
    sheet = Image.new('RGB',(1152,2800),'#171717'); draw = ImageDraw.Draw(sheet)
    for i,p in enumerate(sorted(folder.glob('*.jpg'))):
        x,y = (i%8)*144,(i//8)*280
        sheet.paste(Image.open(p),(x,y+24)); draw.text((x+5,y+5),f'{i/4:.2f}s',fill='white')
    sheet.save(root/(name+'-qa.jpg'),quality=76)
    with open(root/(name+'-audio-control.txt'),'w') as f:
        subprocess.run(['ffmpeg','-v','info','-i',str(path),'-af',
            'loudnorm=I=-16:TP=-2:LRA=9:print_format=json','-f','null','-'],stderr=f,check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(path),'-ss','17.4','-frames:v','1',
        '-vf','scale=360:640','-y',str(root/(name+'-final-cierre.jpg'))],check=True)
    for stem in ['portada','gancho','demostracion','cierre']:
        p=root/(name+'-'+stem+'.png')
        Image.open(p).convert('RGB').save(root/(name+'-'+stem+'.jpg'),quality=95)

for name in ['editorial','energia']:
    assert hashes[name] == hashes[name+'-sin-musica'], 'Cambió la imagen al mezclar audio'
(root/'datos-tecnicos.json').write_text(json.dumps({'videos':probes,'hashes_video':hashes},indent=2))
print(json.dumps(probes,indent=2))

