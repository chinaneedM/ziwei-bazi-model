# Fusion Chart Historical Provenance Audit R1 — Batch 12HZ

## 1959→1987《左傳》局部邻接序列：三条旁证书号稳定，3368→3288 被隔离为目标条目特异变化

Status: **DIRECT NO-OCR CROSS-COLLATION / SHARED LOCAL CORE 7283 → 8643 → TARGET → 10010 PRESERVES ORDER / FLANKING 7283·8643·10010 STABLE / TARGET 3368→3288 ONLY DIFFERENCE / LOCAL OFFSET AND WHOLESALE LOCAL RESEQUENCING DISPROVED / EXACT CAUSE STILL UNRESOLVED / ZERO PRODUCT CHANGE**

## 1. Why this is stronger than one-neighbor control

Batch 12HS/12HT already showed one stable shared neighbor, `10010`, and therefore rejected a simple blanket arithmetic offset. HZ extends the direct visual crosswalk to both sides of the target.

The evidence is taken from the already hash-bound source scans and reviewed directly without OCR:

- 1959 `《北京图书馆善本书目》第一册`: PDF pages 55–56;
- 1987 `《北京图书馆古籍善本书目·经部》`: PDF page 104 / printed page 92.

## 2. Shared four-record local core

The same local catalog order can be aligned as follows:

| role | record/profile | 1959 | 1987 |
|---|---|---:|---:|
| second preceding | `春秋左傳正義三十六卷` / 宋慶元六年紹興府刻宋元遞修本 | 7283 | 7283 |
| immediate preceding | `附釋音春秋左傳註疏六十卷` / 宋劉叔剛刻本 / 十五冊 / 存二十九卷 | 8643 | 8643 |
| **target** | `附釋音春秋左傳註疏六十卷` / 元刻明修本 / 三十二冊 / 1959 瞿捐 | **3368** | **3288** |
| immediate following | `春秋左傳註疏六十卷` / 明嘉靖李元陽刻十三經註疏本 / 二十三冊 | 10010 | 10010 |

Thus the shared sequence is:

```text
1959: 7283 → 8643 → 3368 → 10010
1987: 7283 → 8643 → 3288 → 10010
```

Three flanking controls retain both their numbers and their relative positions. The exact target alone changes.

## 3. What this closes

The evidence now supports:

```text
blanket local arithmetic offset
= DISPROVEN

wholesale local resequencing of the shared four-record core
= DISPROVEN

observed change scope
= TARGET_SPECIFIC_WITHIN_SHARED_LOCAL_NEIGHBORHOOD
```

This is stronger than merely observing `3368 != 3288`: the change is isolated inside a locally stable catalog neighborhood.

## 4. What it still does not close

HZ does **not** recover the target-specific preparation record. Therefore the following causal explanations remain unranked:

- a 1959 catalog/printing/transcription error later corrected;
- a 1987 target-specific editorial correction;
- a target-specific reassignment during recompilation;
- another catalog-preparation change.

The 1987 foreword's generic statement that earlier cataloging errors were corrected is still not promoted into proof that this exact target was one of those corrections.

The observed `-80` target delta is not a numbering rule.

## 5. Hash and artifact controls

```text
1959 source PDF SHA256
3f7eb1d2ab0057f4524eee2fb3dd3ca08561257302ffed32fe1960188184452f

1959 p55 render SHA256
a5b6db55e979c3530fa95273185bc2239ca347f959a89ecc2377a4b4b299541e

1959 p56 render SHA256
39f4348a6d0c3edbf353452251a5037ab9d3b0c88a35533940051382ca689835

1987 source PDF SHA256
9cb2ab3ff5d00fda316a9f0430096ca2a5e68fcd53609a878c0ed9d08a26d3ab

1987 p104 render SHA256
04c1c3a8a33aaa3b401db2fd6ddcc77455a94098f01cc178a284ea8b2f42b6ce

OCR_USED=false
```

## 6. Project boundary

No chart rule, candidate, Matrix row, provenance-defect count or transmission topology changes.

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance defects = 16 / 16 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```

## 7. Next gate

The highest gate is now narrower: obtain a target-specific catalog card, correction slip, catalog-preparation note, accession register or explicit crosswalk that names `3368` and/or `3288` and explains the isolated change.

Exact Qu donation/accession date, Zhang Lijuan 2018 full text, and the exact 2017 facsimile base-copy binding remain separately open.

Research record: `docs/research/ZIWEI-BEITU1959-1987-ZUOZHUAN-LOCAL-NEIGHBOR-SEQUENCE-CROSSWALK-R1.json`.
