# Fusion Chart Historical Provenance & School Audit R1

## Batch 11I - Ming Datong 1578 Physical Almanac Closure

Status: **COMPLETE AS THE SAME-YEAR PHYSICAL MONTH-PAGE IDENTITY/SIZE LAYER; GENERAL HISTORICAL CALENDAR RUNTIME REMAINS FAIL-CLOSED**

Batch ID: `BATCH-11-BAZI-MING-DATONG-1578-PHYSICAL-ALMANAC-CLOSURE-I`

This batch records a new direct-image result obtained after Batch 11H. It does **not** rewrite Batch 11H: at that earlier point, the June page was genuinely unavailable to the renderer and 11/12 was the correct historical state.

## 1. Question closed

The remaining question was narrowly defined:

> Can the exact same-year NCL 06313 Qintianjian almanac's zero-based PDF page 13 be directly rendered and its June month identity / large-small label read, without inferring either from the D1 replay, neighboring pages, or the official-record oracle?

The answer is now **yes**.

## 2. Direct physical evidence

Physical witness:

- title: `《大明萬曆六年歲次戊寅大統曆》`;
- NCL catalog / registration no.: `06313`;
- edition: `明欽天監刊本`;
- seal: `欽天監/曆日印`;
- public scan: Wikimedia Commons NCL backup, 28 PDF pages.

Public scan:

`https://upload.wikimedia.org/wikipedia/commons/7/72/NCL-06313_%E5%A4%A7%E6%98%8E%E8%90%AC%E6%9B%86%E5%85%AD%E5%B9%B4%E6%AD%B2%E6%AC%A1%E6%88%8A%E5%AF%85%E5%A4%A7%E7%B5%B1%E6%9B%86.pdf`

The original renderer path continued to fail on zero-based page 13 even while neighboring pages rendered. Reopening the same PDF through a fresh `#page=14` context allowed that exact zero-based page to render directly.

The recovered page visibly reads:

`六月小`

Therefore:

`DIRECT_PHYSICAL_MONTH_PAGE_COLLATION = 12 / 12`

`DIRECT_MONTH_IDENTITY_MATCH = 12 / 12`

`DIRECT_MONTH_SIZE_MATCH = 12 / 12`

`DIRECT_MONTH_SIZE_MISMATCH = 0`

The directly visible month-length sequence is:

`29 / 30 / 30 / 29 / 30 / 29 / 30 / 29 / 29 / 30 / 29 / 30`

This equals the independently derived official-record oracle and the source-derived D1 replay at month-size resolution.

## 3. Evidence boundary

The recovered page closes **month identity and 大/小 only**.

It does not silently promote the small first-day calendar-grid glyphs into an independently transcribed `辛巳` witness. The repository therefore keeps:

`GRID_VISUALLY_CONSISTENT_BUT_FINE_GLYPH_READING_BOUND_TO_ORACLE_CHAIN`

for the month-start Ganzhi certification field.

The following remain forbidden:

- inferring an unread physical page from neighboring pages;
- treating a month title / size label as a fine first-day Ganzhi transcription;
- treating the physical day grid as an exact true-conjunction subday-time certificate;
- treating the 1578 day-level match as a qishuo geographic / meridian solution;
- treating one same-year almanac match as general Datong runtime certification.

## 4. Relation to Batch 11H and later 1569 collation

Batch 11H remains historically correct as the record of the earlier 11/12 state.

Since then, the 1569 Zhou Xiang primary tables have separately reached direct edition-scoped collation closure:

- solar: `185 / 185`;
- lunar 遲疾: `169 / 169`;
- lunar 行度: `169 / 169`;
- within-edition numeric/glyph ambiguity in those closed primary ledgers: zero.

That primary closure does not close the cross-edition variant-cause ledger. Goryeosa and later received witnesses remain evidence-scoped and may not overwrite the Ming 1569 primary layer.

## 5. What this batch closes

Closed:

- the sole remaining NCL 06313 month-page renderer gap;
- direct June month identity = `六月`;
- direct June size label = `小`;
- 12/12 direct physical month-page identity collation;
- 12/12 direct physical 大/小 collation;
- zero observed physical month identity / size mismatch against the D1 replay and official-record oracle.

Not closed:

- direct diplomatic transcription of every first-day Ganzhi glyph from all twelve physical month grids;
- exact physical certification of true-conjunction subday values;
- universal historical fixed-point truncation / carry / interpolation rules;
- qishuo geographic / meridian reference;
- invalid-date and month-length addition semantics;
- multi-year leap-month behavior;
- ten-year Dayun recurrence under the same historical regime;
- executable historical-calendar runtime;
- cross-edition variant causes requiring direct image adjudication.

## 6. Product and algorithm disposition

`HPA-DAYUN-CAL-002` remains:

`MISSING_FROM_PRODUCT`

The historical adapter remains fail-closed.

`confirmed_chart_algorithm_defect_count = 0`

`algorithm_reopen_count = 0`

`candidate_collapse_count = 0`

No existing deterministic chart coordinate changes in this batch.

## 7. Next work

Priority now moves away from the closed June-page access gap:

1. continue direct-image adjudication of cross-edition Goryeosa / received-table variants;
2. generalize and verify fixed-point truncation / carry / interpolation behavior across more worked cases;
3. close qishuo geographic / meridian reference independently;
4. close invalid-date / month-length addition semantics;
5. close multi-year leap-month and ten-year recurrence behavior;
6. only then consider a regime-scoped executable historical calendar adapter.
