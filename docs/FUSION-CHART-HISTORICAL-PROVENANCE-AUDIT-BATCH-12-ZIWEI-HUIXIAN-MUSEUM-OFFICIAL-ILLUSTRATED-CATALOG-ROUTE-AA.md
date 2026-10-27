# Fusion Chart Historical Provenance Audit R1 — Batch 12AA

## Hui County Museum official illustrated-catalog route and Fullbook duplicate/access controls

Status: **OFFICIAL PUBLICATION-LEVEL PHYSICAL-HOLDING BINDING UPGRADED / DIRECT ENTRY IMAGE NOT YET OBSERVED / DIRECT LATE-ZI TARGET PAGE NOT OBSERVED / ZERO NEW HAI-GLYPH VOTES / DUPLICATE ROUTES QUARANTINED / NO ALGORITHM EFFECT**

## 1. Scope

Batch 12AA continues `HPA-ZDATE-006` after Batch 12Z. It does **not** reopen deterministic chart algorithms. Its purpose is narrower:

1. upgrade the Hui County Museum Fullbook holding from a secondary locator to an institution-bound official publication route;
2. record the exact public resource boundary of that route;
3. deduplicate several apparently new Fullbook routes that are actually already-controlled physical or textual lineages;
4. keep the search gate focused on a second directly collated Fullbook physical target page.

## 2. Hui County Museum: official publication-level binding

National Library Press publicly lists the 2025 publication:

```text
《辉县市博物馆藏古籍珍品书录》
ISBN 978-7-5013-7612-4
国家图书馆出版社
2025-10-31
作者：冯福珍
```

The official product description states that the catalog selects 485 ancient-book titles held by Hui County Museum and supplies representative original-book images for every selected title, prioritizing volume beginnings and otherwise covers/title leaves, imprints, prefaces/postscripts or contents.

The official directory includes:

```text
新鋟希夷陳先生紫微斗數全書四卷 二三三
```

Therefore the Hui County Museum Fullbook route is upgraded to:

```text
OFFICIAL_PUBLICATION_LEVEL_BINDING_TO_HUI_COUNTY_MUSEUM_PHYSICAL_HOLDING
ENTRY_START_PAGE=233
```

This is materially stronger than the prior secondary catalog locator. It is still **not** a direct view of the underlying p233 entry image and is not a late-Zi target-page witness.

## 3. Official publisher resource probes

### 3.1 Product-resource probe AD

Exact-head research run:

```text
run=34255004377
head=ca49b223ec69111c2eeb26f9090ae2f785c16283
job=102158439504
artifact=10067486405
artifact ZIP SHA-256=c50a59d532ebfa0b4b1311071e6ff0c11dba258c1e1cd79d76473fc163a6c0ae
```

The product page returned HTTP 200 and directly exposed:

```text
图书文件下载（TXT） -> javascript:__doPostBack('Booktext','')
目录附件下载 -> anchor present but no href in the current public page
```

General National Library Press download-list routes were public, but no title-specific p233 image or attachment route was exposed by the page.

### 3.2 Public Booktext action AE

The exact public ASP.NET `Booktext` action was submitted once, preserving the page's own hidden fields. No authentication, purchase, identifier guessing or access-control bypass was attempted.

```text
run=34255133141
head=df4c5ce2f8aff6c77607525477c6df1b0a5757e7
job=102158880195
artifact=10067525226
artifact ZIP SHA-256=e1aa4ae2397080ad35e6b5f465f5711f07ea1813c79124c9de8e05fb42a61563
response bytes=32920
response SHA-256=9172da23a2d292c9fc86965a0dad0673ac25be7bfb5e0944f628fa0ad035be10
```

The returned attachment is the product metadata/description/directory TXT. It contains the Hui County catalog identity and the Ziwei directory entry, but no late-Zi target sentence and no physical p233 image.

Thus:

```text
HUIXIAN_OFFICIAL_CATALOG_BINDING=UPGRADED
DIRECT_PAGE_233_IMAGE=NOT_OBSERVED
DIRECT_LATE_ZI_TARGET_PAGE=NOT_OBSERVED
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
```

