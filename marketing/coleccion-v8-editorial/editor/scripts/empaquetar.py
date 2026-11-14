from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,zipfile
from PIL import Image
from pypdf import PdfReader
r=Path(__file__).resolve().parents[2]
archive=r/'INDIGO-ESTUDIOS-DE-PRENDAS.zip'
posts=list((r/'carruseles').rglob('*.png'));reels=list((r/'reels').glob('*.mp4'))
assert len(posts)==10 and len(reels)==2
for p in posts:assert Image.open(p).size==(1080,1350)
assert len(list((r/'editables/svg').glob('*.svg')))==10
for p in (r/'editables').glob('*.pdf'):assert len(PdfReader(p).pages)==5
for x in json.loads((r/'datos-tecnicos.json').read_text()):
 assert x['decode_ok'] and not x['black_segments'] and x['duracion_video_s']==22
 assert x['faststart'] and float(x['audio']['input_tp'])<=-1.5
 assert abs(float(x['audio']['input_i'])+14)<.6
def include(p):
 rel=p.relative_to(r)
 if any(x in ('work','node_modules','.git','__pycache__') for x in rel.parts):return False
 if p.name in ('MANIFIESTO.json','PAQUETE-VERIFICADO.json','.DS_Store') or p.suffix=='.zip':return False
 if str(rel) in ('editor/src/Design.tsx','editor/public/media/azul-crema.jpg','editor/public/media/basica-beige.jpg'):return False
 if rel.parts[0]=='qa':return p.name.endswith(('-40-fotogramas.jpg','-master.json','-contacto.jpg')) and not p.name.startswith(('canva-contacto','figma-contacto','pdf-contacto'))
 return True
files=sorted(p for p in r.rglob('*') if p.is_file() and include(p))
manifest=[dict(path=str(p.relative_to(r)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
(r/'MANIFIESTO.json').write_text(json.dumps(manifest,indent=2))
files.append(r/'MANIFIESTO.json')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,p.relative_to(r))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for m in manifest:assert hashlib.sha256(z.read(m['path'])).hexdigest()==m['sha256']
class Links(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,tag,attrs):self.urls.extend(v for k,v in attrs if k in ('href','src','poster') and v and not urlsplit(v).scheme)
p=Links();p.feed((r/'index.html').read_text())
for target in p.urls:assert (r/unquote(urlsplit(target).path)).is_file(),target
result=dict(files=len(files),mp4=2,png=10,svg=10,pdf=2,crc='OK',sha256='OK',local_links=len(p.urls),archive_bytes=archive.stat().st_size)
(r/'PAQUETE-VERIFICADO.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
