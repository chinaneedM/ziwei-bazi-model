# Historical Provenance Audit R1 — Batch 04: Ziwei Early-Print Core

## State

```text
BATCH_ID=BATCH-04-ZIWEI-EARLY-PRINT-CORE
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
CUMULATIVE_AUDITED_ROW_COUNT=54
MATRIX_ROW_COUNT=116
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=3
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=3
ALGORITHM_REOPEN_COUNT=0
HISTORICAL_CANDIDATE_REGISTRY_COUNT=1
IDENTIFIED_MISSING_CANDIDATE_FAMILY_COUNT=5
```

## Primary witness

This batch adds `EXT-ZIWEI-JIELAN-1581`: the extant Ming Wanli 9 (1581) `新刻纂集紫微斗数捷览`, described bibliographically as the Jinling Wang-shi Luochuan print and used through chapter-level digitized transcriptions.

The audit does not infer Song authorship from the traditional title attribution. Historical authority is attached to the **1581 extant print witness**, not to the legendary attribution.

## 1. Four Transformations

The current `S08_CURRENT_40_ASSIGNMENT_R1` table matches the 1581 `安禄权科忌四化诀` across all ten stems / forty assignments.

This materially strengthens current S08 provenance: it is not merely a modern software convention.

However, received `紫微斗数全书` and later school tables preserve competing cells. Therefore:

- current S08 remains valid and historically supported;
- competing tables must become separate immutable profiles;
- no hybrid table may be assembled by choosing preferred cells from different schools.

## 2. Kui/Yue

The 1581 `安天魁天钺诀` groups 庚辛 at 午/寅. The current QS/received family instead places 庚 with 甲戊 at 丑/未, while Wenmo has an additional Xin-order discriminator.

This is a real output-changing historical variant. It is now preserved in:

`ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATES-R1@1.0.0`

but remains `PRESERVED_NOT_SELECTED`.

## 3. Fire/Bell

The 1581 `安火铃星诀` explicitly gives:

```text
巳酉丑 -> 子时起 火戌 / 铃卯
```

and the same chapter records the received-Fullbook alternate:

```text
巳酉丑 -> 火卯 / 铃戌
```

Current production follows the latter/Wenmo-compatible family. The 1581 family is now preserved as an unselected historical candidate. This is not treated as a production defect because production already has an explicit compatibility identity; it is a missing school candidate.

## 4. TianShang / TianShi

The fixed R4 geometry is older than its compatibility discriminator. The 1581 text gives the Life-palace-relative rule and an example equivalent to:

```text
Life=寅 -> 天伤=未 / 天使=酉
```

which is exactly the repository's `life+5 / life+7` geometry.

Therefore the fixed method is historically supported. Wenmo is a compatibility witness, not the origin of the rule. A later sex-dependent swap family remains a separate competing method.

## 5. Main stars and core auxiliaries

The 1581 `安紫微天府诀` and `布南北二斗诸星诀` directly support:

- Ziwei/Tianfu relationship;
- north/south dipper main-star sequences;
- Fu/Bi month geometry;
- Chang/Qu hour geometry;
- DiKong/DiJie hour geometry.

These base geometries match the current source-bound implementation.

## 6. Five-bureau Changsheng ring

The 1581 `定五局长生例` exactly supports:

- 金局巳;
- 木局亥;
- 火局寅;
- 水土局申;
- 阳男阴女顺 / 阴男阳女逆.

The current ring geometry matches. Its `WENMO_DEFAULT_RING_R1` production name must not be read as historical origin.

## 7. Dignity / 庙旺落陷

The 1581 print contains explicit palace-by-star dignity rules. The current R4 dignity registry is intentionally project-owned / calibration-backed and already declines classical-source authority. Cell-level comparison confirms that it is **not** a replay of the 1581 table.

The 1581 dignity source is therefore registered as:

`SOURCE_TABLE_PRESENT_NORMALIZATION_PENDING`

rather than being forced into the modern seven-grade scale. Edition collation is required before a source-faithful runtime historical dignity profile is created.

## Governance result

```text
CURRENT_S08_FOUR_TRANSFORMATIONS=HISTORICALLY_SUPPORTED
CURRENT_FIXED_TIANSHANG_TIANSHI=HISTORICALLY_SUPPORTED
CURRENT_MAIN_STAR_SEQUENCE=HISTORICALLY_SUPPORTED
CURRENT_CHANGSHENG_RING=HISTORICALLY_SUPPORTED
CURRENT_OPERATIONAL_DIGNITY=MODERN_COMPATIBILITY_ONLY
JIELAN_1581_KUI_YUE=MISSING_FROM_RUNTIME_PRODUCT
JIELAN_1581_FIRE_BELL=MISSING_FROM_RUNTIME_PRODUCT
JIELAN_1581_DIGNITY=MISSING_FROM_RUNTIME_PRODUCT
COMPETING_FOUR_TRANSFORMATION_TABLES=MISSING_FROM_RUNTIME_PRODUCT
```

No closed chart algorithm is reopened by Batch 04.
