# 八字运限神煞目标匹配 Sidecar R1

## 1. 阶段目的

R1.8 将 R1.7 已完成的 `BAZI-TEMPORAL-SHENSHA-TARGET-PROJECTION-R1` 从内部投影内核产品化为独立 sidecar bundle，并接入联合只读 Workbench。

该阶段不改变已经发布的 `BAZI-APPLICATION-FLOW-RESOLUTION-R1`、`BAZI-APPLICATION-FLOW-VIEW-R1` 或 `BAZI-UNIFIED-TARGET-TIMELINE-R1`。旧 flow candidate、`candidate_id`、`view_hash`、`source_fact_hash`、`bundle_hash` 的计算输入保持不变。

## 2. 输入与 lineage

Sidecar 只接受两个已经解析并通过完整性校验的上游对象：

1. `combined_resolution.bazi_bundle`；
2. 与之绑定的 `bazi_target_flow_bundle`。

每个 target-flow candidate 必须通过 `source_application_candidate_ids` 精确回指原局 application candidates。Sidecar 从这些原局 candidate 的 `view["shensha"]` 读取唯一规则输入，再使用该 target-flow candidate 已存在的 timeline 动态干支进行 R1.7 target-match。

Sidecar 不重新构造出生四柱，不从显示文字反推原局，不建立第二套神煞规则表。

## 3. Fail-closed 规则

同一个 target-flow lineage 可能包含多个 source application candidates。只有在这些 candidates 的 `view["shensha"]` 内容完全一致时，才允许进入投影。

如果任一 source candidate：

- 缺少 `view["shensha"]`；
- 无法由 `source_application_candidate_ids` 唯一找到；
- 与同 lineage 的其他 source ShenSha 内容不同；
- 上游 application 或 target-flow 完整性 replay 失败；
- 上游 bundle hash 绑定不一致；

则 sidecar 解析失败。不得选择第一个 candidate 继续，也不得静默合并差异。

## 4. 独立 bundle

Sidecar schema：

`BAZI-TEMPORAL-SHENSHA-PROJECTION-SIDECAR-R1`

每个 sidecar candidate 独立保存：

- 精确的 source target-flow candidate id/index；
- source flow index 与 target coordinate lineage；
- source application candidate ids 与 view hashes；
- source ShenSha hash；
- R1.7 projection；
- candidate `fact_hash`；
- candidate `computation_hash`；
- sidecar `candidate_id`。

整个 resolution 另外保存独立 `fact_hash`、`computation_hash`、`bundle_hash` 与 integrity report。它们不写回旧 flow bundle。

## 5. Replay 与篡改检测

结构完整性验证会重新计算：

- R1.7 projection fact/computation hash；
- sidecar candidate fact/computation hash 与 candidate id；
- resolution fact/computation/bundle hash；
- profile、projection policy、selection semantics 与 semantic scope。

Full replay 会从同一已发布 application bundle 和 target-flow bundle 重新生成整个 sidecar，并要求对象完全相等。任何 target-match 内容、政策字段、lineage 或 hash 的静默修改都必须导致 replay 失败。

## 6. API 接入

`/api/resolve-flow` 在保留原有 payload 的同时新增：

`bazi_temporal_shensha_projection_bundle`

原有：

- `combined_resolution`；
- `bazi_target_flow_bundle`；
- `combined_target_flow_resolution`；

均保持自身 schema/hash 计算不变。

## 7. Workbench 显示边界

大运、小运候选、流年、流月、流日、流时的现有 frame card 会按 `source_bazi_target_flow_candidate_id` 精确找到对应 sidecar candidate，再显示各层 target-match。

固定 UI 标题：

`神煞候选目标命中`

固定免责声明：

`仅为目标身份匹配；岁运神煞适用性尚未作古法/流派裁决。`

禁止把这些结果显示成“流年神煞：XXX”等已经完成古法/流派裁决的结论。

## 8. 仍未裁决的范围

R1.8 不改变 R1.7 的语义边界：

- `temporal_applicability_status` 仍为 `NOT_CLASSICALLY_ARBITRATED`；
- `ONLY_DAY` 仍只允许进入 DAILY target-match；
- `SANQI / JIALU / YUANCHENG` 等结构型候选仍不降格为单干支匹配；
- 两套小运继续并列，不选赢家；
- `PRE_DAYUN` 继续保留 `PRE_DAYUN_NO_GANZHI_PROJECTION`；
- 不输出吉凶、旺衰、格局、用神、喜忌、事件或应期判断。
