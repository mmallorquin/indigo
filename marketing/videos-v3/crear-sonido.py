from pathlib import Path
import numpy as np
import wave

root = Path(__file__).resolve().parent
sr = 48000
duration = 20
rng = np.random.default_rng(303)

def hz(note):
    return 440 * 2 ** ((note - 69) / 12)

for name, accents in [('looks', [0.03, 1.93, 6.97, 12.25, 16]),
                      ('consulta', [0.03, 4.55, 7.3, 12.25, 16])]:
    out = np.zeros(int(sr * duration), dtype=np.float64)
    def add(at, signal, gain=1):
        index = int(at * sr)
        count = min(len(signal), len(out) - index)
        if count > 0:
            out[index:index + count] += signal[:count] * gain

    chords = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 64]]
    for beat in range(40):
        at = beat * .5
        chord = chords[(beat // 8) % 4]
        t = np.arange(int(.22 * sr)) / sr
        kick = np.sin(2 * np.pi * (50 * t + 1.7 * (1 - np.exp(-t * 35)))) * np.exp(-t * 24)
        add(at, kick, .22 if beat % 2 == 0 else .11)
        t = np.arange(int(.65 * sr)) / sr
        freq = hz(chord[beat % 4] + 12)
        pluck = (np.sin(2 * np.pi * freq * t) + .15 * np.sin(4 * np.pi * freq * t))
        add(at, pluck * np.exp(-t * 7) * np.minimum(t / .008, 1), .095)
        if beat % 4 == 0:
            t = np.arange(int(1.7 * sr)) / sr
            pad = sum(np.sin(2 * np.pi * hz(note) * t) for note in chord) / 4
            add(at, pad * np.minimum(t / .1, 1) * np.exp(-t * 2), .15)
        for sub in [0, .25]:
            t = np.arange(int(.04 * sr)) / sr
            noise = rng.normal(size=len(t))
            noise = np.r_[0, np.diff(noise)] * np.exp(-t * 100)
            add(at + sub, noise, .015)

    # Acentos breves de entrada, sintetizados sin muestras externas.
    for at in accents:
        t = np.arange(int(.16 * sr)) / sr
        chirp = np.sin(2 * np.pi * (520 * t + 1800 * t * t))
        add(at, chirp * np.sin(np.pi * t / .16) ** 2 * np.exp(-t * 10), .035)
    t = np.arange(len(out)) / sr
    out *= np.minimum(t / .04, 1) * np.minimum((duration - t) / .6, 1)
    out = np.tanh(out * 1.6)
    out *= .8 / max(np.max(np.abs(out)), .01)
    stereo = np.column_stack([out, out * .98])
    with wave.open(str(root / (name + '-musica-original.wav')), 'wb') as file:
        file.setnchannels(2)
        file.setsampwidth(2)
        file.setframerate(sr)
        file.writeframes((stereo * 32767).astype('<i2').tobytes())


