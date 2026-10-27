# Batch 12DP — 大統 C-II-N 49–58 整刻跨越閉合 × 授時/大統氣策節氣偏移重放

## Status

```text
CII_N_49_TO_58_EXACT_CROSSINGS=CLOSED
CII_N_42_TO_58_CONSECUTIVE_THRESHOLD_SERIES=CLOSED
INTERIOR_THRESHOLD_BEHAVIOR=STRONG_WHOLE_INTEGER_COMPATIBILITY
SHOUSHI_DATONG_QICE_OFFSET_REPLAY=CLOSED_AT_RECEIVED_CALENDAR_COORDINATE_LEVEL
LEIJING_1624_TRANSITION_ALIGNMENT=ALL_42_TO_58_WITHIN_0_5291_DAY_UNDER_PRESERVED_COUNTING_AMBIGUITY
COUNTING_CONVENTION=UNRESOLVED_PRESERVE_ELAPSED_AND_ORDINAL_CANDIDATES
BATCH12CG_DAY89_INDEX=FORWARD_ONLY_CORRECTED
UNIVERSAL_FLOOR_RULE=NOT_PROVED
SUMMER_59_ENDPOINT=REQUIRES_SEPARATE_HANDLING
SANMING_YUELING_EXACT_FINGERPRINT=UNRESOLVED_SEPARATE_BRANCH
PRE1578_EXACT_REDUCTION_RULE=UNRESOLVED
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NO
```

## 1. Why this batch

12DO 已把同一 NCL-06267《大統日出分》物理对象的 42–48 整刻跨越逐格闭合，并留下两个明确门槛：继续直接重校 49–58，以及把后出 1624《類經圖翼》的整刻换档标记放回真实节气积日坐标，而不是用每气恰好 15 日的现代简化近似。本批只处理这两个门槛，并继续把“后出机械同构”与“1578 前直接祖本”严格分开。

## 2. C-II-N 49–58 直接无 OCR 核读

来源不变：workflow `34869676923` / artifact `10358685142` / NCL-06267。源 PDF SHA-256：

```text
0d3ed2b54f92b5eb2f11e5d06babebcc177e04ec5b8c7168b56f1fb25f94797d
```

最终数字全部来自归档页图的直接列对齐核读，不以 OCR 为数值或字形权威。换算仍为：

```text
full_daylight_ke = 2 * half_day_fen / 100
```

| 整刻 | 下界日 / 晝刻 | 上界日 / 晝刻 | 首个越过整数的日 |
| --- | --- | --- | --- |
| 49 | d81 = 48.9632 | d82 = 49.0948 | 82 |
| 50 | d88 = 49.8808 | d89 = 50.0122 | 89 |
| 51 | d96 = 50.9242 | d97 = 51.0548 | 97 |
| 52 | d104 = 51.9662 | d105 = 52.0964 | 105 |
| 53 | d111 = 52.8754 | d112 = 53.0048 | 112 |
| 54 | d119 = 53.9018 | d120 = 54.0282 | 120 |
| 55 | d127 = 54.8950 | d128 = 55.0154 | 128 |
| 56 | d136 = 55.9236 | d137 = 56.0270 | 137 |
| 57 | d146 = 56.9424 | d147 = 57.0322 | 147 |
| 58 | d160 = 57.9862 | d161 = 58.0424 | 161 |

于是 49–58 的首跨日为：

```text
49→d82, 50→d89, 51→d97, 52→d105, 53→d112,
54→d120, 55→d128, 56→d137, 57→d147, 58→d161
```

与 12DO 合并后，42–58 共 **17 个连续整数阈值**全部由相邻物理表日列直接闭合。

## 3. 第三个 12CG 前向索引修正

12CG 的探索性重放曾把 `2494.04` 标成 day89，且明确标注为 `DIRECT_VISUAL_APPROX`。本批直接列对齐得到：

```text
day88 = 2494.04 -> 49.8808 ke
day89 = 2500.61 -> 50.0122 ke
```

