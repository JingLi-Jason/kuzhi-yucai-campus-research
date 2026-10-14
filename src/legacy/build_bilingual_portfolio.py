from pathlib import Path
import json,csv,math,re,zipfile,shutil
import pymupdf as fitz
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
from PIL import Image,ImageOps,ImageDraw
from xml.sax.saxutils import escape

ROOT=Path(__file__).parent
OUT=ROOT/'论文与作品集'
WORK=OUT/'工作文件'; ASSET=OUT/'图表与图纸'
DATA=json.loads((WORK/'manuscript.json').read_text(encoding='utf-8'))
BOUNDS=json.loads((WORK/'drawing_bounds.json').read_text())
PHOTOS=json.loads((WORK/'photos_selected.json').read_text(encoding='utf-8'))
W,H=841.8898,595.2756
INK='#252D2C'; MUTED='#65736D'; PAPER='#F3F1EA'; GREEN='#81968A'; TEAL='#345A60'; CLAY='#B68168'; LINE='#CCD1C7'
FONTS=Path('C:/Windows/Fonts')
for n,f in [('Sans','arial.ttf'),('SansB','arialbd.ttf'),('Serif','georgia.ttf'),('SerifI','georgiai.ttf'),('CN','msyh.ttc'),('CNB','msyhbd.ttc')]:
    pdfmetrics.registerFont(TTFont(n,str(FONTS/f),subfontIndex=0))
SOURCES={'draw':ASSET/'Architectural_drawings_keyed.pdf','site':ASSET/'Site_plan_keyed.pdf'}

