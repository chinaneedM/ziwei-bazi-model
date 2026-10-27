# Fusion Chart Historical Provenance Audit R1 — Batch 12HO

## NLC FID 412004000070 卷首递藏印：直接实物视觉边界

Status: **FID070 DIRECT IMAGE REVIEW COMPLETED / BOOK1 FRONT LEAF CONTAINS PHYSICAL PROVENANCE-SEAL TRACES / SEAL TEXT NOT DIRECTLY READABLE / BOOKS 2, 16, 32 STRATEGIC LEAVES ADD NO CLEAR REPEATED SEAL / AUTHORITATIVE HUANG & TIEQIN SEAL COMPARATORS REVIEWED / SAME-OBJECT IDENTITY NOT PROMOTED / ZERO PRODUCT, MATRIX OR RUNTIME CHANGE**

## 1. Why this batch

12HN closed a historical catalog-number layer:

```text
FID 412004000070
  ↕ strong catalog-profile convergence
1987 北京图书馆古籍善本书目
  book no. 3388
  元刻明修本
  三十二册
```

but exact identity with Zhang Lijuan's Tieqin Tongjian Lou old-collection Yuan-impression copy remained unproved.

12HO moves from bibliographic metadata to direct physical-page review.

## 2. Book 1 direct visual control

Target:

```text
File:NLC892-412004000070-117576
《附釋音春秋左傳註疏》第1冊.pdf
Commons pageid = 124222155
source credit = National Library of China

PDF SHA1 =
b3ea46433dc5df7b056ac2b0fcf4c8d869aec151

PDF SHA256 =
619451dbde84e806293d155a84f21f584e728107d08a139fcdc7ed335cd2ff8a

pages = 67
```

Probe:

```text
run      = 36309706422
artifact = 10928835321
zip sha256 =
509ed98388f6941cc6226eddee7184de039b0f481cde36ea21740dd2a8681f48

OCR_USED=false
```

Reviewed:

```text
front = pp.1-16
tail  = pp.64-67
```

The key leaf is PDF page 2.

Direct visual adjudication:

```text
PHYSICAL_PROVENANCE_SEAL_TRACES_VISIBLE=true

DARK_TITLE_TEXT_OVERLAPS_PALE_SEAL_TRACES=true

DIRECTLY_READABLE "百宋一廛"=false
DIRECTLY_READABLE "鐵琴銅劍樓"=false
DIRECTLY_READABLE QU-FAMILY NAME=false

EXACT_SEAL_COUNT=UNRESOLVED
UNIQUE_SEAL_FINGERPRINT=CANNOT_CLOSE
```

This is a positive material observation: the target object really does carry provenance-seal traces on its opening leaf.

It is **not** a positive reading of the seal text.

## 3. Same-object repeated-seal strategy

To avoid guessing from one faded stamp, 12HO independently discovered all 32 Commons file objects for FID070 and selected books 2, 16 and 32.

Probe:

```text
run      = 36311131378
artifact = 10929560901
zip sha256 =
25980acc777c8b9f27d4d7251a21353aef2a2f0c16e93acb896803d4c05a664b

discovered FID070 file count = 32
OCR_USED=false
```

Controls:

```text
Book 2:
  pageid = 124222161
  PDF SHA1 = 84d35f37387cfb630e1d9d45882591b5350e7a8c
  PDF SHA256 = df966c6149ed8d6c677f0bfdaf6ac29adcdea08b3593f165596fa7ff01ad4ed9
  pages = 58

Book 16:
  pageid = 124222389
  PDF SHA1 = 46b09a9d9ede63906e302ad380dbd5ed8d9489a1
  PDF SHA256 = 9b40b7835ef39aa203879e8b54c301f9fd0c14d0b2f5349629ef03dd226678f5
  pages = 36

Book 32:
  pageid = 124397565
  PDF SHA1 = 783e6facb18fb582cd39ac3e023c35579addc2e8
  PDF SHA256 = 13e0323e849d6025a62a8ad157ca6ac28eba4294a21a738b0f90647e32b625b6
  pages = 57
```

For each selected book, the first 12 and final 5 pages were rendered and visually reviewed.

Result:

```text
DIRECTLY_READABLE_TARGET_PROVENANCE_SEAL_FOUND=false
```

within that bounded strategic review.

This does **not** authorize:

```text
NO_TIEQIN_SEAL_ANYWHERE_IN_FID070
NO_HUANG_SEAL_ANYWHERE_IN_FID070
```

because only selected fascicle boundaries were reviewed.

## 4. Authoritative seal comparators

### 4.1 黃丕烈《百宋一廛》

Central Academia Sinica Fu Ssu-nien Library Digital Archives records:

```text
印主 = 黃丕烈
印文 = 百宋一廛
書體/刻法 = 小篆 / 陰刻
高廣 = 2.73 × 1.31 cm
篆刻者 = 陳鴻壽
```

Source:

```text
https://dap.ihp.sinica.edu.tw/material/41/
```

### 4.2 《鐵琴銅劍樓》

Taiwan National Central Library's 2018 scholarly article
`《古籍裡的風景—國家圖書館的藏書印記初探》`
publishes Figure 7 as:

```text
〈鐵琴銅劍樓〉白文長方印
```

Source:

```text
https://nclfile.ncl.edu.tw/files/201903/638c7a79-fdd5-42f8-ab5a-54f3a45117db.pdf
```

Both are comparator controls only.

A faded target impression may be geometrically compatible with many rectangular/square seals. Shape similarity without readable text or a unique matching fingerprint is not an object identity proof.

## 5. Relation to the historical Tieqin catalog

The historical Tieqin catalog entry for this sixty-juan work records:

```text
旧藏黄氏百宋一廛
```

and the ten-line / seventeen-character format.

12HO therefore establishes that FID070 contains a physical provenance-signal exactly where such a chain might become testable.

But the visual chain currently stops at:

```text
PROVENANCE MARK PRESENT
    ↓
INSCRIPTION UNRESOLVED
```

not at:

```text
PROVENANCE MARK = 百宋一廛 / 鐵琴銅劍樓
```

## 6. Identity adjudication

Forward status:

```text
FID070 == 1985 MICROFILM ORIGINAL CONTROL
= CLOSED

FID070 -> 1987 BOOK NUMBER 3388
= HIGH_CONFIDENCE_CLOSED_AT_CATALOG_PROFILE_AND_CONTIGUOUS_GROUP_LEVEL

DIRECT PROVENANCE MARKS ON FID070
= CLOSED PRESENT ON BOOK1 PAGE2

EXACT PROVENANCE SEAL TEXT
= UNRESOLVED

FID070 == ZHANG LIJUAN TIEQIN-YUAN PHYSICAL COPY
= STRONGLY_COMPATIBLE_NOT_PROVED

SAME_OBJECT_EDGE_AUTHORIZED=false
```

No prior batch is rewritten.

## 7. Current NLC identifier firewall

Still unresolved:

```text
CURRENT SYS
CURRENT UID
CURRENT 905s
CURRENT SHELFMARK
```

And:

```text
3388 -> 03388
= FORBIDDEN WITHOUT DIRECT CURRENT RECORD
```

## 8. HJ / target-volume / product firewalls

No change to:

- Zhao Wanli's 1951 `宋刻《春秋左传注疏》` object mapping;
- `《铜壶漏箭制度》`;
- `《准斋心制几漏图式》`;
- historical target numbers `3482 / 3483`;
- purchase / donation / Ding-intermediary adjudication.

Project consequence:

```text
MATRIX_COUNT_CHANGE=false
RUNTIME_RULE_CHANGE=false
ALGORITHM_REOPEN=false
CANDIDATE_COLLAPSE=false
SAME_OBJECT_EDGE_AUTHORIZED=false
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains:

```text
198 rows
166 audited
10 MISSING_FROM_PRODUCT
14 / 14 provenance metadata defects repaired
0 confirmed chart algorithm defects
```

## 9. Highest next gate

1. recover Zhang Lijuan 2018 full article or another direct source printing `3388`, the current NLC shelfmark, or a Tieqin identifier;
2. seek a cleaner direct image of the same FID070 provenance stamp, but do not infer text from shape;
3. continue literal `3388` legacy/rare-book catalog crosswalk without zero-padding;
4. keep Zhao 1951 and target 3482/3483 paths separately unresolved.

Research record: `docs/research/ZIWEI-NLC-ZUOZHUAN-FID070-PROVENANCE-SEAL-VISUAL-BOUNDARY-R1.json`.
