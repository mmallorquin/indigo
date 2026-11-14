from pathlib import Path
import json,zipfile,hashlib
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[2]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('href','src','poster') and v and not v.startswith(('https://','http://','#')):self.links.append(v)
x=Links();x.feed((ROOT/'index.html').read_text())
for l in x.links:assert (ROOT/l).is_file(),l
for m in json.loads((ROOT/'recursos-utilizados.json').read_text()):assert hashlib.sha256((ROOT/m['path']).read_bytes()).hexdigest()==m['sha256'],m['path']
for m in json.loads((ROOT/'datos-tecnicos.json').read_text()):assert hashlib.sha256((ROOT/'finales'/m['archivo']).read_bytes()).hexdigest()==m['sha256'],m['archivo']
files=[]
for d in ['finales','portadas','captions','licencia']:
 files+=list((ROOT/d).rglob('*'))
for d in ['src','public','scripts']:
 files+=list((ROOT/'editor'/d).rglob('*'))
for n in ['package.json','package-lock.json','tsconfig.json','remotion.config.ts','eslint.config.mjs','README.md','.gitignore','.prettierrc']:files.append(ROOT/'editor'/n)
files+=list(ROOT.glob('*.md'))+list(ROOT.glob('*.json'))+list(ROOT.glob('*.csv'))+[ROOT/'index.html']
files+=list((ROOT/'qa').glob('*-completo.jpg'))
files+=list((ROOT/'work/originales').rglob('*'))+list((ROOT/'work/brand').glob('*'))
files+=list((ROOT/'work/fuentes-nuevas-ui').glob('*.webp'))+list((ROOT/'work/fuentes-nuevas-ui').glob('*cover-frame-original.jpg'))+[ROOT/'work/fuentes-nuevas-ui/provenance-ui.json']
for n in ['09','17','19','22']:files+=list((ROOT/'work/fuentes-nuevas').glob('ig-'+n+'-*.jpg'))
files.append(ROOT/'work/fuentes-nuevas/provenance.json')
files=sorted(set(p for p in files if p.is_file()))
manifest=[dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
(ROOT/'MANIFIESTO-PAQUETE.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
files.append(ROOT/'MANIFIESTO-PAQUETE.json')
z=ROOT/'INDIGO-PY-10-VIDEOS-OLIVO.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=4) as archive:
 for p in files:archive.write(p,'INDIGO-PY-OLIVO/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(z) as archive:
 assert archive.testzip() is None
 names=archive.namelist()
 assert len([n for n in names if n.startswith('INDIGO-PY-OLIVO/finales/') and n.endswith('.mp4')])==10
 assert len([n for n in names if n.startswith('INDIGO-PY-OLIVO/portadas/') and n.endswith('.jpg')])==10
print(f'ZIP verificado: {len(files)} archivos, {z.stat().st_size/1024/1024:.1f} MiB. {len(x.links)} enlaces locales comprobados.')
