# Fusion Chart Historical Provenance Audit R1 — Batch 12NK

## HPA-COMB-002 Independent Ziwei/Bazi date/calendar policy preservation

Status: **MODERN COMPATIBILITY ONLY / ARCHITECTURE MATCH / NO PROVENANCE DEFECT / NO ALGORITHM REOPEN**

本批审计 `HPA-COMB-002`。对象不是某一条古法，而是联合排盘如何在共享同一物理时间事实的同时，保持紫微与八字各自独立的日期、历法与换日规则。

### 1. 共享的只有物理时间底座

`validate_shared_policy_contract()` 只要求两套 profile 的：

- `time_calendar_policy_registry_version` 一致；
- `civil_ambiguous_time_policy` 一致。

它没有要求紫微与八字采用相同的历法日期、换日或晚子时规则。

联合服务随后分别调用紫微时间解析与八字时间解析，再把两套结果写入共享 credential。共享层因此是事实联动层，不是规则归并层。

### 2. 两套规则链保持独立

`shared_time_credential.selected_policies` 明确分成：

- `shared_physical`；
- `ziwei`；
- `bazi`。

紫微侧独立保存 `calendar_date_policy`、`life_body_leap_month_policy`、`day_boundary_policy`；八字侧完整保留其自身 time/calendar policy snapshot，包括 year/day boundary 与 late-Zi hour-stem policy。

完整性校验会重新从两个 subsystem profile 构造预期 policy snapshot；任何一侧被另一侧覆盖都会触发 `SHARED_TIME_SELECTED_POLICIES_BINDING_MISMATCH`。

### 3. 23:00 late-Zi 回归证明规则未被强制统一

`tests/test_combined_late_zi_day_boundary_independence_r1.py` 在同一 local-apparent-solar 物理时刻上同时验证：

- 紫微：`ZI_START_23`；
- 八字：`MIDNIGHT`；
- 八字晚子时：`CLASSICAL_CONTINUOUS`。

该测试进一步验证联合盘生成的紫微 bundle hash 与独立紫微服务一致，八字 bundle hash 与独立八字服务一致。换言之，联合层没有为了“共享”而改变任何子系统结果。

### 4. 历史权威边界

本条规则是现代软件架构约束，不是历史命理规则。

紫微为何采用某个 calendar/date/leap policy，八字为何采用某个 day-boundary/late-Zi policy，必须继续由各自历史审计行决定。联合层只能保存这些选择，不能成为它们的历史权威，也不能用“统一时间底座”推导出“统一换日法”。

### 5. 结论

`HPA-COMB-002=MODERN_COMPATIBILITY_ONLY`。

本批未发现新的 provenance metadata defect，也没有 chart algorithm defect、algorithm reopen 或 candidate collapse。

Matrix rows **220**；audited **214→215**；missing-product rows **10**；provenance defects 保持 **30/30**。

`transmission_impact=NONE`。

下一门：**12NL — HPA-COMB-003 Candidate lineage preservation**。

研究记录：`docs/research/COMBINED-INDEPENDENT-DATE-CALENDAR-POLICY-PRESERVATION-AUDIT-R1.json`。  
审计证据：`docs/research/evidence/batch-12nk/combined-independent-date-calendar-policy-preservation.json`。
