# Fusion Chart Historical Provenance Audit R1 — Batch 12NU

## Post-audit reconciliation — Dayun historical-calendar candidates and product surfaces

Status: **THREE MISSING_FROM_PRODUCT STATUSES CONFIRMED / PROV-DEFECT-039 REPAIRED / NO ALGORITHM REOPEN**

本批复核：

- `HPA-DAYUN-CAL-002` — 明代阴阳历首交运日期、小月/闰月修正；
- `HPA-DAYUN-CAL-003` — 《千里命稿》整岁推进 + 余日法；
- `HPA-DAYUN-CAL-004` — 首交运之后按同一历制十年递推。

### 1. 合同存在，不等于大运 runtime 已接入

仓库已有 `HISTORICAL-CHINESE-CALENDAR-ADAPTER-CONTRACT-R1`，其 live registry 当前仅有：

- `MING-DATONG-CALENDAR-CONTEXT-R1`
- `QING-SHIXIAN-1645-CALENDAR-CONTEXT-R1`

合同定义：

- `MAP_CIVIL_DATE_TO_HISTORICAL_LUNISOLAR`
- `REALIZE_DAYUN_HANDOVER`
- `ADD_CALENDAR_YEARS`

并且 `FailClosedHistoricalCalendarAdapter` 在历法算术未认证时只返回：

`UNRESOLVED_NO_CERTIFIED_HISTORICAL_CALENDAR_ADAPTER`

同时禁止现代中国历法作为古历权威、禁止跨历制回投、禁止古法候选隐式使用 Gregorian anniversary。

但 `BaziTemporalEngine` 当前**完全没有导入 historical_calendar**。这意味着合同是未来实现的 source/regime firewall，不是现有 Dayun engine 的执行分支。

### 2. HPA-DAYUN-CAL-002

这条存在真实的部分基础设施：

- Ming Datong regime descriptor 已注册；
- fail-closed adapter 已存在；
- 1578 / 1569 的大量 source replay、月首 oracle 与物理页考据已建立。

仍然缺：

- 可认证、可泛化的 Ming historical-calendar arithmetic adapter；
- 与 `BaziTemporalEngine` 的显式接线；
- historical Bazi temporal profile；
- API / Workbench 产品选择面。

因此继续 `MISSING_FROM_PRODUCT`。

### 3. HPA-DAYUN-CAL-003 与 PROV-DEFECT-039

旧 Matrix 写：

> ADAPTER_CONTRACT_PRESERVES_UNRESOLVED_REGIME_WITHOUT_FALLBACK

这个表述过度。

当前 `_REGIMES` 只有明大统、清时宪，并没有 Republican/Qianli descriptor。合同的 operation/schema **可以容纳未来新增的后期历制 context**，但不能把“可容纳”写成“已经保存了该 regime”。

所以本批 forward-only 修复为：

- 《千里命稿》方法当前是 Matrix/source candidate；
- live historical-calendar registry **没有** Qianli/Republican regime；
- live Bazi temporal runtime **没有** Qianli historical profile；
- 在 exact calendar coordinate、invalid-date、recurrence semantics 没关闭之前，不得借明大统、时宪、现代中国历或问真兼容算法替代。

此项记为 **PROV-DEFECT-039**，只修 provenance 描述，不改算法。

### 4. HPA-DAYUN-CAL-004

合同层确实已经定义 `ADD_CALENDAR_YEARS`，也禁止 classical candidate 隐式使用 Gregorian anniversary。

但 released engine 的 `_dayun_anniversary()` 目前只有：

- continuous: `PROLEPTIC_GREGORIAN_10Y_UTC_ANNIVERSARY`
- Wenzhen: `PROLEPTIC_GREGORIAN_10Y_CHINA_STANDARD_ANNIVERSARY`

没有 historical-calendar recurrence branch。

所以“十年一换”概念有历史支持，但其实际历制实现继续 `MISSING_FROM_PRODUCT`，并必须继承同一个已认证首交运 regime，不能中途换 Gregorian 或另一个历史历制。

### 5. 当前 MISSING_FROM_PRODUCT 复核阶段完成

12NQ / 12NR / 12NS / 12NT / 12NU 之后，当前全部 **10 条** `MISSING_FROM_PRODUCT` 都已做 live runtime/product-surface reconciliation。

这并不意味着 Historical Audit 结束。当前 Matrix 仍有：

- 30 `DISPUTED_MULTIPLE_CANDIDATES`
- 11 `SOURCE_INSUFFICIENT`
- 1 `NOT_YET_FORMALIZED`

下一阶段应重新按 evidence risk / source accessibility / algorithm impact 排序，而不是因为产品缺口复核结束就强选历史赢家。

### 6. Accounting / firewall

- Matrix rows: **220**
- audited: **220**
- current `MISSING_FROM_PRODUCT`: **10**
- provenance metadata defects: **39 confirmed / 39 repaired**
- chart algorithm defects: **0**
- algorithm reopens: **0**
- candidate collapses: **0**

`batch_classification=POST_AUDIT_RECONCILIATION_NOT_SUPPLEMENTAL_RULE_AUDIT`

`transmission_impact=NONE`

No runtime/schema/hash/rule/candidate-selection/production-default change.

下一门：**12NV — unresolved historical status prioritization and evidence-closure planning**。

Research record: `docs/research/BAZI-DAYUN-HISTORICAL-CALENDAR-CANDIDATE-PRODUCT-SURFACE-RECONCILIATION-R1.json`.  
Evidence: `docs/research/evidence/batch-12nu/bazi-dayun-historical-calendar-candidate-product-surface-reconciliation.json`.
