# Fusion Chart Historical Provenance Audit R1 — Batch 12C

## Independent 《紫微斗數全書》 physical-edition route audit

Status: **EDITION ROUTE MAP CLOSED / TARGET GLYPH NOT CLOSED / NO ALGORITHM REOPEN**

Batch 12A directly read the Nanyangtang target page. Batch 12B closed the generic historical timekeeping meaning of the upper/lower half. Batch 12C now asks whether the crucial `亥時` reading is stable in **independent physical Fullbook editions**.

## 1. Wenguangtang woodblock route

Heart-One's official 2017 facsimile page for ISBN `9789888266944` states that the publication combines two 虛白廬 copies:

- 清刷明末清初文光堂木刻本 `敦化堂刊本`;
- 清刷明末清初文光堂木刻本 `繼述堂刊本`.

The publisher says the Dunhuatang copy is somewhat earlier and the Jishutang copy has red/black collation marks. This gives us two specifically named physical witnesses within the Wenguangtang block family.

Research workflow run `34120317222` captured the official publisher page with HTTP 200 / SHA-256 `a38c86b18471cbb500b10e536c762887b7727356d073be5875ca7e10d9c8ef8d`. Buybook and Xingqiao independently expose the same publication identity, but these retailer repetitions are bibliographic corroboration only.

## 2. Separate Qing Wenchengtang route

Heart-One's official Jielan page states that its point-collation used a `虛白廬藏清中期文誠堂刊本《紫微斗數全書》`.

The 12C workflow directly captured this page with HTTP 200 / SHA-256 `4b424d017441c52a231361aa6d1e42c11aea0aa12f67168797b45a1d3c4a85b8`.

This is retained as a **separate Qing Fullbook edition route**, not merged with the Wenguangtang/Dunhuatang/Jishutang block family.

## 3. Wenshengtang secondary locator

A 2017 secondary comparison reports a 文盛堂 copy whose typeface/layout/missing-glyph pattern appears very similar to 繼述堂, while 敦化堂 is typographically different. That observation is useful for locating another copy, but the author's shared-block hypothesis is not treated as established provenance and no target page is exposed.

## 4. Public preview result

No independent target page was obtained:

- Books.com product route: HTTP 403;
- all 13 known preview-image URLs: HTTP 403;
- saved preview images: `0`;
- Google Books ISBN/title API routes: HTTP 429.

Therefore the correct adjudication is:

`NO_INDEPENDENT_TARGET_PAGE_OBSERVED`

not “target page awaiting visual review”.

## 5. Effect on HPA-ZDATE-006

The independent edition-route map is materially stronger, but it does **not** answer the glyph question.

```text
HAI_GLYPH_STABILITY_ACROSS_PHYSICAL_EDITIONS=UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_TIME_STANDARD_BINDING=UNRESOLVED
ALGORITHM_REOPEN=NO
```

Publisher descriptions cannot prove what the target sentence reads. Retailer repetitions do not count as independent textual witnesses. The next decisive evidence must be a directly visible target page from Dunhuatang, Jishutang and/or Wenchengtang.

## 6. Accounting

Batch 12C is provenance/access-only and changes no Matrix count:

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

Machine evidence: `docs/research/ZIWEI-QUANSHU-INDEPENDENT-EDITION-ROUTES-R1.json`.

The deterministic fusion-chart product remains CLOSED.
