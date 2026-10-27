# Historical Provenance Audit — Batch 12GB

## 1. Batch identity

- Batch: `BATCH-12-ZIWEI-DENG-ZHICHENG-DIARY-2007-NLCPRESS-ITEM-DOWNLOAD-SURFACE-BOUNDARY-GB`
- Prior batch: `BATCH-12-ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-PKU-FULLTEXT-BRIDGE-PUBLIC-ACCESS-BOUNDARY-GA`
- Scope: 2007 National Library Press facsimile product-page download surface for the 1950-01-29 Deng Zhicheng diary target.
- This is an access/provenance-control batch only. It does not reopen deterministic chart algorithms.

## 2. Question

Can the item-level related-download surface on the National Library Press 2007 facsimile product page yield a lawful source-emitted object that directly closes the 1950-01-29 volume-5 page/text or handwriting?

## 3. First-party product control

The National Library Press product page for `邓之诚日记（外五种）（全八册）` remains the controlling first-party publication record:

- product route: `https://www.nlcpress.com/ProductView.aspx?Id=3967`;
- ISBN: `978-7-5013-3477-3/K·1509`;
- publication date: `2007-07-11`;
- the detailed contents place notebook 14, `1949-01-29——1950-02-16`, in volume 5.

Therefore the target date remains securely bound to **volume 5 / notebook 14**.

The same first-party page source-emits the related-download labels:

- `图书文件下载（TXT）`;
- `目录附件下载`.

On the reviewed parsed public surface, however, those labels do not expose an item-specific downloadable URL or target file object. No direct facsimile image, target leaf, target handwriting, or target text object was obtained from that surface.

## 4. Public resource-list controls

Two first-party generic resource sections were reviewed as controls:

### 4.1 目录及部分内容页

`https://www.nlcpress.com/DownLoadList.aspx?Rid=2`

The reviewed current public page exposes one unrelated resource. The Deng diary title is not listed there.

This is **not** proof that National Library Press has no item-specific file.

### 4.2 电子书下载

`https://www.nlcpress.com/DownLoadList.aspx?Rid=3`

The reviewed current public page exposes no listed resource.

This is likewise **not** proof of publisher-side content absence.

No resource-ID enumeration, guessed download URL, authentication bypass, account action, purchase or fee was attempted.

## 5. Authority firewall

The following equivalences are explicitly forbidden:

- item-level `图书文件下载（TXT）` label ≠ target TXT retrieval;
- TXT label ≠ facsimile-image or handwriting authority;
- `目录附件下载` label ≠ target 1950-01-29 page number;
- generic download-list nonappearance ≠ publisher file absence;
- product metadata ≠ direct target glyphs;
- 2008 journal pagination ≠ 2007 facsimile pagination;
- notebook date range ≠ exact target page;
- date position ≠ license to interpolate a page number.

The publisher product page therefore improves **route control**, not direct target-text authority.

## 6. Target status

After Batch 12GB:

- `TARGET_1950_01_29_VOLUME=CLOSED_AS_VOLUME_5_NOTEBOOK_14`;
- `TARGET_1950_01_29_EXACT_FACSIMILE_PAGE=UNRESOLVED`;
- `TARGET_1950_01_29_FACSIMILE_TEXT=NOT_REVIEWED`;
- `TARGET_1950_01_29_HANDWRITING_DIRECTLY_COLLATED=false`;
- `TARGET_1950_01_29_EXACT_JOURNAL_PAGE=UNRESOLVED`;
- `TARGET_1950_01_29_PRIMARY_JOURNAL_TEXT=NOT_REVIEWED`.

The item-level download labels do not close any of these fields.

## 7. Product / genealogy consequence

No transmission node or edge is added.

`NODES_ADDED=0`; `EDGES_ADDED=0`; `ACQUISITION_EDGE_AUTHORIZED=false`; `SAME_OBJECT_EDGE_AUTHORIZED=false`; `RUNTIME_RULE_CHANGE=false`; `ALGORITHM_REOPEN=false`; `CANDIDATE_COLLAPSE=false`.

Matrix row/audited/missing counts remain **198 / 166 / 10**. Provenance defects remain **14 / 14 repaired**. Chart algorithm defects remain **0**. `DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`.

## 8. Highest next gate

1. Continue lawful discovery for a source-emitted primary/fulltext object covering the 2008 serial pp.121–129 and directly locate 1950-01-29 without interpolation.
2. Continue item-specific National Library Press, library and lawful-preview routes that source-emit the exact 2007 volume-5 page/leaf; do not guess resource identifiers from generic download pages.
3. If the target facsimile page is obtained, directly collate handwriting and compare punctuation-independent wording against the editor-checked serial route and the 2012 derivative.
4. Search directly reviewed target/adjacent facsimile pages for `铜壶漏箭制度`, `准斋心制几漏图式`, `3482/3483`, `03482/03483`, the 1823 士礼居 fingerprint or another stable identifier.
5. Continue Gu Tinglong 1950-01-06, NLC [23]/[24], Ji Shuying chapter 9 and Gao Xizeng annotated-catalog routes in parallel.

Machine evidence: `docs/research/ZIWEI-DENG-ZHICHENG-DIARY-2007-NLCPRESS-ITEM-DOWNLOAD-SURFACE-BOUNDARY-R1.json`.
