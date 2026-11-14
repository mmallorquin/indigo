from pathlib import Path
import json, zipfile, hashlib
r=Path(__file__).resolve().parent
out=r/'INDIGO-V5-LANZAMIENTO-COMPLETO.zip'
project_data={}; allowed={}
for name in ['lanzamiento-negro','lanzamiento-blanco']:
 j=json.loads((r/name/'project.json').read_text());scene=json.dumps(j['scenes'])
 j['assets']=[a for a in j['assets'] if a['kind']=='font' or a['id'] in scene]
 project_data[name]=j
 allowed[name]={a['uri'][3:] for a in j['assets'] if a['uri'].startswith('fs:')}
 for uri in allowed[name]: assert (r/name/uri).is_file(),uri
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for file in sorted(r.rglob('*')):
  if not file.is_file():continue
  rel=file.relative_to(r);parts=rel.parts
  if file==out or file.suffix=='.zip' or any(p.startswith('qa-') or p in ['__pycache__','.git','.bg','renders'] for p in parts):continue
  if file.name in ['paquete-integridad.json','control-resumen.json','prueba-lanzamiento.mp4','lectura-mira.png','lectura-corregida.jpg','revision-diseno.jpg','revision-diseno-v2.jpg']:continue
  if parts[0] in project_data:
   if len(parts)>1 and parts[1] in ['media','fonts'] and str(Path(*parts[1:])) not in allowed[parts[0]]:continue
   if file.name=='edit.js':continue
   if file.name=='project.json':
    z.writestr('videos-v5/'+str(rel),json.dumps(project_data[parts[0]],indent=2));continue
  z.write(file,'videos-v5/'+str(rel))
with zipfile.ZipFile(out) as z: assert z.testzip() is None
print(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
