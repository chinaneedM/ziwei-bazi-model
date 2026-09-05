# Fusion Chart Historical Provenance Audit R1 — Batch 11C

## Bazi historical-calendar adapter contract

Status: **AUDITED / REGIME-SCOPED ADAPTER CONTRACT ADDED / CALENDAR ARITHMETIC STILL MISSING / NO ALGORITHM REOPEN**

Batch 11B established that `三命通会` contains real calendarization semantics for Jiaoyun. It did not authorize the repository's modern Chinese-calendar engine as an ancient calendar.

The received `三命通会` witness is Ming and the early extant print is dated 1578. Ming dynastic-history material records `大统历` as the official calendrical context and its relation to `授时历`. A separate institutional witness records the 1645 introduction of the Shixian calendar program. These are distinct regime contexts.

Batch 11C adds:

- `HISTORICAL-CHINESE-CALENDAR-ADAPTER-CONTRACT-R1`;
- `MING-DATONG-CALENDAR-CONTEXT-R1`;
- `QING-SHIXIAN-1645-CALENDAR-CONTEXT-R1`;
- `FailClosedHistoricalCalendarAdapter`.

The contract requires source/regime identity for historical date mapping, Jiaoyun realization and calendar-year recurrence. Until arithmetic is independently source-closed it returns `UNRESOLVED_NO_CERTIFIED_HISTORICAL_CALENDAR_ADAPTER`.

It prohibits modern Chinese-calendar fallback, implicit Gregorian anniversary substitution, cross-regime back-projection and implicit winner selection.

`HPA-DAYUN-CAL-002`, `003` and `004` all remain `MISSING_FROM_PRODUCT`.

```text
TOTAL_MATRIX_ROWS=197
TOTAL_AUDITED_ROWS=165
IDENTIFIED_MISSING_CANDIDATE_FAMILY_COUNT=13
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```

Next work is to source-close one concrete Ming Datong-period adapter with auditable month/leap arithmetic, day/time coordinate, enforcement scope and oracle cases. If that cannot be closed, the candidate remains fail-closed.
