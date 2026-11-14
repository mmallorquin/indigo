"""Paquete portable; excluye las carpetas de muestras individuales de revisión."""
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parent
dest = root/'paquete-produccion.zip'
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4) as z:
    for p in sorted(root.rglob('*')):
        rel = p.relative_to(root)
        if not p.is_file() or p==dest or any(x.startswith('qa-') or x=='__pycache__' for x in rel.parts):
            continue
        z.write(p,Path('videos-v4')/rel)
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    print('Paquete:',dest.stat().st_size,'bytes,',len(z.namelist()),'archivos')
