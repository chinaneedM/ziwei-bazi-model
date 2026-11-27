# 天问15FF-Q｜核心规则篇页与图谱对接：首组未结项检查点（2026-11-27）

## 范围和恢复

基线 HEAD 21237f54935d9531064ed345a5ec20b65161efc7，tree 94c08114c4657008cb465f90b6265d9bb9226da8；R2六绑定逐一符合精确树。连续性运行45969555994成功，clean-training-system 45969552371仍运行；不宣告全CI通过。当前状态1.1570.0，Matrix222/222，来源1488/276，图584/424，58开放风险含五P0。前一正式成果15FF-P；本文件为15FF-Q的部分工作检查点，不是完成批次，不改权威状态或恢复视图、不新增来源/节点/关系、不重开算法。后续从本文件继续而不是重复15FF-P。

本次复用并重新读取既有原页考据报告（不是本轮重新逐字核读扫描）。Matrix blob 5919e1b6bbc3c4b150507c41a13ccc9e13d20f17、graph blob dcfeb1ea164965d5ffb1cc1bb5babcc55ff6b76d完整解析。P0五项均复核派生条目；0001/0002仍阻塞原页获取、0005六组控制5/6而最终裁决0/6、0006夜子候选、0007历法坐标适配器均未关闭。

## A. 紫微本命与主星：第一组证据链

| Matrix ID（现有状态） | 已有作品、物件、数字页及定位 | 已有图谱与下一步边界 |
|---|---|---|
| HPA-ZIWEI-002（HISTORICALLY_SUPPORTED） | 南阳堂七卷《全书》，子060-0001，卷三镜像0073–0075；13ZZ报告核读〈安身命例〉寅起正月、至生月再以子时逆命顺身；闰正月作二月例 | PHYSICAL-COPY-NAJ-NANYANGTANG-Z060-0001 → TG-E0298 ATTESTS → PASSAGE-NAJ-NANYANGTANG-J3-CHART-PLACEMENT；下一步独立身命函数、闰月输入范围，图中尚须核验是否已存在相应机械族，刊年未定 |
| HPA-ZIWEI-003（HISTORICALLY_SUPPORTED） | 同件卷三〈安十二宮例〉，镜像0074，13ZZ | 同一篇页节点和E0298；宫名/排列应分开于宫干及三环，不能从同页推定传承 |
| HPA-ZIWEI-004（HISTORICALLY_SUPPORTED） | 同件卷三〈起五寅例〉，13ZZ页组73–75；Matrix为S01:ZZQS-A-1755/1756 | 同篇页节点，先补精确页及五组干支映射；不可直接将四柱五虎遁当作该版本宫干全证 |
| HPA-ZIWEI-005（HISTORICALLY_SUPPORTED） | 南阳堂卷三纳音，13ZZ页组73–75；Matrix另引S01局数、纳音表；《捷览》五局生日受读见15AM | 南阳堂篇页存在；五局数、命宫干支纳音及安星输入分开核验；不因见纳音就声称整套局数规则已逐字证明 |
| HPA-ZIWEI-006（HISTORICALLY_SUPPORTED） | Matrix《捷览》CH20/22（受读定位）；1581金陵王洛川四卷上海子4051书目与2016开卷影印分开；南阳堂卷三星序页0075 | PASSAGE-JIELAN-1581-OPENING-2016-FACSIMILE仅开卷、星图，未绑定CH20/22目标页；南阳堂篇页可支持局部星序；不得升级为1581原印目标字 |
| HPA-ZIWEI-020（HISTORICALLY_SUPPORTED） | Matrix《捷览》CH22；南阳堂0075所见两组星序 | 复用E0298；北斗/南斗方向、相对偏移需依原页分别核对，未建立同版同法关系 |

反例护栏：15AM对照《捷览》受读金四局初三紫微丑、初八紫微卯，与《续道藏》卷一年支寅则紫微酉。后者原页依据14I，NLC892第167册p27–32，DIGITAL-SURROGATE-NLC892-411999007380-XUDAOZANG-ZIWEI → TG-E0310 ATTESTS → PASSAGE-XUDAOZANG-ZIWEI-J1-ZHAODAN-FEIXING。两式独立，1607为收录层而非成书年；p32极性异文未裁；前者1581目标原刻未证。不得将十八飞星并入十四主星族。朝鲜《玄藪》与乙亥字《紫微数》另有局数起例及太极/天库实例，不能因均有局数而合并。

