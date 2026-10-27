# Fusion Chart Historical Provenance Audit R1 — Batch 12NS

## Post-audit reconciliation — Four-Transformation and Jielan dignity product boundaries

Status: **TWO MISSING_FROM_PRODUCT STATUSES CONFIRMED / PARTIAL INTERNAL SOURCE COVERAGE DISTINGUISHED / PROV-DEFECT-037 + 038 REPAIRED / NO ALGORITHM REOPEN**

本批复核：

- `HPA-ZIWEI-014` — competing Four-Transformation table families；
- `HPA-ZIWEI-018` — 1581 Jielan historical dignity table。

目标不是新增算法，而是把“已有内部来源覆盖”与“完整、可选择的产品候选族”严格分开。

### 1. HPA-ZIWEI-014：已有 Jielan 来源身份，不等于竞争表族已产品化

当前 production 仍只激活：

`S08_CURRENT_40_ASSIGNMENT_R1`

但 `src/fortune_training/ziwei_chart/historical_candidates.py` 已经保存：

- `ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATES-R1@1.1.0`；
- `PRESERVED_NOT_SELECTED`；
- `ZIWEI-JIELAN-1581-SOURCE-SCOPED-CANDIDATE-RUNTIME-R1@1.0.0`；
- `EXT-ZIWEI-JIELAN-1581:CH23` 的十干四化表。

现有回归测试还明确断言：

`JIELAN_1581_FOUR_TRANSFORMATIONS == current S08 target table`

因此，Jielan 1581 已经是一个 source-scoped historical identity/runtime fact，但它在目标表内容上与当前 S08 相同。它不能被拿来证明“竞争表族已经全部产品化”。

真正仍缺的是：

- received `《紫微斗数全书》` 的完整、版本绑定竞争表；
- Zhongzhou/其他流派的完整、来源绑定竞争表；
- whole-table candidate profile，而不是逐格拼接；
- public/local API 的表族选择 lineage；
- Workbench 可审计选择面。

现有 `四化激活来源 / 生成谱系` Workbench 只读展示当前 `/api/resolve` 已发布 activation，不重算、不选择规则。

所以 **HPA-ZIWEI-014 继续 MISSING_FROM_PRODUCT**。

### 2. PROV-DEFECT-037

旧 Matrix 写法概括成：

> alternate historical/school tables are known but not selectable runtime profiles

这会遗漏一个重要事实：Jielan 1581 完整十干表已经进入内部 historical registry/resolver，只是其目标与 S08 相同，而且没有形成“竞争表族选择面”。

本批 forward-only 修复为：

- 已存在：Jielan source-scoped、PRESERVED_NOT_SELECTED、target-identical-to-S08；
- 仍缺：真正 divergent 的 received-Fullbook/Zhongzhou complete candidates + selectable profile lineage。

没有 runtime/candidate-selection/default 改动。

### 3. HPA-ZIWEI-018：来源表状态已进入 runtime，但 normalized dignity table 仍不存在

同一 Jielan registry `1.1.0` 已保存：

- `EXT-ZIWEI-JIELAN-1581:CH69`；
- `EXT-ZIWEI-JIELAN-1581:CH70`；
- `SOURCE_TABLE_PRESENT_NORMALIZATION_PENDING`。

source-scoped resolver 会返回 dignity 状态，同时明确：

`runtime_normalized=false`

也就是说，系统知道“1581 来源表存在且尚未规范化”，但没有把歧义词强行压成现代七级 `庙/旺/得/利/平/不/陷` 单元。

当前 production 继续使用独立的：

`OPERATIONAL-ZIWEI-DIGNITY-R4@4.0.0`

现有 `庙旺注解来源 / 权威边界` Workbench 也只是只读展示 production annotation provenance，不是历史 dignity candidate selector。

所以 **HPA-ZIWEI-018 继续 MISSING_FROM_PRODUCT**。

### 4. PROV-DEFECT-038

HPA-ZIWEI-018 的旧 `current_profile` 仍写：

`ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATES-R1@1.0.0`

而 live registry 已经是 `1.1.0`。此前 PROV-DEFECT-004 只修到了 HPA-ZIWEI-015/016，没有覆盖 018。

本批只修 provenance/profile identity：

- registry -> `1.1.0`；
- 绑定现有 source-scoped resolver；
- 保留 `SOURCE_TABLE_PRESENT_NORMALIZATION_PENDING`；
- 保留 `runtime_normalized=false`。

没有新增任何 dignity cell，也没有把 production R4 追认成 1581 历史表。

### 5. Accounting / firewall

- Matrix rows: **220**
- audited: **220**
- current `MISSING_FROM_PRODUCT`: **10**
- provenance metadata defects: **38 confirmed / 38 repaired**
- chart algorithm defects: **0**
- algorithm reopens: **0**
- candidate collapses: **0**

`batch_classification=POST_AUDIT_RECONCILIATION_NOT_SUPPLEMENTAL_RULE_AUDIT`

`transmission_impact=NONE`

No runtime/schema/hash/rule/candidate-selection/production-default change.

下一门：**12NT — HPA-ZDATE-006 Nanyangtang Fullbook ten-ke Zi/Hai split natal birth-hour candidate product/runtime reconciliation**。

Research record: `docs/research/ZIWEI-FOUR-TRANSFORMATION-DIGNITY-PRODUCT-BOUNDARY-RECONCILIATION-R1.json`.  
Evidence: `docs/research/evidence/batch-12ns/ziwei-four-transformation-dignity-product-boundary-reconciliation.json`.
