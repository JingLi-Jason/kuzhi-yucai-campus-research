from pathlib import Path
import json, math, csv
import pymupdf as fitz
import numpy as np
import shapefile
from shapely.geometry import shape
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.font_manager import FontProperties
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image,ImageOps

ROOT=Path(__file__).parent
OUT=ROOT/'论文与作品集'
WORK=OUT/'工作文件'
ASSET=OUT/'图表与图纸'
ASSET.mkdir(exist_ok=True)
DRAW=Path(r'${ORIGINAL_USER_HOME}\Documents\xwechat_files\wxid_mytycr68cje021_def2\temp\RWTemp\2026-10\5b0e20a984f82b1ea73ccae4d8aabd46')
PAPER='#F3F1EA'; INK='#252D2C'; GREEN='#81968A'; TEAL='#345A60'; CLAY='#B68168'
plt.rcParams.update({'font.family':'Arial','font.size':10,'text.color':INK,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,
                     'axes.edgecolor':'#BBBEB7','pdf.fonttype':42,'svg.fonttype':'none'})
zhfont=FontProperties(fname=r'C:\Windows\Fonts\msyh.ttc')
def save(fig,name):
    fig.savefig(ASSET/(name+'.pdf'),bbox_inches='tight',pad_inches=.08,transparent=True)
    fig.savefig(ASSET/(name+'.png'),dpi=220,bbox_inches='tight',pad_inches=.08,transparent=True)
    plt.close(fig)

# Geographical context uses actual user-provided geometry.
gis=WORK/'map_unpacked'/'commondata'/'gis文件'
geo={}
for name in ['cun','场地','道路','范围']:
    r=shapefile.Reader(str(gis/(name+'.shp')),encoding='utf-8')
    geo[name]=[shape(s.__geo_interface__) for s in r.shapes()]
