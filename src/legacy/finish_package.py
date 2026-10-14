from pathlib import Path
import csv,json,re,zipfile
import pymupdf

root=Path(__file__).parent
out=root/"研究报告交付";data=out/"分析数据"
def csvwrite(name,rows):
    with (data/name).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
audio=[]
for p in sorted((root/"材料整理/录音转写").glob("*.json")):
    obj=json.loads(p.read_text(encoding="utf-8"))
    audio.append({"文件":obj["source"],"文件时长秒":round(obj["duration"],3),"转写方式":"本地faster-whisper small int8","片段数":len(obj["segments"]),"统计用途":"重叠对话按主题合并，不计入书面问卷词频"})
csvwrite("录音文件整理.csv",audio)
chapter=(root/"材料整理/写作源文件/录音分析章节.md").read_text(encoding="utf-8")
source_rows=[]
for line in chapter.split("### 6 主要段落索引")[1].splitlines():
    if line.startswith("|") and not re.match(r'\|\s*(文件|---)',line):
        values=[x.strip() for x in line.strip("|").split("|")]
        if len(values)==3:source_rows.append(dict(zip(["文件","约略时间","整理主题"],values)))
csvwrite("录音主题索引.csv",source_rows)
themes=[
 ("资金制约改善","明确提及","明确提及"),
 ("教室使用集中","明确提及","明确提及"),
 ("操场具有玩耍吸引力","明确提及","明确提及"),
 ("厕所便利性不足","明确提及","未提及"),
 ("医疗照护需要改善","未提及","明确提及"),
 ("生活照顾与成长习惯","明确提及","未提及"),
 ("情绪支持","未提及","明确提及"),
 ("闲置或低使用空间","后坪","第5题提空教室，第7题否认低使用")]
csvwrite("问卷主题对照.csv",[{"主题":t,"R1":a,"R2":b} for t,a,b in themes])
observations=[
 ("约14时","操场","一个班，约20人","教师组织团体活动","树荫与跑道；原表提到中部草地不平"),
 ("约14时","教学楼一、二楼走廊","一楼零星人员、二楼无人","上课期间","与课程状态有关"),
 ("约15时","操场","0人","无体育课活动","单个观察时点"),
 ("约15时","教学楼一、二楼走廊","每层约20至25人","交谈、走动、踢毽子等","集中在教室外"),
 ("约15时","一楼教师办公室","2至3名学生和5名教师","师生交流","接近教师的节点"),
 ("约16时","操场","无人","未记录活动","单个观察时点"),
 ("约16时","教学楼一、二楼走廊","一楼零星人员、二楼无人","上课期间","与课程状态有关"),
 ("约17时","走廊、前坪及教学楼侧面运动区","大部分学生在教室外","文体活动、乒乓球等","地面、器材和照看范围")]
