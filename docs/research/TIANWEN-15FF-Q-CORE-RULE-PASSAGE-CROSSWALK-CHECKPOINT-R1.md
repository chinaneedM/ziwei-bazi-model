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
