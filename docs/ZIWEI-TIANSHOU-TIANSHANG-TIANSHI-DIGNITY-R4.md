# Ziwei TianShou / TianShang / TianShi Dignity R4

## Scope

This release closes the three physical-content objects deliberately left outside the legacy `WENMO_DEFAULT_MINOR_R1` v1.0.0 inventory:

- 天寿 (`STAR.TIANSHOU`)
- 天伤 (`STAR.TIANSHANG`)
- 天使 (`STAR.TIANSHI`)

The change is deterministic Ziwei Chart Engine V1 content work. It does not modify `sources/canonical/`, does not change `NatalChartState` or `DignityAnnotation` schemas, and does not add interpretation or prediction behavior.

## Authority boundary

Wenmo Tianji remains `EXTERNAL_COMPATIBILITY_ORACLE_NOT_CANONICAL_AUTHORITY`.

The external exports are used only to discriminate an operational compatibility profile and to calibrate the project-owned Dignity registry. They do not define canonical historical truth, ontology, schema, renderer layout or source-governance policy.

## Placement closure

### TianShou

The active source route uses Body palace as the 子-origin and advances by the birth-year branch offset. The 1992-06-10 14:00 discriminator has Life=亥, Body=丑, birth-year branch=申 and Wenmo displays 天寿@酉. Body-basis gives 酉 while Life-basis would give 未.

The operational Wenmo-default formula is therefore:

```text
TianShou = BodyAddress + BirthYearBranchIndex (mod 12)
```

### TianShang / TianShi

The source corpus preserves both a fixed traditional palace relation and an alternate yin/yang-sex swap family. The 1975-05-20 chart is an 乙卯 yin-year male, yet Wenmo still displays 天伤 in 交友 and 天使 in 疾厄. The Wenmo-default operational profile therefore selects the fixed family without erasing the alternate historical/profile variant.

```text
TianShang = Life + 5 = 交友
TianShi   = Life + 7 = 疾厄
```

## Minimal calibration closure

The prior 21 Wenmo 2.5.9 / API 1.1.2 / C5VUC exports already covered:

```text
天寿 12/12
天伤 10/12; missing 寅, 酉
天使 10/12; missing 辰, 亥
```

The four missing cells form two paired Life conditions, so two additional charts are both the theoretical lower bound and a sufficient closure pack.

### 2012-09-25 00:30

```text
Life = 酉
Body = 酉
天寿@丑 = 庙
天伤@寅 = 平
天使@辰 = 陷
```

### 2006-04-07 00:30

```text
Life = 辰
Body = 辰
天寿@寅 = 旺
天伤@酉 = 平
天使@亥 = 旺
```

After merging all 23 exports, the three entities are 36/36 reachable cells, all `GRADED`, with zero observed conflicts.

## Frozen R4 rows

Branch order is:

```text
子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥
```

Rows:

```text
STAR.TIANSHOU  平 庙 旺 陷 庙 平 平 旺 旺 平 庙 旺
STAR.TIANSHANG 陷 平 平 陷 平 平 陷 陷 平 平 平 旺
STAR.TIANSHI   陷 陷 平 平 陷 平 平 平 平 陷 陷 旺
```

Added-row matrix SHA256:

```text
5bac16b2f13d240f3adc7846a8aa45ce58f1c9bb2b89c6f7a450aef606b40e23
```

The hash is computed from sorted entity IDs and Z12 branch order using rows of the form:

```text
entity_id|branch|GRADED|grade
```

## Versioning and backward compatibility

The legacy R3 placement profile remains replayable and unchanged:

```text
WENMO_DEFAULT_MINOR_R1 v1.0.0
OPERATIONAL-ZIWEI-DIGNITY-R3 v3.0.0
```

R4 remains in the same operational minor-rule-set family but uses a new immutable content version:

```text
WENMO_DEFAULT_MINOR_R1 v2.0.0
OPERATIONAL-ZIWEI-DIGNITY-R4 v4.0.0
```

Profile validation binds R3 specifically to minor v1.0.0 and R4 specifically to minor v2.0.0. This prevents the three new physical placements from silently changing an already frozen R3 computation snapshot.

## Full R4 Dignity scope

R3 was:

```text
67 physical entities
681 reachable cells
589 GRADED
92 UNRATED
```

R4 adds three entities × twelve reachable branches:

```text
+3 entities
+36 reachable cells
+36 GRADED
+0 UNRATED
```

Therefore the R4 registry summary is:

```text
70 physical entities
717 reachable cells
625 GRADED
92 UNRATED
```

`UNRATED` retains its existing typed meaning: `status=UNRATED`, `grade=null`. It is not equivalent to 平, 不, unknown placement or missing evidence.

## Generator-domain invariant

The R4 tests do not accept a manually asserted count of 36. They enumerate the relevant generator inputs across birth-year branch, Life address and Body address, collect the reachable `(entity_id, branch)` pairs emitted by the three new placement rules, and require exact set equality with the R4 added registry.

Therefore the registry may neither omit a reachable cell nor invent an unreachable one.

## State and hash semantics

R4 reuses the existing generic paths:

```text
Placement
-> DignityAnnotation
-> Integrity
-> FactHash / ComputationHash
-> ChartViewModel / ViewHash
```

No schema mutation is required. A changed Dignity grade/status changes canonical fact state and therefore `FactHash`; provenance-only changes affect `ComputationHash` without rewriting the fact.

## Validation

Required repository checks remain:

```bash
fortune-train verify
python -m unittest discover -s tests -v
```

R4 regression specifically covers:

- exact 36-cell three-entity fixture/runtime equality;
- the frozen matrix SHA256;
- exact generator-derived reachable-domain equality;
- both minimal closure geometries;
- full 70-entity materialization and annotation;
- final 717 / 625 / 92 registry summary;
- R3 legacy profile replay;
- R4 rejection of legacy minor v1.0.0 binding.
