"""Fixed-page editable HTML import for Canva, preserving separate text blocks."""
from pathlib import Path
import json,html,base64,subprocess
r=Path(__file__).resolve().parents[2]
d=json.loads((r/'editor/src/contenido.json').read_text())
def uri(p,mime='image/jpeg'):return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
fonts=r/'editor/public/fonts'
css=''.join('@font-face{font-family:"'+family+'";src:url('+uri(fonts/file,mime)+');font-weight:'+weight+';font-style:'+style+'}' for family,file,mime,weight,style in [('Inter','inter-500.woff2','font/woff2','500','normal'),('Inter','inter-700.woff2','font/woff2','700','normal'),('Cormorant Garamond','cormorant-normal.ttf','font/ttf','600','normal'),('Cormorant Garamond','cormorant-italic.ttf','font/ttf','600','italic')])
for theme,posts in [('neutros',d['posts'][:5]),('pantalones',d['posts'][5:])]:
 pages=[]
 for p in posts:
  nodes=[]
  for n in p['nodes']:
   typ=n['type'];xy=f'position:absolute;left:{n.get("x",0)}px;top:{n.get("y",0)}px;'
   if typ=='text':
    style=xy+f'font-family:{"Cormorant Garamond" if n["serif"] else "Inter"};font-size:{n["size"]}px;font-weight:{600 if n["serif"] else n["weight"]};font-style:{"italic" if n["italic"] else "normal"};line-height:{n["lh"]};letter-spacing:{n["tracking"]}px;color:{n["color"]};white-space:pre;margin:0;'
    nodes.append('<div style="'+style+'">'+html.escape(n['text'])+'</div>')
   elif typ in ('photo','logo'):
    source=r/'editor/public'/('brand/logo.jpg' if typ=='logo' else 'media/'+n['src']);img=uri(source);size=f'width:{n["w"]}px;height:{n["h"]}px;'
    if n.get('crop'):
     x,y,w,h=n['crop'];cropfile=r/'editor/public/media/sastrero-cintura.jpg'
     if not cropfile.exists():subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',f'crop={w}:{h}:{x}:{y},scale=936:590','-frames:v','1','-q:v','2',str(cropfile)],check=True)
     nodes.append(f'<img src="{uri(cropfile)}" alt="Detalle real de la cintura del sastrero" style="{xy}{size}object-fit:cover">')
    else:nodes.append(f'<img src="{img}" alt="{html.escape(n.get("src","Logo oficial Índigo"))}" style="{xy}{size}object-fit:{"contain" if n.get("fit")=="meet" else "cover"};{"border-radius:50%;" if typ=="logo" else ""}">')
   elif typ=='rect':nodes.append(f'<div style="{xy}width:{n["w"]}px;height:{n["h"]}px;background:{n["color"]}"></div>')
   elif typ=='path':nodes.append(f'<svg width="1080" height="1350" viewBox="0 0 1080 1350" style="position:absolute;inset:0"><path d="{n["d"]}" fill="none" stroke="{n["color"]}" stroke-width="{n["stroke"]}"/></svg>')
  pages.append(f'<section data-document-role="page" data-label="{p["id"]}" style="position:relative;width:1080px;height:1350px;overflow:hidden;background:{p["bg"]}">'+''.join(nodes)+'</section>')
 (r/f'editables/{theme}-canva.html').write_text('<!doctype html><html lang="es-PY"><head><meta charset="utf-8"><style>'+css+'body{margin:0}*{box-sizing:border-box}img{display:block}</style></head><body>'+''.join(pages)+'</body></html>')
print('Dos HTML paginados, cinco placas cada uno, con todos los recursos incorporados.')
