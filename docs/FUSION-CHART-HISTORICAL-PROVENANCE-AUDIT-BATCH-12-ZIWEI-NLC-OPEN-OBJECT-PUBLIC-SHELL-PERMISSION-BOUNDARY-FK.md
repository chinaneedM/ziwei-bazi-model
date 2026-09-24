# Fusion Chart Historical Provenance Audit R1 — Batch 12FK

## 國家圖書館數字古籍 OpenObjectBook 公開殼層與頁級對象權限邊界

Status: **TONGHU/ZHUNZHAI PUBLIC OPEN-OBJECT SHELL DIRECTLY CLOSED / BID 113028/113029 + FID 411999008600/601 + INTERNAL PDF OBJECT PATH DIRECTLY EXPOSED / PUBLIC FORMATCATALOG TITLE-ONLY RESPONSE CLOSED / PAGE-LEVEL MANIFEST AND PAGE COUNT NOT EXPOSED BEFORE PERMISSION FLOW / NO PERMISSION ENDPOINT INVOCATION / NO LOGIN EMULATION / NO TOKEN ACQUISITION / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12FJ closed the NLC digital-resource layer:

```text
銅壺漏箭制度:
  data_892 FID = 411999008600
  open-object bid = 113028

準齋心製几漏圖式:
  data_892 FID = 411999008601
  open-object bid = 113029
```

The next gate was deliberately narrow: determine whether the public `OpenObjectBook` route exposes page count or an object manifest **without** invoking authentication, IP entitlement, token generation, or any access-control bypass.

## 2. Controlling first-party probes

### 2.1 Initial public route probe

GitHub Actions:

```text
RUN      = 36024889534
ARTIFACT = 10819487008
DIGEST   = sha256:29d7d4aef4c38beb320f10ce73cdd6ae7cd19d420e878799e5019e9fe54a96de
OCR_USED = false
```

Direct results:

```text
Zhunzhai OpenObjectBook HTTP:
  HTTP 200
  bytes = 14619
  sha256 = 2b3c0bb1aa1e4289ec14434f069e3b0883fbea18f76c8238dea3832780f499b9

Tonghu OpenObjectBook:
  first probe timed out; retried separately below

formatCatalog:
  Tonghu  id=113028 -> HTTP 200
    {"success":true,"msg":"","obj":[{"chapter_name1":"","chapter_num1":"銅壺漏箭制度"}]}
    sha256 = 053f7a3f3a2f08370fea1e4ab73dca4486f1badf01a34f75feab4b2a896f2e11

  Zhunzhai id=113029 -> HTTP 200
    {"success":true,"msg":"","obj":[{"chapter_name1":"","chapter_num1":"準齋心製几漏圖式"}]}
    sha256 = 23b0b6ffcfd551b1f57fce855116c3480ec2c2a84a38ee83bd90d08eb764b921
```

The catalog endpoint returns a one-title catalog entry for each object. It does **not** expose page count, page manifest, image list, or PDF page map.

### 2.2 Tonghu public-shell retry

GitHub Actions:

```text
RUN      = 36025150571
ARTIFACT = 10818922726
DIGEST   = sha256:8ab91df8fa0a06603f5d3b17d871108a12f971008bcf031454299ba8b864281b
OCR_USED = false
```

The first retry succeeds:

```text
HTTP 200
bytes = 14613
sha256 = e9f9e7cc5b57186b74812dcde048058858f7b4a4eaa86e61b9aed996d8083c75
```

The public HTML directly exposes:

```text
indexName  = data_892
id         = 113028.0
identifier = 411999008600
title      = 銅壺漏箭制度
servercode = 3
aid        = 892
bid        = 113028.0
pdfname    = data09/sbgj_shanbenguji/20151221_01szsb4171/duixiang/
             SBGJ03908_00001/SBGJ03908/00001/SBGJ03908_00001.pdf
```

The Zhunzhai shell symmetrically exposes:

```text
indexName  = data_892
id         = 113029.0
identifier = 411999008601
title      = 准齋心製几漏圖式
servercode = 3
aid        = 892
bid        = 113029.0
pdfname    = data09/sbgj_shanbenguji/20151221_01szsb4171/duixiang/
             SBGJ03909_00001/SBGJ03909/00001/SBGJ03909_00001.pdf
```