因此旧记录仅在精确日序索引意义上标记为 `SUPERSEDED_FOR_EXACT_DAY_INDEXING_ONLY`。12CG 原文件不回写，宏观“C-II-N 连续曲线覆盖整刻梯级”结论不变。这与 12DN、12DO 的前两次精确日序修正采用同一 forward-only 规则。

## 4. 42–58 内部阈值现已形成连续实物序列

合并后的首跨日序列为：

```text
42→21, 43→34, 44→43, 45→51, 46→59, 47→67, 48→74,
49→82, 50→89, 51→97, 52→105, 53→112, 54→120,
55→128, 56→137, 57→147, 58→161
```

每一个内部整数都表现为“前一日低于整数、后一日达到或越过整数”。这把 12DO 的七个连续阈值扩展为十七个连续阈值，显著增强“连续南京/大統日长曲线 + 整刻阈值层”的机械解释。

但夏至防火墙完全不变：

```text
C-II-N day182 half-day = 2931.66
full daylight = 58.6332 ke
received endpoint = 59/41
```

所以仍禁止把内部兼容性升级为全域 `floor()`、单一截尾或任何未经文本证明的现代取整函数。

## 5. 授時/大統气策：把节气放回真实积日坐标

本批新增 received-text 坐标控制：《元史》卷54《授時曆經上·步氣朔第一》保存：

```text
氣策，十五日二千一百八十四分三十七秒半
```

按同一日周一万单位，即：

```text
qice = 15.2184375 days
```

并保存“置天正冬至日分，以氣策累加之”以求次气的累加方法。《明史·曆志》大統历 received context继续作为 Ming/Datong 交叉控制。这里的用途仅是建立历史节气坐标；它不等于取得了一个 1578 前目标物理祖本。

从冬至起累加所得关键节气偏移为：

```text
小寒 15.2184375
大寒 30.4368750
立春 45.6553125
雨水 60.8737500
驚蟄 76.0921875
春分 91.3106250
清明 106.5290625
穀雨 121.7475000
立夏 136.9659375
小滿 152.1843750
芒種 167.4028125
夏至 182.6212500
```

## 6. 1624《類經圖翼》完整 42–58 换档重放

12DN/12DO 只登记了前段代表性锚点。本批把 received text 中一直到 58 刻的换档标记完整重放。对于“後六日 / 後十三日”等表达，古代“经过 N 日”与“第 N 日”可能产生一日索引差；本批**不为了拟合而选择训诂赢家**，而是同时保留：

- elapsed-day candidate = 节气积日 + N；
- ordinal-day candidate = 节气积日 + N - 1。

下表的 “nearest” 只用于量化兼容性，不是历史读法裁决：

