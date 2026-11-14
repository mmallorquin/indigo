import numpy as np, wave
sr=44100; dur=24; out=np.zeros(int(sr*dur),dtype=np.float64); rng=np.random.default_rng(27)
def add(start, signal, gain=1):
    i=int(start*sr); n=min(len(signal),len(out)-i)
    if n>0: out[i:i+n]+=gain*signal[:n]
def tone(freq, seconds):
    t=np.arange(int(seconds*sr))/sr
    return (np.sin(2*np.pi*freq*t)+.17*np.sin(4*np.pi*freq*t))*np.exp(-t*3.7)*np.minimum(t/.012,1)
def hz(note): return 440*2**((note-69)/12)
chords=[[57,60,64,67],[53,57,60,64],[48,52,55,59],[55,59,62,64]]
beat=.625
for b in range(39):
    at=b*beat
    if at>=dur: break
    chord=chords[(b//4)%4]
    add(at,tone(hz(chord[b%4]+12),.8),.10)
    if b%4==0:
        for note in chord: add(at,tone(hz(note),2.0),.06)
        add(at,tone(hz(chord[0]-12),.9),.16)
    if b%2==0:
        t=np.arange(int(.17*sr))/sr
        kick=np.sin(2*np.pi*(48*t+2.5*(1-np.exp(-t*30))))*np.exp(-t*27)
        add(at,kick,.09)
    for sub in [0,.5]:
        t=np.arange(int(.045*sr))/sr
        noise=rng.normal(size=len(t))
        noise=np.r_[0,np.diff(noise)]*np.exp(-t*95)
        add(at+sub*beat,noise,.018)
t=np.arange(len(out))/sr
out*=np.minimum(t/.3,1)*np.minimum((dur-t)/1.5,1)
out=np.tanh(out*1.5)
out*=.72/max(np.max(np.abs(out)),.01)
stereo=np.column_stack([out,out*.97]).astype(np.float64)
with wave.open('/home/user/indigo/instrumental-original.wav','wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(sr); f.writeframes((stereo*32767).astype('<i2').tobytes())

