# Fusion Chart Historical Provenance Audit R1 — Batch 12AG

## Shanghai Jiaojingshanfang / Hanauction physical-edition provenance

Status: **SECONDARY COMMERCIAL PHYSICAL-EDITION ROUTE BOUND / TWO HISTORICAL SALE OCCURRENCES / 2012 SOURCE-EMITTED DETAIL PHOTOS CAPTURED / TARGET PAGE NOT DIRECTLY VISUALLY ADJUDICATED / BAOHUTANG-LINE SCHOLARLY GENEALOGY PRESERVED / ZERO TEXTUAL-GLYPH VOTES / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12AG follows Batch 12AF by broadening the physical-edition map for `HPA-ZDATE-006` without treating an edition locator as a target-text witness. The object is Shanghai Jiaojingshanfang's lithographic `《改良紫微斗數全書》`, not a new deterministic runtime rule.

## 2. Exact Hanauction sale routes

Controlling probe: workflow run `34319318823`, job `102362246336`, artifact `10091275632`, ZIP SHA-256 `c348dc9207c5932421e58ca0b01160827a5468a9b7160ba2f6e28e0aacfdfdf1`.

- 2026-02-07: auction 227, lot 127, stable object `101926`, visible description `上海校經山房 印行 ... 改良 紫微斗數全書 ... 4卷 4冊`.
- 2012-07-07: auction 65, lot 173, stable object `27427`, visible description `上海校經山房 印行 石印本 ... 改良 紫微斗數全書 ... 4卷 4冊`.

Hanauction describes the set as 13.7 × 20.5 cm. These are secondary commercial-auction description claims, not an institutional catalog assertion or an exact publication-year proof. Physical-copy identity between the 2012 and 2026 lots is unresolved; they are not counted as two textual witnesses.

## 3. Source-emitted image boundary

Exact target listing thumbnails are `101926S.JPG` (SHA-256 `9e9e7873b28a820b6afc7971ff9ba8dbc1cfe2fc20940f1a1189e3e95ae58fcb`) and `27427S.JPG` (SHA-256 `f74c07bd2c326888be2d729233ee25a30596bf115386406feaad7f609a0036e2`).

The 2012 exact detail page additionally emits two 300×225 JPEGs:
- `20120708024841.jpg` — SHA-256 `c8705995aa695ba7ef285be939960bcef69516aed749937b00b309cf0df321c2`
- `20120708024758.jpg` — SHA-256 `a22d0017171dd0893019b551f9c986de3f89f6c16d2840260ffe8e3a3f685260`

Those detail photos were captured but are **not directly visually adjudicated in the current execution environment**. The probe's overbroad listing ancestor also exposed neighboring lot thumbnails; those are excluded from target-lot evidence.

```text
TARGET_HEADING_DIRECTLY_OBSERVED=NO
TARGET_LATE_ZI_PAGE_DIRECTLY_OBSERVED=NO
TARGET_HAI_GLYPH_DIRECTLY_OBSERVED=NO
INDEPENDENT_TARGET_TEXT_WITNESS_ADDED=0
INDEPENDENT_HAI_GLYPH_WITNESS_ADDED=0
```

## 4. Scholarly genealogy control

Chen Zhaoyin's 2021 NCKU study records Jiaojingshanfang's lithographic `《改良紫微斗數全書》` as a post-1904 late edition and states that both the Guangyi and Jiaojingshanfang late editions were printed from the Baohutang-derived Fullbook line.

Therefore Jiaojingshanfang is important provenance breadth, but no stemmatically independent third “Hai” vote is created merely because another physical edition route exists.

## 5. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
TARGET_PAGE=PENDING_DIRECT_VISUAL_TARGET_PAGE
NEW_CHART_RULE_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CANDIDATE_COLLAPSE=0
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
RUNTIME_TIME_STANDARD_BINDING=UNRESOLVED
```

Nanyangtang and Guangyi/Yulgok remain the two directly read Fullbook physical target pages with explicit `昨夜亥時 / 今日子時`. Korea Springgang remains a direct broader non-Hai transmission control. Jiaojingshanfang adds provenance breadth only.

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

The deterministic fusion-chart product remains CLOSED.

## 7. Next gate

Highest value remains a directly readable target leaf from a genuinely distinct Fullbook edition route, while productization separately requires a source-closed civil/mean/apparent-solar time-standard binding.

## 8. Machine evidence

`docs/research/ZIWEI-JIAOJINGSHANFANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-R1.json`
