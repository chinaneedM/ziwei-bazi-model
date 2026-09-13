# Fusion Chart Historical Provenance Audit R1 — Batch 12BE

## 《新編評註通玄先生張果星宗大全》国图联合目录—普林斯顿独立万历二十二年物质见证与图像权限边界

Status: **NLC FIRST-PARTY UNION-CATALOG OBJECT BOUND / PRINCETON EAST ASIAN LIBRARY TC183/2991 / 1593 PREFACE DATE KEPT DISTINCT FROM 1594 COVER IMPRINT / TANG QIAN JUANDUAN + ZHOU WENGUANG COVER IMPRINT DIRECTLY CATALOGUED / INDEPENDENT EXACT-1594 MATERIAL WITNESS +1 / PUBLIC LARGE-IMAGE ENTRY EXISTS BUT PAGE VIEWER IS PERMISSION-GATED / NO TARGET LEAF / ZERO TARGET-TEXT OR HAI-GLYPH VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Question

After Batch 12BD closed the current Shandong hosted-runner access boundary, the next gate was a genuinely independent first-party exact-1593/1594 item record or target leaf. BE asks:

> Can a first-party union catalog bind a physically independent early-Wanli copy, and can its own emitted image route expose the late-Zi target leaf without bypassing access control?

## 2. NLC search route and exact object binding

The National Library of China public HTTP search surface for `searchType=62` is reachable. The source page itself emits the search URL used in this batch. Long/short and traditional/simplified title queries all converge on one exact result:

```text
record/fid=NJPX95-B1857
indexName=data_467
title=新編評註通玄先生張果星宗大全
responsibility=陸位輯校
shelf/collection no=TC183/2991
holder=普林斯顿大学东亚图书馆
```

The exact result-emitted detail page returned HTTP 200 and is the controlling first-party object for this batch.

## 3. Date/imprint philology: 1593 is not silently collapsed into 1594

The NLC detail exposes three different bibliographic statements and they must remain separate:

```text
catalog time=明萬曆癸巳 [21年, 1593]
preface=萬曆癸巳韓擢《張果星宗序》
juanduan=卷端又題「金陵三山益軒唐謙鋟梓」
cover=封面鐫「萬曆閼逢敦牂張果星宗命格大全周氏文光新梓」；萬曆閼逢敦牂即萬曆二十二年
```

Therefore the evidence is adjudicated as:

```text
PREFACE_YEAR=1593
COVER_IMPRINT_YEAR=1594
TANG_QIAN_JUANDUAN_OBSERVED=true
ZHOU_WENGUANG_COVER_IMPRINT_OBSERVED=true
```

The 1593 catalog/preface year is not treated as proof that the physical printing occurred in 1593. The exact-1594 material control comes from the catalogued cover/imprint statement itself.

## 4. Independence from the NIJL/Tohoku lineage

This object is held by **Princeton University East Asian Library** under `TC183/2991`. It is not the NIJL/Tohoku item-control chain audited in AW/BC. Accordingly:

```text
INDEPENDENT_EXACT_1594_MATERIAL_WITNESS_INCREMENT=1
```

This is a physical-holding/provenance increment only. It is not yet a target-passage vote.

## 5. Public image entry and permission boundary

The exact NLC detail page emits both a thumbnail and a “查看大图” route. The emitted `OpenObjectPic` page itself returns HTTP 200. Its own script, however, checks:

```text
/OutOpenBook/dataInOutPermission
/OutOpenBook/resInOutPermission
/allSearch/picPermission
```

Only after those checks pass does it assign the iframe to the emitted `openBookPic` route. BE does not call that conditional page route directly, does not guess page identifiers, does not log in, and does not bypass any permission check.

Therefore:

```text
PUBLIC_LARGE_IMAGE_ENTRY_OBSERVED=true
PAGE_VIEWER_PERMISSION_GATED=true
DIRECT_PAGE_BYTES_OBTAINED=false
TARGET_LEAF_OBTAINED=false
DIRECT_TARGET_GLYPH_COLLATION_AUTHORIZED=false
```

This is an access boundary, not proof that the target leaf is absent.

## 6. Witness accounting

```text
INDEPENDENT_EXACT_1594_MATERIAL_WITNESS_INCREMENT=1
INDEPENDENT_TARGET_TEXT_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
WHOLE_VOLUME_TEXT_NEGATIVE_AUTHORIZED=false
```

The Princeton object strengthens the independent material history of the early Wanli lineage, but the missing late-Zi rule bridge still requires direct target text.

## 7. Effect on HPA-ZDATE-006 and product state

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
REQUIRED_MISSING_BRIDGE=upper/night Zi -> Hai branch
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

No deterministic chart behavior changes are authorized.

## 8. Accounting

```text
ROW_COUNT=198
AUDITED_ROW_COUNT=166
MISSING_FROM_PRODUCT=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_PROVENANCE_DEFECTS=11
REPAIRED_PROVENANCE_DEFECTS=11
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

## 9. Durable evidence chain

```text
NLC landing/contract: run 34752100584 / artifact 10316301987
NLC title GET:        run 34753132831 / artifact 10315982944
NLC exact detail:     run 34753175084 / artifact 10316627671
NLC image viewer:     run 34753246009 / artifact 10316806982
```

Machine-readable consolidation:

```text
docs/research/ZIWEI-ZHANGGUO-NLC-PRINCETON-1594-HOLDING-AND-IMAGE-ACCESS-R1.json
```

## 10. Next gate

1. Seek a legitimate Princeton/NLC public or reproduction route that can expose the target late-Zi leaf without bypassing the NLC permission chain.
2. Continue independent exact-1593/1594 holdings research; prioritize a copy with public page images rather than another catalog-only duplicate.
3. If a Princeton target page is lawfully obtained, bind provider URL/object ID/digest/page/leaf and visually collate it without OCR before adding a target-text or Hai-glyph vote.
4. Keep HPA-ZDATE-006 unresolved until direct rule evidence supplies `upper/night Zi -> Hai branch`.
