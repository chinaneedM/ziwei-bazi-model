# Historical Chinese Calendar Adapter Contract R1

## State

```text
HISTORICAL_CHINESE_CALENDAR_ADAPTER_CONTRACT_R1=DESIGNED
HISTORICAL_CALENDAR_ARITHMETIC_IMPLEMENTED=NO
HISTORICAL_CALENDAR_DEFAULT_WINNER=NONE
MODERN_CHINESE_CALENDAR_AS_HISTORICAL_AUTHORITY=FORBIDDEN
```

Batch 11B closed a historical Dayun calendarization rule family, not a historical calendar engine. R1 therefore creates a source/regime-scoped, fail-closed boundary before any classical Jiaoyun candidate can become executable.

The 1578 Ming `三命通会` witness is researched first against the Ming Datong calendar context. A distinct Qing Shixian context beginning in 1645 is recorded only as a regime boundary. Neither context is an executable historical calendar in R1.

A future concrete adapter must support, within one explicit source/regime/version:

1. civil/source date → historical lunisolar date mapping;
2. historical lunisolar realization of symbolic Dayun age;
3. calendar-year recurrence for later ten-year Dayun boundaries.

It must retain source references, supported period, leap/month arithmetic, day-boundary and clock assumptions, invalid-date policy and deterministic diagnostics.

R1 explicitly forbids:

- `MODERN-CHINESE-CALENDAR-ASTRONOMICAL-V1` as historical authority;
- cross-regime back-projection;
- implicit Gregorian anniversaries for classical candidates;
- winner selection from chronology alone;
- emitting a historical handover value while regime arithmetic remains uncertified.

`FailClosedHistoricalCalendarAdapter` therefore returns `UNRESOLVED_NO_CERTIFIED_HISTORICAL_CALENDAR_ADAPTER`.

Before a Ming implementation is permitted, research must source-close Datong/Shoushi-derived month and leap-month arithmetic for the target period, the historical date/clock coordinate, enforcement scope, reproducible almanac/oracle cases and invalid-date behavior.
