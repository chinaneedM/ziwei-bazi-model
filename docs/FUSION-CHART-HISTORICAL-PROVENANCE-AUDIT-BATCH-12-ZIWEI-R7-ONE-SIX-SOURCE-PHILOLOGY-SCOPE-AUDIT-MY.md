# Fusion Chart Historical Provenance Audit R1 — Batch 12MY

## R7 一六共宗：河图古词、现代紫微相对第六位与工程中性化

Status: **R7 DECOMPOSED / PREMODERN HETU TERM ATTESTED / MODERN ZIWEI COORDINATE SUPPORTED / NO ALGORITHM REOPEN**

`HPA-STRUCT-007` 初始 inventory 把“一六共宗”术语、紫微宫位投影和 R7 软件封装写在同一行。本批保留旧行完整快照，拆为 `HPA-STRUCT-017`（现代河洛紫微的相对第六宫坐标）和 `HPA-STRUCT-018`（现代工程中性化/identity closure）。父规则改记为现代组合。没有发现坐标错误，不触发算法重开。

### 1. “一六共宗”词组早于本批能证明的紫微用法

公开 received text《青囊经》有“一六共宗、二七同道、三八为朋、四九为友、五十同途”，上下文明示河图阴阳生成数。公开《阳宅正宗》卷上也把同一组数对解释为河图：北一六水、南二七火、东三八木、西四九金、中五十土。

这两条只能证明 **一六共宗作为河图/术数数理词组存在于前现代传承文本**。它们没有紫微十二宫、命宫→疾厄宫、太极换宫或十二对映射，因此不能用来证明 R7 的紫微宫位算法同样古老。作品形成、具体版本、物理字形和文本层年代继续分别处理，不以网页年代替代版刻年代。

### 2. 紫微 R7 的直接坐标证据属于现代河洛资料

公开 received 《紫微斗数精成》第十四章明确写出：以命宫为“一”，逆时钟数至疾厄宫为“六”；太极点改变后，一个命盘可组成十二对“一六”关系，并逐一列出命疾、兄迁、夫奴、子官、财田、疾福、迁父、奴命、官兄、田夫、福子、父财。另一现代《河洛派同步断诀》传录也重复“命一、疾六、一六共宗”。

这足以支持 `HPA-STRUCT-017=SUPPORTED_BUT_SCHOOL_SPECIFIC` 的机械范围，但只在现代河洛/四化紫微资料范围内成立；不宣称所有紫微流派共同采用这一术语，也不把古河图数对直接等同为古紫微宫位规则。

### 3. 训诂与坐标桥接

必须分开四件事：

1. **一**：是当前论事本宫/局部太极点，不永久固定为本命命宫。
2. **六**：采用“本宫为 1”的含首计数，所以实际移动五个功能宫位。
3. 紫微功能宫顺序按逆时针推移，而 runtime 的物理 `Address.index` 顺时针递增，因此 `-5 mod 12 = +7`。
4. 所以 R7 的机械身份是 `relative_ordinal=6`、`relative_role_designation_id=HEALTH`、`clockwise_offset=7`。

独立命名宫表回放全部 **12 个命宫物理旋转 × 12 个本宫＝144 个一六坐标**，宫名配对、源/目标物理索引、ordinal 6 与 offset 7 全部一致。该回放是几何枚举；现有 R2/R7 端到端测试继续承担真实本命链路覆盖。

### 4. “同视”“一荣俱荣”等不是 R7 的软件语义

现代紫微 received text常继续解释一宫与六宫“同视”、荣损同步，甚至导出更强的冲宫吉凶规则。当前 R7 **没有**承载这些判断：它只输出 `DIRECTED_RELATIVE_SIXTH_PALACE_IDENTITY_ONLY`，并冻结 `direct_event_permission=False`、`direct_endpoint_permission=False`。

因此方向性 identity、NATAL-only、R2 hash 绑定、schema/integrity 与禁止直接事件/终点判断均属于现代工程合同，记为 `HPA-STRUCT-018=MODERN_COMPATIBILITY_ONLY`。这不是在否定流派解释，而是防止来源只证明“有这个关系”时，软件擅自升级为强弱、同吉凶、事件或终点结论。

### 5. 账本与下一门

Matrix **216→218 rows、198→201 audited、10 missing-product rows**；来源缺陷仍 **18/18**，排盘算法缺陷、算法重开、候选折叠仍为 **0**。R7 源码、R7 说明、S04 runtime 字节全部冻结不改。

本批没有取得能证明“青囊/阳宅河图词组 → 现代河洛紫微宫位算法”的直接承袭链，因此 `TRANSMISSION_IMPACT=NONE`。古词组见证与现代紫微 received witness 分层登记，不用相似措辞制造师承边。

下一门 **12MZ：HPA-STRUCT-008 R8 太极点 / 主题宫组合**。继续检查 R8 是否只是 R2/R6/R7 等结构的现代组合，还是包含需单独审计的历史/流派语义；同时保留 R4/R6/R7 的最早定义、具体印次与直接承袭缺口。

研究记录：`docs/research/ZIWEI-R7-ONE-SIX-SOURCE-PHILOLOGY-SCOPE-AUDIT-R1.json`。  
回放记录：`docs/research/evidence/batch-12my/r7-one-six-geometry-replay.json`。
