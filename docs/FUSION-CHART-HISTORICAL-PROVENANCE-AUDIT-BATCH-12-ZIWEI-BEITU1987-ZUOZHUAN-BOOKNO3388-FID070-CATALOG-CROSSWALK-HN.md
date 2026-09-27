# Fusion Chart Historical Provenance Audit R1 — Batch 12HN

## 1987《北京图书馆古籍善本书目·经部》书号 3388 与 NLC FID 412004000070 旧著录对象交叉闭合

Status: **1987 CATALOG BOOK NUMBER 3388 DIRECTLY BOUND TO EXACT YUAN-ENGRAVED / MING-REPAIRED 32-BOOK ZUOZHUAN ENTRY / FID070 ↔ 3388 HIGH-CONFIDENCE CATALOG-PROFILE CLOSURE / LEADING-ZERO SEMANTIC FIREWALL CLOSED / CURRENT SYS-UID-905S UNRESOLVED / TIEQIN SAME-OBJECT STILL STRONGLY-COMPATIBLE-NOT-PROVED / ZERO PRODUCT OR MATRIX CHANGE**

## 1. Why this batch

12HM closed:

```text
1985 NLC microfilm 455 original control
    412004000070
        ↕
NLC-backed digital FID
    412004000070
```

and fixed the original's old-catalog profile as:

```text
《附释音春秋左传注疏》
六十卷
元 + 明重修
善本 / 刻本 / 重修
32册
```

But 12HM still lacked a historical Beijing Library book number and therefore could not identify a shelf/catalog-number layer.

12HN directly inspects the 1987 Beijing Library rare-book catalog scan.

## 2. Source integrity

Public scan:

```text
《北京图书馆古籍善本书目·经部》
北京图书馆
1987

PDF pages = 210
PDF SHA256 =
9cb2ab3ff5d00fda316a9f0430096ca2a5e68fcd53609a878c0ed9d08a26d3ab
```

The visual evidence package re-downloads that exact PDF, verifies the PDF hash, and renders only the controlling pages without OCR:

```text
run      = 36309374568
artifact = 10928625832
zip sha256 =
af7d8e6769c22b50caf30ed8ff263ca6371a8637bc7d9f36427845f37b778762

PDF 9   render sha256 =
6a53ed59d695cb5b089ab5083aba60c217f8e1af21e3fe2c43e682fe96a9f5c6
PDF 10  render sha256 =
5c9cde7428bd5abe406e863137df346b86de182fd96649bf470c3da643276b3c
PDF 103 render sha256 =
621692e2ebb98819221ccc7833226cb44f50f2debbc90280e98e849a3d5ae652
PDF 104 render sha256 =
04c1c3a8a33aaa3b401db2fd6ddcc77455a94098f01cc178a284ea8b2f42b6ce
PDF 105 render sha256 =
a03a4d4cbb06caa482cc35514626aa728c1f8f48d0ef4cf4297f506c2d81c10f

OCR_USED=false
COLLATION=manual visual review of hash-bound renders
```

## 3. The catalog itself defines the number layer

The catalog's own 编例, fifth rule, item 7 states:

```text
书号：各书名下方，均注明书号。
书号前加零字头的，系一九三七年以前之本馆旧藏。
```

This is important for two reasons.

First, the number physically printed under a title is expressly a **书号**.

Second, a leading zero is **not a neutral padding convention** in this catalog. The catalog assigns a historical-collection meaning to it.

Therefore:

```text
3388 -> 03388 automatic normalization = FORBIDDEN
```

unless a later/current NLC record directly supplies that normalized value.

## 4. Exact target entry and direct book-number binding

The relevant entry is on printed page 92 / PDF page 104.

Manual visual collation reads:

```text
附釋音春秋左傳註疏六十卷
晉杜預注
唐孔穎達疏
唐陸德明釋文

元刻明修本
三十二冊

十行十七字
小字雙行二十三字
...
```

The book number physically aligned beneath that exact entry is:

```text
三三八八
= 3388
```

The adjacent printed pages 91–93 / PDF pages 103–105 were reviewed as one continuous catalog group. Within that reviewed group there is only one entry combining:

