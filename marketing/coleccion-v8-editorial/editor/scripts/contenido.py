"""Shared layouts for carousels and motion graphics."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
P=dict(olive='#4F5533',dark='#30371F',paper='#F4F0E6',ink='#20251B',sage='#CBD0B2',sand='#C4AB79')
def t(s,x,y,z,c=None,serif=True,italic=False,lh=1.05,weight=500,tracking=0):return dict(type='text',text=s,x=x,y=y,size=z,color=c or P['ink'],serif=serif,italic=italic,lh=lh,weight=weight,tracking=tracking)
def p(s,x,y,w,h,fit='slice',crop=None):return dict(type='photo',src=s,x=x,y=y,w=w,h=h,fit=fit,crop=crop)
def line(x,y,w,c=None):return dict(type='rect',x=x,y=y,w=w,h=1.5,color=c or P['olive'])
def logo(x,y,s):return dict(type='logo',x=x,y=y,w=s,h=s)
def page(id,bg,nodes,n,theme):
 c=P['paper'] if bg in (P['dark'],P['olive']) else P['olive']
 return dict(id=id,bg=bg,width=1080,height=1350,nodes=[t('ÍNDIGO PY',72,62,24,c,False,weight=700,tracking=3),t(theme.upper(),480,65,19,c,False,tracking=1.6),*nodes,line(72,1260,936,c),t('@indigopy_',72,1281,21,c,False),t(f'{n:02} / 05',907,1281,21,c,False)])
N=[
page('neutros-01',P['dark'],[t('Neutros',66,180,211,P['paper']),t('CON PRESENCIA',78,399,27,P['sage'],False,tracking=5),p('conjunto-marron.jpg',454,480,554,739),t('Beige.\nMarrón.\nNegro.',72,665,68,P['paper'],italic=True,lh=1.12),logo(72,1100,100)],1,'Estudio de looks'),
page('neutros-02',P['paper'],[p('sastrero.jpg',72,160,515,1015,'meet'),t('El punto\nde partida.',625,300,69,lh=1.02),t('Un sastrero\nen tono neutro.',625,600,32,serif=False,lh=1.3),line(625,810,383),t('01',625,865,135,P['olive'])],2,'La prenda'),
page('neutros-03',P['dark'],[p('conjunto-marron.jpg',320,105,688,918),t('Un tono,\nconjunto completo.',72,1050,82,P['paper'],lh=1.04),t('02',72,290,136,P['sage'])],3,'El look'),
page('neutros-04',P['paper'],[t('Beige arriba.\nNegro abajo.',72,127,76,lh=.98),p('conjunto-beige.jpg',72,335,600,800),t('+',749,455,175,P['olive']),t('Dos tonos.\nUn look.',730,807,46,lh=1.15)],4,'El contraste'),
page('neutros-05',P['olive'],[logo(892,130,100),t('¿Cuál va\ncon vos?',72,229,139,P['paper'],lh=.98),p('sastrero.jpg',72,700,270,360,'meet'),p('conjunto-marron.jpg',405,700,270,360),p('conjunto-beige.jpg',738,700,270,360),t('Mandanos tu referencia favorita.',72,1147,44,P['paper'],False,weight=700)],5,'Seguimos conversando')]
guide=[dict(type='path',d='M 240 560 L 490 560 L 540 1050 L 430 1050 L 365 750 L 300 1050 L 190 1050 Z',color=P['olive'],stroke=3),line(180,575,410,P['sand']),line(180,675,410,P['sand']),dict(type='path',d='M 555 575 V 1050 M 545 575 H 565 M 545 1050 H 565',color=P['olive'],stroke=2),t('Cintura',650,554,49),t('Cadera',650,665,49),t('Largo',650,920,49)]
B=[
page('pantalones-01',P['paper'],[t('Dos pantalones.\nDos lecturas.',72,190,111,lh=.97),p('sastrero.jpg',72,540,441,585,'meet'),p('jean-detalle.jpg',567,540,441,585),t('SASTRERO',72,1160,26,serif=False,tracking=2),t('JEAN',567,1160,26,serif=False,tracking=2)],1,'Cuaderno de prendas'),
page('pantalones-02',P['dark'],[t('Primero,\nla cintura.',72,175,120,P['paper'],lh=.98),p('sastrero.jpg',72,500,936,590,crop=[230,125,920,580]),t('Una mirada al diseño del sastrero.',72,1164,32,P['paper'],False)],2,'Sastrero'),
page('pantalones-03',P['paper'],[p('jean-detalle.jpg',350,145,658,900),t('El bolsillo.\nLa costura.\nEl lavado.',72,1019,69,lh=1.02),t('02',72,250,140,P['olive'])],3,'Jean'),
page('pantalones-04',P['paper'],[t('Antes de elegir,\npedí las medidas.',72,175,92,lh=1.03),*guide,t('Guía para consultar.',72,1148,28,serif=False)],4,'La consulta'),
page('pantalones-05',P['dark'],[t('¿Sastrero\no jean?',72,177,145,P['paper'],lh=.97),p('sastrero.jpg',72,655,441,410,'meet'),p('jean-detalle.jpg',567,655,441,410),t('Consultanos por el modelo\nque te gustó.',72,1137,42,P['paper'],False,weight=700,lh=1.1),logo(892,155,100)],5,'Tu próxima elección')]
def scene(id,bg,nodes,d):
 c=P['paper'] if bg in (P['dark'],P['olive']) else P['olive']
 return dict(id=id,bg=bg,width=1080,height=1920,duration=d,nodes=[t('ÍNDIGO PY',72,166,27,c,False,weight=700,tracking=3),*nodes,t('@indigopy_',72,1570,27,c,False),line(72,1530,936,c)])
A=[
scene('14-gancho',P['dark'],[t('Neutros',66,315,210,P['paper']),t('CON PRESENCIA',78,548,30,P['sage'],False,tracking=5),p('conjunto-marron.jpg',380,660,628,837),t('Beige.\nMarrón.\nNegro.',72,910,63,P['paper'],italic=True,lh=1.1)],3),
scene('14-prenda',P['paper'],[p('sastrero.jpg',72,290,565,1190,'meet'),t('Una\nprenda.',680,460,89,lh=.98),t('El tono\nneutro.',680,950,55,italic=True,lh=1.1)],4.5),
scene('14-look',P['dark'],[p('conjunto-marron.jpg',300,280,708,944),t('Un tono.\nEl look completo.',72,1285,85,P['paper'],lh=1.02)],4.5),
scene('14-contraste',P['paper'],[t('Beige arriba.\nNegro abajo.',72,295,104,lh=.98),p('conjunto-beige.jpg',72,650,600,800),t('+',756,830,150,P['olive']),t('El\ncontraste.',720,1190,57,lh=1.1)],4.5),
scene('14-cierre',P['olive'],[logo(72,280,150),t('¿Cuál va\ncon vos?',72,530,156,P['paper'],lh=.98),p('sastrero.jpg',72,990,270,360,'meet'),p('conjunto-marron.jpg',405,990,270,360),p('conjunto-beige.jpg',738,990,270,360),t('Mandanos tu\nreferencia favorita.',72,1390,52,P['paper'],False,weight=700,lh=1.05)],5.5)]
g2=[]
for e in guide:
 n=dict(e)
 if n['type']=='path':n['d']='M 240 700 L 490 700 L 540 1190 L 430 1190 L 365 890 L 300 1190 L 190 1190 Z' if n['d'].startswith('M 240') else 'M 555 715 V 1190 M 545 715 H 565 M 545 1190 H 565'
 else:n['y']+=140
 g2.append(n)
C=[
scene('15-gancho',P['paper'],[t('Dos pantalones.\nDos lecturas.',72,315,116,lh=.97),p('sastrero.jpg',72,720,441,620,'meet'),p('jean-detalle.jpg',567,720,441,620),t('SASTRERO',72,1400,28,serif=False,tracking=2),t('JEAN',567,1400,28,serif=False,tracking=2)],3),
scene('15-cintura',P['dark'],[t('Primero,\nla cintura.',72,320,144,P['paper'],lh=.98),p('sastrero.jpg',72,780,936,595,crop=[230,125,920,580]),t('Una mirada al sastrero.',72,1420,34,P['paper'],False)],4.5),
scene('15-denim',P['paper'],[p('jean-detalle.jpg',350,280,658,920),t('El bolsillo.\nLa costura.\nEl lavado.',72,1250,74,lh=1.02),t('JEAN',72,510,28,serif=False,tracking=3)],4.5),
scene('15-medidas',P['paper'],[t('Antes de elegir,\npedí las medidas.',72,300,92,lh=1.03),*g2,t('Cintura · cadera · largo',72,1390,34,serif=False)],5),
scene('15-cierre',P['dark'],[logo(72,280,150),t('¿Sastrero\no jean?',72,530,160,P['paper'],lh=.97),p('sastrero.jpg',72,1000,441,305,'meet'),p('jean-detalle.jpg',567,1000,441,305),t('Consultanos por el modelo\nque te gustó.',72,1390,49,P['paper'],False,weight=700,lh=1.1)],5)]
data=dict(palette=P,posts=N+B,reels=[dict(id='14-Neutros',scenes=A,audio='03.wav'),dict(id='15-Pantalones',scenes=C,audio='07.wav')])
for r in data['reels']:r['duration']=sum(s['duration'] for s in r['scenes'])
assert len(data['posts'])==10 and len(data['reels'])==2
(root/'editor/src/contenido.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('10 placas y 2 guiones visuales generados.')
