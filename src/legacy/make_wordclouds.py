from pathlib import Path
import json,csv,math,random,copy,html,zipfile
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import pymupdf as fitz
from PIL import Image,ImageDraw,ImageFont

R=Path(__file__).parent
B=R/'论文与作品集/工作文件/ppt_build'
OUT=R/'论文与作品集/英文15页_词云版'
FIG=OUT/'Word_Clouds';FIG.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('ArialBold','C:/Windows/Fonts/arialbd.ttf'))
corpus=(R/'研究报告交付/分析数据/词频语料_仅填写答案.txt').read_text('utf8')
pairs=[
 ('教室','Classroom'),('资金','Funding'),('教学楼','Teaching building'),
 ('活动','Activity'),('操场','Playground'),('校医室','School clinic'),
 ('厕所','Toilet'),('玩耍','Play'),('空间','Space'),('公益','Charity'),
 ('志愿活动','Volunteering'),('生活照顾','Daily care'),('情绪支持','Emotional support'),
 ('后坪','Rear grounds'),('后院','Backyard'),('师资','Teaching staff'),
 ('捐款','Donations'),('志愿者','Volunteers'),('医疗','Medical care'),
 ('课桌','Desks'),('宿舍','Dormitory'),('食堂','Dining hall'),
 ('菜地','Vegetable plot'),('设施','Facilities'),('互动','Interaction')]
mapping=dict(pairs)
groups=[
 ('Recurring terms',[cn for cn,en in pairs]),
 ('Campus spaces',['教室','教学楼','操场','校医室','厕所','空间','宿舍','食堂','后坪','后院','菜地']),
 ('Care & resources',['资金','公益','志愿活动','生活照顾','情绪支持','师资','捐款','志愿者','医疗','互动'])
]
palette=['#345A60','#506D62','#687F72','#738C82','#42646A']
def pack(words,w,h,seed):
    words=sorted(words,key=lambda a:-a['count'])
    maximum=max(a['count'] for a in words)
    for maxfont in [31-i*.4 for i in range(35)]:
        rng=random.Random(seed);placed=[]
        for k,a in enumerate(words):
            size=maxfont*math.sqrt(a['count']/maximum)
            tw=pdfmetrics.stringWidth(a['english'],'ArialBold',size)+4
            th=size*1.16+2
            # Cluster the words around the center while keeping a small clear gutter.
            points=[((w-tw)/2,(h-th)/2)]
            points += [(rng.uniform(2,max(2,w-tw-2)),rng.uniform(1,max(1,h-th-1))) for _ in range(4500)]
            points.sort(key=lambda p: ((p[0]+tw/2-w/2)/(w*.53))**2+((p[1]+th/2-h/2)/(h*.62))**2)
            pos=None
            for x,y in points:
                if x+tw>w or y+th>h:continue
                if all(x+tw+1<p['x'] or p['x']+p['w']+1<x or y+th+1<p['y'] or p['y']+p['h']+1<y for p in placed):
                    pos=(x,y);break
            if pos is None:break
            placed.append(dict(**a,x=pos[0],y=pos[1],w=tw,h=th,size=size,color=palette[k%len(palette)]))
        if len(placed)==len(words):
            # Center the actual cluster, rather than its empty bounding canvas.
            x0=min(a['x'] for a in placed);x1=max(a['x']+a['w'] for a in placed)
            y0=min(a['y'] for a in placed);y1=max(a['y']+a['h'] for a in placed)
            for a in placed:a['x']+=(w-x1-x0)/2;a['y']+=(h-y1-y0)/2
            return placed
    raise ValueError('Cloud packing failed')

