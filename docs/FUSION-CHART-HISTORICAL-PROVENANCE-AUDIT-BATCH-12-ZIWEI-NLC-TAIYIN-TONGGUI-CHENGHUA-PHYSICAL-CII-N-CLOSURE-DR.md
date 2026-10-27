# Fusion Chart Historical Provenance Audit R1 — Batch 12DR

## 國圖明成化抄本《太陰通軌》：中國 pre-1578 C-II-N 晨昏逐日數表物理閉合

Status: **CHINESE PRE-1578 PHYSICAL C-II-N CARRIER CLOSED / NLC 411999012050 TWO-VOLUME SURROGATE DIRECTLY REVIEWED / DAY0 2681.70+7318.30 AND DAY178 1819.66+8180.34 EXACTLY MATCH THE JOSEON GK12436 WITNESS / SURVIVING CHENGHUA COPY CANNOT BE THE DIRECT ANCESTOR OF THE EARLIER SEJONG-ERA SURVIVING COPY / EXACT EARLIER EXEMPLAR AND WHOLE-KE REDUCTION RULE STILL UNRESOLVED / ZERO EXACT SANMING-PARENT VOTE / NO RUNTIME CHANGE / NO ALGORITHM REOPEN**

## 1. Why this batch

12CV had already closed a 15th-century Joseon physical witness of the C-II-N daily morning/evening table in Kyujanggak `GK12436_00`. 12DQ then narrowed the remaining mechanism problem to a pre-1578 Chinese source that could bind that continuous daily layer to the independent Nanjing 59-ke endpoint.

One explicit question therefore remained:

> Is the same C-II-N daily table physically preserved in a Chinese pre-1578 carrier, rather than known only through the Joseon transmission branch and later Chinese controls?

12DR answers that question **yes**, while keeping the downstream integer-selection rule open.

## 2. Source identity and access chain

The public NLC backup listing exposes one NLC object under the title `太陰通軌`, `題抱拙子編`, split into two PDFs:

```text
NLC object = 411999012050
vol.1 = NLC892-411999012050-103144 太陰通軌 第1冊.pdf
vol.2 = NLC892-411999012050-103188 太陰通軌 第2冊.pdf
```

The project already registers the modern critical bibliographic control `EXT-IHNS-MING-DATONG-COMPILATION-2019`, which identifies the NLC `元統《太陰通軌》` as a **Ming Chenghua manuscript**, one juan of `《大統曆法通軌》`. That control is used only for copy/work/date identity; final glyph and numeric readings below come from the downloaded physical surrogate itself.

Acquisition control:

```text
WORKFLOW_RUN=35431281149
ARTIFACT=10580972630
ARTIFACT_DIGEST=sha256:cc225798a0ea4dba8163423b94b0e0c891d3b5a1052faaaa1e836d571e5ae964

VOL1 pages=46
VOL1 sha256=5459e8f27ca1eb158d34daa3a8dc96ac150234f80f3b3309362979dd39ff6762

VOL2 pages=41
VOL2 sha256=7d47432648f4dc20075166872811bbb15bd80473284b57426339f071989f7c8c
```

The PDFs contain no useful target text layer. `pdftotext` and outside transcriptions were used only as locators. **No OCR is used as final glyph or numeric authority.**

## 3. Direct physical collation

### 3.1 Volume 2, PDF page 15

Direct visual review reads the heading:

```text
冬夏二至日出晨昏分立成鈐
```

This is deliberately not normalized to the Kyujanggak heading `冬夏二至日晨昏分立成鈐`: the NLC witness visibly preserves an additional `出` after `日`.

The winter-solstice initial-day pair directly reads:

```text
晨分 = 2681.70
昏分 = 7318.30
SUM  = 10000.00
```

Artifact-render control:

```text
vol2-15.jpg sha256=5fe45f2483dd7f5a4e92506845cec74bd72901dae3f62e59de24fd1ef7b4016b
```

### 3.2 Volume 2, PDF page 23

The accumulated-day sequence directly reaches `百七十八日`. Resolving the manuscript table's repeated high-order row prefix with the day-178 column suffixes gives:

```text
day178 晨分 = 1819.66
day178 昏分 = 8180.34
SUM          = 10000.00
```

Artifact-render control:

```text
vol2-23.jpg sha256=17b9dda2a347f3075c834b451417b0adc852313ce168d4f68ae98e6d78ac4f80
```

This reading is a direct visual common-prefix reconstruction from the physical table, not OCR.

## 4. Cross-recension numerical closure

The previously closed Kyujanggak `GK12436_00` physical witness gives:

| control | NLC Chenghua manuscript | Kyujanggak Sejong-era print | result |
| --- | ---: | ---: | --- |
| day0 晨分 | 2681.70 | 2681.70 | exact |
| day0 昏分 | 7318.30 | 7318.30 | exact |
| day178 晨分 | 1819.66 | 1819.66 | exact |
| day178 昏分 | 8180.34 | 8180.34 | exact |

Using the already registered Tonggui conversion:

```text
sunrise = morning + 250 fen
half-daylight = 5000 - sunrise
```

we get:

```text
day0   -> sunrise 2931.70 -> half-day 2068.30
day178 -> sunrise 2069.66 -> half-day 2930.34
```

Both are exact C-II-N controls already closed against the Nanjing Datong daily table.

Therefore:

```text
CHINESE_PRE1578_PHYSICAL_CARRIER_FOR_CII_N = CLOSED
NLC_CHENGHUA_AND_KYUJANGGAK_SAME_NUMERICAL_TABLE_FAMILY = HIGH_CONFIDENCE
```

## 5. Chronology firewall: identical table does not mean direct surviving-copy ancestry

The surviving-copy dates point in the opposite direction from a tempting but invalid shortcut:

```text
Kyujanggak GK12436 provider date scope = Sejong 1418–1450
NLC surviving manuscript control       = Chenghua 1465–1487
```

So the **surviving NLC Chenghua copy cannot be the direct ancestor of the surviving Sejong-era Korean print**.

This does not negate Chinese origin of the table tradition. It means only that the exact surviving Chenghua object is too late to be that Korean object's exemplar. The exact numerical agreement instead strengthens an earlier shared Chinese table tradition / exemplar hypothesis, whose specific physical source remains unresolved.

No reverse direct-copy direction is inferred either.

## 6. What 12DR closes—and what it does not

Closed:

```text
Chinese pre-1578 physical carrier of C-II-N daily 晨昏 table = YES
direct physical day0 fingerprint                              = CLOSED
direct physical day178 fingerprint                            = CLOSED
Chinese/Joseon same numerical table family                    = HIGH_CONFIDENCE
```

Still open:

```text
exact earlier Chinese exemplar used in Joseon transmission     = UNRESOLVED
whole-ke threshold / bin / 改箭 / selection instruction        = UNRESOLVED
explicit binding of C-II-N interior to Nanjing 59-ke endpoint  = UNRESOLVED
Sanming/Yueling 大寒十三後 / 雨水後四日 source                 = UNRESOLVED
direct parent of Sanming 1578                                  = NOT PROVED
```

The new evidence strengthens the substrate, not the final quantization rule.

## 7. Tianwen transmission graph impact

New nodes:

```text
PHYSICAL-COPY-NLC-TAIYIN-TONGGUI-CHENGHUA-411999012050
PASSAGE-NLC-TAIYIN-TONGGUI-CHENHUN-LICHENG
```

New positive edges:

```text
TG-E0060  NLC Chenghua physical copy
          --ATTESTS-->
          NLC 晨昏立成 passage/table

TG-E0061  NLC 晨昏立成 passage/table
          --TRANSMITS_RULE-->
          TABLE-NANJING-DATONG-DAILY-CII-N-1380S
```

A chronology non-edge is also recorded:

```text
NLC Chenghua surviving physical copy
  --DIRECT_ANCESTOR_OF-->
Kyujanggak Sejong-era surviving physical copy
  = DISPROVED BY SURVIVING-COPY CHRONOLOGY
```

This prevents identical numbers from being misread as direct copy identity.

## 8. Product adjudication

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
HPA-ZDATE-006=MISSING_FROM_PRODUCT
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=12
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=12
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

No runtime candidate is added, no candidate winner is selected, and no chart algorithm is reopened.

## 9. Next gate

The highest-value unresolved question has moved one layer downstream:

1. inspect the NLC Chenghua `《太陰通軌》` and related Chinese Datong/Tonggui witnesses for an explicit whole-ke reduction / binning / change-arrow / endpoint-binding instruction;
2. continue the pre-1578 exact-fingerprint search for `大寒十三後 / 雨水後四日`;
3. locate and physically collate the separately reported NLC three-juan manuscript `《大統曆法通軌》`, without assuming identity from title alone;
4. keep NLC call 14202 `《通書類聚》` reproduction access in parallel behind the external-action authorization firewall.

Research record: `docs/research/ZIWEI-NLC-TAIYIN-TONGGUI-CHENGHUA-PHYSICAL-CII-N-CLOSURE-R1.json`.
