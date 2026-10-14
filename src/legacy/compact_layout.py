from pathlib import Path
import json,copy,math,re
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from shapely.geometry import shape

ROOT=Path(__file__).parent
D=ROOT/'论文与作品集/工作文件/ppt_build'
for name,file in [('Arial','arial.ttf'),('ArialB','arialbd.ttf'),('Yahei','msyh.ttc'),('YaheiB','msyhbd.ttc')]:
    pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
INK='#252D2C';TEAL='#345A60';GREEN='#81968A';MUTED='#65736D';LINE='#CCD1C7'
W=841.8898;H=595.2756
report={}

for lang in ['EN','ZH']:
    old=json.loads((D/f'layout_{lang}.json').read_text('utf8'))
    ss=old['slides'];z=lang=='ZH';slides=[];used=set()
    def tr(en,zh):return zh if z else en
    def add(s,o):s['objects'].append(o);return o
    def tx(s,text,x,y,w,size=10,bold=False,color=INK,leading=None):
        leading=leading or size*1.3
        font=('YaheiB' if bold else 'Yahei') if z else ('ArialB' if bold else 'Arial')
        p=Paragraph(escape(text).replace('\n','<br/>'),ParagraphStyle('p',fontName=font,fontSize=size,leading=leading,wordWrap='CJK' if z else None))
        h=p.wrap(w-3,2000)[1]+3
        return add(s,dict(kind='text',text=text,x=x,y=y,w=w,h=h,size=size,font=('CNB' if bold else 'CN') if z else ('SansB' if bold else 'Sans'),leading=leading,color=color,source='paragraph'))
    def ln(s,x,y,x1,y1,color=LINE,width=.6):
        return add(s,dict(kind='line',points=[[x,y],[x1,y1]],color=color,width=width,dash=None))
    def new(title,part='RESEARCH'):
        s={'title':title,'bg':'#FFFFFF','objects':[]};slides.append(s)
        tx(s,'KUZHI YUCAI',30,18,100,8,True,TEAL)
        tx(s,tr('GUIYANG COUNTY / HUNAN / CHINA','中国 · 湖南 · 郴州 · 桂阳'),137,18,380,7.5,color=MUTED)
        tx(s,part,684,18,130,7.5,color=MUTED)
        ln(s,30,39,812,39)
        tx(s,title,30,49,782,21,True)
        ln(s,30,563,812,563)
        tx(s,tr('EVERYDAY CARE, SPATIAL CHOICE','日常照顾与空间选择'),30,573,670,7.2,color=MUTED)
        tx(s,f'{len(slides):02}',784,570,28,10,color=TEAL)
        return s
    def obj(n,i):used.add((n,i));return copy.deepcopy(ss[n-1]['objects'][i])
    def texts(n,lo=100,hi=560):
        return [(i,o) for i,o in enumerate(ss[n-1]['objects']) if o['kind']=='text' and lo<=o['y']<hi]
    def body(n):return [(i,o) for i,o in texts(n,100,360) if o['source']=='paragraph']
    def use_text(s,n,i,x,y,w,size=9.4,bold=False,color=INK):
        o=obj(n,i);return tx(s,o['text'],x,y,w,size,bold,color)
    def imagefit(s,o,x,y,w,h):
        q=copy.deepcopy(o);sc=min(w/o['w'],h/o['h']);q.update(x=x+(w-o['w']*sc)/2,y=y+(h-o['h']*sc)/2,w=o['w']*sc,h=o['h']*sc);add(s,q)
    def images(n):return [(i,o) for i,o in enumerate(ss[n-1]['objects']) if o['kind']=='image']
    def cap(s,n,x,y,w=782,size=7.4):
        for i,o in texts(n,530,555):use_text(s,n,i,x,y,w,size)
    def pair(a,b,title):
        s=new(title)
        for n,x in [(a,30),(b,430)]:
            tx(s,ss[n-1]['title'],x,87,382,11,True,TEAL)
            y=120
            # Use the full paper text, with paragraph spacing rather than fixed figure gaps.
            for i,o in body(n):
                t=use_text(s,n,i,x,y,382,(9.1 if a==11 else 9.3) if not z else 11.7)
                y+=t['h']+5
            print(lang,'pair',n,'ends',round(y))
        ln(s,416,88,416,545)
        return s
    def triplet(s,n,y,size=9.0):
        items=[(i,o) for i,o in texts(n,380,525)]
        for k in range(3):
            x=30+k*266
            for j,(i,o) in enumerate(items[k*3:k*3+3]):
                use_text(s,n,i,x+(0 if j==0 else 35),y+(0 if j<2 else 22),230 if j else 29,size if j else 15,j<2,TEAL if j<2 else INK)
    def retain(n):
        s=copy.deepcopy(ss[n-1]);slides.append(s)
        for i,o in enumerate(s['objects']):
            used.add((n,i))
            if o['kind']=='text' and 563<=o['y']<580 and o['x']>750:o['text']=f'{len(slides):02}'
        return s

    # 01: two former introductory pages become one complete visual introduction.
    s=new(tr('Everyday Care, Spatial Choice','日常照顾与空间选择'),'RESEARCH + DESIGN')
    for i in [7,8]:used.add((1,i))
    use_text(s,1,9,30,100,295,14,True)
    use_text(s,1,12,30,194,285,13)
    use_text(s,1,13,30,253,295,8.5,color=TEAL)
    use_text(s,1,14,30,272,295,8)
    imagefit(s,obj(1,10),331,84,488,329)
    use_text(s,17,1,30,327,300,21,True)
    use_text(s,17,2,30,354,300,21,True)
    use_text(s,17,3,30,399,285,11)
    use_text(s,17,5,30,477,285,9,True,TEAL)
    use_text(s,17,6,30,500,285,10)
    imagefit(s,obj(17,4),372,377,405,170)
    used.add((17,0))

    # 02: abstract and research framework; contents tightened into a small index.
    s=new(tr('Research overview & questions','研究概览与研究问题'))
    y=94
    for i,o in texts(2,110,515):
        if o['x']<420:
            t=use_text(s,2,i,30,y,386,10.3 if not z else 12.5);y+=t['h']+8
    tx(s,tr('ANALYTICAL FRAMEWORK','分析框架'),449,95,360,10,True,TEAL)
    its=texts(3,380,525)
    for k in range(3):
        for j,(i,o) in enumerate(its[k*3:k*3+3]):
            use_text(s,3,i,449 if j==0 else 487,127+k*84+(24 if j==2 else 0),30 if j==0 else 320,17 if j==0 else 10.2,j<2,TEAL if j<2 else INK)
    cap(s,3,449,382,360,7.3)
    tx(s,tr('READING THE PROJECT','项目阅读顺序'),449,413,350,9,True,TEAL)
    tx(s,tr('I   Field research  /  03–11\nII  Evidence & sources  /  11–13\nIII Design portfolio  /  14–24','I   实地研究 / 03–11\nII  证据与资料 / 11–13\nIII 设计作品集 / 14–24'),449,435,350,10)
    use_text(s,2,22,449,500,360,8.8)
    use_text(s,2,23,30,542,782,7.4)
    for i,o in texts(2,110,515):
        if 11<=i<=21:used.add((2,i))

    pair(3,4,tr('Context & research methods','研究背景与资料方法'))
    # 04: new native, editable technical route, with original inventory preserved.
    s=new(tr('Research methodology','研究技术路线'))
    tx(s,tr('Research question: how can everyday care become a spatial design brief?','研究问题：怎样把日常照顾的需求转化为空间设计？'),30,89,782,12,True,TEAL)
    inv=texts(4,380,525)
    for k in range(6):
        x=30+k*132
        use_text(s,4,inv[k*2][0],x,122,118,22,True,TEAL)
        use_text(s,4,inv[k*2+1][0],x,151,118,9)
    cap(s,4,30,181,782)
    stages=[
        ('01','Collect & locate','资料收集与定位',
         'Questionnaires, audit, observation, photographs and interview recordings; timetable, KML route and GIS; plans, elevations and sections.',
         '整理问卷、环境审计、观察、照片及访谈录音；汇合作息表、KML轨迹、GIS，以及平面、立面和剖面。'),
        ('02','Clean & organize','清理与归类',
         'Keep completed answers; remove question wording. Compile 20 answers / 460 Chinese characters. Consolidate overlapping audio passages and retain original audit wording.',
         '保留已填写答案，删除题干；形成20条答案、460个汉字的文本。合并录音中的重叠段落，保留审计原题含义。'),
        ('03','Describe & compare','描述与比较',
         'Count exact terms; compare respondent accounts; tabulate audit scores; read activity against the timetable; map the site and surrounding settlement.',
         '统计关键词，比较受访者表述；汇总审计分数；结合作息阅读活动变化，绘制场地与周边聚落关系。'),
        ('04','Cross-check needs','综合判断需求',
         'Compare text, scores, photographs and observed use. Identify sanitation, small-group choice, nearby adult support and operating needs.',
         '对照文字、分数、照片与使用观察，识别卫生设施、小组活动、邻近成人支持及运行方面的需求。'),
        ('05','Translate & review','设计转化与回访',
         'Develop adjacency, circulation, shared rooms and phased improvements. Proposed review: repeat observations and short conversations after implementation.',
         '转化为功能邻接、交通组织、共享空间和分期改善。后续拟通过重复观察和简短交流，检查建成后的使用情况。')]
    for k,(num,en,zh,ee,zz) in enumerate(stages):
        y=213+k*65
        tx(s,num,30,y,37,20,True,TEAL)
        tx(s,tr(en,zh),84,y,180,11,True)
        tx(s,tr(ee,zz),273,y,536,10)
        if k<4:
            ln(s,47,y+29,47,y+58,GREEN,1.2)
            ln(s,43,y+54,47,y+58,GREEN,1.2);ln(s,51,y+54,47,y+58,GREEN,1.2)
        ln(s,83,y+53,812,y+53)
    s['notes']='Methodology constructed from supplied field sources. Review after implementation is proposed, not an observed outcome.'

    pair(5,6,tr('Questionnaire findings & environmental audit','问卷发现与环境审计'))
    # 06: all three editable charts together, with original figure text.
    s=new(tr('Patterns in words, scores & daily time','词频、环境评分与每日时间'))
    for n,x,kind in [(5,30,'keywords'),(6,430,'audit')]:
        tx(s,tr('Keyword occurrences' if n==5 else 'Environmental audit: raw means','关键词出现次数' if n==5 else '环境审计：原始均值'),x,88,380,12,True,TEAL)
        add(s,dict(kind='chart',chart=kind,x=x,y=116,w=382,h=167))
        for i,o in enumerate(ss[n-1]['objects']):
            if o['kind']=='chart':used.add((n,i))
        yy=287
        for i,o in texts(n,380,525):
            t=use_text(s,n,i,x,yy,382,8.7,False,INK);yy+=t['h']+2
        cap(s,n,x,364,382,7.3)
    add(s,dict(kind='chart',chart='time',x=30,y=376,w=782,h=99))
    for i,o in enumerate(ss[6]['objects']):
        if o['kind']=='chart':used.add((7,i))
    cap(s,7,30,476,782,7.3)
    triplet(s,8,500,8.5)
    cap(s,8,30,548,782,7.2)
    pair(7,8,tr('Daily rhythms & continuing care','每日节奏与持续照顾'))
    pair(9,10,tr('Site relationships & design priorities','场地关系与设计重点'))
    # Design translation figure appears at bottom of this paired paper page.
    s=slides[-1]
    its=texts(10,380,525)
    for k in range(4):
        for j,(i,o) in enumerate(its[k*3:k*3+3]):
            use_text(s,10,i,30+k*198,491+(0 if j==0 else 19 if j==1 else 35),189,9, j==0,TEAL if j==0 else INK)
    cap(s,10,30,544,782,7.2)

    # 09: regional location, real parcel position and original local GIS map.
    s=new(tr('Location | Hunan · Chenzhou · Guiyang','项目区位 | 湖南 · 郴州 · 桂阳'))
    hn=json.loads((D/'maps/430000.json').read_text('utf8'))['features']
    cz=json.loads((D/'maps/431000.json').read_text('utf8'))['features']
    gy=[f for f in cz if f['properties']['adcode']==431021]
    def locator(features,highlight,rect,point=False):
        x,y,w,h=rect;geoms=[shape(f['geometry']).simplify(.006) for f in features]
        bounds=[g.bounds for g in geoms];x0=min(b[0] for b in bounds);y0=min(b[1] for b in bounds);x1=max(b[2] for b in bounds);y1=max(b[3] for b in bounds)
        correction=math.cos(math.radians((y0+y1)/2));sc=min(w/((x1-x0)*correction),h/(y1-y0))
        ox=x+(w-(x1-x0)*correction*sc)/2;oy=y+(h-(y1-y0)*sc)/2
        def project(a,b):return [ox+(a-x0)*correction*sc,oy+(y1-b)*sc]
        for f,g in zip(features,geoms):
            for p in list(g.geoms) if g.geom_type=='MultiPolygon' else [g]:
                add(s,dict(kind='polygon',points=[project(a,b) for a,b in p.exterior.coords],color=GREEN if f['properties']['adcode']==highlight else '#EEF1EF',stroke='#65736D',width=.5))
        if point:
            px,py=project(112.52795170697533,25.826756708463357)
            add(s,dict(kind='ellipse',x=px-3,y=py-3,w=6,h=6,color=TEAL))
            ln(s,px,py,px+23,py-18,TEAL,1)
            tx(s,tr('School','学校'),px+24,py-27,80,9,True,TEAL)
    for x,title in [(30,tr('01 HUNAN / CHENZHOU','01 湖南省 / 郴州市')),(287,tr('02 CHENZHOU / GUIYANG','02 郴州市 / 桂阳县')),(552,tr('03 GUIYANG / SCHOOL','03 桂阳县 / 学校'))]:
        tx(s,title,x,89,253,10,True,TEAL)
    locator(hn,431000,(30,117,235,177))
    locator(cz,431021,(290,117,238,177))
    locator(gy,431021,(552,117,250,177),True)
    tx(s,tr('Regional boundaries: Alibaba Cloud DataV GeoAtlas. School marker: centroid of the supplied GIS site polygon (112.52795°E, 25.82676°N).','区域边界：阿里云DataV GeoAtlas。学校点位：所提供GIS场地面的质心（东经112.52795°，北纬25.82676°）。'),30,303,782,7.5)
    ln(s,30,328,812,328)
    im=images(18)[0];imagefit(s,obj(18,im[0]),30,342,390,204)
    yy=342
    for i,o in texts(18,110,525):
        # Preserve all local-map annotation as a compact legend and description.
        if o['text'] in ['2.94','HECTARES','公顷']:continue
        islegend=o['text'] in ['Mapped site','Settlement fabric','Road surfaces','场地范围','聚落肌理','道路面','场地','周边建筑','道路']
        t=use_text(s,18,i,459 if islegend else 443,yy,351 if islegend else 367,9.4,False)
        if islegend:
            color=GREEN if 'site' in o['text'].lower() or '场地' in o['text'] else '#D5D7D0' if 'Settlement' in o['text'] or '聚落' in o['text'] else '#CCD1C7'
            add(s,dict(kind='rect',x=443,y=yy+3,w=9,h=7,color=color))
        yy+=t['h']+3
    tx(s,tr('2.94 ha · mapped parcel','2.94 公顷 · 图层场地面积'),443,330,367,11,True,TEAL)
    for i,o in texts(18,110,220):used.add((18,i))
    # Original regional distances and map-area text.
    yy=490
    for i,o in texts(9,380,525):
        if o['x']>500:use_text(s,9,i,635,456,176,8.6)
        else:used.add((9,i))
    cap(s,18,30,545,390,6.8);cap(s,9,443,535,368,6.8)
    for i,o in images(9):used.add((9,i)) # same supplied GIS map repeated, retained as larger original map above
    s['notes']='Regional boundaries: https://geo.datav.aliyun.com/areas_v3/bound/430000_full.json and https://geo.datav.aliyun.com/areas_v3/bound/431000_full.json; retrieved 2026-10-12. Provincial and municipal locator maps show administrative context; site centroid from supplied EPSG:32649 GIS transformed to WGS84. Local map from supplied GIS. Regional map panels use separate scales.'

    s=pair(11,12,tr('Architectural organization & implementation','建筑组织与实施安排'))
    its=texts(11,380,525)
    for k in range(4):
        for j,(i,o) in enumerate(its[k*2:k*2+2]):
            use_text(s,11,i,30+k*198,497 if j==0 else 515,190,10 if j==0 else 8.8,j==0,TEAL if j==0 else INK)
    cap(s,11,30,545,782,7.2)

    s=new(tr('Conclusion & sources','结论与资料来源'))
    y=89
    for i,o in body(13):
        t=use_text(s,13,i,30,y,375,9.8 if not z else 10.7);y+=t['h']+6
    im=images(13)[0];imagefit(s,obj(13,im[0]),30,414,375,107)
    cap(s,13,30,532,375,7.1)
    y=90
    ref_prefix=''
    for i,o in texts(14,100,530):
        if o['text'] in ['[1]','[2]','F1','F2','D1']:
            ref_prefix=o['text']+'  '
            continue
        use=obj(14,i)
        t=tx(s,ref_prefix+use['text'],434,y,378,9.4,o['source']=='single',TEAL if o['source']=='single' else INK);y+=t['h']+7
        ref_prefix=''
    for i,o in texts(14,100,530):
        if o['text'] in ['[1]','[2]','F1','F2','D1']:used.add((14,i))
    cap(s,14,434,547,378,7)
    print(lang,'references end',y)

    retain(15);retain(16)
    for n in [19,20,21,22,23,24,25,26,27,28]:
        retain(n)
    s=retain(29)
    # Tighten implementation table to make room for the complete former phasing diagram.
    for o in s['objects']:
        if o['kind']=='line':
            o['points']=[[x,110+(y-110)*.74] if 110<=y<=530 else [x,y] for x,y in o['points']]
        elif 110<=o.get('y',-1)<530:
            o['y']=110+(o['y']-110)*.74
    triplet(s,12,444,8.5)
    cap(s,12,30,503,782,7.2)
    # Track every original substantive text except reusable page furniture / contents references.
    missing=[]
    for n,sl in enumerate(ss,1):
        for i,o in enumerate(sl['objects']):
            if o['kind']=='text' and 100<=o['y']<560 and (n,i) not in used:
                if n==1 and i==8:continue
                missing.append((n,i,o['text']))
    # Content carried by exact reproduction, updated contents or explicit same-map consolidation.
    report[lang]={'slides':len(slides),'unassigned_text':missing}
    out=dict(old,slides=slides)
    (D/f'compact_layout_{lang}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),'utf8')
(D/'compact_content_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
