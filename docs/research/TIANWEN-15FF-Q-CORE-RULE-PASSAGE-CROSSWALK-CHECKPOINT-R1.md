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


## E. 第三组检查点：余下四柱派生、神煞及紫微动态辅助星

基线HEAD 8c5bfeeb26e3f4be5aeb9dde2571c233c7cc01ea，tree ec2f7824454c752f9d3b90d5ec08fc57e5b33e0f。六个权威绑定相符；Matrix、graph、风险ledger与root registry完整读取。基线Actions20项，19成功、clean-training-system运行，未见该HEAD连续性运行，不冒认先前HEAD验收。本轮不新增外部来源；未穷举276片，不据局部查询判断全库无证据。

### E1. 精确Matrix交叉索引（55个新ID）

下表由固定Matrix blob 5919e1b6bbc3c4b150507c41a13ccc9e13d20f17直接投影；现有状态和定位不提升为原页证据。四柱派生字段余25项、神煞余17项、紫微动态辅助星13项。各行具体作用域与证据缺口见E2–E4。

| HPA ID | 规则 | Matrix状态 | 既有定位 |
|---|---|---|---|
| HPA-BAZI-004 | Stem/branch affinity facts | HISTORICALLY_SUPPORTED | src/fortune_training/bazi_chart/hidden_stems.py generate_affinities; HPA-BAZI-002 |
| HPA-BAZI-005 | Raw stem/branch relations | DISPUTED_MULTIPLE_CANDIDATES | sources/canonical-runtime/S14/segment-0001.txt lines 1876–1964; segment-0002.txt opening source atoms; src/fortune_training/bazi_chart/relations.py |
| HPA-BAZI-006 | NaYin annotation | HISTORICALLY_SUPPORTED | S11:YHZP-CH-014; S11 canonical-runtime §7.7 |
| HPA-BAZI-007 | XunKong | HISTORICALLY_SUPPORTED | S14:YHZP-CH-047; S14:7.7 |
| HPA-BAZI-008 | Day-master Twelve Growth | HISTORICALLY_SUPPORTED | S11:YHZP-CH-015; S11 canonical-runtime §7.6; S12 chapter registry |
| HPA-BAZI-009 | Self-sitting Twelve Growth per pillar | HISTORICALLY_SUPPORTED | docs/BAZI-DERIVED-COORDINATES-R1.md; S11:YHZP-CH-015 |
| HPA-BAZI-010 | 胎元 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-ROOT-020-0003/0004; competing S12:SMTH-SEG-01138 |
| HPA-BAZI-011 | 八字命宫 | HISTORICALLY_SUPPORTED | S12:SMTH-SEG-01154/01155 |
| HPA-BAZI-012 | 八字身宫 | HISTORICALLY_SUPPORTED | S11:SHFTK-CL-001-原-001-001/003/006 |
| HPA-BAZI-013 | Hidden-stem exact exposure annotation | HISTORICALLY_SUPPORTED | src/fortune_training/bazi_chart/hidden_stems.py generate_exposures; docs/BAZI-CHART-ENGINE-V1-FOUNDATION.md |
| HPA-BAZI-014 | Stem five-combination identity | HISTORICALLY_SUPPORTED | NTL-9900014379 PDF p23 / printed三 / 天干相合; S14 canonical-runtime segment-0001.txt §7.1 |
| HPA-SHENSHA-002 | 天官贵人 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00240; S11:YHZP-CH-025 |
| HPA-SHENSHA-003 | 禄神 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00278; S11:YHZP-CH-034 |
| HPA-SHENSHA-004 | 驿马 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00285; S11:YHZP-CH-035 |
| HPA-SHENSHA-005 | 华盖 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00296; S11:YHZP-CH-037 |
| HPA-SHENSHA-007 | 月德合 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00262; S11:YHZP-CH-029 |
| HPA-SHENSHA-010 | 福星贵人 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00272; S11:YHZP-CH-032 |
| HPA-SHENSHA-011 | 太极贵人 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00243..244; S11:YHZP-CH-026 |
| HPA-SHENSHA-012 | 三奇 | SUPPORTED_BUT_SCHOOL_SPECIFIC | S11:YHZP-USR-S00248..251; S11:YHZP-CH-027 |
| HPA-SHENSHA-013 | 天赦 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00293; S11:YHZP-CH-036 |
| HPA-SHENSHA-014 | 学堂 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00301; S11:YHZP-CH-014/038 |
| HPA-SHENSHA-015 | 金舆禄 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00312; S11:YHZP-USR-S00278; S11:YHZP-CH-040 |
| HPA-SHENSHA-016 | 暗禄 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00324; S11:YHZP-CH-043; S14:YHZP-CH-007 |
| HPA-SHENSHA-017 | 夹禄 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00327; S11:YHZP-CH-044 |
| HPA-SHENSHA-018 | 拱禄 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00315..317; S11:YHZP-CH-041 |
| HPA-SHENSHA-019 | 垣城 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00330; S11:YHZP-CH-045; S11:YHZP-CH-015; S11:YHZP-USR-S00285; S14:YHZP-CH-007 |
| HPA-SHENSHA-020 | 羊刃 | SUPPORTED_BUT_SCHOOL_SPECIFIC | S11:YHZP-USR-S00282; S11:YHZP-USR-S02740; S11:YHZP-CH-224 |
| HPA-SHENSHA-021 | 飞刃 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00378..388 |
| HPA-ZT-009 | Dynamic 禄存/擎羊/陀罗 | SUPPORTED_BUT_SCHOOL_SPECIFIC | EXT-ZIWEI-QUANSHU-RECEIVED / 卷二《安身命例》安流禄流羊流陀诀; EXT-WANGTINGZHI-ANXING-2013 / 安星法 流曜; S10:ZZTERM-P-0120..0129; S10:ZZZA-A-1097..1099 |
| HPA-ZT-010 | Dynamic 文昌/文曲 | SUPPORTED_BUT_SCHOOL_SPECIFIC | EXT-WANGTINGZHI-ANXING-2013 / 安星法「流昌流曲」「流曜」; S10:ZZZA-A-1097..1103 |
| HPA-ZT-011 | Dynamic 天魁/天钺 | DISPUTED_MULTIPLE_CANDIDATES | EXT-WANGTINGZHI-ANXING-2013 / 安星法「流曜」; S10:ZZZA-A-1097..1099; S01:ZZQS-A-1800..1801; COMPAT:WENMO-CHARTDIFF-005 |
| HPA-ZT-012 | Dynamic 天马 case methods | SUPPORTED_BUT_SCHOOL_SPECIFIC | EXT-WANGTINGZHI-ANXING-2013 / 安星法「流曜」; S10:ZZTERM-P-0121..0122 and ZZTERM-P-0204..0206 |
| HPA-ZAUX-001 | Annual 流禄存 / 流擎羊 / 流陀罗 by annual heavenly stem | HISTORICALLY_SUPPORTED | EXT-ZIWEI-QUANSHU-RECEIVED / 卷二《安身命例》 |
| HPA-ZAUX-002 | Daxian 禄存 / 擎羊 / 陀罗 by Daxian Life-palace stem | SUPPORTED_BUT_SCHOOL_SPECIFIC | EXT-WANGTINGZHI-ANXING-2013 / 年限推断法与流曜; S10:ZZTERM-P-0120..0122 |
| HPA-ZAUX-003 | Month / Day / Hour 禄存羊陀 by target-layer heavenly stem | SUPPORTED_BUT_SCHOOL_SPECIFIC | EXT-WANGTINGZHI-ANXING-2013 / 安星法「流曜」; S10:ZZZA-A-1097..1099; S10:ZZTERM-P-0128..0129 |
| HPA-ZAUX-004 | 流文昌 / 流文曲 Zhongzhou ten-stem table | SUPPORTED_BUT_SCHOOL_SPECIFIC | EXT-WANGTINGZHI-ANXING-2013 / 安星法「流昌流曲」; S10:ZZZA-A-1100..1103 |
| HPA-ZAUX-005 | Dynamic Kui/Yue strict S01-project-corpus table reuse | SUPPORTED_BUT_SCHOOL_SPECIFIC | EXT-WANGTINGZHI-ANXING-2013 / 安星法「流曜」; S01:ZZQS-A-1800..1801 |
| HPA-ZAUX-006 | Dynamic Kui/Yue Wenmo-compatible candidate | MODERN_COMPATIBILITY_ONLY | tests/fixtures / Wenmo compatibility discriminator; src/fortune_training/ziwei_chart/temporal_auxiliary.py |
| HPA-ZAUX-007 | Daxian 运马 by Daxian Life-palace branch | SUPPORTED_BUT_SCHOOL_SPECIFIC | EXT-WANGTINGZHI-ANXING-2013 / 安星法「流曜」与年限推断法; S10:ZZTERM-P-0121..0122 |
| HPA-ZAUX-008 | Annual 流马 by annual branch | SUPPORTED_BUT_SCHOOL_SPECIFIC | EXT-WANGTINGZHI-ANXING-2013 / 安星法「流曜」; S10:ZZTERM-P-0204..0206 |
| HPA-BAFF-001 | Visible-stem exact hidden-stem identity link | HISTORICALLY_SUPPORTED | src/fortune_training/bazi_chart/hidden_stems.py generate_affinities / generate_exposures |
| HPA-BAFF-002 | Visible-stem same-element hidden-stem affinity link | HISTORICALLY_SUPPORTED | src/fortune_training/bazi_chart/hidden_stems.py generate_affinities |
| HPA-BREL-001 | Five heavenly-stem combination pairs and nominal transformation elements | HISTORICALLY_SUPPORTED | S14 relation fact table 7.1; EXT-CTEXT-XINGLI-KAOYUAN-RELATIONS |
| HPA-BREL-002 | Six branch-harmony pair geometry | HISTORICALLY_SUPPORTED | S14 YHZP source atoms S00065..S00071; EXT-CTEXT-XINGLI-KAOYUAN-RELATIONS |
| HPA-BREL-003 | Six branch-clash pair geometry | HISTORICALLY_SUPPORTED | S14 YHZP source atoms S00079..S00082; EXT-CTEXT-MINGLI-TANYUAN relation witness |
| HPA-BREL-004 | 相穿 / 六害 six-pair geometry and terminology bridge | HISTORICALLY_SUPPORTED | S14 YHZP source atoms S00083..S00085; EXT-CTEXT-SANMING-V2-RELATIONS |
| HPA-BREL-005 | Four standard three-combination branch bureaus | HISTORICALLY_SUPPORTED | S14 YHZP source atoms S00072..S00075; EXT-CTEXT-SANMING-V2-RELATIONS |
| HPA-BREL-006 | Directed branch punishments, Zi-Mao mutual punishment, and repeated self-punishment | HISTORICALLY_SUPPORTED | S14 YHZP source atoms S00086..S00088; EXT-CTEXT-SANMING-V2-RELATIONS |
| HPA-BREL-007 | 辰戌丑未 four-earth bureau candidate | HISTORICALLY_SUPPORTED | S14 relation fact table 7.3 / YHZP source atom S00076; EXT-CTEXT-SANMING-V1-FOUR-EARTH-BUREAU |
| HPA-BREL-008 | Four directional three-branch groups: 方 / modern 三会 terminology bridge | HISTORICALLY_SUPPORTED | EXT-CTEXT-SANMING-V6-DIRECTIONAL-TRIADS; S14三会与墓库来源候选运行表 |
| HPA-BREL-009 | Early four-break relation family | HISTORICALLY_SUPPORTED | EXT-CTEXT-WUXING-JINGJI-V23-BREAK line 45 |
| HPA-BREL-010 | Later six-break convention | DISPUTED_MULTIPLE_CANDIDATES | Contrast EXT-CTEXT-WUXING-JINGJI-V23-BREAK with modern compatibility tables; cross-system 六壬 tables are not Bazi authority. |
| HPA-BREL-011 | Branch half-trine / arched-trine modern relation family | MODERN_COMPATIBILITY_ONLY | EXT-MODERN-OPENFATE-HALF-TRINE-2026; EXT-CTEXT-SANMING-V2-RELATIONS《论支元三合》 |
| HPA-BREL-012 | Same-pillar visible-stem ↔ hidden-stem five-combination: 座下自化 / later 干支暗合 | HISTORICALLY_SUPPORTED | EXT-CTEXT-SANMING-V2-ZUOXIA-ZIHUA; EXT-CTEXT-MINGLI-TANYUAN-RELATIONS |
| HPA-ZTEMP-007 | Received-Fullbook annual TianDe / YueDe source-scoped candidates | HISTORICALLY_SUPPORTED | S01:ZZQS-A-1943..1944; EXT-ZIWEI-QUANSHU-RECEIVED / 卷二《安天德月德解神诀》 |

### E2. 四柱派生字段：已有原页、后出传文、产品投影必须分层

1. **十神与天干五合原页锚点补强（D5的前向补充，不改变历史状态）。** 根登记 EXT-NTL-9900014379-YHZP-TEN-GOD-TABLE：国立台湾图书馆NTL-9900014379、登记号31111003618756、秦慎安校勘、文明书局，馆目1926，PDF p2封面上海文明书局印行。PDF 207页，SHA256 664bccd1ea4706c609df8ea6cd69a4565db97dc277e876fc22eb125ea41dcc9f。已核p37–39通变表（五阳/五阴），p61生日为主，p64己身词义（择日语境）；p23印页三天干相合，为同一物件的另一核读，证据docs/research/evidence/batch-12mm/ntl-p023.jpg。HPA-BAZI-003可补晚出实物通变表身份锚；HPA-BAZI-014、BREL-001可补五个配对身份锚（不证明名义化气元素或合化成功）。HPA-BAZI-FLOW-002本轮只作相关交叉引用，不加入55个新ID计数。1926是馆目著录年，物件/印次/作品起源不自动等同；2017 PDF元数据与2022上传属替身层。graph无该NTL物件专属五合/十神篇页族（当前只检查节点ID/相关节点，正式新增前须再做语义去重），适合下一轮实际增链，非新增独立古本。D5说1600已核继善篇/宝法不能直接证明完整十神表仍成立；本项晚出见证不补足1600目标叶。
2. **安命安身不是同义算法。** 15AU报告（blob 7e9c5a391658fbb364c448cb9eaa857dd32c4bda）已有144组月时条件复算：1600喬山堂NCL06593 p3〈論安身命法〉，与1607《续道藏》卷一第167册p29–32月时安命同形（正月子逆月、以该宫标生时顺数至卯）。与南阳堂七卷本子060-0001图73–75寅起月顺、生时逆安命不同；1607按生日二日半步长安身与1600数至酉也不同。HPA-BAZI-011的命宫文字得到邻篇实物支持，但不凭同形认定《三命通会》与两书直传，也不将1600命宫等同紫微十四主星命宫。图谱PASSAGE-YUANHAI-06593-J1-DAY-TO-HOUR邻段、PASSAGE-XUDAOZANG-ZIWEI-J1-ZHAODAN-FEIXING及PASSAGE-NAJ-NANYANGTANG-J3-CHART-PLACEMENT均已存在，需单独审定安命/安身子函数篇页范围。HPA-BAZI-012指定《神峰通考》逢卯安命逢酉安身；1600邻文作同形比较而非指定版《神峰》原字。另有陶宗仪日家安命先定位生日太阳宿度后数至卯，RULE-FAMILY-RIJIA-SOLAR-LODGE-BIRTH-HOUR-COUNT-TO-MAO、TG-E0274，不应混入月时算子。
3. **胎元、纳音、旬空及十二长生。** BAZI-010保留《渊海》按月柱胎元（己巳→庚申例）及《三命通会》受胎日法，输入与时间语义不同。BAZI-006/007/008/009的S11/S14章定位是收到文本索引；纳音配对、旬内空支、日干对支长生、各柱自坐长生是四种独立函数。不得把五行长生、十干阴阳顺逆、自坐、紫微五局长生混同；仍需版本目标页及独立关系。BAZI-004/013、BAFF-001/002是继承藏干成员的现代关系/透干展示事实，历史审计状态不证明现代展示接口见于古籍。
4. **干支关系。** BREL-001/002/005用《星历考原》卷一受读旁证；BREL-004/005/006用《三命通会》卷二受读；三刑无恩/恃势名称与方向几何分离（根登记质量注已指出异名），相穿/六害术语桥须限定同一配对。BREL-007辰戌丑未四土局是四成员，不并作三合；BREL-008《三命通会》卷六〈属象〉四方之气同几何而术语与现代三会不同。BREL-009《五行精纪》卷23〈破杀〉受读明确四破并排除寅申巳亥，BREL-010现代六破加寅亥、巳申属后出竞争族，保留候选。BREL-011半合/拱合现代兼容性与完整三合不同。BREL-012《三命通会》卷二〈座下自化〉与《命理探源》卷五〈化合刑冲〉六组例同形，后者明说干支暗合；只作同柱干与藏干五合出现，不判实际合化，也不是紫微自化。以上受读源不等于1578原刻目标字；精确图谱链缺口仍须补足。

### E3. 神煞：17项剩余字段的独立输入族

以E1逐项S11章/条为索引，不能把整套21项倒投同一古本。天官、禄神、太极、天赦、拱禄、垣城、飞刃为现有历史支持；驿马、华盖、月德合、福星、学堂、金舆、暗禄、夹禄为候选争议；三奇、羊刃为学校限定。驿马及华盖的生年支/日支输入、禄系天干参照、三奇顺序与适用、羊刃阴干分支逐项保留，不能从通行口诀强制选择。S11 received《渊海子平》各章、S14关系及纳音是受读或项目语料层；尚缺具体古刻版次原页/物件链，待下一轮找已登记且有直接证据的版本。紫微天马、流马及禄存擎羊不能仅凭神煞名称与四柱驿马、禄神、羊刃归并。

### E4. 紫微动态辅助星：13项完整模块索引

- ZT-009与ZAUX-001/002/003分别指流禄羊陀总族、流年天干、大限命宫干、月日时目标天干。全书卷二〈安身命例〉为年层受读证据；其余王亭之安星法系学校限定。根登记EXT-WANGTINGZHI-ANXING-2013为复旦2013.06现代讲义见证，EXT-UIBE-WANGTINGZHI-ANXING-2013为独立馆目，不因同版书目证明特定字句；需精确页码、文本见证与馆藏对象绑定。
- ZT-010/ZAUX-004流昌曲十干表、ZT-011/ZAUX-005/006流魁钺S01严格表及文墨对照分别处理，文墨只属兼容见证，非古法。ZT-012/ZAUX-007/008大限运马以大限命宫支、流年流马以太岁支，学校限定，禁止上推完整月日时马算法。
- ZTEMP-007已有明确受读图谱：PASSAGE-ZIWEI-FULLBOOK-ANNUAL-ERDE-JIESHEN，TG-E0145→RULE-FAMILY-ZIWEI-ANNUAL-YUEDE-ZI-START，TG-E0146→RULE-FAMILY-ZIWEI-ANNUAL-TIANDE-YOU-START，均CONFIRMED受读范围；TG-E0150/0151为本命与流年族的PARALLEL_COEXISTS_WITH，不是直接传承。流年月德子起、流年天德酉起，区别本命月德巳起与本命天德酉起；天德起宫相同但出生年/目标年输入不同。EXT-ZIWEI-QUANSHU-RECEIVED、EXT-WIKISOURCE-ZWDSQS-V2、S01条目支持已有受读链，不证明南阳堂古刻目标页或四柱天月德采用关系。

### E5. 恢复与下一步

新55个ID与前两组53个不重复，合计108项初步映射。覆盖全部31个四柱派生字段、21个四柱神煞、13个紫微动态辅助星，以及前组大限/动态和四柱运限等。此计数不等于108个新增史料或完成原页校勘。当前仍须：补剩余紫微本命、十二宫、时间历法等核心模块的缺漏；对明确可重放且已有直接页证的NTL五合/十神、1600/1607安命、南阳堂安身命等先做语义去重并按图谱协议实际增链；检查58项风险与第一阶段门槛，不以数字作为验收。五P0保持。未修改权威状态及图谱；仅复用原证据，无新外部来源或古刻核读。transmission_impact: NONE。


## F. NTL十神及五合原页证据正式回填图谱（15FF-Q阶段检查点）

