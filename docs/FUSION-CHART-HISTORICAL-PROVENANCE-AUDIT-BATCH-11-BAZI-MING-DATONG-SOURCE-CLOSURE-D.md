# Fusion Chart Historical Provenance Audit R1 — Batch 11D

## Bazi Ming-Datong source closure

Status: **AUDITED / PRIMARY MING METHOD WITNESS LOCATED / EXACT 1578 OFFICIAL ALMANAC LOCATED / ARITHMETIC STILL NOT CERTIFIED / NO ALGORITHM REOPEN**

Batch 11C created a fail-closed historical-calendar adapter contract. Batch 11D strengthens the source stack for the Ming target without promoting an incomplete reconstruction into runtime.

## 1. Primary Ming method witness

`EXT-KOTENMON-DAMING-DATONG-1569` preserves a facsimile of Zhou Xiang's `《大明大統曆法》` in a Ming Longqing edition. The preface explicitly places the compilation in 隆慶己巳 (1569), and the first computational volume is headed `步氣朔`.

The facsimile preserves source-era constants and operational push-step sections for new-moon/syzygy work. This is materially stronger than using the Qing-compiled `《明史·曆志》` as if it were the exact Ming official computational edition.

## 2. Edition-control correction

`EXT-IHNS-MING-DATONG-COMPILATION-2019` records a critical bibliographic point: the Datong material in `《明史·曆志》` differs substantially in content and structure from Ming official Datong works, and some algorithms/tables were later altered or recompiled.

Therefore:

- `EXT-CTEXT-MINGSHI-DATONG-CALENDAR` remains useful for dynasty-history context;
- it is not sufficient as the executable arithmetic authority;
- primary Ming witnesses such as `《大統曆法通軌》` and Zhou Xiang's `《大明大統曆法》` must anchor arithmetic reconstruction.

## 3. Exact-year official oracle target

`EXT-NCL-DATONG-1578-ALMANAC` identifies `《大明萬曆六年歲次戊寅大統曆》` as a one-volume `明欽天監刊本`, catalog no. 06313.

This is exactly the 1578 publication-year context of the `《三命通會》` witness. It is therefore the preferred same-year oracle target for:

- month starts / new-moon day labels;
- leap-month presence and position;
- calendrical day labels;
- any printed time coordinate usable to validate the historical clock realization.

A second bibliographic witness in the Peking University rare-book catalog identifies a 1578 Datong almanac associated with 薛體仁等纂, further supporting the survival of this exact-year official calendar family.

## 4. Broader almanac oracle series

`EXT-NLCPRESS-MING-DATONG-ALMANACS-2007` provides a published facsimile series of 99 Ming Datong almanacs (105 fascicles), including nearby Longqing/Wanli years such as 1569, 1577, 1579 and 1581.

The published table of contents does not list 1578, so this series is a cross-year corroboration set, not a replacement for the exact-year NCL witness.

## 5. Why the adapter is still fail-closed

The following gates are not yet all closed:

1. page-level collation of the relevant 1569 `步氣朔` arithmetic against an edition-critical transcription;
2. direct extraction of reproducible 1578 official-almanac month/leap/time oracle values;
3. deterministic replay showing the selected arithmetic reproduces those oracle values;
4. historical day/time coordinate and enforcement scope;
5. invalid-date / month-length behavior required by Jiaoyun calendarization;
6. source-scoped recurrence semantics for later ten-year Dayun boundaries.

Until these close, `HPA-DAYUN-CAL-002` remains `MISSING_FROM_PRODUCT` and `FailClosedHistoricalCalendarAdapter` remains the only permitted runtime behavior for this historical regime.

```text
TOTAL_MATRIX_ROWS=197
TOTAL_AUDITED_ROWS=165
IDENTIFIED_MISSING_CANDIDATE_FAMILY_COUNT=13
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```

Next work is direct oracle extraction/collation, not speculative coding.
