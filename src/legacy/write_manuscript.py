from pathlib import Path
import json,re

ROOT=Path(__file__).parent
OUT=ROOT/'论文与作品集'
OUT.mkdir(exist_ok=True)
sections=[]
def add(en,zh,fig,english,chinese):
    sections.append(dict(en=en,zh=zh,fig=fig,english=english.strip().split('\n\n'),chinese=chinese.strip().split('\n\n')))

add("Abstract","摘要","abstract", """
A school that provides daily care must offer more than places to attend lessons. It also needs places where children can play, wait, ask for help, and spend time together. This study examines how those everyday needs can inform a campus design for Kuzhi Yucai Public Welfare School in Guiyang County, Hunan, China. The material combines two adult questionnaires, a 35-item environmental audit, eight observation entries, a school timetable, photographs, recorded conversations, a researcher route, and a supplied architectural proposal.

Descriptive analysis reveals a recurring difference between having a space and being able to use it well. Both respondents identified classrooms as frequently used and the playground as a place children enjoyed. Yet activity support received the lowest raw audit average, 2.71 out of 5. Toilets, handwashing, small-group settings, movable furniture, and waiting space emerged as practical concerns. A Chinese-language keyword count reinforced the prominence of classrooms and funding, while recorded conversations connected spatial provision with staffing, continuing donations, and everyday companionship.

The design response organizes learning, shared activity, sanitation, and adult support around connected wings and sheltered circulation. It pairs a long-term campus proposal with immediate improvements to the existing school. The central argument is that the quality of a caring campus depends on the relationships between spaces, routines, and people. A useful design makes those relationships easier to sustain.
""","""
承担日常照顾任务的学校，需要的不只是上课的地方。孩子还需要能够玩耍、等待、寻求帮助和相互陪伴的空间。本研究以湖南省桂阳县苦志育才公益学校为对象，讨论这些日常需求如何转化为校园设计依据。研究材料包括两份成人问卷、35项环境审计、8条观察记录、学校作息表、照片、访谈录音、调研者轨迹及一套建筑设计方案。

分析发现，“有这个空间”和“这个空间好用”之间存在明显差别。两位受访者都把教室列为经常使用的场所，也都认为孩子喜欢操场；但活动支持维度的原始评分均值只有2.71分，是五个维度中最低的。厕所、洗手设施、小组活动场所、可移动家具和等候空间，是材料中较为明确的问题。中文答案中的关键词统计显示，教室与资金反复出现；录音则进一步把空间条件与师资、持续捐助和日常陪伴联系起来。

设计回应以相互连接的建筑翼部和有顶通道为基础，组织学习、共享活动、卫生设施及成人支持。同时，将新校园的长期方案与现有学校可以立即实施的改善结合起来。研究认为，照顾型校园的质量取决于空间、日常安排和人员之间的关系。好的设计，应当让这些关系更容易维持。
""")
add("01 / A campus shaped by everyday care","01 / 从日常照顾理解校园","framework","""
The starting point for this project is a simple question: what makes a school feel usable throughout the day? In a classroom, the answer may involve light, furniture, and teaching. Between lessons, it may involve a nearby toilet, a shaded place to sit, or an adult who is easy to find. For children who also rely on school for practical and emotional support, these ordinary arrangements become part of the educational environment. They deserve the same attention as the main teaching rooms.

Kuzhi Yucai Public Welfare School provides a useful setting for examining this question. The two adults who completed questionnaires described children facing substantial difficulties at home, including limited parental care. One emphasized daily living and learning how to behave with others; the other emphasized emotional support. Their accounts suggest a school whose work extends beyond a conventional lesson schedule. This study therefore considers care as something distributed across the campus, expressed through movement, waiting, conversation, meals, and opportunities to choose an activity.

Two published sources help frame the investigation. Barrett and colleagues linked classroom characteristics, including flexibility and ownership, with learning progress in their study of English primary schools [1]. Their work encourages attention to how pupils experience a room, rather than treating floor area as its only useful measure. The World Health Organization's school sanitation guidance connects the location of toilets with convenient handwashing, privacy, cleaning, and maintenance [2]. Together, these sources support looking at physical provision and everyday operation as related questions.

The investigation asks three questions. Which places matter most in the available accounts of school life? Where do facilities, routines, and support fail to connect smoothly? How can those findings inform the supplied design proposal? The intention is to build a clear chain from field evidence to architectural decisions. This is particularly important where funding is uncertain: an attractive new building should be accompanied by a convincing account of how its rooms and outdoor spaces will be used. The resulting proposal is organized around everyday access, varied activity, and dependable human support.
""","""
本项目从一个简单的问题开始：一所学校怎样才能在一天中的不同时间都方便使用？在教室里，答案可能涉及采光、家具和教学；到了课间，答案可能变成附近的厕所、能遮阴的座位，以及容易找到的老师。对于同时依赖学校获得生活和情绪支持的孩子来说，这些普通安排也是教育环境的一部分，值得像主要教学空间一样被认真对待。

苦志育才公益学校为这一问题提供了具体的研究场景。两位填写问卷的成人提到了孩子在家庭生活中面对的困难，包括父母照顾不足。一位强调日常生活照顾和与人相处，另一位强调情绪支持。由此可见，学校承担的工作超出了常规课程安排。因此，本研究把照顾理解为分布在校园各处的日常行为，包括通行、等待、交谈、就餐，以及选择活动的机会。

两项文献为研究提供了参照。Barrett等人对英国小学的研究，把教室的灵活性、归属感等特征与学习进展联系起来[1]。这一研究提醒我们关注学生如何体验空间，而不只是计算面积。世界卫生组织的学校卫生设施指南，则把厕所位置与洗手、隐私、清洁和维护放在一起讨论[2]。两者共同提示：设施配置与日常运行应当结合考虑。

研究围绕三个问题展开：现有材料中，哪些场所最影响学校生活？设施、作息和照顾之间，哪些联系不够顺畅？这些发现如何转化为设计方案？研究希望建立一条从现场证据到建筑决策的清晰路径。在资金不稳定的情况下，这一点尤其重要：一栋好看的新建筑，还需要说明房间和户外场所将如何被持续使用。因此，方案以日常可达、多样活动和稳定的人员支持为组织原则。
""")
add("02 / Reading the field material","02 / 材料与分析方法","methods","""
The field material dates from September 23 to 26, 2026. Two completed questionnaires contain ten questions each. Both respondents knew the school through work and charitable or volunteer activity; one visited frequently and the other occasionally. Their twenty answers provide informed adult perspectives. The analysis keeps the two accounts separate before comparing their common themes, so that differences in familiarity and priorities remain visible. The unused questionnaire template contributes the question structure, not an additional response.

The environmental audit contains thirty-five items grouped into basic safety, comfort, activity support, care support, and spatial or community connections. Scores were transcribed as marked on the original form. Frequencies and arithmetic means describe the record; the item-level pattern carries the interpretation. Because the form mixes questions about desirable features and possible problems, its raw domain averages are read alongside the wording of each item. The analysis uses neither significance tests nor a combined ranking of school quality.

The questionnaire text was cleaned by removing question wording and keeping only completed answers. This produced twenty response units containing 460 Chinese characters after cleaning. Selected terms were counted as exact substrings. For each term, the analysis records its occurrence count, the number of answers containing it, and whether it appeared in one or both respondents' accounts. English labels translate these Chinese terms. This approach makes a small corpus easy to inspect and avoids allowing repeated question wording to dominate the result.

Other sources add time, context, and spatial detail. Eight observation entries describe activity around 14:00, 15:00, 16:00, and 17:00; 111 photographs document the setting. Three audio files were organized by topic, with overlapping recordings treated as repeated material. The timetable was converted into minutes by activity category. A 486-point KML route describes the researcher's visit. Finally, the map package and nineteen supplied architectural sheets, comprising eighteen building sheets and one site sheet, were examined as design resources. Throughout the analysis, observations of the existing school and decisions within the proposed campus remain identifiable through their source and tense.
""","""
调研材料形成于2026年9月23日至26日。两份已填写问卷各有十道题。两位受访者均通过工作和公益、志愿活动了解学校，其中一位经常到访，另一位偶尔到访。二十条答案提供了知情成人的观察。分析先分别梳理两人的回答，再比较共同主题，保留熟悉程度和关注重点的差异。未填写的问卷模板仅用于理解题目结构，不计入样本。

环境审计包含35个项目，分为基础安全、舒适性、活动支持、照护支持和空间联结五个维度。评分按原表勾选结果录入，以频数和算术均值描述记录，并结合具体题目解释。由于题目既包含对有利条件的询问，也包含对问题的询问，各维度原始均值需要与题意一起阅读。研究不进行显著性检验，也不把这些分数合成为学校质量排名。

问卷文本整理时删除题干，仅保留填写答案，形成20个回答单元，清理后共460个中文字符。选定关键词采用精确子串计数，同时记录出现次数、涉及的回答单元数，以及涉及一位还是两位受访者。英文图表中的词语是中文关键词的译名。这种方法便于核对小规模材料，也避免重复题干影响统计结果。

其他材料补充了时间、环境和空间信息。8条观察记录描述了约14时、15时、16时和17时的活动情况，111张照片记录了现场。3份音频按主题整理，重叠录音视为重复材料；作息表按活动类别换算为分钟；486点的KML轨迹描述了调研者的到访过程。地图包和19张设计图纸——18张建筑图及1张总平面图——用于后续设计分析。全文通过资料来源和时态，区分现有学校的观察与新校园方案的设计判断。
""")
add("03 / What the questionnaires reveal","03 / 问卷中的共同点与差异","keywords","""
Both respondents identified the classroom or teaching-building area as the most frequently used part of the school. Both also named the playground as a place children enjoyed. These answers reveal two different forms of importance: classrooms organize the school day, while open ground offers freedom to play. A design brief should therefore consider the relationship between these settings. Simply enlarging a classroom would not respond to the appeal of outdoor choice, and improving a playground would not resolve difficulties inside the teaching block.

The selected keyword count gives this pattern a compact numerical form. The Chinese term translated as classroom appears seven times across four answers, funding five times across five answers, teaching building four times across three answers, and playground three times across three answers. Each of these terms appears in both questionnaires. School clinic and toilet each occur twice, but each is concentrated in one respondent's account. Frequency therefore helps identify recurring topics; the distribution across people shows whether a topic is shared or raised with particular intensity by one person.

The respondents' priorities add detail that a word count alone would miss. R1 described an inconvenient toilet outside the teaching building, frequent classroom use, and a back area largely occupied by soil, with a small vegetable patch. This respondent favored additional children's activity space. R2 described empty classrooms and unused furniture following a temporary suspension of junior-school teaching, which the respondent attributed to funding difficulties. R2's preferred improvement was the school clinic and reliable access to professional support.

One difference is especially informative. Although R2 mentioned unused classrooms in one answer, a later answer said that no notably underused place had been observed and emphasized that the school's functions were necessary. The two statements reflect different ways of judging usefulness: a room may be temporarily empty while its function is still valued. The design response is consequently broader than filling every vacant room. It should first clarify which activities need support, who will organize them, and which existing spaces can accommodate them. Across the two questionnaires, funding is the shared condition beneath otherwise different spatial priorities.
""","""
两位受访者都认为教室或教学楼区域使用最频繁，也都提到孩子喜欢操场。这两类空间的重要性不同：教室组织了学校的一天，开敞场地则提供自由玩耍的机会。设计任务因此需要关注两者的联系。单纯扩大教室，不能回应孩子对户外选择的需要；仅改善操场，也不能解决教学楼内部的不便。

关键词统计把这一特点呈现得更清楚。“教室”出现7次，涉及4条回答；“资金”出现5次，涉及5条回答；“教学楼”出现4次，涉及3条回答；“操场”出现3次，涉及3条回答。这四个词都出现在两份问卷中。“校医室”和“厕所”各出现2次，但分别集中在一位受访者的回答里。因此，次数可以帮助识别反复出现的话题，而受访者分布则说明话题是共同关注，还是某个人着重提出的问题。

两位受访者的改善建议补充了词频无法表达的细节。R1提到教学楼外的厕所使用不便、教室使用频繁，以及后坪大部分为土堆、只有小片菜地的情况，优先希望增加儿童活动空间。R2提到初中教学暂时停止后出现的空教室和闲置家具，并将其与资金问题联系起来；其首选改善项目是校医室和稳定的专业支持。

其中一处差异很有意义：R2在一道题中提到空教室，后面却表示未发现明显低利用率的空间，并强调学校各项功能都有必要。这反映了两种不同的判断角度：房间暂时空着，并不代表其功能没有价值。因此，设计目标不宜只是填满所有空房间，而应先明确需要支持什么活动、由谁组织，以及哪些现有空间能够承载这些活动。两份问卷提出的空间重点不同，但资金都是背后的共同条件。
""")
add("04 / Facilities and the freedom to use them","04 / 设施与使用机会","audit","""
The audit records 118 points across thirty-five items, giving a raw mean of 3.37 out of 5. Care support has the highest domain mean, 3.83, followed by basic safety at 3.75, comfort at 3.44, spatial connections at 3.00, and activity support at 2.71. The spread is more useful than the overall average. Nineteen items were marked 4 or 5, while ten were marked 1 or 2. The campus record therefore contains both considerable provision and several sharply defined weaknesses.

Activity support illustrates this unevenness. Open activity ground received 5, reading space 4, and a place for being alone 4. Small-group space, movable furniture, and permission for children to arrange or change their surroundings each received 1. These results suggest that the missing element is not simply open area. Children may have access to a large field without having many ways to use the edges of a classroom, form a small group, or adapt a setting to a chosen activity.

A similar distinction appears in comfort and care. Shade, shelter, ventilation, and drinking-water provision received high marks, while toilets, handwashing, and quiet areas received 1. Visibility of children and the ability to find adults received 5, as did a psychological conversation space. Waiting space received 1 and medical or temporary-rest provision 3. The different scores for quiet areas and private conversation space should be retained: a designated room can exist while everyday opportunities for calm remain limited elsewhere.

These findings favor specific interventions over a generalized description of the school as lacking facilities. Toilets and handwashing should be considered together. Seating and small-group settings should be distributed near ordinary routes. Waiting should have a recognizable place, and adult presence should remain easy to locate. Some audit questions, including those about slippery surfaces and care blind spots, describe possible problems rather than positive amenities; their raw marks are preserved in the appendix. The strongest design conclusions come from the clearly worded low-scoring items that also connect with questionnaire answers or observations.
""","""
35项审计记录合计118分，原始均值为3.37分。照护支持维度均值最高，为3.83；其次是基础安全3.75、舒适性3.44、空间联结3.00，以及活动支持2.71。相比总均值，分布更能说明问题：19项被标为4分或5分，10项被标为1分或2分。校园既有一定设施基础，也有几个比较集中的薄弱环节。

活动支持最能体现这种不均衡。开放活动场地为5分，阅读空间和可以独处的空间均为4分；小组活动空间、可移动家具，以及允许儿童布置和改变环境，均只有1分。这说明问题并不只是场地面积不足。孩子可能拥有一块大操场，却缺少利用教室边角、组成小组或根据活动调整环境的机会。

舒适性和照护支持也存在类似差别。遮阳、避雨、通风和饮水条件评分较高，而厕所、洗手设施和安静区域均为1分。成人看见儿童、儿童找到老师以及心理交流空间均为5分，等候空间只有1分，医疗或临时休息空间为3分。安静区域与心理谈话空间的差异应当保留：有一间专门房间，并不意味着校园其他地方也方便安静地停留。

这些发现更适合转化为具体改善，而不是笼统地说学校缺少设施。厕所与洗手点需要一起考虑；座位和小组活动场所应靠近日常通行路线；等候应有清楚的位置，成人支持也应容易找到。审计中有关湿滑、照护盲区等题目询问的是可能存在的问题，附录保留了它们的原始标记。最明确的设计依据，来自题意清楚、分数较低，而且能够与问卷或观察相互印证的项目。
""")
add("05 / The school day changes the map","05 / 一天中的空间变化","time","""
The timetable, effective from September 1, 2026, runs from rising at 06:30 to lights out at 21:00, a daytime window of 870 minutes. Lessons, morning reading, and evening study together occupy 390 minutes, or 44.8 percent of that window. Meals occupy 160 minutes, organized activity 90, the midday rest 80, and eye exercises 30. The remaining 120 minutes lie between listed activities. These intervals should remain visible because movement, preparation, informal contact, and waiting also need space.

The schedule explains why the classroom is so prominent in the questionnaires, but observation shows that campus use is not fixed. Around 14:00, approximately twenty children were recorded in a teacher-led outdoor activity, while corridors were relatively quiet. Around 15:00, the field was empty and each observed corridor floor held roughly twenty to twenty-five children talking or playing in small groups. An office entry recorded two or three students with five teachers. These are separate snapshots of settings, not a count of distinct participants.

Around 16:00, the field and corridors were again relatively quiet during lessons. Around 17:00, activity gathered in corridors and the front or side play areas, including table tennis. The notes also described uneven ground, aging equipment, and thin supervision in those areas. The observation times were recorded approximately, so they are best read as a sequence of changing uses rather than a minute-by-minute test of the timetable. Their value lies in showing which thresholds become busy as the school day changes.

This temporal pattern has direct design consequences. A corridor must accommodate movement but may also become an informal social room. A place beside a classroom may be more usable during a short break than a distant field. The 17:00 to 17:50 activity period can support longer outdoor sessions, while smaller pauses require nearby choices. The proposal therefore pairs large shared grounds with modest settings close to lessons: a seat, a reading edge, a small-group table, and a clear route to washing and toilets. These additions give different parts of the timetable an appropriate spatial setting.
""","""
2026年9月1日起执行的作息表，从6:30起床到21:00熄灯，覆盖870分钟。课堂、晨读和晚自习合计390分钟，占44.8%；就餐160分钟，组织性活动90分钟，午休80分钟，眼保健操30分钟。其余120分钟分布在表列活动之间。这些间隙同样需要被看见，因为通行、准备、非正式交流和等待也需要空间。

作息安排解释了教室为何在问卷中如此突出，但观察也表明，校园的使用并不是固定的。约14时，操场记录到约20名儿童参加老师带领的活动，走廊较安静。约15时，操场无人，而被观察的各层走廊约有20至25名儿童聊天或小范围玩耍；办公室的一条记录则有2至3名学生和5名教师。这些是不同场所的观察片段，不能相加作为独立参与人数。

约16时，上课期间的操场与走廊再次较为安静。约17时，活动集中到走廊及楼前、楼侧场地，包括乒乓球等。记录同时提到了地面不平、器材老化和看护力量偏少。观察时间比较粗略，适合用于理解一天中活动的变化，而不是逐分钟核对课程表。它们的价值在于显示：随着作息转换，哪些过渡地带会变得繁忙。

这一规律对设计有直接影响。走廊既承担通行，也可能成为非正式交往空间；短课间里，教室旁的场所可能比远处操场更方便。17:00至17:50的活动时段适合较长时间的户外活动，而更短的间歇需要近处的选择。因此，方案把大面积公共场地与靠近教室的小空间结合：一处座位、一段阅读边界、一张小组桌，以及通往洗手点和厕所的清晰路线，让不同长度的时间都有合适的空间。
""")
add("06 / Care depends on people as well as rooms","06 / 空间背后的人员支持","care","""
The recorded conversations extend the questionnaires by describing how the school keeps everyday support going. Recurring topics include small monthly donations, companionship, living habits, contact with former students, holiday arrangements, and supervision at night. These topics matter architecturally because they explain when a space needs to remain available and who gives it purpose. A conversation corner is useful when someone can listen; a shared room becomes an activity setting when a teacher or volunteer can organize a session.

Funding appears in both written accounts, but the recordings give a more textured picture than a simple absence of support. They describe efforts to build continuing monthly giving. The issue is therefore the stability and adequacy of resources over time. Similarly, the discussion of dance, science, art, and music points toward a need for people able to teach activities. Providing another named room would only partly address that need. Flexible spaces should be paired with a realistic schedule, storage, materials, and a person responsible for opening and using them.

Emotional support also emerges through ordinary relationships. The recordings discuss a home-like atmosphere, communication after students leave, teacher learning, and outside assistance. These themes suggest that care should be present along familiar daily routes, rather than confined to a specialized room at the edge of the campus. At the same time, a child seeking a private conversation should not have to do so in front of a large group. The design can balance easy access to an adult with a small, calmer place for a conversation.

This reading leads to a practical design rule: every important support space should be matched with an operating arrangement. A rest room needs a named adult contact and a clear route to outside help. A shared activity room needs a weekly program and simple storage. An entrance waiting area needs a connection to reception. A courtyard needs someone able to oversee its busy periods. These arrangements are as much a part of the proposal as walls and roofs, because they determine whether the campus can deliver the everyday support described in the field material.
""","""
录音补充了问卷，说明学校如何维持日常支持。反复出现的话题包括小额月捐、陪伴、生活习惯、与离校学生保持联系、假期安排和夜间照看。这些内容与建筑设计有关，因为它们说明空间在什么时候需要开放，以及谁赋予空间实际用途。有人愿意倾听，谈话角才有意义；有老师或志愿者组织，共享房间才能成为活动场所。

资金出现在两份书面回答中，但录音呈现的情况比“缺乏支持”更具体。学校已经在尝试持续月捐，因此问题是资源能否长期稳定、是否足够。舞蹈、科学、美术和音乐等讨论，也指向能够开展课程的人。再增加一间有名称的房间，只能回应其中一部分。灵活空间需要同时配合时间安排、储物、材料，以及负责开放和使用的人。

情绪支持也通过普通关系体现出来。录音谈到像家一样的氛围、学生离校后的联系、教师学习和外部帮助。这些内容说明，照顾应当出现在熟悉的日常路线旁，而不只集中在校园边缘的一间专用房内。同时，希望私下交流的孩子，也不应该必须在一大群人面前提出请求。设计需要兼顾容易找到成人，以及能稍微安静下来交谈的小空间。

由此可以提出一条实际的设计原则：重要的支持空间，都应配有相应的运行安排。临时休息室需要明确的成人联系人和外部求助路径；共享活动室需要每周活动计划和简便储物；入口等候区需要与接待点相连；庭院则需要有人在活动集中时段照看。这些安排与墙和屋顶同样属于方案的一部分，因为它们决定校园能否持续提供调研材料中描述的日常支持。
""")
add("07 / A rural site and its connections","07 / 乡村场地与外部联系","site","""
The supplied map package contains a site polygon, a study boundary, road polygons, and forty-six surrounding settlement polygons. The data use WGS 84 / UTM zone 49N, allowing distances and area to be calculated in meters. The mapped site polygon covers approximately 29,407 square meters, or 2.94 hectares. This figure describes the digitized parcel in the supplied layer. The context map uses the parcel and neighboring fabric to explain the site's relationships, without turning road polygons into an unsupported transport model.

The researcher's KML file records 486 points over approximately 119.9 minutes on September 23. Its recorded length is about 4.21 kilometers. The route helps locate the field visit within the local setting, but its stops and gaps make it unsuitable as a map of children's daily movement. For the design, its main value is to keep the investigation attached to a real place. The portfolio therefore presents the geographic context separately from the proposed circulation diagrams.

Field notes also describe connections beyond the campus: roughly thirty-five kilometers to the county center, around 3.5 kilometers to the town or public transport, and about four kilometers to a health clinic. These are field-record estimates rather than measured routes. Read alongside the questionnaire concern about medical support, they make access to outside services an important part of the brief. Reception, waiting, and the handover between school staff and visiting helpers deserve a clear arrangement at the entrance.

The supplied site plan groups the connected building wings beside outdoor sports grounds, with additional open land along the lower edge of the drawing. This offers a useful distinction between intensive daily spaces and land that can be developed gradually. The proposal keeps the campus legible through a recognizable arrival point, a connected learning core, and differentiated outdoor areas. It also gives maintenance a role in the landscape strategy: extensive decorative planting would add work, while simple planted edges and repairable surfaces can support a more manageable campus setting.
""","""
提供的地图包包含场地边界、研究范围、道路面和46个周边聚落面。数据采用WGS 84 / UTM 49N坐标系，可以米为单位计算距离和面积。场地面面积约29,407平方米，即2.94公顷。这一数值对应所提供图层中的数字化边界。区位图通过场地与周边建设肌理解释空间关系，不把道路面数据当作未经建立的交通网络模型。

调研者的KML文件在9月23日约119.9分钟内记录了486个点，文件记录长度约4.21公里。轨迹有助于将调研放回当地环境，但其中的停留和间断使它不适合作为儿童日常活动路线。对于设计来说，其主要价值是明确研究发生的实际地点。因此，作品集把地理环境图与方案内部的流线示意分别呈现。

现场记录还描述了校园之外的联系：距县城约35公里，距镇区或公共交通约3.5公里，距卫生院约4公里。这些是现场估计，而非测绘路线。结合问卷对医疗支持的关注，可以看出外部服务的进入也是设计任务的一部分。入口应清楚安排接待、等候，以及学校工作人员与到访服务人员之间的交接。

提供的总平面将相互连接的建筑翼部与户外运动场地并置，图面下方还有其他开敞用地。这使高频日常活动空间与可以逐步利用的土地形成区分。方案通过明确的到达点、连贯的教学核心和有所分工的户外场所，提高校园的可辨认性。景观策略同时考虑维护：大面积装饰种植会增加工作，而简单的绿化边界与易修补地面，更有利于持续管理。
""")
add("08 / Turning findings into a spatial brief","08 / 从调研发现形成设计任务","translation","""
The design brief follows four linked priorities. First, make everyday essentials easy to reach. The questionnaire description of an inconvenient toilet and the low audit marks for sanitation point toward short, understandable connections between teaching rooms, washing, and toilets. WHO guidance supports considering convenient access, privacy, and maintenance together [2]. In the proposal, sanitation cores near the junctions of the learning wings form useful anchors. Their approach routes should stay legible, with washing and cleaning arrangements developed as part of the same decision.

Second, provide a range of activity scales. The field already supports large-group play, while smaller settings receive weaker audit marks. The proposal therefore combines sports grounds and shared courtyards with places for two or three children to read, talk, or work. Movable tables and accessible storage can allow a room to change between supervised activities. This applies the idea of flexibility discussed by Barrett and colleagues [1] at a modest, practical scale: the aim is to make different uses possible without rebuilding a room each time.

Third, put adult support within ordinary circulation. Offices, consultation spaces, reception, and temporary rest should relate to places children already pass. Clear sightlines can help adults remain aware of shared areas, while thresholds and small seating positions can support informal contact. Privacy requires its own arrangement: a waiting child should be able to sit near support without becoming the focus of a busy corridor. This is a matter of adjacency, doorway position, and use, as well as room size.

Fourth, make shared facilities manageable. Dining, meeting, and activity spaces can support several parts of the school day, but the operating schedule must distinguish public visits, school routines, and quieter periods. The entrance should make that distinction understandable without isolating the school from visitors. These four priorities connect the evidence to decisions at different scales, from a handwashing point to the whole site. They also establish a test for the portfolio: each highlighted design move should answer an observed need, a respondent priority, or a clear requirement of daily operation.
""","""
设计任务由四个相互联系的重点构成。第一，让日常必需设施容易到达。问卷中的厕所不便，以及审计中卫生设施的低分，都指向教室、洗手点和厕所之间简短、清晰的联系。世界卫生组织指南也把便利、隐私和维护一起考虑[2]。在方案中，教学翼部连接处附近的卫生核心可以成为日常服务节点，通向它们的路线、洗手安排和清洁方式应一起完善。

第二，提供不同规模的活动选择。现场已有支持集体活动的大场地，而小尺度活动条件评分较低。因此，方案将运动场、共享庭院与两三个人阅读、交谈或合作的地方结合。可移动桌椅和方便取用的储物设施，可以让同一房间承载不同活动。这是在具体而朴素的层面运用Barrett等人讨论的灵活性[1]：不必每次改建房间，也能容纳不同用途。

第三，把成人支持放在日常路线附近。办公室、咨询空间、接待和临时休息，应与孩子平时经过的地方建立联系。清晰的视线有助于成人留意共享场所，门口和小型座位则可以支持自然交流。隐私还需要单独安排：等待帮助的孩子，应能坐在支持空间附近，而不成为繁忙走廊中的焦点。这既涉及面积，也涉及相邻关系、门的位置和使用方式。

第四，让共享设施便于运行。餐厅、会议与活动空间可以支持一天中的不同安排，但使用时间应区分访客到校、日常教学和安静时段。入口需要让这些关系容易理解，同时保持学校与外界的联系。四个重点把证据连接到从洗手点到整个场地的不同尺度，也成为作品集的判断标准：每一项被强调的设计，都应回应现场需求、受访者重点或明确的运行需要。
""")
add("09 / Reading the proposed architecture","09 / 建筑方案的空间组织","program","""
The supplied plans establish two long learning wings connected by a perpendicular spine, together with a lower wing for dining and collective activities. The main connected blocks extend through four levels, while the lower wing has three occupied levels and a roof shown on the fourth-floor plan. This arrangement creates a sequence of shared outdoor spaces and covered connections. The portfolio develops the presentation around that existing geometry, so that its diagrams and visual compositions remain consistent with the architectural drawings.

The ground floor combines a library, an entrance hall, school-history display, reception and administrative rooms, multifunction classrooms, and dining or catering functions. These uses suggest a relatively public level that can introduce visitors to the school while supporting daily routines. The entrance hall can organize arrival and waiting; the library and shared rooms can offer activities near the main circulation. Dining should have an understandable relationship to movement through the campus, with service tasks organized so that they do not overwhelm children's routes.

On the upper floors, multifunction classrooms continue in the long wings, while offices occupy the connecting spine. The plans also include rest, consultation, and psychological-support rooms in a smaller suite. Their relationship offers a starting point for locating adult help near teaching. The third level of the lower wing contains meeting and activity rooms, adding a different scale of collective use. The portfolio identifies these source functions and then marks suggested improvements, such as nearby waiting and adaptable furniture, as design development.

The elevations and sections give the campus a consistent architectural language: pitched gray roofs, pale walls, repeated bays, stone-textured bands, and warm vertical screens. The presentation retains that language while reducing distracting scenery around the renderings. Drawings emphasize the rhythm of occupied rooms, sheltered circulation, and changes between the wings. Material choices are discussed through everyday use, including cleaning, repair, and the feel of places where children gather. The architectural argument rests on these relationships, rather than on a claim that a particular facade style will itself improve learning.
""","""
提供的平面以两条长教学翼部和一条垂直连接体为骨架，另有较低的餐饮与集体活动翼部。主要连体建筑共四层，较低翼部有三层使用空间，在四层平面中显示为屋面。这一组织形成了共享户外空间和有顶联系的序列。作品集围绕原有几何关系展开，使分析图和效果图构成与建筑图纸一致。

首层包含图书室、门厅、校史展示、接待与行政房间、多功能教室，以及餐饮后勤功能。这些用途使首层具有较强的公共性，既向到访者介绍学校，也支持日常运行。门厅可以组织到达与等候，图书室和共享房间可以在主要通行路线附近提供活动。餐厅应与校园通行建立易于理解的联系，同时妥善安排后勤工作，减少其对儿童路线的影响。

上部楼层的长翼部继续布置多功能教室，连接体中安排办公室；较小的房间组团中还有休息、咨询和心理辅导空间。这种关系为在教学附近安排成人支持提供了基础。较低翼部三层的会议和活动房间，则提供了另一种集体使用尺度。作品集先标明原图功能，再把邻近等候、可调整家具等建议作为进一步的设计发展。

立面与剖面呈现了统一的建筑语言：灰色坡屋顶、浅色墙面、重复开间、石材质感分带及暖色竖向格栅。排版保留这些特征，同时减少效果图周边景物的干扰。图纸突出房间序列、有顶通行以及翼部之间的变化，材料讨论则落在清洁、修补和儿童聚集处的空间感受上。建筑论证依靠这些具体关系，而不是把某种立面风格直接等同于学习效果。
""")
add("10 / A sequence that can be maintained","10 / 可以持续推进的实施次序","phasing","""
The existing school and the long-term proposal operate on different timescales. Immediate improvements can address daily inconvenience while a larger project is developed. A first stage should concentrate on the items repeatedly connected to use: toilet and handwashing access, uneven activity surfaces, basic seating, waiting, and simple storage. An available room or corridor edge can be tested for small-group activity before permanent construction decisions are made. This gives teachers and children a chance to show what is useful through ordinary use.

A second stage can establish a repeatable program. A small set of movable furniture, durable materials, and an agreed weekly schedule can support reading, art, science, or group activities in shared rooms. The priority is to match activities with the adults able to lead them. The donation efforts described in the recordings could support clearly explained, bounded improvements whose ongoing needs are visible. Cleaning, consumables, repairs, and staff time belong in the planning conversation alongside the initial purchase or construction.

A third stage develops the connected campus as a coordinated project. Floor plans, outdoor areas, service access, and daily supervision should be considered together. The proposed teaching, dining, and support rooms need an operating plan that identifies when they are used and who takes responsibility. Outdoor work can proceed in manageable portions, beginning with surfaces and shaded edges near the most frequently used routes. This sequence allows the architectural vision to remain ambitious while keeping its individual steps understandable.

Evaluation can also stay simple. The school could record whether toilets and washing points are ready at the start of the day, which small-group settings are used during breaks, whether children can find the responsible adult, and how often scheduled activities take place. Short conversations with pupils can add their preferences to the adult accounts gathered here. Repeating the same observations before and after a small change would reveal whether it fits school life. These proposed checks are useful because they ask about use and continuity, the two concerns that run through the field material.
""","""
现有学校的改善与新校园方案具有不同的时间尺度。在推进较大项目的同时，可以先处理日常不便。第一阶段宜围绕反复影响使用的问题展开：厕所和洗手条件、活动地面不平、基础座位、等候和简便储物。现有房间或走廊边缘可以先试行小组活动，让教师与儿童通过实际使用，帮助判断哪些安排值得保留。

第二阶段建立能够重复执行的活动计划。少量可移动家具、耐用材料和约定好的每周时间，可以支持共享空间中的阅读、美术、科学或小组活动。重点是把活动与能够带领它的成人对应起来。录音中提到的持续捐助，可以围绕范围清楚、后续需求明确的改善项目展开。清洁、耗材、修补和人员时间，应与初次购买或建设费用一起考虑。

第三阶段将连体校园作为协调发展的整体。楼层平面、户外空间、后勤进入和日常看护需要同时考虑。教学、餐饮及支持房间应有对应的运行安排，明确何时使用、由谁负责。户外改善可以分段进行，先处理高频路线附近的地面和遮阴边界。这样的次序既保留完整设计愿景，也让每一步都便于理解和落实。

后续观察也可以保持简单。学校可以记录每天开始时厕所和洗手点是否可用、课间哪些小组空间有人使用、孩子是否容易找到负责成人，以及安排好的活动实际开展了多少次。与学生的简短交谈，可以补充本次成人问卷没有直接覆盖的偏好。在小改善前后重复同样的观察，有助于判断安排是否适合学校生活。这些建议紧扣材料中贯穿始终的两个问题：空间是否被使用，以及使用能否持续。
""")
add("11 / Conclusion","11 / 结论","conclusion","""
The field material points toward a campus problem that is more specific than a shortage of buildings. Classrooms structure the day, the playground offers valued freedom, and staff provide visible care. Yet smaller settings, sanitation access, waiting, and flexible use do not connect as smoothly. The questionnaire, audit, timetable, and observations each show a different part of this pattern. Together they support a design brief centered on the spaces between formal activities as well as the rooms assigned to them.

The proposed architecture offers a clear framework for responding. Connected learning wings can shorten the relationship between teaching and support. The spine can make adult help easier to find. Dining, activity rooms, and courtyards can introduce different scales of shared life. These possibilities become convincing when they are paired with practical decisions about furniture, opening times, cleaning, supervision, and staffing. The most useful improvements are those that make a familiar part of the day work better.

For this school, a caring campus can be understood through three everyday questions: can a child reach what is needed, find someone to help, and choose a suitable place to spend time? The research and portfolio use those questions to connect fieldwork with design. The result is a proposal that gives ordinary routines architectural attention, while leaving room for the school's teachers and children to shape how their campus is used.
""","""
材料指向的校园问题，比“缺少建筑”更加具体。教室组织日常时间，操场提供受欢迎的自由活动，工作人员也形成了可见的照顾。但小尺度场所、卫生设施、等候与灵活使用之间的联系仍不够顺畅。问卷、审计、作息和观察分别呈现了这一现象的不同侧面，共同支持一种设计思路：既关注有明确用途的房间，也关注正式活动之间的过渡空间。

提供的建筑方案为回应这些问题建立了清晰骨架。相互连接的教学翼部可以拉近教学与支持的关系，连接体有助于寻找成人，餐饮、活动房间与庭院则能提供不同尺度的集体生活。这些可能性需要通过家具、开放时间、清洁、看护和师资安排变得具体。最有价值的改善，是让某一段熟悉的日常生活变得更顺畅。

对于这所学校，照顾型校园可以通过三个普通问题来理解：孩子能否到达所需设施，能否找到帮助，能否选择合适的地方停留？论文与作品集以这些问题连接调研和设计，让普通的生活安排得到建筑层面的重视，也给教师和儿童留下继续塑造校园使用方式的空间。
""")

