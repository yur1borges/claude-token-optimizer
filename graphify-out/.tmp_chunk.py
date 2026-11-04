import json, os
from pathlib import Path

d = json.loads(Path('graphify-out/.graphify_detect.json').read_text(encoding='utf-8'))
uncached = [line for line in Path('graphify-out/.graphify_uncached.txt').read_text(encoding='utf-8').splitlines() if line]
# 15 images get own chunk each; rest batched 25 per
files = [f for f in uncached if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
text_files = [f for f in uncached if f.lower() not in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}]
chunks = []
n = 0
for cat, flist in (('image', files), ('doc', text_files)):
    for i in range(0, len(flist), 25):
        chunk = flist[i:i+25]
        fname = f'.graphify_chunk_{cat}{len(chunks):02d}.json'
        Path(f'graphify-out/{fname}').write_text(json.dumps({'files': chunk}, ensure_ascii=False), encoding='utf-8')
        chunks.append((fname, chunk))
print(f'Total chunks: {len(chunks)}')
for c, f in chunks[:5]: print(f'  {c}: {len(f)}')
print('  ...')
for c, f in chunks[-3:]: print(f'  {c}: {len(f)}')