```text
《附釋音春秋左傳註疏》六十卷
+ 元刻明修本
+ 三十二冊
```

Other adjacent witnesses differ by edition, extent, or both.

Thus:

```text
1987 historical catalog book number = 3388
```

is directly closed for this exact catalog entry.

## 5. Crosswalk to FID 412004000070

12HM's independent NLC microfilm layer says the original bound to `455$1 = 001412004000070` is:

```text
附释音春秋左传注疏
刻本
32册
善本 / 重修
元[1271-1368]
明[1368-1644]重修
```

The public NLC-backed FID070 object independently consists of exactly 32 digital books covering the complete sixty-juan work.

The 1987 catalog entry is:

```text
same title/work
same 60-juan extent
same Yuan + Ming-repair catalog classification
same 32-book extent
same NLC/Beijing Library institutional object family
```

and is unique at that exact profile within the contiguous catalog group reviewed.

Adjudication:

```text
FID070 -> 1987 BOOK NUMBER 3388
= HIGH_CONFIDENCE_CLOSED_AT_CATALOG_PROFILE_AND_CONTIGUOUS_GROUP_LEVEL
```

This is not falsely described as a direct shared-identifier join: the 1985 455 record does not itself print `3388`.

## 6. Current NLC identifier boundary

A first-party `meta.nlc.cn` probe tested:

```text
3388
03388
SBYL:03388
NLC:SBYL:03388
title + 3388
title + 03388
traditional-title routes
```

Results:

```text
3388            -> no matching result
03388           -> no matching result
SBYL:03388      -> no matching result
NLC:SBYL:03388  -> server error
title + 3388    -> false-positive modern knitting book
title + 03388   -> no matching result
traditional title routes -> timeout in this run
```

Probe:

```text
run      = 36308947738
artifact = 10928431008
zip sha256 =
4b6611283d81f36e6b3f291bc0a90bd5bb6c6ee098206d1bdadb59ea799560f4
```

These are route/index observations only.

Current status:

```text
CURRENT SYS      = UNRESOLVED
CURRENT UID      = UNRESOLVED
CURRENT 905s     = UNRESOLVED
CURRENT SHELFMARK= UNRESOLVED

HISTORICAL 3388 == CURRENT 905s
= NOT PROVED
```

## 7. Tieqin identity firewall

The official NOPSS report remains highly compatible:

```text
NLC Tieqin Tongjian Lou old-collection copy
old classification = 元刻明修本
physical re-adjudication = 元刻元印十行本
```

12HN now adds a historically numbered Beijing Library entry, `3388`, whose old classification and extent converge with FID070.

But the reviewed Zhang report still does **not** print `3388`, nor has a Tieqin seal/current NLC record been directly bound to FID070.

Therefore the forward-only adjudication remains:

```text
3388 = strong historical candidate for Zhang's examined copy
FID070 == Zhang Tieqin physical copy
= STRONGLY_COMPATIBLE_NOT_PROVED

SAME_OBJECT_EDGE_AUTHORIZED=false
```

No evidentiary shortcut is taken merely because the match is persuasive.

## 8. HJ and target-volume firewalls

12HN does not identify Zhao Wanli's 1951 named Song-printed member.

```text
HJ 宋刻《春秋左传注疏》 == FID070
= UNRESOLVED
```

The target `《铜壶漏箭制度》 / 《准斋心制几漏图式》` and historical catalog numbers `3482 / 3483` are not named in this batch. Their acquisition path remains unchanged.

## 9. Product / Matrix consequence

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

## 10. Highest next gate

1. recover Zhang Lijuan's 2018 full article or another direct NLC/Tieqin source that explicitly prints `3388` or its current successor identifier;
2. probe rare-book-specific / legacy NLC catalog routes using literal historical `3388`, **without** automatic zero-padding;
3. directly inspect FID070 provenance leaves for Tieqin/Huang-family seals or unique annotations;
4. keep Zhao 1951 and target 3482/3483 mappings separately unresolved.

Research record: `docs/research/ZIWEI-BEITU1987-ZUOZHUAN-BOOKNO3388-FID070-CATALOG-CROSSWALK-R1.json`.
