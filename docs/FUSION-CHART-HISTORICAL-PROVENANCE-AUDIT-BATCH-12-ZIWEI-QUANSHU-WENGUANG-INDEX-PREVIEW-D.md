# Fusion Chart Historical Provenance Audit R1 — Batch 12D

## Wenguangtang combined facsimile public index / preview audit

Status: **TARGET INDEX TEXT CORROBORATED / TARGET GLYPH NOT PUBLICLY DISPLAYED / BASE COPY UNRESOLVED / NO ALGORITHM REOPEN**

Batch 12C established the edition routes. Batch 12D binds the exact Heart-One 2017 facsimile publication to Google Play/Books volume `aIRbDgAAQBAJ` and asks whether the target passage can be recovered from the public index or free preview without crossing any access boundary.

## 1. Exact distribution volume

The public Google Play page binds:

- volume ID: `aIRbDgAAQBAJ`
- ISBN: `9789888266944`
- declared pages: `266`
- Free sample marker: present
- Play HTML SHA-256: `0e93e42dfd421a2edfb7881b117dc19530e31d4f980f7007e9b6f6541cb8c5f3`

The publication remains the Heart-One combined facsimile whose publisher description names the Dunhuatang and Jishutang Wenguangtang base copies.

## 2. Public search index finds the target

Research run `34121750009` / artifact `10018452113` queried Google's public `SearchWithinVolume2` surface.

The target heading query resolves to `PT165` (plus a contents/index control at PT16). The target page's index text includes:

`如子時有十刻上五刻属昨夜亥時下五刻属今日子時`

Queries for `上五刻`, `下五刻` and `亥時` all independently locate PT165 in the reviewed search run.

This is important corroboration, but it is still a Google search-index/OCR-like textual layer. It is **not** a direct reading of the photographed woodblock glyphs and it does not tell us whether PT165 comes from the Dunhuatang or Jishutang base copy.

## 3. Zero-result queries are not negative proof

The S01-attributed sentence `子時乃一日之始` returned zero search results in the reviewed runs.

No absence conclusion is authorized. A second viewer-oriented run demonstrated search instability: `上五刻` returned zero there even though the first run had already resolved it to PT165, while `下五刻` and `亥時` still located PT165.

Therefore:

`ZERO_SEARCH_RESULT != TEXT_ABSENCE_PROOF`

## 4. Official Embedded Viewer fails closed at glyph level

Research run `34123161798` / artifact `10019011766` used Google's documented Embedded Viewer API.

Observed state:

- volume loaded: true
- initial page: `PT14`
- `goToPageId("PT165")`: returned true
- final page ID after load/zoom: `PT166`
- target page directly observed: false
- PT165 click request: HTTP 200
- saved screenshot SHA-256: `8663286c36fcedeb4a47ddcb6d9f700e78b2070812ce2e4cf28eeb196e3361c8`

Direct screenshot review shows unavailable-preview placeholders rather than the ancient page. A successful navigation method return and HTTP 200 therefore do not equal page-image authority.

## 5. Public sample images and physical-copy access boundaries

Research run `34121401508` / artifact `10018315848` saved seven public Xinyi JPEG samples for the same 2017 Heart-One product. All seven were directly visually reviewed without OCR; none contains the target section.

Kongfz physical-copy image routes for the located Dunhuatang/fullbook objects redirect to login. No authentication or bypass was attempted. The Artron lot exposes public object/image metadata but no target-page binding.

## 6. Historical adjudication

Batch 12D strengthens one proposition:

`THE_2017_COMBINED_WENGUANGTANG_FACSIMILE_SEARCH_INDEX_PRESERVES_THE_HAI_READING_AT_PT165`

It does **not** close these stronger propositions:

- the PT165 photographed glyph itself visibly reads 亥;
- PT165 belongs specifically to Dunhuatang;
- PT165 belongs specifically to Jishutang;
- both Wenguangtang base copies independently preserve 亥;
- the separate mid-Qing Wenchengtang copy preserves 亥.

Therefore:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
HAI_GLYPH_STABILITY_ACROSS_PHYSICAL_EDITIONS=UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES
RUNTIME_TIME_STANDARD_BINDING=UNRESOLVED
ALGORITHM_REOPEN=NO
```

## 7. Accounting

Batch 12D changes no Matrix count:

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

Machine evidence: `docs/research/ZIWEI-QUANSHU-WENGUANG-GOOGLE-INDEX-PREVIEW-R1.json`.

The deterministic fusion-chart product remains CLOSED.
