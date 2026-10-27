# Fusion Chart Historical Provenance Audit R1 — Batch 12NG

## HPA-DAYUN-006 Wenzhen China Dayun compatibility realization：现代兼容见证、Profile 身份与历史权威防火墙

Status: **MODERN COMPATIBILITY ONLY / PROFILE-ID PROVENANCE REPAIRED / NO HISTORICAL WINNER / NO ALGORITHM REOPEN**

本批审计 `HPA-DAYUN-006`。对象不是“大运古法本身”，而是仓库为复现问真八字 A7–A11 观察结果而保留的独立兼容 profile。

### 1. 证据等级

`tests/fixtures/bazi-dayun-wenzhen-compatibility-r1.json` 已明确声明：

- `authority_class=THIRD_PARTY_COMPATIBILITY_WITNESS`；
- `canonical_calendar_truth=false`；
- 捕获模式为 true-solar；
- UI 的符号起运年龄观察精度为 `YEAR_MONTH_DAY_HOUR`；
- `transition_minute_second_certified=false`。

因此 A7–A11 可以证明“该兼容模型能否重放已观察的软件行为”，不能证明“历史上唯一正确的大运法”。

### 2. 兼容 profile 的真实作用域

实际运行时 profile 为：

`BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1`

其 Wenzhen-specific 差异包括：

- 出生端使用出生地 local apparent solar wall clock，节气端使用固定 UTC+8 China-standard wall clock；
- 以 `CALENDAR_MONTH_DISPLACEMENT_THEN_DAY_HOUR_R1` 实现年/月/日/小时的公历位移；
- 十年大运边界按 `PROLEPTIC_GREGORIAN_10Y_CHINA_STANDARD_ANNIVERSARY` 实现；
- UI 只提供小时级外部观察，因此内部微秒仅用于确定性重放与连续帧边界，不能称为问真分钟/秒真值。

方向、顺逆取节、三日一岁比例、大运干支序列并不因为出现在该 profile 中就重新归属于问真。它们已有独立历史审计，必须保持来源分离。

### 3. PROV-DEFECT-028

Matrix 的 `HPA-DAYUN-006.current_profile` 此前写为：

`BAZI-TEMPORAL-V1-WENZHEN-CHINA-COMPATIBILITY-R1`

该 ID 不存在于运行时 profile registry，也不等于 fixture 中的 profile ID。实际代码、fixture 与文档一致使用：

`BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1`

确认：

`PROV-DEFECT-028=HPA_DAYUN_006_MATRIX_CURRENT_PROFILE_USED_NONEXISTENT_STALE_ID`

本批只修复 Matrix provenance identity，不修改代码算法、fixture、候选、起运时刻、大运干支或默认 profile。

### 4. 与历史大运法的边界

Batch 01 已分别审计大运方向、顺逆取节与“三日一岁”等历史规则；Batch 11B 又证明“符号年龄如何落到真实历日”存在历史 calendarized schedule family 与后世千里法等独立候选。

因此问真兼容 profile 只能保留为：

`MODERN_COMPATIBILITY_ONLY`

它不能覆盖、替代或裁决上述历史候选，更不能因现代软件行为一致而提升为古籍权威。

### 5. 结论与记账

Matrix rows **220**；audited **210→211**；missing-product rows **10**。Provenance defects **27→28 confirmed / 27→28 repaired**；chart algorithm defects / reopens / candidate collapses 均为 **0**。

`transmission_impact=NONE`。现代第三方软件兼容见证不建立古籍、版本、人物、流派或师承传承边。

下一门 **12NH：HPA-DAYUN-007 Exact-Jie tie handling**。

研究记录：`docs/research/BAZI-DAYUN-WENZHEN-COMPATIBILITY-SCOPE-AUDIT-R1.json`。  
审计证据：`docs/research/evidence/batch-12ng/wenzhen-dayun-compatibility-scope.json`。
