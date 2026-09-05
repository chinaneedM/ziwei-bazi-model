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

## Batch 11E target-year oracle update

The 1578 target-year **month-start oracle layer** is now machine-auditable without promoting it into calendar arithmetic.

`tests/fixtures/ming-datong-1578-month-start-oracle-r1.json` records the complete Wanli-6 month-start Ganzhi chain from official reign records and the next-year first-month anchor. The resulting 29/30-day transitions, 354-day total and represented non-leap structure are recomputed in tests rather than trusted as prose.

This closes only one evidence gate. It does **not** establish that the repository can generate those values from the 1569 Datong method, and it does not replace page-level collation of the exact 1578 `明欽天監刊本`.

The remaining adapter gates are:

1. edition-scoped replay of the 1569 `步氣朔` / month-new-moon arithmetic against the 1578 fixture;
2. page-level confirmation from the exact 1578 official almanac or an independently equivalent facsimile;
3. historical day boundary / clock coordinate;
4. enforcement and geographic/institutional scope;
5. invalid-date and month-length behavior required by Jiaoyun realization;
6. multi-year generalization and ten-year recurrence under the same historical regime.

`FailClosedHistoricalCalendarAdapter` remains mandatory until these are source-closed and replayed.
## Batch 11F conjunction-method adjudication

The D1/D2 conflict is no longer treated as an unresolved tie.

Primary and near-contemporary evidence converges on D1:

- the 1569 Zhou Xiang facsimile's `推加减差分法` divides by the corresponding lunar `迟/疾行度`;
- Xing Yunlu's Ming worked Datong example for Wanli 24 independently divides the correction by `迟行度`;
- 56 conjunction-time entries from six surviving official Ming Datong almanacs are reported to agree with D1, while most D2 values do not and one near-midnight D2 result crosses to the wrong day.

The Qing-compiled `《明史》` received text instead gives the later `定限度` denominator (D2). Batch 11F therefore classifies D2 as a received transmission variant rather than an equal Ming production candidate.

MING_DATONG_CONJUNCTION_METHOD_HISTORICAL_ADJUDICATION=D1_SHOUSHI_STYLE_CHIJIXINGDU
D2_DISPOSITION=LATER_RECEIVED_TEXT_VARIANT_NOT_EQUAL_PRODUCTION_CANDIDATE
RUNTIME_SELECTION_AUTHORIZED=NO

This historical subrule adjudication does **not** certify a full historical calendar adapter. The remaining gates are complete 1569 table/carry and interpolation transcription, source-derived replay to the 1578 oracle, page-level confirmation from the exact 1578 Qintianjian almanac, historical clock/day-boundary semantics, invalid-date behavior, leap-month generalization and same-regime ten-year recurrence.

`FailClosedHistoricalCalendarAdapter` remains mandatory.
## Batch 11G historical time-coordinate closure

The Ming Datong event-time problem is now split into two independent layers.

### A. Internal computational day/time coordinate — source-closed

The 1569 Zhou Xiang primary facsimile directly gives `推合朔時刻法` and binds event `小餘` to the historical 12-shichen / 100-ke system. The received Datong text independently states `日周一萬=一百刻`, with decimal subdivision below ke. The primary procedure counts the event clock from `子正` and handles the half-shichen `子初` label.

Xing Yunlu's Ming Datong worked example gives a replay case: its `定朔` small remainder is converted by the equivalent `發斂法一分二十秒` shorthand and printed as `乙丑日午正初刻`.

Accordingly:

MING_DATONG_INTERNAL_DAY_UNIT=10000_SOURCE_FEN
MING_DATONG_KE_PER_DAY=100
MING_DATONG_COMPUTATIONAL_DAY_BOUNDARY=ZI_ZHENG
ASTROLOGICAL_DAY_BOUNDARY_INFERENCE=FORBIDDEN

The last line is a hard scope boundary: a historical calendar-astronomy day coordinate does not select a Bazi or Ziwei day-boundary rule.

### B. Geographic/meridian realization — still unresolved for qishuo

Ming institutional sources show that Beijing and Nanjing had materially different polar altitude, clepsydra and sunrise/sunset values. Modern international scholarship independently verifies location dependence in the Datong/Shoushi table tradition. However, a Nanjing or Beijing sunrise/sunset table cannot simply be inherited as the meridian reference for conjunction `小餘`.

Therefore:

MING_DATONG_QISHUO_GEOGRAPHIC_REFERENCE=UNRESOLVED
NO_IMPLICIT_UTC_OR_MODERN_TIMEZONE_MAPPING=TRUE
NO_INHERITANCE_FROM_SUNRISE_SUNSET_TABLE_LOCATION=TRUE

`FailClosedHistoricalCalendarAdapter` remains mandatory until the geographic reference, remaining 1569 tables/carry rules, 1578 source replay, exact official-almanac collation, invalid-date behavior and multi-year recurrence are closed.
