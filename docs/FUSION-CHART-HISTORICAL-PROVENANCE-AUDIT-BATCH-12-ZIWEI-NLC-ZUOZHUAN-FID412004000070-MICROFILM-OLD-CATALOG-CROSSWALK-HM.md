# Fusion Chart Historical Provenance Audit R1 — Batch 12HM

## 国图《附释音春秋左传注疏》FID 412004000070：1985 缩微旧著录与数字对象交叉闭合

Status: **NLC 1985 MICROFILM 455 ORIGINAL-CONTROL → FID 412004000070 CLOSED / OLD CATALOG PROFILE = YUAN + MING REPAIR + RARE BOOK + 32 BOOKS / COMMONS NLC BACKUP = EXACTLY 32 DIGITAL BOOKS, JUAN 1–60 / ZHANG TIEQIN-YUAN IDENTITY STRONGLY COMPATIBLE NOT PROVED / MODERN NLC SYS-UID-905S STILL UNRESOLVED / ZERO PRODUCT, MATRIX OR RUNTIME CHANGE**

## 1. Why this batch matters

Batch 12HL separated two National Library of China witnesses:

- `fid 412004000069`: the NLC half of the split Song Liu Shugang copy;
- Zhang Lijuan's separately researched Tieqin Tongjian Lou old-collection ten-line witness, physically re-adjudicated as Yuan-engraved / Yuan-impression.

The remaining high-value question was whether a second NLC digital object could be tied to the older catalog description that Zhang says was later corrected.

12HM finds exactly such an object-level chain, but deliberately stops one step before claiming the Tieqin identity itself.

## 2. NLC 1985 microfilm old-catalog layer

Two current NLC microfilm records independently describe the same original.

### 2.1 Work/master-style record

```text
SYS  = 003416361
UID  = UCS01003624709
year = 1985
extent = 3盘卷片(76米1520拍)

455a = 附释音春秋左传注疏 / 刻本 / 32册
455b = 善本 / 重修
455d = 元[1271-1368] / 明[1368-1644]重修 / 28cm
4551 = 001412004000070 / 2001^ / 205^^ / 210^^ / 215^^

905b = 00O003551
```

As established by the project's earlier 905$b semantic audit, `00O003551` is a microfilm registration/login-number layer. It is **not** the original rare-book shelfmark.

### 2.2 Distribution-copy record

```text
SYS  = 003026493
UID  = UCS01003601976
edition = 发行拷贝片

455a = 附释音春秋左传注疏 / 刻本 / 32册
455b = 善本 / 重修
455d = 元[1271-1368] / 明[1368-1644]重修 / 28cm
4551 = 001412004000070 / 2001 / 205 / 210 / 215
```

Both records therefore independently carry the same embedded original-record identifier:

```text
412004000070
```

This closes the old-catalog/microfilm link. It does not yet provide the modern original rare-book `SYS / UID / 905s`.

Probe:

```text
run      = 36306742308
artifact = 10927501723
sha256   = 7d4e53ec9359d6575e0c8bbe41b01c7a0f068949b4dbb208bdcadf8ca941954b
OCR_USED = false
```

## 3. FID 412004000070 public digital-object control

The Wikimedia Commons NLC library-backup index exposes:

```text
《附釋音春秋左傳註疏》〔晉〕杜預注
FID = 412004000070
32 PDF books
```

The run is complete from:

```text
第1冊  = 卷首 / 卷第一 / 卷第二
...
第32冊 = 卷第五十九 / 卷第六十
```

The file-list page is:

```text
https://commons.wikimedia.org/wiki/Commons:Library_back_up_project/file_list/NLC/%E6%95%B8%E5%AD%97%E5%8F%A4%E7%B1%8D/15
```

Commons imageinfo exposes National Library of China credit on the file objects. Thus the public backup independently agrees with the 1985 original-description book count:

```text
1985 old catalog: 32册
FID 070 backup:   32 digital books
```

The current NLC `read.nlc.cn` route timed out from the GitHub runner. Current `meta.nlc.cn` ANY search by literal FID `412004000070` returned `no matching result`. Those are route/index boundaries only; neither is evidence that the object or a modern catalog record is absent.

Probe:

```text
run      = 36307000456
artifact = 10927901472
sha256   = 336bc804383c2ed400ffd16616e6411f127b6b549ab55c25040ae1117c08daf6
OCR_USED = false
```

## 4. Relation to Zhang Lijuan's Tieqin witness

The official National Social Science Fund project report says that NLC holds a Tieqin Tongjian Lou old-collection ten-line `《附释音春秋左传注疏》` and records:

```text
旧著录：元刻明修本
实物研究：元刻元印十行本
```

The 1985 FID-070-linked old-catalog description is:

```text
元[1271-1368]
明[1368-1644]重修
善本
32册
```

This is a highly specific compatibility bridge. It explains exactly the type of stale catalog classification Zhang later corrected.

However, 12HM still lacks one of the following decisive object bridges:

- an explicit `铁琴铜剑楼` provenance note on FID 070;
- a modern NLC rare-book shelfmark / `905s` crosswalk;
- an accession/donor record;
- a readable ownership seal;
- a unique defect/page fingerprint explicitly tied to Zhang's examined copy.

Adjudication:

```text
FID070 == 1985 MICROFILM ORIGINAL CONTROL
  = CLOSED

FID070 == ZHANG TIEQIN-YUAN COPY
  = STRONGLY_COMPATIBLE_NOT_PROVED

SAME_OBJECT_EDGE
  = NOT AUTHORIZED
```

No numerical adjacency with FID 069 is used as evidence.

## 5. Relation to HJ's 1951 Song-printed member

HJ names:

```text
宋刻《春秋左传注疏》
```

FID 070 belongs to the Yuan/Ming-repair **old-catalog profile** and cannot be reassigned to Zhao Wanli's 1951 Song-printed donated member without an acquisition-era bridge.

Therefore:

```text
HJ MEMBER == FID070
  = UNRESOLVED
```

The distinct FID 069 Song split-copy track remains governed by 12HL.

## 6. Target-volume firewall

This batch does not name or alter:

- `《铜壶漏箭制度》`;
- `《准斋心制几漏图式》`;
- `3482 / 3483`;
- `03482 / 03483`.

No target-specific purchase, donation, or Ding-intermediary route is selected.

## 7. Product / Matrix / genealogy consequence

```text
MATRIX_COUNT_CHANGE=false
RUNTIME_RULE_CHANGE=false
ALGORITHM_REOPEN=false
CANDIDATE_COLLAPSE=false
TIEQIN_SAME_OBJECT_EDGE_AUTHORIZED=false
ACQUISITION_EDGE_AUTHORIZED=false
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains:

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance metadata defects = 14 / 14 repaired
confirmed chart algorithm defects = 0
```

## 8. Highest next gate

1. recover an explicit Tieqin provenance/ownership seal or NLC catalog note for FID 412004000070;
2. resolve Zhang's exact current NLC `SYS / UID / 905s` or shelfmark;
3. directly review Zhang Lijuan's 2018/2023 article pages for an identifier or physical fingerprint when lawfully accessible;
4. keep Zhao 1951 and target 3482/3483 acquisition-object mappings unresolved until their own bridges are found.

Research record: `docs/research/ZIWEI-NLC-ZUOZHUAN-FID412004000070-MICROFILM-OLD-CATALOG-CROSSWALK-R1.json`.
