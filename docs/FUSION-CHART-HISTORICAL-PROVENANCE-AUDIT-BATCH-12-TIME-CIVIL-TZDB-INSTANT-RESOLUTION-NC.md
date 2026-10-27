# Fusion Chart Historical Provenance Audit R1 — Batch 12NC

## Civil timezone / TZDB instant resolution：现代民用时区权威、历史适用范围与可复现性审计

Status: **MODERN CIVIL-TIME INFRASTRUCTURE / TWO PROVENANCE DEFECTS REPAIRED / OFFSET-DST-FOLD-GAP MECHANICS UNCHANGED / NO ALGORITHM REOPEN**

本批审计 `HPA-TIME-001`。结论是：IANA tzdb + Python `zoneinfo` 是把“已知的民用墙钟时间 + 明示 timezone_id”解析到 UTC instant 的现代基础设施；它不是紫微斗数或四柱八字古法，也不能替代对历史出生记录采用何种地方/官方时间制度的考据。

### 1. 1970 边界是 UTC instant，不是本地年份

IANA tzdb 2026e Theory 把 location zones 的核心一致性范围绑定到 POSIX Epoch `1970-01-01 00:00:00 UTC` 之后的 timestamps，并说明 pre-1970 资料不足以覆盖全部历史民用计时。

旧实现 `_confidence(local_datetime)` 仅检查 `local_datetime.year >= 1970`，会在 UTC 分界附近双向误标：

- `1970-01-01 00:30 Asia/Shanghai` → `1969-12-31 16:30Z`，旧实现误标 POST_1970；
- `1969-12-31 19:30 America/New_York` → `1970-01-01 00:30Z`，旧实现误标 PRE_1970。

确认：
`PROV-DEFECT-021=TZDB_HISTORICAL_CONFIDENCE_BOUNDARY_USED_LOCAL_CALENDAR_YEAR_INSTEAD_OF_UTC_POSIX_EPOCH`

修复后以 wall time 在 zone 中可能形成的 UTC realization(s) 对 POSIX Epoch 保守比较。只改变 `HistoricalTimezoneConfidence` 与 warning，不改变 UTC candidate、offset、DST、fold/gap 或排盘结果。

### 2. ZoneInfo 的真实数据源优先级

Python `zoneinfo` 文档规定：`ZoneInfo(key)` 先在 `TZPATH` 查找系统时区文件，失败后才回退到第一方 PyPI `tzdata` 包。

旧 `_tzdb_version()` 只要发现安装了 `tzdata` 就回报该包版本，因此在 POSIX 环境可能把未参与解析的 PyPI 包版本写进 provenance。

确认：
`PROV-DEFECT-022=TZDB_VERSION_METADATA_REPORTED_INSTALLED_PYPI_TZDATA_WHEN_SYSTEM_ZONEINFO_SOURCE_WON`

修复后系统 zone file 存在时报告 `SYSTEM-TZDB-UNVERSIONED`；只有系统路径没有该 zone、运行时依赖 package fallback 时才回报 PyPI `tzdata` 版本。此修复只纠正来源标记，不改变 `ZoneInfo` 解析路径。

### 3. 中国历史民用时区作用域

IANA 2026e `asia` 源直接区分：

- Beijing time：`Asia/Shanghai`，作为北京时间代表；
- Xinjiang time：`Asia/Urumqi`，作为多人使用的新疆时间代表；若采用北京时间则使用 `Asia/Shanghai`。

IANA 同时说明新疆 1986 年以前资料不足。因此出生地点经度不能自动决定历史出生记录采用哪一种民用时钟标准；`timezone_id` 必须作为明确输入语义保存，也不能与真太阳时、地方平太阳时或中国历日固定 UTC+08:00 边界混为一条规则。

### 4. 权威边界

IANA 自身明确称 tzdb **not authoritative** 且存在错误，尤其 pre-1970 历史覆盖有限。本项目采用：

`reported wall time + explicit timezone_id → modern tzdb realization → UTC instant`

而不采用：

`古代出生记录 → tzdb 自动证明当时当地唯一合法时间制度`

特定历史地点/年代若需更高等级认证，应继续查国家标准、地方档案、官方时制公告、报刊、铁路/电报/天文台材料。

### 5. 工程回放与不重开结论

新增测试覆盖 UTC epoch 两侧的 east/west 反例，以及 system TZPATH / PyPI tzdata 两种来源优先级。既有现代中国时间、1988 中国 DST、1991 中国 gap/fold、New York fold/gap 等测试继续约束 actual civil-time resolution。

结论：`HPA-TIME-001=MODERN_COMPATIBILITY_ONLY`。本批确认 **2 个 provenance/confidence metadata defects**，不是 chart algorithm defect；`algorithm_reopen_authorized=false`。

Matrix rows **220**；audited **206→207**；missing-product rows **10**。Provenance defects **20→22 confirmed / 20→22 repaired**；chart algorithm defects / reopens / candidate collapses 均为 **0**。

### 6. Transmission impact

`transmission_impact=NONE`。本批没有新增古代命理文本、师承、流派或术语传承边。

下一门 **12ND：HPA-TIME-002 Ambiguous civil time fold/gap handling**，继续审计 REJECT / candidate-preservation / explicit fold policy 的现代操作语义。

研究记录：`docs/research/TIME-CIVIL-TZDB-INSTANT-RESOLUTION-AUDIT-R1.json`。  
回放记录：`docs/research/evidence/batch-12nc/timezone-confidence-and-source-provenance-replay.json`。