基线 cb50fa6026d007b7c006edd72c7a9af5018fae2b。依旧登记EXT-NTL-9900014379-YHZP-TEN-GOD-TABLE及12MM/12ML页证，完整图谱语义查重未见专属NTL对象、通变表或五合规则族。新增8节点（合题载体、馆目版次、物件、数字替身、2篇页、2规则族），7条限定边TG-E0425–0431。图592/431。NTL-9900014379登记31111003618756，1926是馆目年、非已证物件印次；207页PDF为同件数字替身，p37–39及61限定日主十神身份，p64择日己身只作词义旁证；p23印页三仅证天干五合配对。合题载体不合并明刊作品，不证明古法首创、实际合化、时间界线或预测。原页核读沿用已有记录，本轮不新增古籍来源。HPA-BAZI-003/014、BREL-001既有状态不变。

状态1.1571.0；58项风险及五P0保持，追加同步检查点。R2视图与图、状态、台账同一原子提交。连接器完整缩进台账写入发生h2传输中断，改用等价紧凑JSON序列化，所有原有issues和checkpoint内容保留，仅新增当前checkpoint并更新binding。此前计划的1600/1607与南阳堂安命安身族未在本次提交落地，留下一轮继续；不得把候选分析当作已入图。确定性排盘CLOSED。

transmission_impact: MATERIAL_EVIDENCE_SCOPED_GRAPH_BACKFILL — 8 nodes, 7 scoped edges, no direct textual dependence or teacher lineage, no algorithm reopen.

### 15FF-Q续｜三组安命安身原页规则族入图（2026-11-27）

复用已登记、已核局部原页的14T、14I、13ZZ及15AU/15AT，**本轮未重新取得或逐字校勘原扫描**。三个已登记分片及其原source ID保持不变。1600为NCL06593卷六p160刊记；1607为《续道藏》收录层；南阳堂确切印年未定。作品形成、版本、物件、替身年代不互代。

| 物件／目标篇页 | 安命子族 | 安身子族 | Matrix边界 |
|---|---|---|---|
| NCL06593《渊海》p3〈論安身命法〉 | 子起正月逆月，生时顺至卯 | 同坐标续至酉 | HPA-BAZI-011/012为同形旁证，不替代指定《三命通会》与《神峰通考》原页 |
| NLC892/411999007380第167册p29、31–32 | 天杖由子逆月、杖宫标生时顺至卯 | 天杖按生日逆数，二日半一宫 | 十八飞星独立家族；半日边界、p32极性异文未裁；不套HPA-ZIWEI-002十四主星排盘 |
| NAJ子060-0001卷三图73–75 | 寅起正月顺月，子时逆至生时 | 同月位子时顺至生时 | HPA-ZIWEI-002普通月时；闰正月按二月为该页例，不据此统一其他流派闰月 |

复算15AU普通月时144组：1600与1607安命144/144相同，南阳堂与两者144/144不同。1600安身与1607生日步距不同；不裁1607半日进位。不把宋元日家太阳宿度安命、月时安命及身宫归一。只证所引见证下的规则结构，不证预测有效性、原始创制者或直接抄传。TW-OPEN-0012、58项未决及五P0继续保留。

**transmission_impact**：新增独立篇页1及规则族6；节点ID如下（原有卷一照胆、卷三本命篇页复用）：
- `PASSAGE-YUANHAI-06593-J1-MINGSHEN`：喬山堂本卷一〈論安身命法〉
- `RULE-FAMILY-BAZI-YUANHAI-MONTH-REVERSE-HOUR-FORWARD-TO-MAO`：1600《渊海》子起正月逆月、生时顺至卯安命
- `RULE-FAMILY-BAZI-YUANHAI-MONTH-HOUR-TO-YOU-BODY`：1600《渊海》同月时坐标续数至酉安身
- `RULE-FAMILY-ZIWEI-XUDAOZANG-TIANZHANG-HOUR-TO-MAO-LIFE`：《续道藏》十八飞星天杖宫生时顺至卯安命
- `RULE-FAMILY-ZIWEI-XUDAOZANG-TIANZHANG-BIRTHDAY-REVERSE-BODY`：《续道藏》天杖宫按生日逆数二日半一宫安身
- `RULE-FAMILY-ZIWEI-NANYANGTANG-MONTH-FORWARD-HOUR-REVERSE-LIFE`：南阳堂十四主星法寅起正月顺月、子时逆数安命
- `RULE-FAMILY-ZIWEI-NANYANGTANG-MONTH-FORWARD-HOUR-FORWARD-BODY`：南阳堂十四主星法寅起正月顺月、子时顺数安身

新增TG-E0432–0438为直接见证范围内ATTESTS；TG-E0439仅同形子函数的PARALLEL_COEXISTS_WITH。无旧边修改、无确认师承/抄写边。图599节点/439边；来源1488（647+841，276分片）、Matrix222/222不变；算法不重开，确定性核心CLOSED。历史问题：指定《三命通会》《神峰》原页、1600/1607互引或独立更早见证、1607生日半步及南阳堂精确印年均不能由本次回填结案。

状态1.1572.0；NEXT：15FF-Q续：补齐剩余紫微本命主星/十二宫/五寅/局数及历法时间规则的作品—版次—篇页—图谱链接；核验1581《捷览》目标页边界；复核58项风险及第一阶段验收门槛。

### 15FF-Q续｜紫微本命宫序、五寅、纳音与主星规则证据分层（2026-11-27）

依据既有13ZZ、Batch 04、Batch 06、15AM及14I的原页核读与受读记录。南阳堂图0074/0075原镜像本轮重新获取失败（连接环境DNS及网页读取不通）；只复用旧图像哈希和既有核读范围，不声称重新核验字形。南阳堂子060-0001图0074（SHA256 78406c40bc7826d8b89bc2e17a9b1eeba80172d0092d68ec2327cfb728ca89b4）确见安十二宫、起五寅、纳音篇题；图0075（SHA256 eb711a4260ce9e9c074082563726a7bd1ad661df575a7b1300a56eb2b66c3a65）为两组星序，未将完整宫序、五组起干、全部六十纳音、局数和星位偏移升级为该古本逐字证据。1581《捷览》子4051馆目及2016影印开卷仅证明版本、署名及框架；CH20–22仍限定现代受读，不声称1581原印目标叶已核。四层年代及物件身份不合并。

| Matrix | 已有精确受读锚 | 机械边界 |
|---|---|---|
| HPA-ZIWEI-003 | S01 ZZQS-A-1749/1751 | 命兄妻子财疾迁奴官田福父逆布，现代显示称谓与宫位几何分离 |
| HPA-ZIWEI-004 | S01 ZZQS-A-1755/1756 | 甲己丙、乙庚戊、丙辛庚、丁壬壬、戊癸甲起寅；10年干×12宫形式化奇偶合法性120/120，非产品运行回归或史料实测 |
| HPA-ZIWEI-005 | S01 ZZQS-A-1747、1760–1767 | 命宫干支→纳音五行→局，甲年命寅丙寅炉中火→火局；五局数字及生日安星另证 |
| HPA-ZIWEI-006/020 | 《捷览》CH20–22受读、15AM | 金四局初三紫微丑天府卯，初八紫微卯天府丑；分开紫微北斗逆行、天府南斗顺行，原刻全图与偏移待核 |
| 独立十八飞星 | 14I第167册p29–30 | 未起子年顺至生年支，寅年紫微酉；与五局生日输入不同，不并入十四主星族 |

**transmission_impact**：新增5篇页、9规则族及TG-E0440–0451共12条限定ATTESTS。仅南阳堂图75向两组星序结构建直接页证边；图74篇题不向完整机械映射强建证据边。受读各规则明确标记RECEIVED_TEXT。节点列表：
- `PASSAGE-NAJ-NANYANGTANG-J3-IMAGE74`：南阳堂卷三图0074安十二宫例、起五寅例、纳音
- `PASSAGE-NAJ-NANYANGTANG-J3-IMAGE75`：南阳堂卷三图0075南北斗星序
- `PASSAGE-FULLBOOK-S01-NATAL-PALACES-STEMS-BUREAU`：受读《全书》安十二宫、起五寅、纳音及定局
- `PASSAGE-JIELAN-RECEIVED-CH20-21-ZIWEI-TIANFU`：《捷览》现代受读CH20–21安紫微天府诀及安紫府图
- `PASSAGE-JIELAN-RECEIVED-CH22-DIPPER-SEQUENCE`：《捷览》现代受读CH22布南北二斗诸星诀
- `RULE-FAMILY-ZIWEI-RECEIVED-TWELVE-PALACE-REVERSE-ORDER`：命宫起十二宫逆序排列
- `RULE-FAMILY-ZIWEI-RECEIVED-FIVE-TIGERS-PALACE-STEMS`：年干五组起寅宫干再顺布十二宫干
- `RULE-FAMILY-ZIWEI-RECEIVED-NAYIN-GANZHI-ELEMENT`：六十甲子纳音五行映射
- `RULE-FAMILY-ZIWEI-RECEIVED-LIFE-PALACE-NAYIN-BUREAU`：命宫干支纳音决定五行局
- `RULE-FAMILY-ZIWEI-JIELAN-RECEIVED-BUREAU-BIRTHDAY-ZIWEI`：五行局与生日查紫微天府位置
- `RULE-FAMILY-ZIWEI-NORTH-SOUTH-DIPPER-GROUP-STRUCTURE`：南北斗两组布星结构
- `RULE-FAMILY-ZIWEI-JIELAN-RECEIVED-NORTH-DIPPER-REVERSE-SEQUENCE`：紫微天机星逆行的北斗星序
- `RULE-FAMILY-ZIWEI-JIELAN-RECEIVED-SOUTH-DIPPER-FORWARD-SEQUENCE`：天府太阴顺贪狼的南斗星序
- `RULE-FAMILY-ZIWEI-XUDAOZANG-YEAR-BRANCH-ZIWEI-ANCHOR`：《续道藏》未起子顺至出生年支安紫微

无新来源、无独立物理见证、无新增师承/抄传、无Matrix修改、无算法重开。图613/451；来源1488（647+841，276分片），Matrix222/222，58 OPEN及五P0原状，核心CLOSED。第一阶段尚未终验。待核《捷览》原刻CH20–22与南阳堂具体表行及星位，保留TW-OPEN-0012等既有线索。

状态1.1573.0；NEXT：15FF-Q续：补紫微与四柱历法时间、换日、闰月、节月、时刻坐标独立证据链；复核所有58项风险及广度第一阶段验收门槛；保留《捷览》CH20–22目标原刻与南阳堂精确条目待核。


### 15FF-Q续｜紫微与四柱历法时间规则分层（2026-11-27）

基线 db56508951f5961a9af77803181ba4564ca13df1。只复用已有原页校勘记录与已登记受读资料，不声称本轮重新取得古籍图像或新原页核读。全量读取Matrix222行、图谱613节点451边、根登记647条、扩展清单276片841条及58项台账，核对五P0；未开展新来源准入或全分片文字查重。现有来源不重复登记。

| 规则域 | 证据定位 | 证据及排盘边界 |
|---|---|---|
| 四柱日归属，HPA-TIME-007 | 1578 NCL06589《三命通會》卷二〈論時刻〉，旧核读p132/133/136/137；既有TG-E0041/0042 | 百刻半子夜半前後分别归昨日、今日；已有1520《革象新書》等文字谱系候选，不重复建族；不由此证明紫微亥/子重分类 |
| 紫微时支归属，HPA-ZDATE-006 | EXT-ZIWEI-QUANSHU-NANYANGTANG-SCAN，527页PDF p320卷五〈論人生時要審的確〉 | 十刻上五刻属昨夜亥、下五刻属今日子；亥/子支身份有别；PDF SHA256 32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7；不将该替身直接绑为NAJ子060-0001同一物件；现代时刻映射未定，TW-OPEN-0006仍P0 |
| 紫微本命闰月，HPA-TIME-010 | NAJ子060-0001卷三图73–75，13ZZ旧核读 | 闰正月按二月安身命；与全书受读相合。仅限该见证，不将1935《斗数宣微》馆目当原句，亦不将中州流月流日半分法推至本命 |
| 四柱年界，HPA-TIME-006/BTIME-002/004 | EXT-CTEXT-MINGLI-TANYUAN-YEAR-MONTH，卷二受读lines 2–10 | 立春交节前后分年，同日时刻例；后出受读、非现代星历精度或明刊原页 |
| 四柱月界，HPA-BTIME-003/004 | 同上lines 11–20；EXT-CTEXT-SANMING-V2-SEASONS为明代季节框架受读旁证 | 以节令分月，不以中气或朔日代替；明代节气框架与后出明确交节实例不可合并成同一原页证明 |
| 四柱时干，HPA-TIME-008 | EXT-CTEXT-MINGLI-TANYUAN-NIGHT-ZI，卷五受读 | 夜子日用今日、时用明日；所引《星平大成》原页未核；三候选不裁，非紫微换日 |

**尚未入图的时间层**：HPA-TIME-001/002/004/005/011、HPA-BTIME-001是现代时区/折叠/历法/节气/近似时刻实现；TIME-003/ZTIME-002真太阳时定义与采用是不同证据；ZTIME-001洛阳地方平太阳时是中州限定候选。ZDATE-001/002是历日索引候选，ZDATE-003/004是有效日期候选，ZDATE-005是双系统独立软件契约，均不得用p320古页直接升级。ZTEMP-006/ZT-015为中州流月流日闰月，不并入本命规则。G893及绝对时刻适配器仍未闭合，保留TW-OPEN-0005/0007。未授权候选收束、预测或算法重开。

**transmission_impact**：9节点（数字替身1、篇页3、规则族5），TG-E0452–0457共6条限定见证边。旧百刻半子文本谱不重复扩增；无新直接承袭边。图622/457，来源1488（647+841，276分片）、Matrix222/222不变。58未决及五P0保留；确定性排盘CLOSED。第一阶段未终验。

状态1.1574.0；NEXT：15FF-Q续：补时刻坐标、现代历法及中州流月与本命闰月的证据范围；完成剩余规则族、58项风险与广度第一阶段验收门槛复核；保留《捷览》CH20–22目标原刻、南阳堂精确条目及五P0。


### 15FF-Q续｜古今计时坐标、中州时间标准及流运闰月（2026-11-27）

基线 a14973fcccfcf89c5dbd052c3775470a5affded8。连续性专项尚排队，故不使用未验证的R2快路径；精确blob回退解析六项权威输入，Matrix222/222、根647、清单276片841、图622/457及58项风险（五P0）计数一致。沿用本会话已核R1/R2与权威政策，复读08B/C/D及时间基础文档；无新来源登记、无全分片正文查重、无原页复校。

| 坐标／作用域 | 证据层与Matrix索引 | 明确界线 |
|---|---|---|
| 民用钟表时刻→绝对瞬间 | TIME-001/002：IANA tzdb、PEP495、zoneinfo；现代实现 | 时区历史、折叠和缺口不是古代计时证据；TIME-011近似时刻采样是工程规则 |
| 地方平太阳时 | ZTIME-001：王亭之讲义出生时间段，现代中州限定 | 项目采用洛阳112°26′的经度换算；不加均时差。古代洛阳制度、精确经度及全派规则不由此证明 |
| 地方视太阳时 | TIME-003/ZTIME-002：USNO定义、EXT-ZIWEI-QVXIAN-TRUE-SOLAR-2022实践 | 地方平太阳时加均时差，天文定义与术式采用分别举证 |
| 农历历日 | TIME-004：GB/T 33661-2017及紫金山天文台术语、HKO对照表 | 冬至月为十一月，朔所在日月首；13月区间首个无中气月为闰月。现行计算结构不是历代历法适配，也非IERS/1秒精度认证 |
| 节气瞬间 | TIME-005/BTIME-001：HKO 24节气及时刻；现代星历 | 太阳视黄经每15°一节气；立春315°、惊蛰345°。四柱历法消费者另见上一段受读年/月界，不等同星历模型史 |
| 紫微历日索引与日界 | ZDATE-001/002：地方视太阳日期／民用日期；ZDATE-003/004：23时／夜半候选；ZDATE-005独立软件契约 | 先选日期索引再选换日；现代争议见证不能补足南阳堂p320亥子重分类，更不能将紫微策略传入八字 |
| 本命闰月 | TIME-010：南阳堂卷三图73–75旧核读；上批已有图谱 | 闰正月按二月安身命；不认作中州流运规则或所有星曜的同一法 |
| 中州流运闰月 | ZT-015/ZTEMP-006：讲义受读及S10 P-0280–0283、0287 | 初一至十五承前月序，十六日起改次月月宫基；流日仍顺数。勿误读为简单将本命月码加一，也勿声称流日宫必然跨日连续 |
| 古代跨时代绝对计时 | MD-G03、TW-OPEN-0005/0007及现有明元漏刻图谱 | 地域、年代、仪器、历书制式、观测与计算坐标仍未统一，不套现代均匀小时逆推 |

形式核算（不是产品实测或历史测量）：112°26′ × 4分/度 = 449分44秒，即UTC+7:29:44；与UTC+8民用标准相差−30分16秒。地方视太阳时还需要出生地经度和相应时刻均时差，不能以该固定差代替。流时宫位的日宫起子与固定子垣起子为另一独立维度（08B/C）。15FF-Q本轮未重跑运行时，不更改Matrix裁决。

**transmission_impact**：新增8节点（4文字见证篇页/聚合入口及4规则族）及TG-E0458–0461共4条受读限定ATTESTS；现代争议两来源为聚合索引，不等同同一本书或独立原件；不新增直接承袭或师承边。现代工程规则保留Matrix/配置导航，不为了覆盖率造历史见证。图630/461，来源1488/276，Matrix222/222，58开放五P0及核心CLOSED保持。第一阶段未终验。

状态1.1575.0；NEXT：15FF-Q续：复核双体系核心规则族索引完整性（按222个Matrix ID逐项区分历史规则、现代实现与未决候选）、58项风险和第一阶段四项验收门槛；保留目标原页及独立传承缺口。


## G. 15FF-Q续｜222规则ID全覆盖导航及广度门槛复核（2026-11-27）

基线 264b28ffddb6d4be9369f7e8c5b0e15979af4f98，tree c3572c39861fb30abf3660b6d373bd72bf0c34ab；R2六绑定与docs树一致，连续性精确HEAD运行45975156521成功；读取285项Actions时284成功、clean-training-system仍运行，不称全绿。Matrix 5919e1b6bbc3c4b150507c41a13ccc9e13d20f17、ledger 4efcb2d760cfd4db135417bca01e9552f1cab204、graph 5589340cabc42f0a126248657dd6fc2c9c8abf7f。已复核两史纲、覆盖台账、15FF-P、15BL/15FF-O、12QD及本检查点；无新来源准入或原页校勘，不作全分片无命中判断。

### G1. 全量规则ID导航（可复算，不是新增历史裁决）

逐条读取Matrix rows；222个唯一ID与222个已审计ID集合完全相同。按ID前缀及现有状态聚合，以下后缀与首列前缀连接即完整ID。H=历史支持104，S=流派特定25，D=多候选27，M=现代相容50，I=来源不足11，P=产品未含4，N=尚未形式化1。历史支持不自动代表原刻直证；现代/产品/结构字段不冒充古法；混合前缀不代替system字段（紫微114、四柱94、共享／组合14）。本索引仅提供逐ID可回查入口，不能证明222条均已建立独立版本—篇页—规则族链。

