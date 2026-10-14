import sys,json,re,math,csv,collections,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(".work_packages").resolve()))
from lxml import etree
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from PIL import Image,ImageOps,ImageDraw,ImageFont
import jieba

ROOT=Path(__file__).parent
OUT=ROOT/"研究报告交付"
DATA=OUT/"分析数据"
FIG=OUT/"图表"
for p in (OUT,DATA,FIG):p.mkdir(exist_ok=True,parents=True)
base=Path(r"${ORIGINAL_USER_HOME}/Documents/WXWork/1688856569769957/Cache/File/2026-09")
fontpath="C:/Windows/Fonts/msyh.ttc"
plt.rcParams.update({"font.family":"Microsoft YaHei","font.size":11,"axes.spines.top":False,"axes.spines.right":False,"axes.unicode_minus":False,"figure.dpi":160})
BLUE="#245C75";GREEN="#568B75";ORANGE="#C88A48";GRAY="#79848C"
questions=["了解来源","服务儿童","教学之外的照护","经常使用的空间","空间问题","愿意停留的地方","使用较少的地方","最需要改善的三方面","首选改善项目","现实限制"]
answers=[
 ["工作接触+公益/志愿活动",
  "想家中没有父母了的孩子，或者孩子只有爷爷奶奶或外公外婆带的孩子",
  "生活照顾，先学会做人",
  "教室、宿舍、食堂。其中使用最频繁的是：教室，大部分活动都是在教室内完成的",
  "缺少厕所，整栋教学楼只有一个厕所，并且是在教学楼外",
  "操场/教学楼前坪，因为他们可以在这个玩耍，并且当学校有人来参观得时候可以学生可以在这里和参观的人互动",
  "学校后坪，因为这里很大，但只是作为一个土堆，没有发挥很大的用处，只用了一小块作为菜地，给学生使用",
  "第一：教室质量。第二：师资。第三：资金问题",
  "增加更多的儿童活动空间，比如利用后院，增加一些设施",
  "资金问题最严重。校长说学校没有长期稳定的捐款来源，导致学校的完善计划耽搁"],
 ["工作接触+公益/志愿活动",
  "家庭困难很严重的学生，还包括一些有缺陷的学生",
  "情绪支持",
  "教学楼区域。其中使用最频繁的是：教室",
  "空间利用率低，有很多空教室，原因是因资金问题学校暂时关闭里初中部，导致很多教室空置，并且很多有用的课桌等资料闲置",
  "操场，很大而且很空，可以让他们随意玩耍",
  "没发现学校有使用率很低的地方，学校已经有了很多有用的功能，并且每个都是对于学生必须的",
  "第一：资金问题。第二：医疗问题，学校的校医室很简陋。第三：操场很简陋",
  "校医室，因为学校没有能力保持一个专业的校医，只能依靠志愿者或送到周边医院",
  "资金"]
]
# Prompts and interviewer-provided bridging words are not part of the response corpus.
answers[0][3]="教室、宿舍、食堂\n教室，大部分活动都是在教室内完成的"
answers[1][3]="教学楼区域\n教室"
answers[0][7]="教室质量\n师资\n资金问题"
answers[1][7]="资金问题\n医疗问题，学校的校医室很简陋\n操场很简陋"
rows=[{"受访者":f"R{r+1}","日期":["2026-09-23","2026-09-26"][r],"题号":i+1,"主题":questions[i],"回答":a} for r,aa in enumerate(answers) for i,a in enumerate(aa)]
def csvwrite(name,rows,fields=None):
 with (DATA/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
csvwrite("问卷逐题回答.csv",rows)
corpus="\n".join(x["回答"] for x in rows)
(DATA/"词频语料_仅填写答案.txt").write_text(corpus,encoding="utf-8")
# Predeclared study-specific terms; these counts are occurrences, not people.
terms=["教室","资金","操场","教学楼","校医室","厕所","玩耍","空间","活动","使用率低","生活照顾","情绪支持","后坪","后院","师资","捐款","志愿者","医疗","课桌","宿舍","食堂","菜地","设施","公益","志愿活动","互动","安静","照明","遮阴","阅读","家长"]
freq=[]
for term in terms:
 count=corpus.count(term)
 if count:
  freq.append({"关键词":term,"次数":count,"涉及受访者数":sum(term in "\n".join(a) for a in answers),"涉及答题单元数":sum(term in r["回答"] for r in rows)})
freq.sort(key=lambda x:(-x["次数"],terms.index(x["关键词"])))
csvwrite("关键词频次.csv",freq)
for word in terms:jieba.add_word(word)
stop=set("学校 学生 儿童 孩子 他们 这里 这个 一些 很多 可以 一个 没有 因为 并且 以及 其中 最 还有 只有 很大 很空 对于 时候 导致 比如 需要 发现 已经 每个 都是 问题 作为 就是 只能 包括 或者 觉得 不是 暂时 增加 更 多 不 等 先 我们 使用 来源 最频繁 完成 有用 第一 第二 第三".split())
tokens=[t for t in jieba.lcut(corpus) if re.fullmatch(r"[\u4e00-\u9fff]{2,}",t) and t not in stop]
csvwrite("分词词频完整表.csv",[{"词语":k,"次数":v} for k,v in collections.Counter(tokens).most_common()])
(DATA/"词频说明.txt").write_text("分析语料为两份已填问卷的20个回答单元，仅剔除下划线、题目、未勾选选项、模板、身份日期及原表第一第二第三顺序标签。保留原回答中的个别笔误。关键词表按预设主题词逐字匹配计数，例如空教室计入教室，资金问题计入资金；同一回答重复出现重复计数。词频不是人数，不根据肯定否定做情感判断。分词完整表另用jieba分词并去除停用词。停用词：\n"+" ".join(sorted(stop)),encoding="utf-8")
fig,ax=plt.subplots(figsize=(9,5.3),layout="constrained")
top=freq[:15][::-1]
ax.barh([r["关键词"] for r in top],[r["次数"] for r in top],color=BLUE,height=.65)
for i,r in enumerate(top):ax.text(r["次数"]+.09,i,str(r["次数"]),va="center",fontsize=11)
ax.set(xlim=(0,max(r["次数"] for r in top)+1),xlabel="出现次数  单位 次",title="两份问卷回答中的关键词")
ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
fig.savefig(FIG/"01_问卷关键词频次.png");plt.close(fig)

# Extract the original 1–5 checked column, not a reconstructed judgement.
import zipfile
with zipfile.ZipFile(base/"环境审计.docx") as z:root=etree.fromstring(z.read("word/document.xml"))
ns={"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
audit=[]
for tr in root.xpath("//w:tr",namespaces=ns):
 cells=["".join(tc.xpath(".//w:t/text()",namespaces=ns)) for tc in tr.findall("w:tc",ns)]
 if len(cells)==7 and "✅" in "".join(cells[2:]):
  checked=[i+1 for i,c in enumerate(cells[2:]) if "✅" in c]
  assert len(checked)==1
  audit.append({"维度":cells[0],"项目":cells[1],"评分":checked[0]})
csvwrite("环境审计全部项目.csv",audit)
groups={}
for r in audit:groups.setdefault(r["维度"],[]).append(r["评分"])
groupstats=[{"维度":k,"项目数":len(v),"总分":sum(v),"均分":round(sum(v)/len(v),3),"低分项目数_1至2分":sum(x<=2 for x in v)} for k,v in groups.items()]
csvwrite("环境审计维度汇总.csv",groupstats)
fig,ax=plt.subplots(figsize=(8.4,3.6),layout="constrained")
rs=groupstats[::-1];ax.barh([r["维度"] for r in rs],[r["均分"] for r in rs],color=[GREEN if r["均分"]>=3.5 else ORANGE for r in rs],height=.6)
for i,r in enumerate(rs):ax.text(r["均分"]+.08,i,f'{r["均分"]:.2f}  （{r["项目数"]}项）',va='center')
ax.set(xlim=(0,5),xlabel="原始项目平均分  满分5分",title="校园环境五个维度的现场评分")
fig.savefig(FIG/"02_环境审计维度均分.png");plt.close(fig)
dist=collections.Counter(r["评分"] for r in audit)
fig,ax=plt.subplots(figsize=(7.8,3.5),layout='constrained')
ax.bar([str(i)+"分" for i in range(1,6)],[dist[i] for i in range(1,6)],color=[ORANGE,ORANGE,GRAY,BLUE,GREEN],width=.6)
for i in range(1,6):ax.text(i-1,dist[i]+.25,str(dist[i]),ha='center')
ax.set(ylabel="项目数",ylim=(0,max(dist.values())+2),title="35项环境审计评分分布");ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
fig.savefig(FIG/"03_评分分布.png");plt.close(fig)

# The daily timetable is transcribed from the supplied photograph.
schedule=[
("早操","06:50","07:10","活动"),("早读","07:10","07:40","学习"),
("早餐","07:40","08:35","就餐"),("第一节","08:35","09:15","学习"),
("第二节","09:30","10:10","学习"),("课间操","10:10","10:30","活动"),
("第三节","10:30","11:10","学习"),("眼保健操","11:10","11:25","保健"),
("第四节","11:25","12:05","学习"),("午餐","12:05","12:50","就餐"),
("午休","12:50","14:10","午休"),("第五节","14:30","15:10","学习"),
("眼保健操","15:10","15:25","保健"),("第六节","15:25","16:05","学习"),
("第七节","16:20","17:00","学习"),("文体活动","17:00","17:50","活动"),
("晚餐","17:50","18:50","就餐"),("晚自习一","19:00","19:40","学习"),
("晚自习二","19:50","20:30","学习")]
tm=lambda t:int(t[:2])*60+int(t[3:])
srows=[{"安排":n,"开始":s,"结束":e,"分钟数":tm(e)-tm(s),"类别":k} for n,s,e,k in schedule]
csvwrite("作息时间统计.csv",srows)
st=collections.Counter()
for r in srows:st[r["类别"]]+=r["分钟数"]
st["间隔与未单列时段"]=870-sum(st.values())
csvwrite("作息分类汇总.csv",[{"类别":k,"分钟数":v,"占日间870分钟比例":round(v/870*100,2)} for k,v in st.items()])
fig,ax=plt.subplots(figsize=(8.6,3.7),layout='constrained')
order=["学习","就餐","活动","午休","保健","间隔与未单列时段"]
ax.barh(order[::-1],[st[k] for k in order[::-1]],color=[GRAY,GREEN,GREEN,ORANGE,ORANGE,BLUE],height=.63)
for i,k in enumerate(order[::-1]):ax.text(st[k]+5,i,str(st[k]),va="center")
ax.set(xlim=(0,440),xlabel="分钟",title="6时30分至21时的日间安排")
fig.savefig(FIG/"04_作息时长.png");plt.close(fig)

# Researcher's route: use point timestamps, distinguish from exporter metadata.
r=etree.parse(str(base/"2026-09-23 14 36 15.kml"));kns={"k":"http://www.opengis.net/kml/2.2","gx":"http://www.google.com/kml/ext/2.2"}
coords=np.array([[float(v) for v in t.split()] for t in r.xpath("//gx:coord/text()",namespaces=kns)])
times=r.xpath("//k:when/text()",namespaces=kns)
data={d.get("name"):"".join(d.xpath("k:value/text()",namespaces=kns)) for d in r.xpath("//k:Data",namespaces=kns)}
R=6371000
lon,lat=np.radians(coords[:,0]),np.radians(coords[:,1])
dlon,dlat=np.diff(lon),np.diff(lat)
h=np.sin(dlat/2)**2+np.cos(lat[:-1])*np.cos(lat[1:])*np.sin(dlon/2)**2
distances=2*R*np.arctan2(np.sqrt(h),np.sqrt(1-h))
x=(lon-lon[0])*R*np.cos(lat.mean());y=(lat-lat[0])*R
from datetime import datetime,timezone,timedelta
dts=[datetime.fromisoformat(t.replace("Z","+00:00")).astimezone(timezone(timedelta(hours=8))) for t in times]
gaps=np.array([(b-a).total_seconds() for a,b in zip(dts[:-1],dts[1:])])
route={"点数":len(coords),"首点时间":dts[0].isoformat(),"末点时间":dts[-1].isoformat(),"点时间跨度分钟":(dts[-1]-dts[0]).total_seconds()/60,"文件记录里程米":float(data["Distance"]),"相邻坐标累加米":float(sum(distances)),"最长采样间隔秒":float(max(gaps)),"大于5分钟间隔数":int(sum(gaps>300)),"元数据开始":datetime.fromtimestamp(int(data["BeginTime"])/1000,timezone(timedelta(hours=8))).isoformat(),"元数据结束":datetime.fromtimestamp(int(data["EndTime"])/1000,timezone(timedelta(hours=8))).isoformat(),"最高点间速度米每秒":float(max(distances/np.maximum(gaps,1)))}
fig,ax=plt.subplots(figsize=(7.6,5.2),layout='constrained')
# Long gaps shown dashed, not as continuous measured walking segments.
for i in range(len(x)-1):ax.plot(x[i:i+2],y[i:i+2],color=BLUE,lw=1.6,linestyle="--" if gaps[i]>300 else "-",alpha=.8)
ax.scatter([x[0]],[y[0]],c=GREEN,s=65,zorder=5,label="首个定位点 14:36")
ax.scatter([x[-1]],[y[-1]],c=ORANGE,s=65,marker="s",zorder=5,label="最后定位点 16:36")
ax.set(xlabel="相对首点的东西距离  米",ylabel="相对首点的南北距离  米",title="9月23日调研人员记录轨迹")
ax.set_aspect("equal",adjustable="datalim");ax.legend(loc="best",fontsize=9);ax.grid(alpha=.15)
fig.savefig(FIG/"05_调研记录轨迹.png");plt.close(fig)

manifest=[]
for p in sorted((ROOT/"材料整理/照片").iterdir()):
 if p.suffix.lower() in [".jpg",".heic"]:manifest.append({"文件名":p.name,"格式":p.suffix.upper(),"字节数":p.stat().st_size,"SHA256":hashlib.sha256(p.read_bytes()).hexdigest()})
csvwrite("照片清单.csv",manifest)
summary={"问卷数":2,"答题单元数":20,"回答中文字数":len(re.findall(r"[\u4e00-\u9fff]",corpus)),"词频":freq,"评分条目数":len(audit),"评分总分":sum(r["评分"] for r in audit),"总体均分":sum(r["评分"] for r in audit)/len(audit),"分布":dict(dist),"维度":groupstats,"作息":dict(st),"轨迹":route,"照片数":len(manifest)}
(DATA/"统计摘要.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False,indent=2))
