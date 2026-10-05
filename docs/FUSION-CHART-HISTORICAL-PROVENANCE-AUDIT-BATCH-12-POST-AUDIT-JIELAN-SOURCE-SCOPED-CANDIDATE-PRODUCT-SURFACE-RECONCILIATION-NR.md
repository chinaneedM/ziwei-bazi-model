# Fusion Chart Historical Provenance Audit R1 — Batch 12NR

## Post-audit reconciliation — Jielan 1581 source-scoped candidate product surfaces

Status: **THREE MISSING_FROM_PRODUCT STATUSES CONFIRMED / INTERNAL RUNTIME ≠ PRODUCT SURFACE / NO NEW PROVENANCE DEFECT / NO ALGORITHM REOPEN**

本批复核：

- `HPA-ZIWEI-015` — 1581 Jielan Kui/Yue Geng-stem variant；
- `HPA-ZIWEI-016` — 1581 Jielan Fire/Bell 巳酉丑 starting-branch variant；
- `HPA-ZIWEI-022` — 1581 Jielan Mingzhu birth-year-branch basis。

三行都已经有 source-scoped deterministic runtime，但仍标记 `MISSING_FROM_PRODUCT`。12NR 的任务是确认这个 product gap 是否仍然真实。

### 1. Internal runtime 已存在

`src/fortune_training/ziwei_chart/historical_candidates.py` 已冻结：

- registry: `ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATES-R1@1.1.0`；
- selection: `PRESERVED_NOT_SELECTED`；
- runtime resolver: `ZIWEI-JIELAN-1581-SOURCE-SCOPED-CANDIDATE-RUNTIME-R1@1.0.0`。

`resolve_jielan_1581_source_scoped_candidate(...)` 会确定性生成 source-bound facts，其中包括：

- Kui/Yue；
- Fire/Bell start branches + birth-hour advancement；
- Mingzhu，且 basis 明确为 `ZIWEI_BIRTH_YEAR_BRANCH`；
- source refs；
- registry/runtime identity；
- candidate hash。

Focused tests 验证 resolver deterministic、fail-closed，且不把候选变成 production winner。

### 2. 但它没有进入产品 profile/API

当前 `fortune_training.ziwei_chart.__init__` 没有导出：

- `resolve_jielan_1581_source_scoped_candidate`；
- Jielan historical registry；
- Jielan runtime resolver identity。

相比之下，后来产品化的 temporal historical candidates 已通过包根导出相应 API/registry/runtime IDs。这说明 Jielan natal/source-scoped resolver 仍停留在内部模块层。

Combined local app 固定使用：

`build_production_ziwei_profile(self.registry)`

并没有：

- `ziwei_calculation_profile_id` request selector；
- Jielan candidate-profile ID；
- historical candidate-profile selector。

`/api/profiles` 只报告当前解析的 Ziwei calculation profile，并没有候选方法列表。

### 3. Workbench 也没有候选 selector

Workbench 只显示既有联合盘和 profile/rule lineage。当前 workbench/local assets 没有：

- Jielan registry/resolver identity；
- Kui/Yue historical candidate selector；
- Fire/Bell historical candidate selector；
- Mingzhu basis candidate selector。

因此“内部 resolver 可调用”不能视为“用户可审计地选择/查看一个产品候选 profile”。

### 4. 三行分别裁决

#### HPA-ZIWEI-015 Kui/Yue

1581 `庚辛逢马虎，午寅二宫` 的 Jielan family 已 source-bound runtime 化，但没有 candidate-profile API/UI lineage。

**MISSING_FROM_PRODUCT 保留。**

#### HPA-ZIWEI-016 Fire/Bell

Jielan `巳酉丑 火戌/铃卯` start family 与 birth-hour advancement 已 deterministic runtime 化，但没有与 current production family 并列的产品候选入口。

**MISSING_FROM_PRODUCT 保留。**

#### HPA-ZIWEI-022 Mingzhu

Jielan birth-year-branch basis 已确定性 materialize；production 仍是 Life-palace-branch basis。两种 basis 没有被错误合并，但 Jielan basis 仍未进入 candidate-profile API/UI lineage。

**MISSING_FROM_PRODUCT 保留。**

### 5. 本批没有新 provenance defect

三行原先的 `current_implementation_match` 已经正确指出：

`SOURCE_SCOPED_RUNTIME_CANDIDATE_EXISTS_BUT_USER_SELECTABLE_PRODUCT_PROFILE_NOT_YET_WIRED`

12NR 只是用当前 package root、local API 和 Workbench 再确认这一点，没有发现旧 Matrix 状态已经过时。

因此：

- provenance defects 保持 **36/36**；
- current missing rows 保持 **10**；
- chart algorithm defects / reopens / candidate collapses 保持 **0**；
- production default 不变；
- candidate selection 不变。

`batch_classification=POST_AUDIT_RECONCILIATION_NOT_SUPPLEMENTAL_RULE_AUDIT`。

`transmission_impact=NONE`。

下一门：**12NS — HPA-ZIWEI-014 competing Four-Transformation tables + HPA-ZIWEI-018 Jielan historical dignity table**。

Research record: `docs/research/ZIWEI-JIELAN-SOURCE-SCOPED-CANDIDATE-PRODUCT-SURFACE-RECONCILIATION-R1.json`.  
Evidence: `docs/research/evidence/batch-12nr/ziwei-jielan-source-scoped-candidate-product-surface-reconciliation.json`.
