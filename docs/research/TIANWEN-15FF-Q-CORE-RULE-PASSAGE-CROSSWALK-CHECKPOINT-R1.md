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
