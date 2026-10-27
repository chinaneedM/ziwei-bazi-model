# Fusion Chart Historical Provenance Audit R1 — Batch 12JE

## 人民日报官方数据档案：公开搜索表单存在，但匿名检索执行层统一落入 500 包装

Status: **OFFICIAL PEOPLE-DATA RMRB ENTRY HTTP 200 / SOURCE-EMITTED SAME-HOST GET SEARCH FORM OBSERVED / SOURCE-EMITTED SEARCH-CENTER LINK OBSERVED / CURRENT SOURCE-EMITTED ARTICLE TITLE USED AS POSITIVE CONTROL / POSITIVE CONTROL + 3 HISTORICAL TARGET QUERIES ALL RETURN IDENTICAL 846-BYTE 500 WRAPPER / SEARCH RESULT SET NOT INTERPRETABLE / NO TARGET-ABSENCE INFERENCE / 12JD 1951-08-13 HIGH-CONFIDENCE DATE PRESERVED / OFFICIAL NEWSPAPER IMAGE STILL NOT REVIEWED / ZERO PRODUCT, MATRIX, RUNTIME OR GENEALOGY CHANGE**

### 1. Why this batch exists

Batch 12JD 已裁决郑振铎《关于〈永乐大典〉》的书目日期冲突：

- 国家图书馆 2019 官方转载：1951-08-13；
- 国家图书馆 2025 官方综述 PDF：1951-08-31；
- 非官方逐日报纸公开转录：8月13日第3版存在目标题名，8月31日页未见目标题名。

12JD 因缺少《人民日报》官方原版影像，只把 8月13日设为 HIGH-confidence controlling date，并将 8月31日隔离为冲突值。

12JE 继续检查**人民日报官方数据档案** `https://data.people.com.cn/rmrb` 是否提供公开、可执行、可校准的搜索路线，从而可能进一步裁决 12JD。

### 2. Reproducible probe

Probe workflow:

`.github/workflows/probe-batch-12je-rmrb-official-archive-search-contract.yml`

Successful run:

- exact probe head: `a1ff4c9a4ac6553349b1025895a626b9f7e36bc6`
- workflow run: `36766920501`
- artifact: `11120444534`
- artifact digest: `sha256:4cbe562934dfc3e4ee4cbb06bc93ca8493a8dd586290051de5ca3e101f4829e0`

No login, account action, subscription bypass, historical-date URL synthesis or private endpoint guessing was used.

### 3. Official entry and source-emitted contract

Official entry:

`https://data.people.com.cn/rmrb`

Current anonymous response:

- HTTP 200；
- redirects to current daily issue route `/rmrb/20260930/1?code=2`；
- directly emits a same-host GET search form:
  - action: `https://data.people.com.cn/rmrb/s`
  - hidden `type=1`
  - hidden `dataTime=DESC`
  - checked `ty=3`
  - text field `queryStr`
- directly emits search-center link `https://data.people.com.cn/sc?cId=23`.

Therefore:

`OFFICIAL_PUBLIC_SEARCH_FORM_CONTRACT = OBSERVED`

The search-center page itself returns HTTP 200 but exposes login wording and no HTML form; 12JE therefore uses only the search form directly emitted by the official RMRB entry page.

### 4. Positive-control calibration

To determine whether the public form is actually executable, the probe does **not** start with the 1951 target.

It first selects a current article link directly emitted by the same official entry page and uses that exact visible title as a positive-control query.

Positive-control title:

`发挥文理工医交叉融合优势 努力在服务新时代国家战略中当先锋作表率`

This article is visibly source-emitted on the entry page, so a functioning exact-title search path should not be treated like an unknown historical target.

Observed result:

- HTTP 200；
- response size: 846 UTF-8 bytes；
- SHA-256 of UTF-8 body:
  `d7aae3f0a88b671c7f7617d3ef8639f141e389d2396bfa967a743671cd9c8a7a`
- visible wrapper contains `500页面` and `网络不给力`；
- positive-control query literal not returned；
- zero same-host result anchors；
- zero followed article results.

Therefore the current anonymous execution backend is not a usable calibrated search result surface.

### 5. Historical target queries

Through the exact same source-emitted GET form contract, the probe submits:

1. `关于《永乐大典》`
2. `关于永乐大典`
3. `永乐大典`

All three return:

- HTTP 200；
- exactly 846 UTF-8 bytes；
- exactly the same SHA-256:
  `d7aae3f0a88b671c7f7617d3ef8639f141e389d2396bfa967a743671cd9c8a7a`
- the same visible `500页面 / 网络不给力` wrapper；
- no query literal；
- no target title；
- no 1951-08-13 / 1951-08-31 date；
- no same-host result anchor.

Because the current-title positive control fails identically:

```text
TARGET_QUERY_ZERO_RESULT = NOT ESTABLISHED
TARGET_ABSENCE = NOT ESTABLISHED
1951_08_31_ABSENCE_IN_OFFICIAL_ARCHIVE = NOT ESTABLISHED
1951_08_13_OFFICIAL_ARCHIVE_HIT = NOT ESTABLISHED
```

The observed 200 status is a transport status for an application-level error wrapper, not a successful search-result status.

### 6. Relation to Batch 12JD

12JE does **not** upgrade 12JD to official-image closure.

Current control remains:

- 郑振铎《关于〈永乐大典〉》 controlling publication date: `1951-08-13`
- confidence: `HIGH`
- NLC 2025 `1951-08-31`: `BIBLIOGRAPHIC_DATE_CONFLICT_QUARANTINED_PENDING_OFFICIAL_NEWSPAPER_SCAN`
- official People's Daily original scan reviewed: `false`

12JE only explains why the currently visible official archive search form cannot resolve that final image-level conflict anonymously.

### 7. Zhao target firewall

The Zheng article remains a parallel exhibition-history source, not Zhao Wanli's target article.

Unchanged:

- 2011《赵万里文集》第1卷 p.197: `NOT_REVIEWED`
- 1951《文物参考资料》第9期 pp.221–233: `NOT_REVIEWED`
- 1997《北京图书馆馆史资料汇编（二）》pp.446–449: `NOT_REVIEWED`

No text witness, historical transaction fact or target-page authority is added.

### 8. Project consequence

- Matrix: 198 rows / 166 audited
- MISSING_FROM_PRODUCT: 10
- provenance metadata defects: 17 / 17 repaired
- chart algorithm defects: 0
- algorithm reopen: 0
- candidate collapse: 0
- transmission graph change: none
- runtime/product change: none

### 9. Next gate

1. Return highest priority to direct lawful recovery of 2011《赵万里文集》第1卷 p.197.
2. Continue 1951《文物参考资料》第9期 pp.221–233 / `wwck195109.pdf` public-object recovery.
3. Continue 1997《北京图书馆馆史资料汇编（二）》pp.446–449 direct-page recovery.
4. Revisit official People's Daily archive search only when the source-emitted form produces a working positive control, or when a source-emitted official historical page/image link becomes directly observable.

Research record: `docs/research/ZIWEI-RMRB-OFFICIAL-ARCHIVE-PUBLIC-SEARCH-EXECUTION-BOUNDARY-R1.json`.
