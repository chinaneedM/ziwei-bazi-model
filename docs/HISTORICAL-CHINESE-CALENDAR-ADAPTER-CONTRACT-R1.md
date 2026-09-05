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

## Batch 11D source-closure update

The evidence stack is now narrower and stronger, but still non-executable:

- `EXT-KOTENMON-DAMING-DATONG-1569` is a Ming-period facsimile witness of Zhou Xiang's `《大明大統曆法》`; its preface and `步氣朔` volume provide a primary method target for arithmetic collation.
- `EXT-NCL-DATONG-1578-ALMANAC` identifies an exact 1578 `明欽天監刊本` official almanac, matching the `《三命通會》` publication-year context.
- `EXT-IHNS-MING-DATONG-COMPILATION-2019` requires us to treat the later `《明史·曆志》` redaction as contextual/received evidence rather than silently using it as the Ming official computational edition.

This does **not** certify arithmetic. The exact 1578 month-start, leap-month and time oracle values have not yet been extracted and replayed against the 1569 method witness, and clock/enforcement/invalid-date semantics remain open. `FailClosedHistoricalCalendarAdapter` therefore remains mandatory.

