# Fusion Chart Historical Provenance Audit R1 — Batch 12O

## Korea University independent physical-copy provenance and post-12N access-control closure

Status: **KOREA UNIVERSITY FIRST-PARTY PHYSICAL SET BOUND / UNDATED JIANGZUO SHULIN WOODBLOCK CATALOG IDENTITY CLOSED / TARGET PAGE STILL PENDING / POST-12N SNU-HANYANG ACCESS PROBES CLOSED AS CONTROLS / NO ALGORITHM REOPEN**

Batch 12O adjudicates the committed probes after Batch 12N. Its main positive result is a new first-party Korea University Library physical-set route. The SNU and Hanyang probes are retained only as access controls because neither exposes a direct `五凶神` target page.

## 1. Korea University first-party catalog identity

Korea University Library's exact public detail page is:

`https://library.korea.ac.kr/detail/?cid=CAT000000737166&ctype=o`

The URL was reached from an exact href rendered by the public integrated-search surface; no hidden endpoint guessing or authentication was used.

The first-party detail directly records:

- title: `新刻合倂十八飛星策天紫微斗數全集`;
- responsibility: `陳搏(宋) 著 ; 白玉蟾(宋) 增 ; 徐良弼 ; 陳道 ; 唐謙(淸) 共校`;
- edition: `木板本(中國)`;
- publication: `[刊寫地未詳] : 江左書林 , [刊寫年未詳]`;
- extent: `6卷6冊 : 圖 ; 16.0 ×11.3 cm`;
- label title: `飛星紫微斗數`;
- juan-3 title note: `新刻希夷陳先生紫微斗數全集`.

This closes only the catalog-scoped identity of an undated Jiangzuo Shulin woodblock set. It does not infer a print year that the reviewed record does not provide.

## 2. Physical holding identity

The holding block lists six physical items at `中央도서관/한적실/`, all under call-number root `대학원 C10 B8` and marked `대출불가(열람가능)`:

| volume | call number | registration number |
| --- | --- | --- |
| 1 | `대학원 C10 B8 1` | `465000245` |
| 2 | `대학원 C10 B8 2` | `465000246` |
| 3 | `대학원 C10 B8 3` | `465000247` |
| 4 | `대학원 C10 B8 4` | `465000248` |
| 5 | `대학원 C10 B8 5` | `465000249` |
| 6 | `대학원 C10 B8 6` | `465000250` |

Therefore Korea University is now independently bound at the **physical holding-object level** from the already bound SNU and Hanyang holdings.

That does not yet establish textual-stemma independence. A distinct holding, or even a distinct catalog imprint, cannot count as a separate late-Zi textual/glyph vote until the relevant target page is directly observed and collated.

## 3. Korea University search-surface controls

The exact-detail workflow is run `34211567451`, artifact `10050023318`, SHA-256 `afa6d4345c3213a525787e19bded25a7a6f161e4638ad10abdaf6d71c2ffb15e`.

Additional public-search controls are:

- KLIN/integrated-search run `34211325461`, artifact `10049960495`;
- old-book archive run `34211721066`, artifact `10050121958`.

One integrated-search surface returned a holdings non-hit for the exact title while the exact first-party detail page demonstrably exists. That result is therefore a search-surface/index-scope control, not evidence of physical absence.

The old-book archive search also does not bind a public digital object for the target page. No conclusion of “never digitized”, “no image exists”, or “target text absent” is authorized.

## 4. SNU public-share control

Run `34209828645`, artifact `10049328514`, directly binds the public share entry:

`【飛星策天紫微斗數全集】一簑古523.5-J562b-v.1-6 陳博(宋) 著 羊城[同治9年(1870)]明經閣 木版本（4）.pdf`

The public browser did **not** open a preview and exposed no target page. The adjudication is therefore:

```text
SNU_V4_PUBLIC_FILE_ROUTE=BOUND
SNU_PUBLIC_PREVIEW_OPENED=NO
SNU_TARGET_PAGE=PREVIEW_ROUTE_BOUND_NOT_TARGET_PAGE
SAME_SNU_LINEAGE_INDEPENDENT_VOTE_ADDED=0
```

The filename is provenance/access evidence, not target-text evidence.

## 5. Hanyang material-request controls

Run `34189277789`, artifact `10041642791`, reaches two normal public service pages:

- `보존서고자료 신청` at `/search/collection-materials/ccls-info`;
- `원문제공신청` at `/search/non-collection-materials/dds-info`.

The reviewed pages do not establish that either route applies to the Hanyang rare-book item `484926 / HOM000001861`. Accordingly:

```text
HANYANG_PRESERVATION_STACK_ROUTE_APPLIES_TO_RAREBOOK=UNRESOLVED
HANYANG_DOCUMENT_COPY_ROUTE_APPLIES_TO_RAREBOOK=UNRESOLVED
REQUEST_SUBMITTED=NO
TARGET_PAGE=PENDING_DIRECT_PAGE
```

No external request is submitted in this batch.

## 6. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
KOREA_UNIVERSITY_CATALOG_CONTROL=CAT000000737166
KOREA_UNIVERSITY_PHYSICAL_SET=BOUND
KOREA_UNIVERSITY_CATALOG_IMPRINT=JIANGZUO_SHULIN_UNDATED_WOODBLOCK
KOREA_UNIVERSITY_TARGET_PAGE=PENDING_DIRECT_PAGE
INDEPENDENT_TARGET_TEXT_WITNESS_ADDED=0
INDEPENDENT_HAI_GLYPH_WITNESS_ADDED=0
NEW_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
```

The next high-value gate is a directly readable `五凶神` target page from the Korea University set, Hanyang, the SNU lineage, or another independently bound physical Quanji copy. Only after page-level binding may the wording be compared mechanically with the Nanyangtang `亥時` witness.

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

Machine evidence: `docs/research/ZIWEI-KOREA-UNIVERSITY-INDEPENDENT-PHYSICAL-COPY-PROVENANCE-R1.json`.

The deterministic fusion-chart product remains CLOSED.
