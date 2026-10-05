# Fusion Chart Historical Provenance Audit R1 — Batch 12NV

## Unresolved historical-status prioritization

Status: **PRIORITIZATION CLOSED / NEXT TARGET HPA-ZIWEI-023 / NO STATUS COLLAPSE / NO ALGORITHM REOPEN**

12NU 之后，当前 10 条 `MISSING_FROM_PRODUCT` 已全部完成 live runtime/product-surface reconciliation。Historical Audit 仍有：

- 30 `DISPUTED_MULTIPLE_CANDIDATES`
- 11 `SOURCE_INSUFFICIENT`
- 1 `NOT_YET_FORMALIZED`

本批不以“把未决数量变少”为目标，而是按**当前 deterministic output 风险**重新排队。

### 1. 排序原则

优先级从高到低：

1. production 正在输出、但历史来源仍 `SOURCE_INSUFFICIENT`；
2. 其中又以“唯一赢家未闭合”“时间层/身份可能改变机械含义”高于纯显示顺序；
3. runtime 已 fail-closed / 尚未 formalize 的问题，研究价值可以很高，但即时算法风险低于 active-output provenance gap；
4. 已经拆成 child rows 的 broad parent row 不重复审；
5. `DISPUTED_MULTIPLE_CANDIDATES` 不因“有争议”就强行选赢家。

### 2. 第一优先：HPA-ZIWEI-023

当前 production：

`WENMO_SHENZHU_BY_YEAR_BRANCH["子"/"午"] = 火星`

严格 source profile：

`QS_SHENZHU_ZI_WU_TEXTUAL_AMBIGUITY`

1581 Jielan registry：

`TEXTUAL_COMPOSITE_FIRE_BELL_NOT_UNIQUELY_ARBITRATED`

来源定位：

`EXT-ZIWEI-JIELAN-1581:CH32`

Matrix 还记录 received Fullbook 的复合文字：

- `子午生人铃火宿`
- `子午人火铃星`

所以目前最关键的问题不是“代码会不会算”，而是 **production 兼容选择 Fire 是否能获得独立、版本绑定的历史/校注证据，还是必须永久保持 compatibility-only**。

在证据关闭前：

- strict QS 继续 fail-closed；
- historical Jielan sidecar 继续 `winner_selected=false`；
- production Fire 不得被改写成“古法真值”。

### 3. 后续梯队

第二优先：`HPA-ZIWEI-026` 将前十二神。production 已输出，但 early-edition authority 与 natal/annual temporal scope 不足。

第三优先：`HPA-ZMINOR-020` standalone 蜚廉。需要继续保持与 `RING.BOSHI12.FEILIAN` 身份隔离，并寻找 standalone 表的 edition-bound witness。

其后：`HPA-ZMINOR-023/024/025/026` 月解、天巫、天月、阴煞。均是 active compatibility tables，但 Ziwei-specific historical placement provenance 尚不足。

`HPA-BAZI-015` / `HPA-BHIDDEN-002` 排序较后，因为 repository 已明确禁止把 hidden-stem ordinal 当作本气/中气/余气或强弱语义。

`HPA-ZIWEI-008` / `HPA-ZIWEI-011` 是 broad parent rows，已经拆解到具体 child rows，不重复作为直接目标。

### 4. HPA-ZT-016 的位置

自化/向心离心方向依然重要，而且是项目 invariant：

`NOT_YET_FORMALIZED`

但当前 runtime 只发 neutral topology，不生成 inward/outward direction。因此它不是当前最高的 deterministic-output provenance 风险。继续保持缺省比为了“清状态”强行 formalize 更正确。

### 5. Accounting

- Matrix rows: **220**
- audited: **220**
- current `MISSING_FROM_PRODUCT`: **10**，且 10/10 已 product-surface reconciled
- provenance defects: **39/39**
- chart algorithm defects: **0**
- algorithm reopens: **0**
- candidate collapses: **0**

`transmission_impact=NONE`

下一门：**12NW — HPA-ZIWEI-023 Zi/Wu Shenzhu Fire/Bell evidence closure**。

Research record: `docs/research/HISTORICAL-UNRESOLVED-STATUS-PRIORITIZATION-R1.json`.  
Evidence: `docs/research/evidence/batch-12nv/historical-unresolved-status-prioritization.json`.
