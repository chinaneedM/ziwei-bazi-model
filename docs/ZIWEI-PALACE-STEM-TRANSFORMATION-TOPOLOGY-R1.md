# 紫微宫干四化目标拓扑 R1

## 1. 目的

本层把已经发布的十二宫宫干与 S08 当前唯一四化表组合成一个**只描述目标落宫几何关系**的确定性 sidecar，用于联合排盘 Workbench 展示宫干四化的目标星与目标宫位关系。

它只回答：

> 对某一个已经发布的宫干，按当前 S08 四化分配表得到的化禄、化权、化科、化忌目标星分别落在同宫、对宫还是其他宫？

它不回答：

- 该关系是否构成离心自化；
- 该关系是否构成向心自化；
- `SAME_PALACE` 是否应解释为 `OUTWARD_DISSIPATION`；
- `OPPOSITE_PALACE` 是否应解释为 `INWARD_RECEPTION`；
- 四化、自化、向心化的吉凶、强弱、事件或结果；
- 存在流派争议时哪个方向候选应该胜出。

因此当前 release boundary 必须保持为：

- `GEOMETRIC_SAME_OPPOSITE_OTHER_ONLY`；
- `NO_SELF_OR_INWARD_DIRECTION_CLASSIFICATION_NO_WINNER`；
- `PALACE_STEM_TARGET_TOPOLOGY_ONLY_NO_SELF_TRANSFORMATION_DIRECTION_OR_INTERPRETATION`。

## 2. Canonical 来源边界

本层不建立第二套四化表，也不使用文墨天机等商业软件的箭头符号反推规则。

Canonical 规则来源仍是 S08：

- `sources/canonical/S08_十干四化自化与禄忌线库.txt`；
- 运行切片：`sources/canonical-runtime/S08/segment-0001.txt`；
- 当前四化规则集：`S08_CURRENT_40_ASSIGNMENT_R1`。

S08 明确把生年、一般宫干、主题宫干、大限、流年与流月四化归入同一当前运行四化表。现有 `TransformationGenerator` 已经承载该表，并允许改变 causal stem / source layer，而不移动星曜的物理落宫地址。

S08 同时定义了自化 / 向心化相关枚举与事实字段，但当前已经释放的 runtime contract **没有证明一个可自动执行的机械 selector**，能够把 `SAME_PALACE / OPPOSITE_PALACE / OTHER_PALACE` 直接转换为 `OUTWARD_DISSIPATION / INWARD_RECEPTION`。因此方向字段继续保持未 formalize。

## 3. 已发布 sidecar

后端入口：

- `src/fortune_training/ziwei_application/palace_stem_topology.py`
- schema：`ZIWEI-PALACE-STEM-TRANSFORMATION-TOPOLOGY-SIDECAR-R1`
- profile：`ZIWEI-PALACE-STEM-TRANSFORMATION-TOPOLOGY-R1`

输入不是重新计算出来的十二宫，而是已经通过 `ZiweiChartService` 发布并校验的 `ApplicationChartBundle`：

- 十二个 `address_attributes` 提供 canonical address + palace stem；
- 已发布 placements 提供四化目标星的物理地址；
- `TransformationGenerator` 按每一个 palace stem 生成四个 transformation activation。

R1 必须得到精确的 `12 × 4 = 48` 条 row：

- 每个 source palace 恰好 4 条；
- transformation type 恰好为 `化禄 / 化权 / 化科 / 化忌`；
- source palace address / branch / stem 保持稳定；
- target star identity 与 target address 来自已发布 placement；
- `assignment_id / mechanism_id / source_refs` 保留 S08 生成器 lineage。

## 4. 拓扑分类

当前只允许三种 `topology_relation`：

- `SAME_PALACE`：source address 与 target address 相同；
- `OPPOSITE_PALACE`：target address 是 source address 的十二宫对宫；
- `OTHER_PALACE`：其余情况。

这三个值只表示宫位几何关系，不含方向、吉凶或事件语义。

尤其不得建立以下隐式等价：

