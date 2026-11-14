from pathlib import Path
import subprocess,json,re,hashlib
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2]
reports=[]
for f in sorted((root/'finales').glob('*.mp4')):
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio');n=int(v['nb_frames']);d=n/30
 full=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(f),'-f','null','-'],capture_output=True,text=True)
 black=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vf','blackdetect=d=0.05:pix_th=0.025:pic_th=0.98','-an','-f','null','-'],capture_output=True,text=True)
 freeze=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vf','freezedetect=n=-60dB:d=0.3','-an','-f','null','-'],capture_output=True,text=True)
 audio=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-vn','-f','null','-'],capture_output=True,text=True);am=json.loads(re.search(r'\{\s*"input_i".*?\}',audio.stderr,re.S).group())
 hashes=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(f),'-an','-f','framemd5','-']).decode().splitlines();last=None;run=0;maxrun=0
 for l in hashes:
  if l.startswith('#') or not l.strip():continue
  h=l.split(',')[-1].strip();run=run+1 if h==last else 1;maxrun=max(maxrun,run);last=h
 folder=root/'qa'/(f.stem+'-frames');folder.mkdir(exist_ok=True)
 frames=[round(i*(n-1)/39) for i in range(40)]
 select='+'.join('eq(n\\,'+str(i)+')' for i in frames)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(f),'-vf','select='+select+',scale=225:400,format=yuvj420p','-fps_mode','vfr','-q:v','2',str(folder/'%03d.jpg')],check=True)
 fs=sorted(folder.glob('*.jpg'));assert len(fs)==40
 sheet=Image.new('RGB',(1800,2125),'#F4F0E6');draw=ImageDraw.Draw(sheet)
 for i,(p,frame) in enumerate(zip(fs,frames)):
  x=i%8*225;y=i//8*425;sheet.paste(Image.open(p),(x,y+25));draw.text((x+5,y+5),f'{frame/30:.2f} s',fill='#20251B')
 sheet.save(root/'qa'/(f.stem+'-40-fotogramas.jpg'),quality=95)
 atoms=[]
 with f.open('rb') as stream:
  while True:
   hdr=stream.read(8)
   if len(hdr)<8:break
   size=int.from_bytes(hdr[:4],'big');typ=hdr[4:].decode('ascii',errors='replace');extra=0
   if size==1:size=int.from_bytes(stream.read(8),'big');extra=8
   if size<8+extra:break
   atoms.append(typ);stream.seek(size-8-extra,1)
 report=dict(archivo=f.name,width=v['width'],height=v['height'],fps=v['avg_frame_rate'],frames=n,duracion_video_s=d,duracion_contenedor_s=float(meta['format']['duration']),codec=v['codec_name'],pixel_format=v['pix_fmt'],color_space=v.get('color_space'),color_primaries=v.get('color_primaries'),color_transfer=v.get('color_transfer'),audio_codec=a['codec_name'],audio_hz=a['sample_rate'],audio_channels=a['channels'],audio=am,decode_ok=full.returncode==0 and not full.stderr,black_segments=re.findall(r'black_start:[^\n]+',black.stderr),freeze_logs=[l for l in freeze.stderr.splitlines() if 'lavfi.freezedetect' in l],max_identical_frames=maxrun,max_identical_duration_s=maxrun/30,faststart=atoms.index('moov')<atoms.index('mdat'),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest())
 assert (v['width'],v['height'])==(1080,1920) and v['avg_frame_rate']=='30/1' and d<=35
 assert report['decode_ok'] and not report['black_segments'] and report['faststart']
 assert abs(float(am['input_i'])+14)<.6 and float(am['input_tp'])<=-1.5
 assert v.get('color_space')=='bt709' and a['codec_name']=='aac'
 reports.append(report);print(f.name, 'OK',d,'s',am['input_i'],'LUFS',am['input_tp'],'dBTP','freeze events',len(report['freeze_logs']),'repeat',maxrun,flush=True)
(root/'datos-tecnicos.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
assert len(reports)==3
