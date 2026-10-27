# Fusion Chart Historical Provenance Audit R1 — Batch 11A

## Bazi hidden-stem text order, normalized display order, and temporal hash semantics

Status: **AUDITED / ORDER DECOMPOSED FROM MEMBERSHIP / PROV-DEFECT-009 REPAIRED / NO CHART ALGORITHM REOPEN**

## 1. Membership and order are different claims

The received YHZP hidden-stem verse gives a stable membership set and also has
its own textual word order. For several multi-stem branches that textual order
differs from the repository tuple.

The historical membership verdict remains closed. Text order is preserved as
source lineage, not silently converted into a universal strength ranking.

## 2. Current registry order

The current `HIDDEN_STEMS` tuple is deterministic and intentionally says that
registry order is not a root-strength scale. Its exact genealogy is not
historically source-closed, so it remains a normalized display/lineage choice.

## 3. Later main-qi hierarchy

A received `子平真诠` passage explicitly says `辰本藏戊` and separately
identifies water storage and `乙余气`. This establishes later hierarchy language
for that example, but not a complete universal 12-branch ordinal table.

Therefore `registry_ordinal` is not renamed to 本气/中气/余气.

## 4. Dynamic-layer reuse

Dayun, Xiaoyun, annual, monthly, daily and hourly annotations reuse exactly the
same `HIDDEN_STEMS` membership registry. There is no second dynamic hidden-stem
doctrine.

`HPA-BAZI-FLOW-003` is therefore historically closed as registry reuse.

## 5. PROV-DEFECT-009

Before this batch, temporal annotation FactHash included display order and
`registry_ordinal`, while natal FactHash explicitly excluded them.

Forward-only repair:

```text
TEMPORAL_CLASSICAL_ANNOTATION_PROFILE_VERSION=1.0.2
TEMPORAL_CLASSICAL_ANNOTATION_HASH_VERSION=1.0.1
FACT_HASH_BINDS=HIDDEN_STEM_MEMBERSHIP_AND_SEMANTIC_BINDINGS
COMPUTATION_HASH_BINDS=HIDDEN_STEM_REGISTRY_ORDER
DISPLAY_ORDER_CHANGE_DOES_NOT_CHANGE_FACT_IDENTITY=YES
MEMBERSHIP_CHANGE_STILL_CHANGES_FACT_IDENTITY=YES
```

No four-pillar, hidden-stem membership, Ten-God, relation or temporal coordinate
algorithm changed.

## 6. Accounting

```text
TOTAL_MATRIX_ROWS=190
TOTAL_AUDITED_ROWS=158
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=9
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=9
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```
