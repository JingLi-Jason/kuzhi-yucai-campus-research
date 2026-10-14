from pathlib import Path
import csv, hashlib, sys
root=Path(__file__).resolve().parents[1]
errors=[]
with (root/'docs/file_manifest.csv').open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
for row in rows:
    p=root/row['path']
    if not p.is_file():errors.append('Missing: '+row['path']);continue
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    if h.hexdigest()!=row['sha256'] or p.stat().st_size!=int(row['bytes']):errors.append('Changed: '+row['path'])
for p in root.rglob('*'):
    if '.git' in p.parts:continue
    if p.is_dir() and not p.name.isascii():errors.append('Non-English directory: '+str(p.relative_to(root)))
print('\n'.join(errors) if errors else f'PASS: {len(rows)} files verified; all directories use ASCII names.')
sys.exit(bool(errors))
