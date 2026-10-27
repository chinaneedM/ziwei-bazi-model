# Fusion Chart Historical Provenance Audit R1 — Batch 12HL

## 国图 `fid 412004000069` 与台北故宫半部宋刘叔刚本：物理分流闭环

Status: **NPM FIRST-PARTY SPLIT-COPY STATEMENT + NPM-SOURCED EXTENT METADATA + NLC-BACKED FID EXTENT CONVERGE / FID 412004000069 HIGH-CONFIDENCE IDENTIFIED AS NLC HALF OF SPLIT SONG LIU SHUGANG COPY / PHYSICAL DISTINCTNESS FROM ZHANG TIEQIN-YUAN WITNESS RESOLVED / 1951 DONATION OBJECT STILL UNRESOLVED / ZERO PRODUCT, MATRIX OR RUNTIME CHANGE**

## 1. Why this batch exists

Batch 12HK correctly refused to collapse two National Library of China descriptions merely because both were ten-line `《附释音春秋左传注疏》` witnesses:

- digital `fid 412004000069`, displayed as Liu Shugang / Song;
- Zhang Lijuan's physically examined Tieqin Tongjian Lou old-collection copy, re-adjudicated as Yuan-engraved / Yuan-impression.

HK left their physical distinctness **UNRESOLVED** because no stable object bridge had yet been found.

12HL adds a cross-institutional copy-extent bridge from the National Palace Museum.

## 2. National Palace Museum first-party split-copy statement

The National Palace Museum's 2025 official exhibition page `皕宋──故宮宋版圖書觀止` records:

```text
附釋音春秋左傳註疏
宋建安劉叔剛刊元修配補元刊明印十行本
故善001224-001238
```

and explicitly states:

```text
今由本院與中國國圖各存其半
```

Source:

```text
https://theme.npm.edu.tw/exh114/TwoHundredTreasures/ch/page-8.html
```

This is a first-party museum statement about one split Song Liu Shugang copy, not a generic same-title comparison.

## 3. NPM half extent

The Digital Archives union record, whose source field points to the National Palace Museum Ancient Books and Maps system, binds the same object ID:

```text
統一編號：故善001224-001238
版本：宋建安劉叔剛一經堂刊配補元刊明修十行本
保存現況：缺卷一－二十九。
總冊數：十五冊
```

Source:

```text
https://catalog.digitalarchives.tw/item/00/12/60/56.html
```

Therefore the NPM-held half is missing juan 1-29. Combined with the NPM first-party statement that NPM and NLC each hold half, the complementary NLC half is the juan 1-29 side.

This inference is explicitly scoped to copy extent; it does not invent a modern NLC shelfmark.

## 4. Match to NLC fid 412004000069

The already-registered NLC-backed digital object has:

```text
fid = 412004000069
display = 劉叔剛 / 宋
book count = 15
book 1 = 卷首 / 卷一 / 卷二
book 15 = 卷二十八 / 卷二十九
```

The convergence is now multi-dimensional:

1. Liu Shugang Song ten-line edition identity;
2. NPM says NPM/NLC each hold half;
3. NPM half is fifteen books and lacks juan 1-29;
4. NLC fid is fifteen books and terminates at juan 29.

Adjudication:

```text
FID_412004000069_MATCHES_NLC_HALF_OF_SPLIT_SONG_COPY
  = HIGH_CONFIDENCE_CLOSED_AT_CROSS_INSTITUTIONAL_EXTENT_AND_DIGITAL_METADATA_LEVEL

EXACT_MODERN_NLC_SHELFMARK_FOR_FID
  = UNRESOLVED
```

## 5. Forward revision of HK physical-distinctness status

The official NOPSS project report independently identifies Zhang Lijuan's NLC witness as:

```text
铁琴铜剑楼旧藏
旧著录：元刻明修本
实物研究：元刻元印十行本
```

12HL therefore closes the HK object-level branch as:

```text
fid 412004000069 == NLC half of split Song Liu Shugang copy
  = HIGH-CONFIDENCE CLOSED

fid 412004000069 == Zhang Tieqin-Yuan physical copy
  = RESOLVED FALSE

PHYSICAL DISTINCTNESS
  = RESOLVED DISTINCT

SAME-PHYSICAL-OBJECT COLLAPSE
  = FORBIDDEN
```

HK is not rewritten. Its earlier `UNRESOLVED` status remains historically auditable; 12HL is the forward-only revision.

The exact modern shelfmark/digital identifier of Zhang's Tieqin-Yuan copy remains unresolved.

## 6. Why this still does not identify Zhao Wanli's 1951 member

HJ's quotation names:

```text
宋刻《春秋左传注疏》
```

Physical separation of the two NLC witnesses does **not** prove which object Zhao meant.

The historical Tieqin catalog itself uses layered language about Song carving and Yuan-period impression. Without a 1951 accession, donor, shelfmark, provenance seal, or contemporaneous catalog crosswalk, the project must not infer:

```text
HJ MEMBER == fid 412004000069
HJ MEMBER == Zhang Tieqin-Yuan copy
```

Both remain unresolved at the acquisition-object layer.

## 7. Target-volume firewall

12HL is a comparator-object provenance batch. It does not name or alter:

- `《铜壶漏箭制度》`;
- `《准斋心制几漏图式》`;
- `3482 / 3483`;
- `03482 / 03483`.

No purchase, donation, or Ding-intermediary route is selected.

## 8. Product / Matrix / genealogy consequence

```text
MATRIX_COUNT_CHANGE=false
RUNTIME_RULE_CHANGE=false
ALGORITHM_REOPEN=false
CANDIDATE_COLLAPSE=false
ACQUISITION_EDGE_AUTHORIZED=false
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

The object comparison is outside the current Ziwei textual transmission graph, so no genealogy node/edge is added. The rejected same-object relation is recorded in this batch evidence.

Accounting remains:

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance metadata defects = 14 / 14 repaired
confirmed chart algorithm defects = 0
```

## 9. Highest next gate

1. Resolve the modern NLC shelfmark/accession/digital ID of Zhang Lijuan's Tieqin-Yuan copy on its now-separate object track.
2. Recover a 1951-era accession/donor/shelfmark/provenance bridge that binds Zhao Wanli's donated Song-printed member to a concrete NLC object.
3. Directly collate Zhao 1951 pp.221–233 / 2011 p.197, Liu Bo 2018 pp.309–310, and the 1997 Beijing Library history pp.446–449 when lawfully accessible.
4. Keep the 3482/3483 target acquisition path unresolved until target-specific evidence appears.

Research record: `docs/research/ZIWEI-NLC-ZUOZHUAN-412004000069-NPM-SPLIT-SONG-COPY-PHYSICAL-DISTINCTNESS-R1.json`.
