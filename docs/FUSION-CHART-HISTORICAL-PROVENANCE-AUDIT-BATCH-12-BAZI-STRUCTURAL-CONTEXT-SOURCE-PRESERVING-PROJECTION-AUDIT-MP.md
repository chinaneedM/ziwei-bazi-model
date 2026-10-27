# Fusion Chart Historical Provenance Audit R1 — Batch 12MP

## 八字 Structural Context：中性结构组合与历史候选防火墙

Status: **HPA-BAZI-FLOW-006 AUDITED AS MODERN_COMPATIBILITY_ONLY / SHARED PRIMITIVES REUSED / HISTORICAL RELATION SIDECAR NOT PROMOTED**

本批审计 `BAZI-STRUCTURAL-CONTEXT-R1@1.1.0` 与 `BAZI-TARGET-FLOW-STRUCTURAL-PROJECTION-R1`。结论不是“古籍存在这一统一 Structural Context 对象”，而是：现代软件把已经分别审计过的藏干、十神、透干、亲和与 raw-relation core 以中性方式组合到活动时限层。

### 1. 历史权威归属

组合层本身判为 `MODERN_COMPATIBILITY_ONLY`。历史依据继续分别归属于：

- HPA-BAZI-002：藏干 membership；
- HPA-BAZI-003：十神 identity mapping；
- HPA-BAZI-004 / HPA-BAFF-002：中性 stem/branch affinity；
- HPA-BAZI-013：exact hidden-stem exposure；
- HPA-BAZI-005：released raw relation core 及其单独保存的历史候选边界。

12MP 不把这些来源合成一个“古典结构论体系”。

### 2. 层级边界

当前 Structural Context 只 materialize `DAYUN / ANNUAL / MONTHLY`。目标 flow 处于 `PRE_DAYUN` 时不制造 Dayun stem/branch participant。Projection 明确列出 `XIAOYUN / DAILY / HOURLY` 为 excluded layers；本批不以“软件以后可能支持”为理由提前扩张历史或运行时范围。

### 3. 共享 primitive 与身份

Temporal hidden stems 直接复用共享 `generate_hidden_stems`；所有 temporal visible/hidden stems 的十神继续以**本命日主**为唯一锚点。Exposure、affinity 与 raw relation 都复用现有 generator，参与者采用 frame-bound instance ID，因此相同干支字符出现在不同 frame 也不折叠为一个 occurrence。

Projection 保留 Structural FactHash/ComputationHash、source Flow lineage、rule-set/version/source refs 与 relation participant layers。

### 4. HPA-BAZI-005 候选防火墙

HPA-BAZI-005 仍为 `DISPUTED_MULTIPLE_CANDIDATES`。当前 Structural Context 使用 released production raw core；`BAZI-HISTORICAL-RELATION-CANDIDATES-R1` 中的四土局、方/三会、早期四破、同柱干支暗合候选继续是 `PRESERVED_NOT_SELECTED` sidecar。

12MP **不**把 sidecar 自动注入 Structural Context，不把它与 raw core 合并，也不利用结构层替这些历史候选选赢家。若未来需要动态历史候选结构投影，必须另建 source-scoped/versioned contract。

### 5. 语义防火墙

`nominal_transformation_element` 只是 registry metadata。禁止从本层推出：

- 合化成功；
- 通根强弱或 root grade；
- relation priority / suppression / cancellation / rescue；
- 旺衰、格局、用神、忌神、调候；
- 神煞意义、事件或预测。

运行时源码不修改；`TRANSMISSION_IMPACT=NONE`。

Matrix 保持 201 rows，audited rows 174→**175**；missing-product 仍 10，provenance defects **17/17**，chart algorithm defects / reopens / candidate collapses **0**。

下一门 **12MQ**：HPA-BAZI-FLOW-007 Structural Support candidate projection，重点审计 support evidence 候选不得被升级成 ROOT/NO_ROOT、强弱、权重、评分、排序或 winner。

研究记录：`docs/research/BAZI-STRUCTURAL-CONTEXT-SOURCE-PRESERVING-PROJECTION-AUDIT-R1.json`。重放摘要：`docs/research/evidence/batch-12mp/projection-replay.json`。
