from pathlib import Path
import json,copy,csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from xml.sax.saxutils import escape

R=Path(__file__).parent
B=R/'论文与作品集/工作文件/ppt_build'
OUT=R/'论文与作品集/英文15页_三张词频图'
FIG=OUT/'Word_Frequency_Figures'
FIG.mkdir(parents=True,exist_ok=True)
corpus=(R/'研究报告交付/分析数据/词频语料_仅填写答案.txt').read_text('utf-8')
groups=[
 ('Recurring terms',[('教室','Classroom'),('资金','Funding'),('教学楼','Teaching building'),('操场','Playground'),('校医室','School clinic'),('厕所','Toilet'),('玩耍','Play'),('空间','Space')]),
 ('Campus spaces',[('教室','Classroom'),('教学楼','Teaching building'),('操场','Playground'),('校医室','School clinic'),('厕所','Toilet'),('宿舍','Dormitory'),('食堂','Dining hall')]),
 ('Care & resources',[('资金','Funding'),('公益','Charity'),('志愿活动','Volunteering'),('生活照顾','Daily care'),('情绪支持','Emotional support'),('师资','Teaching staff'),('捐款','Donations')])
]
datasets=[]
for title,pairs in groups:
    datasets.append(dict(title=title,categories=[en for cn,en in pairs],
                         terms=[cn for cn,en in pairs],values=[corpus.count(cn) for cn,en in pairs]))
with (FIG/'Word_Frequency_Data.csv').open('w',encoding='utf-8-sig',newline='') as f:
    wr=csv.writer(f);wr.writerow(['Chart','English term','Original term','Occurrences'])
    for g in datasets:
        wr.writerows(zip([g['title']]*len(g['terms']),g['categories'],g['terms'],g['values']))
plt.rcParams.update({'font.family':'Arial','font.size':11,'svg.fonttype':'none','pdf.fonttype':42})
def chart(ax,g):
    bars=ax.barh(g['categories'][::-1],g['values'][::-1],color=['#81968A']*(len(g['values'])-1)+['#345A60'],height=.64)
    ax.set_xlim(0,8);ax.set_xticks([0,2,4,6,8]);ax.set_xlabel('Occurrences',fontsize=10,color='#65736D')
    ax.set_title(g['title'],loc='left',fontweight='bold',fontsize=14,pad=15,color='#252D2C')
    ax.xaxis.grid(True,color='#E4E9E6',linewidth=.6);ax.set_axisbelow(True)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.tick_params(axis='both',length=0,pad=7,labelcolor='#252D2C')
    ax.bar_label(bars,padding=5,fontsize=11,color='#252D2C')
for n,g in enumerate(datasets,1):
    fig,ax=plt.subplots(figsize=(6.6,4.4));fig.subplots_adjust(left=.27,right=.95,bottom=.17,top=.86)
    chart(ax,g)
    fig.text(.025,.025,'Questionnaire responses · occurrences in Chinese text',fontsize=8,color='#65736D')
    for ext in ['png','svg','pdf']:fig.savefig(FIG/f'Word_Frequency_{n:02d}.{ext}',dpi=300,facecolor='white')
    plt.close(fig)
fig,axes=plt.subplots(1,3,figsize=(16,5));fig.subplots_adjust(left=.10,right=.975,bottom=.18,top=.86,wspace=.73)
for ax,g in zip(axes,datasets):chart(ax,g)
fig.text(.025,.035,'Questionnaire responses · occurrences in Chinese text',fontsize=10,color='#65736D')
for ext in ['png','svg','pdf']:fig.savefig(FIG/f'Word_Frequency_Triptych.{ext}',dpi=300,facecolor='white')
plt.close(fig)

