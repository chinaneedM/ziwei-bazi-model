# Fusion Chart Historical Provenance Audit R1 — Batch 12GZ

## 《文津学志》第三辑：国家图书馆出版社“相关下载”通用模板控件证据强度纠偏

Status: **CROSS-PRODUCT FIRST-PARTY TEMPLATE CONTROL CLOSED / PRODUCT-4396 LABEL OBSERVATION RETAINED / LABEL PRESENCE ALONE NO LONGER ACCEPTED AS PROOF OF PRODUCT-SPECIFIC ATTACHMENT OBJECT / 12GX EVIDENCE-STRENGTH INTERPRETATION SUPERSEDED FOR CURRENT INFERENCE / ATTACHMENT OBJECT-URL-BYTES STILL UNRESOLVED / ZERO MATRIX, PRODUCT, RUNTIME OR GENEALOGY CHANGE**

## 1. Why this correction is necessary

Batch 12GX directly observed the literal line on 国家图书馆出版社 product 4396:

```text
相关下载 图书文件下载（TXT）  目录附件下载
```

That literal observation remains valid. The over-strong part was the inference that those labels themselves established a product-specific attachment/download surface.

Batch 12GY then showed that the publisher's global public resource center does not list product 4396. That still did not determine whether product-local attachment objects exist.

12GZ adds the missing control: unrelated first-party product pages.

## 2. Cross-product first-party controls

The same label pair appears unchanged on:

```text
Product 9992
文津学志（第九辑）
出版时间 2016-08-01
库存 无书

Product 11285
文津学志（第十四辑）
出版时间 2020-11-17
库存 有书

Product 12345
文津学志（第二十一辑）
出版时间 2024-01-31
库存 有书

Product 12455
郑振铎藏文献保存同志会档案文献汇编（全八册）
页面显示出版时间 2030-09-30
2026-09-27 审查时属于未来日期页面
库存 无书
当前审查文本面未暴露“目录”区块
```

All four pages print:

```text
相关下载 图书文件下载（TXT）  目录附件下载
```

First-party comparator URLs:

- https://www.nlcpress.com/ProductView.aspx?Id=9992
- https://www.nlcpress.com/ProductView.aspx?Id=11285
- https://www.nlcpress.com/ProductView.aspx?Id=12345
- https://www.nlcpress.com/ProductView.aspx?Id=12455

This recurrence materially changes the evidentiary meaning of the labels.

## 3. Current adjudication

```text
PRODUCT_4396_LABELS_LITERAL_OBSERVATION = RETAINED

LABEL_PAIR_GENERIC_TEMPLATE_LIKE_CONTROL
  = HIGH_CONFIDENCE

LABEL_PRESENCE_ALONE_PROVES_PRODUCT_SPECIFIC_ATTACHMENT_OBJECT
  = false

PRODUCT_4396_TXT_ATTACHMENT_OBJECT_EXISTENCE
  = UNRESOLVED

PRODUCT_4396_TOC_ATTACHMENT_OBJECT_EXISTENCE
  = UNRESOLVED

DIRECT_ATTACHMENT_URL
  = UNRESOLVED

ATTACHMENT_BYTES
  = NOT_RECOVERED
```

The correct current statement is therefore narrower than Batch 12GX:

> the product page visibly carries generic related-download labels; the existence of product-specific attachment objects has not yet been demonstrated.

## 4. Forward-only revision of 12GX / 12GY

The repository does not erase the earlier batch records.

```text
12GX literal observation = preserved
12GX "official download surface exists" inference = superseded for current inference
12GY global-resource-center nonlisting = preserved
12GY "product-local labels remain valid" = interpreted as literal label presence only
```

This is an evidence-strength correction, not a claim that the files do not exist.

## 5. Negative-scope firewall

```text
GENERIC_LABEL_CONTROL
  != proof that attachments do not exist

GLOBAL_RESOURCE_CENTER_NONLISTING
  != proof that product-local browser action cannot expose a file

FUTURE-DATED PRODUCT PAGE WITH SAME LABELS
  != proof that all product pages have no downloads
```

No endpoint guessing, enumeration, login, cookie/token reuse, identity transmission or fee occurred.

## 6. Article-level status

```text
《〈冀淑英文集〉补遣》 AUTHOR = UNRESOLVED
PAGE RANGE = UNRESOLVED
BODY = NOT_REVIEWED
FOOTNOTES = NOT_REVIEWED
```

## 7. Product / genealogy consequence

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

Accounting remains `198 / 166 / 10`, provenance metadata defects `14 / 14 repaired`, chart algorithm defects `0`.

## 8. Highest next gate

1. Require a **product-specific object** before calling product 4396's attachment route closed: direct href/action, normal-browser download target/result, or independent first-party resource record.
2. Continue reverse-index discovery for the 2010 `《〈冀淑英文集〉补遣》` author and exact pages.
3. Continue direct 2004 `《冀淑英文集》` p.335 / neighboring pages / final `《編后記》`.
4. Continue direct 1997 `《北京图书馆馆史资料汇编（二）：1949—1966》` pp.446–449 collation.

Research record: `docs/research/ZIWEI-WENJIN-XUEZHI-V3-NLCPRESS-GENERIC-RELATED-DOWNLOAD-TEMPLATE-CORRECTION-R1.json`.
