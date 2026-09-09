# Fusion Chart Historical Provenance Audit R1 — Batch 12AP

## 《紫微斗數捷覽》陰雨生時章的證據範圍校正：PT49 公開索引命中、物理頁仍待取

Status: **AO PAGINATION-SURFACE FACT PRESERVED / AO EARLY-TRANSMISSION INFERENCE RETRACTED / GOOGLE BOOKS PT49 INDEX ATTESTS INCLEMENT BIRTH-TIME DISCUSSION / FULLBOOK-STYLE 羅經—真確時候 CHAIN NOT ATTESTED IN JIELAN / PT49 PHYSICAL GLYPH NOT OBTAINED / PROV-DEFECT-011 REPAIRED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Scope correction

Batch 12AO correctly established that the five current Tianji aggregate pagination pages did not expose the configured `陰雨 / 羅經 / 真確時候` terms. That finite observation remains valid.

The overreach was treating that finite surface as evidence for a new early-Ziwei transmission-variant dimension. Batch 12AP finds source-emitted evidence inside the Jielan publication line that localizes inclement birth-time material to **PT49**. The prior transmission-level inference is therefore retracted.

This is a provenance/evidence-scope defect, not a chart algorithm defect.

## 2. Google Books PT49 positive evidence

Public volume: `rZRcCwAAQBAJ`.

Controlling probe:

```text
WORKFLOW_RUN=34342819087
ARTIFACT=10100441781
ARTIFACT_ZIP_SHA256=6bf56986a8a594c759e088521496ed9c43944c87b11b29e0a4fd489868b483c8
```

SearchWithinVolume2 for `陰雨` source-emits exactly `PT49`. Its index text places the hit under `論十二生時難定訣` and contains the semantic reading `天陰雨下時難定`.

Therefore:

- the Jielan public index **does attest inclement-weather birth-time discussion**;
- the Batch 12AO aggregate pages were not a complete text-level negative;
- the AO transmission-level absence inference cannot remain current.

Search-index/OCR text is not physical glyph authority, so exact PT49 character forms remain unclosed.

## 3. Fullbook operational chain remains a separate question

The same public index returned zero results for `羅經 / 罗经 / 真確時候 / 真确时候 / 行漏 / 壺漏`.

Those are index-surface nonattestations only. They do not prove physical absence.

Accordingly, two questions are now explicitly separated:

1. **Jielan inclement birth-time discussion** — positively attested at PT49 index level;
2. **Fullbook-style `陰雨之際必須羅經以定真確時候` operational chain** — still not established in the Jielan target leaf, and the missing cloudy/rainy clock input remains unresolved.

## 4. Physical-facsimile route progress

Source-emitted Google Books navigation produced directly reviewable PT47 and PT48 facsimile pages. Both are genuine old-print/facsimile pages; neither is PT49. No PT49 image URL was guessed or synthesized.

NCC product `12865` directly binds the 2016 Heart-One two-volume publication `紫微斗數捷覽(明刊孤本)[原(彩)色本] 附 點校本`, ISBN `9789888317127`, 462 pages. Twelve source-emitted sample images were retrieved; direct visual review confirms genuine historical facsimile spreads, but none is PT49.

Thus Batch 12AP adds zero direct target-page glyph witnesses.

## 5. Direct Tianji chapter route

The literal chapter-64 routes in traditional and simplified Chinese both returned HTTP 403 from the exact-head GitHub runner. No chapter bytes were retrieved. Their term non-hits cannot be used as content negatives, and the probe receipt's precomputed “supersedes” boolean is ignored because its content prerequisite failed.

## 6. Provenance repair

```text
PROV-DEFECT-011=EVIDENCE_SCOPE_MISCLASSIFICATION
REPAIR=REPAIRED_FORWARD_ONLY_DURING_BATCH_12AP
```

Repair:

- preserve the exact Batch 12AO Tianji pagination result;
- retract only the unsupported transmission-level extrapolation;
- register PT49 as positive public-index evidence for inclement birth-time discussion;
- keep PT49 physical glyph authority false;
- keep the Fullbook-style 羅經—真確時候 chain unresolved.

Provenance metadata defects therefore move from **10/10 to 11/11 confirmed/repaired**.

## 7. HPA-ZDATE-006 effect

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_TIME_STANDARD_BINDING=JIELAN_INCLEMENT_BIRTH_TIME_DISCUSSION_INDEX_ATTESTED_AO_PAGINATION_SCOPE_CORRECTED_FULLBOOK_LUOJING_CLAUSE_AND_INCLEMENT_CLOCK_INPUT_STILL_UNRESOLVED
NEW_JIELAN_INCLEMENT_BIRTH_TIME_PUBLIC_INDEX_WITNESS=1
NEW_DIRECT_PHYSICAL_TARGET_WITNESS=0
NEW_HAI_GLYPH_WITNESS=0
CANDIDATE_SELECTION=NO
CANDIDATE_COLLAPSE=0
ALGORITHM_REOPEN=NO
```

Unchanged accounting:

- Matrix rows: 198
- audited rows: 166
- current MISSING_FROM_PRODUCT: 10
- cumulative missing candidate families: 14
- confirmed chart algorithm defects: 0
- algorithm reopen: 0
- candidate collapse: 0.

## 8. Next gate

1. Obtain a directly readable **PT49 / 《論十二生時難定訣》 physical facsimile leaf** with edition binding.
2. Independently continue searching Fullbook-line or sufficiently early Ziwei witnesses for an explicit cloudy/rainy **current-time acquisition mechanism**.

Do not merge those two questions and do not infer `羅經 = clock`, true solar time, or local apparent-solar runtime.

Machine evidence: `docs/research/ZIWEI-JIELAN-BIRTH-TIME-CHAPTER-SCOPE-CORRECTION-R1.json`.
