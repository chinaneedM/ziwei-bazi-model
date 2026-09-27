# Fusion Chart Historical Provenance Audit R1 — Batch 12HK

## 国图《附释音春秋左传注疏》：数字号 412004000069 与铁琴旧藏元本身份分流防火墙

Status: **NLC DIGITAL FID 412004000069 CONCRETE OBJECT METADATA CLOSED THROUGH PUBLIC BACKUP / OFFICIAL NOPSS REPORT CLOSES A TIEQIN-OLD-COLLECTION YUAN-ENGRAVED YUAN-IMPRESSION NLC WITNESS / GENERIC TITLE + TEN-LINE FORMAT INSUFFICIENT FOR SAME-OBJECT COLLAPSE / PHYSICAL DISTINCTNESS AND HJ DONATED-MEMBER IDENTITY STILL UNRESOLVED / ZERO PRODUCT, MATRIX, RUNTIME OR GENEALOGY CHANGE**

## 1. Why this batch matters

12HJ introduced a concrete member anchor inside Zhao Wanli's quoted 62-title Qu-family donation group:

```text
宋刻《春秋左传注疏》
```

A tempting public digital candidate is NLC fid `412004000069`. But version research shows that the National Library also has a Tieqin Tongjian Lou old-collection ten-line witness whose modern physical adjudication is Yuan, not simply Song.

12HK prevents those records from being collapsed merely because their title and page layout are close.

## 2. NLC digital fid 412004000069

The public backup identifies its source as:

```text
National Library of China
中華古籍資源庫 數字古籍
fid = 412004000069
```

Displayed metadata:

```text
附釋音春秋左傳注疏 六十卷
劉叔剛 宋[960-1279]
刻本
十行十六至十七字
小字雙行二十三字
細黑口 左右雙邊 雙魚尾
```

The observed backup sequence is 15 books. Book 1 contains `卷首 / 卷一 / 卷二`; book 15 contains `卷二十八 / 卷二十九`.

The source-emitted NLC detail URL resolves to fid 412004000069, but the first-party page timed out in the reviewed web interface. The public backup PDFs were not imported into the repository and no seal/glyph claim is made from them.

## 3. Tieqin old-collection Yuan witness

The official National Social Science Fund project report for Zhang Lijuan's `《春秋左传》校注及研究` says that NLC holds:

```text
一部铁琴铜剑楼旧藏十行本《附释音春秋左传注疏》
```

and records the version-adjudication change:

```text
旧著录：元刻明修本
实物研究：元刻元印十行本
```

The report emphasizes that the copy shows no Ming repair/recarving traces and preserves the Yuan ten-line form.

The report does **not** expose the modern NLC shelfmark or digital fid in the reviewed text.

## 4. Historical Tieqin catalog control

The public transcription of `《铁琴铜剑楼藏书目录》` contains a 60-juan entry with:

```text
旧藏黄氏百宋一廛
十行 / 行十七字
注疏双行 / 行二十三字
```

Its historical version language is layered: it first describes the book as Southern-Song carving, then reasons that the observed impression must be Yuan-period.

That historical record is highly relevant to the Tieqin witness, but it is not a unique modern object identifier.

## 5. Identity bifurcation

Current adjudication:

```text
fid 412004000069 == Zhang Tieqin-Yuan copy
  = NOT PROVED

PHYSICAL DISTINCTNESS
  = UNRESOLVED

GENERIC TITLE IDENTITY
  = SAME WORK FAMILY

TEN-LINE FORMAT SIMILARITY
  = HIGH-INFORMATION BUT NONUNIQUE

SAME-OBJECT COLLAPSE
  = FORBIDDEN
```

A stale or inherited catalog classification is possible. Conversely, separate physical copies are also possible. The project does not choose between these without a stable object bridge.

Required bridge types:

- NLC shelfmark/accession crosswalk;
- readable provenance/ownership seal;
- unique physical defect/page fingerprint;
- first-party catalog statement explicitly linking the fid to Tieqin provenance.

## 6. Consequence for HJ

The 1951 quotation's:

```text
宋刻《春秋左传注疏》
```

remains object-level unresolved.

```text
HJ MEMBER == fid 412004000069
  = UNRESOLVED

HJ MEMBER == Tieqin-Yuan witness
  = UNRESOLVED
```

No title is added to the 62-title list beyond the already closed generic member anchor.

## 7. Target-volume firewall

This batch is a comparator/provenance-object audit for the HJ member. It does not name or alter the target:

- 《铜壶漏箭制度》;
- 《准斋心制几漏图式》;
- 3482 / 3483;
- 03482 / 03483.

No purchase/donation/Ding route is selected.

## 8. Product / genealogy consequence

```text
NODES_ADDED=0
EDGES_ADDED=0
SAME_OBJECT_EDGE_AUTHORIZED=false
ACQUISITION_EDGE_AUTHORIZED=false
RUNTIME_RULE_CHANGE=false
ALGORITHM_REOPEN=false
CANDIDATE_COLLAPSE=false
MATRIX_COUNT_CHANGE=false
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains `198 / 166 / 10`; provenance metadata defects `14 / 14 repaired`; chart algorithm defects `0`.

## 9. Highest next gate

1. Resolve the modern shelfmark/accession/digital identifier for Zhang's Tieqin-Yuan NLC copy.
2. Recover a provenance seal/crosswalk for fid 412004000069.
3. Only then bind HJ's donated Song-printed member to a physical object.
4. Continue direct 1951/2011 page collation, 2018 pp.309–310 and 1997 pp.446–449 in parallel.

Research record: `docs/research/ZIWEI-NLC-ZUOZHUAN-412004000069-TIEQIN-YUAN-IDENTITY-BIFURCATION-FIREWALL-R1.json`.