| 完整ID前缀 | 现有状态及三位后缀 | 条数 |
|---|---|---:|
| HPA-TIME | M: 001, 002, 003, 004, 005, 011；H: 006；D: 007, 008, 009；S: 010 | 11 |
| HPA-BAZI | M: 001, 016, 018, 019；H: 017, 020, 002, 003, 004, 006, 007, 008, 009, 011, 012, 013, 014；D: 005, 010；I: 015 | 20 |
| HPA-DAYUN | S: 001；H: 002, 003, 004；M: 005, 006, 007 | 7 |
| HPA-XIAOYUN | D: 001, 002 | 2 |
| HPA-SHENSHA | D: 001, 004, 005, 007, 008, 009, 010, 014, 015, 016, 017；H: 002, 003, 006, 011, 013, 018, 019, 021；S: 012, 020 | 21 |
| HPA-BAZI-FLOW | M: 001, 005, 006, 007；H: 002, 003, 004, 008, 009, 010 | 10 |
| HPA-ZIWEI | D: 001, 007, 012, 025；H: 002, 003, 004, 005, 006, 010, 013, 014, 015, 016, 017, 018, 019, 020, 021, 022, 024；I: 008, 011, 023, 026；M: 009 | 26 |
| HPA-ZT | H: 001, 002, 003, 004, 005, 006, 007, 008, 013；S: 009, 010, 012, 015；D: 011, 014；N: 016 | 16 |
| HPA-STRUCT | M: 001, 002, 003, 012, 004, 005, 006, 007, 008, 014, 016, 018, 020；S: 009, 010, 011, 013, 015, 017, 019 | 20 |
| HPA-COMB | M: 001, 002, 003, 004, 005, 006, 007, 008 | 8 |
| HPA-ZMINOR | H: 001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 016, 017, 018, 019, 020, 021, 023；I: 022, 024, 025, 026, 027 | 27 |
| HPA-ZAUX | H: 001；S: 002, 003, 004, 005, 007, 008；M: 006 | 8 |
| HPA-ZTEMP | H: 001, 002, 003, 004, 007；S: 005, 006 | 7 |
| HPA-ZTIME | S: 001；M: 002 | 2 |
| HPA-ZDATE | M: 001, 002, 004, 005；D: 003；P: 006 | 6 |
| HPA-BTIME | M: 001；H: 002, 003, 004 | 4 |
| HPA-DAYUN-SEQ | H: 001, 002 | 2 |
| HPA-BAFF | H: 001, 002 | 2 |
| HPA-BREL | H: 001, 002, 003, 004, 005, 006, 007, 008, 009, 012；D: 010；M: 011 | 12 |
| HPA-BCAND | D: 001 | 1 |
| HPA-BHIDDEN | H: 001；I: 002；S: 003 | 3 |
| HPA-DAYUN-CAL | H: 001；P: 002, 003, 004；M: 005, 006, 007 | 7 |

### G2. 本命辅星、杂曜、四化、庙陷、三环补足导航

以下47条为对A/D等既有本命主星重点索引之外的紫微本命及杂曜条目的补充；定位原样取自Matrix，而非本轮新核原文。所列捷览CH为受读章节定位，尚未与1581子4051目标原刻逐页绑定，不从目录升级为直接原页。现代实现与既有源流索引分别读取。

| Matrix ID | 规则／字段 | 状态 | 既有证据定位 |
|---|---|---|---|
| HPA-ZIWEI-001 | Ziwei day-boundary policy | D | S01:ZZZA-A-0052..0057; S01:ZZZA-CF-001; EXT-ZIWEI-QUANSHU-NANYANGTANG-SCAN PDF p.320; docs/research/ZIWEI-QUANSHU-NANYANGTANG-LATE-ZI-DIRECT-COLLATION-R1.json |
| HPA-ZIWEI-007 | Core auxiliary placement | D | EXT-ZIWEI-JIELAN-1581:CH22／CH25／CH27; S01:ZZZA-PR-016..021 |
| HPA-ZIWEI-008 | Operational minor-star family R4 | I | EXT-ZIWEI-JIELAN-1581:CH24; S01:ZZQS-A-1854/1855; minor-star rule routes |
| HPA-ZIWEI-009 | Operational R4 dignity states | M | docs/ZIWEI-DIGNITY-ANNOTATION-PROVENANCE-R1.md; EXT-ZIWEI-JIELAN-1581:CH69／CH70 |
| HPA-ZIWEI-010 | Ten-stem four-transformation assignment | H | EXT-ZIWEI-JIELAN-1581:CH23; S08-ASG-01..40 |
| HPA-ZIWEI-011 | 博士/将前/岁前三环 | I | docs/research/ZIWEI-THREE-RING-SOURCE-SCOPE-AUDIT-R1.json |
| HPA-ZIWEI-012 | Star role/dependency identities | D | EXT-ZIWEI-JIELAN-1581:CH31／CH32; S01:ZZQS-A-1995..1997／2003..2004 |
| HPA-ZIWEI-013 | Body-palace Ganzhi visibility | H | S01:ZZQS-A-1744 and ZZQS-A-1755..1756 (received Fullbook atoms already audited in Batch 06); src/fortune_training/combined_chart_application/ziwei_basic_info_assets.py:palaceGanzhi |
| HPA-ZIWEI-014 | Competing Four-Transformation table families | H | EXT-ZIWEI-JIELAN-1581:CH23; EXT-SHIDIAN-ZWDSQS-FOUR-TRANSFORMATIONS; S01:ZZZA-A-0393..0395 |
| HPA-ZIWEI-015 | 1581 Jielan Kui/Yue Geng-stem variant | H | EXT-ZIWEI-JIELAN-1581:CH25 |
| HPA-ZIWEI-016 | 1581 Jielan Fire/Bell 巳酉丑 starting-branch variant | H | EXT-ZIWEI-JIELAN-1581:CH27 |
| HPA-ZIWEI-017 | TianShang/TianShi fixed Life-palace geometry | H | EXT-ZIWEI-JIELAN-1581:CH24; S01:ZZQS-A-1854/1855 |
| HPA-ZIWEI-018 | 1581 Jielan historical dignity table | H | EXT-ZIWEI-JIELAN-1581:CH69／CH70 |
| HPA-ZIWEI-019 | Five-bureau Changsheng ring anchor and direction | H | EXT-ZIWEI-JIELAN-1581:CH19; S01:ZZZA-PR-057 |
| HPA-ZIWEI-021 | Fu/Bi, Chang/Qu, DiKong/DiJie early-print placement geometry | H | EXT-ZIWEI-JIELAN-1581:CH22 |
| HPA-ZIWEI-022 | 1581 Jielan Mingzhu birth-year-branch basis | H | EXT-ZIWEI-JIELAN-1581:CH31 |
| HPA-ZIWEI-023 | Zi/Wu Shenzhu Fire/Bell textual composite | I | EXT-ZIWEI-JIELAN-1581:CH32; S01:ZZQS-A-2003 |
| HPA-ZIWEI-024 | Boshi Twelve-God ring | H | EXT-ZIWEI-JIELAN-1581:BOSHI12; S01:ZZQS-A-1862..1866 |
| HPA-ZMINOR-001 | 天哭 / 天虚 birth-year-branch geometry | H | S01:ZZQS-A-1886; S01:ZZQS-A-1887 |
| HPA-ZMINOR-002 | 红鸾 / 天喜 birth-year-branch geometry | H | S01:ZZQS-A-1918; S01:ZZQS-A-1919 |
| HPA-ZMINOR-003 | 龙池 / 凤阁 birth-year-branch geometry | H | S01:ZZQS-A-1893 |
| HPA-ZMINOR-004 | 台辅 / 封诰 birth-hour geometry | H | S01:ZZQS-A-1899; S01:ZZQS-A-1905 |
| HPA-ZMINOR-005 | 天刑 / 天姚 lunar-month geometry | H | S01:ZZQS-A-1872; S01:ZZQS-A-1873 |
| HPA-ZMINOR-006 | Year-based 解神 geometry (modern 年解 display) | H | S01:ZZQS-A-1945; EXT-ZIWEI-QUANSHU-RECEIVED / 卷二《安天德月德解神诀》 |
| HPA-ZMINOR-007 | 天厨 birth-year heavenly-stem ten-value table | H | EXT-WIKISOURCE-XINGXUE-DACHENG-TIANCHU / 《星学大成》(四库全书本)卷一《论天厨》; S01:ZZZA-PR-023 |
| HPA-ZMINOR-008 | 天寿 Body-palace basis + birth-year-branch offset | H | EXT-ZIWEI-JIELAN-1581 / 卷一第35章《安天才天寿台辅封诰星诀》; S01:ZZZA-A-0830..0834 |
| HPA-ZMINOR-009 | 天官 / 天福 birth-year-stem tables | H | EXT-ZIWEI-JIELAN-1581 / 卷一第37章《安天官贵人星诀》、第38章《安天福贵人星诀》; S01:ZZZA-PR-022 |
| HPA-ZMINOR-010 | 天空 birth-year-branch next-palace geometry | H | EXT-ZIWEI-JIELAN-1581 / 卷一第39章《安天空星诀》; S01:ZZZA-PR-027 |
| HPA-ZMINOR-011 | 旬中空亡 two-branch pair geometry (旬空 / 副旬 presentation split) | H | EXT-ZIWEI-JIELAN-1581 / 卷一第40章《定旬中空亡诀》; S01:ZZZA-PR-025 |
| HPA-ZMINOR-012 | 截路空亡 / 截空 pair and 正空/傍空 ordering | H | EXT-ZIWEI-JIELAN-1581 / 卷一第41章《定截路空亡诀》; S01:ZZZA-PR-024 |
| HPA-ZMINOR-013 | 孤辰 / 寡宿 birth-year-branch group table | H | EXT-ZIWEI-JIELAN-1581 / 卷一第43章《安孤辰寡宿星诀》; S01:ZZZA-PR-030 |
| HPA-ZMINOR-014 | 劫煞 birth-year-branch trine-group table | H | EXT-ZIWEI-JIELAN-1581 / 卷一第44章《安劫杀星诀》; S01:ZZZA-PR-031 |
| HPA-ZMINOR-015 | 华盖 birth-year-branch trine-group table | H | EXT-ZIWEI-JIELAN-1581 / 卷一第45章《安华盖星诀》; S01:ZZZA-PR-035 |
| HPA-ZMINOR-016 | 咸池 placement geometry / 1581 桃花杀 naming bridge | H | EXT-ZIWEI-JIELAN-1581 / 卷一第46章《安桃花杀诀》; S01:ZZZA-PR-036 |
| HPA-ZMINOR-017 | 大耗 birth-year-branch placement | H | EXT-ZIWEI-JIELAN-1581 / 卷一第47章《安大耗杀诀》; S01:ZZZA-PR-032 |
| HPA-ZMINOR-018 | 破碎 birth-year-branch group table | H | EXT-ZIWEI-JIELAN-1581 / 卷一第48章《安破碎杀诀》; S01:ZZZA-PR-034 |
| HPA-ZMINOR-019 | 天才 Life-palace basis + birth-year-branch offset | H | EXT-ZIWEI-JIELAN-1581 / 卷一第35章《安天才天寿台辅封诰星诀》; S01:ZZZA-PR-041 |
| HPA-ZMINOR-020 | Standalone 蜚廉 birth-year-branch table vs 博士十二神 飞/蜚廉 identity | H | EXT-SHIDIAN-LISHIMINGYUAN-FEILIAN; EXT-CTEXT-XINGLI-KAOYUAN-FEILIAN; EXT-WIKISOURCE-XIEJI-BIANFANG-FEILIAN; docs/research/ZIWEI-STANDALONE-FEILIAN-HISTORICAL-IDENTITY-CLOSURE-R1.json |
| HPA-ZMINOR-021 | 龙德 birth-year-branch +7 geometry / 岁前十二神 projection | H | EXT-ZIWEI-JIELAN-1581 / 卷一第49章《安生年太岁十二神诀》; S01:ZZZA-PR-037 |
| HPA-ZMINOR-022 | Natal 月德 birth-year Si-start geometry and historical adoption scope | I | EXT-CTEXT-SHENFENG-TONGKAO / 鸾喜二德解神歌; S01:ZZQS-A-1944; EXT-ZIWEI-QUANSHU-RECEIVED / 卷二《安天德月德解神诀》 |
| HPA-ZMINOR-023 | 月解 / month-based 解神 two-month table | H | EXT-SHIDIAN-LISHIMINGYUAN-JIESHEN; EXT-CTEXT-XINGLI-KAOYUAN-JIESHEN; EXT-WIKISOURCE-XIEJI-BIANFANG-JIESHEN; docs/research/ZIWEI-MONTH-JIESHEN-HISTORICAL-IDENTITY-CLOSURE-R1.json |
| HPA-ZMINOR-024 | 天巫 lunar-month table | I | EXT-SHIDIAN-LISHIMINGYUAN-TIANWU; EXT-CTEXT-XINGLI-KAOYUAN-TIANWU; EXT-WIKISOURCE-XIEJI-BIANFANG-TIANWU; docs/research/ZIWEI-TIANWU-HOMONYM-MECHANICAL-SEPARATION-R1.json |
| HPA-ZMINOR-025 | 天月 lunar-month twelve-value table | I | EXT-IZTRO-TIANYUE-MODERN; EXT-XSTARS-TIANYUE-MODERN; docs/research/ZIWEI-TIANYUE-MODERN-RECEIVED-SOURCE-BOUNDARY-R1.json |
| HPA-ZMINOR-026 | 阴煞 lunar-month six-palace cycle | I | EXT-IZTRO-YINSHA-MODERN; EXT-XSTARS-YINSHA-MODERN; docs/research/ZIWEI-YINSHA-MODERN-RECEIVED-SOURCE-BOUNDARY-R1.json |
| HPA-ZIWEI-025 | TaiSui / Suiqian twelve-member birth-branch ring: geometry vs label candidates | D | EXT-ZIWEI-JIELAN-SHIXINGJI-RECEIVED-RINGS 卷一（五）; docs/research/ZIWEI-THREE-RING-SOURCE-SCOPE-AUDIT-R1.json |
| HPA-ZIWEI-026 | Jiangqian twelve-member trine-wang ring and temporal/source scope | I | EXT-WANGTINGZHI-ANXING-RECEIVED-RING-TEXT printed pp47–48 heading40; EXT-ZIWEI-JIELAN-1581:CH58; docs/research/ZIWEI-JIANGQIAN-TEMPORAL-SOURCE-SCOPE-CLOSURE-R1.json |
| HPA-ZMINOR-027 | Natal 天德 birth-year You-start geometry and historical adoption scope | I | EXT-CTEXT-SHENFENG-TONGKAO / 鸾喜二德解神歌; S01:ZZQS-A-1943; EXT-ZIWEI-QUANSHU-RECEIVED / 卷二《安天德月德解神诀》 |

已有图谱的关键分族核对（读实际节点与边）：
- 四化 HPA-ZIWEI-010/014：TG-E0157–0162 保留《捷览》CH23、识典《全书》卷三、中州王亭之三表的限定见证及平行关系；ZT-016仍N，不从十干四化推出自化方向。
- 庙陷 HPA-ZIWEI-009/018：TG-E0163/0164 连接CH69/70原始语词规则族；现代庙旺显示为M，不以古籍存在推出现行整表。
- 蜚廉 ZMINOR-020：TG-E0117–0124 分开年支表与博士飞廉；解神 ZMINOR-006/023：E0125–0134 分开月与年基；天巫 ZMINOR-024：E0135–0144 历法月神与紫微四马月表平行，不能以同名补历史采用。
- 天德/月德 ZMINOR-022/027、ZTEMP-007：E0145–0151 只支持相应年运、岁支起位或结构候选；本命采纳与流年分立，不补作确定传承。天才/天寿 ZMINOR-019/008：E0152–0154 分命宫与身宫输入。天月/阴煞 ZMINOR-025/026保持I。
- 辅星魁钺庚干、火铃巳酉丑、命主/身主火铃合词、博士/将前/岁前三环，按ZIWEI-007/011/012/015/016/019/021–026独立处理；CH25/27/31/32与现代归一化不可混同。剩余杂曜和动态条目只有Matrix/受读入口者，不强造原页图谱边。四柱FLOW及STRUCT/COMB全ID已在G1定位，现代时间投影与古典本命继承需分别追证，不能以历史支持字样证明古代已有七层软件结构。

### G3. 58项风险及四门槛复核（非终验）

完整读取58项风险对象，核验每项证据边界、缺失证据、下一动作、关闭条件字段存在；58项均未解决，其中BLOCKED_SOURCE_ACCESS 3、OPEN 55，P0五项不动。未实施各项原页取证，字段存在不代表内容实证充分。产品未含四项逐项交叉：HPA-ZDATE-006 → TW-OPEN-0006；HPA-DAYUN-CAL-002 → TW-OPEN-0008；HPA-DAYUN-CAL-003 → TW-OPEN-0010；HPA-DAYUN-CAL-004 → TW-OPEN-0011。其他53项P1仍留原优先级；0003/0004/0009属抄本身份/卷页，0012–0017属早期源流与跨域术式，0018–0051属实际使用、原刊、书目和近现代出版传播，0052–0058属东南亚及全球区域边界。分组仅导航，不改变原条目。

| 第一阶段门槛 | 本轮有限判定 | 未完成边界 |
|---|---|---|
| 双史纲可读、按时代和证据 | 结构具备；两份史纲有独立时间线及来源索引 | 旧段落的时间性缺口与新增批次需合并阅读；未完成历史事实终验 |
| 时代×知识×地域覆盖表 | 结构具备；15FF-O三轴及U/E/A/B/C/D分层 | 13地域组非国家穷举；未把材料条目数当覆盖率 |
| 关键作品版本与规则族 | 222/222 ID导航、24术式模块已具；图谱630/461 | 仍部分符合：原刻目标篇页、动态规则、杂曜、四柱派生/神煞等链未完全建立；不能以本索引代替证据链 |
| 风险与矛盾公开保留 | 58条在册，五P0、四未入产品均有入口 | 风险台账明确非穷尽；需对剩余未建图/未具原页链按证据缺口逐项归并，不能以台账数字宣告全史完成 |

下一步：优先复用现有杂曜/四化/三环和四柱动态字段的历史审计报告，对G2所列源入口逐族判定已存在的篇页图谱、限定受读或尚缺证据（不制造重复节点）；随后将G1全量导航与图谱规则族做双向可查映射，区分纯现代字段，不以222条机械建222节点。再评估第三/第四门槛，第一阶段暂不终验。此检查点只增加索引和结构审查，未改变任何权威历史裁决、风险状态、源登记、图谱、产品或当前下一任务；因此六个权威JSON和R2视图保持不变，不另增语义版本。transmission_impact: NONE。


## H. 15FF-Q续｜紫微动态规则、环系双向索引（待原子图谱发布的检查点，2026-11-27）

基线 e54e4895676b1a32ad6b9eedc5a5a53402bdda5f / ad0c913fbc47e1fabe850ce65ce24e798dae6f40；六个R2绑定与精确HEAD树一致。该HEAD读取时20项Actions，19成功、clean-training-system运行中；未取得精确HEAD连续性专项成功，故回退读取六个权威blob。Matrix222/222、来源1488/276、图630/461、58未决（五P0）不变。复读05、08A/B、12MV及Matrix的实际规则定位和根登记；仅复用既有来源，不新增原件，不作全分片无命中结论。旧报告的早期未入产品状态不得覆盖最新Matrix。

### H1. 待发布的规则族映射（22族，11个篇页）

以下映射为本轮完成的证据范围索引，拟新增关系均为限定ATTESTS，不为1581原刻直接证据，也不新增直接承袭或师承。各规则ID与节点ID可双向导航；尚未写入权威图谱，拟节点、拟关系不得当作现有图谱事实。

