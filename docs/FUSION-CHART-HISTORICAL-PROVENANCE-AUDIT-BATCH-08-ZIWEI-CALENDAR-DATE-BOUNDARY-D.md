# Fusion Chart Historical Provenance Audit R1 — Batch 08D

## Ziwei calendar-date basis and late-Zi day boundary

Status: **AUDITED / TWO POLICY AXES DECOMPOSED / NO ALGORITHM REOPEN**

## 1. The key decomposition

Ziwei effective chart date currently composes two independent questions:

1. which Gregorian date is used to index the Chinese calendar;
2. whether Ziwei rolls the chart date at 23:00 or at midnight.

`LOCAL_SOLAR_DATE_INDEXED` is therefore not synonymous with `ZI_START_23`.

## 2. Date-index basis

- `LOCAL_SOLAR_DATE_INDEXED`: use local apparent-solar Gregorian date.
- `ABSOLUTE_CALENDAR`: use reported civil Gregorian date.

Both are modern operational candidates. No early Ziwei witness has been established for the repository's exact Gregorian-index abstraction.

## 3. Late-Zi boundary

Production selects `ZI_START_23`, but the S01 sentence attributed to 《紫微斗数全书》 remains under PROV-DEFECT-005 quarantine because edition-scoped verbatim support has not been closed.

Modern references explicitly preserve both current-day and next-day late-Zi methods. This proves the dispute exists; it does not prove an ancient winner.

Critically, 1581 Jielan `日上起子时` is a flow-hour palace instruction. It is not evidence that the calendar date rolls at 23:00.

## 4. Cross-system independence

The combined product already demonstrates independent day-boundary behavior. The same physical local-apparent-solar instant can use:

- Ziwei `ZI_START_23`;
- Bazi `MIDNIGHT`.

The frozen Ziwei V1 profile still carries Bazi policy fields inside a legacy shared `PolicySelection`, but combined Bazi execution uses its own Bazi profile. This is metadata/architecture debt, not a chart algorithm defect.

## 5. New rows

- HPA-ZDATE-001 local-solar date index;
- HPA-ZDATE-002 civil-date index;
- HPA-ZDATE-003 Ziwei 23:00 rollover;
- HPA-ZDATE-004 midnight/current-day late-Zi candidate;
- HPA-ZDATE-005 cross-system independence guard.

## 6. Accounting

```text
TOTAL_MATRIX_ROWS=166
TOTAL_AUDITED_ROWS=127
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
IDENTIFIED_MISSING_CANDIDATE_FAMILY_COUNT=8
```