## B. 四柱构造与跨系统配干：第二组证据链

| Matrix ID（现有状态） | 已有作品、版本、数字页 | 图谱与限定 |
|---|---|---|
| HPA-BAZI-017（HISTORICALLY_SUPPORTED） | 方氏《三车一览命书详论》1261序文层，BL 15212-e.8乙亥字印本系，实际印年未定；韩国国图CNTS-00109637789第1份p42〈起月例〉，14W；1600喬山堂《渊海》NCL06593 p3〈論年上起月法〉，14T | DIGITAL-SURROGATE-NLK-FANG-SANCHE-CNTS-00109637789 → TG-E0353 ATTESTS → PASSAGE-BL-FANG-SANCHE-J1-P42-STEM-STARTS；配干不等于节气定月，两个物件/版次不得归一 |
| HPA-BAZI-020（HISTORICALLY_SUPPORTED） | 14W同页〈起時例〉；14T NCL06593 p3〈論日上起時法〉，p160庚子刊记 | PHYSICAL-COPY-NCL-06593-YUANHAI-ZIPING → TG-E0330 ATTESTS → PASSAGE-YUANHAI-06593-J1-DAY-TO-HOUR → TG-E0332 ATTESTS → MECHANICAL-RULE-YUANHAI-1600-DAY-STEM-TO-HOUR。E0333另有NLC-2642数字替身支持同一篇章节点，不能由此断定NLC与NCL同一物件 |
| HPA-ZT-007 / HPA-ZTEMP-002（均HISTORICALLY_SUPPORTED） | Matrix指《五行精纪》卷28起月建，四柱与紫微共享配干算子可作旁证比较；14W p42已核五组 | 只支持给定年干/月支的配干关系；不支持紫微流月宫序、斗君或闰月政策，不能自动新增紫微采用边 |

已核配干例重放（来自14T/14W的既有实值，不是新增史料）：丁日子时庚子，丑辛丑，寅壬寅；甲年亥月乙亥、戊日申时庚申。给定日干与支位下的算子可复现，晚子时日干、月界、年界未被解决。古籍中的年本、日主、命宫不能因同名而机械归一。

## C. 既有原页记录索引与恢复边界

- 13ZZ：TIANWEN-13ZZ-WENYUANGE-NANYANGTANG-FOLIO-COLLATION-R1.md（68ec8a9f28cda40bf1b1850c3a02070038d3f30f），EXT-TIANWEN-13ZZ-NANYANGTANG-OPENING-J3-VISUAL。
- 14T：TIANWEN-14T-CHUOGENG-ANMING-YUANHAI-HOUR-STEM-R1.md（e5ce73d30fa33edcee7239991034a62bd860e5c9），EXT-TIANWEN-14T-NCL-YUANHAI-06593。
- 14W：TIANWEN-14W-XUANSOU-ORIGINAL-AND-FANG-SANCHE-R1.md（1b3427b7b11f305e6ff5f587de5083c00d3d42af），EXT-TIANWEN-14W-BL-FANG-SANCHE-CNTS-00109637789-SCAN。
- 15AM：TIANWEN-15AM-JIELAN-FIVE-BUREAU-BIRTHDAY-VS-XUDAOZANG-YEAR-BRANCH-ZIWEI-R1.md（44f4caa3585c52b1d6aec03779e87adc3a8b149e）。

本检查点覆盖10个既有Matrix ID的初步映射；没有宣告对应族全部闭合。尚未完成：逐项定位原页和来源登记、其余本命与十二宫、紫微大限及动态层、四柱十神/藏干/大运/小运/神煞；随后按证据补图谱，并复核58项风险及第一阶段门槛。新增来源查重未启动，因为本次只复用已有证据。下一轮必须检查本文件之后的远端提交和精确HEAD CI；现有状态指向15FF-Q，不得把本检查点误当正式完成批次。

