# Fusion Chart Historical Provenance Audit R1 — Batch 12NF

## HPA-TIME-011 Approximate birth-time candidate sampling：离散采样契约、覆盖边界与分类语义审计

Status: **MODERN OPERATIONAL POLICY / SAMPLE GEOMETRY UNCHANGED / TWO PROVENANCE DEFECTS REPAIRED / NO ALGORITHM REOPEN**

本批审计 `HPA-TIME-011`。该规则不是紫微斗数或四柱古法，而是当出生时间存在“约”“分钟级”“小时级”等输入不确定性时，软件如何确定性地生成候选墙钟时刻。

### 1. 当前算法的真实性质

R1 的 `_sample_wall_times` 是**点采样器**，不是连续区间求解器。它保持：

- 区间起点、用户报告中心点、区间终点；
- 总跨度不超过 24 小时时按分钟网格补点；
- 更宽区间使用至少 3600 秒的步长；
- 宽区间按 `int(span_seconds / 1998)` 增大步长；
- 总样本集上限 2001 点。

这些 mechanics 本批全部冻结，不改变候选盘。

### 2. PROV-DEFECT-026：采样策略与覆盖粒度此前不可见

旧输出的 `input_interval` 只有：

- `uncertainty_seconds_each_side`
- `sample_count`
- `ambiguous_sample_count`

它没有告诉调用方采用什么策略、最大点数、步长或最大的实际样本间隔。因此相同的 `sample_count` 无法独立判断是分钟级密集采样还是多小时级稀疏采样。

确认：

`PROV-DEFECT-026=UNCERTAINTY_SAMPLING_STRATEGY_CAP_STEP_AND_GAP_NOT_EXPOSED_IN_RESULT_PROVENANCE`

修复后每个结果明确输出：

- `sampling_strategy=DETERMINISTIC-WALL-TIME-POINT-GRID-R1`
- `sample_cap=2001`
- `nominal_step_seconds`
- `max_sample_gap_seconds`
- `continuous_interval_exhaustive`
- `classification_scope`

### 3. PROV-DEFECT-027：单一分类状态的连续区间语义过强风险

旧状态名 `RESOLVED_RANGE_SINGLE_CLASSIFICATION` 容易被误读成：

> 整个连续出生时间区间都已经被穷举证明为同一分类。

实际算法只能证明：

> 当前确定性采样策略生成的所有**采样点**属于同一观察分类。

因此确认：

`PROV-DEFECT-027=RESOLVED_RANGE_SINGLE_CLASSIFICATION_SCOPE_NOT_EXPLICITLY_LIMITED_TO_SAMPLED_POINTS`

为保持 API 兼容，稳定 status ID 不改；但输出现在明确：

- 非零 uncertainty：`classification_scope=SAMPLED_POINTS_ONLY`
- 非零 uncertainty：`continuous_interval_exhaustive=false`
- 零 uncertainty：`classification_scope=EXACT_POINT`

任何未来真正的连续区间边界求解器必须另建版本化策略，不能无声改变 R1 语义。

### 4. 回放边界

固定中心点 `1994-05-17 23:11` 的采样机械回放包括：

| uncertainty each side | samples | nominal step | max gap |
|---:|---:|---:|---:|
| 30s | 3 | 60s | 30s |
| 120s | 5 | 60s | 60s |
| 1800s | 61 | 60s | 60s |
| 12h | 1441 | 60s | 60s |
| 1d | 51 | 3600s | 3600s |
| 100d | 2001 | 8648s | 8648s |
| 500d | 2001 | 43243s | 43243s |

宽区间结果清楚展示：2001 点上限会使采样转为稀疏点集，因此不得声称连续完备。

### 5. 结论

`HPA-TIME-011=MODERN_COMPATIBILITY_ONLY`。本批修复的是输出 provenance 与状态解释，不是采样算法，不改变任何 wall-time candidate、CivilTimeResolver 候选、Bazi/Ziwei 分类或用户默认配置。

Matrix rows **220**；audited **209→210**；missing-product rows **10**。Provenance defects **25→27 confirmed / 25→27 repaired**；chart algorithm defects / reopens / candidate collapses 均为 **0**。

### 6. Transmission impact

`transmission_impact=NONE`。这是软件不确定性采样契约，没有古籍、流派或师承边。

下一门 **12NG：HPA-DAYUN-006 Wenzhen China Dayun compatibility realization**。

研究记录：`docs/research/TIME-APPROXIMATE-BIRTH-TIME-SAMPLING-AUDIT-R1.json`。  
回放记录：`docs/research/evidence/batch-12nf/approximate-birth-time-sampling-replay.json`。
