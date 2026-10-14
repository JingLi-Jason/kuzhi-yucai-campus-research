from pathlib import Path
import copy, json, re
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).parent
B = ROOT / '论文与作品集/工作文件/ppt_build'
src = json.loads((B/'publication_layout_EN.json').read_text('utf-8'))
M = json.loads((B.parent/'manuscript_publication.json').read_text('utf-8'))
for name, file in [('Sans','arial.ttf'),('SansB','arialbd.ttf'),('Serif','georgia.ttf')]:
    pdfmetrics.registerFont(TTFont(name, 'C:/Windows/Fonts/'+file))
INK, TEAL, MUTED, PALE = '#252D2C', '#345A60', '#65736D', '#F2F5F2'
W, H = src['width'], src['height']
slides, used, log = [], set(), []

def original(page, idx):
    o=copy.deepcopy(src['slides'][page-1]['objects'][idx])
    o['_origin']=[page,idx]
    used.add((page,idx))
    return o

def measure(text,w,size,font='Sans',leading=None):
    leading=leading or size*1.23
    p=Paragraph(escape(text).replace('\n','<br/>'),
                ParagraphStyle('p',fontName=font,fontSize=size,leading=leading))
    return p.wrap(w-3,5000)[1]+2

def txt(s,text,x,y,w,size=9.5,font='Sans',color=INK,leading=None,origin=None):
    o=dict(kind='text',text=text,x=x,y=y,w=w,size=size,font=font,color=color,
           leading=leading or size*1.23,source='paragraph')
    o['h']=measure(text,w,size,font,o['leading'])
    if origin:
        o['_origin']=list(origin);used.add(tuple(origin))
    s['objects'].append(o)
    return o

def put(s,p,i,x,y,w,size=None,font=None,color=None,leading=None):
    a=src['slides'][p-1]['objects'][i]
    return txt(s,a['text'],x,y,w,size or a['size'],font or a['font'],
               color or a['color'],leading,(p,i))

def rect(s,x,y,w,h,color=PALE):
    s['objects'].append(dict(kind='rect',x=x,y=y,w=w,h=h,color=color))

def line(s,x,y,x2,y2,color='#CAD3CF',width=.55):
    s['objects'].append(dict(kind='line',points=[[x,y],[x2,y2]],color=color,width=width))

def img(s,p,i,x,y,w,h):
    o=original(p,i)
    o.update(x=x,y=y,w=w,h=h)
    s['objects'].append(o)
    return o

def image_fit(s,p,i,x,y,w,h):
    a=src['slides'][p-1]['objects'][i]
    scale=min(w/a['w'],h/a['h'])
    ww,hh=a['w']*scale,a['h']*scale
    return img(s,p,i,x+(w-ww)/2,y+(h-hh)/2,ww,hh)

def page(title,section='RESEARCH'):
    n=len(slides)+1
    s=dict(title=title,bg='#FFFFFF',objects=[],notes=
           'Kuzhi Yucai Public Welfare School. Field survey and interviews, September 2026. '
           'Campus design. References on page 7: Barrett et al. (2015); Adams et al. (2009).')
    txt(s,'KUZHI YUCAI',24,13,105,7.6,'SansB',TEAL)
    txt(s,'GUIYANG COUNTY / HUNAN / CHINA',137,13,380,7.3,color=MUTED)
    txt(s,section,701,13,117,7.3,color=MUTED)
    line(s,24,31,818,31)
    txt(s,title,24,43,794,22 if n==1 else 19,'SansB')
    line(s,24,579,818,579)
    txt(s,'EVERYDAY CARE, SPATIAL CHOICE',24,583,710,6.5,color=MUTED)
    txt(s,f'{n:02d} / 15',777,582,42,7.5,color=MUTED)
    slides.append(s)
    return s

def heading(s,text,x,y,w,size=10.7,origin=None):
    return txt(s,text,x,y,w,size,'SansB',TEAL,origin=origin)