| Matrix ID | 拟规则节点 | 拟受读篇页 | 证据作用域 |
|---|---|---|---|
| HPA-ZT-001 | `RULE-FAMILY-ZIWEI-DAXIAN-DIRECTION` — 大限年干阴阳性别顺逆 | `PASSAGE-JIELAN-RECEIVED-CH51-DAXIAN` — 《捷览》CH51定大限诀受读 | 方向，非四柱交运 |
| HPA-ZT-002 | `RULE-FAMILY-ZIWEI-DAXIAN-BUREAU-AGE` — 大限以局数为起岁 | `PASSAGE-JIELAN-RECEIVED-CH51-DAXIAN` — 《捷览》CH51定大限诀受读 | 名义起岁 |
| HPA-ZT-003 | `RULE-FAMILY-ZIWEI-DAXIAN-TEN-YEAR-PALACE-STEP` — 大限命宫起每十年移一宫 | `PASSAGE-JIELAN-RECEIVED-CH51-DAXIAN` — 《捷览》CH51定大限诀受读 | 非公历周年交界 |
| HPA-ZT-008 | `RULE-FAMILY-ZIWEI-XIAOXIAN-YEAR-BRANCH-AGE-ONE` — 小限生年支起一岁、男女顺逆 | `PASSAGE-JIELAN-RECEIVED-CH52-XIAOXIAN` — 《捷览》CH52定小限诀受读 | 非四柱小运 |
| HPA-ZT-004 / HPA-ZTEMP-001 | `RULE-FAMILY-ZIWEI-FLOW-YEAR-TAISUI-ANCHOR` — 流年太岁所在支宫为岁建锚 | `PASSAGE-JIELAN-RECEIVED-CH54-TEMPORAL` — 《捷览》CH54安流年斗君法受读 | 与斗君正月宫分立 |
| HPA-ZT-005 | `RULE-FAMILY-ZIWEI-FLOW-YEAR-DOUJUN-BIRTH-MONTH-HOUR` — 太岁宫逆数生月顺数生时定斗君 | `PASSAGE-JIELAN-RECEIVED-CH54-TEMPORAL` — 《捷览》CH54安流年斗君法受读 | 闰月另证 |
| HPA-ZT-006 | `RULE-FAMILY-ZIWEI-FLOW-MONTH-DOUJUN-SEQUENCE` — 斗君起正月顺行逐月 | `PASSAGE-JIELAN-RECEIVED-CH54-TEMPORAL` — 《捷览》CH54安流年斗君法受读 | 普通月序，闰月另族 |
| HPA-ZT-013 / HPA-ZTEMP-003 | `RULE-FAMILY-ZIWEI-FLOW-DAY-MONTH-PALACE-ANCHOR` — 月宫起初一顺数流日 | `PASSAGE-JIELAN-RECEIVED-CH54-TEMPORAL` — 《捷览》CH54安流年斗君法受读 | 宫序非换日及流日干支 |
| HPA-ZT-014 / HPA-ZTEMP-004 | `RULE-FAMILY-ZIWEI-FLOW-HOUR-DAY-PALACE-ANCHOR` — 流日宫起子时顺数流时 | `PASSAGE-JIELAN-RECEIVED-CH54-TEMPORAL` — 《捷览》CH54安流年斗君法受读 | 日宫锚候选 |
| HPA-ZT-007 / HPA-ZTEMP-002 | `RULE-FAMILY-ZIWEI-FIVE-TIGERS-REGULAR-MONTH-STEM` — 五组年干起寅月干并顺布 | `PASSAGE-WUXING-JINGJI-RECEIVED-V28-QIYUEJIAN` — 《五行精纪》卷28起月建例受读 | 只证配干形式，非紫微宫序与四柱节月界 |
| HPA-ZT-014 / HPA-ZTEMP-005 | `RULE-FAMILY-ZIWEI-ZHONGZHOU-FLOW-HOUR-FIXED-BRANCH` — 中州固定子垣起子时 | `PASSAGE-ZHONGZHOU-CHUJI-FIXED-BRANCH-HOUR` — 中州初级讲义固定地支宫流时受读 | 不等于日宫锚，不择胜者 |
| HPA-ZT-009 / HPA-ZAUX-001 | `RULE-FAMILY-ZIWEI-ANNUAL-LU-YANG-TUO` — 流年年干重排禄羊陀 | `PASSAGE-FULLBOOK-RECEIVED-ANNUAL-LU-YANG-TUO` — 《全书》卷二流禄流羊流陀受读 | 己丑禄午羊未陀巳，限流年 |
| HPA-ZT-009 / HPA-ZAUX-002 | `RULE-FAMILY-ZIWEI-ZHONGZHOU-DAXIAN-LU-YANG-TUO` — 中州大限命宫干起禄羊陀 | `PASSAGE-ZHONGZHOU-ANXING-FLOW-AUXILIARIES` — 王亭之《安星法及推断实例》流曜、流昌曲、运马流马 | 大限宫干限定 |
| HPA-ZT-009 / HPA-ZAUX-003 | `RULE-FAMILY-ZIWEI-ZHONGZHOU-FINE-LAYER-LU-YANG-TUO` — 中州月日时目标干起禄羊陀 | `PASSAGE-ZHONGZHOU-ANXING-FLOW-AUXILIARIES` — 王亭之《安星法及推断实例》流曜、流昌曲、运马流马 | 时层授权与几何分开 |
| HPA-ZT-010 / HPA-ZAUX-004 | `RULE-FAMILY-ZIWEI-ZHONGZHOU-FLOW-CHANG-QU` — 中州流昌流曲独立十干表 | `PASSAGE-ZHONGZHOU-ANXING-FLOW-AUXILIARIES` — 王亭之《安星法及推断实例》流曜、流昌曲、运马流马 | 巳酉起位不入四墓，不等于本命昌曲 |
| HPA-ZT-011 / HPA-ZAUX-005 | `RULE-FAMILY-ZIWEI-ZHONGZHOU-FLOW-KUI-YUE-NATAL-REUSE` — 中州流魁流钺依本命安法 | `PASSAGE-ZHONGZHOU-ANXING-FLOW-AUXILIARIES` — 王亭之《安星法及推断实例》流曜、流昌曲、运马流马 | 只证复用方法，不证明S01具体表唯一 |
| HPA-ZT-012 / HPA-ZAUX-007 | `RULE-FAMILY-ZIWEI-ZHONGZHOU-DAXIAN-YUNMA` — 中州运马取大限命宫支 | `PASSAGE-ZHONGZHOU-ANXING-FLOW-AUXILIARIES` — 王亭之《安星法及推断实例》流曜、流昌曲、运马流马 | 不外推月日时 |
| HPA-ZT-012 / HPA-ZAUX-008 | `RULE-FAMILY-ZIWEI-ZHONGZHOU-ANNUAL-LIUMA` — 中州流马取流年支 | `PASSAGE-ZHONGZHOU-ANXING-FLOW-AUXILIARIES` — 王亭之《安星法及推断实例》流曜、流昌曲、运马流马 | 非大限运马或四柱驿马 |
| HPA-ZIWEI-019 | `RULE-FAMILY-ZIWEI-FIVE-BUREAU-CHANGSHENG-RING` — 紫微五局长生锚及顺逆 | `PASSAGE-JIELAN-RECEIVED-CH19-CHANGSHENG` — 《捷览》CH19定五局长生例受读 | 金巳木亥火寅水土申，非四柱日主长生 |
| HPA-ZIWEI-024 | `RULE-FAMILY-ZIWEI-BOSHI-TWELVE-RING` — 博士十二神禄存锚及阴阳性别顺逆 | `PASSAGE-JIELAN-RECEIVED-BOSHI12` — 《捷览》博士十二神诀受读 | 异名未归一，非独立蜚廉 |
| HPA-ZIWEI-025 / HPA-ZMINOR-021 | `RULE-FAMILY-ZIWEI-SUIQIAN-YEAR-BRANCH-RING` — 岁前年支起太岁顺行十二位 | `PASSAGE-JIELAN-SHIXINGJI-RECEIVED-SUIQIAN` — 拾星集《捷览》岁前受读 | 坐标与龙德第7位，四个标签桥接未决 |
| HPA-ZIWEI-026 | `RULE-FAMILY-ZIWEI-JIANGQIAN-MODERN-TRINE-WANG-RING` — 现代将前三合旺支起十二成员顺行 | `PASSAGE-ZHONGZHOU-ANXING-RECEIVED-JIANGQIAN` — 王亭之安星法传录印页47–48第40条 | 仅现代几何，早期出处与时层未证 |

### H2. 受读篇页来源定位（均为现有根登记）

| 拟篇页节点 | 来源及既有考据 | 限制 |
|---|---|---|
| `PASSAGE-JIELAN-RECEIVED-CH51-DAXIAN` | EXT-ZIWEI-JIELAN-1581；docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-05-ZIWEI-ROLES-LIMITS-RINGS.md | 1581原刻目标叶未核 |
| `PASSAGE-JIELAN-RECEIVED-CH52-XIAOXIAN` | EXT-ZIWEI-JIELAN-1581；docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-05-ZIWEI-ROLES-LIMITS-RINGS.md | 受读章节，非原印目标叶 |
| `PASSAGE-JIELAN-RECEIVED-CH54-TEMPORAL` | EXT-ZIWEI-JIELAN-1581；docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-08-ZIWEI-TEMPORAL-FRAMES-B.md | 不以2016开卷影印作目标页直证 |
| `PASSAGE-WUXING-JINGJI-RECEIVED-V28-QIYUEJIAN` | EXT-CTEXT-WUXING-JINGJI-V28；docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-08-ZIWEI-TEMPORAL-FRAMES-B.md | 配干表，非术式采用及月界证据 |
| `PASSAGE-ZHONGZHOU-CHUJI-FIXED-BRANCH-HOUR` | EXT-WANGTINGZHI-ZHONGZHOU-CHUJI；docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-08-ZIWEI-TEMPORAL-FRAMES-B.md | 现代流派文字 |
| `PASSAGE-FULLBOOK-RECEIVED-ANNUAL-LU-YANG-TUO` | EXT-ZIWEI-QUANSHU-RECEIVED；docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-08-ZIWEI-DYNAMIC-AUXILIARIES-A.md | 己丑例，未绑定独立原叶 |
| `PASSAGE-ZHONGZHOU-ANXING-FLOW-AUXILIARIES` | EXT-WANGTINGZHI-ANXING-2013；docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-08-ZIWEI-DYNAMIC-AUXILIARIES-A.md | 2013书目不替代规则原页 |
| `PASSAGE-JIELAN-RECEIVED-CH19-CHANGSHENG` | EXT-ZIWEI-JIELAN-1581；docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json | 紫微五局长生，非四柱日干长生 |
| `PASSAGE-JIELAN-RECEIVED-BOSHI12` | EXT-ZIWEI-JIELAN-1581；docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-05-ZIWEI-ROLES-LIMITS-RINGS.md | 官符/官府、飞/蜚语境待分 |
| `PASSAGE-JIELAN-SHIXINGJI-RECEIVED-SUIQIAN` | EXT-ZIWEI-JIELAN-SHIXINGJI-RECEIVED-RINGS；docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-THREE-RING-SOURCE-SCOPE-AND-IDENTITY-AUDIT-MV.md | 2015/2025整理层，非1581原刻 |
| `PASSAGE-ZHONGZHOU-ANXING-RECEIVED-JIANGQIAN` | EXT-WANGTINGZHI-ANXING-RECEIVED-RING-TEXT；docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-THREE-RING-SOURCE-SCOPE-AND-IDENTITY-AUDIT-MV.md | 现代传录未绑定2013物件，早期将前未获 |

复用已有节点：ZT-015/ZTEMP-006→RULE-FAMILY-ZIWEI-ZHONGZHOU-FLOW-LEAP-HALF-SPLIT（E0459）；TIME-010→RULE-FAMILY-ZIWEI-NANYANGTANG-NATAL-LEAP-NEXT-MONTH；ZTEMP-007→两流年二德族（E0145/0146）。本命和流运闰月分开，不将流日顺数推定为跨日宫必然连续。ZAUX-006现代相容、ZT-016未形式化，不增历史边。ZIWEI-011为拆分汇总，ZIWEI-025四名称桥接与ZIWEI-026古源、时层未裁；已有独立蜚廉、博士飞廉、年解月解等关系保持不变。五虎配干与BAZI-017的形式可对照，不证明跨系统传承或节界同一。上述均不修改Matrix状态或产品候选。

### H3. 原子发布阻塞与恢复

已成功生成候选图谱blob c8eb896391fec7021e141c9058630bca22833c8f（拟663/483）和候选state blob d05c9214707a48241a1efb7a655b4bea40823e16（拟1.1576.0）。**二者均未纳入分支tree，不能当作远端当前事实；孤立对象可能被回收。** 对约367万字符的遗漏台账进行完整更新时，批量create_blob、独立create_blob以及create_tree内联content均出现HTTP/2连接读取错误。为维持原子性，不单独发布图谱或state，不压缩/删减历史台账来规避门禁。先提交本检查点保全实际证据映射；当前权威六文件及R2视图不变，state 1.1575.0、图630/461，58未决五P0，核心CLOSED。

恢复时优先从当前HEAD核实H段、CI及六权威绑定；尝试可靠的完整台账写入路径，再将11篇页+22规则族+22 ATTESTS、state/ledger/R2及本段发布结果同一原子提交。若候选blob不可读，使用H1/H2表重建（所有日期未定、REGISTERED_RECEIVED_TEXT_SCOPED、CONFIRMED/MEDIUM仅限scope，adjudication_batch=15FF-Q）。不擅自把待发布图谱算作已交付，不制造新来源或权威状态。可在不改变语义状态的前提下继续四柱动态继承与剩余本命辅杂曜的证据定位，但第三/第四门槛正式验收前必须完成本次待发布单元。transmission_impact: PENDING_ATOMIC_PUBLICATION。


### H4. 待发布单元恢复与原子交付（2026-11-27）

恢复基线 3bbf25805a3b1d85117be707187e7f6b1a21284c / b4e1e10daad9b1d6df42ba6916a1b472f4c4c5ae；六项R2绑定与远端树一致；读取时19/20 Actions成功，clean-training-system仍运行，未取得该HEAD连续性专项成功，故实际读取六权威blob回退。候选图谱与state对象均可回读。定位到原风险台账紧凑JSON为3,673,310字符（3,978,782 UTF-8字节，不含结尾换行），而重新二空格缩进后达4,182,132字符，额外508,822字符；此前HTTP/2错误的具体平台上限未证，但无损恢复原有紧凑序列化后完整ledger create_blob实际成功。未更改任何既有风险条目、历史checkpoint或原有图谱节点/边；逐对象核验保留全部58 issues及1006旧checkpoints，追加第1007个checkpoint；state旧focus完整保留，追加第3272条。图谱新33节点、22边，所有ID唯一及端点存在；22规则族、11受读篇页严格按H1/H2，不升级原页、版本、源流或师承证据。

本原子提交纳入graph c8eb896391fec7021e141c9058630bca22833c8f、state d05c9214707a48241a1efb7a655b4bea40823e16、ledger 271c3e8d7ef278b9ff692d0cc68db14004b54d55、重新派生R2及本检查点：state1.1576.0、图663/483、222/222 Matrix、1488来源/276分片、58 OPEN含五P0、核心CLOSED。精确HEAD远端CI结果须在提交后单独核验，不在提交前声称已通过。H3为当时真实阻塞，保留不覆盖。传输恢复仅解决本次，无证据保证未来无限增长；后续优先保持已有紧凑JSON，若再次失败再评估有验证门禁的历史归档分片方案，禁止删除历史或改写风险内容规避限制。

transmission_impact: 新增22个限定ATTESTS（TG-E0462–0483）、11受读篇页和22规则族；无新增直接抄传/师承/同版关系。NEXT 四柱动态继承与剩余紫微本命辅杂星的双向索引；第三/第四门槛仍待复评。


## I. 四柱动态继承／紫微本命辅杂曜双向导航检查点（2026-11-27）

固定基线 fa525e109e941653e74488f7d23b1f635c992f72 / c48c1ebb12bcfe2a38665a7a958f7c50096963a6。六个R2绑定逐一核对；直接读取六权威JSON（state、ledger、Matrix、root、manifest、graph）而非以空fetch_file正文冒认。精确HEAD连续性CI 45978846506已成功；分页观察时284项中仍有排队/执行，clean-training-system 45978849435尚未完成，不宣告全CI通过。PR 364为独立换日审计，仍OPEN，不合并。五项P0保留，0001/0002原叶访问阻塞、0005控制5/6最终0/6、0006夜子时候选、0007计时适配器；58风险不改。此单元仅复用已登记史料、既有审计和图谱，未检索新外部来源，未逐片搜索276分片，不作全库来源缺失断言。

### I1. 四柱动态十项双向导航（Matrix 10/10）

正向：目标投影→父本命规则→已有来源/图谱；反向：父规则仅给其现代消费者提供机械身份，不给整个现代时间轴授予历史地位。复读12ML、12MN、12MO与固定Matrix。以下候选新族仅为后续导航，不是已经新增的节点或关系。

| Matrix | 规则 | 当前状态 | 已有定位 | 对接与禁止越界 |
|---|---|---|---|---|
| HPA-BAZI-FLOW-001 | Unified target timeline 原局→大运→小运→流年→流月→流日→流时 | MODERN_COMPATIBILITY_ONLY | src/fortune_training/bazi_application/flow_service.py BaziApplicationFlowService._build_view; src/fortune_training/bazi_application/flow_integrity.py; docs/BAZI-ZIWEI-UNIFIED-TARGET-TIMELINE-R1.md | 仅现代统一时间轴；不建立古籍ATTESTS。 |
| HPA-BAZI-FLOW-002 | Target-layer Ten-God projection | HISTORICALLY_SUPPORTED | Inherited S11:YHZP-CH-016／017／057／065; NTL-9900014379 PDF pp37-39 / printed18-20 table; PDF p64 / printed47 day-self anchor; source content and locations are distinct from modern layer/API composition. | 父003→既有RULE-FAMILY-BAZI-TEN-GOD-RELATIONAL-IDENTITY（E0430）；藏干父002及FLOW-003另行定位。本命日干为参照，不改为目标干。 |
| HPA-BAZI-FLOW-003 | Target-layer hidden stems | HISTORICALLY_SUPPORTED | src/fortune_training/bazi_application/temporal_annotations.py temporal_classical_annotation; docs/BAZI-TEMPORAL-CLASSICAL-ANNOTATIONS-R1.md | 父002藏干成员；时层仅复用合法目标支，显示顺序是lineage而非独立历史规则。待独立藏干篇页锚。 |
| HPA-BAZI-FLOW-004 | Target-layer NaYin/XunKong/Twelve Growth | HISTORICALLY_SUPPORTED | src/fortune_training/bazi_application/temporal_annotations.py; src/fortune_training/bazi_application/classical_annotations.py; src/fortune_training/bazi_nayin_annotation/registry.py; inherited source locations in HPA-BAZI-006/007/008 | 父006/007/008；由子008/009/010拆分，汇总项不重复造一个古代规则族。 |
| HPA-BAZI-FLOW-005 | Temporal ShenSha target projection | MODERN_COMPATIBILITY_ONLY | docs/BAZI-TEMPORAL-SHENSHA-PROJECTION-R1.md; src/fortune_training/bazi_application/temporal_shensha.py | 父SHENSHA-001..021；保留每项来源及候选，temporal_applicability_status=NOT_CLASSICALLY_ARBITRATED；不建立神煞激活或预测关系。 |
| HPA-BAZI-FLOW-006 | Structural Context target projection | MODERN_COMPATIBILITY_ONLY | docs/BAZI-STRUCTURAL-CONTEXT-R1.md; docs/BAZI-TARGET-FLOW-STRUCTURAL-PROJECTION-R1.md; src/fortune_training/bazi_structural/generation.py; src/fortune_training/bazi_application/structural_projection.py | 父002/003/004/005/013及BAFF-002；中性结构事实的现代合成，不能作为古法统一结构。 |
| HPA-BAZI-FLOW-007 | Structural Support candidate projection | MODERN_COMPATIBILITY_ONLY | docs/BAZI-STRUCTURAL-SUPPORT-FOUNDATION-R1.md; docs/BAZI-TARGET-FLOW-STRUCTURAL-SUPPORT-PROJECTION-R1.md; src/fortune_training/bazi_structural_support/generation.py; src/fortune_training/bazi_application/structural_support_projection.py | 父002/004/013、BAFF-002、FLOW-003/006；现代证据类别候选，非旺衰、格局、用神裁决。 |
| HPA-BAZI-FLOW-008 | Target-layer NaYin identity projection | HISTORICALLY_SUPPORTED | HPA-BAZI-006; S11:YHZP-CH-014; src/fortune_training/bazi_nayin_annotation/registry.py | 父006纳音；已有RULE-FAMILY-ZIWEI-RECEIVED-NAYIN-GANZHI-ELEMENT仅作同型检索入口，仍需四柱作品/表的独立见证，不能跨系统挪用证据。 |
| HPA-BAZI-FLOW-009 | Target-layer XunKong identity projection | HISTORICALLY_SUPPORTED | HPA-BAZI-007; S14:YHZP-CH-047; S14:7.7; src/fortune_training/bazi_application/classical_annotations.py | 父007旬空；合法目标干支所属旬的两空支；不等于紫微副旬显示或吉凶判断。待四柱独立篇页锚。 |
| HPA-BAZI-FLOW-010 | Target-layer Twelve-Growth identity projections | HISTORICALLY_SUPPORTED | HPA-BAZI-008; S11:YHZP-CH-015; src/fortune_training/bazi_application/classical_annotations.py; src/fortune_training/bazi_application/temporal_annotations.py | 父008十二长生；本命日主→目标支、目标干→目标支两视图；非紫微五局长生或旺衰预测。待四柱独立篇页锚。 |

