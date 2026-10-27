# Fusion Chart Historical Provenance Audit R1 — Batch 12K

## Wenguangtang public color samples + PT165 base-copy provenance

Status: **PUBLIC COLOR SAMPLES CLOSED / TARGET INDEX REPLAYED / PT165 BASE COPY UNRESOLVED / PAGE-RANGE INFERENCE FORBIDDEN / NO ALGORITHM REOPEN**

Batch 12K tests the strongest remaining inference around the Heart-One 2017 combined Wenguangtang facsimile: whether Google Books target page `PT165` can be assigned to the Dunhuatang or Jishutang base copy from public sample images and index metadata.

The answer is **no** at the current evidence level.

## 1. Reproducible public acquisition

Workflow `34174455835`, job `101900988129`, artifact `10036772401` captured:

- the Sanmin product page;
- the Heart-One publisher page;
- all eight directly linked Sanmin large try-read JPEGs;
- a fresh Google Books `SearchWithinVolume2` replay for base-copy and target terms.

Artifact ZIP SHA-256: `a5116e6a644fdb1ddd282296c853248fcb2d20ee3f4a7757ba32cef624a68a75`.

No OCR, authentication bypass or identifier guessing was used.

## 2. Eight public color facsimile samples

All eight saved JPEGs are genuine facsimile-page samples rather than site UI assets. Direct visual review without OCR finds conspicuous red collation marks on at least samples 4 and 6.

That visual feature is consistent with the publisher's description that the Jishutang witness carries red/black collation. It is **not**, however, a page-level provenance key: the reviewed public pages do not label each sample as Dunhuatang or Jishutang, and the publisher statement does not establish that every red mark is exclusive to only one source copy.

None of the eight samples contains:

- `論人生時要審的確`;
- the ten-ke target passage;
- the target `亥時` glyph in that passage.

Therefore the color samples add edition-format evidence, not the missing target glyph.

## 3. Fresh index replay

The fresh run gives:

```text
敦化堂          -> PT10, PT11
敦化堂藏板      -> PT10, PT11
繼述堂          -> no hit
繼述堂藏板      -> PT10
文光堂          -> PT18, PT28, PT79, PT122, PT154, PT237, PT250, PT251

論人生時要審的確 -> PT16, PT165
上五刻           -> PT165
下五刻           -> PT165
亥時             -> PT71, PT165, PT238, PT243
子時有十刻       -> PT82, PT165, PT182
```

The target index text at PT165 again contains the Nanyangtang-compatible reading:

`如子時有十刻上五刻属昨夜亥時下五刻属今日子時`.

This strengthens reproducibility of the **combined facsimile search-index reading** only.

## 4. Why PT165 cannot be assigned by page position

The critical provenance control is PT10.

PT10 is returned by both the Dunhuatang query and the Jishutang-cangban query. The Jishutang hit is embedded in modern editorial/publication-description text about the facsimile project, not a page-level source-switch marker.

Therefore:

```text
SOURCE_NAME_SEARCH_HIT != BASE_COPY_PAGE_BOUNDARY
PT10_MIXED_SOURCE_NAME_HITS=YES
POSITIONAL_INTERPOLATION_TO_PT165=FORBIDDEN
```

Likewise, the generic `文光堂` hits across the volume do not distinguish Dunhuatang from Jishutang.

This directly blocks a tempting but unsupported inference such as “PT165 lies after a Dunhuatang title page, therefore it must be Dunhuatang” or “red marks imply Jishutang, therefore every nearby target page is Jishutang.”

## 5. Historical adjudication

Batch 12K can support:

```text
COMBINED_WENGUANGTANG_INDEX_AT_PT165=CORROBORATES_HAI_READING
```

It cannot support:

```text
PT165=DUNHUATANG_TARGET_PAGE
PT165=JISHUTANG_TARGET_PAGE
BOTH_BASE_COPIES_INDEPENDENTLY_PRESERVE_HAI
```

Those stronger claims require an actual target image with page-level base-copy provenance or separate physical target pages.

## 6. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
DIRECT_INDEPENDENT_HAI_GLYPH_WITNESS_COUNT_ADDED=0
WENGUANG_PT165_BASE_COPY=UNRESOLVED_DUNHUATANG_VS_JISHUTANG
WENGUANG_DIRECT_TARGET_GLYPH_SUPPORT=NOT_OBTAINED
HAI_GLYPH_STABILITY_ACROSS_PHYSICAL_EDITIONS=UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES
RUNTIME_TIME_STANDARD_BINDING=UNRESOLVED
NEW_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
```

Next gate: obtain a directly readable target page with explicit Dunhuatang/Jishutang provenance, or an independent Jingluntang/Wenchengtang/Lianyuange target page.

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

Machine evidence: `docs/research/ZIWEI-WENGUANG-PUBLIC-SAMPLE-BASE-COPY-PROVENANCE-R1.json`.

The deterministic fusion-chart product remains CLOSED.