def flow(s,p,indices,x,y,w,maxy,size=9.8,leading=1.23,gap=7,minsize=9):
    # Preserve each paragraph verbatim and choose the largest size that fits.
    while True:
        heights=[measure(src['slides'][p-1]['objects'][i]['text'],w,size,
                         src['slides'][p-1]['objects'][i]['font'],size*leading) for i in indices]
        if y+sum(heights)+gap*(len(indices)-1)<=maxy+.01:break
        size=round(size-.1,2)
        if size<minsize:raise ValueError(('text does not fit',len(slides),p,indices,y,maxy,size))
    yy=y
    for i,h in zip(indices,heights):
        put(s,p,i,x,yy,w,size,leading=size*leading)
        yy+=h+gap
    log.append(dict(page=len(slides),source=p,indices=indices,font=size,end=round(yy-gap,1)))
    return yy-gap

def transform(s,p,indices,sx,sy,scale,dx,dy,text_min=6.8):
    for i in indices:
        o=original(p,i)
        if o['kind'] in ('line','polygon'):
            o['points']=[[(x-sx)*scale+dx,(y-sy)*scale+dy] for x,y in o['points']]
            o['width']=max(.3,o.get('width',.5)*scale)
        else:
            o['x']=(o['x']-sx)*scale+dx;o['y']=(o['y']-sy)*scale+dy
            o['w']*=scale;o['h']*=scale
            if o['kind']=='text':
                o['size']=max(text_min,o['size']*scale)
                o['leading']=o['size']*1.16
                o['source']='paragraph'
                o['w']=max(o['w'],pdfmetrics.stringWidth(o['text'].split('\n')[0],o['font'],o['size'])+3)
                o['h']=measure(o['text'],o['w'],o['size'],o['font'],o['leading'])
        s['objects'].append(o)

# 01 — no cover: title, keywords, abstract and opening section share one page.
s=page(M['title_en'])
put(s,2,24,24,78,794,9.1,color=TEAL)
put(s,1,8,24,100,794,10.2,font='SansB')
heading(s,'Abstract',24,132,383)
put(s,3,8,427,132,391,10.7)
flow(s,2,[8,9,10],24,154,383,455,10.2,1.24,8,9.5)
flow(s,3,[9,10,11,12],427,154,391,477,9.8,1.23,7,9.1)
line(s,24,487,818,487)
put(s,2,11,24,496,794,8.5)
for k,(a,b,c) in enumerate([(12,13,14),(15,16,17),(18,19,20)]):
    x=24+k*270
    put(s,2,a,x,515,27,16,font='SansB')
    put(s,2,b,x+34,513,220,9.4,font='SansB')
    put(s,2,c,x+34,531,220,9.1)
put(s,2,21,24,565,794,7.0)

