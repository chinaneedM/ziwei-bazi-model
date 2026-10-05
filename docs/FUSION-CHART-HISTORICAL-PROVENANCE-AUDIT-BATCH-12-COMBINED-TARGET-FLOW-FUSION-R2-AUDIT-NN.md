# Fusion Chart Historical Provenance Audit R1 — Batch 12NN

## HPA-COMB-006 Combined Target Flow Fusion R2

Status: **MODERN COMPATIBILITY ONLY / COMPOSITION-ONLY SCOPE CONFIRMED / PROVENANCE REPAIRED / NO ALGORITHM REOPEN**

本批审计 `HPA-COMB-006`：Combined Target Flow Fusion R2 是否只是把已发布的目标时点对象绑定到同一 lineage，还是在 Combined 层重新解释了紫微、八字的时限规则。

### 1. R2 的输入都是上游已发布对象

`CombinedTargetFlowFusionR2Service` 先调用 R1 `CombinedTargetFlowService.resolve_with_bundles(...)`，取得 base combined、BaZi target-flow 与 R1 target-flow；随后从同一 `TargetTemporalInput` 重放 target coordinate，并要求 R1 与 BaZi 的 target fact/computation hash、profile ID/version 与重放结果完全一致。

紫微侧不是由 R2 重新排盘，而是调用已经发布的 `SharedZiweiSelectorProjectionService`。该 selector 必须通过 structural integrity 和 full replay，且它的 source target-coordinate hashes 必须与同一 target resolution 相同。

因此 R2 的职责是 **identity binding + replay verification**，不是新的历法、宫位或星曜算法。

### 2. RESOLVED 不是命理裁决

R2 的 `_expected_status(...)` 仅在以下条件全部成立时返回 `RESOLVED`：

- target coordinate status = `RESOLVED`；
- BaZi target-flow status = `RESOLVED`；
- Ziwei selector status = `RESOLVED`；
- Ziwei selector candidate count = 1。

否则返回 `UNCERTAINTY_PRESENT`。

DST fold 回归明确让 target 与 BaZi 保留多候选，并让 R2 返回 `UNCERTAINTY_PRESENT`。因此这个 status 只表示软件组合面的候选/边界状态，不表示某种命理方法已被证明正确，也不授权选出 winner。

### 3. Hash lineage 绑定上游事实，不复制上游语义

R2 的 `source_fact_hash` 绑定：

- base combined manifest；
- R1 target-flow bundle；
- target-coordinate fact hash；
- BaZi target-flow source fact hash；
- Ziwei selector fact hash。

`view_hash` 绑定 renderer-neutral target input、三个上游状态、BaZi view hash 与 Ziwei selector candidate count。

`bundle_hash` 再绑定 target-coordinate computation/profile、BaZi target-flow bundle、Ziwei selector computation hash 与 R2 algorithm identity。

因此后续加入 selector projection 的 source-scoped historical candidates 会经 selector hashes 被 R2 **传递绑定**，但 R2 不会把这些候选重新解释为自己的历史规则。

### 4. Full replay 防止自洽伪造

focused regression 会把 `ziwei_selector_fact_hash` 改成格式合法的新值，再重算 R2 自身 source/view/bundle hash 和 local integrity；虽然局部结构检查仍可 PASS，full replay 重新执行整个 service 后会以 `COMBINED_TARGET_FLOW_FUSION_R2_FULL_REPLAY_MISMATCH` 拒绝。

这说明 R2 的可信度来自“上游对象可重放”，而不是“本地哈希自洽即可”。

### 5. R1 与浏览器边界

R2 是 additive：回归测试确认调用 R2 前后的 R1 dataclass、JSON、source fact hash、view hash 与 bundle hash 完全不变。

Workbench R2 panel 只调用 `/api/resolve-flow-fusion-r2` 并显示状态/hash；浏览器资产明确不包含 `BaziTimeResolver`、`TargetTemporalCoordinateFoundation`、`ZiweiTemporalEngine`、`SharedZiweiSelectorProjectionService`、`candidates[0]` 等重算/静默首候选逻辑。

### 6. PROV-DEFECT-033

Matrix 原先：

- `primary_source=composition-only`；
- `source_quote=PENDING_VERBATIM_EXTRACTION`；
- `source_quote_location` 仅指向 `docs/COMBINED-TARGET-FLOW-FUSION-R2.md`。

这不足以作为当前审计后的 provenance 绑定。实际 contract 还依赖 live composer、local endpoint、Workbench read-only boundary、DST uncertainty、R1 immutability 与 full-replay tamper regressions。

确认：

`PROV-DEFECT-033=HPA_COMB_006_PENDING_SOURCE_QUOTE_AND_DOC_ONLY_PROVENANCE_UNDERDESCRIBED_LIVE_R2_CONTRACT`

修复为直接采用 R2 Purpose 中的原始软件合同句：

> R2 adds the already-released SharedZiweiSelectorProjectionService to that same target-coordinate lineage. It does not introduce a new placement rule.

并扩展 provenance location 到实现与 focused tests。没有修改 runtime、schema、hash algorithm、status rule、候选或任何子系统计算。

### 7. 裁决

`HPA-COMB-006=MODERN_COMPATIBILITY_ONLY`。

Matrix rows **220**；audited **217→218**；missing-product rows **10**。Provenance defects **32→33 confirmed / 32→33 repaired**。Chart algorithm defects / reopens / candidate collapses 均为 **0**。

`transmission_impact=NONE`：R2 是现代软件组合层，没有新增历史文本—人物—流派传承边。

下一门：**12NO — HPA-COMB-007 Resolved profile/rule/algorithm lineage**。

研究记录：`docs/research/COMBINED-TARGET-FLOW-FUSION-R2-AUDIT-R1.json`。  
审计证据：`docs/research/evidence/batch-12nn/combined-target-flow-fusion-r2.json`。
