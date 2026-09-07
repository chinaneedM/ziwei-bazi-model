# Fusion Chart Historical Provenance Audit R1 — Batch 12E

## Qing Jingluntang independent physical-edition route

Status: **INDEPENDENT JINGLUNTANG EDITION IDENTITY CLOSED / TARGET PAGE NOT OBSERVED / NO ALGORITHM REOPEN**

Batch 12E expands the physical-edition horizon beyond the Nanyangtang and Wenguangtang routes. It asks whether an independent Qing `經綸堂` Fullbook witness can be bound at library and physical-copy level, while refusing to infer the late-Zi glyph without the target page.

## 1. Shanghai Library official linked-data identity

Shanghai Library public linked data directly binds instance `1pjr6vy1ffsq3l1y` to:

- title: `新鋟希夷陳先生紫微斗數全書四卷`;
- edition label: `清經綸堂刻本`;
- identifier: `子30814110`;
- creator field: `宋陳摶撰`.

The same object was captured via HTML, JSON-LD, Turtle and RDF/XML. The JSON-LD object SHA-256 is `6f030fc56ff2da35f711594ccacc6fe1fda6ec2802b650b85520cf89e71890bd`.

This closes a library-grade Qing Jingluntang edition identity.

## 2. Anonymous digital-object boundary

The reviewed SHLIB metadata does not explicitly expose `IIIF`, `manifest`, `itemId`, `dhapi` or another page-object identifier. Anonymous controls for the current ancient-book root and `dhapi/pdfview/` root returned HTTP 412.

No item ID was guessed. No login, token reuse, authentication bypass or page enumeration was attempted.

Therefore:

`SHLIB_TARGET_PAGE=NOT_OBSERVED`

not “digitized page unavailable forever” and not “target page absent”.

## 3. Independent public physical copy

Kumyo auction object `BBAA18036` publicly describes an approximately 19th-century `經綸堂梓行` Chinese `新镌希夷陈先生紫微斗数全书` in four volumes.

The public HTML embeds physical photographs directly as base64 JPEGs. Research run `34124948029` / artifact `10019806060` extracted 36 JPEG occurrences collapsing to **8 unique physical-image hashes**.

All eight unique photographs were directly visually reviewed without OCR. They include cover/label, opening/title material, prose leaves, chart/table material and closing leaves. The cover/label visibly establishes:

- `陳希夷先生著`;
- `紫微斗數`;
- `經綸堂梓行`.

This independently confirms the physical Jingluntang edition family rather than relying on the Shanghai Library catalog alone.

## 4. Target-page result

None of the eight unique photographs is 《論人生時要審的確》. No reviewed physical image shows the target late-Zi sentence or the disputed `亥` glyph.

Thus Batch 12E closes only:

`JINGLUNTANG_EDITION_FAMILY_IDENTITY=CLOSED_AT_LIBRARY_AND_PUBLIC_PHYSICAL_COPY_LEVEL`

while preserving:

`HAI_GLYPH_STABILITY_ACROSS_PHYSICAL_EDITIONS=UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES`

## 5. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_TIME_STANDARD_BINDING=UNRESOLVED
CANDIDATE_SELECTION_AUTHORIZED=NO
ALGORITHM_REOPEN=NO
```

The Jingluntang route is independent of the previously documented Dunhuatang/Jishutang Wenguangtang route and is not merged with it merely because the title belongs to the same received Fullbook tradition.

## 6. Accounting

Batch 12E is provenance/access-only and changes no Matrix count:

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

Machine evidence: `docs/research/ZIWEI-QUANSHU-JINGLUNTANG-PHYSICAL-ROUTE-R1.json`.

The deterministic fusion-chart product remains CLOSED.
