# Fusion Chart Historical Provenance Audit R1 — Batch 12AH

## Jiaojingshanfang / Hanauction detail-photo visual adjudication

Status: **PROVENANCE SCOPE DEFECT CONFIRMED AND REPAIRED / TWO 2012 MEDIA OBJECTS DIRECTLY REVIEWED / AUCTION-EVENT SCENERY NOT TARGET-LOT BOOK PHOTOS / ZERO TEXTUAL-GLYPH VOTES / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12AH reopens **only the evidentiary classification** of the two 300×225 JPEG objects captured by Batch 12AG. It does not reopen the Ziwei chart algorithm and does not change the already-bound 2012/2026 Jiaojingshanfang auction-row provenance.

## 2. Parent machine archive

The controlling source archive remains workflow run `34319318823`, artifact `10091275632`, ZIP SHA-256 `c348dc9207c5932421e58ca0b01160827a5468a9b7160ba2f6e28e0aacfdfdf1`.

Relevant archived members:

- `auction-65-lot-173-detail-browser.html` — SHA-256 `93e6d80fd3d65e58fccd81a683cdfcd013d1aff8eabadc934c7aca764d2fec65`
- `auction-65-lot-173-detail.png` — SHA-256 `8a5bc72cc904f6b953f3a99e3a4fb52ad87caf4e7f6c3ea5de42714e5f1771dd`
- raw `auction-65-lot-173-detail.html` — SHA-256 `d5ce39994a436ede8b4ea9314f8c0ffaa37ecf7185dfc79417b4f2072bd6ff93`, which is the anti-bot cookie challenge rather than target-object content.

The browser-derived surface still contains the exact lot-173 row for stable object `27427`, but its two 300×225 media objects occur under the auction-round context `제65회 우리 얼 찾기 경매전 풍경`.

## 3. Direct visual adjudication

No OCR was used.

### `20120708024841.jpg`

- archive member: `auction-65-lot-173-detail-09.jpg`
- SHA-256: `c8705995aa695ba7ef285be939960bcef69516aed749937b00b309cf0df321c2`
- 300×225 / 51,812 bytes
- HTML role: `7/7 경매 전시 동영상`
- direct visual content: a wide auction-room/exhibition scene with tables, books and wall displays.

### `20120708024758.jpg`

- archive member: `auction-65-lot-173-detail-10.jpg`
- SHA-256: `a22d0017171dd0893019b551f9c986de3f89f6c16d2840260ffe8e3a3f685260`
- 300×225 / 38,858 bytes
- HTML role: `7/7 경매 진행 동영상`
- direct visual content: an auction-event presenter at a lectern.

Neither image is a target-book page, neither exposes `論人生時要審的確`, and neither supplies a `亥` glyph.

## 4. Provenance defect

`PROV-DEFECT-010 = EVIDENCE_SCOPE_MISCLASSIFICATION`.

Batch 12AG described these two hashes as target-route “exact detail photo objects”. The archive itself shows that they are auction-round event scenery/video thumbnails. The repair is forward-only:

```text
AG_PHOTO_HASHES=RETAINED_FOR_LINEAGE
AG_EXACT_TARGET_DETAIL_PHOTO_CLASSIFICATION=REVOKED
AH_MEDIA_SCOPE=AUCTION_EVENT_MEDIA_NOT_TARGET_OBJECT
TARGET_TEXT_WITNESS_INCREMENT=0
HAI_GLYPH_WITNESS_INCREMENT=0
```

The exact 2012 and 2026 auction rows still bind the Jiaojingshanfang physical-edition route. The defect is in evidence scope, not in that bibliographic locator.

## 5. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
JIAOJINGSHANFANG_TARGET_PAGE=PENDING_DIRECT_VISUAL_TARGET_PAGE
RUNTIME_TIME_STANDARD_BINDING=UNRESOLVED
NEW_CHART_RULE_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CANDIDATE_COLLAPSE=0
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
```

Nanyangtang and Guangyi/Yulgok remain the two directly read Fullbook physical target pages with explicit `昨夜亥時 / 今日子時`. Jiaojingshanfang still contributes provenance breadth only.

## 6. Accounting

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=10
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=10
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

The deterministic fusion-chart product remains CLOSED.

## 7. Next gate

The highest-value Jiaojingshanfang gate is now an **actual target-object page image**, not further interpretation of the two event-media hashes. In parallel, HPA-ZDATE-006 productization still requires source-closed civil/mean/apparent-solar time-standard binding.

## 8. Machine evidence

`docs/research/ZIWEI-JIAOJINGSHANFANG-HANAUCTION-DETAIL-PHOTO-VISUAL-ADJUDICATION-R1.json`
