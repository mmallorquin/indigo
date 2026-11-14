"""Pulsos, bajos, impactos y barridos sintetizados; sin muestras externas."""
from pathlib import Path
import numpy as np, json, wave, subprocess

r=Path(__file__).resolve().parent
sr=48000; seconds=20; grid=json.loads((r/'beats.json').read_text())
for name in ['lanzamiento-negro','lanzamiento-blanco']:
 dark=name.endswith('negro'); rng=np.random.default_rng(508 if dark else 509)
 out=np.zeros(seconds*sr)
 def add(at,signal,gain):
  start=round(at*sr);n=min(len(signal),len(out)-start)
  if n>0:out[start:start+n]+=signal[:n]*gain
 def sine(note,dur):
  t=np.arange(round(dur*sr))/sr;f=440*2**((note-69)/12)
  return t,np.sin(2*np.pi*f*t)
 # Base de pulso y bajo: oscuro más grave, claro más abierto.
 for beat in range(40):
  at=beat*.5; t=np.arange(round(.35*sr))/sr
  kick=np.sin(2*np.pi*(45*t+2.5*(1-np.exp(-30*t))))*np.exp(-18*t)
  add(at,kick,.32 if dark else .21)
  note=([33,33,36,31] if dark else [45,48,43,48])[(beat//4)%4]
  t,s=sine(note,.44)
  add(at,s*np.minimum(t/.012,1)*np.exp(-5*t),.19 if dark else .12)
  if beat%2==1:
   t=np.arange(round(.15*sr))/sr
   snap=rng.normal(size=len(t));snap=np.r_[0,np.diff(snap)]*np.exp(-45*t)
   add(at,snap,.031 if dark else .023)
  for off in ([.25] if dark else [0,.25]):
   t=np.arange(round(.045*sr))/sr
   hi=np.r_[0,np.diff(rng.normal(size=len(t)))]*np.exp(-110*t)
   add(at+off,hi,.012)
  if not dark:
   t,s=sine([69,72,67,72][beat%4],.38)
   add(at+.25,s*np.minimum(t/.008,1)*np.exp(-9*t),.044)
 # Cama amplia y suave, sin melodía de terceros.
 for at in range(0,20,4):
  chord=[45,52,57] if dark else [57,60,64]
  t=np.arange(round(3.8*sr))/sr
  pad=sum(sine(n,3.8)[1] for n in chord)/3
  add(at,pad*np.minimum(t/.15,1)*np.minimum((3.8-t)/.5,1),.065)
 cues=grid['negro_cues' if dark else 'blanco_cues']
 for at in cues:
  t=np.arange(round(.32*sr))/sr
  impact=np.sin(2*np.pi*(36*t+1.5*(1-np.exp(-25*t))))*np.exp(-12*t)
  add(at,impact,.18)
  if at>.4:
   t=np.arange(round(.28*sr))/sr
   sweep=np.r_[0,np.diff(rng.normal(size=len(t)))]
   add(at-.28,sweep*np.sin(np.pi*t/.28)**2,.025 if dark else .018)
 t=np.arange(len(out))/sr
 out=np.tanh(out*1.5)*np.minimum(t/.02,1)*np.minimum((seconds-t)/.7,1)
 out*=.77/max(np.max(np.abs(out)),.01)
 with wave.open(str(r/(name+'-musica.wav')),'wb') as f:
  f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr)
  f.writeframes((np.column_stack([out,out*.98])*32767).astype('<i2').tobytes())

