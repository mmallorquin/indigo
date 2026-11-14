"""Produce native-text PDFs for Canva and self-contained editable SVG layouts."""
from pathlib import Path
import sys,json,base64,html,re
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'work/python'))
from fontTools.ttLib import TTFont as ConvertFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from PIL import Image
data=json.loads((root/'editor/src/contenido.json').read_text())
fonts=root/'editor/public/fonts'
for w in (500,700):
 p=fonts/f'inter-{w}.ttf'
 if not p.exists():
  f=ConvertFont(fonts/f'inter-{w}.woff2');f.flavor=None;f.save(p)
for name,file in [('Inter','inter-500.ttf'),('InterBold','inter-700.ttf'),('Cormorant','cormorant-normal.ttf'),('CormorantItalic','cormorant-italic.ttf')]:pdfmetrics.registerFont(TTFont(name,str(fonts/file)))

def src(n):return root/'editor/public'/('brand/logo.jpg' if n['type']=='logo' else 'media/'+n['src'])
def font(n):return 'CormorantItalic' if n.get('italic') else 'Cormorant' if n.get('serif') else 'InterBold' if n.get('weight')==700 else 'Inter'
def draw(c,p):
 H=p['height'];c.setFillColor(HexColor(p['bg']));c.rect(0,0,1080,H,fill=1,stroke=0)
 for n in p['nodes']:
  typ=n['type']
  if typ=='text':
   for k,line in enumerate(n['text'].split('\n')):
    assert n['x']+pdfmetrics.stringWidth(line,font(n),n['size'])+max(0,len(line)-1)*n.get('tracking',0)<1080,(p['id'],line)
    t=c.beginText(n['x'],H-n['y']-k*n['size']*n['lh']-n['size']*.78);t.setFont(font(n),n['size']);t.setFillColor(HexColor(n['color']));t.setCharSpace(n.get('tracking',0));t.textOut(line);c.drawText(t)
  elif typ in ('photo','logo'):
   c.saveState();path=c.beginPath()
   if typ=='logo':path.circle(n['x']+n['w']/2,H-n['y']-n['h']/2,n['w']/2)
   else:path.rect(n['x'],H-n['y']-n['h'],n['w'],n['h'])
   c.clipPath(path,stroke=0,fill=0);im=src(n);iw,ih=Image.open(im).size
   if n.get('crop'):
    x,y,w,h=n['crop'];s=max(n['w']/w,n['h']/h);dx=n['x']-x*s;dy=H-n['y']+y*s-1920*s;w=1440*s;h=1920*s
   else:
    s=(min if n.get('fit')=='meet' else max)(n['w']/iw,n['h']/ih);w=iw*s;h=ih*s;dx=n['x']+(n['w']-w)/2;dy=H-n['y']-n['h']+(n['h']-h)/2
   c.drawImage(str(im),dx,dy,w,h,mask='auto');c.restoreState()
  elif typ=='rect':c.setFillColor(HexColor(n['color']));c.rect(n['x'],H-n['y']-n['h'],n['w'],n['h'],fill=1,stroke=0)
  elif typ=='path':
   path=c.beginPath();tokens=re.findall(r'[MLHVZ]|-?\d+(?:\.\d+)?',n['d']);i=0;x=y=0
   while i<len(tokens):
    cmd=tokens[i];i+=1
    if cmd in ('M','L'):x=float(tokens[i]);y=float(tokens[i+1]);i+=2;(path.moveTo if cmd=='M' else path.lineTo)(x,H-y)
    elif cmd=='H':x=float(tokens[i]);i+=1;path.lineTo(x,H-y)
    elif cmd=='V':y=float(tokens[i]);i+=1;path.lineTo(x,H-y)
    elif cmd=='Z':path.close()
   c.setStrokeColor(HexColor(n['color']));c.setLineWidth(n['stroke']);c.drawPath(path,fill=0,stroke=1)

def svg(p):
 out=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1080" height="1350" viewBox="0 0 1080 1350"><title>{p["id"]}</title><rect width="1080" height="1350" fill="{p["bg"]}"/>']
 for i,n in enumerate(p['nodes']):
  typ=n['type']
  if typ=='text':
   family='Cormorant Garamond' if n['serif'] else 'Inter'
   for k,l in enumerate(n['text'].split('\n')):out.append(f'<text x="{n["x"]}" y="{n["y"]+k*n["size"]*n["lh"]+n["size"]*.78}" font-family="{family}" font-weight="{600 if n["serif"] else n["weight"]}" font-style="{"italic" if n["italic"] else "normal"}" font-size="{n["size"]}" fill="{n["color"]}" letter-spacing="{n["tracking"]}">{html.escape(l)}</text>')
  elif typ in ('photo','logo'):
   im='data:image/jpeg;base64,'+base64.b64encode(src(n).read_bytes()).decode();crop=n.get('crop');vb=' '.join(map(str,crop)) if crop else f'0 0 {n["w"]} {n["h"]}';iw=1440 if crop else n['w'];ih=1920 if crop else n['h']
   if typ=='logo':out.append(f'<defs><clipPath id="logo{i}"><circle cx="{n["x"]+n["w"]/2}" cy="{n["y"]+n["h"]/2}" r="{n["w"]/2}"/></clipPath></defs><g clip-path="url(#logo{i})">')
   out.append(f'<svg x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" viewBox="{vb}" overflow="hidden" preserveAspectRatio="{"xMidYMid slice" if crop else "none"}"><image xlink:href="{im}" width="{iw}" height="{ih}" preserveAspectRatio="xMidYMid {n.get("fit","slice")}"/></svg>')
   if typ=='logo':out.append('</g>')
  elif typ=='rect':out.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" fill="{n["color"]}"/>')
  elif typ=='path':out.append(f'<path d="{n["d"]}" fill="none" stroke="{n["color"]}" stroke-width="{n["stroke"]}"/>')
 return ''.join(out)+'</svg>'

for theme,posts in [('neutros',data['posts'][:5]),('pantalones',data['posts'][5:])]:
 c=canvas.Canvas(str(root/f'editables/{theme}-canva.pdf'),pagesize=(1080,1350));c.setTitle('Índigo / '+theme)
 for post in posts:
  draw(c,post);c.showPage();(root/'editables/svg'/(post['id']+'.svg')).write_text(svg(post))
 c.save()
print('2 PDF de cinco páginas con texto nativo y 10 SVG con imágenes incorporadas.')
