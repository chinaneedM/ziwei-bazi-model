# Batch 12CR — 《虎鈐經·傳箭》識典 × 天一閣數字替身去重控制

## Status

```text
SHIDIAN_PUBLIC_PHYSICAL_PAGE_ROUTE=CLOSED
SHIDIAN_TIAN YIGE_IMAGE_IDENTITY=HIGH_CONFIDENCE_SAME_UNDERLYING_PHYSICAL_COPY
NEW_INDEPENDENT_PHYSICAL_WITNESS=false
NEW_RECENSION_VOTE=false
HUQIAN_MECHANICAL_VOTE_INCREMENT=0
SANMING_ANCESTRY_VOTE_INCREMENT=0
TRANSMISSION_IMPACT=NONE
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
CANDIDATE_COLLAPSE=NONE
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

> Note: the status token above should be read as `SHIDIAN_TIANYIGE_IMAGE_IDENTITY`; spacing in the human-readable label is not a schema identifier.

## 1. Why this batch exists

Batch 12CJ had already counted two genuinely distinct received physical witnesses for the core 《虎鈐經·傳箭》 mechanics: a Tianyige Ming-print witness and a CADAL/Siku-recension witness. After Batch 12CQ, a new Shidian public-reader route for `NGJ8921188204889` yielded source-bound images for 卷七. Before using those pages as evidence, Tianwen must decide whether they represent a third physical witness or merely another platform serving the already-counted Tianyige object.

This batch closes that deduplication question.

## 2. Shidian source-bound physical-page acquisition

Exact live-head acquisition route:

```text
HEAD=d14cbe2155e76bbce366acbb9be1cde612e2e7d1
WORKFLOW_RUN=35245252336
ARTIFACT=10507166653
ARTIFACT_DIGEST=sha256:201c538217056e21b726c0ae9eb7b17eaa4d76e86543575f48f5e1730880c5bf
BOOK_ID=NGJ8921188204889
CHAPTER=虎鈐經卷第七
RETURNED_PHYSICAL_PAGES=137..158 (22 leaves)
OCR_USED_FOR_GLYPH_OR_IDENTITY_CLAIMS=false
```

The runner used the site's own public browser chain:

```text
public chapter page
-> byted_psdk.getPtokenStatus
-> /api/ancientlib/read/book/pages/v3/
-> byted_psdk.decrypt
-> source-bound WebP images
```

The first request returned transient `40001`; a fresh page/token cycle returned `errorCode=0` and all 22 requested leaves available within the returned range. The workflow hard-failed if fewer than 20 images were obtained.

## 3. Direct physical reading remains consistent with the already-known Huqian rule

Direct visual review of the source-bound Shidian leaves shows the same target sequence already closed in 12CJ. In particular:

- Shidian p147 visibly begins `傳箭第七十六` and the hundred-ke / sixty-fen framework;
- the winter sequence begins from the 40/60 end of the ladder;
- Shidian pp151–152 cover the late-spring / summer-solstice transition area, including the familiar 59/41 and 60/40 region;
- the subsequent leaves continue the descending half-year sequence.

No OCR is used as glyph authority, and no new mechanical claim is created from the Shidian transcription surface.

## 4. Digital-surrogate identity test

The decisive issue is not whether the words agree, but whether the **physical image object** is independent.

A no-OCR image comparison was run between individual Shidian leaves and the previously archived Tianyige/Wikimedia spread images from Batch 12CJ. The continuous mapping is:

```text
Shidian 137..158
  = Tianyige spreads 69R,69L,70R,70L,71R,71L,72R,72L,73R,73L,
    74R,74L,75R,75L,76R,76L,77R,77L,78R,78L,79R,79L
```

The target section gives especially strong machine controls:

| Shidian leaf | Tianyige spread half | SIFT good matches | RANSAC inliers | inlier ratio |
|---:|---|---:|---:|---:|
| 147 | 74R | 411 | 355 | 0.864 |
| 148 | 74L | 534 | 454 | 0.850 |
| 149 | 75R | 558 | 491 | 0.880 |
| 150 | 75L | 371 | 309 | 0.833 |
| 151 | 76R | 484 | 384 | 0.793 |
| 152 | 76L | 501 | 402 | 0.802 |
| 153 | 77R | 487 | 409 | 0.840 |
| 154 | 77L | 505 | 401 | 0.794 |

Direct visual comparison independently shows the same column geometry, gutter/border shape, paper damage, ink defects and stains at the same positions. This is far stronger than textual agreement.

## 5. Deduplication adjudication

The safe conclusion is:

```text
Shidian NGJ8921188204889
    = alternate digital surrogate / rehosted page route
      for the already-counted Tianyige Ming-print physical scan sequence

therefore:
NEW_PHYSICAL_WITNESS=NO
NEW_RECENSION_VOTE=NO
NEW_HUQIAN_NUMERIC_VOTE=NO
```

Platform independence is not physical-witness independence. Counting Shidian and Wikimedia/Tianyige separately would double-count the same underlying copy and artificially inflate evidence weight.

The provider's public text page need not itself declare “Tianyige” for this adjudication: image-level identity binds the digital route to the previously established Tianyige scan sequence.

## 6. Transmission-genealogy impact

```text
TRANSMISSION_IMPACT=NONE
```

Reason: no new historical text, edition, physical copy, mechanical rule or lineage edge is introduced. This batch only strengthens access-route provenance and prevents duplicate evidence counting. The existing graph nodes and edges created/strengthened in 12CJ remain controlling.

This distinction is important for Tianwen's future large-scale source graph:

```text
same physical scan on two platforms != two historical witnesses
same physical copy with two digital surrogates != independent recension support
```

## 7. Product adjudication

Nothing in this batch changes the deterministic product or late-Zi problem:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_CHANGE=NONE
NEW_RUNTIME_CANDIDATE=false
ALGORITHM_REOPEN=NONE
CANDIDATE_COLLAPSE=NONE
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Audit accounting remains:

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
CUMULATIVE_IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
PROVENANCE_METADATA_DEFECTS=12/12_REPAIRED
```

## 8. Next gate

The Shidian route is now closed as a deduplicated surrogate route. The Sanming ancestry search returns to the unresolved high-value gates from 12CQ:

1. obtain direct `大統曆通軌 / 大統曆日通軌` morning-evening numerical cells;
2. continue securely pre-1578 Nanjing/Datong witnesses for the `59/41` cap;
3. require reproduction of the 1578 Sanming intermediate/change-day fingerprint, not merely shared extrema;
4. keep exact parentage and historical quantization unresolved until page-level evidence closes them.

Research record:

`docs/research/ZIWEI-HUQIANJING-SHIDIAN-TIANYIGE-DIGITAL-SURROGATE-DEDUP-R1.json`
