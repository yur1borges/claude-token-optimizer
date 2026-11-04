import json
from pathlib import Path

d = Path('graphify-out')
for f in sorted(d.glob('.graphify_chunk_*.json')):
    try:
        j = json.loads(f.read_text(encoding='utf-8'))
    except Exception as e:
        print(f'{f.name}: JSON INVALIDO -> {e}')
        continue
    if 'files' in j:
        print(f'{f.name}: AINDA MANIFESTO ({len(j["files"])} arquivos)')
    else:
        print(f'{f.name}: OK  nodes={len(j.get("nodes", []))} edges={len(j.get("edges", []))} hyper={len(j.get("hyperedges", []))}')
