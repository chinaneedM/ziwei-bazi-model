# 八字运限神煞 Sidecar Replay Closure R1

## 1. 阶段定位

R1.9 不新增神煞规则，也不改变 R1.7/R1.8 的 target-match 语义。它只收紧 `BAZI-TEMPORAL-SHENSHA-PROJECTION-SIDECAR-R1` 的产品完整性边界。

R1.8 已经完成独立 sidecar、hash、integrity、full replay、API payload 与 Workbench 展示。R1.9 处理两个剩余工程风险：

1. public `resolve()` 之前虽然可由测试显式调用 full replay，但产品路径本身没有强制即时 replay closure；
2. sidecar 已同时拥有 base application 与 target-flow lineage，却只按 candidate id 找 source application candidate，没有额外验证该 id 是否与 flow 声明的 `natal_candidate_index + source_temporal_candidate_indices` 精确对应。

本阶段不修改已经发布的：

- `BAZI-APPLICATION-FLOW-RESOLUTION-R1`；
- `BAZI-APPLICATION-FLOW-VIEW-R1`；
- `BAZI-UNIFIED-TARGET-TIMELINE-R1`；
- 旧 flow candidate id / view hash / source fact hash / bundle hash 计算输入。

## 2. Source application lineage closure

对每个 target-flow candidate，sidecar 现在同时验证两条 source 身份路径：

```text
source_application_candidate_ids
        +
flow.natal_candidate_index
        +
flow.source_temporal_candidate_indices
        ↓
必须指向同一组 base application candidates
```

具体要求：

- base application candidate id 必须唯一；
- `(natal_candidate_index, temporal_candidate_index)` 坐标必须唯一；
- `source_application_candidate_ids` 数量必须与 `source_temporal_candidate_indices` 一致；
- 每个 source id 必须存在；
- 每个 source id 必须就是同一 natal index、同一 temporal index 坐标上的 candidate；
- 不允许用另一个合法 application candidate id 替代正确 lineage 后继续投影。

任何不一致都 fail closed，不选择第一个，也不按 ShenSha 内容相同而放宽 lineage。

## 3. Public resolve replay closure

`BaziTemporalShenshaSidecarService.resolve()` 现在执行两个相互独立的即时 deterministic materialization：

```text
same validated base application
+ same validated target-flow bundle
        ↓
resolve once
        ↓
resolve replay
        ↓
objects must be exactly equal
```

如果第二次 materialization 与第一次不完全一致，public resolve 直接失败：

`BAZI_TEMPORAL_SHENSHA_FULL_REPLAY_FAILED`

因此 `/api/resolve-flow` 只要调用 public sidecar service，就天然经过 replay-closed 边界。现有独立 `validate_temporal_shensha_sidecar_full_replay()` 继续保留，用于外部对象、持久化对象和 tamper replay。

正常 deterministic 输入的 sidecar schema、candidate ids、fact hashes、computation hashes 与 bundle hash 算法均不改变。

## 4. Multi-candidate preservation

R1.9 增加产品级 DST fold 回归：目标时间若存在两个合法 civil-time realizations，则：

- `bazi_target_flow_bundle` 保留两个 target-flow candidates；
- ShenSha sidecar 同样保留两个 candidates；
- 每个 sidecar candidate 精确绑定对应 flow candidate id；
- 每个 sidecar candidate 精确绑定对应 target coordinate candidate id；
- 不自动选择 fold=0 或 fold=1。

这不是神煞规则差异，而是目标时间身份差异，必须原样传播。

## 5. PRE_DAYUN preservation

目标时点位于交运前时，R1.9 固定回归：

- 大运 slot 状态仍为 `PRE_DAYUN_NO_GANZHI_PROJECTION`；
- 不制造大运干支；
- 不制造大运 ShenSha target-match；
- 其他已合法解析的流年、流月、流日、流时层仍按各自已有坐标处理。

## 6. Wrapper schema hardening

`combined-local-target-flow-response-r1.schema.json` 继续保留 additive sidecar payload，但现在将 ShenSha sidecar 顶层设为 closed object，并要求完整的 source fact hashes、diagnostics 与 bundle hashes。

这只收紧 wrapper validation，不改变实际 API payload 结构，也不把 sidecar 字段写进旧 `bazi_target_flow_bundle`。

## 7. 语义边界保持不变

R1.9 继续禁止：

- 把 target-match 称为已经裁决的“流年神煞/流月神煞”；
- 把 `NOT_CLASSICALLY_ARBITRATED` 改成确定适用；
- 将 `ONLY_DAY` 传播到非 DAILY 层；
- 将 `SANQI / JIALU / YUANCHENG` 降格成单干支匹配；
- 合并两套小运并选择赢家；
- 输出旺衰、格局、用神、喜忌、吉凶、事件或应期。

R1.9 的目标只有一个：让 R1.8 sidecar 在真实产品路径上的 lineage 与 replay contract 完整闭合。