| 晝刻 | 1624 received marker | C-II-N 首跨日 | 两种候选坐标 | nearest | signed residual (day) |
| --- | --- | ---: | --- | --- | ---: |
| 42 | 小寒後六日 | d21 | elapsed_day_count=21.2184375; ordinal_day_count=20.2184375 | ELAPSED_DAY_COUNT | -0.2184375 |
| 43 | 大寒後四日 | d34 | elapsed_day_count=34.436875; ordinal_day_count=33.436875 | ELAPSED_DAY_COUNT | -0.4368750 |
| 44 | 大寒後十三日 | d43 | elapsed_day_count=43.436875; ordinal_day_count=42.436875 | ELAPSED_DAY_COUNT | -0.4368750 |
| 45 | 立春後六日 | d51 | elapsed_day_count=51.6553125; ordinal_day_count=50.6553125 | ORDINAL_DAY_COUNT | +0.3446875 |
| 46 | 立春後十三日 | d59 | elapsed_day_count=58.6553125; ordinal_day_count=57.6553125 | ELAPSED_DAY_COUNT | +0.3446875 |
| 47 | 雨水後六日 | d67 | elapsed_day_count=66.87375; ordinal_day_count=65.87375 | ELAPSED_DAY_COUNT | +0.1262500 |
| 48 | 雨水後十三日 | d74 | elapsed_day_count=73.87375; ordinal_day_count=72.87375 | ELAPSED_DAY_COUNT | +0.1262500 |
| 49 | 驚蟄後六日 | d82 | elapsed_day_count=82.0921875; ordinal_day_count=81.0921875 | ELAPSED_DAY_COUNT | -0.0921875 |
| 50 | 驚蟄後十四日 | d89 | elapsed_day_count=90.0921875; ordinal_day_count=89.0921875 | ORDINAL_DAY_COUNT | -0.0921875 |
| 51 | 春分後七日 | d97 | elapsed_day_count=98.310625; ordinal_day_count=97.310625 | ORDINAL_DAY_COUNT | -0.3106250 |
| 52 | 春分後十五日 | d105 | elapsed_day_count=106.310625; ordinal_day_count=105.310625 | ORDINAL_DAY_COUNT | -0.3106250 |
| 53 | 清明後七日 | d112 | elapsed_day_count=113.5290625; ordinal_day_count=112.5290625 | ORDINAL_DAY_COUNT | -0.5290625 |
| 54 | 清明後十五日 | d120 | elapsed_day_count=121.5290625; ordinal_day_count=120.5290625 | ORDINAL_DAY_COUNT | -0.5290625 |
| 55 | 穀雨後七日 | d128 | elapsed_day_count=128.7475; ordinal_day_count=127.7475 | ORDINAL_DAY_COUNT | +0.2525000 |
| 56 | 立夏 | d137 | solar_term_anchor=136.9659375 | SOLAR_TERM_ANCHOR | +0.0340625 |
| 57 | 立夏後十一日 | d147 | elapsed_day_count=147.9659375; ordinal_day_count=146.9659375 | ORDINAL_DAY_COUNT | +0.0340625 |
| 58 | 小滿後十日 | d161 | elapsed_day_count=162.184375; ordinal_day_count=161.184375 | ORDINAL_DAY_COUNT | -0.1843750 |

全部 42–58 换档的最小候选残差均小于 0.53 日，最大绝对残差为：

```text
0.5290625 day
```

这是一项很强的机械同构结果：C-II-N 的连续数值阈值与后出 1624 整刻换档表，在历史气策坐标下可以逐项对齐到半日量级。

但三道防火墙必须同时保留：

1. 1624 晚于 1578，不能反投为《三命通會》的直接祖本；
2. elapsed/ordinal 两种日序训诂尚未裁决，不能从“更接近”反推古人一定采用某一种；
3. 1578/1589 的 `雨水後四日 -> 48/52` 仍与这条干净支路不同，不得合并。

## 7. Genealogy consequence

本批新增/强化一个历史坐标控制节点：

- `RULE-SHOUSHI-DATONG-QICE-15_2184375`

并前向强化 `TG-E0054`：

```text
TABLE-NANJING-DATONG-DAILY-CII-N-1380S
  -- STRUCTURAL_MECHANISM_CANDIDATE_FOR -->
TABLE-FAMILY-POST1578-NANJING-59-41-STEPPED
```

其证据范围从 42–48 七个内部跨越扩大为 42–58 十七个连续跨越，并加入气策积日下的完整换档重放。状态仍为 `PROBABLE`，因为 chronology、夏至端点与 Sanming/Yueling 异常指纹都没有闭合。

对“1578 前精确 Sanming 父本”的文字/数值投票增量仍为 **0**。

## 8. Product adjudication

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=12
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=12
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

没有新增 runtime candidate，没有 winner，没有 candidate collapse，也不重新打开排盘算法。

## 9. Next gate

下一步应把搜索进一步收窄到：

1. **1578 前中国本土的南京/大統整刻 reduction/selection rule**，尤其是能解释 59 刻夏至端点而不是只解释 42–58 内部阈值的规则；
2. 优先寻找能同时复现 Sanming/Yueling 大寒/雨水特殊换档日的前出通书、历书、漏刻/改箭或官历文本；
3. 继续搜索独立中国本土 C-II-N/晨昏立成物理载体，以减少对朝鲜传本与后出 received control 的谱系依赖；
4. NLC call 14202 复制服务路线继续并行，但仍不提交需要用户身份、费用或馆方授权的外部请求。

Research record: `docs/research/ZIWEI-DATONG-CIIN-49-58-CROSSING-AND-QICE-OFFSET-REPLAY-R1.json`.