反向索引：BAZI-003→FLOW-002；BAZI-002→FLOW-002/003/006/007；BAZI-004/013、BAFF-002→FLOW-006/007；BAZI-005→FLOW-006；BAZI-006→FLOW-004/008；BAZI-007→FLOW-004/009；BAZI-008→FLOW-004/010；SHENSHA-001..021→FLOW-005；FLOW-003→FLOW-002/007，FLOW-006→FLOW-007。FLOW-001现代组合总轴不作为以上历史规则的共同祖本。FLOW-003的父002由12ML明确，Matrix该行无显式upstream_rule_ids，本文只记录可复核导航而不直接改Matrix字段。12MN所述profile同步是既有PROV-DEFECT-009，不重复计为新缺陷。

### I2. 紫微本命杂曜全27项对接表

读取07A/B/C、固定Matrix与全部663图谱节点/483边。以下是逐项当前导航及候选入图边界，并非27项新历史裁决；其中受读章名、项目语料定位不能替代1581原刻目标叶。历史身份与现代显示保持分立。

| Matrix | 规则 | 当前状态 | 已有定位 | 对接或待核入口 |
|---|---|---|---|---|
| HPA-ZMINOR-001 | 天哭 / 天虚 birth-year-branch geometry | HISTORICALLY_SUPPORTED | S01:ZZQS-A-1886; S01:ZZQS-A-1887 | 候选新族：生年支天哭/天虚，分两输出；S01受读定位待绑定原页。 |
| HPA-ZMINOR-002 | 红鸾 / 天喜 birth-year-branch geometry | HISTORICALLY_SUPPORTED | S01:ZZQS-A-1918; S01:ZZQS-A-1919 | 候选新族：生年支红鸾/天喜；对宫关系不证明历史传承。 |
| HPA-ZMINOR-003 | 龙池 / 凤阁 birth-year-branch geometry | HISTORICALLY_SUPPORTED | S01:ZZQS-A-1893 | 候选新族：生年支龙池/凤阁，两方向分别审。 |
| HPA-ZMINOR-004 | 台辅 / 封诰 birth-hour geometry | HISTORICALLY_SUPPORTED | S01:ZZQS-A-1899; S01:ZZQS-A-1905 | 候选新族：生时台辅/封诰，另核《捷览》CH35目标文字，不能只由篇名推定完整表。 |
| HPA-ZMINOR-005 | 天刑 / 天姚 lunar-month geometry | HISTORICALLY_SUPPORTED | S01:ZZQS-A-1872; S01:ZZQS-A-1873 | 候选新族：农历月天刑/天姚，两起宫独立。 |
| HPA-ZMINOR-006 | Year-based 解神 geometry (modern 年解 display) | HISTORICALLY_SUPPORTED | S01:ZZQS-A-1945; EXT-ZIWEI-QUANSHU-RECEIVED / 卷二《安天德月德解神诀》 | 复用 RULE-FAMILY-ZIWEI-JIESHEN-YEAR，E0147仅受读年支语境；不合并月解。 |
| HPA-ZMINOR-007 | 天厨 birth-year heavenly-stem ten-value table | HISTORICALLY_SUPPORTED | EXT-WIKISOURCE-XINGXUE-DACHENG-TIANCHU / 《星学大成》(四库全书本)卷一《论天厨》; S01:ZZZA-PR-023 | 复用 RULE-FAMILY-ZIWEI-NATAL-TIANCHU-CURRENT；E0156 PROBABLE，古天厨表不证明紫微采用。 |
| HPA-ZMINOR-008 | 天寿 Body-palace basis + birth-year-branch offset | HISTORICALLY_SUPPORTED | EXT-ZIWEI-JIELAN-1581 / 卷一第35章《安天才天寿台辅封诰星诀》; S01:ZZZA-A-0830..0834 | 复用 RULE-FAMILY-ZIWEI-NATAL-TIANSHOU-BODY-BASIS；E0153，身宫基准非命宫。 |
| HPA-ZMINOR-009 | 天官 / 天福 birth-year-stem tables | HISTORICALLY_SUPPORTED | EXT-ZIWEI-JIELAN-1581 / 卷一第37章《安天官贵人星诀》、第38章《安天福贵人星诀》; S01:ZZZA-PR-022 | 候选两族：天官/天福生年干表，《捷览》CH37/38分别入图。 |
| HPA-ZMINOR-010 | 天空 birth-year-branch next-palace geometry | HISTORICALLY_SUPPORTED | EXT-ZIWEI-JIELAN-1581 / 卷一第39章《安天空星诀》; S01:ZZZA-PR-027 | 候选新族：生年支下一宫天空；非地空。 |
| HPA-ZMINOR-011 | 旬中空亡 two-branch pair geometry (旬空 / 副旬 presentation split) | HISTORICALLY_SUPPORTED | EXT-ZIWEI-JIELAN-1581 / 卷一第40章《定旬中空亡诀》; S01:ZZZA-PR-025 | 候选新族：旬中两空支；正副显示另层，不倒投古文。 |
| HPA-ZMINOR-012 | 截路空亡 / 截空 pair and 正空/傍空 ordering | HISTORICALLY_SUPPORTED | EXT-ZIWEI-JIELAN-1581 / 卷一第41章《定截路空亡诀》; S01:ZZZA-PR-024 | 候选新族：截路空亡两值及正傍次序分别审；非旬空。 |
| HPA-ZMINOR-013 | 孤辰 / 寡宿 birth-year-branch group table | HISTORICALLY_SUPPORTED | EXT-ZIWEI-JIELAN-1581 / 卷一第43章《安孤辰寡宿星诀》; S01:ZZZA-PR-030 | 候选两族：孤辰/寡宿年支组；不借同名四柱神煞。 |
| HPA-ZMINOR-014 | 劫煞 birth-year-branch trine-group table | HISTORICALLY_SUPPORTED | EXT-ZIWEI-JIELAN-1581 / 卷一第44章《安劫杀星诀》; S01:ZZZA-PR-031 | 候选新族：劫煞年支三合组；不等于四柱时层适用。 |
| HPA-ZMINOR-015 | 华盖 birth-year-branch trine-group table | HISTORICALLY_SUPPORTED | EXT-ZIWEI-JIELAN-1581 / 卷一第45章《安华盖星诀》; S01:ZZZA-PR-035 | 候选新族：华盖年支三合组；同名不证明从四柱移植。 |
| HPA-ZMINOR-016 | 咸池 placement geometry / 1581 桃花杀 naming bridge | HISTORICALLY_SUPPORTED | EXT-ZIWEI-JIELAN-1581 / 卷一第46章《安桃花杀诀》; S01:ZZZA-PR-036 | 候选新族：桃花杀/咸池几何与名称桥分层。 |
| HPA-ZMINOR-017 | 大耗 birth-year-branch placement | HISTORICALLY_SUPPORTED | EXT-ZIWEI-JIELAN-1581 / 卷一第47章《安大耗杀诀》; S01:ZZZA-PR-032 | 候选新族：独立大耗，区别岁前、博士同名成员。 |
| HPA-ZMINOR-018 | 破碎 birth-year-branch group table | HISTORICALLY_SUPPORTED | EXT-ZIWEI-JIELAN-1581 / 卷一第48章《安破碎杀诀》; S01:ZZZA-PR-034 | 候选新族：破碎年支分组。 |
| HPA-ZMINOR-019 | 天才 Life-palace basis + birth-year-branch offset | HISTORICALLY_SUPPORTED | EXT-ZIWEI-JIELAN-1581 / 卷一第35章《安天才天寿台辅封诰星诀》; S01:ZZZA-PR-041 | 复用 RULE-FAMILY-ZIWEI-NATAL-TIANCAI-LIFE-BASIS；E0152，命宫基准。 |
| HPA-ZMINOR-020 | Standalone 蜚廉 birth-year-branch table vs 博士十二神 飞/蜚廉 identity | HISTORICALLY_SUPPORTED | EXT-SHIDIAN-LISHIMINGYUAN-FEILIAN; EXT-CTEXT-XINGLI-KAOYUAN-FEILIAN; EXT-WIKISOURCE-XIEJI-BIANFANG-FEILIAN; docs/research/ZIWEI-STANDALONE-FEILIAN-HISTORICAL-IDENTITY-CLOSURE-R1.json | 复用 RULE-FAMILY-FEILIAN-YEAR-BRANCH；E0117–0119；区别RULE-FAMILY-ZIWEI-BOSHI-FEILIAN。 |
| HPA-ZMINOR-021 | 龙德 birth-year-branch +7 geometry / 岁前十二神 projection | HISTORICALLY_SUPPORTED | EXT-ZIWEI-JIELAN-1581 / 卷一第49章《安生年太岁十二神诀》; S01:ZZZA-PR-037 | 复用 RULE-FAMILY-ZIWEI-SUIQIAN-YEAR-BRANCH-RING；E0482；龙德位置与名称桥分立。 |
| HPA-ZMINOR-022 | Natal 月德 birth-year Si-start geometry and historical adoption scope | SOURCE_INSUFFICIENT | EXT-CTEXT-SHENFENG-TONGKAO / 鸾喜二德解神歌; S01:ZZQS-A-1944; EXT-ZIWEI-QUANSHU-RECEIVED / 卷二《安天德月德解神诀》 | 复用 RULE-FAMILY-ZIWEI-NATAL-YUEDE-SI-START；E0148 POSSIBLE；本命采用证据未足，流年子起另族。 |
| HPA-ZMINOR-023 | 月解 / month-based 解神 two-month table | HISTORICALLY_SUPPORTED | EXT-SHIDIAN-LISHIMINGYUAN-JIESHEN; EXT-CTEXT-XINGLI-KAOYUAN-JIESHEN; EXT-WIKISOURCE-XIEJI-BIANFANG-JIESHEN; docs/research/ZIWEI-MONTH-JIESHEN-HISTORICAL-IDENTITY-CLOSURE-R1.json | 复用 RULE-FAMILY-JIESHEN-MONTH；E0125/0128/0131；E0134并存非同算法。 |
| HPA-ZMINOR-024 | 天巫 lunar-month table | SOURCE_INSUFFICIENT | EXT-SHIDIAN-LISHIMINGYUAN-TIANWU; EXT-CTEXT-XINGLI-KAOYUAN-TIANWU; EXT-WIKISOURCE-XIEJI-BIANFANG-TIANWU; docs/research/ZIWEI-TIANWU-HOMONYM-MECHANICAL-SEPARATION-R1.json | 复用 RULE-FAMILY-ZIWEI-TIANWU-FOUR-HORSE-MONTH；E0144仅并存，择日月建前二辰非紫微月表。 |
| HPA-ZMINOR-025 | 天月 lunar-month twelve-value table | SOURCE_INSUFFICIENT | EXT-IZTRO-TIANYUE-MODERN; EXT-XSTARS-TIANYUE-MODERN; docs/research/ZIWEI-TIANYUE-MODERN-RECEIVED-SOURCE-BOUNDARY-R1.json | 候选现代天月月表；无足够早期原页，不新增历史传承边。 |
| HPA-ZMINOR-026 | 阴煞 lunar-month six-palace cycle | SOURCE_INSUFFICIENT | EXT-IZTRO-YINSHA-MODERN; EXT-XSTARS-YINSHA-MODERN; docs/research/ZIWEI-YINSHA-MODERN-RECEIVED-SOURCE-BOUNDARY-R1.json | 候选现代阴煞六宫循环；无足够早期原页，不新增历史传承边。 |
| HPA-ZMINOR-027 | Natal 天德 birth-year You-start geometry and historical adoption scope | SOURCE_INSUFFICIENT | EXT-CTEXT-SHENFENG-TONGKAO / 鸾喜二德解神歌; S01:ZZQS-A-1943; EXT-ZIWEI-QUANSHU-RECEIVED / 卷二《安天德月德解神诀》 | 复用 RULE-FAMILY-ZIWEI-NATAL-TIANDE-YOU-START；E0149 POSSIBLE；起宫同流年而输入不同，不升级本命采用。 |

补充本命核心辅星：ZIWEI-007为候选总族，015《捷览》CH25庚干魁钺异表、016 CH27巳酉丑火铃起支异法、021 CH22左辅右弼/昌曲/地空地劫各分独立规则；017 CH24天伤天使固定命宫几何，不能替008整个R4杂曜源不足项；009运行时庙旺为现代兼容、018 CH69/70历史表另族；012星曜角色/依赖争议、022 CH31命主年支依据、023 CH32子午身主火铃复合源不足应保持独立。下一步核读各章具体已登记受读文本及先前审计，按精确机械输入、表项和边界生成候选图谱，勿把篇名当作整表实证。上述涉及源不足的ZMINOR-022/024/025/026/027及ZIWEI-008/023均保持原状态。

### I3. 恢复与验收边界

本次建立10项动态与27项本命杂曜的可重放导航，另明确11个核心辅星/角色/庙旺Matrix ID的拆分入口；均是既有222项的索引完善，不增加已审计行数、来源、图谱边或历史裁决数。未改语义状态/R2/Matrix/graph/ledger，故无新状态版本及风险结项。此前H4已经正式发布，不再重复。当前仍为15FF-Q未结项；下一轮按I1/I2中明确证据逐族核对、语义去重并原子发布新图谱和状态（优先四柱藏干、纳音、旬空、十二长生与紫微《捷览》CH35/37–48等可定位受读族）；随后才复评第三/第四门槛。transmission_impact: NONE（仅索引检查点）。核心CLOSED，预测仍OUT_OF_SCOPE。


## J. 四柱派生与紫微本命杂曜实际图谱回填（2026-11-27）

基线 c3fa2dcec668e4622c65e09b2864208c9bea43b7 / a0085b5c8fbe071a41e5465633c281df4aba30a9，20/20 Actions success（clean-training-system 45979513845）；此HEAD未见独立连续性专项运行，直接回读六权威blob，绑定一致。状态1.1576.0，图663/483，Matrix222/222、1488来源/276分片，58 OPEN含五P0。重读02、07A、07B与Matrix；S11 segment-0009 §7.3/7.6/7.7 实际复核12支成员、120长生坐标、30纳音对；S14 segment-0001 §7.7 实际复核6旬空对。上述为项目受读语料及既有审计，不宣称新原叶，外部根登记仅在确有对应作用域时引用。未新增外部来源，未做全276分片外部候选去重，不作来源全库无命中断言。全663节点/483边查重，新增20篇页索引和26规则族，26限定ATTESTS；不新增直接抄传/师承关系。

| 边 | 篇页 | 规则族 | 限定 |
|---|---|---|---|
| TG-E0484 | PASSAGE-YUANHAI-CORPUS-CH061-HIDDEN-STEMS | RULE-FAMILY-BAZI-HIDDEN-STEM-MEMBERSHIP | HPA-BAZI-002；FLOW-003/002继承；不证明显示顺序 |
| TG-E0485 | PASSAGE-YUANHAI-CORPUS-CH014-NAYIN | RULE-FAMILY-BAZI-NAYIN-SEXAGENARY-PAIR-IDENTITY | HPA-BAZI-006；FLOW-004/008继承；非紫微定局 |
| TG-E0486 | PASSAGE-YUANHAI-CORPUS-CH047-XUNKONG | RULE-FAMILY-BAZI-XUNKONG-SIX-XUN-VOID-PAIR | HPA-BAZI-007；FLOW-004/009继承；非吉凶与紫微主副旬 |
| TG-E0487 | PASSAGE-YUANHAI-CORPUS-CH015-TWELVE-GROWTH | RULE-FAMILY-BAZI-TEN-STEM-TWELVE-GROWTH | HPA-BAZI-008；FLOW-004/010继承；非旺衰结论、紫微五局或历史时层授权 |
| TG-E0488 | PASSAGE-JIELAN-RECEIVED-CH37-TIANGUAN | RULE-FAMILY-ZIWEI-NATAL-TIANGUAN-STEM-TABLE | HPA-ZMINOR-009；仅天官，不混天福或四柱天官 |
| TG-E0489 | PASSAGE-JIELAN-RECEIVED-CH38-TIANFU | RULE-FAMILY-ZIWEI-NATAL-TIANFU-AUX-STEM-TABLE | HPA-ZMINOR-009；非十四主星天府 |
| TG-E0490 | PASSAGE-JIELAN-RECEIVED-CH39-TIANKONG | RULE-FAMILY-ZIWEI-NATAL-TIANKONG-YEAR-NEXT-PALACE | HPA-ZMINOR-010；非地空 |
| TG-E0491 | PASSAGE-JIELAN-RECEIVED-CH40-XUNKONG | RULE-FAMILY-ZIWEI-NATAL-XUNKONG-VOID-PAIR | HPA-ZMINOR-011；不证明主副旬的现代显示顺序 |
| TG-E0492 | PASSAGE-JIELAN-RECEIVED-CH41-JIEKONG | RULE-FAMILY-ZIWEI-NATAL-JIEKONG-STEM-PAIR | HPA-ZMINOR-012；非六旬空亡 |
| TG-E0493 | PASSAGE-JIELAN-RECEIVED-CH41-JIEKONG | RULE-FAMILY-ZIWEI-NATAL-JIEKONG-ZHENG-PANG | HPA-ZMINOR-012；明确甲己例与既有机械审计限定 |
| TG-E0494 | PASSAGE-JIELAN-RECEIVED-CH43-GUCHEN-GUASU | RULE-FAMILY-ZIWEI-NATAL-GUCHEN-GUASU-YEAR-GROUP | HPA-ZMINOR-013；两输出配对，不推定四柱同名直传 |
| TG-E0495 | PASSAGE-JIELAN-RECEIVED-CH44-JIESHA | RULE-FAMILY-ZIWEI-NATAL-JIESHA-YEAR-TRINE | HPA-ZMINOR-014；杀/煞字形桥，不证明其他时层 |
| TG-E0496 | PASSAGE-JIELAN-RECEIVED-CH45-HUAGAI | RULE-FAMILY-ZIWEI-NATAL-HUAGAI-YEAR-TRINE | HPA-ZMINOR-015；非四柱同名采用证明 |
| TG-E0497 | PASSAGE-JIELAN-RECEIVED-CH46-TAOHUASHA | RULE-FAMILY-ZIWEI-NATAL-TAOHUASHA-XIANCHI-YEAR-TRINE | HPA-ZMINOR-016；保留历史名与现代显示名桥，不认定原题咸池 |
| TG-E0498 | PASSAGE-JIELAN-RECEIVED-CH47-DAHAO | RULE-FAMILY-ZIWEI-NATAL-STANDALONE-DAHAO-YEAR-PAIR | HPA-ZMINOR-017；非岁前/博士同名成员 |
| TG-E0499 | PASSAGE-JIELAN-RECEIVED-CH48-POSUI | RULE-FAMILY-ZIWEI-NATAL-POSUI-YEAR-GROUP | HPA-ZMINOR-018；不外推流年 |
| TG-E0500 | PASSAGE-FULLBOOK-S01-TIANKU-TIANXU | RULE-FAMILY-ZIWEI-NATAL-TIANKU-YEAR-REVERSE | HPA-ZMINOR-001；生年支 |
| TG-E0501 | PASSAGE-FULLBOOK-S01-TIANKU-TIANXU | RULE-FAMILY-ZIWEI-NATAL-TIANXU-YEAR-FORWARD | HPA-ZMINOR-001；生年支 |
| TG-E0502 | PASSAGE-FULLBOOK-S01-HONGLUAN-TIANXI | RULE-FAMILY-ZIWEI-NATAL-HONGLUAN-YEAR-REVERSE | HPA-ZMINOR-002；生年支 |
| TG-E0503 | PASSAGE-FULLBOOK-S01-HONGLUAN-TIANXI | RULE-FAMILY-ZIWEI-NATAL-TIANXI-HONGLUAN-OPPOSITE | HPA-ZMINOR-002；依赖红鸾，不证明其他时层 |
| TG-E0504 | PASSAGE-FULLBOOK-S01-LONGCHI-FENGGE | RULE-FAMILY-ZIWEI-NATAL-LONGCHI-YEAR-FORWARD | HPA-ZMINOR-003；年支 |
| TG-E0505 | PASSAGE-FULLBOOK-S01-LONGCHI-FENGGE | RULE-FAMILY-ZIWEI-NATAL-FENGGE-YEAR-REVERSE | HPA-ZMINOR-003；年支 |
| TG-E0506 | PASSAGE-FULLBOOK-S01-TAIFU-FENGGAO | RULE-FAMILY-ZIWEI-NATAL-TAIFU-HOUR-FORWARD | HPA-ZMINOR-004；出生时支 |
| TG-E0507 | PASSAGE-FULLBOOK-S01-TAIFU-FENGGAO | RULE-FAMILY-ZIWEI-NATAL-FENGGAO-HOUR-FORWARD | HPA-ZMINOR-004；出生时支 |
| TG-E0508 | PASSAGE-FULLBOOK-S01-TIANXING-TIANYAO | RULE-FAMILY-ZIWEI-NATAL-TIANXING-MONTH-FORWARD | HPA-ZMINOR-005；普通月 |
| TG-E0509 | PASSAGE-FULLBOOK-S01-TIANXING-TIANYAO | RULE-FAMILY-ZIWEI-NATAL-TIANYAO-MONTH-FORWARD | HPA-ZMINOR-005；普通月 |

