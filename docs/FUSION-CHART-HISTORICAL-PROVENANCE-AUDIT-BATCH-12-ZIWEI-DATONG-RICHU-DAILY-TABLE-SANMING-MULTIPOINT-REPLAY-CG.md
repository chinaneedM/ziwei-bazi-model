# Fusion Chart Historical Provenance Audit R1 — Batch 12CG

## NCL《大統日出分》逐日南京數表 × 1578《三命通會》多點刻數重放

Status: **1380s NANJING DATONG DAILY SUNRISE/DAYLENGTH TABLE FAMILY INDEPENDENTLY IDENTIFIED AND PHYSICALLY REVIEWED / MULTIPLE 42→59 SANMING INTEGER ANCHORS NUMERICALLY REPLAYED FROM THE DAILY HALF-DAY CURVE / SONG 1068 SELF-DATED RECEIVED TEXT INDEPENDENTLY ATTESTS INTRA-SOLAR-TERM INTEGER DAY/NIGHT-KE BINS / MECHANICAL BRIDGE CLOSED ONE LAYER / EXACT SANMING CHANGE-DAY PARENT AND QUANTIZATION RULE STILL OPEN / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO HAI VOTE / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Why this follows Batch 12CF

Batch 12CF physically closed the pre-1578 Nanjing solstitial `59` layer with the 1447 `《明英宗實錄》`, but deliberately left the intermediate `42/58`, `45/55`, `47/53`, `48/52`-style ladder open.

This batch asks whether an earlier Ming/Nanjing *daily numerical substrate* and an independently older *integer-bin timekeeping form* can explain those intermediate anchors without inventing a genealogy.

## 2. Direct NCL physical object

```text
SOURCE=NCL-06267 大統日出分
RUN=34869676923
ARTIFACT=10358685142
ARTIFACT_DIGEST=sha256:fdb1fd4b9e0fc785d9fb467e00daa71544c412482e2093d31cf553152bd518fe
SOURCE_SHA256=0d3ed2b54f92b5eb2f11e5d06babebcc177e04ec5b8c7168b56f1fb25f94797d
PDF_PAGES=21
OCR_USED_FOR_GLYPH_CLAIMS=false
```

Direct review shows a daily table rather than a 24-row solar-term summary. It contains daily arguments after the solstices and columns `晨分 / 日出分 / 半晝分 / 日入分 / 昏分`. Representative rendered page hashes are machine-bound in the research record.

## 3. Independent identification: 1380s Type C-II-N = Nanjing

Li Liang's study *Tables of Sunrise and Sunset in Yuan and Ming China (1271–1644) and their Adoption in Korea* independently classifies:

```text
大統日出入分 = 1380s = C-II-N
C = Chinese source
II = daily pick-up table type
N = Nanjing
```

The published Type C-II-N excerpt prints days `0..10` and `178..182`. Its `半晝分` values begin at `2068.30` and end at `2931.66`; those opening/end fingerprints agree with the physical NCL object. The source also explains Type II as a daily table and identifies the relevant columns.

This supplies a secure external identity bridge. It does **not** make the modern article a historical authority, and it does not prove Wan Minying handled this exact surviving copy.

## 4. Numerical replay against the Sanming integer ladder

Under the hundred-ke day / 10,000-fen day framework, the table's `半晝分` converts to full daylight ke by:

```text
daylight_ke = 2 * half_day_fen / 100
```

Selected direct no-OCR points across the NCL curve replay distinct integer anchors:

```text
day 21   half-day ≈2101.63 -> daylight ≈42.0326 -> 42
day 34   half-day ≈2154.21 -> daylight ≈43.0842 -> 43
day 43   half-day ≈2208.19 -> daylight ≈44.1638 -> 44
day 52   half-day ≈2257.14 -> daylight ≈45.1428 -> 45
day 59   half-day ≈2302.41 -> daylight ≈46.0482 -> 46
day 67   half-day ≈2348.62 -> daylight ≈46.9724 -> 47
day 74   half-day ≈2401.90 -> daylight ≈48.0380 -> 48
day 89   half-day ≈2494.04 -> daylight ≈49.8808 -> 50
day 98   half-day ≈2559.25 -> daylight ≈51.1850 -> 51
day 178  half-day 2930.34  -> daylight 58.6068  -> 59
day 181  half-day 2931.51  -> daylight 58.6302  -> 59
```

The daily curve therefore supplies the entire continuous numerical range in which the Sanming 42→59 integer ladder sits. The important result is **generative compatibility at daily resolution**, not a claim that `round()` was Wan Minying's textual rule.

Firewall:

```text
EXACT_SANMING_CHANGE_DAY_THRESHOLDS_RECOVERED=false
NEAREST_INTEGER_ROUNDING_PROVED_AS_HISTORICAL_RULE=false
DIRECT_COPY_FROM_NCL06267_TO_SANMING=false
```

## 5. Much earlier integer-bin form: Song received 景福殿秤漏 passage

The received `《盂蘭盆經疏鈔餘義》` identifies 日新 as recorder, and its own preface dates the lecture/republication to `熙寧元年` (1068). The current CBETA object is a later received digital text, **not a 1068 physical scan**.

Its `〈節氣加減刻漏規式〉` states:

```text
今依本朝定景福殿秤漏，春秋二分各五十刻
```

and then assigns every integer day/night pair from `40/60` through `60/40` to explicit ranges *inside* solar terms, e.g. rows such as `42/58`, `43/57`, `44/56` and onward.

This is decisive for algorithmic form: long before 1578, a received Song text already preserves a scheme in which seasonal timekeeping is discretized into integer ke bins whose change-points occur inside solar terms.

It is **not** the exact Sanming table: its day ranges differ, and no direct genealogy is asserted.

## 6. Historical synthesis

The safe reconstruction is now narrower:

```text
older intra-term integer-bin leak-clock tradition
  +
Ming/Nanjing daily Datong sunrise/daylength numerical substrate
  ->
historically plausible generative bridge for Sanming's stepped multipoint display
```

This closes one mechanical layer that Batch 12CF had left open. It still does not identify the exact pre-1578 parent text, the compositing event, or the exact quantization/change-day convention used by Wan Minying.

## 7. Product adjudication

For `HPA-ZDATE-006`:

- pre-1578 Nanjing daily numerical substrate: **closed at table-family level**;
- pre-1578 intra-term integer-bin algorithm family: **closed at received-text level**;
- exact Sanming multipoint parent/change-day fingerprint: **open**;
- upper-Zi → Hai mechanical vote: **0**;
- runtime candidate/winner/collapse: **none**;
- algorithm reopen: **no**;
- status: **MISSING_FROM_PRODUCT**.

Counts remain `198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families`; provenance defects remain `11 confirmed / 11 repaired`; chart algorithm defect/reopen/collapse remain `0/0/0`.

## 8. Next gate

Search for a securely pre-1578 calendrical, mantic, tongshu or institutional source that either:

1. prints the **same Sanming intra-term change-day fingerprint**, or
2. states an exact quantization rule that deterministically reproduces those change-days from a Nanjing/Datong daily table.

Continue the Fullbook `上五刻 -> 昨夜亥時` line independently; none of the evidence in this batch supplies a Hai-branch vote.

Research record: `docs/research/ZIWEI-DATONG-RICHU-DAILY-TABLE-SANMING-MULTIPOINT-REPLAY-R1.json`.
