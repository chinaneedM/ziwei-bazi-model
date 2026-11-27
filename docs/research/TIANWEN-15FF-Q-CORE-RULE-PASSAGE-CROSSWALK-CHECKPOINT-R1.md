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
