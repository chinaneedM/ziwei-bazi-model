# Fusion Chart Historical Provenance Audit R1 — Batch 12NB

## R2 relative-palace frame：现代旋转坐标层审计

Status: **MODERN COMPUTATIONAL FRAME / 1728 ROTATIONAL REPLAY ROWS CLOSED / PROV-DEFECT-020 REPAIRED / NO ALGORITHM REOPEN**

本批审计 `HPA-STRUCT-002`。R2 不是一条独立古法，而是把已经审计过的十二宫 designation 顺序围绕任一本宫旋转，生成一个可供 R3–R8 调用的相对宫位坐标层。

### 1. 上游历史事实与现代抽象必须分开

`HPA-ZIWEI-003` 已在 Batch 06 以 received《全书》文本闭合十二宫顺序：

`命、兄弟、妻妾/夫妻、子女、财帛、疾厄、迁移、奴仆、官禄、田宅、福德、父母`。

R2 直接复用这个冻结顺序，但“把每个本宫临时设为 relative ordinal 1，并将同一套 12 个 role 顺序循环旋转”是现代软件坐标抽象。它不声称古籍记载了 144 行 RelativePalaceRoleFact，也不把 hash/schema/integrity 倒写成传统术法。

因此 `HPA-STRUCT-002` 保持 `MODERN_COMPATIBILITY_ONLY`。

### 2. 机械公式

对任一 origin designation index `i` 与 relative role offset `j`：

`target_designation_index = (i + j) mod 12`  
`relative_ordinal = j + 1`  
`clockwise_offset = (-j) mod 12`

目标物理地址不由 R2 自创，而必须等于 V1 natal designation binding；同时该 source→target 物理边必须存在于已审 R1 的 144-fact 中性 Z12 topology。

### 3. 1728 条全旋转回放

单个本命盘的 R2 状态包含 **12 origins × 12 ordinals = 144 facts**。本批再把命宫可能落在 12 个物理地址的情况全部枚举：

**12 LIFE rotations × 12 origins × 12 ordinals = 1728 rows**。

独立 oracle 对每一行重算 origin/target designation、physical address、relative role/ordinal 与 clockwise offset；1728 行全部与当前 R2 公式一致。

### 4. 命名传统语义继续 fail-closed

R2 profile 强制 `semantic_rule_set_id/version=None`。本层不激活三方四正、对宫、气数位、一六共宗、邻宫/夹宫、借星、吉凶、评分、事件或终点语义。这些名称必须由已经审计的后续 source-scoped 层单独绑定，不能从 ordinal 数字自动推出。

### 5. PROV-DEFECT-020

本批发现 Matrix Markdown 顶部的 **current audit ledger** 仍写“18 confirmed provenance metadata defects”，而机器 Matrix JSON 与 State 在 12MZ/PROV-DEFECT-019 后已是 **19/19**。这不是历史快照，而是当前总览，所以确认：

`PROV-DEFECT-020=CURRENT_AUDIT_MATRIX_MD_PROVENANCE_DEFECT_COUNT_STALE_AFTER_12MZ`

修复方式只更新当前总览和权威计数，历史批次快照保持原样。修复后 provenance defects **19→20 confirmed / 19→20 repaired**。排盘算法、候选、运行时与历史规则结论均不变。

### 6. 工程合同与账本

R2 schema、FactHash/ComputationHash、canonical projection、V1/R1 profile binding、cross-chart fail-closed 与 tamper rejection 均属于现代工程合同。没有发现 implementation mismatch；R2 runtime/schema/hash/V1/R1 字节全部冻结不改。

Matrix rows 保持 **220**；audited **205→206**；missing-product rows 仍为 **10**。Provenance defects **20/20**；chart algorithm defects / reopens / candidate collapses 均为 **0**。

R2 完成后，Structural R1–R8 当前 Matrix 行全部进入 audited IDs。

下一门 **12NC：HPA-TIME-001 Civil timezone/TZDB instant resolution**。该门将审计现代时区数据库权威、历史中国时区适用范围与可重复性边界，继续禁止把现代 TZDB 规则伪装成古代历法规则。

研究记录：`docs/research/ZIWEI-R2-RELATIVE-PALACE-FRAME-AUDIT-R1.json`。  
回放记录：`docs/research/evidence/batch-12nb/r2-relative-palace-frame-replay.json`。
