# Fusion Chart Historical Provenance Audit R1 — Batch 12J

## Shanghai Guangyi public physical-set collation

Status: **PHYSICAL SET/IMPRINT DIRECTLY PHOTOGRAPHED / EXACT PRINTING BRIDGE UNRESOLVED / TARGET PAGE NOT OBSERVED / STEMMATIC DEPENDENCE PRESERVED / NO ALGORITHM REOPEN**

Batch 12J upgrades the later Shanghai Guangyi route from the official-library catalog identity already closed in Batch 12F to a directly reviewed public physical-set photograph route. It does not promote an antiquarian listing into exact publication-date authority and does not treat a non-target photographed page as the missing late-Zi glyph witness.

## 1. Reproducible public capture

Research workflow `34140027356`, job `101799700213`, artifact `10025522997` captured the public Yetnal item page and four directly linked JPEGs. Artifact ZIP SHA-256 is `35be2589ac50228eab9a03a77401ad283fb40be1981d4f4bddeab9bd42c06485`.

The item page returned HTTP 200 and directly describes a Shanghai-edition `校正紫薇斗數全書`, four juan / four books complete. No login, identifier guessing, page enumeration or OCR was used.

## 2. Direct visual review of the four photographs

Direct no-OCR review gives four distinct controls:

1. cover/title slip: `校正紫薇斗數全書` and `上海廣益書局印行`;
2. a four-book physical set laid out together;
3. inner title page: `陳希夷先生著 / 紫薇斗數全書 / 上海廣益書局印行`;
4. an open text spread that is not the target `論人生時要審的確` page.

Therefore:

```text
GUANGYI_PHYSICAL_SET_IDENTITY=CLOSED_AT_PUBLIC_PHOTO_AND_IMPRINT_LEVEL
TARGET_SECTION=NOT_OBSERVED
TARGET_HAI_GLYPH=NOT_OBSERVED
DIRECT_HAI_GLYPH_WITNESS_ADDED=0
```

## 3. Bridge to the Batch 12F Dalian catalog object

Batch 12F already bound an official Dalian Library record for a Republican Shanghai `廣益書局 / 石印本 / 四卷 / 四冊一函` Fullbook.

The new physical set strongly matches that **work/publisher/form family**, but an exact same-printing or exact-catalog-item equation remains unclosed. The seller surface says only Shanghai edition and does not expose a date or lithograph statement, while the photographed title surface uses `紫薇` and the Dalian catalog uses normalized `紫微`.

The audit therefore records:

```text
SAME_GUANGYI_PUBLICATION_FAMILY=HIGH_CONFIDENCE
EXACT_PRINTING_IDENTITY=UNRESOLVED
SILENT_薇_TO_微_NORMALIZATION=FORBIDDEN
```

## 4. Stemma/source criticism

The NCKU edition-genealogy study already bound in Batch 12H identifies the Shanghai Guangyi Fullbook as a late-Qing/early-Republic publisher edition printed from a Ronghetang base, and places Ronghetang/Nanyangtang within the same Jianyang publishing-origin family.

Consequently a future Guangyi target page is useful transmission evidence from a later physical edition, but it must **not** be counted as a fully independent stemmatic branch merely because the photographed copy is physically separate.

This is exactly the distinction required by the project's evidence-weighted conflict policy: physical-copy independence, printing-edition difference and textual-stemma independence are three separate axes.

## 5. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
GUANGYI_TARGET_LATE_ZI_PAGE=NOT_OBSERVED
HAI_GLYPH_STABILITY_ACROSS_PHYSICAL_EDITIONS=UNRESOLVED_PENDING_DIRECT_TARGET_PAGES
STEMMATIC_INDEPENDENCE_FROM_NANYANGTANG=NOT_CLAIMED
RUNTIME_TIME_STANDARD_BINDING=UNRESOLVED
NEW_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
```

The higher-value next gate remains a directly readable target section from Guangyi itself or, preferably for stronger stemmatic discrimination, a Wenguangtang, Jingluntang, Wenchengtang or Lianyuange witness.

## 6. Accounting

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

Machine evidence: `docs/research/ZIWEI-GUANGYI-PHYSICAL-SET-COLLATION-R1.json`.

The deterministic fusion-chart product remains CLOSED.