The internal PDF object paths are therefore direct public-shell metadata. They are **not** treated as permission to bypass the reader.

## 3. Permission-flow boundary

Both public shells contain the same reader control chain:

```text
/OutOpenBook/resIpPermission
/OutOpenBook/dataInOutPermission
/allSearch/permissionNew
/static/webpdf/indexnobj.html
```

The shell code states that the actual web-PDF reader path is selected only after the permission checks return an allowed state. The permission response can supply the last-read page and open flag before the iframe reader is loaded.

This batch intentionally does **not** call:

- `resIpPermission`;
- `dataInOutPermission`;
- `permissionNew`;
- login/SSO emulation;
- token acquisition;
- direct internal-PDF retrieval intended to bypass the reader.

Therefore:

```text
PUBLIC_SHELL_METADATA                 = CLOSED
PUBLIC_BID/FID/PDF_OBJECT_PATH        = CLOSED
PUBLIC_FORMATCATALOG_TITLE            = CLOSED
PUBLIC_PAGE_COUNT                     = NOT_EXPOSED_ON_REVIEWED_PRE_PERMISSION_SURFACE
PUBLIC_PAGE_MANIFEST                  = NOT_EXPOSED_ON_REVIEWED_PRE_PERMISSION_SURFACE
AUTHORIZED_READER_PAGE_MANIFEST       = NOT_ACQUIRED
ACCESS_CONTROL_BYPASS                 = NOT_ATTEMPTED
```

This is an access-boundary conclusion, not a claim that no page manifest exists behind authorized reader access.

## 4. Bounded public image-name test

The first probe also checked only three bounded cover-like names per title. It did **not** enumerate a page namespace.

Observed:

```text
Tonghu:
  SBGJ03908_00001.jpg -> HTTP 200 image/jpeg
  SBGJ03908_00002.jpg -> HTTP 404
  SBGJ03908_00003.jpg -> HTTP 404

Zhunzhai:
  _00001 request timed out in that run
  _00002 -> HTTP 404
  _00003 -> HTTP 404
```

The successful Tonghu first image is the already-known cover image. The 404s show that simple numeric suffix increment is not a demonstrated page-image route. No page count may be inferred from these three bounded probes.

## 5. Identifier and object-layer firewall

Batch 12FK changes none of the FJ classifications:

```text
Original rare-book current SYS:
  001775082 / 001775083

Original rare-book local holdings:
  NLC:SBYL:03482 / NLC:SBYL:03483

NLC digital FID:
  411999008600 / 411999008601

NLC open-object bid:
  113028 / 113029

Microfilm work SYS:
  002146415 / 002146416

Microfilm 905$b login/registration:
  00O003570 / 00O003571
```

The newly recovered `pdfname` values are internal digital-object path metadata. They are not:

- rare-book call numbers;
- microfilm registration numbers;
- public barcodes;
- Qu-family acquisition/donation identifiers;
- evidence for a different physical-copy identity.

## 6. Transmission-genealogy consequence

12FK strengthens the two existing NLC `data_892` digital-surrogate nodes and their evidence-scoped `ATTESTS` edges:

```text
DIGITAL-NLC-DATA892-TONGHU-FID411999008600-BID113028
DIGITAL-NLC-DATA892-ZHUNZHAI-FID411999008601-BID113029

TG-E0113
TG-E0114
```

No new physical-copy node, `SAME_OBJECT`, direct-copy, authorship, chronology, or Sanming-parent edge is authorized.

## 7. Product firewall

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
MISSING_FROM_PRODUCT=10
PROVENANCE_DEFECTS=13/13_REPAIRED
CONFIRMED_CHART_ALGORITHM_DEFECTS=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
DIRECT_SANMING_PARENT_VOTE_INCREMENT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 8. Next gate

1. Continue target-specific Qu-family sale/donation/transfer/accession research; the historical acquisition route remains unresolved.
2. If a legitimately public NLC endpoint later exposes page-count or manifest metadata before authorization, bind it separately; do not call permission/token endpoints merely to complete this audit.
3. Keep the pre-1578 Zhunzhai rule line and independent Sanming/Yueling Dahan–Rainwater + Nanjing-59 lines active.

Research record: `docs/research/ZIWEI-NLC-OPEN-OBJECT-PUBLIC-SHELL-PERMISSION-BOUNDARY-R1.json`.
