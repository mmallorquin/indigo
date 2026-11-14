from pathlib import Path
import subprocess,json,re,hashlib,math,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
qa=ROOT/'qa';qa.mkdir(exist_ok=True)
wanted=sys.argv[1:]
previous=json.loads((ROOT/'datos-tecnicos.json').read_text()) if wanted and (ROOT/'datos-tecnicos.json').exists() else []
reports=[r for r in previous if not any(r['archivo'].startswith(n) for n in wanted)]
for f in sorted((ROOT/'finales').glob('*.mp4')):
 if wanted and not any(f.name.startswith(n) for n in wanted):continue
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]))
 v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio');dur=float(meta['format']['duration'])
 decode=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(f),'-f','null','-'],capture_output=True,text=True)
 black=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vf','blackdetect=d=0.05:pix_th=0.025:pic_th=0.98','-an','-f','null','-'],capture_output=True,text=True)
 audio=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-af','loudnorm=I=-18:TP=-3:LRA=7:print_format=json','-vn','-f','null','-'],capture_output=True,text=True)
 m=re.search(r'\{\s*"input_i".*?\}',audio.stderr,re.S);am=json.loads(m.group(0)) if m else {}
 samples=qa/(f.stem+'-frames');samples.mkdir(exist_ok=True)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(f),'-vf','fps=1,scale=270:480,format=yuvj420p','-q:v','2',str(samples/'%03d.jpg')],check=True)
 last=samples/'ultimo.jpg';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(f),'-frames:v','1','-vf',f"select='eq(n,{int(v['nb_frames'])-1})',scale=270:480,format=yuvj420p",'-q:v','2',str(last)],check=True)
 first=samples/'cero.jpg';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(f),'-frames:v','1','-vf','scale=270:480,format=yuvj420p','-q:v','2',str(first)],check=True)
 fs=[first]+sorted(samples.glob('[0-9]*.jpg'))+[last];cols=5;rows=math.ceil(len(fs)/cols);sheet=Image.new('RGB',(cols*270,rows*505),'#F4F0E6');d=ImageDraw.Draw(sheet)
 for i,p in enumerate(fs):
  x=(i%cols)*270;y=(i//cols)*505;sheet.paste(Image.open(p),(x,y+25));d.text((x+6,y+6),('Ultimo fotograma' if p==last else ('0 s' if p==first else f'{i-0.5:.1f} s')),fill='#20251B')
 sheet.save(qa/(f.stem+'-completo.jpg'),quality=94)
 report=dict(archivo=f.name,duracion_s=dur,ancho=v['width'],alto=v['height'],fps=v['avg_frame_rate'],frames=v.get('nb_frames'),codec=v['codec_name'],pix_fmt=v['pix_fmt'],audio_codec=a['codec_name'],audio_hz=a['sample_rate'],audio_canales=a['channels'],bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),decode_correcto=decode.returncode==0 and not decode.stderr,fotogramas_negros=re.findall(r'black_start:[^\r\n]+',black.stderr),audio_medicion=am)
 assert (v['width'],v['height'])==(1080,1920) and v['avg_frame_rate']=='30/1'
 assert report['decode_correcto'] and not report['fotogramas_negros']
 assert a['codec_name']=='aac' and a['channels']==2 and float(am['input_tp'])<0
 reports.append(report);print(f.name, 'OK',dur,'s',am.get('input_i'),'LUFS',am.get('input_tp'),'dBTP',flush=True)
reports.sort(key=lambda r:r['archivo'])
(ROOT/'datos-tecnicos.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
assert len(reports)==10
print('Diez exports: decodificación completa y control técnico aprobados.',flush=True)