site=geo['场地'][0]
metrics={'site_area_m2':site.area,'site_area_ha':site.area/10000,'crs':'EPSG:32649','settlement_features':len(geo['cun'])}
(WORK/'gis_metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
for lang in ['EN','ZH']:
    fp={} if lang=='EN' else {'fontproperties':zhfont}
    fig,ax=plt.subplots(figsize=(8,5.1))
    for name,color,edge in [('cun','#D5D7D0','#BDC3BB'),('道路','#FFFFFF','#A3ADA3'),('场地','#C3D0BE',TEAL)]:
        for geom in geo[name]:
            for g in (list(geom.geoms) if geom.geom_type=='MultiPolygon' else [geom]):
                ax.add_patch(Polygon(np.array(g.exterior.coords),facecolor=color,edgecolor=edge,lw=.6 if name!='场地' else 1.6))
    ax.set_xlim(652760,653530); ax.set_ylim(2857080,2857735); ax.set_aspect('equal'); ax.axis('off')
    x,y=site.representative_point().coords[0]
    ax.text(x,y,'SITE\n2.94 ha' if lang=='EN' else '场地\n2.94公顷',ha='center',va='center',fontsize=11,color=TEAL,**fp)
    ax.annotate('N',xy=(653470,2857670),xytext=(653470,2857580),ha='center',va='center',arrowprops=dict(arrowstyle='-|>',color=INK),fontsize=12)
    ax.plot([652800,652900],[2857120,2857120],color=INK,lw=2)
    for sx in [652800,652850,652900]: ax.plot([sx,sx],[2857116,2857124],color=INK,lw=.8)
    ax.text(652800,2857090,'0',fontsize=8)
    ax.text(652900,2857090,'100 m',ha='right',fontsize=8)
    save(fig,'context_'+lang)

for lang in ['EN','ZH']:
    fp={} if lang=='EN' else {'fontproperties':zhfont}
    labels=['Classroom','Funding','Teaching building','Playground','School clinic','Toilet','Play','Space'] if lang=='EN' else ['教室','资金','教学楼','操场','校医室','厕所','玩耍','空间']
    nums=[7,5,4,3,2,2,2,2]
    fig,ax=plt.subplots(figsize=(7.8,2.1))
    ax.barh(range(8),nums,color=[TEAL,CLAY,GREEN,GREEN,'#BBC7BC','#BBC7BC','#BBC7BC','#BBC7BC'],height=.62)
    ax.set_yticks(range(8),labels,**fp); ax.invert_yaxis(); ax.set_xlim(0,8.2)
    ax.set_xticks(range(0,9,2));ax.xaxis.grid(True,alpha=.18);ax.set_axisbelow(True)
    for i,n in enumerate(nums): ax.text(n+.12,i,str(n),va='center',fontsize=9)
    for sp in ax.spines.values():sp.set_visible(False)
    ax.tick_params(axis='both',length=0,labelsize=9)
    fig.subplots_adjust(left=.19,right=.98,bottom=.12,top=.98)
    save(fig,'keywords_'+lang)

    labels=['Basic safety','Comfort','Activity support','Care support','Spatial connections'] if lang=='EN' else ['基础安全','舒适性','活动支持','照护支持','空间联结']
    vals=[3.75,31/9,19/7,23/6,3]
    fig,ax=plt.subplots(figsize=(7.8,2.0))
    ax.barh(range(5),vals,color=[GREEN,GREEN,CLAY,TEAL,GREEN],height=.54)
    ax.set_yticks(range(5),labels,**fp);ax.invert_yaxis();ax.set_xlim(0,5);ax.set_xticks(range(6))
    for i,v in enumerate(vals):ax.text(v+.07,i,f'{v:.2f}',va='center',fontsize=10)
    ax.grid(axis='x',alpha=.18);ax.set_axisbelow(True)
    for sp in ax.spines.values():sp.set_visible(False)
    ax.tick_params(length=0)
    fig.subplots_adjust(left=.23,right=.98,bottom=.15,top=.98)
    save(fig,'audit_'+lang)

    labels=['Study','Meals','Activity','Midday rest','Eye exercises','Intervals'] if lang=='EN' else ['学习','就餐','活动','午休','眼保健操','间隙']
    nums=[390,160,90,80,30,120]
    colors=[TEAL,GREEN,CLAY,'#ABBBA8','#D5BFA4','#D9DDD4']
    fig,ax=plt.subplots(figsize=(9,1.45));left=0
    for n,c in zip(nums,colors):
        ax.barh(0,n,left=left,height=.34,color=c)
        if n>=80: ax.text(left+n/2,0,str(n),ha='center',va='center',color='white' if c in [TEAL,GREEN,CLAY] else INK,fontsize=10)
        left+=n
    ax.set_xlim(0,870);ax.set_ylim(-.45,.48);ax.axis('off')
    for i,(lab,n,c) in enumerate(zip(labels,nums,colors)):
        xx=(i%3)*.34; yy=-.10-(i//3)*.25
        ax.text(xx,yy,f'●  {lab}  {n} min',transform=ax.transAxes,color=c if i<3 else INK,fontsize=9,**fp)
    save(fig,'time_'+lang)

# Keep source PDF linework as vectors; replace outlined Chinese room names by numbered keys.
src=fitz.open(DRAW/'建筑平立剖.pdf')
sc=1191/1888
def rect(x,y,w=50,h=17):
    return fitz.Rect((x-w/2)*sc,(y-h/2)*sc,(x+w/2)*sc,(y+h/2)*sc)
common=[(617,280),(1236,330),(843,860),(1236,996),(903,759),(903,805),
        (1082,901),(1235,901),(1397,901)]
stairs=[(813,218),(837,218),(1483,274),(1508,274),(936,700),(936,724),(1483,933),(1508,933),(539,1188),(539,1212)]
plans=[]
for i in range(4):
    p=src[i]
    if i==0:
        labels=common+[(567,186),(925,234),(1082,234),(1200,234),(1277,234),(1356,234),(1433,234),(928,519),
                       (515,768),(488,986),(610,986),(518,1158)]
    else:
        labels=common+[(484,186),(542,186),(601,186),(657,186),(922,222),(1082,234),(1235,234),(1397,234),
                       (903,418),(903,496),(903,550),(903,607),(903,659)]
        if i==1:labels += [(515,767),(486,986),(634,986),(515,1137)]
        if i==2:labels += [(558,762),(558,896),(558,1071)]
    for x,y in labels: p.draw_rect(rect(x,y),color=None,fill=(1,1,1),overlay=True)
    for x,y in stairs:p.draw_rect(rect(x,y,11,13),color=None,fill=(1,1,1),overlay=True)
    # Program tints, lightly overlaid so the original geometry stays visible.
    color_learning=tuple(int(GREEN[k:k+2],16)/255 for k in (1,3,5))
    color_care=tuple(int(CLAY[k:k+2],16)/255 for k in (1,3,5))
    color_shared=tuple(int(TEAL[k:k+2],16)/255 for k in (1,3,5))
    for rr,col in [((1008,832,1465,954),color_learning),((457,122,683,239),color_care if i else color_shared),
                   ((856,369,946,674),color_care if i else color_shared)]:
        p.draw_rect(fitz.Rect(*[v*sc for v in rr]),color=None,fill=col,fill_opacity=.13)
    if i>0:p.draw_rect(fitz.Rect(*[v*sc for v in (1008,178,1465,295)]),color=None,fill=color_learning,fill_opacity=.13)
    if i<3:p.draw_rect(fitz.Rect(*[v*sc for v in (460,708,706,1170)]),color=None,fill=color_shared,fill_opacity=.09)
    # Numbered program markers; one common key on all four plans.
    marks=[(1082,899,'01'),(1235,899,'01'),(1397,899,'01'),(743,204,'04'),(885,958,'04'),(925,234,'07')]
    if i==0:marks +=[(567,186,'06'),(1082,234,'08'),(1200,234,'09'),(1277,234,'09'),(1356,234,'03'),(1433,234,'03'),(602,985,'05')]
    else:
        marks +=[(484,186,'02'),(542,186,'02'),(601,186,'02'),(657,186,'02'),(903,548,'03'),
                  (1082,234,'01'),(1235,234,'01'),(1397,234,'01')]
        if i==1:marks +=[(604,980,'05')]
        if i==2:marks +=[(558,762,'10'),(558,896,'10'),(558,1071,'10')]
    for x,y,t in marks:
        p.draw_circle((x*sc,y*sc),9,color=None,fill=(1,1,1))
        p.insert_text((x*sc-6.7,y*sc+4),t,fontsize=12,fontname='hebo',color=(.19,.32,.33))
    plans.append([275,62,969,785])
src.save(ASSET/'Architectural_drawings_keyed.pdf',garbage=4,deflate=True)
src.close()
src=fitz.open(DRAW/'建筑平立剖.pdf')
# Bounds for original elevations and sections, removing sheet borders.
bounds=[]
for i,p in enumerate(src):
    if i<4:bounds.append(plans[i]);continue
    dd=[]
    for d in p.get_drawings():
        r=d['rect']
        if r.width>.88*p.rect.width or r.height>.88*p.rect.height:continue
        if r.x0<8 or r.x1>p.rect.width-8 or r.y0<8 or r.y1>p.rect.height-8:continue
        dd.append(r)
    union=fitz.Rect(dd[0])
    for r in dd[1:]:union|=r
    union+=(-8,-8,8,8)
    bounds.append(list(union))
(WORK/'drawing_bounds.json').write_text(json.dumps(bounds),encoding='utf-8')

sitepdf=fitz.open(DRAW/'总平面图.pdf');p=sitepdf[0];ss=p.rect.width/1800
original_paths=p.get_drawings()
mask_rects=[]
for x,y in [(836,746),(902,700),(904,755),(956,776),(893,830),(1090,778),(998,865)]:
    rr=fitz.Rect((x-34)*ss,(y-29)*ss,(x+34)*ss,(y+29)*ss)
    mask_rects.append(rr)
    p.draw_rect(rr,fill=(1,1,1),color=None)
# Restore architectural edges crossing the label masks. Chinese glyph strokes
# are much smaller than the continuous wall, roof and ground outlines.
for d in original_paths:
    if max(d['rect'].width,d['rect'].height)<16*ss:continue
    if not any(d['rect'].intersects(rr) for rr in mask_rects):continue
    sh=p.new_shape()
    for item in d['items']:
        if item[0]=='l':sh.draw_line(item[1],item[2])
        elif item[0]=='c':sh.draw_bezier(*item[1:])
        elif item[0]=='re':sh.draw_rect(item[1])
        elif item[0]=='qu':sh.draw_quad(item[1])
    sh.finish(width=d.get('width',.2),color=d.get('color'),fill=d.get('fill'),
              closePath=d.get('closePath',False),lineCap=max(d.get('lineCap',(0,0,0))),
              lineJoin=d.get('lineJoin',0),dashes=d.get('dashes'),even_odd=d.get('even_odd',False))
    sh.commit()
for x,y,n in [(835,746,'01'),(902,700,'01'),(950,779,'01'),(895,830,'02'),(1020,660,'03'),(1090,778,'04'),(998,865,'05')]:
    p.draw_circle((x*ss,y*ss),12*ss,fill=(1,1,1),color=None)
    p.insert_text((x*ss-8,y*ss+5),n,fontsize=14,fontname='hebo',color=(.2,.35,.37))
sitepdf.save(ASSET/'Site_plan_keyed.pdf',garbage=4,deflate=True)

# Architectural collage: PDF clipping preserves the source building pixels.
# The original site's roads, sports fields and fences fall outside the clipping path.
renders=[
dict(name='Aerial',file=r'${ORIGINAL_USER_HOME}\AppData\Local\Temp\codex-clipboard-3a7ac352-41a5-4321-bc6a-770916403593.png',
 poly=[(410,145),(459,104),(616,130),(944,197),(937,223),(922,231),(902,376),(878,370),(879,414),(828,633),(409,518),(387,449),(303,583),(136,540),(136,450),(133,438),(318,271),(353,280),(368,249),(415,261)],
 hole=[(641,330),(654,317),(899,373),(882,412),(629,352)],bounds=(128,98,952,642)),
dict(name='Arrival',file=r'${ORIGINAL_USER_HOME}\AppData\Local\Temp\codex-clipboard-2a5719c0-8231-4434-967d-fd28e7631377.jpg',
 poly=[(58,756),(73,747),(72,670),(354,603),(632,640),(618,574),(817,510),(1495,443),(1638,490),(1650,486),(1733,537),(1730,550),(1718,558),(1715,577),(1740,567),(1879,623),(1878,635),(1864,640),(1866,835),(1905,843),(1905,854),(1871,854),(1871,914),(1837,925),(1807,925),(1768,940),(1711,963),(1712,983),(1664,991),(633,960),(357,967),(59,952)],
 hole=None,bounds=(50,434,1909,1000)),
dict(name='Courtyard',file=r'${ORIGINAL_USER_HOME}\AppData\Local\Temp\codex-clipboard-c2be6ea8-9d49-4f4b-9b55-a063328cc074.jpg',
 poly=[(107,418),(461,325),(897,477),(997,463),(982,429),(1115,377),(1602,317),(1750,357),(1777,401),(1909,377),(1909,1108),(1488,1090),(1489,991),(999,984),(900,966),(804,986),(605,1014),(543,1025),(134,1014),(134,877),(123,872),(124,857),(136,857),(136,494),(124,493),(124,484),(134,480),(134,436),(107,430)],
 hole=None,bounds=(96,307,1910,1115)),
]
W,H=1400,950
c=canvas.Canvas(str(ASSET/'Architectural_collages.pdf'),pagesize=(W,H))
for r in renders:
    c.setFillColor(HexColor(PAPER));c.rect(0,0,W,H,fill=1,stroke=0)
    # Restrained diagrammatic ground, explicitly an editorial collage.
    c.setFillColor(HexColor('#E5E8DE'))
    g=c.beginPath();g.moveTo(85,170);g.lineTo(1130,110);g.lineTo(1360,410);g.lineTo(530,570);g.close()
    c.drawPath(g,fill=1,stroke=0)
    b=r['bounds'];width=b[2]-b[0];height=b[3]-b[1]
    scale=min(1240/width,720/height)
    px=(W-width*scale)/2;py=155+(720-height*scale)/2
    def pt(v):return px+(v[0]-b[0])*scale,py+(b[3]-v[1])*scale
    c.saveState()
    path=c.beginPath()
    for j,v in enumerate(r['poly']):
        (path.moveTo if j==0 else path.lineTo)(*pt(v))
    path.close()
    if r['hole']:
        for j,v in enumerate(r['hole']):(path.moveTo if j==0 else path.lineTo)(*pt(v))
        path.close()
    c.clipPath(path,stroke=0,fill=0,fillMode=0)
    im=Image.open(r['file'])
    c.drawImage(r['file'],px-b[0]*scale,py+(b[3]-im.height)*scale,width=im.width*scale,height=im.height*scale)
    c.setFillColor(HexColor(PAPER));c.setFillAlpha(.09);c.rect(0,0,W,H,fill=1,stroke=0)
    c.restoreState()
    if r['hole']:
        c.setFillColor(HexColor('#E5E8DE'))
        hp=c.beginPath()
        for j,v in enumerate(r['hole']):(hp.moveTo if j==0 else hp.lineTo)(*pt(v))
        hp.close()
        c.drawPath(hp,fill=1,stroke=0)
    c.showPage()
c.save()
d=fitz.open(ASSET/'Architectural_collages.pdf')
for i,r in enumerate(renders):
    d[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(ASSET/(r['name']+'_collage.png'))

# Source photo assets are unchanged; contact sheet for editorial selection.
photos=ROOT/'材料整理'/'照片'
chosen={}
for num in [3680,3691,3712,3703]:
    files=list(photos.rglob(f'IMG_{num}.JPG'))
    if files:chosen[str(num)]=str(files[0])
(WORK/'photos_selected.json').write_text(json.dumps(chosen,ensure_ascii=False,indent=2),encoding='utf-8')
print('Assets prepared',metrics, 'photos',len(chosen))
