# Fusion Chart Historical Provenance Audit R1 — Batch 12BB

## 《張果星宗大全》复旦大学明万历间实体馆藏一手绑定与“1594 唐谦刻本”证据边界校勘

Status: **FUDAN FIRST-PARTY GENERAL-ANCIENT-BOOK-CATALOG ROUTE CLOSED / TARGET CATALOG RECORD DIRECTLY BOUND / ONE PHYSICAL HOLDING DIRECTLY BOUND / INDEPENDENT MING-WANLI MATERIAL HOLDING CONTROL +1 / EXACT WANLI-22 OR 1594 NOT ATTESTED / TANG-QIAN NOT ATTESTED / SECONDARY 1594 LOCATOR NOT PROMOTED / ZERO TARGET-TEXT OR HAI-GLYPH VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Why this batch exists

After Batch 12BA separated the SOAS/NCL 1593 metadata from the 1797 Morrison physical reprint, a secondary rare-book locator pointed to another copy of 《新編評註通玄先生張果星宗大全》 at Fudan and described a Wanli-22 / 1594 Tang-Qian edition. BB tests that claim only through **Fudan first-party public systems** before allowing any early-witness vote.

The batch deliberately distinguishes four questions:

```text
DOES_FUDAN_HAVE_A_TARGET_TITLE_PHYSICAL_ITEM?
IS_THE_ITEM_MING_WANLI?
IS_IT_EXACTLY_WANLI_22 / 1594?
HAS_THE_TARGET_LATE-ZI LEAF BEEN DIRECTLY COLLATION-BOUND?
```

A positive answer to an earlier question does not imply a positive answer to a later one.

## 2. First-party route discovery: 古籍 portal -> general ancient-book OPAC

Fudan's public ancient-book portal source-emits the route:

```text
館藏書目
綫裝古籍書目 -> https://opac.fudan.edu.cn/#/gjRedirect
```

An initially visible `/guji/gujisearch/mingGuji` endpoint belongs to the **明人文集书目** specialty database, not the general line-bound ancient-book holding catalog. BB therefore rejects that specialty endpoint as authority for a general Fudan holding negative or positive and follows the portal's own `綫裝古籍書目` route instead.

## 3. Public OPAC contract recovered from the Fudan frontend

The OPAC's own public frontend exposes:

```text
API base=https://fdulspgw.fudan.edu.cn/urdh
resource type: 古籍 = 10
title field: 题名关键词 = resource_ztm
match type=contains
POST /open-api/opac/search/advanced
GET  /open-api/opac/search/smjlh/{id}
GET  https://fdulspgw.fudan.edu.cn/alsp/open-api/opac/v2/holdings?catalogueId={id}
```

The search-result route passes the record's `resource_smjlh` into `/gjInfo/`; the detail frontend decodes that value and calls the public item-detail and holdings APIs. No hidden object identifier was guessed.

## 4. Direct target-title catalog hit

The first-party ancient-book OPAC directly returns:

```text
title=新編評註通玄先生張果星宗大全
responsibility=(唐)張果撰; (明)陸位輯
extent=10卷
physical extent=10冊（1函）
date=不详#明萬曆間
edition=刻本
rare-book class=善本
binding=綫裝
call number=rb2314
resource book no=FDU01001127121
docId=34053686
resource_smjlh=34053686
```

This closes target catalog-item identity at the Fudan first-party OPAC level.

## 5. Direct physical-holding binding

Using source-emitted `resource_smjlh=34053686`, the first-party holdings API returns exactly one holding:

```text
holding_total=1
call number=rb2314
barcode=AB0613271-80
permanent library=复旦大学
permanent location=光华楼古籍书库
item status=在馆
catalogueId=34053686
```

Therefore BB authorizes:

```text
FUDAN_TARGET_TITLE_PHYSICAL_HOLDING=ESTABLISHED
FUDAN_MING_WANLI_MATERIAL_HOLDING_CONTROL_INCREMENT=1
```

This is institutionally independent of the SOAS/Morrison lineage audited in BA.

## 6. Critical firewall: “明萬曆間” is not “萬曆二十二年 / 1594”

The Fudan first-party catalog and holdings expose `明萬曆間`, but do **not** expose `萬曆二十二`, `万历二十二`, `1594`, `唐謙`, or `唐谦`.

Accordingly:

```text
INDEPENDENT_EXACT_1594_MATERIAL_WITNESS_INCREMENT=0
SECONDARY_LOCATOR_1594_TANG_QIAN_CLAIM_PROMOTED=false
```

The secondary locator remains useful for discovery, but its exact-year/imprint statement cannot substitute for first-party edition evidence.

## 7. No target-leaf vote

The item record proves a material holding; it does not expose a reviewed target leaf for the late-Zi passage. No target-leaf image/full-text object was directly collated.

```text
TARGET_LEAF_OBTAINED=false
INDEPENDENT_TARGET_TEXT_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
```

No whole-holding textual negative is authorized.

## 8. Jiangsu/Nanjing route boundary

A parallel first-party Jiangsu/Nanjing ancient-book-platform probe timed out over both reviewed HTTP and HTTPS routes from the GitHub runner. BB records this only as an execution-environment/public-route boundary; reachability failure is not bibliographic absence.

## 9. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

Fudan materially strengthens the independent Ming-Wanli copy landscape, but it does not supply the missing mechanical bridge `upper/night Zi -> Hai branch` and does not justify changing deterministic runtime behavior.

## 10. Accounting

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

BB is a provenance/access-only adjudication and changes no Matrix row count.

## 11. Durable artifacts

```text
docs/research/ZIWEI-ZHANGGUO-FUDAN-MING-WANLI-FIRST-PARTY-HOLDING-RECONCILIATION-R1.json
docs/research/ZIWEI-ZHANGGUO-FUDAN-OPAC-TITLE-QUERY-R1.json
docs/research/ZIWEI-ZHANGGUO-FUDAN-OPAC-ITEM-DETAIL-R1.json
```

## 12. Next gate

1. Seek a Fudan first-party digitized-image or reproduction route for `rb2314 / FDU01001127121 / catalogueId 34053686`; if a target leaf becomes available, collate it directly without OCR.
2. Continue seeking a genuinely independent first-party copy whose **physical edition field itself** binds Wanli-22 / 1594 (or 1593) and then bind the target leaf.
3. Keep the Shandong/Weifang and Jiangsu/Nanjing leads locator-scoped until first-party object bytes or item metadata become reachable.
4. Do not collapse HPA-ZDATE-006 until direct rule evidence supplies the missing upper/night-Zi -> Hai mapping.
