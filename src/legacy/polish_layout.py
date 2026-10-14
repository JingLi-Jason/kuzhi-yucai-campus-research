from pathlib import Path
import json,copy,re
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT=Path(__file__).parent
B=ROOT/'论文与作品集/工作文件/ppt_build'
WORK=B.parent
old=json.loads((WORK/'manuscript.json').read_text('utf8'))
new=json.loads((WORK/'manuscript_publication.json').read_text('utf8'))
for n,f in [('Sans','arial.ttf'),('SansB','arialbd.ttf'),('CN','msyh.ttc'),('CNB','msyhbd.ttc'),('Serif','georgia.ttf')]:
    pdfmetrics.registerFont(TTFont(n,'C:/Windows/Fonts/'+f))
TEAL='#345A60';INK='#252D2C';MUTED='#65736D'
proof={}
for lang in ['EN','ZH']:
    z=lang=='ZH';pk='chinese' if z else 'english';lk='zh' if z else 'en'
    d=json.loads((B/f'compact_layout_{lang}.json').read_text('utf8'))
    ss=d['slides']
    def tr(en,zh):return zh if z else en
    def resize(o,size=None,w=None):
        if size:o['size']=size;o['leading']=size*1.3
        if w:o['w']=w
        p=Paragraph(escape(o['text']).replace('\n','<br/>'),ParagraphStyle('p',fontName=o['font'],fontSize=o['size'],leading=o['leading'],wordWrap='CJK' if z else None))
        o['h']=p.wrap(o['w']-3,3000)[1]+3
        return o
    def settext(page,index,en,zh,size=None):
        o=ss[page-1]['objects'][index]
        o['text']=tr(en,zh)
        if size:resize(o,size)
        else:resize(o)
        return o
    def title(page,en,zh):
        s=ss[page-1];s['title']=tr(en,zh)
        ts=[o for o in s['objects'] if o['kind']=='text' and 40<o['y']<85]
        ts[0]['text']=tr(en,zh);resize(ts[0])
    def remove(page,indices):
        for i in indices:ss[page-1]['objects'][i]['drop']=True
    mapping={}
    for a,b in zip(old['sections'],new['sections']):
        mapping.update(zip(a[pk],b[pk]));mapping[a[lk]]=b[lk]
    for s in ss:
        for o in s['objects']:
            if o['kind']=='text' and o['text'] in mapping:
                o['text']=mapping[o['text']];resize(o)
        s['notes']=tr('Kuzhi Yucai Public Welfare School. Field survey and interviews, September 2026. Campus design. References: Barrett et al. (2015); Adams et al. (2009).',
                      '苦志育才公益学校。2026年9月实地调研与访谈；校园设计。参考文献：Barrett等（2015）；Adams等（2009）。')
    # Reflow each full manuscript column within the established compact layout.
    for page,a,b,limit in [(3,1,2,543),(5,3,4,543),(7,5,6,543),(8,7,8,479),(10,9,10,485)]:
        s=ss[page-1]
        for sec,x in [(a,30),(b,430)]:
            obs=[o for o in s['objects'] if o['kind']=='text' and o['text'] in new['sections'][sec][pk]]
            size=11.7 if z else 9.3
            def place():
                y=120
                for o in obs:
                    o['x']=x;o['y']=y;resize(o,size,382);y+=o['h']+6
                return y
            end=place()
            while end>limit and size>(10.4 if z else 9):
                size-=.1;end=place()
            assert end<=limit,(lang,page,sec,end)
    for page,section,x,y,w,maxy,base in [(2,0,30,94,386,520,12.5 if z else 10.3),(11,11,30,89,375,405,11.5 if z else 10)]:
        obs=[o for o in ss[page-1]['objects'] if o['kind']=='text' and o['text'] in new['sections'][section][pk]]
        size=base
        while True:
            yy=y
            for o in obs:o.update(x=x,y=yy);resize(o,size,w);yy+=o['h']+8
            if yy<=maxy:break
            size-=.1
    title(3,'School life & research methods','学校生活与调研方法')
    title(5,'Questionnaire findings & environmental assessment','问卷发现与环境评价')
    title(7,'Daily rhythms & care','日常节奏与照顾')
    title(8,'Site relationships & design priorities','场地关系与设计重点')
    settext(2,21,'Figure 1. Everyday access, nearby support, and a choice of activity settings.','图1  日常到达、邻近支持与活动选择。')
    remove(2,[25]) # manuscript word counts are editorial metadata

    # Methodology describes the research work rather than an inventory of files or people.
    sourceheads=[('Voice','需求','Questionnaires','问卷反馈'),('Place','环境','Environmental audit','环境审计'),
                 ('Use','活动','Activity observation','活动观察'),('Scene','现场','Site photography','现场摄影'),
                 ('Care','照顾','Interviews','学校访谈'),('Space','空间','Mapping and drawings','测绘与建筑设计')]
    for k,(a,b,c,e) in enumerate(sourceheads):
        settext(4,9+2*k,a,b,16);settext(4,10+2*k,c,e,9)
    settext(4,21,'Figure 2. Research methods and their connection to campus design.','图2  调研方法及其与校园设计的联系。')
    settext(4,24,'Document everyday needs through questionnaires, interviews, environmental assessment, activity observation, photography, and site mapping.',
                    '通过问卷、访谈、环境审计、活动观察、摄影与场地测绘，了解校园日常需求。')
    settext(4,30,'Organize themes','整理主题')
    settext(4,31,'Group feedback by place, activity, and resources; organize observations and interviews around daily use and school operations.',
                    '按场所、活动与资源整理反馈，围绕日常使用和学校运行归纳观察与访谈。')
    settext(4,38,'Count recurring words; compare priorities, environmental scores, and daily activity patterns; examine the site and its surroundings.',
                    '统计反复出现的关键词，对照需求重点、环境评分与每日活动变化，分析校园及周边关系。')
    settext(4,44,'Identify priorities','确定重点')
    settext(4,45,'Connect questionnaire themes with observed use: sanitation, small-group activity, nearby adult support, and manageable shared spaces.',
                    '结合问卷主题与使用观察，明确卫生设施、小组活动、邻近成人支持及共享空间的改善重点。')
    settext(4,51,'Design and follow up','设计与回访')
    settext(4,52,'Develop room relationships, circulation, shared spaces, and phased improvements; follow use through observation and conversations with pupils and staff.',
                    '落实功能联系、交通组织、共享空间和分期改善，再通过观察及师生交流了解使用情况。')

    settext(6,10,'RECURRING THEMES','反复出现的主题')
    settext(6,12,'Learning spaces, outdoor activity, and the resources that keep them in use.','学习空间、户外活动，以及维持使用所需的资源。')
    settext(6,13,'Figure 3. Keyword occurrences in questionnaire feedback.','图3  问卷反馈中的关键词出现次数。')
    settext(6,14,'Environmental audit: domain means','环境审计：维度均值')
    settext(6,19,'Figure 4. Mean scores across five environmental domains (1–5).','图4  五个环境维度的评分均值（1—5分）。')
    settext(6,21,'Figure 5. Time allocated to daily activities, 06:30–21:00 (minutes).','图5  6:30至21:00各类日常活动的时间分配，单位：分钟。')
    settext(6,31,'Figure 6. Continuing resources, familiar adults, and organized activities support everyday care.','图6  持续资源、熟悉的成人和稳定活动共同支持日常照顾。')
    # Accurate geographical attribution is retained without data-processing commentary.
    settext(9,43,'Regional boundaries: Alibaba Cloud DataV GeoAtlas. Location: Guiyang County, Chenzhou, Hunan.',
                    '行政区划底图：阿里云DataV GeoAtlas。项目位于湖南省郴州市桂阳县。')
    settext(9,47,'The school sits among local roads and dispersed village buildings. A clear entrance connects this setting with the compact teaching and shared-activity areas.',
                    '学校周边分布着地方道路与村落建筑，清楚的校园入口将外部环境与紧凑的教学、共享活动区域相连接。')
    settext(9,46,'A rural school within a dispersed village landscape.','分散村落环境中的乡村校园。')
    for o in ss[8]['objects']:
        if o['kind']=='text' and ('2.94 ha ·' in o['text'] or '2.94 公顷 ·' in o['text']):
            o['text']=tr('2.94 ha · campus site','2.94 公顷 · 校园用地');resize(o)
        if o['kind']=='text' and o['text']=='Mapped site':o['text']='Campus site'
    settext(9,56,'Campus boundary, village buildings, and local roads.','校园边界、村落建筑与地方道路。')
    settext(9,57,'Figure 7. Regional location and links to nearby services.','图7  区域位置及周边服务联系。')
    ss[8]['notes']='Regional administrative boundaries: Alibaba Cloud DataV GeoAtlas, https://geo.datav.aliyun.com/areas_v3/bound/430000_full.json and https://geo.datav.aliyun.com/areas_v3/bound/431000_full.json. Campus location and local map: site survey GIS. Retrieved 2026-10-12.'

    # Replace captions about how drawings were processed with descriptions of architecture.
    captions={
        (8,None):('Figure 8. Sanitation, activity, care, and resources translated into spatial priorities.','图8  卫生、活动、照顾与资源需求对应的空间重点。'),
        (10,None):('Figure 9. Activities and support across the four levels.','图9  四个楼层的活动与支持功能。'),
        (11,12):('Figure 11. Entrance elevation and the rhythm of sheltered circulation.','图11  入口立面与有顶通道的连续节奏。'),
        (12,67):('Questionnaire feedback organized by theme.','按主题整理的问卷反馈。'),
        (13,137):('Environmental assessment across safety, comfort, activity, care, and spatial connections. Scores: 1–5.','基础安全、舒适性、活动支持、照护支持与空间联结的环境评价。评分：1—5分。'),
        (14,28):('Existing school spaces and the design priorities they inform.','现有校园空间与相应的设计重点。'),
        (15,20):('Masterplan: connected teaching wings, shared facilities, sports grounds, and open space.','总平面：连贯的教学翼部、共享设施、运动场与开敞空间。'),
        (16,28):('Ground floor: arrival, reception, learning, and dining.','首层：到达、接待、学习与餐饮。'),
        (17,24):('Level 2: teaching spaces connected to staff offices and care facilities.','二层：教学空间与教师办公、照护设施相联系。'),
        (18,14):('Levels 3 and 4: learning, shared activities, and the lower roof terrace.','三层与四层：教学、共享活动与高低翼部之间的屋面关系。'),
        (19,28):('Care and activity along daily routes','日常路径中的照顾与活动'),
        (19,42):('Washing, adult contact, and small-group activity placed near teaching and shared circulation.','洗手、成人支持和小组活动邻近教学区域与共享通道。'),
        (20,16):('Elevations: pitched roofs, repeated bays, and sheltered thresholds.','立面：坡屋顶、重复开间与有遮蔽的门前空间。'),
        (21,15):('Sections through the shared wing and the main teaching wing.','共享翼部与主要教学翼部的剖面。'),
        (22,13):('Courtyard perspective: connected wings frame a shared outdoor setting.','庭院透视：相连的建筑翼部围合共享户外场所。'),
        (23,21):('Pale walls, gray roofs, vertical screens, and planting define the campus character.','浅色墙面、灰色屋顶、竖向格栅与绿化共同构成校园形象。'),
        (24,42):('Figure 10. Immediate improvements, regular activities, and coordinated campus development.','图10  日常改善、稳定活动与整体校园建设的实施顺序。')
    }
    for (page,index),(en,zh) in captions.items():
        if index is None:
            for o in ss[page-1]['objects']:
                if o['kind']=='text' and 540<=o['y']<560:o['text']=tr(en,zh);resize(o)
        else:settext(page,index,en,zh)
    # Three distinct sources, stated as references rather than an explanation to the author.
    for index,code in [(17,'F1'),(18,'F2'),(19,'D1')]:
        rr=next(r for r in new['references'] if r['id']==code)
        ss[10]['objects'][index]['text']=code+'  '+rr[lk]
        resize(ss[10]['objects'][index],9.4)
    settext(11,15,'Research perspectives','研究视角')
    settext(11,16,'Classroom flexibility and ownership [1]; accessible sanitation, privacy, and maintenance [2].',
                     '教室的灵活性与归属感[1]；卫生设施的便利到达、隐私与维护[2]。')
    remove(11,[20,21,22])
    y=90
    for i in range(13,20):
        o=ss[10]['objects'][i];o['y']=y;resize(o,9.4);y+=o['h']+12
    title(11,'Conclusion & references','结论与参考资料')
    title(12,'Appendix A / Questionnaire feedback','附录A / 问卷反馈')
    for o in ss[11]['objects']:
        if o['kind']=='text':
            if re.match(r'R1',o['text']):o['text']=tr('FEEDBACK A','反馈摘录A')
            elif re.match(r'R2',o['text']):o['text']=tr('FEEDBACK B','反馈摘录B')
            resize(o)
    settext(12,42,'Playground and forecourt: play and conversation with visitors','操场与楼前场地：玩耍、与来访者交流')
    settext(13,37,'Do monitoring and supervision cover key areas?','监控与管理是否覆盖关键区域')
    settext(13,96,'Does the setting suit children of different ages?','场所是否适合不同年龄的儿童')
    settext(13,110,'Is there space for counseling or private conversation?','是否有心理交流或安静交谈的空间')
    settext(13,121,'Is school–family communication supported?','是否有家校沟通的渠道')
    settext(13,131,'Is there space for visiting community or charity services?','是否有接待乡镇或公益服务的空间')
    settext(13,135,'Can community members use school resources?','学校资源是否可以向社区开放')
    # Replace residual coaching phrases with the design's own decisions.
    settext(16,27,'Reception has an adjacent waiting place, clear access to washing, and small-group activity beside shared circulation.',
                     '接待旁设置等候位置，保持通往洗手点的路径清楚，并在共享通道旁安排小组活动。')
    settext(17,23,'A calm waiting place sits beside the support suite; movable furniture allows shared classrooms to accommodate different activities.',
                     '支持空间旁设置安静等候，可移动家具帮助共享教室容纳不同活动。')
    settext(21,14,'The teaching wing connects rooms vertically through a regular sequence of floors, stairs, and shared circulation.',
                     '教学翼部通过连续的楼层、楼梯与共享通道，将各层房间联系起来。')
    settext(22,12,'Courtyard settings\nA quiet edge / a small-group table / an open center / nearby adult support',
                     '庭院活动\n安静边缘 / 小组桌椅 / 开敞中心 / 邻近成人支持')
    # A roof is a roof: no new use is assigned in the portfolio.
    settext(18,14,'Levels 3 and 4: learning, shared activities, and the roof over the lower wing.','三层与四层：教学、共享活动与较低翼部的屋面。')
    for page in [16,17]:
        for o in ss[page-1]['objects']:
            if o['kind']=='text' and o['text']=='Offices in the spine':o['text']='Offices in the connecting block'
    for o in ss[12]['objects']:
        if o['kind']=='text' and o['text'] in ['ITEM / ORIGINAL QUESTION WORDING','项目 / 原始题意']:
            o['text']=tr('ASSESSMENT ITEM','评价项目')
    settext(24,32,'Follow-up observations and conversations with pupils and staff guide adjustments to daily use.','通过使用观察与师生交流，持续调整空间的日常安排。')
    # Clean all image accessibility labels and retain only audience-facing notes.
    for s in ss:
        s['objects']=[o for o in s['objects'] if not o.get('drop')]
        for o in s['objects']:
            if o['kind']=='image':o['alt']=tr('Campus drawing or field photograph','校园图纸或现场照片')
            if o['kind']=='text':
                o['text']=o['text'].replace('raw means','domain means').replace('Raw mean','Domain mean')
    texts='\n'.join(o['text'] for s in ss for o in s['objects'] if o['kind']=='text')
    banned=r'supplied|user.provided|KML|486|119\.9|460|two adult|two questionnaire|both respondent|both accounts|twenty answers|20 answers|原始文件|所提供|提供的|用户提供|两份问卷|两位受访|两份成人|不计入|未经|并非|而非|仅用于|not a validated|not measured|not fixed|not counted|rather than measured'
    hits=[(i+1,o['text']) for i,s in enumerate(ss) for o in s['objects'] if o['kind']=='text' and re.search(banned,o['text'],re.I)]
    assert not hits,hits
    norm=lambda t:re.sub(r'\s+','',t)
    assert all(norm(p) in norm(texts) for sec in new['sections'] for p in sec[pk])
    proof[lang]={'slides':len(ss),'manuscript_paragraphs':sum(len(sec[pk]) for sec in new['sections']),'wording_scan':hits}
    (B/f'publication_layout_{lang}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
(B/'publication_wording_check.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),'utf8')
print(json.dumps(proof,ensure_ascii=False))