transmission_impact: NONE（证据交叉索引；不新增传承或同本关系，不更改Matrix历史裁决）。排盘CLOSED，预测/AI解释OUT_OF_SCOPE。


## D. 第二组检查点：紫微动态、四柱运限、派生字段与神煞（2026-11-27）

基线HEAD 9632a984b4ed948f8c87aaf86661e16b0d8d7f00，tree 6fb5a73d8df40cea569609c3e20ea95f5dfcb11b。权威六绑定不变；Matrix、graph、风险台账（58 issues，1001 checkpoints）及根647来源完整解析。基线Actions20项，读取时19成功、clean-training-system运行中；当前HEAD未见连续性运行，不能使用前HEAD的成功代替。仅复用已登记证据，未登记新来源，未穷举276分片，不作全库无命中判断。

### D1. 前向勘误：15FF-P 四柱大运模块

15FF-P 将未入产品的三个规则误列为 CAL-002/004/006。保持原记录；依据精确Matrix blob 5919e1b6bbc3c4b150507c41a13ccc9e13d20f17、风险ledger blob a9f1e7f0a8e1ac256bdb65ca5c2f2caafe61e81e，正确交叉表如下：

| 规则 | Matrix状态 | 未决台账 |
|---|---|---|
| HPA-DAYUN-CAL-002 | MISSING_FROM_PRODUCT | TW-OPEN-0008 |
| HPA-DAYUN-CAL-003 | MISSING_FROM_PRODUCT | TW-OPEN-0010 |
| HPA-DAYUN-CAL-004 | MISSING_FROM_PRODUCT | TW-OPEN-0011 |
| HPA-DAYUN-CAL-006 | MODERN_COMPATIBILITY_ONLY | 非上述三项；文墨公历月位移实现 |

这是一处索引笔误修正，不改变Matrix、产品、遗漏台账或历史裁决。前述15FF-P文件继续保存。三项未入产品不等于算法缺陷，不授权重开。

### D2. 紫微动态规则：受读层与原页层的分别索引

复核根登记 EXT-ZIWEI-JIELAN-1581 是在线受读；EXT-SHANGHAI-LIB-JIELAN-1581 是1581四卷馆目。2016影印开卷图谱节点仅支持开卷与星图，未绑定CH51/52/54原印目标叶。中州派来源 EXT-WANGTINGZHI-ZHONGZHOU-CHUJI 是后出讲义受读，EXT-XINGQIAO-WANGTINGZHI-ZHONGZHOU-CHUJI 是出版目录。以下均是已审计规则的索引，而非原刻原字新裁决。

| HPA规则编号（省略共同HPA-前缀） | 当前Matrix状态 | 目标章、独立算子、证据缺口 |
|---|---|---|
| ZT-001/002/003 | HISTORICALLY_SUPPORTED | 《捷览》CH51定大限诀。分别为男女阴阳顺逆、局数起岁、每十年移一宫；金四局起四岁、顺行下一宫十四岁的例，仅支持所见受读，不能扩张为公历交界法。 |
| ZT-004、ZT-005、ZT-006、ZTEMP-001 | HISTORICALLY_SUPPORTED | 《捷览》CH54安流年斗君法、S01全书受读。流年宫序、太岁宫锚、斗君由生月时定位、流月由斗君起正月四个算子分开。未获得与1581子4051物件相绑定目标页。 |
| ZT-008 | HISTORICALLY_SUPPORTED | 《捷览》CH52定小限诀、全书受读。紫微小限为宫序体系，不能与四柱干支小运合并。 |
| ZT-013、ZTEMP-003 | HISTORICALLY_SUPPORTED | CH54及中州流日受读；月宫起初一按日顺移。宫位序列不等于流日干支或实际午夜换日政策。 |
| ZT-014 | DISPUTED_MULTIPLE_CANDIDATES | CH54与中州讲义流时两候选，不能坍缩。 |
| ZTEMP-004 | HISTORICALLY_SUPPORTED | CH54受读日宫起子时顺行，给定流日宫和时支。 |
| ZTEMP-005 | SUPPORTED_BUT_SCHOOL_SPECIFIC | 中州讲义固定地支宫对应时支及五子遁，固定地支候选不等于CH54日宫锚。 |
| ZT-015、ZTEMP-006 | SUPPORTED_BUT_SCHOOL_SPECIFIC | 中州闰月分段候选；与南阳堂卷三本命闰月安身命例分层，不以一个领域的闰月规则代替另一领域。 |

