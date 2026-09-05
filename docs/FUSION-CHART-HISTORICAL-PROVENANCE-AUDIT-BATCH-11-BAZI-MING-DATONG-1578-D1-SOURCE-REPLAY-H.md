# Fusion Chart Historical Provenance & School Audit R1

## Batch 11H - Ming Datong 1578 D1 Source Replay

Status: **COMPLETE AS A TARGET-YEAR RESEARCH MILESTONE; GENERAL HISTORICAL CALENDAR RUNTIME REMAINS FAIL-CLOSED**

Batch ID: `BATCH-11-BAZI-MING-DATONG-1578-D1-SOURCE-REPLAY-H`

This batch closes one narrowly defined question left open after Batch 11G:

> Can the Ming-production D1 conjunction method, reconstructed from the 1569 Zhou Xiang `《大明大統曆法》`, reproduce the actual 1578 Wanli-6 month-start chain without reading the answer from the target-year oracle?

The answer is **yes at day resolution for this target year**. That result does not authorize a general Ming historical-calendar adapter.

## 1. Evidence layers

The evidence is deliberately separated into three non-identical layers.

1. **Method / computation** - the 1569 Zhou Xiang facsimile and the source-derived numeric reconstruction artifacts.
2. **Independent textual oracle** - `《明神宗顯皇帝實錄》` month-start Ganzhi chain, with `《萬曆起居注》` secondary corroboration.
3. **Same-year physical almanac** - NCL book 06313, `《大明萬曆六年歲次戊寅大統曆》`, a Ming Qintianjian printed copy.

These layers must not be double-counted as if they were one witness.

## 2. 1569 source-derived numerical path

Before the target-year replay, the repository machine-reconstructed:

- both solar `盈初縮末 / 縮初盈末` numeric table families;
- all 168 lunar `遲疾日率` rows;
- the complete numeric `損益 / 遲疾度 / 遲疾行度` path;
- the special 83/84 central sign transition;
- the Ming D1 conjunction correction using the corresponding `遲/疾行度`.

The reconstruction remains explicitly distinct from a row-by-row diplomatic transcription. A calculated full table is not automatically a verbatim-edition closure.

## 3. 1578 D1 replay result

Artifact:

`docs/research/MING-DATONG-1578-D1-SOURCE-REPLAY-R1.json`

The replay starts from the Ming epoch/constants and derives the 1578 winter-solstice / run-remainder / mean-conjunction state, then advances month by month through solar and lunar corrections. It does **not** use the oracle to select the month-start answers.

Observed zero-based sexagenary month-start indices:

`49, 18, 48, 18, 47, 17, 46, 16, 45, 14, 44, 13, 43`

Corresponding starts:

`癸丑 → 壬午 → 壬子 → 壬午 → 辛亥 → 辛巳 → 庚戌 → 庚辰 → 己酉 → 戊寅 → 戊申 → 丁丑 → 丁未`

This equals the twelve Wanli-6 month starts plus the Wanli-7 first-month anchor from the independent official-record oracle:

`13 / 13 matched; mismatch = 0`.

The inferred month-length sequence is therefore:

`29 / 30 / 30 / 29 / 30 / 29 / 30 / 29 / 29 / 30 / 29 / 30`

for a 354-day non-leap represented year.

The minimum replayed distance from a day boundary is 197.31 historical source units (about 28.41 modern minutes if used only as a scale comparison), so the **day labels in this target-year chain** are not sensitive to unresolved sub-0.01-source-unit truncation details. This does not universalize the observed truncation policy.

## 4. Same-year physical NCL almanac

Artifact:

`docs/research/MING-DATONG-1578-NCL-06313-PHYSICAL-ALMANAC-COLLATION-R1.json`

NCL catalog identity:

- title: `大明萬曆六年歲次戊寅大統曆`;
- book / registration no.: `06313`;
- edition: `明欽天監刊本`;
- seal: `欽天監/曆日印`;
- one-volume line-bound physical copy.

A public 28-page scan is also located.

The twelve calendar-month pages are contiguous at zero-based PDF pages 8-19. Eleven pages rendered directly in the current research environment and all eleven visible month identities / 大小 month labels agree with the D1 replay and official-record chain. There are zero observed physical-page month-size mismatches.

The zero-based PDF page 13, corresponding to **六月**, repeatedly fails the available screenshot renderer while adjacent pages render successfully. Therefore:

`DIRECT_PHYSICAL_MONTH_PAGE_COLLATION = 11 / 12`

`MONTH_6_DIRECT_PHYSICAL_PAGE = UNRESOLVED_TECHNICAL_ACCESS_GAP`

It is forbidden to infer a direct physical June-page reading from the replay, neighboring pages, or the official-record oracle.

## 5. Independent second 1578 copy lineage

`EXT-PKU-DATONG-1578-ALMANAC` records another exact-year copy in the `《北京大学图书馆藏善本书目》`:

- `大明萬曆六年歲次戊寅大統曆`;
- `明薛體仁等纂`;
- `明萬曆刻本（附復翁跋語一紙）`;
- one volume;
- call number `528.7/1578`.

This is currently a bibliographic second-copy witness, not a page-value witness. No second-copy month image is silently substituted for the unavailable NCL June rendering.

## 6. What Batch 11H closes

Closed:

- source-derived D1 replay to the 1578 official-record month-start oracle;
- twelve Wanli-6 starts plus next-year first-month anchor, 13/13 at day resolution;
- same-year NCL Qintianjian physical-copy identity;
- 11/12 direct physical month-page / large-small month-label collation with zero mismatch;
- evidence-layer separation between calculation, official record and physical almanac.

Not closed:

- NCL June page direct rendering / second-copy page image;
- exact subday conjunction-time certification from the 1578 physical month grids;
- complete row-by-row diplomatic collation of every 1569 table value;
- universal historical truncation / carry policy;
- qishuo geographic / meridian reference;
- invalid-date and month-length addition semantics;
- multi-year leap-month generalization;
- ten-year Dayun recurrence under the same historical regime;
- executable historical-calendar runtime.

## 7. Product and algorithm disposition

`HPA-DAYUN-CAL-002` remains:

`MISSING_FROM_PRODUCT`

The historical adapter remains fail-closed.

`confirmed_chart_algorithm_defect_count = 0`

`algorithm_reopen_count = 0`

`candidate_collapse_count = 0`

No existing deterministic chart coordinate is changed by this batch.

## 8. Next work

Priority order:

1. obtain a direct alternate render or a page image from the second 1578 copy for the June page;
2. finish row-by-row 1569 primary table collation and variant ledger;
3. generalize fixed-point precision / truncation / carry behavior across additional worked cases;
4. close qishuo geographic / meridian reference independently;
5. close invalid-date / month-length addition semantics;
6. close multi-year leap-month and ten-year recurrence behavior;
7. only then consider a regime-scoped executable historical calendar adapter.