## 4. Duplicate and access-control findings

### 4.1 Kumyo / Jingluntang

The current Kumyo route resolves to the same `BBAA18036` physical object already reviewed in Batch 12E. Batch 12E already bound the same 36 source occurrences to eight unique physical photographs. Re-review therefore adds **zero** independent witness weight.

### 4.2 Liaoning / Wenchengtang

The Qing Wenchengtang / Liaoning Provincial Library locator is already controlled by Batch 12F. Current public research did not obtain a newly exposed target page. It remains a route target, not a new witness.

### 4.3 Shidian received text

Shidian's current volume-five transcription preserves:

```text
上五刻屬昨夜亥時，下五刻屬今日子時
```

but Shidian's own book identity surfaces the base as:

```text
南陽堂較梓
```

It is therefore a modern received-text control of the already-collated Nanyangtang lineage, not an independent Fullbook edition. It adds zero Hai-glyph votes.

### 4.4 Anonymous 33.75 MB `全書１.pdf`

Public resource indexes repeatedly list:

```text
新鋟希夷陳先生紫微斗数全書１.pdf 33.75 MB
```

Shuge independently exposes the Japan Cabinet Library Nanyangtang/Baohetang object in an approximately 34.5 MB black-and-white derivative alongside the 813 MB color source. The anonymous 33.75 MB file is therefore conservatively quarantined as a likely same-lineage derivative unless a contrary physical imprint/title-page surface is directly observed.

This is a deduplication presumption, **not** a positive edition identification.

### 4.5 Buybook / Books.com.tw preview route

Buybook publicly emits Books.com.tw image-proxy URLs whose query parameters disclose the underlying product-image URLs. Both the wrapper route and the exact page-disclosed underlying URLs returned HTTP 403 from GitHub runners.

This is only an execution-environment access boundary:

```text
CONTENT_ABSENCE_CLAIM=FORBIDDEN
TARGET_PAGE_ABSENCE_CLAIM=FORBIDDEN
WITNESS_INCREMENT=0
```

## 5. HPA-ZDATE-006 adjudication after Batch 12AA

Nothing in this batch changes the Batch 12Z textual conflict:

- Nanyangtang Fullbook directly preserves explicit `昨夜亥時 / 今日子時`.
- Korea Springgang manuscript directly preserves `昨夜 / 今夜` without an explicit `亥` in the exact span.
- Hui County Museum now has a stronger official physical-holding route, but its target page remains unobserved.
- no second Fullbook physical target page has yet been directly collated.

Therefore:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
WITHIN_FULLBOOK_HAI_GLYPH_STABILITY=UNRESOLVED
DIRECT_INDEPENDENT_FULLBOOK_HAI_GLYPH_WITNESS_INCREMENT_BATCH_12AA=0
NEW_CANDIDATE_FAMILY=NO
CANDIDATE_SELECTION=NO
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
```

The deterministic fusion-chart product remains CLOSED.

## 6. Next evidence gate

The next high-value gate remains direct physical collation of `論人生時要審的確` from another Fullbook edition with bound provenance. Priority routes:

```text
敦化堂
繼述堂
文盛堂
經綸堂
文誠堂
輝縣市博物館藏清刻本
or another independently bound Fullbook physical witness
```

Only after that textual/edition question is sufficiently bounded should a separate runtime time-standard decision be considered. No historical wording in this batch authorizes civil-time, mean-solar-time or apparent-solar-time binding.

## 7. Closure execution binding

Batch 12AA state synchronization was executed by fail-closed workflow run `34255864333`. Before committing, that workflow passed the Historical Provenance machine gate, Project Continuity machine gate, and focused historical-provenance matrix tests. It then produced closure commit `d5d943de8e1835bae266c7360a44bc9d2984ef3b` (tree `b23fd0c60eeef1518dd5d65c1cb682d7591aa754`). This section is a durable execution binding only; it does not add textual evidence or alter any witness count.
