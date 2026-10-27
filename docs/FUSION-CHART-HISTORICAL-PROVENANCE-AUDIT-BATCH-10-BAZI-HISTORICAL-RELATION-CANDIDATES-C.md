# Fusion Chart Historical Provenance Audit R1 — Batch 10C

## Bazi source-scoped historical relation candidate runtime

Status: **PRODUCTIZED AS UNSELECTED SIDECAR / RAW CORE UNCHANGED / NO ALGORITHM REOPEN**

## 1. Runtime boundary

A new sidecar `BAZI-HISTORICAL-RELATION-CANDIDATES-R1` materializes source-closed relation candidates without mutating `BAZI-RAW-RELATION-CLASSICAL-CORE-R1`.

```text
SELECTION_STATUS=PRESERVED_NOT_SELECTED
HISTORICAL_CANDIDATE_REGISTRY_COUNT=2
HISTORICAL_CANDIDATE_RUNTIME_RESOLVER_COUNT=2
CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```

## 2. Productized candidate families

- `FOUR_EARTH_BUREAU`: 辰戌丑未土局, arity 4;
- `DIRECTIONAL_TRIAD`: the four 方/三会 directional triples, arity 3;
- `BRANCH_BREAK_EARLY_FOUR`: the four-pair 《五行精纪》/李虚中 method, arity 2;
- `STEM_HIDDEN_COMBINATION`: same-pillar visible stem with a hidden stem that matches the existing five-stem-combination registry.

Each output is a `RelationCandidate` carrying a separate rule-set ID, source refs and no automatic transformation permission.

## 3. Explicit exclusions

The sidecar does not emit:

- the later six-break additions 寅亥 / 巳申;
- modern half-trine or arched-trine relations;
- arbitrary cross-pillar visible-stem ↔ hidden-stem combinations;
- successful 化/成局 conclusions;
- strength, auspiciousness or event semantics.

## 4. Overlap is allowed without semantic collapse

A chart containing 辰戌丑未 can simultaneously contain the arity-4 four-earth bureau and source-supported early break pairs such as 丑辰 and 未戌. These are different mechanical relation facts and are not deduplicated merely because they share participants.

## 5. Provenance repair

`PROV-DEFECT-008` repaired the relation-chapter source scope for 《命理探源》. The previous Night-Zi source ID was unrelated to the cited relation passage. A dedicated `EXT-CTEXT-MINGLI-TANYUAN-RELATIONS` ID now binds both Matrix and runtime source refs.

## 6. Accounting

```text
TOTAL_MATRIX_ROWS=187
TOTAL_AUDITED_ROWS=154
HISTORICAL_CANDIDATE_EXTENSION_COUNT=4
HISTORICAL_CANDIDATE_REGISTRY_COUNT=2
HISTORICAL_CANDIDATE_RUNTIME_RESOLVER_COUNT=2
IDENTIFIED_MISSING_CANDIDATE_FAMILY_COUNT=12  # cumulative discoveries
CURRENT_MISSING_FROM_PRODUCT_ROWS=8
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=8
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=8
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```