d=json.loads((B/'wordfreq3_layout_EN.json').read_text('utf8'))
s=d['slides'][2];clouds=[]
oldcharts=[o for o in s['objects'] if o.get('chart')=='frequency']
for n,((title,terms),o) in enumerate(zip(groups,oldcharts),1):
    words=[dict(chinese=t,english=mapping[t],count=corpus.count(t)) for t in terms]
    cloud=pack(words,o['w'],o['h'],40+n)
    clouds.append(dict(title=title,width=o['w'],height=o['h'],words=cloud))
    idx=s['objects'].index(o)
    shapes=[]
    for a in cloud:
        shapes.append(dict(kind='text',text=a['english'],x=o['x']+a['x'],y=o['y']+a['y'],
                           w=a['w'],h=a['h'],size=a['size'],leading=a['size']*1.16,
                           font='SansB',color=a['color'],source='single'))
    s['objects'][idx:idx+1]=shapes
    # Vector exports and raster previews share the same data-derived layout.
    fw,fh=1200,680;scale=1100/o['w']
    pdf=FIG/f'Word_Cloud_{n:02d}.pdf'
    c=canvas.Canvas(str(pdf),pagesize=(fw,fh))
    c.setFillColorRGB(1,1,1);c.rect(0,0,fw,fh,fill=1,stroke=0)
    c.setFillColor('#252D2C');c.setFont('ArialBold',27);c.drawString(42,fh-50,title)
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{fw}" height="{fh}" viewBox="0 0 {fw} {fh}">',
         '<rect width="100%" height="100%" fill="white"/>',
         f'<text x="42" y="50" font-family="Arial" font-size="27" font-weight="bold" fill="#252D2C">{html.escape(title)}</text>']
    yoff=90+(fh-150-o['h']*scale)/2
    for a in cloud:
        x=50+a['x']*scale
        y=yoff+(a['y']+a['size']*.92)*scale
        c.setFont('ArialBold',a['size']*scale);c.setFillColor(a['color'])
        c.drawString(x,fh-y,a['english'])
        svg.append(f'<text x="{x:.2f}" y="{y:.2f}" fill="{a["color"]}" font-family="Arial" font-weight="bold" font-size="{a["size"]*scale:.2f}">{html.escape(a["english"])}</text>')
    c.setFont('ArialBold',12);c.setFillColor('#65736D')
    c.drawString(42,24,'Word size reflects occurrences in the questionnaire responses.')
    c.showPage();c.save()
    svg.append('<text x="42" y="656" font-family="Arial" font-size="12" fill="#65736D">Word size reflects occurrences in the questionnaire responses.</text></svg>')
    (FIG/f'Word_Cloud_{n:02d}.svg').write_text('\n'.join(svg),'utf8')
    doc=fitz.open(pdf);doc[0].get_pixmap(matrix=fitz.Matrix(2,2)).save(FIG/f'Word_Cloud_{n:02d}.png');doc.close()
# Update only the visual-format captions.
for o in s['objects']:
    if o.get('text')=='Figure 3. Keyword occurrences in questionnaire feedback.':
        o['text']='Figure 3. Word clouds of questionnaire themes.'
    elif o.get('text')=='Occurrences in Chinese questionnaire responses.':
        o['text']='Word size reflects frequency in questionnaire responses.'
s['notes']+=' Word clouds: font size is proportional to the square root of the literal frequency, with one uniform scale per panel. All terms appear once per panel. Three panels contain selected recurring words, campus spaces, and care/resources. English labels translate the original Chinese terms.'
(B/'wordcloud_layout_EN.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
(B/'wordcloud_audit.json').write_text(json.dumps(clouds,ensure_ascii=False,indent=2),'utf8')
with (FIG/'Word_Cloud_Data.csv').open('w',encoding='utf-8-sig',newline='') as f:
    wr=csv.writer(f);wr.writerow(['Cloud','English word','Chinese term','Occurrences'])
    for cl in clouds:
        for a in cl['words']:wr.writerow([cl['title'],a['english'],a['chinese'],a['count']])
tiles=[Image.open(FIG/f'Word_Cloud_{n:02d}.png').convert('RGB') for n in range(1,4)]
sheet=Image.new('RGB',(2400,1360*3),'white')
for n,t in enumerate(tiles):sheet.paste(t,(0,1360*n))
sheet.save(FIG/'Three_Word_Clouds.png',dpi=(300,300))
js=(B/'build_wordfreq3.mjs').read_text('utf8')
for a,b in [('英文15页_三张词频图','英文15页_词云版'),('wordfreq3_','wordcloud_'),('3WordCharts','3WordClouds'),
            ('requiredNativeChartOwnerSlides:[3,4,8]','requiredNativeChartOwnerSlides:[4,8]')]:
    js=js.replace(a,b)
(B/'build_wordcloud.mjs').write_text(js,'utf8')
ps=(R/'export_wordfreq3_checks.ps1').read_text('utf8')
for a,b in [('英文15页_三张词频图','英文15页_词云版'),('3WordCharts','3WordClouds'),('WordFreq3','WordCloud')]:ps=ps.replace(a,b)
(R/'export_wordcloud_checks.ps1').write_text(ps,'utf8')
qa=(R/'review_wordfreq3.py').read_text('utf8')
for a,b in [('英文15页_三张词频图','英文15页_词云版'),('3WordCharts','3WordClouds'),('WordFreq3','WordCloud'),('wordfreq3_review','wordcloud_review'),('len(charts)==5 and len(books)==5','len(charts)==2 and len(books)==2')]:qa=qa.replace(a,b)
(R/'review_wordcloud.py').write_text(qa,'utf8')
print('Clouds built:',[(a['title'],len(a['words'])) for a in clouds])
