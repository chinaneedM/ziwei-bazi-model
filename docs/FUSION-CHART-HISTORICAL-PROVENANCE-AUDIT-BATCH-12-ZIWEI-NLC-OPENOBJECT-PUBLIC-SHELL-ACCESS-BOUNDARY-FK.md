# Fusion Chart Historical Provenance Audit R1 — Batch 12FK

## NLC data_892 OpenObject 公開對象殼、PDF 對象路徑與權限邊界

Status: **TONGHU/ZHUNZHAI PUBLIC OPENOBJECT SHELL METADATA DIRECTLY CLOSED / PDF OBJECT PATH DIRECTLY CLOSED / PUBLIC FORMATCATALOG TITLE RESPONSE CLOSED / PAGE COUNT AND FULL OBJECT MANIFEST NOT PUBLICLY CLOSED WITHOUT PERMISSION RESULT / NO PERMISSION ENDPOINT INVOKED / NO LOGIN OR TOKEN EMULATION / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Scope

Batch 12FJ closed:

```text
銅壺      data_892 FID 411999008600 / bid 113028
準齋      data_892 FID 411999008601 / bid 113029
```

12FK asks how much of the corresponding NLC reader object can be established from public routes **without invoking permission endpoints or bypassing access controls**.

## 2. First-party probes

### 2.1 Main public-object probe

```text
RUN      = 36024889534
ARTIFACT = 10819487008
DIGEST   = sha256:29d7d4aef4c38beb320f10ce73cdd6ae7cd19d420e878799e5019e9fe54a96de
OCR_USED = false
```

This probe requested only public GET/object/catalog/image routes. It did **not** invoke:
- `/OutOpenBook/resIpPermission`
- `/OutOpenBook/dataInOutPermission`
- `/allSearch/permissionNew`
- login/SSO/token endpoints.

### 2.2 Tonghu shell retry

The first broad Tonghu shell request timed out. A bounded public-shell-only retry succeeded:

```text
RUN      = 36025150571
ARTIFACT = 10818922726
DIGEST   = sha256:8ab91df8fa0a06603f5d3b17d871108a12f971008bcf031454299ba8b864281b
HTTP     = 200
OCR_USED = false
```

## 3. Public OpenObject shell metadata

### 3.1 銅壺漏箭制度

Direct public loader HTML:

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

HTML SHA-256:

```text
e9f9e7cc5b57186b74812dcde048058858f7b4a4eaa86e61b9aed996d8083c75
```

### 3.2 準齋心製几漏圖式

Direct public loader HTML:

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

HTML SHA-256:

```text
2b3c0bb1aa1e4289ec14434f069e3b0883fbea18f76c8238dea3832780f499b9
```

The two objects therefore form a direct first-party paired object-shell control:

```text
FID 411999008600 -> bid 113028 -> SBGJ03908_00001.pdf
FID 411999008601 -> bid 113029 -> SBGJ03909_00001.pdf
```

## 4. Public formatCatalog control

The first-party public catalog endpoint returned:

```json
{"success":true,"msg":"","obj":[{"chapter_name1":"","chapter_num1":"銅壺漏箭制度"}]}
{"success":true,"msg":"","obj":[{"chapter_name1":"","chapter_num1":"準齋心製几漏圖式"}]}
```

Source hashes:

```text
Tonghu   053f7a3f3a2f08370fea1e4ab73dca4486f1badf01a34f75feab4b2a896f2e11
Zhunzhai 23b0b6ffcfd551b1f57fce855116c3480ec2c2a84a38ee83bd90d08eb764b921
```

This closes the public one-chapter title structure exposed by that endpoint. It does not expose page count.

## 5. Permission architecture observed in the public shell

The public loader JavaScript directly shows this sequence before reading:

```text
/OutOpenBook/resIpPermission
/OutOpenBook/dataInOutPermission
/OutOpenBook/resInOutPermission
login/SSO check when required
/allSearch/permissionNew
```

Only after `permissionNew` succeeds does the page consume:

```text
openFlag
readPageNum
```

and choose one of the web PDF readers.

The project did not invoke these permission endpoints in this batch.

Therefore:

```text
PUBLIC_SHELL_METADATA                 = CLOSED
PUBLIC_PDF_OBJECT_PATH                = CLOSED
PUBLIC_FORMATCATALOG_CHAPTER_TITLE    = CLOSED
READ_PAGE_COUNT_WITHOUT_PERMISSION    = NOT_PROVED
FULL_PUBLIC_OBJECT_MANIFEST           = NOT_PROVED
ACCESS_CONTROL_BYPASS                 = NOT_ATTEMPTED
```

## 6. Bounded image control

A first-party public image URL for Tonghu's first `SBGJ03908_00001` image returned HTTP 200 as JPEG:

```text
SHA256 = 71701a6dc199c6a3541a2550628df72f90d1e23b08aa0fb95723836721d028f3
```

The bounded `00002/00003` guesses returned 404 and must not be used to infer page count. Zhunzhai image attempts were partly timeout/404. This image probe is only a public-object/cover control.

## 7. Identifier firewall

12FK strengthens, but does not merge, the layers closed in 12FJ:

```text
meta.nlc.cn original rare-book SYS/UID
905$s rare-book local call
read.nlc.cn data_892 FID
OpenObject aid/bid
public loader pdfname
microfilm SYS/UID
microfilm 905$b 登錄號
public barcode
historical acquisition/donation event
```

No layer is substituted for another.

## 8. Acquisition-provenance side finding

Independent public historical sources continue to support a mixed Qu-family transfer history (sale + donation). A separate 1953-03-03 donation inventory is reported as only 99 titles / 100 volumes, while NLC's official historical overview reports 246 donated titles in total. This further warns that nonappearance in one donation inventory may not be an exhaustive negative.

Target-specific classification remains:

```text
SALE_ROUTE_SELECTED     = false
DONATION_ROUTE_SELECTED = false
FINAL_ACQUISITION_PATH  = UNRESOLVED
```

## 9. Transmission and product consequence

12FK strengthens the two existing NLC digital-resource nodes and `TG-E0113/TG-E0114` with public object-shell and permission-boundary evidence. No new lineage edge is required.

```text
DIRECT_SANMING_PARENT_VOTE_INCREMENT=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 10. Next gate

1. prioritize target-specific Qu-family sale/donation/acquisition archival evidence rather than further permission-gated page-count probing;
2. keep the NLC page-count/full-manifest field explicitly `ACCESS_CONTROL_BOUNDARY_NOT_PUBLICLY_CLOSED` unless a lawful public first-party route appears;
3. continue pre-1578 Zhunzhai and independent Sanming/Yueling Dahan–Rainwater + Nanjing-59 lines in parallel.

Research record: `docs/research/ZIWEI-NLC-OPENOBJECT-PUBLIC-SHELL-ACCESS-BOUNDARY-R1.json`.
