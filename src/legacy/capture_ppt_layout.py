from pathlib import Path
import json,io,hashlib
import pymupdf as fitz
import numpy as np
from PIL import Image,ImageOps
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from xml.sax.saxutils import escape
import build_bilingual_portfolio as B

ROOT=Path(__file__).parent
TMP=ROOT/'论文与作品集'/'工作文件'/'ppt_build'
TMP.mkdir(exist_ok=True)
MEDIA=TMP/'media';MEDIA.mkdir(exist_ok=True)
def palette(color):
    return {'#F3F1EA':'#FFFFFF','#B68168':'#81968A','#D8CBBB':'#DCE5DC'}.get(color.upper(),color)
def white_collage(im):
    a=np.asarray(im.convert('RGBA')).copy()
    # Exact flat paper color is presentation scenery, not building material.
    mask=np.max(np.abs(a[:,:,:3].astype(int)-np.array([243,241,234])),axis=2)<=2
    a[mask,:3]=255
    return Image.fromarray(a)
class Capture(B.Book):
    def __init__(self,lang):
        self.lang=lang;self.z=lang=='ZH';self.font='CN' if self.z else 'Sans'
        self.bold='CNB' if self.z else 'SansB';self.body='CN' if self.z else 'Serif'
        self.p=0;self.inventory=[];self.heights=[];self.slides=[]
        self.c=canvas.Canvas(io.BytesIO())
    def add(self,kind,**kw):
        if 'color' in kw:kw['color']=palette(kw['color'])
        if kind=='text' and self.p==17:
            kw['color']='#345A60' if kw['size']<22 else '#252D2C'
        self.slides[-1]['objects'].append(dict(kind=kind,**kw))
    def start(self,title,part='PAPER',bg=B.PAPER,number=None):
        self.slides.append(dict(title=title,objects=[],bg='#FFFFFF'))
        super().start(title,part,bg,number)
    def text(self,text,x,y,size=10,font=None,color=B.INK):
        if not text:return
        fn=font or self.font
        width=pdfmetrics.stringWidth(text,fn,size)+4
        self.add('text',text=text,x=x,y=y,w=min(B.W-x-4,width+2),h=size*1.5,
                 size=size,font=fn,color=color,leading=size*1.2,source='single')
    def para(self,text,x,y,w,size=10.3,leading=None,font=None,color=B.INK,maxh=None):
        if self.p==1 and x==40 and y==210:w=245
        if self.p==24 and y==525:y=517
        leading=leading or size*1.45;fn=font or self.font
        st=ParagraphStyle('p',fontName=fn,fontSize=size,leading=leading,wordWrap='CJK' if self.z else None)
        pp=Paragraph(escape(text).replace('\n','<br/>'),st);_,h=pp.wrap(w,1000)
        # Native paragraphs keep the source text and the source's usable box.
        self.add('text',text=text,x=x,y=y,w=min(w+10,B.W-x-32),h=h+5,size=size,font=fn,color=color,leading=leading,source='paragraph')
        return h
    def rect(self,x,y,w,h,color):
        # A whole-page fill replaces, rather than covers, any earlier objects.
        if x==0 and y==0 and abs(w-B.W)<.01 and abs(h-B.H)<.01:
            self.slides[-1]['bg']='#FFFFFF'
            if self.slides[-1]['objects']:self.slides[-1]['objects']=[]
        else:self.add('rect',x=x,y=y,w=w,h=h,color=color)
    def rule(self,x,y,w,color=B.LINE):
        self.add('line',points=[[x,y],[x+w,y]],color=color,width=.55,dash=None)
    def dot(self,x,y,r=4,color=B.TEAL):
        self.add('ellipse',x=x-r,y=y-r,w=r*2,h=r*2,color=color)
    def line(self,points,color=B.TEAL,width=1.2,dash=None):
        self.add('line',points=points,color=color,width=width,dash=dash)
    def image(self,path,x,y,w,h,cover=False):
        im=ImageOps.exif_transpose(Image.open(path))
        if 'collage' in str(path).lower():im=white_collage(im)
        key=hashlib.sha1((str(path)+str((w,h,cover))+'white-v1').encode()).hexdigest()[:16]
        dest=MEDIA/f'{key}.png'
        if cover:im=ImageOps.fit(im,(int(w*3),int(h*3)),method=Image.Resampling.LANCZOS)
        else:
            scale=min(w/im.width,h/im.height);ww,hh=im.width*scale,im.height*scale
            x+=(w-ww)/2;y+=(h-hh)/2;w,h=ww,hh
        if not dest.exists():im.save(dest)
        self.add('image',path=str(dest),x=x,y=y,w=w,h=h,alt=Path(path).stem)
    def pdf(self,path,pno,rect,clip=None):
        name=Path(path).stem
        if name.startswith(('keywords_','audit_','time_')):
            self.add('chart',chart=name.split('_')[0],x=rect[0],y=rect[1],w=rect[2]-rect[0],h=rect[3]-rect[1])
            return
        d=fitz.open(path);pg=d[pno];cr=fitz.Rect(clip) if clip else pg.rect
        x,y,x1,y1=rect;ww,hh=x1-x,y1-y
        scale=min(ww/cr.width,hh/cr.height);w,h=cr.width*scale,cr.height*scale
        x+=(ww-w)/2;y+=(hh-h)/2
        key=hashlib.sha1((str(path)+str(pno)+str(clip)+'white-v2').encode()).hexdigest()[:16]
        dest=MEDIA/f'{key}.png'
        if not dest.exists():
            # 450 dpi at final placement, including vector lines.
            pg.get_pixmap(matrix=fitz.Matrix(scale*6.25,scale*6.25),clip=cr,alpha=True).save(dest)
            if 'collage' in str(path).lower():white_collage(Image.open(dest)).save(dest)
            if 'Architectural_drawings_keyed' in str(path):
                a=np.asarray(Image.open(dest).convert('RGBA')).copy()
                transparent_tint=(a[:,:,0]>160)&(a[:,:,1]>100)&(a[:,:,1]<145)&(a[:,:,2]<125)&(a[:,:,3]<100)
                a[transparent_tint,:3]=[128,151,135]
                opaque_tint=(a[:,:,0]>=240)&(a[:,:,0]<=249)&(a[:,:,1]>=234)&(a[:,:,1]<=241)&(a[:,:,2]>=230)&(a[:,:,2]<=237)&(a[:,:,3]>240)
                a[opaque_tint,:3]=[238,241,239]
                Image.fromarray(a).save(dest)
        self.add('image',path=str(dest),x=x,y=y,w=w,h=h,alt=name+' sheet '+str(pno+1))
        d.close()

for lang in ['EN','ZH']:
    b=Capture(lang)
    b.cover();b.abstract();b.paper();b.references();b.questionnaire();b.audit_appendix()
    b.portfolio_divider();b.site_context();b.field_design();b.masterplan();b.plan_page(0);b.plan_page(1)
    b.upper_plans();b.circulation();b.elevations();b.sections();b.courtyard();b.material();b.implementation()
    assert len(b.slides)==29
    payload=dict(lang=lang,width=B.W,height=B.H,slides=b.slides)
    (TMP/f'layout_{lang}.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    print(lang, len(b.slides),'slides',sum(len(s['objects']) for s in b.slides),'objects')
