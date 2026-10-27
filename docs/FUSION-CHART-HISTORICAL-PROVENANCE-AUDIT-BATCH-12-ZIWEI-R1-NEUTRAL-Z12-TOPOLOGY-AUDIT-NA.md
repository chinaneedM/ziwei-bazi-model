# Fusion Chart Historical Provenance Audit R1 — Batch 12NA

## R1 neutral Z12 topology：现代坐标底座审计

Status: **MODERN COMPUTATIONAL SUBSTRATE / 144 TOPOLOGY FACTS CLOSED / NO HISTORICAL DOCTRINE CLAIM / NO ALGORITHM REOPEN**

本批审计 `HPA-STRUCT-001`。R1 的设计目的就是在任何传统结构名义出现之前，建立一个完整、可验证、可哈希的十二地址循环关系空间。因此本批不寻找“古籍是否记载 144 矩阵”来替现代数据结构背书，也不把数学同构关系倒写成传统术语。

### 1. 审计对象

`NEUTRAL-Z12-TOPOLOGY@1.0.0` 只定义：

- 12 个 canonical Address，index 0..11 对应子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥；
- 每个 source 到每个 target 的有序关系；
- `clockwise_offset = (target.index - source.index) mod 12`；
- source-major / target-minor 的 canonical 顺序。

因此恰有 **12×12 = 144** 个 `AddressOffsetFact`。自关系 offset=0；+6 具有纯几何二次回返性质，但 R1 不把它命名为“对宫”；其它 offset 同样不被命名为三方、四正、邻宫、气数位或一六共宗。

### 2. 为什么是 MODERN_COMPATIBILITY_ONLY

R1 并不是一条需要追溯到某部古籍的命理规则，而是现代软件的**中性坐标层**。它明确禁用 `semantic_rule_set_id/version`，并 fail-closed 拒绝把未冻结传统语义绑定进来。

传统紫微当然存在十二地支宫位、对宫、三合、夹宫等概念，但 R1 不声明这些语义的历史来源，也不以“传统上有十二宫”推导 144 有序对矩阵、哈希层、schema 或完整性校验是古法。后续 R2–R8 再按各自来源把局部语义投影到这个中性底座。

因此 `HPA-STRUCT-001` 保持 `MODERN_COMPATIBILITY_ONLY`，此次只是由 inventory 状态进入正式 audited 状态，不拆新历史子规则。

### 3. 独立回放与不变量

独立 oracle 对子至亥的 12 个地址枚举全部 144 个 source/target 有序对，并重新计算模 12 offset。回放与 runtime contract 一致，并保留以下边界：

- 144 个 pair 全部唯一；
- 每个 source 覆盖 12 个 target；
- 每个 target 在全域被覆盖；
- offset 始终在 0..11；
- `shift(source, offset)` 回到 target；
- `shift(shift(source, offset), -offset)` 回到 source；
- +6 的二次 shift 回到 source，但不附传统名称。

现有 R1 测试还继续覆盖 schema、determinism、input-order-independent FactHash projection、upstream Natal hash binding 与 profile/version fail-closed。

### 4. 来源与历史边界

本批的“来源”是**当前仓库发布合同与代码实现**，不是历史古籍：

- `src/fortune_training/ziwei_structural/topology.py`
- `src/fortune_training/ziwei_structural/profile.py`
- `docs/ZIWEI-STRUCTURAL-RUNTIME-V2-R1.md`
- `schemas/ziwei-structural-state-v2-r1.schema.json`

没有新增历史文本 witness、作者/师承或传抄边，因此 `TRANSMISSION_IMPACT=NONE`。

### 5. 账本与下一门

Matrix rows 保持 **220**；audited **204→205**；missing-product rows 仍为 **10**。Provenance defects 保持 **19/19**；chart algorithm defects / reopens / candidate collapses 均为 **0**。R1 runtime、schema、hash algorithm 与 V1 natal release 全部冻结不改。

下一门 **12NB：HPA-STRUCT-002 R2 relative-palace frame**。重点审计“冻结十二宫 designation 顺序围绕任一本宫旋转”为现代坐标投影，继续禁止在 R2 层偷渡三方四正、对宫、气数位、一六共宗等命名语义。

研究记录：`docs/research/ZIWEI-R1-NEUTRAL-Z12-TOPOLOGY-AUDIT-R1.json`。  
回放记录：`docs/research/evidence/batch-12na/r1-neutral-z12-topology-replay.json`。
