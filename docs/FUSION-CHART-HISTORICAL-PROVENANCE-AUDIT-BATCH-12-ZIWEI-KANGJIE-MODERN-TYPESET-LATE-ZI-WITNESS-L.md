# Fusion Chart Historical Provenance Audit R1 — Batch 12L

## Xuelin / Kangjie modern typeset late-Zi received-text witness

Status: **MODERN TYPESET TARGET PAGE DIRECTLY REVIEWED / HAI READING CORROBORATED / OLD-EDITION GLYPH AUTHORITY FORBIDDEN / NO ALGORITHM REOPEN**

Batch 12L closes a public `《康节说易全书·紫微斗数》` route discovered after Batch 12K. The source is useful, but only after its format is correctly classified.

## 1. Source identity

The public PDF is 345 pages, 11,640,365 bytes, SHA-256 `0bbb04a3d274f192f16e1d519fa91f31dc48fab0e440e16ee04109393830cbf8`.

Direct visual review of the front matter, without OCR, shows:

- title: `康节说易全书·紫微斗数`;
- `陈明点校`;
- `学林出版社`;
- modern horizontal simplified-character typesetting.

It is therefore **not** a photographic reproduction of another old woodblock/stone-print target page. A front-matter `二〇〇〇年十二月` date is preserved only as an editorial/preface surface and is not promoted to exact publication-date proof.

## 2. Table-of-contents control

Direct review of PDF pp.11–12 shows the modern contents list:

- `新镌希夷陈先生紫微斗数全书卷之三 ... 127`;
- `论人生日时要审的确 ... 151`.

The first probe found no usable PDF text-layer hits, confirming that the source must be reviewed from rendered page images rather than by assuming its hidden text layer is authoritative.

## 3. Finite page-offset replay

A second workflow rendered only eight finite candidate pages.

Direct page-number review gives:

```text
PDF 138 = printed 124
PDF 139 = printed 125
PDF 140 = printed 126
PDF 161 = printed 147
PDF 162 = printed 148
PDF 163 = printed 149
PDF 164 = printed 150
PDF 165 = printed 151
```

Thus the target is exactly PDF p165. Its render SHA-256 is `eded525967698552a199b21f0c886043402f8dde3b4b74ca6ef621ab23542824`.

## 4. Direct target-page reading

Direct no-OCR visual review of PDF p165 / printed p151 shows heading:

`论人生日时要审的确`

and the modern typeset passage:

`如人生子、亥二时，最难定准，要仔细推详。如子时有十刻，上五刻属昨夜亥时，下五刻属今日子时。如天气阴雨之际，必须罗经以定真确时候，若差讹，则命不准矣。`

This is a clear received-text corroboration of the Nanyangtang mechanical reading:

```text
UPPER_FIVE=PREVIOUS_NIGHT_HAI
LOWER_FIVE=CURRENT_DAY_ZI
```

## 5. Authority ceiling

The important limitation is equally clear.

This source is a modern edited/typeset transmission layer. Therefore it cannot establish:

- the historical printed glyph in an old edition;
- independent Dunhuatang/Jishutang/Jingluntang/Wenchengtang/Lianyuange support;
- a distinct physical stemmatic branch;
- historical punctuation or traditional/simplified glyph identity.

Accordingly:

```text
MODERN_TYPESET_RECEIVED_TEXT_CORROBORATION=YES
INDEPENDENT_OLD_EDITION_HAI_GLYPH_WITNESS=NO
SOURCE_COUNT_VOTE_EFFECT=NONE
```

## 6. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RECEIVED_TEXT_CORROBORATION_ADDED=YES
DIRECT_INDEPENDENT_HAI_GLYPH_WITNESS_COUNT_ADDED=0
OLD_EDITION_HAI_GLYPH_STABILITY=UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES
RUNTIME_TIME_STANDARD_BINDING=UNRESOLVED
NEW_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
```

The next high-value gate remains a directly readable target page from an explicitly identified historical physical edition.

## 7. Accounting

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

Machine evidence: `docs/research/ZIWEI-KANGJIE-MODERN-TYPESET-LATE-ZI-WITNESS-R1.json`.

The deterministic fusion-chart product remains CLOSED.
