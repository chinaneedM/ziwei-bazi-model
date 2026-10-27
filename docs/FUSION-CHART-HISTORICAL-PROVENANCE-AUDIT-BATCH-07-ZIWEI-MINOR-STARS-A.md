# Fusion Chart Historical Provenance Audit R1 — Batch 07

## Ziwei minor-star decomposition A

Status: **AUDITED / GRANULARITY EXPANSION / NO ALGORITHM REOPEN**

Invariant states:

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```

## 1. Why the old bundle is not authoritative enough

`HPA-ZIWEI-008` originally represented the entire operational R4 minor-star
family. The runtime actually combines more than twenty independent placement
rules with different anchors:

- birth-year stem;
- birth-year branch;
- lunar month;
- birth hour;
- Life palace;
- Body palace;
- source-internal conflicts;
- Wenmo compatibility discriminators.

A single historical verdict for that bundle would be misleading. Batch 07 starts
a rule-family decomposition and audits eight high-value subfamilies.

The parent row remains an implementation-review summary until all children are
closed.

## 2. Received-Fullbook rules directly matching runtime

### 2.1 天哭 / 天虚

`S01:ZZQS-A-1886..1887`:

```text
天哭天虚起午宫，午宫起子两分踪。
哭逆巳兮虚顺未，数到生年便居中。
```

Runtime:

```text
天哭 = 午起子，逆数年支
天虚 = 午起子，顺数年支
```

Verdict: exact geometry match.

### 2.2 红鸾 / 天喜

`S01:ZZQS-A-1918..1919`:

```text
卯上起子逆数之，数到当生太岁支。
坐守此宫红鸾位，对宫天喜不差移。
```

Runtime uses `3-year_branch_ordinal` for 红鸾 and its opposite palace for
天喜. Exact match.

### 2.3 龙池 / 凤阁

`S01:ZZQS-A-1893`:

```text
龙池子顺辰，凤阁子戌逆。
```

Runtime uses 辰 as 子-year LongChi start and 戌 as Zi-year FengGe start,
advancing forward/reverse respectively. Exact match.

### 2.4 台辅 / 封诰

`S01:ZZQS-A-1899`:

```text
从午宫起子，顺数至本生时安之。
```

`S01:ZZQS-A-1905`:

```text
从寅宫起子，顺数至本生时安之。
```

Runtime places 台辅 from 午 and 封诰 from 寅 by birth-hour ordinal. Exact
match.

This is stronger provenance than the modern normalized `ZZZA-PR-045`
relationship description; runtime already cites the direct QQS atoms.

### 2.5 天刑 / 天姚

`S01:ZZQS-A-1872..1873`:

```text
天刑星从酉上起正月，顺至本生月安之。
天姚从丑上起正月，顺至本生月安之。
```

Runtime uses 酉/丑 as month-one anchors and advances by lunar-month ordinal.
The ordinary-month geometry matches exactly. Leap-month month-coordinate policy
remains a separate profile issue.

### 2.6 天德 / year-based 解神 → modern 年解 label

`S01:ZZQS-A-1943`:

```text
天德星从酉上起子，顺数至流年太岁上是也。
```

`S01:ZZQS-A-1945`:

```text
解神从戌上起子，逆数至当生年太岁上是也。
```

For natal birth-year use, the released coordinates reproduce these two
geometries:

```text
天德: 子年酉起顺行
年解: 子年戌起逆行
```

The important provenance point is naming: the received text calls the second
star `解神`, whereas the current product calls the year-anchored implementation
`年解` to distinguish it from a separate month-anchored `解神/月解` rule.

That label normalization is now explicit. It is not treated as evidence of a
different ancient geometric rule.

## 3. Two families remain genuinely disputed

### 3.1 天厨

S01 normalized route `ZZZA-PR-023` records the current stem table and
explicitly flags it as differing from a Fullbook table.

The operational product uses the Wenmo-compatible/Zhongzhou table:

```text
甲丁巳
乙戊辛午
丙子
己申
庚寅
壬酉
癸亥
```

Until both source tables are extracted and edition-bound, the correct audit state
is:

`DISPUTED_MULTIPLE_CANDIDATES`

No winner is inferred from product compatibility.

### 3.2 天寿

`ZZZA-PR-042` describes a Body-palace-based year-branch derivation but also
records a source-body/table-header basis conflict. R4 selects the Body-basis
candidate because the frozen Wenmo discriminator matches it.

This is a valid operational choice, not proof of unique classical authority.

Audit state:

`DISPUTED_MULTIPLE_CANDIDATES`

## 4. New granular Matrix rows

Batch 07 adds:

- `HPA-ZMINOR-001` 天哭 / 天虚;
- `HPA-ZMINOR-002` 红鸾 / 天喜;
- `HPA-ZMINOR-003` 龙池 / 凤阁;
- `HPA-ZMINOR-004` 台辅 / 封诰;
- `HPA-ZMINOR-005` 天刑 / 天姚;
- `HPA-ZMINOR-006` 天德 / year-based 解神（modern 年解）;
- `HPA-ZMINOR-007` 天厨 competing tables;
- `HPA-ZMINOR-008` 天寿 basis conflict.

The first six are source-closed enough to mark historically supported for their
placement geometry. The last two remain disputed candidates.

## 5. Product impact

No production result changes in Batch 07.

The improvement is epistemic and architectural:

- broad minor-star provenance is decomposed;
- direct received-text anchors replace bundle-level generalization;
- naming normalization is documented;
- known source conflicts are isolated instead of hidden inside
  `WENMO_DEFAULT_MINOR_R4`.

## 6. Batch verdict

```text
BATCH_07_ZIWEI_MINOR_STARS_A=AUDITED
NEW_GRANULAR_RULE_ROWS=8
NEW_AUDITED_ROWS=8
HISTORICALLY_SUPPORTED_CHILD_ROWS=6
DISPUTED_CHILD_ROWS=2
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
PRODUCTION_DEFAULT_CHANGE_COUNT=0
```

Part B should continue with 天官/天福、截空/旬空、天空、孤辰寡宿、劫煞、
大耗、蜚廉、破碎、华盖、咸池、龙德/月德、天才、解神/月解、天巫、
天月、阴煞 and the remaining basis-dependent minor stars.
