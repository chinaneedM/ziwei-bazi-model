# Fusion Chart Historical Provenance Audit R1 — Batch 12NM

## HPA-COMB-005 Shared target → Ziwei projection

Status: **MODERN COMPATIBILITY ONLY / PROVENANCE SCOPE REPAIRED / UPSTREAM HISTORICAL AUTHORITY PRESERVED / NO ALGORITHM REOPEN**

本批审计 `HPA-COMB-005`：共享目标时点进入紫微投影后，Combined 层究竟是在“创造一套新的紫微时限规则”，还是只把已经发布的紫微规则与候选映射到同一物理目标坐标上。

### 1. 投影层本身是现代软件组合

`SharedZiweiSelectorProjectionService.project(...)` 接收已经解析的共享目标坐标候选。每个候选继续保留 `source_target_candidate_index` / `source_target_candidate_id`、sample local datetime、UTC、DST fold、共享目标坐标 hashes 与 Ziwei application/temporal 身份。

随后紫微侧使用自己的 calendar-date policy、day-boundary policy 与 lunar-date resolver 重算有效日期。Combined 层没有把八字年/月/日/晚子时规则覆盖到紫微，也没有建立“紫微＋八字共同历法”的历史主张。

### 2. 已发布层事实只读投影，不重新发明

当前投影保存已发布的大限、流年、小限及原局三环交会、正常流月、流日、流时方法候选及各层已有动态辅助星、四化与候选身份。

完整 replay 会重新调用同一 projection service 并比较整个 dataclass。局部重算 hash 不能掩盖上游 frame、policy、candidate 或 lineage 漂移。

因此 `HPA-COMB-005` 的历史属性只能是现代软件投影层；真正的紫微历史权威必须回到各上游规则行和 source-scoped candidate registry。

### 3. R1.10 之后新增的历史候选必须分层

原始 `SHARED-ZIWEI-TARGET-PROJECTION-PRODUCTIZATION-R1.md` 正确声明“没有新增 doctrinal arbitration”，但它形成于 R1.10，早于后续两个 source-scoped temporal historical candidates 的产品化：

1. `JIELAN-1581-DAY-ANCHORED-FLOW-HOUR-R1`：单独输出在 `historical_hourly_method_candidates`；与原有 fixed-branch case candidates 分列；`selection_status=PRESERVED_NOT_SELECTED`；1581 来源只授权日宫锚定的流时宫位几何，不授权现代时间标准或跨流派辅助星/四化。
2. `ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1`：单独输出在 `leap_month_method_candidates`；正常 production 月/日字段仍维持 `LEAP_MONTH_UNRESOLVED_NO_FRAME` / `PARENT_LEAP_MONTH_UNRESOLVED_NO_FRAME`；候选只关闭闰月前后半月归属与十五/十六不重置，未关闭闰月初一的流日起点。

这些历史候选的权威属于既有 Ziwei 历史审计和 registry，而不是 Combined projection。

### 4. PROV-DEFECT-032

Matrix 原先的 `source_quote_location` 只指向 R1.10 productization 文档，且 `current_implementation` 只概括 Daxian/Annual/Month/MinorLimit/Daily。它已经不足以描述当前运行面，因为后续 source-scoped temporal historical candidates 已进入同一个 projection payload。

确认：

`PROV-DEFECT-032=HPA_COMB_005_SOURCE_SCOPE_STOPPED_AT_R1_10_AND_OMITTED_LATER_SOURCE_SCOPED_TEMPORAL_CANDIDATES`

修复仅扩展 Matrix provenance 到当前 projection service、R1.10 productization、历史候选 productization/runtime 和 focused tests。没有修改 runtime、schema、hash、候选、默认方法或紫微算法。

### 5. 裁决

`HPA-COMB-005=MODERN_COMPATIBILITY_ONLY`。Combined projection 的职责是共享物理 target identity、紫微独立政策重放、上游层事实只读投影、候选身份完整保留；它不选 winner，也不从软件组合层反推历史流派权威。

Matrix rows **220**；audited **216→217**；missing-product rows **10**。Provenance defects **31→32 confirmed / 31→32 repaired**。Chart algorithm defects / reopens / candidate collapses 均为 **0**。

`transmission_impact=NONE`：本批只修现代软件组合层的 provenance 归属；1581 与中州候选已有自己的来源/流派节点，本批不新增文本—人物—流派传承边。

下一门：**12NN — HPA-COMB-006 Combined Target Flow Fusion R2**。

研究记录：`docs/research/COMBINED-SHARED-TARGET-ZIWEI-PROJECTION-AUDIT-R1.json`。  
审计证据：`docs/research/evidence/batch-12nm/combined-shared-target-ziwei-projection.json`。
