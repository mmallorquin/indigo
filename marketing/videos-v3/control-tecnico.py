from pathlib import Path
import subprocess
import json
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
probes = {}
for name in ['looks', 'consulta', 'looks-sin-musica', 'consulta-sin-musica']:
    path = root / (name + '.mp4')
    probes[name] = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries',
        'stream=codec_name,width,height,r_frame_rate,nb_frames,bit_rate,sample_rate,channels,duration:format=duration,size,bit_rate',
        '-of', 'json', str(path)]))
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'null', '-'], check=True)
    if name.endswith('-sin-musica'):
        continue
    folder = root / ('qa-' + name)
    folder.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-vf', 'fps=4,scale=144:256',
                    '-y', str(folder / '%03d.jpg')], check=True)
    sheet = Image.new('RGB', (1152, 2800), '#10182F')
    draw = ImageDraw.Draw(sheet)
    for index, image in enumerate(sorted(folder.glob('*.jpg'))):
        x, y = (index % 8) * 144, (index // 8) * 280
        sheet.paste(Image.open(image), (x, y + 24))
        draw.text((x + 5, y + 5), f'{index / 4:.2f}s', fill='white')
    sheet.save(root / (name + '-qa.jpg'), quality=77)
    subprocess.run(['ffmpeg', '-v', 'info', '-i', str(path), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json',
                    '-f', 'null', '-'], stderr=open(root / (name + '-audio-control.txt'), 'w'), check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-ss', '17.1', '-frames:v', '1',
                    '-vf', 'scale=360:640', '-y', str(root / (name + '-final-cierre.jpg'))], check=True)
(root / 'datos-tecnicos.json').write_text(json.dumps(probes, indent=2))
print(json.dumps(probes, indent=2))

