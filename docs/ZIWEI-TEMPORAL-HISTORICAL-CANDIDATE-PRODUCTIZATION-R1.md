# Ziwei Temporal Historical Candidate Productization R1

Status: **CLOSED FOR SOURCE-SCOPED CANDIDATE OUTPUT / NO PRODUCTION WINNER CHANGE**

Baseline historical decomposition remains Batch 08B. The Zhongzhou leap-month daily-origin closure is updated forward-only by Batch 12OP.

- `HPA-ZTEMP-004` — 1581 《新刻纂集紫微斗数捷览》 day-anchored flow-hour candidate;
- `HPA-ZTEMP-006` / `HPA-ZT-015` — modern Zhongzhou leap-month month/day geometry, source-scoped and unselected.

This document records productization only; it does not create a new historical batch.\n\nThis document records the current product contract. Historical evidence claims remain in the audit batches and research records.

## 1. Shared candidate registry

```text
ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-API-R1@1.2.0
ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-REGISTRY-R1@1.1.0
ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-RUNTIME-R1@1.1.0
selection_status=PRESERVED_NOT_SELECTED
```

The registry still contains exactly two source-scoped method families: `JIELAN-1581-DAY-ANCHORED-FLOW-HOUR-R1` and `ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1`. The version bump adds no winner or third method; it extends the existing Zhongzhou candidate with source-closed daily geometry.

## 2. 1581 day-anchored flow hour

The Jielan mechanics are unchanged: Zi hour is anchored to the resolved flow-day active palace and later hours advance by hour-branch ordinal. Its parent daily frame remains time-standard-specific.

## 3. Zhongzhou leap-month month/day geometry

Direct Wang Tingzhi text plus the S10 collation close the source-scoped mechanics: days 1–15 use the preceding regular month; leap day 1 continues after that regular month's last flow day, so its 29/30-day length is explicit input; days 16–end use the following regular month's monthly active-palace basis; the actual leap-day ordinal is retained rather than renumbered at day 16.

The candidate emits backend-computed `leap_day_one_active_branch`, `daily_basis_branch`, `daily_active_address_branch`, `half_split_basis_switch=true`, and `half_split_reset=false`.

Ordinary released fields remain fail-closed:

```text
monthly_projection_status=LEAP_MONTH_UNRESOLVED_NO_FRAME
daily_projection_status=PARENT_LEAP_MONTH_UNRESOLVED_NO_FRAME
```

The complete Zhongzhou geometry is exposed only through `leap_month_method_candidates` as `PRESERVED_NOT_SELECTED`; it is not the universal production default.

## 4. Schema, replay and Workbench

The strict Shared Ziwei Selector Projection schema binds API/registry/runtime versions consistently for both methods. Workbench renders backend-returned assigned month, candidate flow-day palace, basis and switch/reset flags; browser code contains no branch-placement formula or winner selector.

## 5. Current audit accounting after Batch 12OP

```text
TOTAL_MATRIX_ROWS=222
AUDITED_ROWS=222
CUMULATIVE_IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CURRENT_MISSING_FROM_PRODUCT_ROWS=4
HISTORICAL_CANDIDATE_EXTENSION_COUNT=14
HISTORICAL_CANDIDATE_REGISTRY_COUNT=5
HISTORICAL_CANDIDATE_RUNTIME_RESOLVER_COUNT=5
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=44
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=44
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 6. Remaining boundaries

- other leap-month doctrines remain separate source/school questions;
- natal leap-month handling is not silently equated with flow-month/day handling;
- no historical winner is selected merely because this school-scoped candidate is mechanically complete;
- no prediction, ranking, 吉凶 or 应验 semantics are introduced.
