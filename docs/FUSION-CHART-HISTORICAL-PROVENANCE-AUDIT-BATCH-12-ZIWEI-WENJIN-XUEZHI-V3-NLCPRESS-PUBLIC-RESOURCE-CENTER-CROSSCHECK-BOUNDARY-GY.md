# Fusion Chart Historical Provenance Audit R1 — Batch 12GY

## 《文津学志》第三辑：国家图书馆出版社公共资源下载中心反向检索边界

Status: **FIRST-PARTY NLCPRESS GLOBAL PUBLIC RESOURCE CENTER CROSSCHECKED / PRODUCT 4396 NOT LISTED IN CURRENT PUBLIC DOWNLOAD LISTS / 12GX PRODUCT-LOCAL TXT + TOC LABELS REMAIN VALID / NO CLAIM THAT ATTACHMENTS DO NOT EXIST OR THAT NORMAL BROWSER ACTION CANNOT EXPOSE THEM / ARTICLE BYLINE-PAGES-BODY STILL UNRESOLVED / ZERO PRODUCT OR GENEALOGY CHANGE**

## 1. Why this batch matters

Batch 12GX closed a first-party product-local fact: product `4396` for `《文津学志（第三辑）》` explicitly prints two labels under `相关下载`:

```text
图书文件下载（TXT）
目录附件下载
```

The unresolved question was whether the publisher's own global public download center exposes those same resources as independently listed downloadable objects. Batch 12GY checks that reverse-discovery route without guessing any URL.

## 2. First-party global resource-center structure

The National Library of China Press public site exposes separate download categories:

```text
书目下载
目录及部分内容页
电子书下载
MARC数据下载
其他下载
```

The reviewed public routes are:

```text
https://www.nlcpress.com/DownLoadList.aspx?Rid=1
https://www.nlcpress.com/DownLoadList.aspx?Rid=2
https://www.nlcpress.com/DownLoadList.aspx?Rid=3
https://www.nlcpress.com/DownLoadList.aspx?Rid=4
https://www.nlcpress.com/DownLoadList.aspx?Rid=5
```

## 3. Direct crosscheck result

On the currently reviewed public surfaces:

- `目录及部分内容页` lists exactly one object: `《中国图书馆馆史》（全四册）综合索引`, whose public detail route is `DownloadView.aspx?RId=87`;
- `电子书下载` exposes no listed records;
- `MARC数据下载` exposes no listed records;
- the reviewed `书目下载` and `其他下载` lists contain unrelated resources;
- no list exposes product `4396`, `《文津学志（第三辑）》`, or a target-specific TXT/目录 attachment record.

Therefore:

```text
GLOBAL_PUBLIC_RESOURCE_CENTER_TARGET_LISTING = NOT_OBSERVED
DIRECT_PRODUCT_4396_ATTACHMENT_URL = UNRESOLVED
ATTACHMENT_BYTES = NOT_RECOVERED
```

## 4. Critical negative-scope firewall

This is a route-specific negative, not a claim of nonexistence.

```text
NOT_LISTED_IN_CURRENT_GLOBAL_PUBLIC_RESOURCE_CENTER
  != attachment does not exist
  != Batch 12GX product-local labels are false
  != normal interactive browser action cannot expose a product-local target
  != JavaScript/postback/product-event route is absent
```

No download endpoint was guessed or enumerated. No login, cookie/token reuse, identity transmission or fee occurred.

## 5. Article-level status

Nothing in the global resource-center crosscheck exposes the article byline or page span.

```text
《〈冀淑英文集〉补遣》 AUTHOR = UNRESOLVED
PAGE RANGE = UNRESOLVED
BODY = NOT_REVIEWED
FOOTNOTES = NOT_REVIEWED
```

Batch 12GQ's formal article-existence conclusion, Batch 12GU's physical-holding routes and Batch 12GX's product-local download-label conclusion all remain intact.

## 6. Product / genealogy consequence

```text
NODES_ADDED=0
EDGES_ADDED=0
DIRECT_COPY_EDGE_AUTHORIZED=false
SAME_OBJECT_EDGE_AUTHORIZED=false
ACQUISITION_EDGE_AUTHORIZED=false
RUNTIME_RULE_CHANGE=false
ALGORITHM_REOPEN=false
CANDIDATE_COLLAPSE=false
MATRIX_COUNT_CHANGE=false
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains `198 / 166 / 10`, provenance defects `14 / 14 repaired`, chart algorithm defects `0`.

## 7. Highest next gate

1. Continue only lawful public first-party discovery for product 4396 attachment targets when actually surfaced by normal publisher UI, search results or navigation; do not guess paths or enumerate endpoints.
2. Continue public article-level reverse-index discovery for `《〈冀淑英文集〉补遣》` author and exact page span.
3. Continue direct 2004 `《冀淑英文集》` p.335 / neighboring pages / final `《編后記》`.
4. Continue direct 1997 `《北京图书馆馆史资料汇编（二）：1949—1966》` pp.446–449 collation.
5. Any library reference/copy request remains an explicit user-authorized external action.

Research record: `docs/research/ZIWEI-WENJIN-XUEZHI-V3-NLCPRESS-PUBLIC-RESOURCE-CENTER-CROSSCHECK-BOUNDARY-R1.json`.
