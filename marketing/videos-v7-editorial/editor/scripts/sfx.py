from pathlib import Path
import numpy as np,wave
out=Path(__file__).resolve().parents[1]/'public/audio'
fs=48000
scenes={'11':(30.5,[3,4.5,9.5,14.5,19.5,25.5],[20.1,20.5,20.9]),'12':(30.5,[3,4.5,10,15.5,21,25.5],[21.4,22,22.7]),'13':(31.5,[3,4.5,10.5,16.5,22.5,26.5],[22.8,23.45,24.15])}
for n,(seconds,changes,ticks) in scenes.items():
 rng=np.random.default_rng(int(n)+320)
 audio=np.zeros((int(seconds*fs),2),dtype=np.float64)
 for cue in changes:
  t=np.arange(int(.24*fs))/fs
  raw=rng.normal(0,1,len(t));noise=np.convolve(raw,np.ones(30)/30,mode='same')
  pulse=noise*np.sin(np.pi*np.arange(len(t))/len(t))**2*.055
  i=int(cue*fs);audio[i:i+len(t),0]+=pulse;audio[i:i+len(t),1]+=pulse*.92
 for cue in ticks:
  t=np.arange(int(.11*fs))/fs
  pulse=np.sin(2*np.pi*(720-240*t)*t)*np.exp(-t*40)*np.minimum(1,t/.008)*.012
  i=int(cue*fs);audio[i:i+len(t),:]+=pulse[:,None]
 pcm=(np.clip(audio,-.99,.99)*32767).astype('<i2')
 with wave.open(str(out/f'sfx-{n}.wav'),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(fs);f.writeframes(pcm.tobytes())
 print(n,seconds,'s; peak',round(20*np.log10(np.max(np.abs(audio))),1),'dBFS')