refs=[
{"id":"1","en":"Barrett, P., Davies, F., Zhang, Y., & Barrett, L. (2015). The impact of classroom design on pupils' learning: Final results of a holistic, multi-level analysis. Building and Environment, 89, 118-133. DOI: 10.1016/j.buildenv.2015.02.013.","zh":"Barrett, P., Davies, F., Zhang, Y., & Barrett, L.（2015）. The impact of classroom design on pupils' learning: Final results of a holistic, multi-level analysis. Building and Environment, 89, 118-133. DOI: 10.1016/j.buildenv.2015.02.013."},
{"id":"2","en":"Adams, J., Bartram, J., Chartier, Y., & Sims, J. (Eds.). (2009). Water, sanitation and hygiene standards for schools in low-cost settings. World Health Organization. ISBN 978-92-4-154779-6. Sections 3.8-3.9 and Guideline 5.","zh":"Adams, J., Bartram, J., Chartier, Y., & Sims, J.（编）（2009）. Water, sanitation and hygiene standards for schools in low-cost settings. 世界卫生组织. ISBN 978-92-4-154779-6. 第3.8至3.9节及指南5。"},
{"id":"F1","en":"Student fieldwork collection (September 23-26, 2026). Two completed adult questionnaires, environmental audit, observation notes, photographs, school timetable, and KML field route. User-provided primary material.","zh":"学生调研资料（2026年9月23日至26日）：两份成人问卷、环境审计、观察记录、照片、作息表及KML调研轨迹。用户提供的一手材料。"},
{"id":"F2","en":"School interview recordings (September 2026). Two M4A files and one MP3 file; topic-based reading with overlapping passages consolidated. User-provided primary material.","zh":"学校访谈录音（2026年9月）：两份M4A和一份MP3文件，按主题整理并合并重叠内容。用户提供的一手材料。"},
{"id":"D1","en":"Supplied campus proposal. Building plans, elevations and sections (18 sheets); site plan (1 sheet); map package; four architectural renderings. Used as design sources.","zh":"提供的校园设计方案：建筑平立剖18张、总平面图1张、地图包及4张建筑效果图。作为设计来源使用。"}
]

data={"title_en":"Everyday Care, Spatial Choice","title_zh":"日常照顾与空间选择",
 "subtitle_en":"Field Research and a Campus Design Proposal for Kuzhi Yucai Public Welfare School, Guiyang County",
 "subtitle_zh":"桂阳县苦志育才公益学校调研与校园设计方案",
 "sections":sections,"references":refs}
wc=len(re.findall(r"\b[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*\b",' '.join(p for s in sections for p in s['english'])))
data['word_count']=wc
(OUT/'工作文件'/'manuscript.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for lang,key in [('EN','english'),('ZH','chinese')]:
    lk='en' if lang=='EN' else 'zh'
    md=f"# {data['title_'+lk]}\n\n{data['subtitle_'+lk]}\n\n"
    for s in sections: md+=f"## {s[lk]}\n\n"+'\n\n'.join(s[key])+'\n\n'
    md+=('## References\n\n' if lang=='EN' else '## 参考资料\n\n')
    md+='\n\n'.join(f"[{r['id']}] {r[lk]}" for r in refs)
    (OUT/f'Paper_{lang}.md').write_text(md,encoding='utf-8')
print('English manuscript word count:',wc)
