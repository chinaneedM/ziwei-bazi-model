# Fusion Chart Historical Provenance Audit R1 — Batch 12FJ

## 國家圖書館數字古籍 FID / 閱讀對象 bid 與縮微 905$b 登錄號分層閉合

Status: **NLC READ DATA_892 FID 411999008600/601 DIRECTLY CLOSED / READ OBJECT BID 113028/113029 DIRECTLY CLOSED / MICROFILM WORK-RECORD PAIR SYS 002146415/416 CLOSED / STRUCTURED 905$b 00O003570/571 CLOSED / 905$b CLASSIFIED AS MICROFILM REGISTRATION-LOGIN NUMBER USING CNMARC SEMANTIC CONTROLS / CURRENT RARE-BOOK SYS+905s LAYERS REMAIN SEPARATE / NO PUBLIC BARCODE / NO ACQUISITION-ROUTE VERDICT / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12FI closed the current rare-book pair:

```text
銅壺漏箭制度      SYS 001775082 / UID UCS01003828992 / NLC:SBYL:03482
準齋心製几漏圖式  SYS 001775083 / UID UCS01003828993 / NLC:SBYL:03483
```

It also closed the reciprocal microfilm free-text notes:

```text
銅壺縮微：準齋另拍在 00O003571
準齋縮微：銅壺另拍在 00O003570
```

but intentionally left `00O003570/571` and linked controls `411999008600/601` incompletely classified. Batch 12FJ asks which identifier layers those values actually belong to.

## 2. Controlling first-party NLC evidence

### 2.1 read.nlc.cn digital-object route

GitHub Actions source-bound probe:

```text
RUN      = 36022930599
ARTIFACT = 10816989283
DIGEST   = sha256:9073537533143383592026aa3aa05d4fec86dbb5e5a2c2dcab8174442d21dc04
OCR_USED = false
```

Direct NLC pages returned HTTP 200:

```text
data_892 identifier/FID = 411999008600
title                   = 銅壺漏箭制度
cover                    = img892/SBGJ03908_00001.jpg
open-object route        = /OutOpenBook/OpenObjectBook?aid=892&bid=113028.0

data_892 identifier/FID = 411999008601
title                   = 准齋心製几漏圖式
cover                    = img892/SBGJ03909_00001.jpg
open-object route        = /OutOpenBook/OpenObjectBook?aid=892&bid=113029.0
```

Target HTML hashes:

```text
Tonghu   d29a1e9453d4570017485d0d830e2f67fa6ebfb55e8966127849f1dfc88f0831
Zhunzhai 8c46c8eafcc5dd8e3132aaa4755b764275366e65c8bf43adfbb3b7f9af9636aa
```

Thus `411999008600/601` are directly closed as first-party NLC `data_892` resource identifiers/FIDs for the two digitized ancient-book records. `113028/113029` are separately closed as the NLC reading-object `bid` values used by the open-object route.

A Wikimedia NLC-backup index independently preserves the same FID→title→file-object-number pair, but it is locator/corroboration only; the NLC pages above are controlling.

## 3. 455 embedded-001 crosswalk

The already-gated current microfilm metadata had:

```text
銅壺   455$1 raw = 001411999008600
準齋   455$1 raw = 001411999008601
```

UNIMARC/CNMARC 455 is a reproduction-link field and the embedded `001` is a record identifier. 12FJ now directly demonstrates that the parsed values:

```text
411999008600
411999008601
```

are also active first-party NLC `read.nlc.cn data_892` identifiers for the corresponding digitized ancient-book resources.

This closes a cross-system relationship, not an identifier collapse:

```text
microfilm 455 embedded record-control value
        ↕ directly concordant
read.nlc.cn data_892 FID / identifier
```

It does **not** make the value a current `meta.nlc.cn` bibliographic SYS, UID, rare-book call number or barcode.

## 4. Current microfilm work-record pair and structured 905$b

A second first-party probe reads all four current microfilm records:

```text
RUN      = 36023804174
ARTIFACT = 10819360343
DIGEST   = sha256:3d1bba50289697254336125cf47da28bb440d363ddd81f3ac06d504328241802
OCR_USED = false
```

The two work/master-style records directly emit structured 905 fields:

```text
銅壺
SYS 002146415 / UID UCS01003553255
1盤卷片(3米32拍)
905a = 全国图书馆文献缩微中心
905b = 00O003570
905q = swkf
455$1 = 001411999008600
455 note -> 準齋另拍在00O003571

準齋
SYS 002146416 / UID UCS01003553256
1盤卷片(3米26拍)
905a = 全国图书馆文献缩微中心
905b = 00O003571
905q = swkf
455$1 = 001411999008601
455 note -> 銅壺另拍在00O003570
```

Target JSON hashes:

```text
Tonghu   02c0ff8fe206e9b3cbc5763da14a3916be2818b451024d208c59b68bc85e02e1
Zhunzhai f00b982db4b7297fc140ce550ebcddcf70e21a804cd0478663d255377ae88db0
```

The distribution-copy records `002597933/934` do not contain 905$b, but preserve the same 455 original-source and reciprocal `另拍在` notes. This is consistent with two record layers rather than contradictory semantics.

## 5. 905$b semantic adjudication

Multiple institutional CNMARC cataloging specifications explicitly define:

```text
905 = holdings information
905$a = institution/library code
905$b = 登錄號 / registration-accession number
905$d/e = classification/call-number components
```

The target NLC records themselves directly establish the value placement; external CNMARC controls supply the field semantics.

Therefore the safe target-specific classification is:

```text
00O003570 = Tonghu microfilm registration/login number in structured 905$b
00O003571 = Zhunzhai microfilm registration/login number in structured 905$b
```

The word “accession” here is library item-registration semantics for the **1985 microfilm objects**. It must not be confused with:
- the historical acquisition/transfer of the Huang/Tieqin rare-book object into Beijing Library/NLC;
- a current rare-book call number;
- a public barcode;
- a donation number.

## 6. Identifier-layer firewall

The now-closed layers are:

```text
Original rare-book catalog SYS:
  001775082 / 001775083

Original rare-book current local-call components:
  905$s 03482 / 03483
  NLC:SBYL:03482 / NLC:SBYL:03483

Digitized ancient-book NLC read identifiers/FIDs:
  411999008600 / 411999008601

NLC reading-object bid:
  113028 / 113029

Microfilm work-record SYS:
  002146415 / 002146416

Microfilm distribution-copy SYS:
  002597933 / 002597934

Microfilm registration/login numbers:
  905$b 00O003570 / 00O003571
```

Numeric adjacency or title pairing does not authorize substituting one layer for another.

## 7. Acquisition-provenance firewall

NLC historical material establishes that Tieqin Tongjianlou books entered Beijing Library through mixed sale and donation channels. The target 1959 entries do not carry `瞿捐`, and secondary research reports not locating these two titles in the separate Qu donation list. This narrows the search, but does not identify the target-specific legal transfer event.

```text
TARGET_3482_3483_SALE_ROUTE     = NOT_SELECTED
TARGET_3482_3483_DONATION_ROUTE = NOT_SELECTED
FINAL_ACQUISITION_PATH          = UNRESOLVED
```

The microfilm 905$b registration numbers are unrelated to that unresolved historical acquisition question.

## 8. Transmission-genealogy consequence

12FJ should strengthen the existing current/microfilm object-family controls and add explicit digital-resource nodes for the two `data_892` resources. Any new edges are evidence-scoped `ATTESTS` / digital-surrogate links only.

No `SAME_OBJECT`, direct-copy, authorship-redating or Sanming-parent edge is authorized.

## 9. Product firewall

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
MISSING_FROM_PRODUCT=10
PROVENANCE_DEFECTS=13/13_REPAIRED
CONFIRMED_CHART_ALGORITHM_DEFECTS=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
DIRECT_SANMING_PARENT_VOTE_INCREMENT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 10. Next gate

1. test whether the NLC open-object `bid=113028/113029` routes expose page-count/object-manifest metadata that can be hash-bound without login;
2. search NLC/archive/bibliographic sources for a target-specific Qu sale/donation/accession entry, keeping “not found in donation list” as bounded evidence rather than a sale verdict;
3. continue the pre-1578 Zhunzhai rule line and independent Sanming/Yueling Dahan–Rainwater + Nanjing-59 lines.

Research record: `docs/research/ZIWEI-NLC-DIGITAL-FID-AND-MICROFILM-REGISTRATION-R1.json`.
