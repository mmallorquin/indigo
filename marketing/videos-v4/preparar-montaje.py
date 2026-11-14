from pathlib import Path
import subprocess
import json

root = Path(__file__).resolve().parent
cuts = [(321, 60), (189, 75), (125, 45), (372, 150),
        (540, 60), (630, 105), (765, 60), (63, 45)]
grid = {'bpm': 120, 'duration': 20, 'beats': [i * .5 for i in range(40)],
        'downbeats': list(range(0, 20, 2)),
        'editorial_cues': [.1, 2, 6, 14, 16],
        'energia_cues': [.1, 2, 6, 9, 13, 16]}
(root / 'beats.json').write_text(json.dumps(grid, indent=2))
chain = []
timeline = []
offset = 0
for i, (start, count) in enumerate(cuts):
    chain.append(f'[0:v]trim=start_frame={start}:end_frame={start + count},setpts=PTS-STARTPTS[v{i}]')
    timeline.append({'at': offset / 30, 'from': start / 30, 'dur': count / 30,
                     'source_frames': [start, start + count - 1]})
    offset += count
assert offset == 600
chain.append(''.join(f'[v{i}]' for i in range(len(cuts))) +
             f'concat=n={len(cuts)}:v=1:a=0,crop=590:1048:100:232,'
             'scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p[v]')
subprocess.run(['ffmpeg', '-v', 'error', '-i', str(root / 'source.mp4'),
                '-filter_complex', ';'.join(chain), '-map', '[v]', '-an',
                '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-g', '1',
                '-bf', '0', '-r', '30', '-y', str(root / 'montaje-base.mp4')], check=True)
(root / 'timeline.json').write_text(json.dumps(timeline, indent=2))

