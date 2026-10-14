from pathlib import Path
import json,re,ast
import pymupdf as fitz
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).parent
OUT=ROOT/'论文与作品集';QA=OUT/'工作文件'/'版式检查';QA.mkdir(exist_ok=True)
result={}
for lang in ['EN','ZH']:
    doc=fitz.open(OUT/f'Everyday_Care_Research_and_Portfolio_{lang}.pdf')
    imgs=[];outside=[];texts=[]
    for i,p in enumerate(doc):
        pix=p.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
        target=QA/f'{lang}_{i+1:02d}.png';pix.save(target)
        im=Image.open(target).convert('RGB');im.thumbnail((420,297))
        tile=Image.new('RGB',(440,328),'#E1E4DF');tile.paste(im,((440-im.width)//2,20))
        ImageDraw.Draw(tile).text((12,309),f'{lang}  {i+1:02d}',fill='#252D2C')
        imgs.append(tile);texts.append(p.get_text())
        for b in p.get_text('dict')['blocks']:
            if 'lines' not in b:continue
            for line in b['lines']:
                for sp in line['spans']:
                    r=fitz.Rect(sp['bbox'])
                    if r.x0<0 or r.x1>p.rect.width+1 or r.y0<0 or r.y1>p.rect.height+1:
                        outside.append((i+1,sp['text'],list(r)))
    for start in range(0,len(imgs),9):
        chunk=imgs[start:start+9]
        sheet=Image.new('RGB',(1320,328*((len(chunk)+2)//3)),'#E1E4DF')
        for j,im in enumerate(chunk):sheet.paste(im,((j%3)*440,(j//3)*328))
        sheet.save(QA/f'{lang}_contact_{start//9+1}.jpg',quality=93)
    (QA/f'{lang}_extracted.txt').write_text('\n\n'.join(texts),encoding='utf-8')
    result[lang]={'pages':len(doc),'out_of_bounds':outside,'all_a4_landscape':all(abs(p.rect.width-841.8898)<.1 and abs(p.rect.height-595.2756)<.1 for p in doc),
                  'chinese_chars_in_english':len(re.findall(r'[\u4e00-\u9fff]',''.join(texts))) if lang=='EN' else None,
                  'has_undefined_replacement_char':'\ufffd' in ''.join(texts)}
    print(lang,result[lang])
(QA/'structural_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
# Compare the number of audit translations to recorded scores.
tree=ast.parse((ROOT/'build_bilingual_portfolio.py').read_text(encoding='utf-8'))
for n in ast.walk(tree):
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='english' for t in n.targets):
        items=ast.literal_eval(n.value)
        print('Audit English items',len(items))
        for i,t in enumerate(items):print(i+1,t)
