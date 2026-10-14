from pathlib import Path
import json,re,zipfile
import pymupdf as fitz
from PIL import Image,ImageDraw,ImageFont
from lxml import etree

root=Path(__file__).parent
out=root/"研究报告交付"
qa=root/"材料整理/最终版式检查";qa.mkdir(exist_ok=True)
pdf=fitz.open(out/"桂阳县苦志育才公益学校调研报告.pdf")
font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf",18)
checks=[]
for i,page in enumerate(pdf):
    pix=page.get_pixmap(matrix=fitz.Matrix(1.25,1.25))
    pix.save(str(qa/f"page_{i+1:02}.png"))
    text=page.get_text()
    blocks=page.get_text("blocks")
    outside=[list(b[:4]) for b in blocks if b[0]<-1 or b[1]<-1 or b[2]>page.rect.width+1 or b[3]>page.rect.height+1]
    lines=text.splitlines()
    checks.append({"页码":i+1,"文字数":len(text),"超出页面内容":outside,"开头":lines[:5],"末尾":lines[-3:]})
for start in range(0,len(pdf),4):
    sheet=Image.new("RGB",(1320,1760),"#dddddd");d=ImageDraw.Draw(sheet)
    for k,i in enumerate(range(start,min(start+4,len(pdf)))):
        im=Image.open(qa/f"page_{i+1:02}.png").convert("RGB");im.thumbnail((650,845))
        x=(k%2)*660;y=(k//2)*880
        sheet.paste(im,(x,y+25));d.text((x+10,y+2),f"PAGE {i+1}",font=font,fill="black")
    sheet.save(qa/f"contact_{start//4+1:02}.jpg",quality=93)
alltext="".join(p.get_text() for p in pdf)
assert "{{" not in alltext
assert not any(x["超出页面内容"] for x in checks)
for expected in ["3.37","2.71","460","486","118","19:50","20:30","00:27"]:
    assert expected in alltext,expected
stat=json.loads((out/"分析数据/统计摘要.json").read_text(encoding="utf-8"))
assert stat["评分条目数"]==35 and stat["评分总分"]==118
assert sum(stat["分布"].values())==35 and sum(stat["作息"].values())==870
assert stat["照片数"]==111
with zipfile.ZipFile(out/"桂阳县苦志育才公益学校调研报告.docx") as z:
    doc=etree.fromstring(z.read("word/document.xml"))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    assert not doc.xpath('//w:pBdr',namespaces=ns)
    pics=doc.xpath('//*[local-name()="blip"]')
    assert len(pics)==7
(qa/"版式与数据核查.json").write_text(json.dumps({"总页数":len(pdf),"数据核查":"通过","页面":checks},ensure_ascii=False,indent=2),encoding="utf-8")
for x in checks:
    print(x["页码"],x["文字数"],"|".join(x["开头"][2:4]),"...","|".join(x["末尾"]))
print("PASS",len(pdf),"pages")
