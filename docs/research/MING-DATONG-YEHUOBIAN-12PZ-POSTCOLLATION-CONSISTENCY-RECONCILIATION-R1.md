# 天问 12PZ — direct-image-review consistency reconciliation (2026-10-10)

**Scope:** Machine-readable evidence cleanup after source-hashed, independently copy-identified old-20-volume physical page review. This is not a new textual witness, completion of 12PZ, or a new historical adjudication.

## Identified stale states

1. The China NLC fascicle-10 ledger still listed “the last ten PDF pages have all been glyph-reviewed” as unproved, although a later SHA-verified visual collation had reviewed every image from PDF p136 to p145. **Review of pages ≠ exhaustive character transcription.** The negative result covers only absence of an *identified heading* 改造漏刻 in those ten pages.
2. The source-digest object preserved the earlier generic “萬曆野獲編卷二十” as a preexisting p137 reading; the later directly verified literal heading is **萬曆肆拾伍丁巳卷二十**. The old reading stays historically visible as superseded, not silently erased.
3. The prior browser-only heading crosswalk had a null PDF digest even though the same source surrogate was subsequently downloaded, SHA-pinned and tied to the rendered page p137. The exact PDF SHA256 is now backfilled with revision history.

## Source binding

- China NLC accession **411999003250**, fascicle 10 (distinct from Taiwan NCL 02260 and 02261); source PDF SHA256 **`8e746faaadcd961c7983981d419862d97fdc2a1f3ec33ecb02046e9e79a6376c`**, 145 pages, 46,469,798 bytes, GitHub Actions run 38029093566 / artifact 11662045134.
- Direct source-derived p137 JPEG SHA256 **`b6a67b0495556eb9cd57d011b0622717c9b72fd11b966fb5571e105a6a00339a`**; directly read heading 萬曆肆拾伍丁巳卷二十. p145 has 萬曆野獲編二十卷紀事畢.
- Only p136–145 are within this negative heading check. Original target heading/folio may be elsewhere. The Taiwan NCL 02260 p592 TOC is a different thematic arrangement, but this alone proves no directed copying or Inoue A/B assignment.

## Immutable research boundaries

- Zero new old20 target 改造漏刻 / 官漏・宮漏 direct text witnesses; an existing Shanghai **reorganized 30-volume** page pair must not be counted as old20 or verified 1827 print.
- No proof of the 1447 clock rebuild being completed, or the 1450 eclipse observation instrument, observer, locality or time coordinate.
- **MD-G03 = OPEN_BLOCKING_GENERAL_ADAPTER**; **HPA-DAYUN-CAL-002 = MISSING_FROM_PRODUCT**. No Matrix count, current semantic state, transmission edge, deterministic chart algorithm or runtime change. Batch **12PZ remains open**.
- Evidence changes are guarded by `tests/test_ming_datong_yehuobian_12pz_witness_boundary_r1.py`.

## Next physical proof

Acquire old20 manuscript *target heading plus original folio* by scanning **other original volumes/TOC pages** with precise identity, then compare the actual identified **1827 扶荔山房 printed target leaf**. Do not reuse a recut 30-volume “卷二十” number as the manuscript locator.