- `SAME_PALACE -> OUTWARD_DISSIPATION`；
- `OPPOSITE_PALACE -> INWARD_RECEPTION`。

如果未来 canonical source 能够证明自化 / 向心化 selector，必须新增独立、版本化、可 replay 的方向事实层；不能通过修改本 R1 拓扑枚举偷偷获得方向结论。

## 5. 完整性与 replay

每条 row 保存：

- `row_id`；
- `fact_hash`；
- `computation_hash`；
- source palace identity；
- source stem / source layer / context id；
- transformation type；
- target star identity；
- target palace identity；
- topology relation；
- assignment / mechanism / source refs。

sidecar 另外保存：

- source application bundle hash；
- source natal FactHash / ComputationHash；
- S08 transformation rule-set id / version；
- profile / algorithm identity；
- aggregate FactHash / ComputationHash / BundleHash；
- integrity report。

同一个已发布 application bundle 必须 full replay 得到完全相同的 topology sidecar。任何 source/target identity、分类关系、S08 lineage 或 hash 的静默变化都应导致完整性检查失败。

## 6. 联合 Workbench 产品边界

联合工作台通过：

`POST /api/ziwei-palace-stem-topology`

读取 sidecar。local controller 必须把 sidecar 的 `source_application_bundle_hash` 与本次 combined resolution 的精确 Ziwei bundle hash 绑定，不允许跨候选或跨盘复用。

浏览器实现位于：

- `src/fortune_training/combined_chart_application/palace_stem_topology_local_app.py`；
- `src/fortune_training/combined_chart_application/palace_stem_topology_assets.py`。

浏览器只能展示后端释放的：

- source palace / stem；
- transformation type；
- target star / branch；
- `SAME_PALACE / OPPOSITE_PALACE / OTHER_PALACE`；
- classification policy / selection semantics / semantic scope；
- source rule-set / source refs；
- FactHash / ComputationHash / BundleHash / integrity。

浏览器不得包含 S08 40 项分配表，不得自行执行 `+6 mod 12` 对宫算术，也不得生成 `OUTWARD_DISSIPATION / INWARD_RECEPTION` 或 `SELF_* / OPPOSITE_*` 方向标签。

Workbench 当前固定提示：

> 同宫 / 对宫 / 其他宫不等于离心 / 向心自化；方向未裁决，不作吉凶或事件解释。

## 7. Field Parity Matrix 状态

`docs/FUSION-CHART-FIELD-PARITY-MATRIX-R1.json` 当前必须同时保留两条不同状态：

1. `ZIWEI_PALACE_STEM_TRANSFORMATION_TOPOLOGY = ALREADY_VISIBLE`
   - 代表 48 条确定性目标拓扑已经由 engine/API 发布并进入 Workbench。
2. `ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION = NOT_YET_FORMALIZED`
   - 代表离心自化 / 向心自化方向 selector 仍没有满足 release 标准的 canonical mechanical contract。

这两个状态不矛盾。前者是**可见的几何事实**，后者是**尚未 formalize 的方向语义**。

不得因为拓扑已经可见，就把方向字段升级成 `ALREADY_VISIBLE` 或 `DISPUTED_CANDIDATE_ONLY`；只有在来源、selector、候选保持、hash/replay 与 fail-closed tests 全部完成后，才能改变该状态。

## 8. 后续 formalization 门槛

未来若继续开发离心自化 / 向心自化，至少需要同时满足：

1. 从 S08 或其他允许进入 canonical runtime 的来源恢复明确的机械 selector；
2. 明确 source palace、palace stem、transformed star、transformation type、direction、opposite palace、time layer 的事实结构；
3. 对有争议的 selector 保留 candidates，不自动选 winner；
4. 明确区分 `忌坐` 与 `忌冲`；
5. 与生年、宫干、大限、流年、流月等 transformation layer 共存，不覆盖既有事实；
6. 建立独立 FactHash / ComputationHash / BundleHash 与 replay；
7. 后端先发布，Workbench 只消费，不在浏览器重算。

在上述门槛满足之前，本 R1 只作为宫干四化目标拓扑产品层存在，不承担自化 / 向心化方向裁决。