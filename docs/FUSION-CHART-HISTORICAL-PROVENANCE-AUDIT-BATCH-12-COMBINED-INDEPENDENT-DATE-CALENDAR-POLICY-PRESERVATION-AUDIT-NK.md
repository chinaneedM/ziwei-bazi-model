# Fusion Chart Historical Provenance Audit R1 — Batch 12NK

## HPA-COMB-002 Independent Ziwei/Bazi date/calendar policy preservation：共享物理时间下的双规则链隔离审计

Status: **MODERN COMPATIBILITY ONLY / INDEPENDENT POLICY CHAINS VERIFIED / NO NEW PROVENANCE DEFECT / NO ALGORITHM REOPEN**

本批审计 `HPA-COMB-002`。对象是联合盘在共享同一物理时间底座时，是否仍保留紫微与八字各自独立的日期、历法和换日规则。

### 1. 联合层真正要求一致的项目

`validate_shared_policy_contract()` 只要求两个子系统：

- `time_calendar_policy_registry_version` 一致；
- `civil_ambiguous_time_policy` 一致。

这是为了保证同一个墙钟输入产生同一组合法物理时间候选，而不是为了统一命理规则。

联合层并不要求：

- 紫微与八字使用相同 day boundary；
- 使用相同 calendar-date policy；
- 使用相同 late-Zi policy。

### 2. 两套规则快照明确分离

共享 credential 的 `selected_policies` 明确拆成：

- `shared_physical`
- `ziwei`
- `bazi`

其中紫微独立保留：

- `calendar_date_policy`
- `life_body_leap_month_policy`
- `day_boundary_policy`

八字则保留完整的 Bazi time selected-policies snapshot。

`validate_combined_resolution()` 会从当前 Ziwei / Bazi profiles 重新构造预期 policy snapshot；若 credential 被篡改或两边政策被错误合并，则以 `SHARED_TIME_SELECTED_POLICIES_BINDING_MISMATCH` fail closed。

### 3. late-Zi 回归证明不是“同输入=同换日”

`tests/test_combined_late_zi_day_boundary_independence_r1.py` 使用同一 local-apparent-solar 时间：

`2008-11-03 23:12`

并同时保持：

- 紫微：`ZI_START_23`
- 八字：`MIDNIGHT`
- 八字晚子时：`CLASSICAL_CONTINUOUS`

结果中八字 effective day 仍为 `2008-11-03`，而紫微按自身 23:00 换日规则进入下一日 chart-date 语义。

这直接证明：共享物理时间并没有把两个系统压成一个换日规则。

### 4. 历史审计边界

本条本身不是传统命理法，而是软件架构不变量。

真正具有历史/流派内容的是下游各自规则，例如：

- 紫微 calendar-date / late-Zi / leap-month；
- 八字 year/month/day boundary 与 late-Zi hour-stem。

这些规则继续由各自 HPA rows 独立审计。联合层不得替它们选赢家，也不得因为“融合”而消除候选。

### 5. 结论与记账

`HPA-COMB-002=MODERN_COMPATIBILITY_ONLY`。

本批没有发现新的 provenance metadata defect，也没有 chart algorithm defect。现有架构已经正确实现“共享物理时间、保留术数规则独立性”。

Matrix rows **220**；audited **214→215**；missing-product rows **10**。Provenance defects 保持 **30/30**；chart algorithm defects / reopens / candidate collapses 均为 **0**。

`transmission_impact=NONE`。这是现代联合运行时的规则隔离架构，不建立历史文本、流派或师承传承边。

下一门 **12NL：HPA-COMB-003 Candidate lineage preservation**。

研究记录：`docs/research/COMBINED-INDEPENDENT-DATE-CALENDAR-POLICY-PRESERVATION-AUDIT-R1.json`。  
证据记录：`docs/research/evidence/batch-12nk/combined-independent-date-calendar-policy-preservation.json`。