csvwrite("现场时空观察.csv",[dict(zip(["约略时间","位置","原记录人数","活动","空间关系"],v)) for v in observations])
(data/"整理口径说明.txt").write_text(
"""一 数据范围
问卷为两份已填写的随行人员访谈问卷，共20个回答单元。空白模板不计入样本。R1、R2代替原表个人称谓。

二 词频
主报告采用预选主题关键词的字符串出现次数，不是受访者人数。完整分词表使用jieba并剔除停用词。实际语料及词频口径另有对应文件。460为整理后的回答中的汉字数量，空白和标点不计。跨主题关键词可有包含关系，如“活动”包含“志愿活动”中的词段，不能把相互包含的关键词次数直接相加当作词总量。

三 环境评分
35项直接读取原表勾选的1至5分。表内有不同方向的问法，按填写值保留，未自行反向编码。35项总分118，总均分118/35=3.3714286；维度均分分别计算。总均分不是五个维度均分的简单平均。

四 时空观察与作息
8条现场观察以整点概记时间，人数多为目测；不累加为独立学生数。作息来自照片：日间870分钟，学习390、就餐160、活动90、午休80、眼保健操30、间隔120。所列时段不是实测活动或睡眠时长。

五 录音
3个文件已在本地转写。两份长录音大量重叠，短录音与MP3末段对应，按主题合并使用。转写用于主题检索和上下文对照，没有并入问卷词频；不清楚的姓名、年份、人数和金额未用于报告量化结论。完整机器转写工作稿保留在工作区“材料整理/录音转写”，未混入正式报告。

六 照片与轨迹
压缩包内111张照片，排除Mac系统附属文件；照片文件数不是观察样本人数。主报告使用8张没有突出个人身份信息的空间与道路照片。图组仅缩放与排版。
KML为调研人员记录，486点，记录里程4210.846米，相邻坐标球面距离累加4205.919米。坐标点时间2026-09-23 14:36:16至16:36:10，均为北京时间。文件开始元数据14:36:15，结束元数据20:36:17.161，与最后定位点不同。超过5分钟采样间隔共4处，图上用虚线连接。记录中有较快移动，不把整条路线解释为连续步行，更不作为儿童活动轨迹。
""",encoding="utf-8")
pdf=pymupdf.open(out/"桂阳县苦志育才公益学校调研报告.pdf")
text=(out/"桂阳县苦志育才公益学校调研报告.md").read_text(encoding="utf-8")
han_count=len(re.findall(r"[\u4e00-\u9fff]",text))
(out/"文件说明.txt").write_text(
f"""桂阳县苦志育才公益学校调研报告

报告共{len(pdf)}页，全文约{han_count}个汉字，含7幅统计图及照片组合图。

1. 桂阳县苦志育才公益学校调研报告.docx
   可继续编辑的Word版本，含目录、图表和附录。

2. 桂阳县苦志育才公益学校调研报告.pdf
   固定排版阅读及打印版本。

3. 桂阳县苦志育才公益学校调研报告.md
   便于复制和继续调整的纯文字版本；图表保存在同级“图表”文件夹。

4. 分析数据
   问卷逐题回答、词频语料和频次、主题对照、环境评分、
   现场观察、作息计算、录音主题索引、照片清单及整理口径。
   CSV使用UTF-8带BOM编码，便于在Excel中打开。

5. 图表
   报告中7幅图的独立PNG文件。

原始问卷、录音、照片压缩包和KML未改动。报告以所提供实地材料为基础撰写。
""",encoding="utf-8")
# Confirm TOC page references against actual page headings.
toc=pdf[1].get_text()
heading_names=re.findall(r'^## (.+)$',text,re.M)
toc_checks=[]
for heading in heading_names:
    key=re.sub(r"\s+","",heading)
    actual=[]
    for i in range(2,len(pdf)):
        for line in pdf[i].get_text().splitlines():
            if re.sub(r"\s+","",line)==key:actual.append(i+1)
    match=[l for l in toc.splitlines() if re.sub(r"\s+","",l).startswith(key)]
    if actual and match:
        page=int(re.search(r'(\d+)\s*$',match[0]).group(1))
        assert page==actual[0],(heading,page,actual)
        toc_checks.append({"章节":heading,"目录页码":page,"实际页码":actual[0]})
(root/"材料整理/最终版式检查/目录页码核对.json").write_text(json.dumps(toc_checks,ensure_ascii=False,indent=2),encoding="utf-8")
package=out/"桂阳县苦志育才公益学校研究报告及分析数据.zip"
with zipfile.ZipFile(package,"w",zipfile.ZIP_DEFLATED) as z:
    for name in ["桂阳县苦志育才公益学校调研报告.docx","桂阳县苦志育才公益学校调研报告.pdf","桂阳县苦志育才公益学校调研报告.md","文件说明.txt"]:
        z.write(out/name,name)
    for folder in ["分析数据","图表"]:
        for p in sorted((out/folder).rglob("*")):
            if p.is_file():z.write(p,p.relative_to(out))
with zipfile.ZipFile(package) as z:
    assert z.testzip() is None
print("TOC checked",len(toc_checks),"entries")
print("Packaged",package,package.stat().st_size)