d=json.loads((B/'tight15_layout_EN.json').read_text('utf-8'))
for n,f in [('Sans','arial.ttf'),('SansB','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(n,'C:/Windows/Fonts/'+f))
def resize(o,x,y,w,size=None):
    o.update(x=x,y=y,w=w)
    if size:o['size']=size;o['leading']=size*1.18
    p=Paragraph(escape(o['text']).replace('\n','<br/>'),ParagraphStyle('p',fontName=o['font'],fontSize=o['size'],leading=o['leading']))
    o['h']=p.wrap(w-3,2000)[1]+2
def text(t,x,y,w,size=9,font='SansB'):
    o=dict(kind='text',text=t,x=x,y=y,w=w,size=size,leading=size*1.2,font=font,color='#345A60',source='paragraph')
    resize(o,x,y,w);return o
def origin(s,p,i):
    return next(o for o in s['objects'] if o.get('_origin')==[p,i])

s3,s7,s8=d['slides'][2],d['slides'][6],d['slides'][7]
# Preserve all existing text, moving the three recurring-theme notes under references.
for i,y in [(10,536),(11,547),(12,558)]:
    o=origin(s3,6,i);s3['objects'].remove(o);resize(o,24,y,383,7.3)
    s7['objects'].append(o)
# Move the environmental domain summary to the environmental audit page.
audit=[]
for i in [14,15,16,17,18,19]:
    o=origin(s3,6,i);s3['objects'].remove(o);audit.append(o);s8['objects'].append(o)
resize(audit[0],437,100,381,10)
audit[1].update(x=435,y=120,w=383,h=124)
resize(audit[2],437,247,48,9)
resize(audit[3],490,247,152,7.8)
resize(audit[4],638,247,180,7.8)
resize(audit[5],437,261,381,6.6)
# Reflow the existing-school photographs and design priorities under the audit chart.
for k,(ii,ci) in enumerate([(8,9),(10,11),(12,13),(14,15)]):
    o=origin(s8,14,ii);x=437+(k%2)*196;y=279+(k//2)*105
    ar=o['w']/o['h'];hh=86;ww=hh*ar
    o.update(x=x+(185-ww)/2,y=y,w=ww,h=hh)
    resize(origin(s8,14,ci),x,y+89,185,7.9)
for k,(a,b,c) in enumerate([(16,17,18),(19,20,21),(22,23,24),(25,26,27)]):
    x=437+(k%2)*196;y=493+(k//2)*34
    resize(origin(s8,14,a),x,y,23,10.5)
    resize(origin(s8,14,b),x+28,y,157,7.9)
    resize(origin(s8,14,c),x+28,y+12,157,7.7)
resize(origin(s8,14,28),437,565,381,6.8)
# Three equally scaled editable frequency charts.
resize(origin(s3,6,8),566,80,252,10.6)
origin(s3,6,8)['text']='01 / Recurring terms'
kw=origin(s3,6,9);kw.update(x=562,y=101,w=256,h=140,**datasets[0],chart='frequency',max=8)
resize(origin(s3,6,13),566,243,252,6.6)
for k,(y,h) in enumerate([(261,121),(418,122)],1):
    s3['objects'].append(text(f'0{k+1} / {datasets[k]["title"]}',566,y,252,10.6))
    s3['objects'].append(dict(kind='chart',chart='frequency',x=562,y=y+20,w=256,h=h,max=8,**datasets[k]))
    s3['objects'].append(text('Occurrences in Chinese questionnaire responses.',566,y+h+21,252,6.5,'Sans'))
s3['notes']+=' Word-frequency figures count literal occurrences of selected Chinese terms in written questionnaire responses. English labels are translations. The three panels show selected recurring terms, campus spaces, and care/resources; their vocabularies overlap. See Word_Frequency_Data.csv for exact term mappings.'
(B/'wordfreq3_layout_EN.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf-8')
# All earlier substantive text must remain verbatim, except the updated keyword heading.
old=json.loads((B/'tight15_layout_EN.json').read_text('utf-8'))
newtext=[o['text'] for s in d['slides'] for o in s['objects'] if o['kind']=='text']
missing=[o['text'] for s in old['slides'] for o in s['objects'] if o['kind']=='text' and o['text'] not in newtext and o.get('_origin')!=[6,8]]
assert not missing,missing
(B/'wordfreq3_audit.json').write_text(json.dumps(dict(datasets=datasets,pages=15,original_text_missing=missing),indent=2,ensure_ascii=False),'utf-8')

# Reuse the validated artifact-tool builder, extending the native chart data input.
js=(B/'build_tight15.mjs').read_text('utf-8')
js=js.replace('../../英文15页紧凑版','../../英文15页_三张词频图')
js=js.replace('tight15_layout_','wordfreq3_layout_').replace('tight15_candidate_','wordfreq3_candidate_').replace('tight15_exact_','wordfreq3_exact_')
js=js.replace('Campus_Research_Portfolio_${lang}_15pages_Final.pptx','Campus_Research_Portfolio_${lang}_15pages_3WordCharts.pptx')
js=js.replace('validation_tight15_${lang}_Final.json','validation_wordfreq3_${lang}.json')
js=js.replace('requiredNativeChartOwnerSlides:[3,4]','requiredNativeChartOwnerSlides:[3,4,8]')
js=js.replace("if(o.chart==='keywords'){","if(o.chart==='frequency'){\n    categories=[...o.categories];values=[...o.values];colors=values.map((v,i)=>i===0?teal:green);\n  }else if(o.chart==='keywords'){")
js=js.replace("o.chart==='keywords'?", "(o.chart==='keywords'||o.chart==='frequency')?")
(B/'build_wordfreq3.mjs').write_text(js,'utf-8')
ps=(R/'export_tight15_checks.ps1').read_text('utf-8')
ps=ps.replace('英文15页紧凑版','英文15页_三张词频图').replace('15pages_Final.pptx','15pages_3WordCharts.pptx')
ps=ps.replace('Tight15_metrics_','WordFreq3_metrics_').replace('Tight15_${language}.pdf','WordFreq3_${language}.pdf')
(R/'export_wordfreq3_checks.ps1').write_text(ps,'utf-8')
qa=(R/'review_tight15.py').read_text('utf-8')
qa=qa.replace('英文15页紧凑版','英文15页_三张词频图').replace('15pages_Final.pptx','15pages_3WordCharts.pptx')
qa=qa.replace('tight15_review','wordfreq3_review').replace('Tight15_metrics_','WordFreq3_metrics_').replace('Tight15_{lang}.pdf','WordFreq3_{lang}.pdf')
qa=qa.replace('len(charts)==3 and len(books)==3','len(charts)==5 and len(books)==5')
(R/'review_wordfreq3.py').write_text(qa,'utf-8')
print(json.dumps(datasets,ensure_ascii=False,indent=2))
