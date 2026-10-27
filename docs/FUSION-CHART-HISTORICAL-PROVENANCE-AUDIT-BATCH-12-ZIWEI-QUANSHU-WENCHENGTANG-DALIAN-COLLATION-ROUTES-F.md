# Fusion Chart Historical Provenance Audit R1 — Batch 12F

## Wenchengtang institutional/editorial routes + Dalian Guangyi later-edition control

Status: **POST-12E ROUTES ADJUDICATED / DALIAN REPUBLIC EDITION IDENTITY CLOSED / WENCHENGTANG TARGET GLYPH NOT OBSERVED / NO ALGORITHM REOPEN**

Batch 12F closes the seven post-12E research commits already present on the live development branch. It does not treat search-index text, a secondary catalog locator, or website UI images as facsimile evidence.

## 1. Liaoning Wenchengtang route

A secondary catalog locator records `新鐫希夷陳先生紫微斗數全書四卷 / 清文誠堂刻本 / 遼寧省圖書館`. This remains **secondary locator evidence only**.

An independent institutional control strengthens only the access route: Nankai University Library's public ancient-book external-resource page directly labels `辽宁省图书馆古籍书目查询` and links it to `http://www.lnlib.com/gj/index.htm`.

The current Liaoning Library home/resource pages and both HTTP/HTTPS legacy `/gj/index.htm` controls timed out in the research run. Therefore Batch 12F does **not** claim that the official Liaoning target record was directly read.

```text
LIAONING_LEGACY_CATALOG_ROUTE=INSTITUTIONALLY_BOUND
WENCHENGTANG_LIAONING_HOLDING=SECONDARY_LOCATOR_ONLY
OFFICIAL_LIAONING_TARGET_RECORD=PENDING
TARGET_PAGE=NOT_OBSERVED
```

## 2. Dalian Library: independent Republican Guangyi edition

Dalian Library's official public item page directly records:

- title: `(新鐫希夷陳先生)紫微鬥數全書`;
- `四卷`;
- `(宋)陳希夷撰`;
- `石印本`;
- publication place `上海`;
- publication statement `廣益書局 民國`;
- physical form `四冊一函`.

This closes a **later Republican Guangyi lithograph edition identity** at official-library catalog level.

The route probe discovered seven image-like URLs and saved six. All six were directly visually reviewed without OCR. They are library-site chrome: one logo and five tiny decorative/separator assets. None is a photographed or scanned book page. The previous machine hint `REQUIRES_DIRECT_VISUAL_REVIEW` is therefore resolved as:

```text
DALIAN_PUBLIC_IMAGE_CANDIDATES=SITE_UI_ASSETS
BOOK_PAGE_OBSERVED=NO
TARGET_SECTION_OBSERVED=NO
```

## 3. Dalian published GET-form search control

The public old-book and rare-book catalog pages expose a normal GET form with fields `id / keyword / author`. Fourteen normal queries were executed across catalog IDs 7 and 14.

All returned HTTP 200, but the returned page text reflected none of the query terms and contained no `紫微`; the parser consequently harvested generic navigation/list links rather than demonstrated query hits. This route is retained as a **search-behavior control**, not as a negative catalog search.

No conclusion such as “Dalian has no other Ziwei witnesses” is authorized.

## 4. Jielan Google Books index and Wenchengtang collation layer

The public Google Books index for volume `rZRcCwAAQBAJ` directly returns a PT176 editorial snippet stating that the point-collated Jielan edition used a Qing Wenchengtang `《紫微斗數全書》` (abbreviated `《文本斗數全書》`) together with a Qing Lianyuange `《紫微斗數全集》` to note textual differences without changing the Jielan base text.

This strengthens the already publisher-documented Wenchengtang route as an **active editorial collation witness**.

It does not close the target late-Zi glyph:

- exact `論人生時要審的確`: 0 results in all three request forms;
- exact `子時有十刻`: 0 results in all three request forms;
- `上五刻 / 下五刻` hits resolve to PT174/PT177 editorial/front-matter snippets, not a Wenchengtang target quotation;
- `亥時` resolves to unrelated pages PT29/PT33/PT34/PT43/PT44/PT126.

Search-index zero results are not negative textual proof, and index snippets are not physical glyph authority.

## 5. Effect on HPA-ZDATE-006

Batch 12F adds routes and edition controls, not a new runtime rule.

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
HAI_GLYPH_STABILITY_ACROSS_PHYSICAL_EDITIONS=UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES
RUNTIME_TIME_STANDARD_BINDING=UNRESOLVED
CANDIDATE_SELECTION_AUTHORIZED=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
```

The direct Nanyangtang facsimile remains the controlling glyph witness for `上五刻屬昨夜亥時 / 下五刻屬今日子時`. Wenguangtang, Wenchengtang, Jingluntang and the later Guangyi route remain additional collation targets until the relevant physical target page is directly observed.

## 6. Accounting

Batch 12F is provenance/access/editorial-collation only and changes no Matrix count:

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

Machine evidence: `docs/research/ZIWEI-QUANSHU-WENCHENGTANG-DALIAN-COLLATION-ROUTES-R1.json`.

The deterministic fusion-chart product remains CLOSED.
