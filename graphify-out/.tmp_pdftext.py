import json, sys, re
from pathlib import Path
import pymupdf

manifest = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
outdir = Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
index = []
for p in manifest['files']:
    p = Path(p)
    try:
        doc = pymupdf.open(p)
        txt = "\n".join(page.get_text() for page in doc)
        doc.close()
    except Exception as e:
        txt = f"ERROR {e}"
    name = re.sub(r'[^A-Za-z0-9_.-]', '_', p.stem)
    f = outdir / (name + '.txt')
    f.write_text(txt, encoding='utf-8')
    index.append({'file': str(p), 'txt': str(f), 'chars': len(txt), 'head': txt[:1200]})
Path(outdir / '_index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')
print('done', len(index))
