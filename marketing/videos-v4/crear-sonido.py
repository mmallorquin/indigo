"""Dos pistas sintetizadas sin muestras externas; pulso compartido a 120 BPM."""
from pathlib import Path
import json
import numpy as np
import wave

root = Path(__file__).resolve().parent
sr, duration = 48000, 20
grid = json.loads((root / 'beats.json').read_text())

def hz(note):
    return 440 * 2 ** ((note - 69) / 12)

for name in ['editorial', 'energia']:
    soft = name == 'editorial'
    rng = np.random.default_rng(404 if soft else 405)
    out = np.zeros(sr * duration)
    def add(at, signal, gain=1):
        i = round(at * sr)
        n = min(len(signal), len(out) - i)
        if n > 0:
            out[i:i+n] += signal[:n] * gain

    chords = [[57,60,64,67], [53,57,60,64], [48,52,55,59], [55,59,62,64]]
    for beat in range(40):
        at = beat * .5
        chord = chords[(beat // 8) % 4]
        t = np.arange(round(.22 * sr)) / sr
        kick = np.sin(2*np.pi*(50*t+1.7*(1-np.exp(-35*t)))) * np.exp(-24*t)
        add(at, kick, (.14 if beat%2==0 else .06) if soft else (.28 if beat%2==0 else .16))
        t = np.arange(round(.75 * sr)) / sr
        f = hz(chord[beat % 4] + 12)
        pluck = (np.sin(2*np.pi*f*t)+.12*np.sin(4*np.pi*f*t)) * np.exp(-6*t) * np.minimum(t/.01,1)
        add(at, pluck, .12 if soft else .09)
        if beat % 4 == 0:
            t = np.arange(round(1.8 * sr)) / sr
            pad = sum(np.sin(2*np.pi*hz(n)*t) for n in chord)/4
            add(at, pad*np.minimum(t/.12,1)*np.exp(-1.8*t), .2 if soft else .12)
        for sub in [0,.25]:
            t = np.arange(round(.045 * sr))/sr
            noise = np.r_[0,np.diff(rng.normal(size=len(t)))]*np.exp(-110*t)
            add(at+sub,noise,.009 if soft else .024)
        if not soft and beat%2==1:
            t = np.arange(round(.13 * sr))/sr
            snap = rng.normal(size=len(t))*np.exp(-45*t)
            add(at,snap,.055)
    accents = grid[name + '_cues']
    for at in accents:
        t = np.arange(round(.16 * sr))/sr
        chirp = np.sin(2*np.pi*(520*t+1800*t*t))
        add(at,chirp*np.sin(np.pi*t/.16)**2*np.exp(-10*t),.018 if soft else .038)
    t = np.arange(len(out))/sr
    out *= np.minimum(t/.04,1)*np.minimum((duration-t)/.6,1)
    out = np.tanh(out*1.6)
    out *= .8/max(np.max(np.abs(out)),.01)
    stereo = np.column_stack([out,out*.98])
    with wave.open(str(root/(name+'-musica-original.wav')),'wb') as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(sr)
        f.writeframes((stereo*32767).astype('<i2').tobytes())

