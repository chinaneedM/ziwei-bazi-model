# Fusion Chart Historical Provenance Audit R1 — Batch 12ND

## Ambiguous civil time fold/gap handling：现代重复/缺失墙钟时间与候选保留审计

Status: **PEP-495 / ZONEINFO OPERATIONAL CONTRACT CLOSED / PROV-DEFECT-023 REPAIRED / NO ALGORITHM REOPEN**

本批审计 `HPA-TIME-002`。它不是古代命理时间规则，而是现代民用时制在时钟回拨、前拨时如何把一个墙钟坐标解释为零个、一个或两个真实 UTC instant 的操作层。

### 1. PEP 495 的机械语义

PEP 495 将回拨产生的重复本地时间称为 fold，将前拨跳过的本地时间称为 gap。对真正的 ambiguous local time：

- `fold=0` 是时间轴上较早的读数；
- `fold=1` 是时间轴上较晚的读数。

这一定义并不要求“DST 开关必须不同”，也不要求跳变恰好一小时。Python `zoneinfo` 对 IANA zone 实现同一 fold 语义。

### 2. 当前 resolver 的实现与标准一致

`CivilTimeResolver._candidate()` 对 fold 0/1 分别构造 aware datetime，转成 UTC 后再转回原 zone。只有 round-trip 后仍等于原墙钟值的 reading 才是合法候选。

因此：

- fold 中有两个合法 UTC 候选；
- 普通时间两个 fold 探针会 deduplicate 为同一 UTC 候选；
- gap 中两个探针都不能 round-trip 回原墙钟值，因此 `NONEXISTENT`、候选为空。

随后候选按 UTC instant 排序。显式 `EARLIER_OFFSET` 选择 chronologically earlier reading，`LATER_OFFSET` 选择 later reading；两个稳定 ID 中的 `OFFSET` 不是“UTC offset 数值大小”的含义。

### 3. 非一小时、非典型 DST 回放

本批增加三类控制：

1. **America/New_York 2020-11-01 01:30**：两个合法 reading 为 05:30Z / 06:30Z，差 1 小时；
2. **Australia/Lord_Howe 2020-04-05 01:45**：两个合法 reading 仅差 30 分钟，证明实现没有偷写“一小时 DST”假设；同地 2020-10-04 02:15 为 30 分钟 gap，零合法候选；
3. **Europe/Kyiv 1990-07-01 01:30**：两个合法 reading 的 DST seconds 都为 3600，但 UTC offset 从 +04:00 变 +03:00，证明算法不依赖“一个是 DST、一个不是 DST”的 shortcut。

### 4. REJECT 的真实语义与 PROV-DEFECT-023

旧 registry 文案：

`REJECT = Return both UTC candidates and require an explicit choice.`

底层 resolver 的确不选择 winner；但上层 `TimeCalendarFoundation` 的既有设计会把两个合法候选继续展开为两个分支，而不是中断请求等待立即人工选择。也就是说，真实合同一直是：

`REJECT_IMPLICIT_WINNER_SELECTION + PRESERVE_ALL_LEGAL_CANDIDATES`

因此确认：

`PROV-DEFECT-023=AMBIGUOUS_TIME_REJECT_POLICY_DESCRIPTION_IMPLIED_HARD_EXPLICIT_CHOICE_WHILE_RUNTIME_PRESERVES_ALL_BRANCHES`

修复仅调整 registry/docs 的语义说明，不改 policy ID、默认值、候选算法、分支结果或任何排盘事实。

### 5. 显式选择也不抹掉事实层 ambiguity

当选择 `EARLIER_OFFSET` / `LATER_OFFSET` 时：

- emitted branch 可缩为一个；
- 原 `CivilResolution.status` 仍为 `AMBIGUOUS`；
- 原两个合法 candidates 仍保留在 provenance；
- higher-level `ambiguous_sample_count` 仍记录该输入曾经存在两个真实读数。

这不是“已选择就把历史事实改写成 UNIQUE”。选择是 policy；ambiguous 是 fact。

### 6. 审计裁决

`HPA-TIME-002=MODERN_COMPATIBILITY_ONLY`。

本批无 chart algorithm defect，无 algorithm reopen，无 candidate collapse。Matrix rows **220**；audited **207→208**；missing-product rows **10**。Provenance defects **22→23 confirmed / 22→23 repaired**。

### 7. Transmission impact

`transmission_impact=NONE`。PEP 495 / zoneinfo 属现代计算机民用时制语义，不构成紫微或八字古代文本、人物、流派传承边。

下一门 **12NE：HPA-TIME-004 Chinese lunar calendar construction**。将把现代天文算法实现、固定 UTC+08:00 中国历日标准与历史王朝历法权威严格分层。

研究记录：`docs/research/TIME-AMBIGUOUS-CIVIL-FOLD-GAP-HANDLING-AUDIT-R1.json`。  
回放记录：`docs/research/evidence/batch-12nd/ambiguous-fold-gap-replay.json`。