图谱：当前已存在 PASSAGE-JIELAN-1581-OPENING-2016-FACSIMILE、PASSAGE-NAJ-NANYANGTANG-J3-CHART-PLACEMENT，均非CH51/52/54目标页。当前未建立上述15条规则专属完整作品—版本—篇页—规则链。可索引但不作新增ATTESTS/TRANSMITS_RULE边。后续原页复核须按卷次、版心、影像页与受读章编号对齐，避免把现代章节编号直接写作古刻页码。

### D3. 四柱大运16条、小运2条：版本及规则层拆分

| HPA编号（省略共同HPA-前缀） | Matrix状态 | 版本/来源/规则与图谱缺口 |
|---|---|---|
| DAYUN-001 | SUPPORTED_BUT_SCHOOL_SPECIFIC | 《三命通会》卷二《论大运》四库受读，按年干阴阳及性别决定顺逆；原刻目标页另核。 |
| DAYUN-002/003、DAYUN-CAL-001 | HISTORICALLY_SUPPORTED | EXT-CTEXT-SANMING-V2-DAYUN、EXT-CTEXT-WUXING-JINGJI-V33-DAYUN：节锚、三日一年、离散余数换算；受读定位不等于1578原页或宋刊原字。 |
| DAYUN-004、DAYUN-SEQ-001/002 | HISTORICALLY_SUPPORTED | 《千里命稿》受读242–258行及《命理探源》例42–47：月柱相邻起运、同方向逐步推移。序列与首次交运绝对时刻分立。 |
| DAYUN-CAL-002 | MISSING_FROM_PRODUCT | 《三命通会》卷二小月闰月修正，以及大统历历日控制；TW-OPEN-0008，未完成所有适配语义。 |
| DAYUN-CAL-003/004 | MISSING_FROM_PRODUCT | 1934/1936《韋千里命學講義》原页报告已区分两个物件；见D4完整链。TW-OPEN-0010/0011。 |
| DAYUN-005/006/007、DAYUN-CAL-005/006/007 | MODERN_COMPATIBILITY_ONLY | 连续时间实现、文墨兼容、节界平局、微秒乘120、公历月位移、公历十年周年；不倒投为古籍规则。 |
| XIAOYUN-001 | DISPUTED_MULTIPLE_CANDIDATES | 《三命通会》卷二醉醒子从时柱按年阴阳顺逆，四库受读；原刻目标叶及起运界待核。 |
| XIAOYUN-002 | DISPUTED_MULTIPLE_CANDIDATES | 同书固定男女起点法、《五行精纪》卷33、朱翌传文与隋《五行大义》卷5受读；起点、方向、步长及交界各自举证。 |

15CK报告（blob 15d716578bd9682989426900c0a318d612927453）核对朱翌传文与《五行精纪》卷33。甲子年男丙寅女壬申同时符合固定起点与年遁寅申月，不能由单例归一。四库受读有女起丙申/壬申文字冲突，待原叶。15CU报告（blob 0a412d3fcafaf59fe78ac7cfa350ee75c86f29e3）核对《五行大义》卷5固定六甲行年及候病六旬法，并列1699日本刊本、1804许校本等书目；隋作品年代与后出物件必须分离，京都/维基受读不作两件古本。固定起点同形只支持比较，不支持隋至宋明的直接子平师承；亦非八卦游年算法。以上小运候选未新增图谱关系，未关闭。

### D4. 韦千里大运的既有完整图谱链与复算

