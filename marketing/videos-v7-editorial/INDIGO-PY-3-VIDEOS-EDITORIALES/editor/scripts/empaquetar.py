"""Package the self-contained delivery and verify files, hashes and local links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import hashlib
import json
import zipfile

root = Path(__file__).resolve().parents[2]
archive = root / 'INDIGO-PY-3-VIDEOS-EDITORIALES.zip'


def include(path):
    rel = path.relative_to(root)
    if any(p in ('node_modules', 'work', '.git', '__pycache__') for p in rel.parts):
        return False
    if path.suffix == '.zip' or path.name in ('MANIFIESTO-SHA256.json', '.DS_Store'):
        return False
    if rel.parts[0] == 'qa':
        return path.name.endswith(('-40-fotogramas.jpg', '-master.json'))
    if str(rel) == 'editor/public/audio/01.wav':
        return False  # not used in these compositions
    return True


files = sorted(p for p in root.rglob('*') if p.is_file() and include(p))
manifest = [dict(archivo=str(p.relative_to(root)), bytes=p.stat().st_size,
                 sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
mp4 = [p for p in files if p.suffix == '.mp4']
assert len(mp4) == 3 and all(p.parent.name == 'finales' for p in mp4)
(root / 'MANIFIESTO-SHA256.json').write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2))
files.append(root / 'MANIFIESTO-SHA256.json')
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for p in files:
        z.write(p, p.relative_to(root))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for entry in manifest:
        assert hashlib.sha256(z.read(entry['archivo'])).hexdigest() == entry['sha256']


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        self.targets += [v for k, v in attrs if k in ('href', 'src', 'poster') and v]


parser = Links()
parser.feed((root / 'index.html').read_text())
local = [unquote(urlsplit(s).path) for s in parser.targets if not urlsplit(s).scheme]
for target in local:
    assert (root / target).is_file(), target
report = dict(archivos=len(files), mp4=len(mp4), enlaces_locales_verificados=len(local),
              bytes=archive.stat().st_size, crc='OK', hashes='OK',
              sha256=hashlib.sha256(archive.read_bytes()).hexdigest())
(root / 'PAQUETE-VERIFICADO.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