# 02 — method text and editable route, with a small location strip.
s=page('Research methods & location')
put(s,3,13,24,80,383,10.7)
flow(s,3,[14,15,16,17],24,101,383,423,9.5,1.15,5,9)
put(s,4,8,427,80,391,10.4,font='SansB')
for k in range(6):
    x=427+(k%3)*131
    y=120+(k//3)*32
    put(s,4,9+k*2,x,y,125,9.5,font='SansB')
    put(s,4,10+k*2,x,y+13,125,7.7)
for k,(a,b,c) in enumerate([(22,23,24),(29,30,31),(36,37,38),(43,44,45),(50,51,52)]):
    y=190+k*42
    put(s,4,a,427,y,24,13,font='SansB')
    put(s,4,b,461,y,357,9.0,font='SansB')
    put(s,4,c,461,y+14,357,8.15,leading=9.6)
    if k<4:
        line(s,439,y+18,439,y+36,TEAL,.65)
        line(s,436,y+33,439,y+36,TEAL,.65)
        line(s,442,y+33,439,y+36,TEAL,.65)
put(s,4,21,427,405,391,6.9)
line(s,24,428,818,428)
# Three regional boundaries stay editable. Their footprint is deliberately small.
transform(s,9,range(11,43),30,107,.40,24,458,6.5)
for k,i in enumerate([8,9,10]):
    put(s,9,i,24+k*105,438,103,6.6,font='SansB')
put(s,9,43,24,546,316,6.4,leading=7.6)
image_fit(s,9,45,351,439,141,121)
put(s,9,56,351,563,163,6.2)
put(s,9,54,514,438,304,11,font='SansB')
put(s,9,46,514,456,304,8.5)
put(s,9,47,514,474,304,8.1,leading=9.9)
for k,i in enumerate([48,50,52]):
    rect(s,514+k*102,514,5,5,['#8D9D8E','#C8CCC7','#FFFFFF'][k])
    put(s,9,i,522+k*102,512,96,7.0)
put(s,9,55,514,529,304,7.5,leading=9)
put(s,9,57,514,564,304,6.4)
s['notes'] += ' Regional boundaries: Alibaba Cloud DataV GeoAtlas, https://geo.datav.aliyun.com/areas_v3/bound/430000_full.json and https://geo.datav.aliyun.com/areas_v3/bound/431000_full.json.'

# 03 — findings directly beside the two quantitative charts.
s=page('Questionnaire findings & environmental assessment')
for x,head,inds in [(24,8,[9,10,11,12]),(291,13,[14,15,16,17])]:
    put(s,5,head,x,80,249,10.4,font='SansB')
    flow(s,5,inds,x,111,249,564,9.4,1.14,6,9.0)
line(s,550,81,550,564)
put(s,6,8,566,80,252,10.7,font='SansB')
o=original(6,9);o.update(x=562,y=108,w=256,h=174);s['objects'].append(o)
for i,y in [(10,285),(11,301),(12,326),(13,354)]:
    put(s,6,i,566,y,252,7.6 if i!=10 else 8.4,leading=9.4)
put(s,6,14,566,382,252,10.0,font='SansB')
o=original(6,15);o.update(x=562,y=404,w=256,h=124);s['objects'].append(o)
put(s,6,16,566,534,49,10.3,font='SansB')
put(s,6,17,622,534,196,8.0)
put(s,6,18,566,548,252,7.6)
put(s,6,19,566,563,252,6.6)

# 04 — retain the full daily rhythm / operations account and time chart.
s=page('Daily rhythms & care')
for x,head,inds in [(24,8,[9,10,11,12]),(427,13,[14,15,16,17])]:
    put(s,7,head,x,80,391,10.7,font='SansB')
    flow(s,7,inds,x,103,391,425,9.5,1.2,6,9.0)
o=original(6,20);o.update(x=24,y=424,w=794,h=95);s['objects'].append(o)
put(s,6,21,24,510,794,7.0)
for k,(a,b,c) in enumerate([(22,23,24),(25,26,27),(28,29,30)]):
    x=24+270*k
    put(s,6,a,x,528,25,13,font='SansB')
    put(s,6,b,x+31,527,227,8.6,font='SansB')
    put(s,6,c,x+31,542,227,8.0,leading=9.5)
put(s,6,31,24,566,794,6.8)

# 05 — two generous reading columns, with a compact translation diagram.
s=page('Site relationships & design priorities')
for x,head,inds in [(24,8,[9,10,11,12]),(427,13,[14,15,16,17])]:
    put(s,8,head,x,80,391,11,font='SansB')
    flow(s,8,inds,x,106,391,494,10.1,1.25,9,9.3)
line(s,24,504,818,504)
for k,(a,b,c) in enumerate([(19,20,21),(22,23,24),(25,26,27),(28,29,30)]):
    x=24+k*201
    put(s,8,a,x,515,190,9.5,font='SansB')
    put(s,8,b,x,532,190,8.5)
    put(s,8,c,x+15,533,175,9.0)
put(s,8,31,24,562,794,7.0)

# 06 — architecture and delivery stay together as a complete reading spread.
s=page('Architectural organization & implementation')
for x,head,inds in [(24,8,[9,10,11,12]),(427,13,[14,15,16,17])]:
    put(s,10,head,x,80,391,11,font='SansB')
    flow(s,10,inds,x,106,391,495,10.1,1.25,9,9.3)
line(s,24,506,818,506)
for k,(a,b) in enumerate([(19,20),(21,22),(23,24),(25,26)]):
    x=24+k*201
    put(s,10,a,x,518,190,13,font='SansB')
    put(s,10,b,x,540,190,9)
put(s,10,27,24,563,794,7)

# 07 — conclusion, references and the full questionnaire appendix.
s=page('Conclusion & questionnaire feedback')
heading(s,'Conclusion',24,80,383)
y=flow(s,11,[8,9,10],24,102,383,350,9.5,1.21,7,9.0)+10
heading(s,'References',24,y,383,9.4);y+=19
for i in [13,14,15,16,17,18,19]:
    o=put(s,11,i,24,y,383,7.7 if i!=15 else 8.5,
          font='SansB' if i==15 else 'Sans',leading=9.0 if i!=15 else 10.2)
    y+=o['h']+5
log.append(dict(page=7,reference_end=y))
heading(s,'Appendix A / Questionnaire feedback',427,80,391,10.7)
rect(s,427,102,391,24)
for i,x,w in [(9,433,85),(10,521,141),(11,670,142)]:
    put(s,12,i,x,109,w,7.6,font='SansB',color=TEAL)
rows=[]
ob=src['slides'][11]['objects']
for j,o in enumerate(ob):
    if o['kind']=='text' and re.fullmatch(r'\d{2}',o['text']) and j>=8:
        rows.append([j,j+1,j+2,j+3])
for k,(num,topic,a,b) in enumerate(rows):
    yy=128+k*41.8
    if k%2==0:rect(s,427,yy,391,41.8)
    put(s,12,num,433,yy+6,18,7.8,color=MUTED)
    put(s,12,topic,455,yy+6,62,8.1,font='SansB')
    put(s,12,a,521,yy+6,141,8.4,leading=10.2)
    put(s,12,b,670,yy+6,142,8.4,leading=10.2)
    line(s,427,yy+41.8,818,yy+41.8,width=.35)
put(s,12,67,427,558,391,7.2)

# 08 — full audit beside existing-site photographs and all four design priorities.
s=page('Environmental audit & the existing school')
heading(s,'Appendix B / Environmental audit',24,80,391)
rect(s,24,102,391,22)
put(s,13,9,49,108,319,8.1,font='SansB',color=TEAL)
put(s,13,10,377,108,34,8.1,font='SansB',color=TEAL)
# Repeated column headers are retained, integrated as the start of the second block.
rows=[];obs=src['slides'][12]['objects']
for j,o in enumerate(obs):
    if o['kind']=='text' and re.fullmatch(r'\d{2}',o['text']) and j>=8:
        rows.append([j,j+1,j+2])
for k,(num,q,score) in enumerate(rows):
    yy=126+k*12.15
    if k%2==0:rect(s,24,yy,391,12.15)
    put(s,13,num,29,yy+1.5,19,7.5,color=MUTED)
    put(s,13,q,49,yy+1.4,320,7.8,leading=9.1)
    put(s,13,score,385,yy+1.2,22,8.1,font='SansB',
        color=TEAL if obs[score]['text'] in ['1','2'] else INK)
put(s,13,137,24,555,391,6.8,leading=8.1)
# These two repeated table-header objects are covered by the identical first header.
used.update({(13,75),(13,76)})
heading(s,'From school life to a design brief',437,80,381)
for k,(im,cap) in enumerate([(8,9),(10,11),(12,13),(14,15)]):
    x=437+(k%2)*196;y=104+(k//2)*164
    image_fit(s,14,im,x,y,185,143)
    put(s,14,cap,x,y+147,185,8.4,font='SansB')
for k,(a,b,c) in enumerate([(16,17,18),(19,20,21),(22,23,24),(25,26,27)]):
    x=437+(k%2)*196;y=443+(k//2)*56
    put(s,14,a,x,y,24,13,font='SansB')
    put(s,14,b,x+29,y,156,8.6,font='SansB')
    put(s,14,c,x+29,y+16,156,8.2,leading=10.0)
put(s,14,28,437,560,381,7.0)

# 09 — site plan and the editable care / circulation diagram.
s=page('A connected campus, open grounds','PORTFOLIO')
image_fit(s,15,8,24,81,391,437)
put(s,15,9,437,81,381,15.5,font='SansB')
put(s,19,29,437,126,381,10.4,font='SansB')
transform(s,19,range(8,28),57,146,.55,480,165,7.3)
put(s,19,28,437,377,381,7.7)
for k,(letter,label,body) in enumerate([(31,32,33),(35,36,37),(39,40,41)]):
    y=399+k*47
    rect(s,437,y+1,19,19,TEAL)
    put(s,19,letter,442,y+4,15,9.1,font='SansB',color='#FFFFFF')
    put(s,19,label,466,y,352,9.4,font='SansB')
    put(s,19,body,466,y+17,352,9.1)
for k,(a,b) in enumerate([(10,11),(12,13),(14,15),(16,17),(18,19)]):
    x=24+(k%2)*200;y=524+(k//2)*15
    put(s,15,a,x,y,21,8.5,font='SansB')
    put(s,15,b,x+26,y,171,8.1)
put(s,15,20,24,567,391,6.4,leading=7.5)
put(s,19,42,437,553,381,6.8,leading=8.0)

# 10 — ground floor enlarged only enough to read its room keys.
s=page('Ground level: arrival and shared life','PORTFOLIO')
image_fit(s,16,8,24,81,466,477)
put(s,16,9,515,83,67,31,font='SansB')
put(s,16,10,591,85,227,15,font='SansB')
for k,(a,b) in enumerate([(11,12),(13,14),(15,16),(17,18),(19,20),(21,22),(23,24),(25,26)]):
    y=153+k*27
    put(s,16,a,515,y,24,10.3,font='SansB')
    put(s,16,b,546,y,272,10.0)
put(s,16,27,515,382,303,10.0,leading=13)
line(s,515,443,818,443)
image_fit(s,11,11,515,452,303,80)
put(s,11,12,515,539,303,7,leading=8.5)
put(s,16,28,24,565,466,7.2)

# 11 — level two retains the drawing and complete room legend.
s=page('Level 2: learning with support nearby','PORTFOLIO')
image_fit(s,17,8,24,81,481,477)
put(s,17,9,528,86,67,32,font='SansB')
put(s,17,10,605,88,213,16.0,font='SansB')
for k,(a,b) in enumerate([(11,12),(13,14),(15,16),(17,18),(19,20),(21,22)]):
    y=181+k*37
    put(s,17,a,528,y,25,11,font='SansB')
    put(s,17,b,560,y,258,10.3)
line(s,528,420,818,420)
put(s,17,23,528,439,290,11,leading=15)
put(s,17,24,24,565,794,7.2)

# 12 — upper plans use the same scale and a shared bottom legend.
s=page('Upper levels: continuity and variety','PORTFOLIO')
put(s,18,8,24,81,391,19,font='SansB')
put(s,18,9,427,81,391,19,font='SansB')
image_fit(s,18,10,24,111,391,408)
image_fit(s,18,11,427,111,391,408)
put(s,18,12,24,529,391,9.2,leading=11.4)
put(s,18,13,427,529,391,9.2,leading=11.4)
put(s,18,14,24,566,794,7.2)

# 13 — four complementary drawings share a single architectural spread.
s=page('Elevations & sections','PORTFOLIO')
image_fit(s,20,8,24,82,391,144)
image_fit(s,20,9,427,82,391,144)
for k,(a,b) in enumerate([(10,11),(12,13),(14,15)]):
    x=24+k*270
    put(s,20,a,x,235,255,11.2,font='SansB')
    put(s,20,b,x,255,255,9.2,leading=11.8)
put(s,20,16,24,293,794,7.2)
line(s,24,310,818,310)
image_fit(s,21,8,24,321,391,186)
image_fit(s,21,9,427,321,391,186)
for x,a,b in [(24,11,12),(427,13,14)]:
    put(s,21,a,x,516,391,9.3,font='SansB')
    put(s,21,b,x,535,391,8.7,leading=10.7)
put(s,21,15,24,568,794,6.8)

# 14 — two architectural views, with their complete narrative and material palette.
s=page('Courtyard, material & a human scale','PORTFOLIO')
image_fit(s,22,8,24,82,381,259)
put(s,22,9,431,84,387,23,font='SansB')
put(s,22,10,431,161,387,11.5,leading=15)
put(s,22,12,431,253,387,10.7,leading=14)
put(s,22,13,431,316,387,7.3,leading=9.1)
line(s,24,350,818,350)
image_fit(s,23,8,24,358,535,207)
for k,(a,b) in enumerate([(10,11),(13,14),(16,17),(19,20)]):
    x=585+(k%2)*122;y=372+(k//2)*91
    rect(s,x,y,19,12,['#D6D7D1','#9BA3A1','#ACAA96','#81968A'][k])
    put(s,23,a,x,y+20,111,9.4,font='SansB')
    put(s,23,b,x,y+49,111,9.0,leading=11.3)
put(s,23,21,24,567,794,7.0)

# 15 — delivery table and phasing above two compact architectural views.
s=page('Keep the campus working','PORTFOLIO')
for i,x,w in [(8,24,157),(9,208,278),(10,508,310)]:
    put(s,24,i,x,83,w,9,font='SansB')
line(s,24,102,818,102)
for k,(a,b,c) in enumerate([(12,13,14),(16,17,18),(20,21,22),(24,25,26),(28,29,30)]):
    y=114+k*40
    if k%2==0:rect(s,24,y-5,794,40)
    put(s,24,a,24,y,167,10.5,font='SansB')
    put(s,24,b,208,y,278,10.0,leading=12.4)
    put(s,24,c,508,y,310,10.0,leading=12.4)
for k,(a,b,c) in enumerate([(33,34,35),(36,37,38),(39,40,41)]):
    x=24+k*270
    put(s,24,a,x,322,26,15,font='SansB')
    put(s,24,b,x+33,322,220,9.8,font='SansB')
    put(s,24,c,x+33,342,220,9.1,leading=11.4)
put(s,24,42,24,379,794,7.2)
image_fit(s,1,12,24,396,391,155)
image_fit(s,1,18,427,396,391,155)
put(s,24,32,24,562,794,7.3)

# Content audit: only cover furniture and the superseded contents index are removed.
exempt={(1,i) for i in range(len(src['slides'][0]['objects'])) if i not in [8,12,18]}
exempt.update({(2,22),(2,23)})
missing=[]
for p,ss in enumerate(src['slides'],1):
    for i,o in enumerate(ss['objects']):
        if i<8 or o['kind'] not in ['text','image','chart']:continue
        if (p,i) not in used and (p,i) not in exempt:missing.append((p,i,o.get('text',o['kind'])))
assert not missing, missing
assert len(slides)==15
texts=[o['text'] for s in slides for o in s['objects'] if o['kind']=='text']
paras=[p for sec in M['sections'] for p in sec['english']]
assert all(p in texts for p in paras)
out=dict(lang='EN',width=W,height=H,slides=slides)
(B/'tight15_layout_EN.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
audit=dict(slides=15,manuscript_paragraphs=len(paras),paragraphs_preserved=sum(p in texts for p in paras),
           missing_substantive_objects=missing,layout_fit=log,
           chart_slides=[n for n,s in enumerate(slides,1) if any(o['kind']=='chart' for o in s['objects'])],
           approved_removals='Separate cover furniture and previous reading index; duplicate table headings consolidated.')
(B/'tight15_content_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(audit,indent=2))
