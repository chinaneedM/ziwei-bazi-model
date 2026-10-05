# Fusion Chart Historical Provenance Audit R1 — Batch 12NE

## HPA-TIME-004 Chinese lunar calendar construction：现代农历规则、数值认证边界与历史历法防火墙

Status: **MODERN_COMPATIBILITY_ONLY / RULE STRUCTURE MATCHES / STRICT GB/T NUMERICAL CERTIFICATION NOT PROVED / TWO PROVENANCE DEFECTS REPAIRED / NO ALGORITHM REOPEN**

本批审计 `HPA-TIME-004`。结论分成三个层次：

1. **规则层**：现行实现与现代农历核心编排规则一致——北京时间、朔日为初一、冬至所在月为十一月、两个十一月之间若有 13 个月则取最先无中气月为闰月。
2. **数值实现层**：当前使用 Astronomy Engine 计算朔与太阳视黄经事件；这是一套现代天文计算实现，但本项目没有证明其满足 GB/T 33661-2017 所要求的 IERS 模型口径与朔/节气北京时间 1 秒计算精度，因此不得标成“严格国标认证实现”。
3. **历史层**：现代国标农历不能倒投为明大统、清时宪或更早王朝历法；历史 calendar adapter 继续 fail-closed。

### 1. 现代标准身份与规则结构

全国标准信息公共服务平台显示 GB/T 33661-2017《农历的编算和颁行》仍为现行国家推荐标准，2017-09-01 实施，2023-12-28 复审结论为继续有效，主要起草单位为中国科学院紫金山天文台。

紫金山天文台公开材料明确说明：

- 农历以月亮朔的时刻所在日期作为月首；
- 包含冬至的农历月固定为十一月；
- 若两个十一月之间有 13 个农历月，则最先出现的不含中气月为闰月；
- 十一月后第二个非闰月为正月。

当前 `ChineseCalendarEngine` 的 month-start、month-11、principal-term、leap-index 和 month numbering 机制与这一规则层一致。

### 2. 数值认证边界

GB/T 33661 的编算层不仅规定规则，还规定计算模型与精度。紫金山天文台对标准的官方解读明确指出，朔和节气用于日期判定时的北京时间计算精度应达到 1 秒，并基于规定的基本天文学/IERS 模型体系。

仓库使用的 Astronomy Engine 上游公开定位是小型、快速、约 ±1 arcminute 位置精度的 VSOP87/NOVAS 系实现。它非常适合作为现代工程计算引擎，但“约 ±1 arcminute 的上游设计目标”不能直接等价为“已验证满足 GB/T 33661 的 IERS 模型与 1 秒事件时刻门槛”。

因此确认：

`PROV-DEFECT-025=GBT33661_RULE_COMPATIBILITY_MISLABELED_AS_STRICT_NUMERICAL_CONFORMANCE`

修复方式：在 `ChineseCalendarEngine` 与 audit trace 中明确记录：

`RULE_STRUCTURE_COMPATIBLE_NOT_CERTIFIED_FOR_IERS_MODEL_OR_1S_EVENT_TIMING`

不改变任何朔、节气、月份、闰月或日期运算。

### 3. 1901–2100 的真实含义

香港天文台官方公历—农历对照表公开覆盖 1901–2100。此前文档把相同的 `supported_years=(1901,2100)` 写成 “R1 validated range”，但当前仓库只保存了少量 HKO 日期级回归 oracle，并没有对整个 200 年逐日独立认证。

因此确认：

`PROV-DEFECT-024=MODERN_CHINESE_CALENDAR_1901_2100_SUPPORT_RANGE_MISLABELED_AS_VALIDATED_RANGE`

修复后统一为：

`HKO_PUBLIC_CONVERSION_TABLE_RANGE_NOT_EXHAUSTIVE_FULL_RANGE_VALIDATION`

1901–2100 仍是运行支持边界，不缩减功能，不改变任何日期结果。

### 4. HKO 未来近午夜不确定性

香港天文台明确提示：数十年后的月相和节气计算可能有数分钟误差；若事件接近午夜，相关农历月份或节气日期可能相差一天。HKO 特别列出以下新月：

- 2057-09-28
- 2089-09-04
- 2097-08-07

R1 现把这三日登记为 provenance-level forecast boundary warnings。它们不表示当前算法一定错误，也不授权人为改一天；它们表示“当前预测结果不应被包装成未来日期的绝对国标认证”。

### 5. 历史历法防火墙

`docs/HISTORICAL-CHINESE-CALENDAR-ADAPTER-CONTRACT-R1.md` 继续有效：

- `MODERN-CHINESE-CALENDAR-ASTRONOMICAL-V1` 不得作为历史王朝历法权威；
- 明大统、清时宪等必须按各自 source/regime/version 建立适配器；
- 不能用现代 Gregorian anniversary 或现代农历回投古代规则；
- 未认证的历史算术必须 fail-closed。

### 6. 工程变更与结论

本批新增的运行时信息仅是 provenance metadata：

- `standard_reference`
- `standard_conformance`
- `support_range_basis`
- HKO 近午夜未来新月不确定性日期
- audit trace 中的标准/认证/支持范围字段

以下 mechanics 完全不变：

- new-moon search；
- fixed UTC+08 日界；
- winter-solstice month selection；
- principal-term containment；
- leap-month selection；
- month numbering；
- lunar day calculation。

因此 `HPA-TIME-004=MODERN_COMPATIBILITY_ONLY`，`algorithm_reopen_authorized=false`。

Matrix rows **220**；audited **208→209**；missing-product rows **10**。Provenance defects **23→25 confirmed / 23→25 repaired**；chart algorithm defects / reopens / candidate collapses 均为 **0**。

### 7. Transmission impact

`transmission_impact=NONE`。本批是现代国家历法标准与软件数值实现的 provenance 边界，没有新增古代紫微/八字师承或文本传承边。

下一门 **12NF：HPA-TIME-011 Approximate birth-time candidate sampling**。

研究记录：`docs/research/TIME-MODERN-CHINESE-CALENDAR-CONSTRUCTION-AUDIT-R1.json`。  
证据记录：`docs/research/evidence/batch-12ne/modern-chinese-calendar-authority-boundary.json`。