四柱4族均为PROJECT_CORPUS_RECEIVED_TEXT_SCOPED；藏干成员不含排序，纳音名称/五行身份与紫微定局分开，六旬空亡不等于紫微主副旬，十干十二长生不作旺衰断。FLOW-002/003/004/008/009/010依I1导航继承，不为现代投影层增古籍ATTESTS。紫微《捷览》CH37–41/43–48和《全书》受读5组明确为REGISTERED_RECEIVED_TEXT_SCOPED，不把书目身份当作目标原刻核读；双输出拆分（截空配对与次序、天哭天虚、红鸾天喜、龙池凤阁、台辅封诰、天刑天姚），其余受读表保持精确输入。孤辰寡宿为同组配对表；天官天福分章，天福非天府。未裁的本命天月、阴煞、天巫、二德、火铃与魁钺候选不提升。

状态1.1577.0；图709/509，来源/Matrix/风险不变。图/state/ledger/R2/本检查点同一原子提交；台账采用无损紧凑JSON，保留全部旧issues/checkpoints，追加TW-CHECKPOINT-15FF-Q-NATAL-MINOR-BAZI-DERIVED-MAP-20261127；未修改排盘。此次核实图谱节点ID/边ID唯一，所有端点存在；完整CI须提交后核查，不提前宣告成功。NEXT核心辅星CH22/24/25/27与命主身主、庙旺证据及四柱其他机械规则；第三/第四门槛仍待复评。transmission_impact: 46 nodes, 26 evidence-scoped ATTESTS, no direct lineage or runtime change.


## K. 紫微核心辅星、角色与四柱干支关系实际入图（2026-11-27）

基线 a3ea424235c1abb473d9a1ad48e857145f0c2596 / 30cf1e8eef30c2e29ba8c232517e3adf8b87c709，R2六绑定一致；284项Actions分页观察241成功、28排队、15运行，连续性45984787025成功、clean-training-system 45984789425运行中，不作全绿声明。五P0/58风险保持；同对话未变的Matrix/root/manifest继续使用此前核验，变更的graph/state/ledger直接精确blob读取。复读04、05、12OI、12ON、10A/B/C及Matrix，核对辅助星/角色源码关键函数。全图709/509去重；来源均为已登记受读记录与既有审计，不新增外部来源、不宣称新原叶或对276分片做新候选全库查重。所有新增关系仅限定机械或文本范围。

| 边 | 篇页 | 规则族 | 限定 |
|---|---|---|---|
| TG-E0510 | PASSAGE-JIELAN-RECEIVED-CH22-DIPPER-SEQUENCE | RULE-FAMILY-ZIWEI-NATAL-ZUOFU-MONTH-FORWARD | HPA-ZIWEI-021；普通月；复用既有篇页；普通月与生时基础几何，闰月另证 |
| TG-E0511 | PASSAGE-JIELAN-RECEIVED-CH22-DIPPER-SEQUENCE | RULE-FAMILY-ZIWEI-NATAL-YOUBI-MONTH-REVERSE | HPA-ZIWEI-021；普通月；复用既有篇页；普通月与生时基础几何，闰月另证 |
| TG-E0512 | PASSAGE-JIELAN-RECEIVED-CH22-DIPPER-SEQUENCE | RULE-FAMILY-ZIWEI-NATAL-WENCHANG-HOUR-REVERSE | HPA-ZIWEI-021；本命非流昌；复用既有篇页；普通月与生时基础几何，闰月另证 |
| TG-E0513 | PASSAGE-JIELAN-RECEIVED-CH22-DIPPER-SEQUENCE | RULE-FAMILY-ZIWEI-NATAL-WENQU-HOUR-FORWARD | HPA-ZIWEI-021；本命非流曲；复用既有篇页；普通月与生时基础几何，闰月另证 |
| TG-E0514 | PASSAGE-JIELAN-RECEIVED-CH22-DIPPER-SEQUENCE | RULE-FAMILY-ZIWEI-NATAL-DIKONG-HOUR-REVERSE | HPA-ZIWEI-021；非天空；复用既有篇页；普通月与生时基础几何，闰月另证 |
| TG-E0515 | PASSAGE-JIELAN-RECEIVED-CH22-DIPPER-SEQUENCE | RULE-FAMILY-ZIWEI-NATAL-DIJIE-HOUR-FORWARD | HPA-ZIWEI-021；非劫煞；复用既有篇页；普通月与生时基础几何，闰月另证 |
| TG-E0516 | PASSAGE-JIELAN-RECEIVED-CH24-TIANSHANG-TIANSHI | RULE-FAMILY-ZIWEI-NATAL-TIANSHANG-TIANSHI-FIXED-LIFE | HPA-ZIWEI-017；命宫+5/+7；不裁性别交换法；命寅例天伤未天使酉，受读非目标原叶 |
| TG-E0517 | PASSAGE-JIELAN-RECEIVED-CH25-KUIYUE | RULE-FAMILY-ZIWEI-JIELAN-KUIYUE-GENG-XIN | HPA-ZIWEI-015；未选历史候选；非QS庚丑未；庚辛午寅；不以书目充原页 |
| TG-E0518 | PASSAGE-FULLBOOK-RECEIVED-KUIYUE | RULE-FAMILY-ZIWEI-FULLBOOK-KUIYUE-GENG-JIA-WU | HPA-ZIWEI-007；文墨辛干顺序另为兼容差异；Batch04所比收到表；无独立目标原页 |
| TG-E0519 | PASSAGE-JIELAN-RECEIVED-CH27-FIRE-BELL | RULE-FAMILY-ZIWEI-JIELAN-FIRE-BELL-SI-YOU-CHOU-START | HPA-ZIWEI-016；不选历史胜者；巳酉丑子时起火戌铃卯；仅已核差异家族 |
| TG-E0520 | PASSAGE-FULLBOOK-RECEIVED-FIRE-BELL | RULE-FAMILY-ZIWEI-FULLBOOK-FIRE-BELL-SI-YOU-CHOU-START | HPA-ZIWEI-007；文墨兼容不是古法来源；Batch04对照受读巳酉丑火卯铃戌 |
| TG-E0521 | PASSAGE-JIELAN-RECEIVED-CH31-MINGZHU | RULE-FAMILY-ZIWEI-JIELAN-MINGZHU-YEAR-BRANCH | HPA-ZIWEI-022；不等同命宫支；生年十二支为主 |
| TG-E0522 | PASSAGE-FULLBOOK-S01-MINGZHU | RULE-FAMILY-ZIWEI-FULLBOOK-MINGZHU-LIFE-BRANCH | HPA-ZIWEI-012；相同表值不证明同一规则；命宫支查表 |
| TG-E0523 | PASSAGE-JIELAN-RECEIVED-CH32-SHENZHU | RULE-FAMILY-ZIWEI-SHENZHU-ZI-WU-TEXTUAL-COMPOSITE | HPA-ZIWEI-023 SOURCE_INSUFFICIENT；仅证明文本歧义，不证明选择火或铃；子午铃火复合文字，非唯一单星 |
| TG-E0524 | PASSAGE-XINGLI-KAOYUAN-RECEIVED-RELATIONS | RULE-FAMILY-BAZI-BRANCH-SIX-HARMONY-PAIR | HPA-BREL-002；出现不等于成化；既有受读对照与S14，不证明原刻或化成 |
| TG-E0525 | PASSAGE-MINGLI-TANYUAN-RECEIVED-RELATIONS | RULE-FAMILY-BAZI-BRANCH-SIX-CLASH-PAIR | HPA-BREL-003；仅原始关系；后出受读关系章，不借夜子时源ID |
| TG-E0526 | PASSAGE-SANMING-RECEIVED-V2-RELATIONS | RULE-FAMILY-BAZI-BRANCH-CHUAN-HAI-SIX-PAIR | HPA-BREL-004；同几何只计一次；不等于因果直传；受读关系几何；不推定1578目标原页 |
| TG-E0527 | PASSAGE-SANMING-RECEIVED-V2-RELATIONS | RULE-FAMILY-BAZI-BRANCH-COMPLETE-THREE-COMBINATION | HPA-BREL-005；缺一成员不作完整三合；受读关系几何；不推定1578目标原页 |
| TG-E0528 | PASSAGE-SANMING-RECEIVED-V2-RELATIONS | RULE-FAMILY-BAZI-BRANCH-DIRECTED-PUNISHMENT | HPA-BREL-006；无恩/恃势命名异文不裁；受读关系几何；不推定1578目标原页 |
| TG-E0529 | PASSAGE-SANMING-RECEIVED-V1-FOUR-EARTH | RULE-FAMILY-BAZI-BRANCH-FOUR-EARTH-BUREAU | HPA-BREL-007；arity4非三合；不判成局；四成员独立候选 |
| TG-E0530 | PASSAGE-SANMING-RECEIVED-V6-DIRECTIONAL | RULE-FAMILY-BAZI-BRANCH-DIRECTIONAL-TRIADS | HPA-BREL-008；几何同型不等同后世完整解释；四方三支组；后出术语三会 |
| TG-E0531 | PASSAGE-WUXING-JINGJI-RECEIVED-V23-BREAK | RULE-FAMILY-BAZI-BRANCH-EARLY-FOUR-BREAK | HPA-BREL-009；排寅申巳亥；BREL-010后出六破保留；引李虚中书；作品佚文不视原本 |
| TG-E0532 | PASSAGE-SANMING-RECEIVED-V2-ZUOXIA-ZIHUA | RULE-FAMILY-BAZI-SAME-PILLAR-STEM-HIDDEN-COMBINATION | HPA-BREL-012；非成功合化或紫微自化；六组同柱显干藏干关系 |
| TG-E0533 | PASSAGE-FULLBOOK-S01-SHENZHU-ZIWU | RULE-FAMILY-ZIWEI-SHENZHU-ZI-WU-TEXTUAL-COMPOSITE | 仅证子午火铃复合文字；HPA-ZIWEI-023仍SOURCE_INSUFFICIENT |
| TG-E0534 | PASSAGE-MINGLI-TANYUAN-RECEIVED-RELATIONS | RULE-FAMILY-BAZI-SAME-PILLAR-STEM-HIDDEN-COMBINATION | 后出干支暗合语词与同柱机械关系；不推定直接抄传 |

**核心辅星**：CH22复用既有篇页节点，左辅右弼、昌曲、空劫独立，普通月/出生时支，闰月另证。CH24天伤使固定+5/+7，仅固定方法，性别交换候选不裁。CH25庚辛午寅对照受读庚丑未，文墨辛干差异现代兼容；CH27巳酉丑两起位不选胜者。12OI已提供独立未选历史候选API，不能沿用04/05早期缺产品措辞为当前状态。

**命主身主与庙旺**：命主生年支与命宫支为两个查表算子，不因同表值合并。身主子午两受读复合文字仅证明歧义，HPA-ZIWEI-023 SOURCE_INSUFFICIENT；现代默认火不取得史证权。HPA-ZIWEI-018复用PASSAGE-JIELAN-1581-CH69-DIGNITY-PALACE、PASSAGE-JIELAN-1581-CH70-DIGNITY-STAR及RULE-FAMILY-JIELAN-1581-DIGNITY-SOURCE-LEXEMES，E0163/0164/0165。12ON的300格对勘：97同原词、37原文明示等价、54局部极性冲突、21均有见证无直接等价、82 CH69未载、8 CH69文本未决、1 CH70未载。保留紫微午、巨门丑冲突与天机巳缺格；不能用CH69补CH70。HPA-ZIWEI-009现代R4庙旺不继承该表的历史权威。图谱不重复造庙旺节点。12OI/12ON的历史时点产品状态不替代当前Matrix。

**四柱关系**：BREL-001既有NTL五合配对E0431仅证五组配对，不证名义化气元素或合化；新入图BREL-002..009及012只证几何/语词。相穿/害同几何，三刑命名异文保留；四土局与三合不同元数；早四破与后六破不合并；座下自化与紫微自化无直传证据。BREL-010后出六破保持争议，BREL-011现代半合拱合仍现代兼容，BAFF中性透干/同元素显示不伪造古籍规则族。所有既有候选、风险及Matrix状态不变。

状态1.1578.0；新39节点/25限定ATTESTS，累计图748/534。state/graph/ledger/R2/本检查点原子提交；无损紧凑台账保留全部旧issues/checkpoints。节点ID/边ID唯一、端点存在，CI待新HEAD核实。NEXT四柱运限/神煞及第三第四门槛；核心CLOSED。transmission_impact: 39 nodes, 25 evidence-scoped ATTESTS, no direct lineage, no runtime changes.


## L. 四柱运限／神煞机械族逐项导航（2026-11-27，待入图）

基线 29309ddd875d793c82b846ffae1b61b6061e4357 / f926ee7cdc158cb863e3c0c69fe0f0e7459a24e3；R2六绑定与完整树一致，schema 1.1578.0、五P0已复核。精确HEAD连续性 run45985660666 success；分页285项Actions观察284成功、clean-training-system 45985660186运行中，不能宣告全绿。读取完整222行Matrix、全748节点/534边（ID检查入口）、01、03、09B、11B、12NH、12OR、12OV、12MO、S11 segment-0001..0009的目标索引与神煞实现函数入口。S11 segment-0009的CH024..045及054目录行区间已核；目录不是逐字受读文本，更不是原页。以下是既有证据的机械规则导航，不是新原页校勘或新裁决。既有登记来源复用，不新增外部候选、未执行276分片新来源全库查重，不作缺失断言。

### L1. 大运、小运、交运（18行）

| Matrix ID | 机械族 | 当前状态 | 既有证据坐标 | 拆分/入图限定 |
|---|---|---|---|---|
| HPA-DAYUN-001 | Dayun direction by year-stem yin/yang and sex | SUPPORTED_BUT_SCHOOL_SPECIFIC | EXT-CTEXT-SMTHE-SIKU-V2 / 《论大运》 | 年干阴阳与性别为本族输入；日干派不能据异说名义直接确立。 |
| HPA-DAYUN-002 | Jie anchor for Jiaoyun | HISTORICALLY_SUPPORTED | EXT-CTEXT-SMTHE-SIKU-V2 / 《论大运》 | 前/后节；不以中气替代；等号另族。 |
| HPA-DAYUN-003 | Three-days-one-year symbolic-age conversion | HISTORICALLY_SUPPORTED | EXT-CTEXT-WUXING-JINGJI-V33-DAYUN; EXT-CTEXT-SANMING-V2-DAYUN | 三日一岁及十年一辰的符号比例；非UTC绝对时长。 |
| HPA-DAYUN-004 | Dayun Ganzhi sequence from month pillar | HISTORICALLY_SUPPORTED | EXT-CTEXT-QIANLI-MINGGAO-DAYUN lines 242–258; EXT-CTEXT-MINGLI-TANYUAN-DAYUN examples 42–47 | 月柱为序列基，SEQ-001/002拆分；不重复入图。 |
| HPA-DAYUN-005 | Continuous temporal realization of Jiaoyun interval | MODERN_COMPATIBILITY_ONLY | src/fortune_training/bazi_temporal/engine.py _symbolic_age/_jiaoyun_for_seed; profile.py; Batch 11B sources | 现代连续实现，不设古籍ATTESTS。 |
| HPA-DAYUN-006 | Wenzhen China Dayun compatibility realization | MODERN_COMPATIBILITY_ONLY | tests/fixtures/bazi-dayun-wenzhen-compatibility-r1.json authority/capture/model contract | 现代文真兼容，不设古籍ATTESTS。 |
| HPA-DAYUN-007 | Exact-Jie tie handling | MODERN_COMPATIBILITY_ONLY | EXT-CTEXT-WUXING-JINGJI-V33-DAYUN; EXT-CTEXT-SANMING-V2-DAYUN | 严格前后措辞不证明等号；项目FAIL_CLOSED，不设古籍正面等号边。 |
| HPA-XIAOYUN-001 | Hour-pillar start + year yin/yang/sex direction Xiaoyun | DISPUTED_MULTIPLE_CANDIDATES | EXT-CTEXT-SMTHE-SIKU-V2 / 《论小运》; repository S12:SMTH-SEG-01200 and S12:YHZP-USR-S03778 | 醉醒子时柱起，年定顺逆；年龄索引须另证。 |
| HPA-XIAOYUN-002 | Fixed male Bingyin / female Renshen Xiaoyun | DISPUTED_MULTIPLE_CANDIDATES | EXT-CTEXT-SMTHE-SIKU-V2 / 《论小运》; repository S12:SMTH-SEG-01199 | 男丙寅顺女壬申逆；与时柱法并存，非同一算法或直接师承。 |
| HPA-DAYUN-SEQ-001 | First formal Dayun is adjacent to natal month pillar in resolved direction | HISTORICALLY_SUPPORTED | EXT-CTEXT-QIANLI-MINGGAO-DAYUN received text lines 242–258; EXT-CTEXT-MINGLI-TANYUAN-DAYUN | 首正式运相邻月柱；PRE_DAYUN不是第一运。 |
| HPA-DAYUN-SEQ-002 | Subsequent Dayun Ganzhi advance one sexagenary step in the same direction | HISTORICALLY_SUPPORTED | EXT-CTEXT-QIANLI-MINGGAO-DAYUN received text lines 244–258 | 后续每步同方向干支推进。 |
| HPA-DAYUN-CAL-001 | Discrete source-resolution Dayun remainder conversion | HISTORICALLY_SUPPORTED | EXT-CTEXT-WUXING-JINGJI-V33-DAYUN; EXT-CTEXT-SANMING-V2-DAYUN《论大运》 | 整日/时辰粒度360/30/10；不推出微秒精度。 |
| HPA-DAYUN-CAL-002 | Classical lunisolar first Jiaoyun calendarization with small/leap-month correction | MISSING_FROM_PRODUCT | EXT-CTEXT-SANMING-V2-DAYUN《论大运》; S15 LHV-04 | 12OV小月补差与闰月总量校正仅限实例；非法日、重复闰月坐标未决。 |
| HPA-DAYUN-CAL-003 | Later calendar-age years plus remainder-days Jiaoyun method | MISSING_FROM_PRODUCT | 《韋千里命學講義》1934/1936 NLC target leaves; docs/research/QIANLI-MINGXUE-JIANGYI-JIAOYUN-CALENDAR-SEMANTICS-R1.json | 复用韦千里既有篇页/规则节点；140/190为30日名义位置单位，非实际天数。 |
| HPA-DAYUN-CAL-004 | Ten-year Dayun exchange recurrence from first handover | MISSING_FROM_PRODUCT | 《韋千里命學講義》1934/1936 NLC target leaves; docs/research/QIANLI-MINGXUE-JIANGYI-JIAOYUN-CALENDAR-SEMANTICS-R1.json | 复用韦千里节点；明受读十周年与民国同农历坐标须分别记载；异常日期执行仍阻塞。 |
| HPA-DAYUN-CAL-005 | Continuous microsecond x120 absolute-duration Jiaoyun realization | MODERN_COMPATIBILITY_ONLY | src/fortune_training/bazi_temporal/engine.py _symbolic_age/_jiaoyun_for_seed | 现代连续微秒×120，不设古籍ATTESTS。 |
| HPA-DAYUN-CAL-006 | Wenzhen Gregorian month-displacement Jiaoyun realization | MODERN_COMPATIBILITY_ONLY | src/fortune_training/bazi_temporal/engine.py realize_wenzhen_calendar_month_displacement_utc | 现代固定UTC+8公历移月，不设古籍ATTESTS。 |
| HPA-DAYUN-CAL-007 | Proleptic-Gregorian ten-year Dayun boundary anniversaries | MODERN_COMPATIBILITY_ONLY | src/fortune_training/bazi_temporal/profile.py dayun_boundary_rule_set; engine.py _dayun_anniversary | 现代公历周年，不设古籍ATTESTS。 |

