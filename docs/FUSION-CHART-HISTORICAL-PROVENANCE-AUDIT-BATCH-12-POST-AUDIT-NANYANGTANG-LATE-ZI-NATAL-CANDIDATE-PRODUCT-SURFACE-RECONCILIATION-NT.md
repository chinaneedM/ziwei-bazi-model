# Fusion Chart Historical Provenance Audit R1 — Batch 12NT

## Post-audit reconciliation — Nanyangtang late-Zi natal candidate product surface

Status: **MISSING_FROM_PRODUCT CONFIRMED / SOURCE EVIDENCE ≠ RUNTIME CANDIDATE / NO NEW PROVENANCE DEFECT / NO ALGORITHM REOPEN**

本批复核 `HPA-ZDATE-006`：南陽堂《紫微斗數全書》“子時十刻，上五刻屬昨夜亥時，下五刻屬今日子時”本命出生時辰候選。

### 1. 当前 natal runtime 仍不能表达该候选

`src/fortune_training/ziwei_chart/natal.py` 当前固定：

`23:00..00:59 -> 子`

即 `_hour_branch_index()` 对整段子时统一映射，不存在“上半子时重分类为亥”的 source-scoped 分支。

`ResolvedZiweiCalculationProfile` 当前没有 natal hour-branch reclassification policy；`config/time-calendar-policies.json` 的 Ziwei 维度仍只有：

- `ziwei.calendar_date_policy`
- `ziwei.life_body_leap_month_policy`

所以这不是“已有 policy 但 UI 未接线”，而是 natal calculation profile 本身就没有这个候选维度。

### 2. 现有 historical temporal candidate API 不是同一问题

当前公开的 Ziwei historical temporal candidates 包括：

- Jielan 1581 day-anchored **flow-hour** candidate；
- Zhongzhou **leap-month** half-split candidate。

它们解决的是目标时间投影/闰月月份归属，不会重分类本命出生时辰地支。

因此不能把“已有 temporal historical candidate API”误记成“Nanyangtang natal candidate 已实现”。

### 3. Product surface 仍不存在

当前产品面确认：

- production 仍使用唯一 `ZIWEI-CHART-ENGINE-V1` 计算 profile；
- package root 没有 Nanyangtang natal resolver/profile；
- combined local request 没有 Ziwei historical natal-candidate selector；
- `/api/profiles` 没有多套 Ziwei natal calculation options；
- Workbench 没有 Nanyangtang late-Zi selector。

所以 **HPA-ZDATE-006 继续 MISSING_FROM_PRODUCT**。

### 4. 为什么仍不能现在实现

历史证据已经比 Batch 12A 更强：

- 南陽堂直接物理影像见 `昨夜亥時 / 今日子時`；
- 廣益書局 Fullbook 物理页再次见同一 Hai 读法；
- generic upper/lower half orientation 已经关闭。

但仍有两个必须保留的防火墙：

1. **Hai 并非 broader received Ziwei transmission 全部版本通行**：韩国春岡抄本直接物理文本保留昨夜/今夜十刻结构但没有 Hai 字；
2. **runtime time-standard binding 尚未关闭**：历史时刻到底如何绑定到当前 civil / mean / local-apparent-solar instant，以及阴雨时的 source-scoped current-time acquisition chain，仍不足以授权一个可执行 natal winner。

因此不能把来源句直接硬映射成现代 23:00–24:00 的 universal runtime rule，也不能借现有 `ZI_START_23` 日期换日策略代替时辰地支重分类。

### 5. Provenance adjudication

12NT 没有发现新的 provenance defect。

现有 Matrix 已正确写明：

- current runtime 不能表达 upper-half-Zi→Hai；
- generic orientation 已关闭；
- runtime time-standard binding 未关闭；
- candidate 必须保持 source-scoped；
- no algorithm reopen。

`PROV-DEFECT-010` 是 Batch 12AH 已修复的拍卖媒体证据范围错误，本批不重复计数。

### 6. Accounting / firewall

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

下一门：**12NU — HPA-DAYUN-CAL-002 / 003 / 004 historical Jiaoyun calendarization and ten-year recurrence product/runtime reconciliation**。

Research record: `docs/research/ZIWEI-NANYANGTANG-LATE-ZI-NATAL-CANDIDATE-PRODUCT-SURFACE-RECONCILIATION-R1.json`.  
Evidence: `docs/research/evidence/batch-12nt/ziwei-nanyangtang-late-zi-natal-candidate-product-surface-reconciliation.json`.