class Book:
    def __init__(self,lang):
        self.lang=lang;self.z=lang=='ZH'
        self.font='CN' if self.z else 'Sans';self.bold='CNB' if self.z else 'SansB'
        self.body='CN' if self.z else 'Serif'
        self.temp=WORK/f'layout_{lang}.pdf'
        self.c=canvas.Canvas(str(self.temp),pagesize=(W,H))
        self.c.setTitle(DATA['title_zh' if self.z else 'title_en'])
        self.c.setAuthor('Student field research and campus design')
        self.c.setSubject('Guiyang County Kuzhi Yucai Public Welfare School')
        self.p=0;self.inserts=[];self.inventory=[];self.heights=[]
    def t(self,en,zh):return zh if self.z else en
    def text(self,text,x,y,size=10,font=None,color=INK):
        self.c.setFont(font or self.font,size);self.c.setFillColor(HexColor(color));self.c.drawString(x,H-y-size*.83,text)
    def para(self,text,x,y,w,size=10.3,leading=None,font=None,color=INK,maxh=None):
        st=ParagraphStyle('p',fontName=font or self.font,fontSize=size,leading=leading or size*1.45,
                          textColor=HexColor(color),wordWrap='CJK' if self.z else None,alignment=TA_LEFT,spaceAfter=0)
        pp=Paragraph(escape(text).replace('\n','<br/>'),st);aw,ah=pp.wrap(w,1000)
        if maxh and ah>maxh+.5:raise ValueError(f'{self.lang} p{self.p}: text overflow {ah}>{maxh} {text[:70]}')
        pp.drawOn(self.c,x,H-y-ah);return ah
    def rule(self,x,y,w,color=LINE):
        self.c.setStrokeColor(HexColor(color));self.c.setLineWidth(.55);self.c.line(x,H-y,x+w,H-y)
    def rect(self,x,y,w,h,color):
        self.c.setFillColor(HexColor(color));self.c.rect(x,H-y-h,w,h,stroke=0,fill=1)
    def dot(self,x,y,r=4,color=TEAL):
        self.c.setFillColor(HexColor(color));self.c.circle(x,H-y,r,fill=1,stroke=0)
    def line(self,points,color=TEAL,width=1.2,dash=None):
        self.c.saveState();self.c.setStrokeColor(HexColor(color));self.c.setLineWidth(width)
        if dash:self.c.setDash(dash)
        p=self.c.beginPath();p.moveTo(points[0][0],H-points[0][1])
        for x,y in points[1:]:p.lineTo(x,H-y)
        self.c.drawPath(p);self.c.restoreState()
    def image(self,path,x,y,w,h,cover=False):
        im=ImageOps.exif_transpose(Image.open(path));iw,ih=im.size
        if cover:
            crop=ImageOps.fit(im,(int(w*3),int(h*3)),method=Image.Resampling.LANCZOS)
            self.c.drawImage(ImageReader(crop),x,H-y-h,width=w,height=h,mask='auto')
        else:
            s=min(w/iw,h/ih);ww,hh=iw*s,ih*s
            self.c.drawImage(ImageReader(im),x+(w-ww)/2,H-y-h+(h-hh)/2,width=ww,height=hh,mask='auto')
    def pdf(self,path,pno,rect,clip=None):
        self.inserts.append(dict(page=self.p-1,path=str(path),pno=pno,rect=rect,clip=clip))
    def start(self,title,part='PAPER',bg=PAPER,number=None):
        if self.p:self.c.showPage()
        self.p+=1;self.inventory.append(title)
        self.rect(0,0,W,H,bg)
        self.text('KUZHI YUCAI',38,23,8,self.bold,TEAL)
        self.text(self.t('GUIYANG COUNTY / HUNAN / CHINA','中国 · 湖南 · 桂阳'),137,23,7.2,color=MUTED)
        self.text(self.t(part,{'PAPER':'研究论文','PORTFOLIO':'设计作品集','APPENDIX':'数据附录','REFERENCES':'参考资料'}.get(part,part)),655,23,7.3,self.bold)
        self.rule(38,43,766)
        self.text(title,38,62,23 if not self.z else 22,self.bold)
        self.rule(38,555,766)
        self.text(self.t('EVERYDAY CARE, SPATIAL CHOICE','日常照顾与空间选择'),38,568,7.3,color=MUTED)
        self.text(f'{self.p:02d}',782,565,10,self.bold,TEAL)
    def caption(self,en,zh,x=38,y=534,w=760):
        self.para(self.t(en,zh),x,y,w,7.6,10,color=MUTED,maxh=22)
    def smalltitle(self,en,zh,x,y):
        self.text(self.t(en,zh),x,y,9.5,self.bold,TEAL)
    def diagram3(self,items,y=410,h=115):
        for i,(num,en,zh,be,bz) in enumerate(items):
            x=38+i*260
            self.text(num,x,y,25,self.bold,GREEN if i!=1 else CLAY)
            self.smalltitle(en,zh,x+46,y+3)
            self.para(self.t(be,bz),x+46,y+25,196,9.3,13.6,maxh=h-28)
            if i<2:self.rule(x,y+h-5,232)
    def paper_figure(self,kind):
        y=393
        if kind=='framework':
            self.diagram3([
                ('01','Reach essentials','到达所需','Teaching, toilets and washing connected by familiar routes.','通过熟悉的路线连接教学、厕所和洗手点。'),
                ('02','Find support','找到支持','Reception, waiting and adult help located close to daily life.','接待、等候和成人帮助靠近日常生活。'),
                ('03','Choose a setting','选择场所','Large-group play, small groups and quiet moments each have a place.','集体活动、小组交流和安静时刻各有去处。')],y)
            self.caption('Figure 1. Analytical framework developed from the field material.','图1  由现场材料形成的分析框架。')
        elif kind=='methods':
            nums=[('02','Adult questionnaires','成人问卷'),('35','Audit items','审计项目'),('08','Observation entries','观察记录'),
                  ('111','Photographs','现场照片'),('03','Audio files','录音文件'),('19','Drawing sheets','设计图纸')]
            for i,(n,en,zh) in enumerate(nums):
                x=38+i*129
                self.text(n,x,y+10,32,self.bold,TEAL)
                self.para(self.t(en,zh),x,y+57,117,9.2,13)
            self.caption('Figure 2. Source inventory. Audio files overlap; the questionnaires contain adult accounts.','图2  资料构成。录音存在重叠；问卷记录的是成人观察。')
        elif kind=='keywords':
            self.pdf(ASSET/f'keywords_{self.lang}.pdf',0,[38,385,535,527])
            self.smalltitle('SHARED ACROSS BOTH ACCOUNTS','两份问卷共同提及',560,397)
            self.para(self.t('Classroom / funding / teaching building / playground.','教室 / 资金 / 教学楼 / 操场。'),560,422,240,10,15)
            self.para(self.t('Counts refer to Chinese answer text; English labels are translations.','按中文答案计数；英文标签为对应译名。'),560,472,240,9,13,color=MUTED)
            self.caption('Figure 3. Selected exact-term occurrences in 20 answers, after excluding question wording. Source: F1.','图3  删除题干后，20条答案中的选定关键词出现次数。资料：F1。')
        elif kind=='audit':
            self.pdf(ASSET/f'audit_{self.lang}.pdf',0,[38,389,541,526])
            self.text('10 / 35',576,401,30,self.bold,CLAY)
            self.para(self.t('items marked 1 or 2','项目标为1分或2分'),576,442,222,10.5,15)
            self.para(self.t('28.6% of all recorded items','占全部记录项目的28.6%'),576,474,222,9.5,14,color=MUTED)
            self.caption('Figure 4. Raw domain means on the original 1-5 form; item wording is retained in Appendix B. Source: F1.','图4  原表1至5分的各维度原始均值，具体题意见附录B。资料：F1。')
        elif kind=='time':
            self.pdf(ASSET/f'time_{self.lang}.pdf',0,[40,393,800,527])
            self.caption('Figure 5. Scheduled minutes within the 06:30-21:00 day (870 min). Intervals are time between listed activities.','图5  6:30至21:00内的作息分钟数，共870分钟；间隙指表列活动之间的时间。')
        elif kind=='care':
            self.diagram3([
                ('01','Continuing support','持续支持','Monthly giving and reliable everyday resources.','持续月捐，以及可靠的日常资源。'),
                ('02','A familiar adult','熟悉的成人','Companionship, teacher learning and a clear contact.','陪伴、教师学习与明确的联系人。'),
                ('03','Rooms in use','真正使用的房间','A weekly program, storage and someone to lead it.','每周活动、储物与负责带领的人。')],y)
            self.caption('Figure 6. Interview themes translated into operating requirements. Source: F2; themes are paraphrased.','图6  访谈主题与运行需求的联系。资料：F2；采用主题归纳。')
        elif kind=='site':
            self.pdf(ASSET/f'context_{self.lang}.pdf',0,[38,382,285,529])
            self.text('2.94 ha',328,401,33,self.bold,TEAL)
            self.para(self.t('Mapped site area','图层场地面积'),330,445,185,10,14)
            self.para(self.t('35 km / county center\n3.5 km / town or transport\n4 km / health clinic',
                                '约35公里 / 县城\n约3.5公里 / 镇区或公交\n约4公里 / 卫生院'),562,408,236,10,19)
            self.caption('Figure 7. Parcel area calculated from the map layer; external distances are field-record estimates. Sources: F1, D1.','图7  场地面积由地图图层计算；外部联系距离为现场记录估计值。资料：F1、D1。')
        elif kind=='translation':
            items=[
                ('Sanitation','卫生设施','Short routes + washing','短路径与洗手点'),
                ('Small-group activity','小组活动','Movable settings','可调整的活动场所'),
                ('Emotional support','情绪支持','Nearby help + privacy','邻近帮助与隐私'),
                ('Funding and staffing','资金与人员','Phased, shared use','分期改善与共享使用')]
            for i,(a,b,cc,d) in enumerate(items):
                x=38+i*195;self.rule(x,y+9,170,GREEN)
                self.para(self.t(a,b),x,y+23,175,10,self.font=='CN' and 16 or 14,font=self.bold)
                self.text('↓',x,y+55,16,self.font,CLAY)
                self.para(self.t(cc,d),x,y+80,177,10,15)
            self.caption('Figure 8. Evidence-to-design relationships developed in this study.','图8  本研究建立的证据与设计回应关系。')
        elif kind=='program':
            levels=[('L4','Learning + support','教学与支持'),('L3','Learning + shared activities','教学与共享活动'),
                    ('L2','Learning + care + dining','教学、照顾与餐饮'),('L1','Arrival + learning + dining','到达、教学与餐饮')]
            for i,(l,en,zh) in enumerate(levels):
                yy=392+i*31;self.text(l,40,yy+4,12,self.bold,TEAL)
                self.rect(86,yy+3,242,17,[GREEN,GREEN,GREEN,CLAY][i])
                self.para(self.t(en,zh),353,yy+3,438,10,14)
            self.caption('Figure 9. Program reading of the supplied plans. The lower shared wing ends below Level 4. Source: D1.','图9  提供方案的功能解读；较低共享翼部在四层为屋面。资料：D1。')
        elif kind=='phasing':
            self.diagram3([
                ('01','Make daily use easier','先改善日常使用','Washing, surfaces, seats, waiting and simple storage.','洗手、地面、座位、等候与简便储物。'),
                ('02','Establish a routine','建立稳定活动','Match flexible rooms to people and a weekly schedule.','把灵活房间与人员、每周安排对应。'),
                ('03','Build the whole campus','形成完整校园','Coordinate buildings, landscape, access and maintenance.','协调建筑、景观、通行和维护。')],y)
            self.caption('Figure 10. Proposed implementation sequence; stages describe priorities, not fixed dates or budgets.','图10  建议的实施次序；阶段表示优先关系，不对应固定工期或预算。')
        elif kind=='conclusion':
            self.pdf(SOURCES['draw'],9,[38,377,804,524],BOUNDS[9])
            self.caption('Figure 11. Entrance elevation from the supplied proposal, presented as a vector drawing. Source: D1, sheet 10.','图11  提供方案的入口立面，保留矢量线稿。资料：D1，第10张。')
    def cover(self):
        self.start('',part='RESEARCH + DESIGN' if not self.z else '调研与设计')
        self.text(self.t('Everyday Care,','日常照顾'),38,85,43 if not self.z else 42,self.bold)
        self.text(self.t('Spatial Choice','空间选择'),38,137,43 if not self.z else 42,self.bold)
        self.para(DATA['subtitle_zh' if self.z else 'subtitle_en'],40,210,305,14,21,maxh=120)
        self.image(ASSET/'Aerial_collage.png',295,177,530,356)
        self.rule(40,393,178,TEAL)
        self.para(self.t('A school understood through its everyday life.','从日常生活理解一所学校。'),40,411,203,15,23)
        self.text(self.t('FIELDWORK  /  SEPTEMBER 2026','现场调研  /  2026年9月'),40,500,8.5,self.bold,TEAL)
        self.text(self.t('A4 LANDSCAPE EDITION  /  ENGLISH','A4横向版  /  中文'),40,519,8,color=MUTED)
    def abstract(self):
        self.start(self.t('Research overview','研究概览'))
        s=DATA['sections'][0];yy=114
        for p in s['chinese' if self.z else 'english']:
            hh=self.para(p,38,yy,363,11.4 if self.z else 10.7,18 if self.z else 15.6,self.body,maxh=390-(yy-114));yy+=hh+13
        self.smalltitle('READING THE PROJECT','阅读路径',449,117)
        self.rule(449,143,352)
        for yy,n,a,b,c in [(168,'I','Field research','现场研究','03-13'),(258,'II','Evidence & sources','资料与数据','14-16'),(348,'III','Design portfolio','设计作品集','17-29')]:
            self.text(n,449,yy,25,self.bold,GREEN)
            self.text(self.t(a,b),505,yy+3,15,self.bold)
            self.text(c,744,yy+5,11,color=MUTED)
        self.para(self.t('Keywords: school design; everyday care; activity settings; environmental audit; rural campus.',
                            '关键词：学校设计；日常照顾；活动场所；环境审计；乡村校园。'),449,451,350,10,16,color=MUTED)
        self.caption(f'Paper length: {DATA["word_count"]:,} English words, including the abstract and excluding references and captions.',
                     f'英文论文共{DATA["word_count"]:,}词，含摘要，不含参考资料和图注；本版为完整中文对应文本。')
    def paper(self):
        for s in DATA['sections'][1:]:
            self.start(s['zh' if self.z else 'en'])
            ps=s['chinese' if self.z else 'english'];split=2 if len(ps)==4 else 2
            for x,paras in [(38,ps[:split]),(439,ps[split:])]:
                y=111
                for pp in paras:
                    hh=self.para(pp,x,y,365,11.2 if self.z else 10.0,17.2 if self.z else 13.8,self.body,maxh=372-y)
                    y+=hh+13
                self.heights.append((self.p,y))
            self.rule(38,382,766)
            self.paper_figure(s['fig'])
    def references(self):
        self.start(self.t('References & field sources','参考文献与现场资料'),'REFERENCES')
        y=117
        for r in DATA['references'][:2]:
            self.text('['+r['id']+']',38,y,13,self.bold,TEAL)
            hh=self.para(r['zh' if self.z else 'en'],73,y,326,10,15)
            y+=hh+28
        self.smalltitle('HOW THE LITERATURE IS USED','文献与本研究的联系',38,360)
        self.para(self.t('Classroom research informs the attention to flexibility and ownership. School sanitation guidance informs access, handwashing and maintenance. Findings from those sources are not counted as results of the field study.',
                            '教室研究为灵活性与归属感的讨论提供参照；学校卫生设施指南用于理解可达、洗手和维护。本次现场研究的结果仍来自所提供的调研材料。'),38,386,365,10.5,16)
        y=117
        for r in DATA['references'][2:]:
            self.text(r['id'],439,y,14,self.bold,CLAY)
            hh=self.para(r['zh' if self.z else 'en'],480,y,320,10,15)
            y+=hh+28
        self.smalltitle('DRAWING AND IMAGE CREDITS','图纸与图像来源',439,391)
        self.para(self.t('Original plans and renderings: supplied project material. Analytical diagrams, translations, layouts and architectural collages: developed for this report. Reference board: page-format inspiration.',
                            '原始图纸与效果图：所提供的项目资料。分析图、译文、版式与建筑拼贴：为本报告整理制作。科研展板参考：用于页面组织参照。'),439,417,362,9.5,15)
        self.caption('Primary-source full texts were consulted for references [1] and [2].','参考文献[1]与[2]均查阅了原始全文。')
    def questionnaire(self):
        self.start(self.t('Appendix A / The two questionnaires','附录A / 两份问卷逐题对照'),'APPENDIX')
        rows=[
        ('Connection','了解来源','Work and charitable / volunteer contact','工作接触及公益、志愿活动','Work and charitable / volunteer contact','工作接触及公益、志愿活动'),
        ('Children served','服务儿童','Children without parental care or raised by grandparents','缺乏父母照顾、由祖辈抚养的孩子','Children with serious family difficulties; some with additional needs','家庭困难严重，部分有额外支持需求'),
        ('Beyond lessons','教学之外','Daily living and learning to get along with others','生活照顾与学习做人','Emotional support','情绪支持'),
        ('Frequent use','高频空间','Classrooms, dormitories and dining; classrooms most used','教室、宿舍和食堂；教室最多','Teaching-building area; classrooms','教学楼区域、教室'),
        ('Spatial issue','空间问题','An inconvenient toilet outside the teaching building','教学楼外的厕所不便','Idle classrooms and desks after junior-school suspension, linked to funding','初中暂时停办后空教室和桌椅闲置，认为与资金有关'),
        ('Enjoyed places','愿意停留','Playground and front apron: play and visitor interaction','操场及楼前坪：玩耍、与来访者互动','Large, open playground: freedom to play','宽大开敞的操场：自由玩耍'),
        ('Underused places','较少使用','Back area: soil and a small vegetable patch','后坪主要为土堆，仅小片菜地','None noticed; existing functions considered necessary','未发现；认为各项功能都有必要'),
        ('Three priorities','三项重点','Classroom quality; teachers; funding','教室质量、师资、资金','Funding; medical provision; playground','资金、医疗条件、操场'),
        ('First improvement','首选改善','More activity space, including the backyard','增加活动空间，包括利用后院','Clinic and reliable professional support','校医室与可靠的专业支持'),
        ('Main constraint','现实限制','Funding and unstable continuing donations','资金及长期捐助不稳定','Funding','资金')]
        self.rect(38,111,766,29,TEAL)
        for x,text in [(47,self.t('TOPIC','题目主题')),(208,'R1 / 2026-09-23'),(509,'R2 / 2026-09-26')]:
            self.text(text,x,120,9,self.bold,'#FFFFFF')
        y=141
        for i,(a,b,c,d,e,f) in enumerate(rows):
            if i%2==0:self.rect(38,y,766,35,'#E9ECE3')
            self.text(f'{i+1:02d}',47,y+9,8.5,self.bold,TEAL)
            self.para(self.t(a,b),69,y+7,125,8.6,11.6)
            self.para(self.t(c,d),208,y+5,280,8.5,11.5,maxh=34)
            self.para(self.t(e,f),509,y+5,283,8.5,11.5,maxh=34)
            self.rule(38,y+35,766)
            y+=35
        self.caption('Concise translations of all 20 answers. R1 visited frequently; R2 occasionally. Respondents are adults. Source: F1.',
                     '20条答案的完整逐题归纳。R1经常到访，R2偶尔到访；两位受访者均为成人。资料：F1。',y=512)
    def audit_appendix(self):
        self.start(self.t('Appendix B / Environmental audit','附录B / 环境审计全部项目'),'APPENDIX')
        english=[
        'Is the ground level?','Are there obvious level changes?','Are there sharp edges?','Do vehicles and pedestrians mix?',
        'Do stairs have handrails?','Is it slippery when it rains?','Is there lighting at night?','Do monitoring / management cover key areas?',
        'Is shade available?','Is rain shelter available?','Is there ventilation?','Are seats available?','Is drinking water available?',
        'Are handwashing facilities available?','Are waste bins available?','Are toilets available?','Are quiet areas available?',
        'Is open activity ground available?','Are small-group spaces available?','Is reading space available?',
        'Is there a place to be alone?','Is movable furniture available?','May children arrange or change the setting?',
        'Does it suit children of different ages?','Can adults see the children?','Can children quickly find adults?',
        'Is there waiting space?','Is there space for psychological / quiet conversation?','Is medical / temporary-rest space available?',
        'Are there blind spots in care coverage?','Is there an interface with families?','Is space shared with the community?',
        'Can external service staff enter easily?','Is there space for town / charity services?','Can school resources open to the community?',
        ]
        # Place the two positive and one problem-worded items in original CSV sequence.
        raw=list(csv.DictReader((ROOT/'研究报告交付'/'分析数据'/'环境审计全部项目.csv').open(encoding='utf-8-sig')))
        assert len(raw)==len(english)==35
        # Exact sequence follows raw data (including the safety section's eight items).
        for ci,items in enumerate([list(enumerate(raw))[:18],list(enumerate(raw))[18:]]):
            x=38+401*ci
            self.rect(x,111,365,28,TEAL)
            self.text(self.t('ITEM / ORIGINAL QUESTION WORDING','项目 / 原始题意'),x+8,120,8.2,self.bold,'#FFFFFF')
            self.text(self.t('SCORE','分数'),x+323,120,8,self.bold,'#FFFFFF')
            y=141
            for idx,row in items:
                if idx%2==0:self.rect(x,y,365,20.6,'#E9ECE3')
                self.text(f'{idx+1:02d}',x+6,y+6,7.2,self.bold,MUTED)
                en=english[idx] if idx<len(english) else ''
                self.para(row['项目'] if self.z else en,x+27,y+3,287,8 if self.z else 7.5,9.3,maxh=19)
                self.text(row['评分'],x+334,y+4,9,self.bold,CLAY if int(row['评分'])<=2 else TEAL)
                y+=20.6
        self.caption('35 original marks, 1-5. Mixed question direction is retained; raw means summarize the form rather than a validated scale.',
                     '保留35项原始1至5分标记及不同题目方向；均值用于描述记录表，而非经验证的量表。',y=527)
    def portfolio_divider(self):
        self.start('',part='PORTFOLIO',bg=TEAL)
        self.rect(0,0,W,H,TEAL)
        self.text('III',38,35,18,self.bold,'#CFDACE')
        self.text(self.t('A campus for','让校园支持'),38,91,43,self.bold,'#F3F1EA')
        self.text(self.t('everyday life.','每一天的生活。'),38,145,43,self.bold,'#F3F1EA')
        self.para(self.t('Connected learning. Familiar support. Room to choose.','相互连接的学习空间，熟悉的支持，以及选择的余地。'),40,226,550,14,21,color='#E0E8DD')
        self.image(ASSET/'Arrival_collage.png',278,308,527,211)
        self.text(self.t('DESIGN PORTFOLIO','设计作品集'),40,459,10,self.bold,'#D6E1D4')
        self.para(self.t('Kuzhi Yucai\nGuiyang County, Hunan','苦志育才公益学校\n湖南省桂阳县'),40,486,220,11,18,color='#D6E1D4')
        self.text('17',784,565,10,self.bold,'#D6E1D4')
    def site_context(self):
        self.start(self.t('01 / In its rural setting','01 / 置于乡村环境之中'),'PORTFOLIO')
        self.pdf(ASSET/f'context_{self.lang}.pdf',0,[28,104,566,527])
        self.text('2.94',588,120,50,self.bold,TEAL);self.text(self.t('HECTARES','公顷'),590,177,10,self.bold,MUTED)
        self.para(self.t('A mapped parcel within a dispersed settlement landscape.','一处位于分散聚落环境中的校园地块。'),590,215,209,15,22)
        self.para(self.t('The site boundary, surrounding built fabric and road surfaces are drawn from the supplied map package. The map establishes the setting for a compact, connected campus.',
                            '场地边界、周边建设肌理与道路面均来自提供的地图包，为紧凑、相互连接的校园确定环境背景。'),590,303,209,10,16)
        for yy,col,en,zh in [(427,'#C3D0BE','Mapped site','场地'),(449,'#D5D7D0','Settlement fabric','聚落肌理'),(471,'#FFFFFF','Road surfaces','道路面')]:
            self.rect(592,yy,14,8,col);self.text(self.t(en,zh),617,yy-1,9)
        self.caption('Map: supplied GIS layers, WGS 84 / UTM zone 49N. Area calculated from the site polygon. North and scale refer to this map.',
                     '地图：提供的GIS图层，WGS 84 / UTM 49N；面积由场地面计算。指北与比例尺对应本图。')
    def field_design(self):
        self.start(self.t('02 / From school life to a design brief','02 / 从学校生活到设计任务'),'PORTFOLIO')
        names=[('3680','Open ground','开敞场地'),('3691','Everyday corridor','日常走廊'),('3712','Sheltered connection','有顶联系'),('3703','A learning room','学习空间')]
        for i,(num,en,zh) in enumerate(names):
            x=38+(i%2)*194;y=112+(i//2)*202
            self.image(PHOTOS[num],x,y,182,154,cover=True)
            self.text(self.t(en,zh),x,y+165,9,self.bold)
        xx=456
        for y,n,en,zh,be,bz in [
            (113,'01','Use the edges','利用边缘','Small-group settings close to lessons.','把小组活动场所放在教室附近。'),
            (216,'02','Connect the essentials','连接必需设施','Pair toilets, washing and legible routes.','把厕所、洗手点和清晰路线一起安排。'),
            (319,'03','Keep care nearby','让照顾就在身边','Locate waiting and adult help along familiar paths.','沿熟悉的路线安排等候和成人支持。'),
            (422,'04','Plan for continued use','考虑持续使用','Give shared spaces a program and a responsible adult.','为共享空间安排活动和负责成人。')]:
            self.text(n,xx,y,22,self.bold,CLAY)
            self.text(self.t(en,zh),xx+47,y+2,13,self.bold)
            self.para(self.t(be,bz),xx+47,y+29,292,10,15)
        self.caption('Left: existing-school photographs from the field collection. Right: design priorities developed from the research.',
                     '左：调研照片中的现有学校。右：由研究形成的设计重点。')
    def masterplan(self):
        self.start(self.t('03 / A connected campus, open grounds','03 / 连贯校园与开敞场地'),'PORTFOLIO',bg='#FFFFFF')
        self.pdf(SOURCES['site'],0,[32,104,573,533],[900,560,1640,1390])
        self.para(self.t('Learning and shared life form one readable group.','让教学与共享生活形成清楚的整体。'),588,120,213,21,28)
        items=[
            ('01','Connected school wings','连体教学建筑'),
            ('02','Dining and shared activity','餐饮与共享活动'),
            ('03','Sports grounds and track','球场与跑道'),
            ('04','Table-tennis area','乒乓球活动区'),
            ('05','Flexible landscape reserve','弹性景观用地')]
        y=261
        for n,en,zh in items:
            self.text(n,589,y,12,self.bold,TEAL);self.para(self.t(en,zh),621,y,176,10,14)
            y+=40
        self.caption('Source: supplied site plan, cropped and re-keyed. Drawing orientation is retained; numbered uses follow the source plan.',
                     '来源：提供的总平面图，经裁切和编号整理。保留原图方向，功能编号对应原方案。')
    def plan_page(self,level):
        titles={0:('04 / Ground level: arrival and shared life','04 / 首层：到达与共享生活'),1:('05 / Level 2: learning with support nearby','05 / 二层：教学与邻近支持')}
        self.start(self.t(*titles[level]),'PORTFOLIO',bg='#FFFFFF')
        self.pdf(SOURCES['draw'],level,[29,101,533,522],BOUNDS[level])
        self.text('L1' if level==0 else 'L2',567,112,42,self.bold,TEAL)
        self.para(self.t('A public beginning to the school day.' if level==0 else 'Adult support within the learning network.',
                            '从公共空间开始学校的一天。' if level==0 else '把成人支持放进学习网络。'),568,172,229,18,25)
        if level==0:
            items=[('01','Multifunction classroom','多功能教室'),('03','Administration / archive','行政与档案'),('04','Toilets','厕所'),
                   ('05','Dining and catering wing','餐饮后勤翼部'),('06','Library','图书室'),('07','Entrance hall / connection','门厅与联系空间'),
                   ('08','School-history display','校史展示'),('09','Reception / discussion','接待与洽谈')]
            note=('Suggested development: define a waiting position near reception, keep the route to washing clear, and offer small-group activity beside the shared circulation.',
                  '深化建议：在接待附近明确等候位置，保持通往洗手点的路线清楚，并在共享通行空间旁设置小组活动。')
        else:
            items=[('01','Multifunction classroom','多功能教室'),('02','Rest, consultation and support','休息、咨询与支持'),
                   ('03','Offices in the spine','连接体中的办公室'),('04','Toilets','厕所'),('05','Dining and catering wing','餐饮后勤翼部'),
                   ('07','Activity / circulation junction','活动与通行节点')]
            note=('Suggested development: create a calm waiting place beside the support suite and test movable furniture in a shared classroom.',
                  '深化建议：在支持房间附近设置安静等候位置，并在共享教室试行可移动家具。')
        y=254
        for n,en,zh in items:
            self.text(n,570,y,10,self.bold,TEAL)
            self.para(self.t(en,zh),603,y,199,9.2,13)
            y+=24
        self.para(self.t(*note),568,464,231,9.3,14,maxh=64)
        self.caption(f'Source: building drawing sheet {level+1}. Numbered keys translate room programs; colored areas identify broad use groups.',
                     f'来源：建筑图第{level+1}张。编号整理房间功能，浅色区分主要用途。')
    def upper_plans(self):
        self.start(self.t('06 / Upper levels: continuity and variety','06 / 上部楼层：延续与变化'),'PORTFOLIO',bg='#FFFFFF')
        self.text('L3',38,112,25,self.bold,TEAL);self.text('L4',439,112,25,self.bold,TEAL)
        self.pdf(SOURCES['draw'],2,[38,151,405,482],BOUNDS[2])
        self.pdf(SOURCES['draw'],3,[439,151,806,482],BOUNDS[3])
        self.para(self.t('01 Learning  /  02 Support  /  03 Offices  /  04 Toilets\n10 Meeting and activity rooms in the lower wing',
                            '01 教学 / 02 支持 / 03 办公 / 04 厕所\n10 较低翼部中的会议与活动房间'),38,490,365,9.2,14)
        self.para(self.t('Learning and support continue in the main wings.\nThe lower wing is shown as a roof at this level.',
                            '主要翼部延续教学与支持功能。\n较低翼部在本层显示为屋面。'),439,490,365,9.2,14)
        self.caption('Source: building drawing sheets 3-4. Both plans use the same graphic scale on this page.',
                     '来源：建筑图第3至4张。本页两张平面采用相同的图面缩放比例。')
    def circulation(self):
        self.start(self.t('07 / Make the short journey work','07 / 让短距离通行更顺畅'),'PORTFOLIO')
        # An abstract topological diagram, deliberately separate from scaled plans.
        x,y=57,146
        self.rect(x,y,436,60,'#DBE2D7');self.rect(x,y+216,436,60,'#DBE2D7')
        self.rect(x+164,y+43,49,195,'#B6C8BA');self.rect(x,y+216,95,157,'#D8CBBB')
        self.rect(x+225,y+82,181,116,'#E5E8DE')
        self.text(self.t('LEARNING WING','教学翼部'),x+229,y+41,10,self.bold,TEAL)
        self.text(self.t('LEARNING WING','教学翼部'),x+229,y+262,10,self.bold,TEAL)
        self.para(self.t('SHARED\nACTIVITIES','共享\n活动'),x+13,y+294,82,10,16,font=self.bold)
        self.text(self.t('COURTYARD','庭院'),x+265,y+132,10,self.bold,MUTED)
        route=[(x+424,y+28),(x+190,y+28),(x+190,y+247),(x+420,y+247)]
        self.line(route,TEAL,2.3,dash=[4,3])
        for xx,yy,lab in [(x+150,y+28,'W'),(x+150,y+247,'W'),(x+190,y+129,'A'),(x+239,y+211,'S'),(x+210,y+80,'S')]:
            self.dot(xx,yy,12,CLAY if lab=='S' else TEAL)
            self.text(lab,xx-4,yy-5,10,self.bold,'#FFFFFF')
        self.para(self.t('Diagram of relationships / not to scale','关系示意 / 不按比例'),59,525,438,8,12,color=MUTED)
        self.para(self.t('Nearby choices make short breaks useful.','近处有选择，短课间才好用。'),548,126,247,22,30)
        items=[('W','Washing + toilets','洗手与厕所','A clear connection to teaching and activity.','与教学和活动建立清楚联系。'),
               ('A','Adult support','成人支持','An easy-to-find contact along everyday routes.','日常路线旁，容易找到的联系人。'),
               ('S','Small-group settings','小组场所','Seats and tables outside the main flow.','避开主要通行带的座位与桌面。')]
        for i,(n,a,b,cc,d) in enumerate(items):
            yy=255+i*85
            self.dot(562,yy+11,11,CLAY if n=='S' else TEAL)
            self.text(n,558,yy+6,9,self.bold,'#FFFFFF')
            self.smalltitle(a,b,584,yy)
            self.para(self.t(cc,d),584,yy+24,211,9.6,14)
        self.caption('Design-development diagram based on the connected-wing arrangement. Markers describe proposed relationships, not measured routes.',
                     '基于连体翼部关系的设计深化示意。标记表达建议的联系，而非实测路线。')
    def elevations(self):
        self.start(self.t('08 / A calm and consistent exterior','08 / 平静而统一的外部表达'),'PORTFOLIO',bg='#FFFFFF')
        self.pdf(SOURCES['draw'],4,[37,116,591,302],BOUNDS[4])
        self.pdf(SOURCES['draw'],9,[37,326,591,518],BOUNDS[9])
        self.text(self.t('Repeated bays','重复开间'),623,124,17,self.bold)
        self.para(self.t('A steady rhythm gives the long wings a recognizable order.','稳定的节奏让长翼部具有清楚的秩序。'),623,154,178,10,16)
        self.text(self.t('Deep thresholds','有厚度的边界'),623,259,17,self.bold)
        self.para(self.t('Open corridors and recessed faces mediate between rooms and shared ground.','开敞走廊与后退界面连接房间和共享场地。'),623,289,178,10,16)
        self.text(self.t('A limited palette','克制的材料组合'),623,391,17,self.bold)
        self.para(self.t('Pale walls, gray roofs and warm screens keep the building legible.','浅墙、灰瓦与暖色格栅共同形成清晰的建筑形象。'),623,423,178,10,16)
        self.caption('Sources: building drawing sheets 5 and 10. Original vector linework is preserved; each view is fitted to its panel.',
                     '来源：建筑图第5、10张。保留原始矢量线稿，各视图按版面分别缩放。')
    def sections(self):
        self.start(self.t('09 / Section: rooms, edges and shared air','09 / 剖面：房间、边界与开敞联系'),'PORTFOLIO',bg='#FFFFFF')
        self.pdf(SOURCES['draw'],15,[36,114,420,394],BOUNDS[15])
        self.pdf(SOURCES['draw'],17,[461,110,802,397],BOUNDS[17])
        self.rule(38,414,766)
        self.smalltitle('THE LOWER SHARED WING','较低的共享翼部',38,434)
        self.para(self.t('Three occupied levels connect dining and collective activities. The section clarifies the relationship between the entry, upper rooms and pitched roof.',
                            '三层使用空间联系餐饮与集体活动。剖面呈现入口、上部房间和坡屋顶之间的关系。'),38,460,356,10.2,16,maxh=70)
        self.smalltitle('THE FOUR-LEVEL LEARNING WING','四层教学翼部',439,434)
        self.para(self.t('Rooms and circulation repeat vertically. The design review should connect each level to support, sanitation and an understandable way through the building.',
                            '房间与通行空间沿竖向延续。深化时，应把各层与支持、卫生设施及清楚的通行方式联系起来。'),439,460,362,10.2,16,maxh=70)
        self.caption('Sources: building drawing sheets 16 and 18. Sectional reading of the shared wing and the main learning wing.',
                     '来源：建筑图第16、18张。本页为提供剖面的空间解读。')
    def courtyard(self):
        self.start(self.t('10 / The courtyard as a shared address','10 / 庭院成为共同的场所'),'PORTFOLIO')
        self.image(ASSET/'Aerial_collage.png',252,105,563,419)
        self.para(self.t('A place between lessons.','课与课之间的地方。'),38,131,213,26,34)
        self.para(self.t('The connected wings define a common outdoor room. Its value comes from how easily children can reach it and how many kinds of activity its edges can support.',
                            '相互连接的翼部围合出共同的户外空间。它的价值取决于孩子能否方便到达，以及边缘能够支持多少种活动。'),38,239,213,11,17)
        self.rule(38,377,188,TEAL)
        self.para(self.t('Design development\nA quiet edge / a small-group table / an open center / a clear adult contact',
                            '深化方向\n安静边缘 / 小组桌面 / 开敞中心 / 明确的成人联系人'),38,399,204,10,17)
        self.caption('Architectural collage using the supplied aerial rendering. Building geometry is retained; the surrounding ground is recomposed.',
                     '以提供的鸟瞰效果图制作建筑拼贴，保留建筑几何关系，重新组织周边底景。')
    def material(self):
        self.start(self.t('11 / Material, rhythm and a human scale','11 / 材料、节奏与人的尺度'),'PORTFOLIO')
        self.pdf(ASSET/'Architectural_collages.pdf',1,[38,111,804,422],[55,214,1345,729])
        items=[('#DFDDD4','Pale mineral walls','浅色墙面','A bright, quiet background.','明亮、平静的背景。'),
               ('#666C68','Gray roof surfaces','灰色屋面','A continuous roofscape.','连贯的屋顶轮廓。'),
               ('#B3946A','Warm vertical screens','暖色竖向格栅','Rhythm at close range.','近距离可感知的节奏。'),
               ('#9DAD9A','Restrained landscape','克制的景观','Simple edges to maintain.','便于维护的简单边界。')]
        for i,(col,a,b,cc,d) in enumerate(items):
            x=38+i*195;self.rect(x,438,29,29,col)
            self.para(self.t(a,b),x+39,439,140,10,14,font=self.bold)
            self.para(self.t(cc,d),x,483,172,9.5,14)
        self.caption('Recomposed architectural collage and an interpretive material palette derived from the supplied renderings.',
                     '重新构成的建筑拼贴，以及根据提供效果图整理的材料色彩组合。')
    def implementation(self):
        self.start(self.t('12 / Keep the campus working','12 / 让校园持续运转'),'PORTFOLIO')
        # Plain editorial rows; no decorative cards.
        headings=[(38,'PRIORITY','重点'),(220,'SPATIAL ACTION','空间行动'),(498,'OPERATING ARRANGEMENT','运行安排')]
        for x,en,zh in headings:self.text(self.t(en,zh),x,119,9,self.bold,TEAL)
        self.rule(38,145,766,TEAL)
        rows=[
            ('Daily essentials','日常必需','Toilets, washing and repaired surfaces.','厕所、洗手和地面修补。','Assign checks, cleaning and repair responsibilities.','明确检查、清洁和修补责任。'),
            ('Choice in short breaks','短课间的选择','Seats, movable tables and accessible storage.','座位、可移动桌面和方便的储物。','Agree when and how children can use them.','约定儿童使用的时间和方式。'),
            ('Support close by','邻近的支持','Waiting and private conversation near staff.','靠近工作人员的等候与私下交流。','Name a contact and arrange access to outside help.','明确联系人和外部帮助的联系办法。'),
            ('Shared activity','共享活动','Adaptable rooms and courtyard edges.','可调整的房间与庭院边缘。','Match a weekly program with available teachers.','将每周活动与可到场教师匹配。'),
            ('Long-term campus','长期校园','Coordinate wings, grounds and service access.','协调翼部、场地与后勤进入。','Plan maintenance and recurring resources with construction.','把维护与持续资源和建设一起考虑。')]
        y=165
        for a,b,cc,d,e,f in rows:
            self.para(self.t(a,b),38,y,158,12,17,font=self.bold)
            self.para(self.t(cc,d),220,y,247,11,17)
            self.para(self.t(e,f),498,y,303,11,17)
            self.rule(38,y+60,766);y+=72
        self.caption('Proposed action sequence. Progress can be reviewed through repeated observations and short conversations with pupils and staff.',
                     '建议的行动次序。可以通过重复观察，以及与学生和教职工的简短交流，了解实施后的使用情况。')
    def finish(self):
        self.c.save()
        doc=fitz.open(self.temp)
        cache={}
        for item in self.inserts:
            path=item['path']
            if path not in cache:cache[path]=fitz.open(path)
            doc[item['page']].show_pdf_page(fitz.Rect(item['rect']),cache[path],item['pno'],clip=fitz.Rect(item['clip']) if item['clip'] else None)
        toc=[]
        for i,title in enumerate(self.inventory):
            if title:toc.append([1,title,i+1])
        doc.set_toc(toc)
        final=OUT/(f'Everyday_Care_Research_and_Portfolio_{self.lang}.pdf')
        doc.save(final,garbage=4,deflate=True)
        for d in cache.values():d.close()
        doc.close()
        (WORK/f'page_inventory_{self.lang}.json').write_text(json.dumps({'pages':self.p,'titles':self.inventory,'body_ends':self.heights},ensure_ascii=False,indent=2),encoding='utf-8')
        print(self.lang,'pages',self.p,'saved',final)
        return final

if __name__=='__main__':
    for lang in ['EN','ZH']:
        b=Book(lang)
        b.cover();b.abstract();b.paper();b.references();b.questionnaire();b.audit_appendix()
        b.portfolio_divider();b.site_context();b.field_design();b.masterplan();b.plan_page(0);b.plan_page(1)
        b.upper_plans();b.circulation();b.elevations();b.sections();b.courtyard();b.material();b.implementation()
        b.finish()
