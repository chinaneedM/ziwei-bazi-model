# Fusion Chart Historical Provenance Audit R1 — Batch 07B

## Ziwei minor-star early-print closure

Status: **AUDITED / EARLY-PRINT RULE DECOMPOSITION / NO ALGORITHM REOPEN**

Invariant states:

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```

## 1. Evidence boundary

This batch continues the granular decomposition begun in Batch 07A. It does not
treat S00–S19 as historical authority and does not infer authority from Wenmo
compatibility.

The rule-text witness is `EXT-ZIWEI-JIELAN-1581`, the project registry entry
for the chapter-scoped transcription of 《新刻纂集紫微斗数捷览》. Its edition
identity is independently corroborated by
`EXT-SHANGHAI-LIB-JIELAN-1581`: 上海图书馆古籍联合目录 子4051,
明万历九年金陵书坊王洛川刻本.

This distinction matters: the web transcription is used to collate mechanical
rule text; the library record verifies bibliographic identity. The library
catalog is not itself rule text, and this batch does not claim facsimile-level
character criticism where no scan was inspected.

## 2. Closed rule families

### 2.1 天官 / 天福

Jielan chapters 37 and 38 both anchor the stars to the birth-year heavenly stem
and enumerate the same ten-stem tables currently implemented by
`TIANGUAN_TIANFU_BY_STEM`.

Verdict: **exact table match**.

### 2.2 天空

Chapter 39 places 天空 one palace ahead of the birth-year 太岁 position.
The runtime uses `year_branch_index + 1`.

Verdict: **exact geometry match**.

### 2.3 旬中空亡

Chapter 40 gives the six ten-year xun void pairs:

- 甲子旬 → 戌亥;
- 甲戌旬 → 申酉;
- 甲申旬 → 午未;
- 甲午旬 → 辰巳;
- 甲辰旬 → 寅卯;
- 甲寅旬 → 子丑.

The runtime derives the same pair mechanically from the sexagenary index.

Important scope boundary: the 1581 chapter establishes the **two void
palaces**, not the product's later main/sub display ordering by stem yin/yang.
That display convention remains separately auditable and is not upgraded to an
early-print rule by this batch.

Verdict: **pair geometry historically supported; display ordering remains
profile-scoped**.

### 2.4 截路空亡 / 截空

Chapter 41 gives the same five stem-pair families used by
`JIEKONG_PAIR_BY_STEM` and explicitly distinguishes 正空/傍空 with 甲 and 己
examples. The runtime's primary/secondary selection reproduces those examples.

Verdict: **exact pair and ordering match**.

### 2.5 孤辰 / 寡宿

Chapter 43 groups birth-year branches into the same four seasonal triples used
by `GUCHEN_GUASU_BY_BRANCH`.

Verdict: **exact four-group table match**.

### 2.6 劫煞

Chapter 44 gives:

- 申子辰 → 巳;
- 亥卯未 → 申;
- 寅午戌 → 亥;
- 巳酉丑 → 寅.

This is exactly `JIESHA_BY_BRANCH`. Historical 杀 and product 煞 are retained
as an orthographic/name normalization, not a different coordinate rule.

Verdict: **exact table match**.

### 2.7 华盖

Chapter 45 gives the same four trine-group targets as
`HUAGAI_BY_BRANCH`.

Verdict: **exact table match**.

### 2.8 桃花杀 → current 咸池 label

Chapter 46 places the year-branch trine groups at 卯、酉、子、午 exactly as
`XIANCHI_BY_BRANCH`.

The early-print chapter calls the rule 桃花杀; the current product calls the
same geometry 咸池. Batch 07B records this as an explicit naming bridge instead
of silently claiming that the 1581 heading already used the product label.

Verdict: **geometry supported; historical naming bridge explicit**.

### 2.9 大耗

Chapter 47 gives six reciprocal birth-year pairs: 子未、丑午、寅酉、卯申、
辰亥、巳戌. The current formula starts from the opposing palace and shifts one
palace according to the sexagenary year's yin/yang. Because stem and branch
yin/yang are paired in a valid sexagenary year, the formula reduces to the same
twelve-branch table.

Verdict: **mechanically equivalent exact match**.

### 2.10 破碎

Chapter 48 gives three groups:

- 子午卯酉 → 巳;
- 寅申巳亥 → 酉;
- 辰戌丑未 → 丑.

This is exactly `POSUI_BY_BRANCH`.

Verdict: **exact table match**.

### 2.11 天才

Chapter 35 says to treat the Life palace as the 子-year position and advance by
birth-year branch. Its 丑-year example moves one palace forward from Life.

The runtime `life_index + year_branch_offset` is the same rule.

Verdict: **exact Life-basis geometry match**.

This closure is deliberately independent of 天寿. The TianShou Body/Life-basis
conflict remains `DISPUTED_MULTIPLE_CANDIDATES` under HPA-ZMINOR-008.

## 3. New granular Matrix rows

Batch 07B adds:

- `HPA-ZMINOR-009` 天官 / 天福;
- `HPA-ZMINOR-010` 天空;
- `HPA-ZMINOR-011` 旬中空亡 pair geometry;
- `HPA-ZMINOR-012` 截路空亡 / 截空;
- `HPA-ZMINOR-013` 孤辰 / 寡宿;
- `HPA-ZMINOR-014` 劫煞;
- `HPA-ZMINOR-015` 华盖;
- `HPA-ZMINOR-016` 桃花杀 → 咸池 geometry/name bridge;
- `HPA-ZMINOR-017` 大耗;
- `HPA-ZMINOR-018` 破碎;
- `HPA-ZMINOR-019` 天才.

All eleven rows are scoped `HISTORICALLY_SUPPORTED` for the placement claim
stated in the row. None authorizes an algorithm reopen.

## 4. Product impact

No production coordinate changes are required. The current runtime already
matches the scoped early-print mechanics.

The change is provenance precision:

- eleven independent rules leave the broad R4 bundle;
- 1581 chapter identities are bound to current mechanics;
- naming normalization is explicit where historical and product labels differ;
- the XunKong display-order claim is kept narrower than the void-pair claim;
- TianShou remains disputed rather than being accidentally closed by the nearby
  TianCai text.

## 5. Batch verdict

```text
BATCH_07B_ZIWEI_MINOR_STARS_EARLY_PRINT=AUDITED
NEW_GRANULAR_RULE_ROWS=11
NEW_AUDITED_ROWS=11
HISTORICALLY_SUPPORTED_CHILD_ROWS=11
TOTAL_MATRIX_ROWS=138
TOTAL_AUDITED_ROWS=88
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
PRODUCTION_DEFAULT_CHANGE_COUNT=0
```

The next minor-star pass should prioritize 蜚廉、龙德/月德、月解/解神、
天巫、天月、阴煞 and any remaining source-basis conflicts. Each should remain
a separate rule family rather than being closed by analogy.
