# Fusion Chart Historical Provenance Audit R1 — Batch 12AZ

## 《張果星宗大全》濰坊市圖書館萬曆二十二年本線索與山東公開路由跨出口審計

Status: **HIGH-VALUE 1594 WEIFANG LOCATOR RETAINED / FIRST-PARTY SHANDONG OBJECT NOT BOUND / LINUX + MACOS + WINDOWS GITHUB RUNNERS TIME OUT ON REVIEWED OFFICIAL/API/OBJECT ROUTES / NO TARGET BYTES / ACCESS FAILURE IS NOT TEXTUAL ABSENCE / ZERO TEXT OR HAI-GLYPH VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Why this batch exists

Batch 12AW supplied a direct 1594 physical witness. Batch 12AY confirmed a separate Jangseogak 1594 holding but could not obtain its target leaf. AZ follows another high-value lead that repeatedly identifies Shandong resource `151613020240003` as a Weifang Library holding of 《新編評註通玄先生張果星宗大全》, ten juan, described as a Wanli-22 / 1594 Tang-Qian edition.

The research question is deliberately narrow: can this locator be promoted to a first-party Shandong object with readable page bytes? Until that happens, it is not a direct physical witness.

## 2. Locator identity and scope

The discovery route converges on:

```text
resource_id=151613020240003
title=新編評註通玄先生張果星宗大全
extent=十卷
edition_claim=明萬曆二十二年(1594)唐謙刻本
holding_claim=濰坊市圖書館藏
```

These fields are retained as a **multi-index/route locator claim**. AZ did not receive a first-party Shandong catalog/API response, so:

```text
OFFICIAL_CATALOG_METADATA_DIRECTLY_BOUND=false
PHYSICAL_COPY_IDENTITY_DIRECTLY_BOUND=false
DIRECT_PHYSICAL_WITNESS_AUTHORITY=false
```

The locator remains important because, if bound, it could provide an independently held 1594 comparison leaf.

## 3. Reviewed Shandong routes

First-party-domain routes tested:

```text
http://guji.sdlib.com/dev-api/ancientbooks/front/getFileContentPage/3/151613020240003
https://guji.sdlib.com/dev-api/ancientbooks/front/getFileContentPage/3/151613020240003
http://guji.sdlib.com/front/#/bookInfo?resId=151613020240003
https://guji.sdlib.com/front/#/bookInfo?resId=151613020240003
```

A secondary-locator-derived old object-host pattern was also tested only for byte reachability:

```text
http://124.133.52.174:9009/res-book/wsok/潍坊市图书馆12种36册2818拍/151613020240003/object/PDF/{volume}/{page}.pdf
```

The old-host template is not treated as bibliographic authority.

## 4. Initial Linux acquisition probe

```text
workflow_run_id=34596426615
job_id=103253128834
artifact_id=10262594953
artifact_digest=sha256:b87cc49072291d22824f233a4e9947e4bfc7ab7fa119d2774137b41115eed4bd
```

The official domain and sampled old-object routes timed out. No PDF bytes and no rendered pages were obtained.

```text
OFFICIAL_API_RESPONSE_OBTAINED=false
DOWNLOADED_PDF_SAMPLES=0
RENDERED_PAGES=0
```

That result alone could have been a runner-specific network issue, so AZ did not stop there.

## 5. Cross-egress verification

Run `34597728895` repeated a minimal five-route reachability probe on three GitHub-hosted operating systems/regions.

### Linux / westus3

```text
job_id=103257322652
artifact_id=10263155974
digest=sha256:09e64e311d183bec3118281067e87fd96efd77049122efd55e2aa4c79ad12813
```

All five reviewed routes timed out.

### macOS / westus

```text
job_id=103257322513
artifact_id=10263650215
digest=sha256:27a7e18e197fc9d2f048cd5661f5be04119f594359290e8164aa43485aacc4e6
```

All five reviewed routes timed out.

### Windows / eastus

```text
job_id=103257322572
artifact_id=10263550354
digest=sha256:94edec77055a666f98cf78d62febe80928e3c90435a2f7ca05c651e2dbd0e267
```

All five reviewed routes timed out.

## 6. Adjudication: reachability is not absence

The combined observation is stronger than a single-run failure: multiple GitHub-hosted environments could not reach the reviewed Shandong endpoints. It still authorizes only an execution/public-route boundary.

It does **not** authorize:

```text
RESOURCE_GONE=true
NO_DIGITIZATION=true
PHYSICAL_HOLDING_ABSENT=true
TARGET_PASSAGE_ABSENT=true
WHOLE_HOLDING_TEXT_NEGATIVE=true
```

No first-party bytes means no glyph adjudication.

## 7. Witness accounting

```text
HIGH_VALUE_1594_LOCATOR_RETAINED=true
OFFICIAL_SHANDONG_OBJECT_BYTES_OBTAINED=false
TARGET_LEAF_OBTAINED=false
DIRECT_GLYPH_COLLATION_AUTHORIZED=false
WHOLE_HOLDING_TEXT_NEGATIVE_AUTHORIZED=false
SAME_EDITION_TEXT_STABILITY_VOTE_INCREMENT=0
INDEPENDENT_TARGET_TEXT_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
```

The AW 1594 NIJL/Tohoku leaf remains the controlling direct physical witness for its own wording.

## 8. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

No runtime behavior changes are authorized.

## 9. Accounting

```text
ROW_COUNT=198
AUDITED_ROW_COUNT=166
MISSING_FROM_PRODUCT=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_PROVENANCE_DEFECTS=11
REPAIRED_PROVENANCE_DEFECTS=11
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

No Historical Audit Matrix count changes are authorized.

## 10. Durable artifact

```text
docs/research/ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-R1.json
```

## 11. Next gate

1. Obtain a reachable **first-party** Shandong/Weifang catalog or object response for `151613020240003`; bind edition/holding metadata before upgrading source authority.
2. If page bytes become readable, directly collate the target leaf without OCR and compare it to the AW 1594 physical page.
3. In parallel, pursue other early independent holdings, especially the SOAS/NCL union-catalog lead, while separating genuine early copies from later reprints such as Morrison-line material.
