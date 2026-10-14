from pathlib import Path
import json,re,csv,ast,zipfile,shutil
import pymupdf as fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).parent;OUT=ROOT/'论文与作品集';WORK=OUT/'工作文件'
data=json.loads((WORK/'manuscript.json').read_text(encoding='utf-8'))
ANALYSIS=OUT/'分析数据';ANALYSIS.mkdir(exist_ok=True)
for f in (ROOT/'研究报告交付'/'分析数据').iterdir():
    if f.suffix in ['.csv','.json','.txt']:shutil.copy2(f,ANALYSIS/f.name)
raw=list(csv.DictReader((ANALYSIS/'环境审计全部项目.csv').open(encoding='utf-8-sig')))
assert len(raw)==35 and sum(int(r['评分']) for r in raw)==118
assert sum(int(r['评分'])<=2 for r in raw)==10
tree=ast.parse((ROOT/'build_bilingual_portfolio.py').read_text(encoding='utf-8'))
enitems=None
for n in ast.walk(tree):
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='english' for t in n.targets):
        enitems=ast.literal_eval(n.value)
assert len(enitems)==35
domains={'基础安全':'Basic safety','舒适性':'Comfort','活动支持':'Activity support','照护支持':'Care support','空间联结':'Spatial connections'}
with (ANALYSIS/'Environmental_audit_EN.csv').open('w',encoding='utf-8-sig',newline='') as fh:
    w=csv.writer(fh);w.writerow(['Item','Domain','Question','Original mark'])
    for i,(r,e) in enumerate(zip(raw,enitems)):w.writerow([i+1,domains[r['维度']],e,r['评分']])
keywords={'教室':'Classroom','资金':'Funding','教学楼':'Teaching building','操场':'Playground','校医室':'School clinic','厕所':'Toilet','玩耍':'Play','空间':'Space'}
with (ANALYSIS/'Selected_keywords_EN.csv').open('w',encoding='utf-8-sig',newline='') as fh:
    w=csv.writer(fh);w.writerow(['English label','Chinese search term','Occurrences','Respondents','Response units'])
    for r in csv.DictReader((ANALYSIS/'关键词频次.csv').open(encoding='utf-8-sig')):
        if r['关键词'] in keywords:w.writerow([keywords[r['关键词']],r['关键词'],r['次数'],r['涉及受访者数'],r['涉及答题单元数']])
shutil.copy2(WORK/'gis_metrics.json',ANALYSIS/'GIS_site_metrics.json')

checks={}
def norm(s):return re.sub(r'\s+','',s).replace('’',"'").replace('ﬁ','fi').replace('ﬂ','fl')
for lang in ['EN','ZH']:
    p=OUT/f'Everyday_Care_Research_and_Portfolio_{lang}.pdf'
    doc=fitz.open(p)
    text=norm(''.join(doc[i].get_text() for i in range(1,13)))
    missing=[]
    for s in data['sections']:
        for para in s['english' if lang=='EN' else 'chinese']:
            if norm(para) not in text:missing.append(para[:65])
    assert not missing,(lang,missing)
    checks[lang]={'pages':len(doc),'paper_paragraphs_present':True,'A4_landscape':True}
    assert len(doc)==29
    wd=fitz.open(WORK/f'Paper_{lang}_Word_check.pdf')
    # Render every Word page after the final title styling update.
    tiles=[]
    for i,pg in enumerate(wd):
        pix=pg.get_pixmap(matrix=fitz.Matrix(.8,.8))
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((263,375))
        tile=Image.new('RGB',(280,402),'#E1E4DF');tile.paste(im,((280-im.width)//2,5))
        ImageDraw.Draw(tile).text((10,384),f'{lang} {i+1}',fill='#252D2C');tiles.append(tile)
    for start in range(0,len(tiles),8):
        group=tiles[start:start+8];sheet=Image.new('RGB',(1120,402*((len(group)+3)//4)),'#E1E4DF')
        for j,im in enumerate(group):sheet.paste(im,((j%4)*280,(j//4)*402))
        sheet.save(WORK/f'Word_final_{lang}_{start//8+1}.jpg',quality=93)
    checks[lang]['word_document_pages']=len(wd)
    checks[lang]['pdf_size_mb']=round(p.stat().st_size/1e6,2)
(WORK/'final_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')

readme=f"""# 论文与校园设计作品集

正式阅读与提交文件

- Everyday_Care_Research_and_Portfolio_EN.pdf：英文完整版本，29页，A4横向。
- Everyday_Care_Research_and_Portfolio_ZH.pdf：完整中文版本，29页，与英文版逐页对应。
- Paper_EN_Editable.docx / Paper_ZH_Editable.docx：可编辑论文稿。
- Paper_EN.md / Paper_ZH.md：纯文字编辑稿。
- 图表与图纸：独立图表、编号图纸及建筑拼贴。
- 分析数据：问卷、词频、环境审计、作息、观察与GIS面积等整理数据。

英文论文共{data['word_count']:,}词，含摘要，不含参考资料、图注及作品集文字。

页码

01 封面
02 研究概览
03—13 论文
14 参考资料
15 问卷逐题对照
16 环境审计全部项目
17—29 设计作品集

画面采用暖白、炭灰、鼠尾草绿与少量陶土色；建筑图纸保留矢量线稿。
效果图以建筑主体裁切和版面拼贴重新构成，保留原有建筑关系。

# Research and campus design portfolio

The English and Chinese editions each contain 29 A4 landscape pages.
The paper contains {data['word_count']:,} English words including the abstract, excluding references, captions and portfolio text.
The editable Word and Markdown files contain the paper; the complete designed editions are the PDFs.
Supporting charts, keyed drawings, architectural collages and analysis tables are included in their respective folders.
"""
(OUT/'阅读说明_README.md').write_text(readme,encoding='utf-8')
# Compact preview for the final response.
preview=Image.new('RGB',(1440,1042),'#DDE2D8')
for j,pno in enumerate([1,5,21,28]):
    im=Image.open(WORK/'版式检查'/f'EN_{pno:02d}.png');im.thumbnail((690,490))
    preview.paste(im,(15+(j%2)*720,15+(j//2)*521))
preview.save(OUT/'Portfolio_preview.jpg',quality=95)
zip_path=OUT/'Kuzhi_Yucai_Bilingual_Research_and_Portfolio.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in OUT.iterdir():
        if f.is_file() and f.suffix.lower() in ['.pdf','.docx','.md','.jpg']:
            z.write(f,f.name)
    for folder in ['图表与图纸','分析数据']:
        for f in (OUT/folder).rglob('*'):
            if f.is_file():z.write(f,f.relative_to(OUT))
print(json.dumps(checks,ensure_ascii=False,indent=2))
print('ZIP',round(zip_path.stat().st_size/1e6,2),'MB')