精确旧证据文件 QIANLI-MINGXUE-JIANGYI-JIAOYUN-CALENDAR-SEMANTICS-R1.json，2026-10-06 OR批，直接物件：
- 1934：EXT-NLC-QIANLI-MINGXUE-JIANGYI-1934，17jh007058 / 102955；TG-E0166/0167/0168 版本、物件、数字替身。
- 1936：EXT-NLC-QIANLI-MINGXUE-JIANGYI-1936，01jh000368 / 10155；TG-E0169/0170/0171 对应独立版本链。
- TG-E0172/0173 两物件分别 ATTESTS 同一作用域的起例问答篇页 PASSAGE-QIANLI-MINGXUE-JIANGYI-QILI-JIAOYUN；E0174 TRANSMITS_RULE（HIGH_CONFIDENCE）→ RULE-FAMILY-QIANLI-JIAOYUN-NOMINAL-30DAY-LUNISOLAR，对应CAL-003/004。此链已存在，无须重复建节点；未证明两版全书相同。

复核旧算例：140名义日=4月20日，正月十五推至六月初五；实际137日。190名义日=6月10日，正月十五推至七月廿五；实际215日且期间有闰二月。故30日名义月推进与实际天数增加不能混同。每十年同名义农历坐标递推是另一算子。小月不存在目标日、闰月重复坐标及递推边界仍未解决，产品未实现状态不变。目标页数字页码尚需回查原叶定位记录，不能从报告内物品号臆定。

### D5. 四柱派生字段与神煞首批

| HPA编号（省略HPA-） | 当前状态 | 文本与范围 |
|---|---|---|
| BAZI-002、BHIDDEN-001 | HISTORICALLY_SUPPORTED | S11 YHZP-CH-061《又地支藏遁歌》及 EXT-CTEXT-YHZP-RECEIVED，藏干成员与原文次序分别保存；尚无确定古刻目标页链。 |
| BAZI-015、BHIDDEN-002 | SOURCE_INSUFFICIENT | 现代藏干展示序及规范化registry不能由成员歌诀直接推出。 |
| BHIDDEN-003 | SUPPORTED_BUT_SCHOOL_SPECIFIC | EXT-CTEXT-ZIPING-ZHENQUAN-PINGZHU-ZAQI《论杂气如何取用》受读，本气层级与显示序不同。 |
| BAZI-003 | HISTORICALLY_SUPPORTED | S11 YHZP-CH-016/017/057/065；生我、我生、克我、我克、同类及阴阳映射。已见1600《渊海》继善篇与宝法篇页图谱节点不直接证明完整十神配对表，须核对应原叶。 |
| SHENSHA-001 | DISPUTED_MULTIPLE_CANDIDATES | S11 YHZP-CH-024；15CK《密斋笔记》宋作品层传文中甲戊庚牛羊只支持部分映射，年干/日干与昼夜政策均未由此裁决。 |
| SHENSHA-008 | DISPUTED_MULTIPLE_CANDIDATES | S11 YHZP-CH-030及《三命通会》卷三天月德受读；15CK《密斋笔记》寅月丁、卯月申是两项局部映射，非完整12项表；与紫微本命/流年天德分族。 |
| SHENSHA-006 | HISTORICALLY_SUPPORTED | S11 YHZP-CH-028；四柱月德与图谱中紫微月德年支顺行族不是同一输入函数。 |
| SHENSHA-009 | DISPUTED_MULTIPLE_CANDIDATES | S11 YHZP-CH-031《论天厨贵人》，食神禄推法；已有 RULE-FAMILY-PREMODERN-TIANCHU-STEM-TABLE 与 RULE-FAMILY-ZIWEI-NATAL-TIANCHU-CURRENT 两个规则族，不能仅因名称相同增加跨系统传承边。 |

### D6. 当前恢复点

本次新增43个不同Matrix ID的分组索引，合计首、第二组53个；并复核大运未入产品编号及3项风险绑定。这里的索引数量不是原页闭合数。未修改权威状态、R2视图、Matrix、根/分片、图谱或风险记录。仍属15FF-Q未结项；下一步优先补全其他八字派生字段、剩余神煞、紫微动态辅助星，并对真正有确切作品/版本/原页绑定的节点判定增链；复核风险台账及整体验收。无新原图、无新登记、无算法重开，五P0保留。不能将本检查点当作第一阶段完成。transmission_impact: NONE。
