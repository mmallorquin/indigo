#!/usr/bin/env python3
"""Synthesize ten sample-free instrumental beds and verify their final WAVs.

Requirements: Python 3, NumPy, ffmpeg and ffprobe on PATH.
Run this script from any directory. Its only persisted outputs are
editor/public/audio/01..10.wav and videos-v6-olivo/licencia/origen.md.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import wave

import numpy as np

SR = 48_000
DURATION = 24.0
TARGET_I = -18.0
TARGET_TP = -3.2
EDITOR = Path(__file__).resolve().parents[1]
PACKAGE = EDITOR.parent
OUTPUT = EDITOR / "public" / "audio"
FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")

# Bass roots use MIDI pitches; keys voice the 3rd, 5th, 7th and 9th/13th.
VOICINGS = {
    "min9": (3, 7, 10, 14),
    "min7": (3, 7, 10, 12),
    "maj9": (4, 7, 11, 14),
    "13": (4, 10, 14, 21),
}
TRACKS = [
    ("01", "Estampa", 100, [(38, "min9"), (43, "13"), (36, "maj9"), (45, "min9")]),
    ("02", "Capas", 102, [(41, "maj9"), (45, "min7"), (43, "min9"), (36, "13")]),
    ("03", "Base", 104, [(40, "min9"), (45, "13"), (38, "maj9"), (47, "min9")]),
    ("04", "Lineas", 106, [(45, "min9"), (41, "maj9"), (36, "maj9"), (43, "13")]),
    ("05", "Tres ideas", 108, [(36, "maj9"), (40, "min7"), (38, "min9"), (43, "13")]),
    ("06", "Detalle", 110, [(47, "min9"), (40, "13"), (45, "maj9"), (42, "min9")]),
    ("07", "Diptico", 112, [(43, "min9"), (36, "13"), (41, "maj9"), (38, "min9")]),
    ("08", "Cuello", 103, [(38, "maj9"), (47, "min9"), (40, "min9"), (45, "13")]),
    ("09", "Azul y crema", 105, [(36, "min9"), (41, "13"), (46, "maj9"), (43, "min9")]),
    ("10", "Referencias", 109, [(42, "min9"), (47, "13"), (40, "maj9"), (37, "min9")]),
]


def frequency(midi: float) -> float:
    return 440.0 * 2.0 ** ((midi - 69.0) / 12.0)


def smooth_edges(signal: np.ndarray, attack: float, release: float) -> np.ndarray:
    signal = signal.copy()
    a = min(len(signal), round(attack * SR))
    r = min(len(signal), round(release * SR))
    if a:
        signal[:a] *= np.sin(np.linspace(0, math.pi / 2, a)) ** 2
    if r:
        signal[-r:] *= np.cos(np.linspace(0, math.pi / 2, r)) ** 2
    return signal


def key(midi: float, length: float, brightness: float) -> np.ndarray:
    t = np.arange(round(length * SR), dtype=np.float64) / SR
    f = frequency(midi)
    # Gentle electric-piano-like FM, with a quickly decaying overtone.
    phase = 2 * math.pi * f * t
    fm = brightness * np.exp(-t / 0.38) * np.sin(2 * phase)
    wave_ = np.sin(phase + fm) + 0.11 * np.sin(2 * phase) * np.exp(-t / 0.24)
    wave_ += 0.045 * np.sin(3 * phase) * np.exp(-t / 0.16)
    envelope = np.exp(-t / 0.65) * (0.98 + 0.02 * np.sin(2 * math.pi * 4.2 * t))
    return smooth_edges(wave_ * envelope, 0.014, min(0.12, length / 3))


def bass(midi: float, length: float) -> np.ndarray:
    t = np.arange(round(length * SR), dtype=np.float64) / SR
    phase = 2 * math.pi * frequency(midi) * t
    wave_ = np.sin(phase) + 0.16 * np.sin(2 * phase)
    return smooth_edges(wave_ * np.exp(-t / 0.48), 0.022, min(0.09, length / 3))


def kick() -> np.ndarray:
    t = np.arange(round(0.30 * SR), dtype=np.float64) / SR
    # Smooth 100-to-49 Hz pitch fall, with no click sample.
    phase = 2 * math.pi * (49 * t + 51 * 0.034 * (1 - np.exp(-t / 0.034)))
    wave_ = np.sin(phase) * np.exp(-t / 0.081)
    return smooth_edges(wave_, 0.006, 0.06)


def filtered_noise(rng: np.random.Generator, length: float, low_pass: int) -> np.ndarray:
    noise = rng.standard_normal(round(length * SR))
    return np.convolve(noise, np.ones(low_pass) / low_pass, mode="same")


def hat(rng: np.random.Generator, length: float = 0.075) -> np.ndarray:
    t = np.arange(round(length * SR), dtype=np.float64) / SR
    noise = filtered_noise(rng, length, 4)
    # Remove much of the low/mid band; keep hats quiet and rounded.
    noise -= np.convolve(noise, np.ones(21) / 21, mode="same")
    return smooth_edges(noise * np.exp(-t / 0.022), 0.003, 0.02)


def snare(rng: np.random.Generator) -> np.ndarray:
    length = 0.18
    t = np.arange(round(length * SR), dtype=np.float64) / SR
    noise = filtered_noise(rng, length, 8)
    body = 0.25 * np.sin(2 * math.pi * 170 * t) * np.exp(-t / 0.042)
    return smooth_edges(noise * np.exp(-t / 0.039) + body, 0.007, 0.04)


def synthesize(index: int, bpm: int, progression: list) -> np.ndarray:
    rng = np.random.default_rng(20261011 + index * 1009)
    stereo = np.zeros((round(DURATION * SR), 2), dtype=np.float64)
    beat = 60.0 / bpm
    swing = [0.018, 0.030, 0.012, 0.025, 0.016][index % 5]
    rhythm = [(0.0, 1.5, 3.0), (0.0, 2.5), (0.5, 2.0, 3.5), (0.0, 1.75, 3.25), (0.0, 2.0)][index % 5]
    arp_rhythm = [(0.5, 1.0, 2.5, 3.5), (1.0, 2.0, 3.5), (0.0, 1.5, 2.5), (1.0, 2.5, 3.0), (0.5, 1.5, 3.0)][index % 5]

    def place(mono: np.ndarray, start: float, level: float, pan: float = 0.0):
        offset = round(start * SR)
        if offset >= len(stereo) or offset < 0:
            return
        stop = min(len(stereo), offset + len(mono))
        p = max(-1.0, min(1.0, pan))
        # Equal-power stereo panning. No widening or phase inversion.
        gains = np.array([math.cos((p + 1) * math.pi / 4), math.sin((p + 1) * math.pi / 4)])
        stereo[offset:stop] += mono[:stop - offset, None] * gains * level

    k = kick()
    n_beats = math.ceil(DURATION / beat)
    for q in range(n_beats):
        when = q * beat
        place(k, when, 0.13 * (1.0 if q % 4 == 0 else 0.86))
        place(hat(rng), when + beat / 2 + swing, 0.022, 0.30 if q % 2 == 0 else -0.30)
        if index % 3 != 0 and q % 2:
            place(hat(rng, 0.055), when, 0.009, -0.15)
        if q % 4 in (1, 3):
            place(snare(rng), when + 0.010, 0.051 if q % 4 == 3 else 0.039, -0.06)

    for bar in range(math.ceil(DURATION / (4 * beat))):
        root, quality = progression[bar % len(progression)]
        notes = [root + 12 + interval for interval in VOICINGS[quality]]
        # A small inversion change every second phrase, without changing roots.
        if (bar // 4 + index) % 2:
            notes = notes[1:] + [notes[0] + 12]
        bar_start = bar * 4 * beat
        for accent, pos in enumerate(rhythm):
            when = bar_start + pos * beat + (0.007 if pos % 1 else 0.0)
            for voice, note in enumerate(notes):
                place(key(note, 1.36, 0.35 + index * 0.008), when + voice * 0.006,
                      (0.043 if accent == 0 else 0.028) * (1.0 - voice * 0.07),
                      (-0.28 + voice * 0.18) * (1 if index % 2 else -1))
        for step, pos in enumerate(arp_rhythm):
            note = notes[(step + index + bar) % len(notes)] + (12 if index in (1, 5) and step == 1 else 0)
            place(key(note, 0.56, 0.24), bar_start + pos * beat + swing,
                  0.016 + 0.002 * (index % 3), 0.38 if step % 2 else -0.38)
        for pos, interval, level in [(0.0, 0, 0.100), (2.0, 0, 0.070), (3.5, 7 if index % 2 else 0, 0.040)]:
            place(bass(root + interval, min(0.66, beat * 0.92)), bar_start + pos * beat,
                  level, 0.0)

    # Low-level cross delays on the music bus give space without dense reverb.
    dry = stereo.copy()
    for delay, gain in [(0.13, 0.065), (0.26, 0.033), (0.39, 0.016)]:
        samples = round(delay * SR)
        stereo[samples:] += dry[:-samples, ::-1] * gain
    stereo -= np.mean(stereo, axis=0)
    stereo = np.tanh(stereo * 1.20) / 1.20
    fade_in = np.sin(np.linspace(0, math.pi / 2, round(0.80 * SR))) ** 2
    fade_out = np.cos(np.linspace(0, math.pi / 2, round(2.0 * SR))) ** 2
    stereo[:len(fade_in)] *= fade_in[:, None]
    stereo[-len(fade_out):] *= fade_out[:, None]
    return np.asarray(stereo, dtype="<f4")


def parse_measurement(stderr: str) -> dict:
    blocks = re.findall(r'\{\s*"input_i".*?\}', stderr, re.DOTALL)
    if not blocks:
        raise RuntimeError("ffmpeg did not return loudnorm measurements: " + stderr[-1000:])
    return json.loads(blocks[-1])


def measure_raw(samples: np.ndarray) -> dict:
    command = [FFMPEG, "-hide_banner", "-nostdin", "-f", "f32le", "-ar", str(SR),
               "-ac", "2", "-i", "pipe:0", "-af",
               f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA=7:print_format=json",
               "-f", "null", "-"]
    run = subprocess.run(command, input=samples.tobytes(), capture_output=True, check=True)
    return parse_measurement(run.stderr.decode())


def normalize(samples: np.ndarray, destination: Path) -> None:
    first = measure_raw(samples)
    filter_ = (f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA=7:"
               f"measured_I={first['input_i']}:measured_TP={first['input_tp']}:"
               f"measured_LRA={first['input_lra']}:measured_thresh={first['input_thresh']}:"
               f"offset={first['target_offset']}:linear=true:print_format=json")
    command = [FFMPEG, "-y", "-hide_banner", "-nostdin", "-f", "f32le", "-ar", str(SR),
               "-ac", "2", "-i", "pipe:0", "-af", filter_, "-ar", str(SR), "-ac", "2",
               "-t", str(DURATION), "-c:a", "pcm_s16le", str(destination)]
    subprocess.run(command, input=samples.tobytes(), capture_output=True, check=True)


def inspect(destination: Path, bpm: int, name: str) -> dict:
    command = [FFMPEG, "-hide_banner", "-nostdin", "-i", str(destination), "-af",
               f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA=7:print_format=json", "-f", "null", "-"]
    run = subprocess.run(command, capture_output=True, check=True)
    stats = parse_measurement(run.stderr.decode())
    with wave.open(str(destination), "rb") as wav:
        assert wav.getframerate() == SR and wav.getnchannels() == 2
        assert wav.getsampwidth() == 2
        frames = wav.getnframes()
        data = np.frombuffer(wav.readframes(frames), dtype="<i2").astype(np.float64) / 32768
    peak = float(np.max(np.abs(data)))
    duration = frames / SR
    row = {"archivo": destination.name, "nombre": name, "bpm": bpm, "duracion_s": duration,
           "sample_rate": SR, "canales": 2, "pico_dBFS": round(20 * math.log10(peak), 3),
           "LUFS_I": float(stats["input_i"]), "pico_verdadero_dBTP": float(stats["input_tp"]),
           "LRA_LU": float(stats["input_lra"])}
    assert duration == DURATION, row
    assert row["pico_dBFS"] <= -3.0 and row["pico_verdadero_dBTP"] <= -3.0, row
    assert abs(row["LUFS_I"] - TARGET_I) <= 1.0, row
    return row


def write_origin(rows: list[dict]) -> None:
    destination = PACKAGE / "licencia" / "origen.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Música instrumental original — Índigo Py v6 olivo", "",
        "Las diez pistas se sintetizaron íntegramente con el generador local `editor/scripts/musica.py`. "
        "No contienen voz, grabaciones de personas, loops, samples, melodías importadas ni archivos de audio externos. "
        "Los timbres de teclas, bajo, kick, hi-hat y caja suave se construyen con osciladores, envolventes y ruido "
        "pseudoaleatorio de semilla fija. Las progresiones y patrones están definidos en el script.", "",
        "## Uso", "",
        "Audio creado por encargo para estas piezas de Índigo Py. Se entrega para usar, editar, "
        "recortar y distribuir en el contenido de la marca, sin pago adicional ni atribución obligatoria. "
        "No se incorpora material musical de terceros. Python, NumPy y FFmpeg son herramientas de síntesis "
        "y procesamiento; sus archivos o grabaciones no se incluyen como samples.", "",
        "## Reproducción", "",
        "Requisitos: Python 3 con NumPy y FFmpeg/FFprobe en PATH. Ejecutar `python3 editor/scripts/musica.py` "
        "desde la raíz de `videos-v6-olivo`, o ejecutar el script por ruta absoluta. "
        "Las semillas son fijas. La síntesis es reproducible; pequeñas diferencias de normalización "
        "pueden depender de la versión de FFmpeg.", "",
        "Formato: WAV PCM de 16 bits, 48.000 Hz, estéreo, 24 segundos por pista. "
        "Entrada de 0,8 s y salida de 2 s con curva suave. Pulsos entre 100 y 112 BPM. "
        "Normalización EBU R128 hacia −18 LUFS-I con techo de −3,2 dBTP.", "",
        "Al recortar una pista para un video de menos de 24 s, aplicar una nueva salida suave "
        "durante el último segundo del video; la salida incluida termina al segundo 24.", "",
        "## Mediciones de los WAV finales", "",
        "| Archivo | Referencia | BPM | Duración s | Pico dBFS | LUFS-I | Pico dBTP | LRA LU |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['archivo']} | {row['nombre']} | {row['bpm']} | {row['duracion_s']:.3f} | "
                     f"{row['pico_dBFS']:.3f} | {row['LUFS_I']:.2f} | "
                     f"{row['pico_verdadero_dBTP']:.2f} | {row['LRA_LU']:.2f} |")
    lines.extend(["", "Mediciones realizadas sobre cada WAV exportado, con FFmpeg/loudnorm "
                  "para LUFS-I y true peak, y muestras PCM para el pico dBFS. "
                  "El generador verifica duración, frecuencia, canales, techo de picos y tolerancia de ±1 LU "
                  "antes de escribir este informe.", ""])
    destination.write_text("\n".join(lines))


def main() -> None:
    if not FFMPEG or not FFPROBE:
        raise RuntimeError("ffmpeg and ffprobe must be available on PATH")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, (identifier, name, bpm, progression) in enumerate(TRACKS):
        destination = OUTPUT / f"{identifier}.wav"
        normalize(synthesize(index, bpm, progression), destination)
        row = inspect(destination, bpm, name)
        rows.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
    write_origin(rows)
    print(json.dumps({"pistas": len(rows), "origen": str(PACKAGE / "licencia" / "origen.md")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
