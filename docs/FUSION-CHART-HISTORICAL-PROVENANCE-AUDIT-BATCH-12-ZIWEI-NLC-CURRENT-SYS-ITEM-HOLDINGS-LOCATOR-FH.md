# Fusion Chart Historical Provenance Audit R1 — Batch 12FH

## 國家圖書館 current meta：原善本 SYS / UID / 905 館藏定位與 455 複製來源控制號分層

Status: **CURRENT NLC ORIGINAL-RARE-BOOK RECORD CLOSED / SYS 001775083 + UID UCS01003828993 CLOSED / CURRENT LOCAL HOLDINGS LOCATOR NLC:SBYL:03483 CLOSED / 905s 03483 CLOSED AS LOCAL CALL-NUMBER COMPONENT / SBYL = 善本閱覽室 / PUBLIC BARCODE NOT EXPOSED / 455 EMBEDDED 001 LINK CLASSIFIED AS RECORD-CONTROL PAYLOAD, NOT SHELFMARK / 00O003570 REMAINS SEPARATE-PHOTO REFERENCE / ACQUISITION ROUTE UNRESOLVED / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12FG closed the 1959 historical catalog-number layer but deliberately left the current NLC item locator open. Batch 12FH asks whether original rare-book doc `001775083` is still represented in the current NLC metadata platform, which current record/holding identifiers it exposes, and how `001411999008601` and `00O003570` should be classified without shape inference.

## 2. Source-bound current-platform recovery

The current National Library of China metadata frontend exposes `POST /v2/doSearch?hight=false` and item-detail `POST /api/v1/item/<UID>/1/999`. The controlling GitHub Actions evidence is:

```text
current JSON search: run 36018407574 / artifact 10816096193 / sha256:49cd661d1d890b6ed247db2ddaf4a1cac21fd26145504ab63f86c68560b7e5f4
holding bridge:      run 36019233451 / artifact 10816056823 / sha256:1dcf44b657ca3c0d236dd04d5d28df624507b5feeb92a14aa26e25b622f2f17c
SYS field:           run 36019435493 / artifact 10815952788 / sha256:384e4acedb67dad3b5099129bf80463046b9c2a2c22da6f2544aacaf32db98e9
item detail:         run 36019748667 / artifact 10815419291 / sha256:be9cc2db66d4ad150a975f08f2956b6ab068314b9afbdf69fd5d4a6a564eda65
OCR_USED=false
```

## 3. Current SYS / UID closure

A field-level positive-control probe establishes that current `meta.nlc.cn` indexes legacy OPAC `doc_number` values as `SYS`. The original rare book uniquely resolves as:

```text
SYS = 001775083
UID = UCS01003828993
WDT = 善本
YEA = 1823
PUB = 黃氏士禮居
PAG = 1冊
title = 准齋心製几漏圖式
holding = 国家图书馆
```

The 1985 microfilm separately resolves as `SYS=002597934 / UID=UCS01003581458`. Thus `001775083` is directly closed as the current NLC metadata platform system identifier for the original rare-book record. `UCS01003828993` is a separate current platform UID. Neither is a barcode.

## 4. Current local-holdings locator

The original-record item API directly returns:

```text
905a = NLC
905q = SBYL
905s = 03483
3165 = NLC:SBYL:03483
852a = A100000NLC
```

CNMARC search/index documentation maps `905s` to Local Call Numbers, and NLC sublibrary documentation identifies `SBYL` as `善本阅览室`. The safe classification is therefore:

```text
current NLC local holdings locator = NLC:SBYL:03483
institution component             = NLC
sublibrary/location component     = SBYL = 善本閱覽室
local call-number component       = 03483
public barcode                    = NOT EXPOSED / NOT PROVED
```

This does not collapse identifier layers. The same number was historically printed as 3483 in the 1959 catalog and later used by OPAC as 原文献03483; 12FH now additionally observes `03483` in the current local call-number field. Historical catalog-number semantics and current holdings semantics remain separately recorded.

## 5. `001411999008601` classification

The current microfilm item payload emits the prior 12FF value inside MARC linking field `455 $1`. UNIMARC defines 455 as `Reproduction Of` and permits embedded fields including `001 Record Identifier`. The safe parse is:

```text
raw linked payload = 001411999008601
embedded tag       = 001
record control id  = 411999008601
```

Therefore `001411999008601` is not a physical shelfmark, barcode, acquisition number or donation number. It is the serialized embedded-field payload for the reproduction-to-original record link. Whether `411999008601` is separately addressable in the current public platform is a later lookup question.

## 6. `00O003570` boundary

The first-party note still says only `铜壶漏箭制度另拍在00O003570`. No reviewed field labels `00O003570` as a call number, barcode, accession number, donation number or current SYS. It remains `SEPARATE_PHOTOGRAPH_REFERENCE_ONLY`.

## 7. Acquisition-provenance firewall

The current item record does not settle how the Tieqin copy entered Beijing Library/NLC. The 1959 target entries lack `瞿捐`, while the same catalog uses that mark elsewhere; NLC historical material shows the Qu-family transfer used both sale and donation channels; secondary research reports not finding these two works in the separate donation list. This narrows the problem but does not authorize selecting a target-specific route. Final acquisition/transfer path remains `UNRESOLVED`.

## 8. Transmission-genealogy consequence

12FH adds `CATALOG-NLC-CURRENT-ZHUNZHAI-SYS001775083-UIDUCS01003828993` and `TG-E0111` as a current-record `ATTESTS` edge to the 1823 Huang Shiliju physical-copy node. It also strengthens the existing OPAC microfilm/source-record node and physical-copy node. No `SAME_OBJECT`, direct-copy or Sanming-parent edge is authorized.

## 9. Chronology / product firewall

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

1. locate the current NLC `銅壺漏箭制度` record and test whether its local holdings locator carries `NLC:SBYL:03482`, closing both halves of the composite current locator;
2. determine the exact first-party identifier class/current route of `00O003570`;
3. test whether linked record-control `411999008601` is separately addressable and preserve its relationship to SYS `001775083`;
4. continue Qu-family sale/donation/transfer/accession archival research without converting catalog silence into a target-specific verdict;
5. keep the pre-1578 Zhunzhai and Sanming/Yueling Dahan–Rainwater + Nanjing-59 lines active in parallel.

Research record: `docs/research/ZIWEI-NLC-CURRENT-SYS-ITEM-HOLDINGS-LOCATOR-R1.json`.