三层算子必须分立：选节及实历时距→符号岁数→实际交运历日。小月补差、闰月总量调整与重号月份身份并非同一问题。12OR两件NLC原页（1934 17jh007058/102955；1936 01jh000368/10155）已有 PASSAGE-QIANLI-MINGXUE-JIANGYI-QILI-JIAOYUN 与 RULE-FAMILY-QIANLI-JIAOYUN-NOMINAL-30DAY-LUNISOLAR；后续不再创建等价节点。HKO旧控制137/215实际日与原文140/190名义日不一致，故不套用现代连续加日。三项DAYUN-CAL-002..004保持MISSING_FROM_PRODUCT；全部历法边界与现存遗漏风险不关闭。明代《三命通会》卷二目标受读本不是1578目标原叶；宋《五行精纪》卷三十三为后出受读，不误标宋刻原页。

### L2. 神煞（21行）

| Matrix ID | 机械族 | 当前状态 | 既有证据坐标 | 已审计机械范围／限制 |
|---|---|---|---|---|
| HPA-SHENSHA-001 | 天乙贵人 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00235; S11:YHZP-CH-024 | Simple five-group table matches; anchor candidates are preserved, but Sanming yin/yang/day-night formulations are not yet all productized. Add separate formalized Tianyi school candidates only after each formulation is fully replayable; current simple table remains valid, not universal. |
| HPA-SHENSHA-002 | 天官贵人 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00240; S11:YHZP-CH-025 | Year-stem anchor and branch table match exactly. No reopen. |
| HPA-SHENSHA-003 | 禄神 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00278; S11:YHZP-CH-034 | Ten-stem Lu table matches. No reopen; keep identity separate from fortune judgment. |
| HPA-SHENSHA-004 | 驿马 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00285; S11:YHZP-CH-035 | Branch table matches; year/day/other anchor scope is intentionally preserved as candidates. Keep anchor candidates separate; continue school attribution. |
| HPA-SHENSHA-005 | 华盖 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00296; S11:YHZP-CH-037 | Branch table matches; anchor scope remains candidate-shaped. No winner until source scopes are fully separated. |
| HPA-SHENSHA-006 | 月德 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00255..256; S11:YHZP-CH-028 | Month-group table and ONLY_DAY scope match explicit source wording. No reopen. |
| HPA-SHENSHA-007 | 月德合 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00262; S11:YHZP-CH-029 | Value table matches; source target scope is less explicit, so day-only and all-pillars remain candidates. Preserve both scopes. |
| HPA-SHENSHA-008 | 天德 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00264..265; S11:YHZP-CH-030; EXT:CTEXT-SMTHE-V3-TIANYUEDE | Value table matches. Product now preserves YHZP all-pillars commentary scope and Sanming day-only scope as separate candidates. Keep both; no winner. |
| HPA-SHENSHA-009 | 天厨贵人 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00268; S11:YHZP-USR-S00304; S11:YHZP-CH-031 | Derived table matches source logic; which stem is the operative anchor remains candidate-shaped. Preserve stem-anchor candidates. |
| HPA-SHENSHA-010 | 福星贵人 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00272; S11:YHZP-CH-032 | Target table matches received verse; operative stem anchor remains candidate-shaped. Preserve candidates and continue collation of variant verses. |
| HPA-SHENSHA-011 | 太极贵人 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00243..244; S11:YHZP-CH-026 | Year-stem-only implementation matches explicit source restriction. No reopen. |
| HPA-SHENSHA-012 | 三奇 | SUPPORTED_BUT_SCHOOL_SPECIFIC | S11:YHZP-USR-S00248..251; S11:YHZP-CH-027 | Ordered consecutive-stem base sequence matches; output explicitly marks auxiliary qualification conditions as not arbitrated. Continue formalizing Tianmen/wind-thunder/etc. qualifiers; do not upgrade base sequence to full qualification. |
| HPA-SHENSHA-013 | 天赦 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00293; S11:YHZP-CH-036 | Seasonal Ganzhi table and ONLY_DAY scope match source. No reopen. |
| HPA-SHENSHA-014 | 学堂 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00301; S11:YHZP-CH-014/038 | NaYin-element table matches; year/day NaYin anchor alternatives remain explicit candidates. Trace '生人' anchor genealogy before selecting a default. |
| HPA-SHENSHA-015 | 金舆禄 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00312; S11:YHZP-USR-S00278; S11:YHZP-CH-040 | Derived target branch is correct; source-stem anchor remains candidate-shaped. No winner. |
| HPA-SHENSHA-016 | 暗禄 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00324; S11:YHZP-CH-043; S14:YHZP-CH-007 | Lu-Liuhe derivation matches; anchor ambiguity remains explicit. Retain commentary qualification separately from identity. |
| HPA-SHENSHA-017 | 夹禄 | DISPUTED_MULTIPLE_CANDIDATES | S11:YHZP-USR-S00327; S11:YHZP-CH-044 | Both-neighbour requirement and derivation match; anchor ambiguity remains. No reopen. |
| HPA-SHENSHA-018 | 拱禄 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00315..317; S11:YHZP-CH-041 | Exact four reciprocal Ganzhi cases match source closure. Keep exact finite set; do not generalize. |
| HPA-SHENSHA-019 | 垣城 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00330; S11:YHZP-CH-045; S11:YHZP-CH-015; S11:YHZP-USR-S00285; S14:YHZP-CH-007 | Formula replay matches source example. A stale Twelve-Growth source ref was repaired from CH016 to CH015. Provenance repair only; no algorithm reopen. |
| HPA-SHENSHA-020 | 羊刃 | SUPPORTED_BUT_SCHOOL_SPECIFIC | S11:YHZP-USR-S00282; S11:YHZP-USR-S02740; S11:YHZP-CH-224 | Current five-yang-stem table is a scoped operational family, while the corpus also preserves broader ten-stem blade/Feiren material. Do not collapse yin-stem blade traditions into the current Yangren table; continue school genealogy. |
| HPA-SHENSHA-021 | 飞刃 | HISTORICALLY_SUPPORTED | S11:YHZP-USR-S00378..388 | All-ten-stem Feiren table matches explicit source enumeration. No reopen. |

S11 segment-0009 目录核对：CH024 1167–1205，025 1206–1241，026 1242–1283，027 1284–1328，028 1329–1371，029 1372–1408，030 1409–1440，031 1441–1452，032 1453–1488，034 1524–1569，035 1570–1612，036 1613–1646，037 1647–1691，038 1692–1733，040 1777–1811，041 1812–1825，043 1853–1885，044 1886–1923，045 1924–1967，054 2303–2353。均为项目受读语料编目行号，非版刻叶码。CH224及飞刃具体段落仍须另取正文核实。

历史身份须分为表值、锚点、目标柱、资格条件。天乙五组仅是本族；额外昼夜阴阳方法不伪造。月德ONLY_DAY、月德合双候选、天德渊海全柱/三命日柱分别保存；垣城须日干长生＋日支驿马六合（CH015而非CH016），三奇只证有序基础序列，不证明辅条件成立；拱禄严格四组，不概括为夹禄。羊刃五阳干与飞刃十干不并族。跨紫微同名神煞仅可作比较入口，不能以几何相同确立直接传承。FLOW-005依12MO仅继承来源候选target-match；21个profile、38 source candidates（32单目标/6结构排除）与15项常用显示口径不是同一计数对象；不宣称跨时层古法成立或神煞激活。

### L3. 后续与证据边界

本节给出39个既有Matrix ID的具体入图导航；未新增图节点或关系，未修改六个权威输入、状态版本、风险或R2。下一步在本节坐标上逐族打开已登记受读正文、与图全ID/语义去重，区分宋/明的比例与交运、近代韦氏既有原页、两种小运和各神煞独立锚点，原子发布graph/state/ledger/R2；再依路线逐项复评第三/第四门槛。保持图748/534、Matrix222/222、1488来源/276分片、58 OPEN五P0、核心CLOSED。transmission_impact=NONE（导航检查点）。本轮没有新原页、版本、直传或运行时结论。


## M. 四柱运限受读证据实际入图（2026-11-27）

基线 8e62e60ff8f1b7792da669af7225bba4fa28df9b / c8e4ba9299eb36163153cc43c1ff7928928722ae；20项Actions观察19成功、clean-training-system运行中，未观察到独立连续性专项（文档检查点），回读权威graph/state/ledger及Matrix/root/manifest，六绑定一致，58风险五P0维持。全图748/534及相关中文语义检索无同族节点；韦千里现有E0174及其规则节点复用。

