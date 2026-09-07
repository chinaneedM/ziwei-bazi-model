# Ziwei Temporal Historical Candidate Productization R1

Status: **CLOSED FOR SOURCE-SCOPED CANDIDATE OUTPUT / NO PRODUCTION WINNER CHANGE**

Historical authority remains Batch 08B:

- `HPA-ZTEMP-004` — 1581 《新刻纂集紫微斗数捷览》 `日上起子时皆顺行`;
- `HPA-ZTEMP-006` — Zhongzhou leap-month half split, `S10:ZZTERM-P-0280..0281`.

This document records productization only. It is not a new historical-evidence batch.

## 1. Shared candidate registry

The two methods are registered under:

```text
ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-REGISTRY-R1@1.0.0
selection_status=PRESERVED_NOT_SELECTED
runtime_resolver=ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-RUNTIME-R1@1.0.0
```

The registry contains exactly two source-scoped method families:

1. `JIELAN-1581-DAY-ANCHORED-FLOW-HOUR-R1`;
2. `ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1`.

They are candidates, not production defaults and not a ranked list.

## 2. 1581 day-anchored flow hour

Mechanical rule:

```text
Zi-hour active palace = current flow-day active palace
later hour active palace = parent flow-day palace + hour-branch ordinal
```

The resolver requires a parent daily frame whose effective Gregorian date matches the **same** time-standard clock and the current Ziwei calendar-date/day-boundary policies.

This prevents an invalid shortcut where Luoyang mean-solar time and local-apparent-solar time reuse one daily parent when their effective dates differ.

The early-print source authorizes the active-palace geometry only. It does **not** authorize either modern time standard, a 23:00 date boundary, or Zhongzhou dynamic auxiliary/four-transformation projection. Those remain separate axes.

The existing fixed-branch case candidates remain unchanged in `hourly_method_candidates`. The early-print candidates are emitted separately in `historical_hourly_method_candidates`.

## 3. Zhongzhou leap-month half split

Direct source scope closes:

- leap days 1–15 belong to the previous regular month and use that month Ganzhi;
- leap days 16–end belong to the following regular month and use that month Ganzhi;
- the flow-day sequence does not reset at the 15/16 split.

The source sentence does **not**, by itself, close whether leap-month day 1 restarts from a month palace or continues from the preceding regular month's final day.

Therefore the candidate deliberately records:

```text
half_split_reset=false
daily_active_address_emitted=false
daily_origin_semantics=NOT_CLOSED_BY_THIS_MONTH_POLICY_API
```

Existing projection fields remain fail-closed for a leap target:

```text
monthly_projection_status=LEAP_MONTH_UNRESOLVED_NO_FRAME
daily_projection_status=PARENT_LEAP_MONTH_UNRESOLVED_NO_FRAME
```

The school candidate is emitted separately through `leap_month_method_candidates`.

## 4. Hash, schema and replay

Both candidate payloads bind:

- registry ID/version/hash;
- runtime-resolver ID/version;
- method/source/authority identity;
- `PRESERVED_NOT_SELECTED`;
- candidate hash.

The Shared Ziwei Selector Projection R1 schema remains strict with `additionalProperties=false` for the new nested candidates.

The shared candidate hash includes both new candidate arrays and statuses. Structural integrity reconstructs them independently, and full replay compares the complete projection object.

The Workbench is read-only: it renders returned candidate fields and contains no branch/hour/month placement formula.

## 5. Audit accounting

The historical sources were already audited, so the audited row count remains unchanged.

```text
TOTAL_MATRIX_ROWS=197
AUDITED_ROWS=165
CUMULATIVE_IDENTIFIED_MISSING_CANDIDATE_FAMILIES=13
CURRENT_MISSING_FROM_PRODUCT_ROWS=9
HISTORICAL_CANDIDATE_EXTENSION_COUNT=6
HISTORICAL_CANDIDATE_REGISTRY_COUNT=3
HISTORICAL_CANDIDATE_RUNTIME_RESOLVER_COUNT=3
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

The cumulative discovery count remains 13 by definition; productizing two previously discovered gaps reduces the current `MISSING_FROM_PRODUCT` row count from 11 to 9 rather than rewriting discovery history.

## 6. Remaining research boundaries

- continue edition/facsimile research for Ziwei late-Zi doctrine independently of the 1581 flow-hour wording;
- continue Zhongzhou and competing-school research for leap-month day-one flow-day origin before emitting a daily active palace;
- do not collapse the 1581 day-anchored method with the fixed-branch case method;
- do not select a winner merely because candidates share an output in some timestamps;
- no prediction, ranking, 吉凶 or 应验 semantics are introduced.
