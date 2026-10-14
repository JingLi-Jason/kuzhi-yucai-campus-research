from pathlib import Path
import json,zipfile,re
from lxml import etree as E
import pymupdf as fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).parent/'论文与作品集'
BUILD=ROOT/'工作文件'/'ppt_build'
QA=BUILD/'tight15_review';QA.mkdir(exist_ok=True)
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
all_results={}
for lang in ['EN']:
    deck=ROOT/'英文15页紧凑版'/f'Campus_Research_Portfolio_{lang}_15pages_Final.pptx'
    with zipfile.ZipFile(deck) as z:
        names=sorted([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',n)],key=lambda x:int(re.search(r'(\d+)\.xml',x).group(1)))
        colors=[];texts=[];objs=0;nonwhite=[]
        for i,n in enumerate(names):
            rt=E.fromstring(z.read(n));bg=rt.find('p:cSld/p:bg/p:bgPr/a:solidFill/a:srgbClr',ns)
            if bg is None or bg.get('val')!='FFFFFF':nonwhite.append(i+1)
            colors.extend(rt.xpath('//a:srgbClr/@val',namespaces=ns))
            texts.extend(rt.xpath('//a:t/text()',namespaces=ns))
            objs+=len(rt.findall('.//p:sp',ns))
        charts=[n for n in z.namelist() if re.search(r'/charts/chart\d+\.xml$',n)]
        books=[n for n in z.namelist() if n.endswith('.xlsx')]
        result={'slides':len(names),'editable_shapes':objs,'native_charts':len(charts),'embedded_chart_workbooks':len(books),
                'nonwhite_slide_backgrounds':nonwhite,'terracotta_color_present':'B68168' in colors}
        assert len(names)==15 and not nonwhite and len(charts)==3 and len(books)==3 and 'B68168' not in colors
    metrics=BUILD/f'Tight15_metrics_{lang}.json'
    if metrics.exists():
        mm=json.loads(metrics.read_text(encoding='utf-8-sig'));overflow=[]
        for o in mm:
            if o['boundHeight']>o['height']+1.5 or o['boundWidth']>o['width']+2:
                overflow.append({k:o[k] for k in ['slide','id','width','height','boundHeight','boundWidth','text']})
        result['powerpoint_text_overflows']=overflow
    pdf=BUILD/f'Tight15_{lang}.pdf'
    if pdf.exists():
        doc=fitz.open(pdf);tiles=[]
        for i,p in enumerate(doc):
            imfile=QA/f'{lang}_{i+1:02d}.png'
            p.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(imfile)
            im=Image.open(imfile).convert('RGB');im.thumbnail((420,298))
            tile=Image.new('RGB',(440,329),'#E5E9E3');tile.paste(im,((440-im.width)//2,10))
            ImageDraw.Draw(tile).text((10,312),f'{lang} {i+1:02d}',fill='black');tiles.append(tile)
        for start in range(0,len(tiles),9):
            group=tiles[start:start+9];sheet=Image.new('RGB',(1320,329*((len(group)+2)//3)),'#E5E9E3')
            for j,im in enumerate(group):sheet.paste(im,((j%3)*440,(j//3)*329))
            sheet.save(QA/f'{lang}_contact_{start//9+1}.jpg',quality=94)
        result['powerpoint_rendered_pages']=len(doc)
    all_results[lang]=result
    print(lang,json.dumps({k:v for k,v in result.items() if k!='powerpoint_text_overflows'},ensure_ascii=False))
    if 'powerpoint_text_overflows' in result:
        print('OVERFLOWS',len(result['powerpoint_text_overflows']))
        for o in result['powerpoint_text_overflows'][:12]:
            print(o['slide'],o['id'],round(o['height'],1),round(o['boundHeight'],1),round(o['width'],1),round(o['boundWidth'],1),o['text'][:65])
(QA/'review_results.json').write_text(json.dumps(all_results,ensure_ascii=False,indent=2),encoding='utf-8')

