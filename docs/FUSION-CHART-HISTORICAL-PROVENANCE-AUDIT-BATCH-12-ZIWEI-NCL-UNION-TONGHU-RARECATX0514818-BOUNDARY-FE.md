# Fusion Chart Historical Provenance Audit R1 — Batch 12FE

## 國圖聯合目錄 `rarecatx0514818`：閉合公開記錄身份，明確阻止把資料庫登錄號升格為實體唯一索書號

Status: **OFFICIAL UNION-CATALOG RECORD IDENTITY CLOSED / RARECATX0514818 = PUBLIC REGISTRATION-RECORD IDENTIFIER / UNIQUE PHYSICAL SHELFMARK NOT EXPOSED / SAME NLC HUANG COPY FAMILY HIGH-CONFIDENCE / EXACT PHYSICAL COPY NOT PROVED / HUANG 原書舊鈔・錄副 FIREWALL PRESERVED / NO PRE-1578 RULE CLOSURE / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12FD directly identified the lower collector's seal on the current NLC/Xuxiu1031 Copper title page as **鐵琴銅劍樓**, closing the object's later Tieqin-collection provenance. It still withheld exact unique-object collapse because a collection seal can occur on multiple books and Huang Pilie's 1823 paratext independently preserves multiple copy layers:

```text
原書舊鈔 != 錄副
```

The next object-level gate was therefore narrower:

> Can an official catalog/holding surface expose a unique physical shelfmark, acquisition/donation number, or other one-object identifier tying the current NLC Copper/Zhunzhai composite object to the specific copy described in the Tieqin catalog?

## 2. Official union-catalog surface

The committed source-bound research record identifies the official National Central Library (Taiwan) Chinese Rare Books Union Catalog detail surface for 《銅壺漏箭制度》.

Observed public fields:

```text
書名 / title:       銅壺漏箭制度
版本 / version:     抄本
附註 / note:        清黃丕烈跋
登錄號:              rarecatx0514818
來源:                國家圖書館中文古籍聯合目錄
現藏:                中國國家圖書館
國別:                中國
```

The exposed field is explicitly labelled **登錄號**.

## 3. Identifier adjudication

The safe identity statement is:

```text
rarecatx0514818
    = public union-catalog registration / record identifier
    != proved unique physical shelfmark
    != proved China-NLC call number
    != acquisition/donation number
    != Tieqin-era shelfmark
```

The reviewed public surface does not expose a separate:

- 索書號 / call number;
- China NLC shelfmark;
- old registration / accession number;
- acquisition or donation number;
- Tieqin-era item number;
- unique physical-object identifier.

Therefore the project must not silently reclassify `rarecatx0514818` as a unique book identifier.

## 4. What the record does bind

The official record strongly converges with the current NLC Huang-family Copper copy route through four features:

- title 《銅壺漏箭制度》;
- manuscript/copy class;
- Huang Pilie paratext association (`清黃丕烈跋`);
- current holder = 中國國家圖書館.

This supports:

```text
current NLC/Xuxiu1031 Huang-family Copper object
    ↔
rarecatx0514818 catalog record
    = HIGH_CONFIDENCE_SAME_NLC_HUANG_COPY_FAMILY
```

But the public union-catalog surface itself does **not** expose:

- 道光三年 / 1823;
- 黃氏士禮居;
- 準齋心製几漏圖式合裝;
- 士禮居藏 / 黃印丕烈 / 蕘圃 seals;
- 鐵琴銅劍樓 seal;
- a unique physical shelfmark.

So the record alone cannot formally prove exact identity with the reviewed 1823 composite object.

## 5. Zhunzhai companion-record boundary

No exact-title official union-catalog record for 《準齋心製几漏圖式》 was closed on the current search horizon.

This is recorded only as an **access/search-horizon result**:

```text
exact-title record located = false
absence claim authorized = false
```

Failure to locate an indexed result is not evidence that the union catalog lacks such a record.

## 6. Copy-layer, chronology and rule firewalls

Batch 12FE does not decide:

- whether the reviewed 1823 object is Huang's 原書舊鈔 or 錄副;
- whether it is exactly the 1827 Airijinglu 從吳門黃氏藏舊抄本;
- whether it is the unique physical object described by the reviewed Tieqin catalog entry;
- whether any surviving Song physical exemplar exists;
- whether exact 25-arrow prose is physically attested before 1578;
- whether the Yuan 1281 Yanling Sun Fengji is exactly the Zhunzhai author;
- whether Zhunzhai is a direct parent of the Sanming/Yueling table;
- whether the Nanjing-59 endpoint is directly bound to the Sanming/Yueling target.

Thus:

```text
direct Sanming-parent vote increment = 0
algorithm reopen = 0
candidate collapse = 0
deterministic product = CLOSED
```

## 7. Transmission-genealogy consequence

Batch 12FE adds a catalog-record node:

```text
CATALOG-NCL-UNION-TONGHU-RARECATX0514818
```

and records TG-E0108 as a **HIGH_CONFIDENCE / ATTESTS** catalog-to-current-copy-family binding.

The edge is deliberately scope-limited:

- it records a high-confidence record-level binding to the same NLC Huang copy family;
- it does not create a SAME_OBJECT edge;
- it does not claim that `rarecatx0514818` is a physical shelfmark;
- it does not collapse Huang's multiple copy layers.

## 8. Project accounting

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
MISSING_FROM_PRODUCT=10
PROVENANCE_DEFECTS=13/13_REPAIRED
CONFIRMED_CHART_ALGORITHM_DEFECTS=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
DIRECT_SANMING_PARENT_VOTE_INCREMENT=0
DETERMINISTIC_PRODUCT=CLOSED
```

No Matrix row changes and no provenance-defect increment are authorized.

## 9. Next gate

1. Search China NLC OPAC / rare-book catalogs / archival descriptions for a physical call number, old registration/accession number, acquisition/donation field, or other one-object identifier tied to 《銅壺漏箭制度》.
2. Continue searching for an official 《準齋心製几漏圖式》 companion record and test whether it shares any object-level identifier with `rarecatx0514818`.
3. Keep database record IDs, catalog identifiers, collection seals and physical shelfmarks as separate identifier classes.
4. Keep the pre-1578 Zhunzhai rule line and the independent Sanming/Yueling Dahan–Rainwater + Nanjing-59 lines active.

Research record: `docs/research/ZIWEI-NCL-UNION-TONGHU-RARECATX0514818-BOUNDARY-R1.json`.
