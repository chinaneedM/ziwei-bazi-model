# Fusion Chart Historical Provenance Audit R1 — Batch 12MX

## R6 气数位：逆数第九坐标、河洛术语与现代语义封装

Status: **R6 DECOMPOSED / MODERN HELUO COORDINATE SUPPORTED / PREMODERN ORIGIN OPEN / NO ALGORITHM REOPEN**

`HPA-STRUCT-006` 的 inventory 初始标签为 `HISTORICALLY_SUPPORTED`，但原文、年代、版本和流派栏均待审，也未进入 audited IDs。本批保留整行旧快照，将 R6 总体裁决为现代组合，并拆为 `HPA-STRUCT-015` 坐标规则与 `HPA-STRUCT-016` 工程语义规则。没有发现排盘坐标错误，不触发算法重开。

### 1. “逆数第九”与当前 +4 坐标完全同一

现代河洛四化 received text 明确给出：以本宫为 1，逆数到第 9 宫为“气数位”；命宫例为官禄宫，财帛宫例为命宫，并概括为各宫自己的官禄宫。S04 河洛来源原子亦保存同一结构：命宫逆数九位为官禄宫；十二宫皆可为本宫；某宫立为本宫后，其官禄宫就是该宫气数位。

训诂必须区分三个层面：

1. **本宫**是论事时旋转的局部参照宫，不固定等于本命命宫。
2. **官禄宫**在此是相对 `CAREER` 角色；命宫作为本宫时才与本命官禄宫重合。
3. **逆数第九**采用“本宫为 1”的含首计数，所以实际移动八格。功能宫顺序逆时针排列，而 runtime 的物理 Address index 顺时针递增，因此 `-8 mod 12 = +4`。这正是 R2 ordinal 9 / R6 clockwise offset 4。

独立命名宫表回放全部 **12 个命宫物理旋转 × 12 个本宫＝144 个气数位坐标**，目标宫名、源/目标物理索引、ordinal 9 与 offset 4 全部一致。该回放是几何枚举，不冒充 144 个历法本命盘；现有 R2/R6 端到端测试继续承担真实链路覆盖。

因此 `HPA-STRUCT-015=SUPPORTED_BUT_SCHOOL_SPECIFIC`：当前坐标得到现代河洛/四化 received witness 支持，但不能扩张为所有紫微流派的共同术语，更不能在没有实物/版本证据时倒推为明清旧法。

### 2. 年代与传承边界

Google Books 的《紫微斗数精成》记录绑定大德山人与風車文化出版社，并转录作者说明：该书以 1998 年玉林办班教材等材料为基础。这只能说明现代作品的自述材料背景，**不能**把 1998 当成“气数位”规则首次形成时间。公开 page 366 可直接核对河洛四化“气数位分析论断法”，但上传日期、网页发布日期与书籍版本日期严格分离。

另一条《河洛派紫微斗数同步断诀》公开传录把“命一、疾六、一六共宗、官九、气数位”连写，并把同步断诀归于司徒阳。本批只把它当现代河洛 received corroboration；网页转录既不是第一方出版物，也不足以证明“发明者”或师承边。

截至本批，没有取得可把“气数位”术语或完整逆九定义直接锁到前现代实物版的证据；最早定义、具体印次、作者/师承与直接文本承袭继续开放。多份现代网页重复同文不按“独立古证”计票。

### 3. S04“现实承接”不是历史原文

这里必须把坐标与语义拆开。所审现代河洛文本会进一步谈成败、气运、生气、吉凶，并以气数位宫干四化作判断；而当前 S04/R6 刻意收缩为“现实承接”，并固定禁止“见禄=成功”“见忌=失败”“受冲=离婚或破产”等单信号终点化。

所以十二条 `fixed_support_meaning`、NATAL-only、mapping ID、R2 hash 绑定、integrity/fail-closed 与结果语义防火墙都属于 **现代工程合同**，并非本批所见历史文本的逐字继承。对应 `HPA-STRUCT-016=MODERN_COMPATIBILITY_ONLY`。

这项裁决提高历史严谨度：外部来源只认证它真正能认证的“逆九/相对官禄”坐标，不借其权威替 S04 的现代中性化设计背书。

### 4. 账本、传承图与下一门

Matrix **214→216 rows、195→198 audited、10 missing-product rows**；来源缺陷仍 **18/18**，排盘算法缺陷、算法重开、候选折叠仍为 **0**。R6 源码、S04 runtime/canonical 字节与 R6 说明文档全部冻结不改。

本批没有新增可证明的实体古本、首次年代、作者/师承或直接传抄边，故 `TRANSMISSION_IMPACT=NONE`，不向传承图虚增边。外部现代 witness 只登记为流派/文本范围证据。

下一门 **12MY：R7 一六共宗**。将继续把“相对第六坐标”与河洛解释分开，并做 12×12 命名宫回放；R4 最早定义/印次、12MV 三环来源缺口以及本批 R6 前现代起源/具体版本缺口全部保留。

研究记录：`docs/research/ZIWEI-R6-QISHU-SOURCE-PHILOLOGY-SCOPE-AUDIT-R1.json`。  
回放记录：`docs/research/evidence/batch-12mx/r6-qishu-geometry-replay.json`。

外部来源：Google Books《紫微斗数精成》书目/前言上下文、FlipHTML5 received page 366，以及公开《河洛派紫微斗数同步断诀论命法》传录。它们均按现代 received/bibliographic witness 使用，不替代未取得的历史实物版权威。
