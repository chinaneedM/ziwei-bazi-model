# Fusion Chart Historical Provenance Audit R1 — Batch 12N

## 1870 Mingjingge Quanji: Hanyang official volume-4 physical-copy binding and public-resource closure

Status: **HANYANG FIRST-PARTY PHYSICAL COPY BOUND / VOLUME 4 ITEM IDENTITY CLOSED / CURRENT PUBLIC DIGITAL RESOURCE ROUTE RETURNS NO RECORD / FIVE-XIONG-SHEN TARGET PAGE STILL PENDING / NO ALGORITHM REOPEN**

Batch 12N upgrades the Batch 12M Hanyang University locator from a secondary bibliography to Hanyang University Library's own public catalogue, item and resource APIs.

## 1. Official public search

The public Hanyang UI at `/search/i-discovery` directly returned six local holdings for `新刻合倂十八飛星策天紫微斗數全集`. Volume 4 is visible as:

`新刻合倂十八飛星策天紫微斗數全集. 卷4 / 羊城 : 明經閣, 同治九年(1870)`

with call number `133.3 진412ㅅ v.4` at `[서울]백남학술정보관`.

The search interaction naturally emitted the public catalogue request. No hidden endpoint guessing, authentication or parameter expansion was used.

## 2. Structured record identity

The public search JSON binds:

```text
V3=484927
V4=484926
V5=484925
V6=484924
```

Volume 4 is therefore not merely a title-string locator; it is Hanyang bibliographic object `484926`.

## 3. Official volume-4 physical description

A click on the rendered public UI result naturally navigates to:

`/search/i-discovery/484926?type=biblios-list-view`

The first-party detail/API record directly gives:

- title: `新刻合倂十八飛星策天紫微斗數全集. 卷4`;
- responsibility: `陳博(宋) 著 ; 徐良弼(淸) 校正`;
- edition: `木板本`;
- publication: `羊城 : 明經閣, 同治九年(1870)`;
- extent: `1冊`, with set note `6卷6冊`;
- physical format: `四周單邊, 半郭 10.4 x 9.2 cm, 無界, 12行24字, 頭註, 上內向黑魚尾 ; 15.7 ×10.8 cm`;
- cover title: `紫微斗數`;
- inside-cover title: `飛星紫微斗數`;
- banxin title: `飛星斗數`;
- colophon note: `同治九年(1870) 新鐫 陳希夷先生 飛星紫微斗數 羊城 明經閣板`;
- item id: `872523`;
- accession/barcode: `HOM000001861`;
- call number: `133.3 진412ㅅ v.4`;
- location: `[서울]백남학술정보관 / 고전자료실`;
- item state: on shelf; circulation: not available.

This closes Hanyang as a first-party, separately held physical copy rather than a secondary locator.

## 4. Current public digital-resource boundary

The public detail UI naturally requested:

`/pyxis-api/1/biblios/484926/resources?isForPyxis3=true`

The exact observed request was replayed without modification. It returned HTTP 200 with:

```json
{"success":true,"code":"success.noRecord","message":"조회된 결과가 없습니다."}
```

Therefore the authorized conclusion is narrowly:

`HANYANG_CURRENT_PUBLIC_CATALOG_DIGITAL_RESOURCE_OBJECT=NO_RECORD`

This does **not** mean the physical volume has never been digitized, cannot be reproduced, or is absent from non-public/institutional systems.

## 5. Target-text boundary

Neither the bibliographic detail nor the public resources route exposes `五凶神`, `子有十刻`, or a page image. A catalogue detail is not a target-text search corpus, so no negative textual claim is permitted.

Accordingly:

```text
HANYANG_PHYSICAL_COPY=INDEPENDENTLY_BOUND
HANYANG_TARGET_PAGE=PENDING_DIRECT_PAGE
INDEPENDENT_TARGET_TEXT_WITNESS_ADDED=0
INDEPENDENT_HAI_GLYPH_WITNESS_ADDED=0
```

The SNU and Hanyang holdings are distinct physical-object routes at the catalogue level. They become independent textual/glyph votes only after target pages are directly observed.

## 6. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
HANYANG_VOLUME4_BIBLIO_ID=484926
HANYANG_VOLUME4_ITEM_ID=872523
HANYANG_VOLUME4_ACCESSION=HOM000001861
HANYANG_PUBLIC_RESOURCES=success.noRecord
HANYANG_FIVE_XIONG_SHEN_TARGET_PAGE=PENDING_DIRECT_PAGE
DIRECT_INDEPENDENT_HAI_GLYPH_WITNESS_COUNT_ADDED=0
NEW_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
```

Next gate: a directly readable `五凶神` target page from the Hanyang physical copy or another independent Quanji physical copy.

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

Machine evidence: `docs/research/ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-R1.json`.

The deterministic fusion-chart product remains CLOSED.