本轮重核[《三命通会》卷二四库受读](https://zh.wikisource.org/zh-hans/三命通會_(四庫全書本)/卷02)第232–233、242、244行，[朱翌《猗觉寮杂记》卷下SK1789](https://www.shidianguji.com/book/SK1789/chapter/1m1e9xkcnzyfd)第411行。前者属现存四库电子受读，与已登记CTEXT入口不计独立物件，不宣称1578原页。15CK《五行精纪》卷33末入口本轮被安全验证阻断，《命理探源》CTEXT入口403；既有登记和审计保留原等级，不称本轮重新核文或新原叶。15CK分片blob 72f00b7e0c8f63c5e35aafaf293b82498575a91a 已核真实内容及manifest；未新增外部来源或宣称全276分片新来源无命中。

| 边 | 篇页 | 规则族 | 限定 |
|---|---|---|---|
| TG-E0535 | PASSAGE-SANMING-RECEIVED-V2-DAYUN | RULE-FAMILY-BAZI-DAYUN-YEAR-SEX-DIRECTION | 阳男阴女顺、阴男阳女逆；甲子阳男例支持年干输入，非唯一历史传统 |
| TG-E0536 | PASSAGE-SANMING-RECEIVED-V2-DAYUN | RULE-FAMILY-BAZI-DAYUN-STRICT-JIE-ANCHOR | 生日后／生日前节气与六节措辞；不证精确等号归属 |
| TG-E0537 | PASSAGE-SANMING-RECEIVED-V2-DAYUN | RULE-FAMILY-BAZI-DAYUN-DISCRETE-SYMBOLIC-AGE | 受读63时例630名义日即1年9月；电子本文字实历过六十三日与下句时数不一致，保留不裁原字；不推微秒插值 |
| TG-E0538 | PASSAGE-WUXING-JINGJI-RECEIVED-V33-DAYUN | RULE-FAMILY-BAZI-DAYUN-DISCRETE-SYMBOLIC-AGE | 既有11B审计支持实历日时折除与三日一岁；不声称新读取宋本 |
| TG-E0539 | PASSAGE-SANMING-RECEIVED-V2-DAYUN | RULE-FAMILY-BAZI-DAYUN-NATAL-MONTH-PILLAR-BASE | 卷二第242行月上起；不以一句话证明完整干支步进 |
| TG-E0540 | PASSAGE-SANMING-RECEIVED-V2-DAYUN | RULE-FAMILY-BAZI-DAYUN-MING-SMALL-MONTH-DEFICIT | 实例进六日；不普遍化为历法适配器 |
| TG-E0541 | PASSAGE-SANMING-RECEIVED-V2-DAYUN | RULE-FAMILY-BAZI-DAYUN-MING-INTERCALARY-COUNT | 实例退一月以足十二月；不裁常月／闰月目标重号选择 |
| TG-E0542 | PASSAGE-SANMING-RECEIVED-V2-DAYUN | RULE-FAMILY-BAZI-DAYUN-MING-TEN-ANNIVERSARY-STATEMENT | 交运后十周年方换一运；不证现代公历周年或异常日处理 |
| TG-E0543 | PASSAGE-SANMING-RECEIVED-V2-XIAOYUN | RULE-FAMILY-BAZI-XIAOYUN-FIXED-SEX-START | 后段明确丙寅／壬申；同页开头丙申保留，非明刻原字裁决 |
| TG-E0544 | PASSAGE-ZHUYI-YIJUELIAO-RECEIVED-V2-XIAOYUN | RULE-FAMILY-BAZI-XIAOYUN-FIXED-SEX-START | 朱翌仅证两个起点，不证每岁一步或方向 |
| TG-E0545 | PASSAGE-WUXING-JINGJI-RECEIVED-V33-XIAOYUN | RULE-FAMILY-BAZI-XIAOYUN-FIXED-SEX-START | 15CK既有受读《烛神经》引文；非独立原书 |
| TG-E0546 | PASSAGE-SANMING-RECEIVED-V2-XIAOYUN | RULE-FAMILY-BAZI-XIAOYUN-FIXED-SEX-DIRECTION-ANNUAL-STEP | 固定法明确男顺女逆；同章年步语句与历史解释不等于现代交界规则 |
| TG-E0547 | PASSAGE-WUXING-JINGJI-RECEIVED-V33-XIAOYUN | RULE-FAMILY-BAZI-XIAOYUN-FIXED-SEX-DIRECTION-ANNUAL-STEP | 15CK引《烛神经》《三命提要》一岁起、每年一位、61岁循环；引书不算独立古本 |
| TG-E0548 | PASSAGE-SANMING-RECEIVED-V2-XIAOYUN | RULE-FAMILY-BAZI-XIAOYUN-HOUR-PILLAR-YEAR-DIRECTION | 阳年阳命甲子时，出生行乙丑、二岁丙寅；逆行类另依年与性别，非现代边界授权 |

机械复算：明受读五日三时＝63时辰，×10＝630名义日＝360＋270＝一岁九月；同电子本另见六十三日措辞，不能当作原刻正确字形。小运固定法一岁男丙寅女壬申，二岁男丁卯女辛未，六十一岁回到起点（15CK既有逐年一位证据）。醉醒子阳年阳命甲子时首运乙丑、二岁丙寅；不是固定起点，也不由此证明具体民用岁界。明小月补差与闰月总量调整分立；闰月目标重号及非法日仍无闭合规则。HPA-DAYUN-CAL-002..004依然MISSING_FROM_PRODUCT。HPA-DAYUN-007精确交节FAIL_CLOSED和现代continuous／文真历法不造古籍ATTESTS。未证明早期全套起运法、直接传承或流派胜者。

新增15节点（5篇页、10规则族）/14限定ATTESTS，累计763/548。全节点/边ID唯一，端点完整；原有图谱对象未覆盖。状态1.1579.0，同一原子提交更新state/graph/ledger/R2/本检查点；58个旧issues与全部旧checkpoints保持；Matrix222/222、1488来源/276分片、核心CLOSED。NEXT 09B两序列子规则与21项神煞正文仍待入图，第三/第四门槛待复评。transmission_impact: 15 nodes/14 scoped ATTESTS, no direct lineage, no runtime change. 新HEAD CI待验证。


## N. 大运正式首运及后续序列：受读复核与待入图检查点（2026-11-27）

基线 b9f4e8979f2e6218c91dd4f2b4d6ee7a5284f0b6 / 86bf4d6ed0544ffac84448612cf6914d9af19bb4。六项R2绑定吻合，连续性45987834927成功；285项Actions分三页核查，初见283成功、12IZ失败、clean-training-system运行中。12IZ的规则、连续性、图谱验证均通过，状态发布环节报Unexpected end of JSON input；45987838876重跑第2次成功。clean-training-system未确认完成。五P0及58项未决均保留。

核对09B、Matrix HPA-DAYUN-SEQ-001/002及root registry EXT-CTEXT-MINGLI-TANYUAN-DAYUN、EXT-CTEXT-QIANLI-MINGGAO-DAYUN。两登记CText入口本轮均403。韦氏CText题名《千里命稿》底本未绑定，不能归为1935《千里命稿》第一集原页；1934/1936《命学讲义》已核交运内容也不自动证明本处列运文字。补充公开电子受读观察 https://www.cafengshuinet.com/m/show_detail.php?id=3251 及 https://libokang.com/classics/bazi/%E5%91%BD%E7%90%86%E6%8E%A2%E6%BA%90/ 与袁氏壬寅逆首辛丑、后庚子己亥相符，并见壬寅顺首癸卯；底本未核、未全库查重，不准入、不计独立物件。

| 待入图规则 | 已有09B受读回放 |
|---|---|
| HPA-DAYUN-SEQ-001 正式首运相邻 | 袁氏壬寅逆辛丑；韦氏受读丙寅顺丁卯、戊寅逆丁丑 |
| HPA-DAYUN-SEQ-002 后续同向一步 | 袁氏辛丑→庚子→己亥；韦氏丁卯→戊辰→己巳／丁丑→丙子→乙亥 |

机械复算（甲子0）：丙寅2→丁卯3→戊辰4→己巳5；戊寅14→丁丑13→丙子12→乙亥11；壬寅38→辛丑37→庚子36→己亥35。正式第n运=(生月index+方向×n) mod 60，n从1起；n=0为交运前生月基点。序列与起运岁数、交运历日、现代时间边界分别验证。明代月上起/一辰十年仅框架，不推直接传承。

待发布图谱计划：PASSAGE-MINGLI-TANYUAN-RECEIVED-DAYUN、PASSAGE-QIANLI-RECEIVED-DAYUN-EXAMPLES，RULE-FAMILY-BAZI-DAYUN-FORMAL-FIRST-ADJACENT、RULE-FAMILY-BAZI-DAYUN-SUBSEQUENT-SEXAGENARY-STEP；两篇页分别指向两规则族的四条限定ATTESTS，证据以09B及已登记受读为限。全图语义核查仅见既有生月基点节点，未见这两条独立序列节点。此前原子提交工具返回h2读取连接错误，重新检查分支仍为b9f4e8979f2e6218c91dd4f2b4d6ee7a5284f0b6，故本检查点只保存实证、计划和阻塞，不声称入图。六权威输入未修改，状态1.1579.0、图763/548、Matrix222/222、来源1488/276分片、58 OPEN五P0、核心CLOSED均保持。NEXT 先安全发布上述序列图谱及R2，再核21神煞和广度第三/第四门槛。transmission_impact=NONE (unpublished proposal).

### N.1 原子发布补记（2026-11-27）

检查点HEAD 015064ed13b88c88c1e3ff31e45069a9131e2aa5，tree 30ac5957a3be1b53a25ce508eca6cc3e9f4eb11e；20项Actions观察19成功、clean-training-system运行中，未见独立连续性专项，故回读权威graph/state/ledger并依R2合同重新生成视图。前轮大文件一次上传h2错误复现于风险台账4.23M字符的缩进序列化；本轮以紧凑JSON 3.71M字符成功生成Blob，旧issues及全部历史checkpoint逐对象一致，仅追加新检查点和更新绑定；排版改变不改变证据。分别生成五个Blob后以单一tree/commit、HEAD lease发布，不逐文件提交。

四条限定关系：TG-E0549/0550 袁氏受读→正式首运相邻／后续同向一步；TG-E0551/0552 韦氏受读→同两规则。均REGISTERED_RECEIVED_TEXT_SCOPED，MEDIUM；非本轮新核原叶，非新物件、非直接传承。保留上节受读访问和作品身份边界。新增4节点/4边，图767/552，状态1.1580.0；Matrix222/222、来源1488/276分片、58未决五P0、核心CLOSED。NEXT 21项四柱神煞正文及机械条件，随后复评广度第三/第四门槛。transmission_impact: 4 nodes/4 scoped ATTESTS, no direct lineage, no runtime change. exact-HEAD CI待验证。


## O. 四柱神煞21项目标正文复核：待入图导航检查点（2026-11-27）

基线 311616654df7045cd8d327dad6d1515afa1f3244，连续性专项45990854134成功；其余Actions尚未全量结束。读S11 index及segment-0009（目录，3ee78ed3178dec1a6244589fe28f777d1b60c053）、segment-0010（正文，671fadc0c31f94ca3d73cd658ac3081bcb3b8974）、segment-0011（正文，8b0a65cab154c56be44293ac49decc63f8cca94d）。实际解析41个目标USR记录（0010内40、0011内S02740），另读CH054及CH224周边记录；层级为CLASSICAL_ORIGINAL/CLASSICAL_COMMENTARY，非可绑定历史原版原叶。Matrix 21项分类：8 HISTORICALLY_SUPPORTED，11 DISPUTED_MULTIPLE_CANDIDATES，2 SUPPORTED_BUT_SCHOOL_SPECIFIC；读Batch03及shensha.py，核查表值和部分目标选择逻辑。全图767节点语义筛查未见上述21族BAZI专属节点；不把紫微同名当同一规则。

| 规则 | S11 USR编号（五位数字前加YHZP-USR-S） | 读后机械证据与限界 |
|---|---|---|
| 001 天乙 | 00235 | 甲戊丑未、乙己子申、丙丁亥酉、庚辛午寅、壬癸卯巳；五组表不证唯一锚点或昼夜阴阳方法 |
| 002 天官 | 00240 | 明说生年干；甲未乙辰丙巳丁酉戊戌己卯庚亥辛申壬寅癸午；乙句受读有异字，不自行修订 |
| 003 禄神 | 00278 | 十干禄表；不将查禄等同有福 |
| 004 驿马 | 00285 | 申子辰寅、寅午戌申、巳酉丑亥、亥卯未巳；锚点仍需分源 |
| 005 华盖 | 00296 | 寅午戌戌、巳酉丑丑、申子辰辰、亥卯未未；不据表值裁年日 |
| 006 月德 | 00255/256 | 四组三合月支对应丙壬甲庚；明限日上 |
| 007 月德合 | 00262 | 对应辛丁己乙；此段未明确目标柱 |
| 008 天德 | 00264/265 | 月定干或支；眉批分年月、日时，保留全柱候选；三命日柱证据按既有审计、待另核目标 |
| 009 天厨 | 00268/304 | 星宫歌诀及食神表；食神禄推导与锚点分别记录，受读星宫术语不等于原刻校勘 |
| 010 福星 | 00272 | 甲/丙等歌诀多目标，丙另戌、丁亥酉；不删多值，锚点未裁 |
| 011 太极 | 00243/244 | 年干明确，戊己四季；不扩成日干法 |
| 012 三奇 | 00248/249/251/252 | 甲戊庚、乙丙丁、壬癸辛；顺序说与另引倒乱说并存；天门/风雷等辅资格原句句法有疑，不强译成布尔条件；运行时仅有序连续三柱基础匹配 |
| 013 天赦 | 00293 | 春戊寅夏甲午秋戊申冬甲子；生日限定，不扫四柱 |
| 014 学堂 | 00301 | 纳音五行对应支及正干支；生人锚点未决 |
| 015 金舆 | 00312/278 | 禄前第二位，甲寅→辰；锚点保留 |
| 016 暗禄 | 00324 | 禄的六合支，甲寅亥乙卯戌；无显禄眉批条件与基本身份分开 |
| 017 夹禄 | 00327 | 禄两邻支同时出现；甲丑卯、乙寅辰 |
| 018 拱禄 | 00315/316/317 | 戊辰丙午、丁巳己未各互见，明限四个有向例；不作泛化夹拱 |
| 019 垣城 | 00330/285 | 甲辰日亥时，甲长生亥、辰驿马寅、寅亥合；历史身份不等同判断；依赖长生及六合表后续核对 |
| 020 羊刃 | 00282/02740/00379..00389 | 00282仅为禄刃关系眉批，不能单独证明五阳干表；02740举丙戊午、壬子及日刃；CH054列十干刃和飞刃；运行时五阳干体系仅作已审流派限定，不把十干文本倒裁为五干 |
| 021 飞刃 | 00378..00388 | 明列十干刃与对宫飞刃，对应酉戌子丑子丑卯辰午未；与五阳干羊刃表独立 |

说明：上述USR数字均为既有五位编号，如00235对应YHZP-USR-S00235，02740对应YHZP-USR-S02740；不是原书叶码。三奇引文另有倒乱说和天门/风雷措辞不明，属于既有HPA-SHENSHA-012辅助条件未裁、羊刃属既有020流派边界，不新增或关闭历史裁决。天乙多套方法、天德三命正文、学堂锚点、垣城依赖及三奇资格按现有未决范围保留。下一步：将上述已读篇页与独立机械规则族、范围限定及已有候选对应入图；不要把所有21族一次概括为无争议或将匹配等同成格。无新增来源、图节点、边、算法或风险状态，六项权威输入与R2不变；状态1.1580.0、图767/552、Matrix222/222、来源1488、58 OPEN五P0、核心CLOSED。transmission_impact=NONE（正文导航检查点，待原子入图）。


## P. 四柱神煞篇页—规则图谱原子发布（2026-11-27）

基线 3014af1e9f92f57e6dd7bd32b489392c5cf1fc6f / a9d4e214b3b64e22824fcdeedd515eef0a215166；20项Actions见19成功、clean-training-system运行中，故回读graph/state/ledger、Matrix、root registry与extension manifest；六绑定吻合，五P0维持。O节正文记录复用。本轮另复查已登记EXT:CTEXT-SMTHE-V3-TIANYUEDE，CText入口403；[维基文库四库受读卷三](https://zh.wikisource.org/zh-hans/三命通會_(四庫全書本)/卷03)第177、193–196、285行成功读取，同属四库受读层，不计独立原版或新来源。不得把引书当独立实物。下列图谱仅见证文本存在及有界规则，不等同历史普遍性或运行时授权。

要点：天乙阴阳贵冬夏至分与寅申昼夜分另立，庚的牛羊与马虎归属差异不静默改表；三奇天/地归类、顺逆及得体得地有异，原语料顺序说并非唯一；天月德日上及不犯时位刑冲为吉格条件，不能凭此证明全部识别口径；壶中子逐月辰法另立；三命羊刃篇列阴阳木火金水刃位，土未逐干单列，仅旁证十干传统；渊海全十干表与五阳干运行时子集明确隔离。所有原页、边界与流派归属未决照旧。

| 边 | 篇页 | 规则族 | 证据界限 |
|---|---|---|---|
| TG-E0553 | PASSAGE-YUANHAI-CORPUS-CH024-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-TIANYI-FIVE-GROUP-TABLE | HPA-SHENSHA-001；S11 USR 00235；五组表；庚辛午寅；不证锚点、阴阳或昼夜唯一法 |
| TG-E0554 | PASSAGE-YUANHAI-CORPUS-CH025-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-TIANGUAN-YEAR-STEM | HPA-SHENSHA-002；S11 USR 00240；明限生年干；乙句异字待校；非贵格授权 |
| TG-E0555 | PASSAGE-YUANHAI-CORPUS-CH034-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-LU-TEN-STEM-BRANCH | HPA-SHENSHA-003；S11 USR 00278；十干禄位，不等于福禄判断 |
| TG-E0556 | PASSAGE-YUANHAI-CORPUS-CH035-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-YIMA-TRINE-BRANCH-TABLE | HPA-SHENSHA-004；S11 USR 00285；表值明确；年日或其他锚点不裁 |
| TG-E0557 | PASSAGE-YUANHAI-CORPUS-CH037-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-HUAGAI-TRINE-TOMB-TABLE | HPA-SHENSHA-005；S11 USR 00296；四组三合对应墓支；锚点不裁 |
| TG-E0558 | PASSAGE-YUANHAI-CORPUS-CH028-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-YUEDE-MONTH-DAY-STEM | HPA-SHENSHA-006；S11 USR 00255/00256；三合月组对应干；受读明确日上 |
| TG-E0559 | PASSAGE-YUANHAI-CORPUS-CH029-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-YUEDEHE-MONTH-TARGET-TABLE | HPA-SHENSHA-007；S11 USR 00262；月德合四组；此段未限定目标柱 |
| TG-E0560 | PASSAGE-YUANHAI-CORPUS-CH030-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-TIANDE-MONTH-MIXED-TARGET-YUANHAI | HPA-SHENSHA-008；S11 USR 00264/00265；干支混合目标；眉批年月日时分论；不据此排除日柱限制传统 |
| TG-E0561 | PASSAGE-YUANHAI-CORPUS-CH031-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-TIANCHU-FOOD-GOD-LU | HPA-SHENSHA-009；S11 USR 00268/00304；歌诀和食神表相参；星宫词待校，锚点不裁 |
| TG-E0562 | PASSAGE-YUANHAI-CORPUS-CH032-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-FUXING-MULTI-TARGET-TABLE | HPA-SHENSHA-010；S11 USR 00272；保留甲丙等多值；锚点不裁 |
| TG-E0563 | PASSAGE-YUANHAI-CORPUS-CH026-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-TAIJI-YEAR-STEM | HPA-SHENSHA-011；S11 USR 00243/00244；明限生年，非他干；戊己四季 |
| TG-E0564 | PASSAGE-YUANHAI-CORPUS-CH027-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-SANQI-YUANHAI-BASE-SEQUENCES | HPA-SHENSHA-012；S11 USR 00248/00249/00251/00252；有序三干基础；另引倒乱说；天门风雷辅资格未裁，不证完整成格 |
| TG-E0565 | PASSAGE-YUANHAI-CORPUS-CH036-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-TIANSHE-SEASON-DAY-GANZHI | HPA-SHENSHA-013；S11 USR 00293；四季四干支；生日限定 |
| TG-E0566 | PASSAGE-YUANHAI-CORPUS-CH038-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-XUETANG-NAYIN-BRANCH-EXACT | HPA-SHENSHA-014；S11 USR 00301；生人锚点待裁；普通支与正干支区分 |
| TG-E0567 | PASSAGE-YUANHAI-CORPUS-CH040-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-JINYU-LU-FORWARD-TWO | HPA-SHENSHA-015；S11 USR 00312/00278；甲禄寅取辰；不裁干锚点 |
| TG-E0568 | PASSAGE-YUANHAI-CORPUS-CH043-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-ANLU-LU-LIUHE | HPA-SHENSHA-016；S11 USR 00324；例甲亥乙戌；无显禄眉批资格独立 |
| TG-E0569 | PASSAGE-YUANHAI-CORPUS-CH044-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-JIALU-LU-TWO-NEIGHBOURS | HPA-SHENSHA-017；S11 USR 00327；两邻同时；甲丑卯乙寅辰；锚点不裁 |
| TG-E0570 | PASSAGE-YUANHAI-CORPUS-CH041-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-GONGLU-FOUR-DIRECTED-CASES | HPA-SHENSHA-018；S11 USR 00315/00316/00317；两组互见四有向例，明确不泛化 |
| TG-E0571 | PASSAGE-YUANHAI-CORPUS-CH045-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-YUANCHENG-GROWTH-YIMA-LIUHE | HPA-SHENSHA-019；S11 USR 00330/00285；甲辰日亥时例；长生及六合依赖；不证判断 |
| TG-E0572 | PASSAGE-YUANHAI-CORPUS-CH054-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-YANGREN-TEN-STEM-BLADE-TABLE | HPA-SHENSHA-020；S11 USR 00379..00389；阴阳十干明确列举；不等同五阳干运行时体系 |
| TG-E0573 | PASSAGE-YUANHAI-CORPUS-CH054-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-FEIREN-TEN-STEM-OPPOSITE | HPA-SHENSHA-021；S11 USR 00378..00388；全十干明列；对宫；不以五阳干羊刃覆盖 |
| TG-E0574 | PASSAGE-YUANHAI-CORPUS-CH054-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-YANGREN-FIVE-YANG-SUBSET | 仅直接支持甲卯丙午戊午庚酉壬子五个值，不证明仅五阳干 |
| TG-E0575 | PASSAGE-YUANHAI-CORPUS-CH224-SHENSHA | RULE-FAMILY-BAZI-SHENSHA-YANGREN-FIVE-YANG-SUBSET | 眉批举丙戊午、壬子，部分值旁证，不证明五干排他 |
| TG-E0576 | PASSAGE-SANMING-RECEIVED-V3-TIANYI | RULE-FAMILY-BAZI-SHENSHA-TIANYI-SOLSTICE-YIN-YANG | 卷三引通玄经：先后天坤起贵、冬夏至区分；非昼夜，不登记完整运行表 |
| TG-E0577 | PASSAGE-SANMING-RECEIVED-V3-TIANYI | RULE-FAMILY-BAZI-SHENSHA-TIANYI-DAY-NIGHT-YIN-SHEN | 卷三另载寅申起昼夜；不裁昼夜边界、不等同冬夏至 |
| TG-E0578 | PASSAGE-SANMING-RECEIVED-V3-TIANYUEDE | RULE-FAMILY-BAZI-SHENSHA-TIANDE-SANMING-DAY-QUALIFICATION | 卷三引阎东叟：日上见且时位不犯克冲刑破为吉；身份与完整吉格分离 |
| TG-E0579 | PASSAGE-SANMING-RECEIVED-V3-TIANYUEDE | RULE-FAMILY-BAZI-SHENSHA-TIANYUEDE-HUZHONGZI-MONTH-STEP | 正月天德亥、月德未，各逐月顺行；引书不是独立实物；不激活 |
| TG-E0580 | PASSAGE-SANMING-RECEIVED-V3-SANQI | RULE-FAMILY-BAZI-SHENSHA-SANQI-SANMING-CLASSIFICATION-QUALIFIERS | 不同天/地分类、顺逆、日夜及地支条件并存；非全部机械化 |
| TG-E0581 | PASSAGE-SANMING-RECEIVED-V3-YANGREN | RULE-FAMILY-BAZI-SHENSHA-YANGREN-TEN-STEM-BLADE-TABLE | 285行列阴阳木火金水刃位及禄前一辰原理；戊己土未逐干单列，不宣称全十干表二次核实 |

25篇页+27规则族＝52节点，29条限定ATTESTS；图819/581，状态1.1581.0。Matrix222/222（21项神煞8支持、11争议、2特定流派）；来源1488/276分片、58 OPEN五P0、核心CLOSED。历史风险旧对象及checkpoint逐对象保留；未增来源、未裁候选、未作运行时修改。NEXT 对照双史纲、覆盖图册、图谱和风险台账复评广度第三/第四门槛。transmission_impact: 52 nodes/29 scoped ATTESTS, no direct lineage, no runtime change. exact-HEAD CI待验证。


## Q. 广度第三／第四门槛实测复评（2026-11-27，非终验）

基线 HEAD `f38e018bc30701b845aaf00ffd83e1e3c8325f44` / tree `7ada2174f3302ec2b1866c8ed07cf7603441f565`。精确HEAD Actions 285项分100/100/85三页全部成功，连续性专项[45992468344](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45992468344)成功。R2六个绑定与真实docs tree吻合；常规state fetch_file空正文，依已通过的R2快路径恢复，不将空文当作权威正文。额外直接解析真实graph、Matrix、ledger blob及双史纲、覆盖图册、15FF-P/Q正文。相关开放PR #364 为独立历法政策审计，不合并。

### Q1. 第三门槛：版本与规则源流骨架

按图谱node_type∈{RULE_FAMILY,MECHANICAL_RULE}及**精确**system_scope=ZIWEI或BAZI筛选，检查from为PASSAGE、to为该规则、relation为ATTESTS或TRANSMITS_RULE的有向边；不把其他历史历法、旧细分scope、跨术式或现代结构节点硬归入两个分母。

| 对象 | 紫微 | 四柱 |
|---|---:|---:|
| Matrix独立规则ID（史纲逐ID实际字面定位） | 114/114 | 94/94 |
| 明确system_scope的图谱规则节点 | 78 | 60 |
| 具有上述篇页关系的规则节点 | 78/78 | 60/60 |
| 对应篇页节点（各术内去重） | 48 | 49 |
| 篇页→规则关系 | 80 ATTESTS | 67 ATTESTS + 2 TRANSMITS_RULE |

共享/组合14条在覆盖图册逐ID定位，三文件222/222无缺失；不要求每条Matrix恰好有一规则节点。全图819节点及581边ID唯一、0悬空端点；全部scope的PASSAGE→规则 ATTESTS有157边、143目标，合入TRANSMITS_RULE为184边、159目标。两条仅有TRANSMITS_RULE而无ATTESTS的明确四柱族为RULE-FAMILY-BAZI-TEN-GOD-RELATIONAL-IDENTITY和RULE-FAMILY-BAZI-FIVE-STEM-COMBINATION-PAIR-IDENTITY（NTL-9900014379篇页）；不据筛选误报缺链。上述149条明确两术边均有evidence和scope_note。图谱现有87 explicit_non_edges、1 lineage_hypothesis；不把513 CONFIRMED关系自动解释为直接师承。

15FF-P的24个模块索引及G1导航，与A–P实际篇页回填合读；第三门槛**核心规则骨架结构具备**（由15FF-P的部分符合推进），但这是导航与限定关系实测，不是每个规则版本—物件—数字替身—篇页完整链均获原刻验证。历史受读、现代流派表、古代原页分层；14/18星及朝鲜紫微数分别保留。尚须确认作品及版本链未证目标均有后续入口；不以关系数量证实传承。来源不足、现代兼容、候选及未形式化状态一律不升级。

### Q2. 第四门槛：现有风险可恢复与深研入口缺口

逐项解析58个风险：55 OPEN、3 BLOCKED_SOURCE_ACCESS（0001/0002/0003）；5 P0、53 P1。全部58项有evidence_boundary、missing_evidence、next_action、closure_criteria，最新checkpoint.reviewed_issue_ids全部覆盖；未验证每个风险原页。四条MISSING_FROM_PRODUCT准确绑定HPA-ZDATE-006→0006、HPA-DAYUN-CAL-002→0008、003→0010、004→0011。五P0保持原状态和下一动作。

额外检查所有11条SOURCE_INSUFFICIENT：目前无逐ID matrix_rule_ids风险绑定（不违反现有四条MISSING_FROM_PRODUCT强制门禁，亦非新发现历史异文）。保留Matrix既有原始状态，不能把导航空白当作无史料；给后续深研显式索引如下，避免11条重复立项：

| 范围 | 既有Matrix ID | 深研边界 |
|---|---|---|
| 两个父级汇总 | HPA-ZIWEI-008、HPA-ZIWEI-011 | 子项已拆，不另造统一历史祖本；随子项核查 |
| 藏干序位一组 | HPA-BAZI-015、HPA-BHIDDEN-002 | 来源文字顺序、软件显示顺序、主中余气/强度语义分立；不把ordinal解释为强度 |
| 子午神主火铃 | HPA-ZIWEI-023 | 火铃复合措辞；需版本限定异文及机械定义，保持fail-closed |
| 本命月德/天德 | HPA-ZMINOR-022、HPA-ZMINOR-027 | 《神峰通考》跨术同形不能证明紫微本命采用；流年另立 |
| 天巫、天月、阴煞 | HPA-ZMINOR-024、HPA-ZMINOR-025、HPA-ZMINOR-026 | 分别追月表、十二值与六宫循环，历法同名/现代软件不是前现代紫微证据 |
| 将前环 | HPA-ZIWEI-026 | 现代中州整环与《捷览》局部年支证据；本命与流年独立 |

该表是已有缺口索引，不新增或关闭历史风险，不把两个父级重复计为独立问题。另27 DISPUTED_MULTIPLE_CANDIDATES、25 SUPPORTED_BUT_SCHOOL_SPECIFIC、50 MODERN_COMPATIBILITY_ONLY、104 HISTORICALLY_SUPPORTED、1 NOT_YET_FORMALIZED及4 MISSING_FROM_PRODUCT保持现状。第四门槛**现有台账结构与强制交叉索引符合，非穷尽性仍明确**；下一步将上述既有不足项按语义检查旧风险关联，并为真实独立深研问题建立有界入口，避免重复父项；同时对双纲15FF-P旧时点提示追加当前版本说明。之后再做四门槛整体验收决定，而非在本检查点宣告阶段二启动。任何版本原页、直接师承、早期传播或未证争议均不因广度验收自动关闭。

本轮仅结构复评及既有缺口导航，无新增源、原页、历史裁决、图谱边、风险状态或排盘改变；六权威输入与R2不变，保持state 1.1581.0、Matrix222/222、1488来源/276分片、图819/581、58未决五P0、核心CLOSED。transmission_impact=NONE。新文档HEAD Actions待验。
