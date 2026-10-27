# Fusion Chart Historical Provenance Audit R1 — Batch 12AQ

## 1581《紫微斗數捷覽》書目身份校勘：4051 / 王洛川直接掃描確認

Status: **DIRECT PRINTED BIBLIOGRAPHY SCAN REVIEWED / CATALOG ITEM 4051 CONFIRMED / 王洛川 GLYPH CONFIRMED WITHOUT OCR / SEARCH-SURFACE 王德川 + 4052 REJECTED AS OCR/TABLE-ALIGNMENT ARTIFACT / CURRENT REGISTRY IMPPRINT PRESERVED / NO NEW REPOSITORY PROVENANCE DEFECT / NO ALGORITHM EFFECT**

## 1. Question

After Batch 12AP corrected the evidence scope around the Jielan birth-time chapter, external search surfaced a new bibliographic conflict:

- repository / Heart-One / several received records: `明萬曆九年金陵書坊王洛川刻本`;
- one search-engine extraction of 《中國古籍善本書目·子部三》: `王德川`, with the Jielan row apparently attached to item `4052`.

Because the project treats edition identity independently from rule text, this could not be dismissed or normalized from familiarity. Batch 12AQ therefore returns to the **printed bibliography scan itself**.

## 2. Direct scan

Controlling run:

```text
WORKFLOW_RUN=34350629959
ARTIFACT=10103542053
ARTIFACT_ZIP_SHA256=c50fff947d5adf8e4eb9109d7d00485dbe7d04a7767090ca6e9109603b8c7f88
```

Direct bibliography PDF:

```text
《中國古籍善本書目·子部三》
PDF_SHA256=e562a7af9c9aac5daf641172110133f8f203cebeb1ebcd1bad4fd515979cf2ab
PAGE_COUNT=160
TARGET_PDF_PAGE=40
```

The PDF has no usable text layer for the target entry. Final adjudication therefore used the **rendered printed page, without OCR**.

Runner-produced images:

```text
FULL_PAGE_SHA256=fe32995fed004f54e94795dafa528231ba7a670c99eb13e5bea79a6ac56802b6
TARGET_CONTEXT_CROP_SHA256=e24212dbf2213be31969b995f9058dd06df6bc1beabd87b486ad752edd2a053e
```

## 3. Direct visual reading

On PDF page 40 the target column visibly reads:

```text
新刻纂集紫微斗數捷覽四卷
題宋陳摶撰
宋白玉蟾增輯
明萬曆九年金陵書坊王洛川刻本
```

The bottom catalog number directly aligned to that column is:

```text
4051
```

The immediately adjacent columns provide a built-in alignment control:

- item 4050: 《神相全編十二卷首一卷》
- item 4051: 《新刻纂集紫微斗數捷覽四卷》
- item 4052: 《上官拜命玉曆大全不分卷》

Therefore the search-surface pairing of Jielan with `4052` is demonstrably shifted by one column.

The final character judgment is also direct: the printed imprint reads **洛**, not **德**.

## 4. Independent bookseller-name control

The same runner fetched the Taiwan National Central Library official catalog record for a different Ming Jinling book, 《新刊大宋宣和遺事》. The official page directly records:

```text
明金陵王氏洛川校刊本
```

This is **not** evidence that the two books are the same copy or edition. It is an independent official-library bibliographic control showing that `王氏洛川` is a real Ming Jinling imprint/bookseller string and should not be normalized away as an implausible modern reading.

## 5. Adjudication

```text
JIELAN_1581_CATALOG_ITEM=4051
JIELAN_1581_IMPRINT_NAME=王洛川
DIRECT_GLYPH_AUTHORITY=中國古籍善本書目_SCAN_PAGE_40
SEARCH_SURFACE_王德川=REJECTED_OCR_INDEX_ARTIFACT
SEARCH_SURFACE_4052=REJECTED_TABLE_ALIGNMENT_ARTIFACT
CURRENT_REPOSITORY_REGISTRY_王洛川=PRESERVE
NEW_REPOSITORY_PROVENANCE_DEFECT=0
```

This batch therefore **does not** increment the project provenance-defect counter. The repository metadata was already on the reading supported by the direct scan.

## 6. Holding scope

Some secondary catalog/search surfaces point to an Anhui holding. Batch 12AQ does not promote that to item-level official provenance because no official Anhui item record for this exact Jielan object was bound in the controlling artifact.

Accordingly:

```text
ANHUI_HOLDING=SECONDARY_LOCATOR_ONLY
OFFICIAL_ITEM_RECORD=NOT_OBTAINED
PT49_PHYSICAL_PAGE_ROUTE=NOT_OBTAINED
```

This firewall matters because edition identity, holding identity and target-page glyph authority are separate claims.

## 7. Product / Matrix effect

No chart-affecting mechanical result changes.

```text
HPA-ZDATE-006=UNCHANGED_MISSING_FROM_PRODUCT
MATRIX=198/166
CURRENT_MISSING_FROM_PRODUCT=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
PROVENANCE_DEFECTS=11_CONFIRMED/11_REPAIRED
CHART_ALGORITHM_DEFECT=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
```

## 8. Next gate

The highest-value chart-affecting evidence remains:

1. obtain a directly readable **Jielan PT49 / 《論十二生時難定訣》 physical facsimile leaf** with edition binding;
2. independently obtain a Fullbook-line or sufficiently early Ziwei witness that explicitly states the cloudy/rainy **current-time acquisition mechanism**.

Do not spend further cycles on `王德川` unless a genuinely independent direct scan contradicts the printed bibliography reviewed here.

Machine evidence: `docs/research/ZIWEI-JIELAN-BIBLIOGRAPHIC-IMPRINT-RECONCILIATION-R1.json`.
