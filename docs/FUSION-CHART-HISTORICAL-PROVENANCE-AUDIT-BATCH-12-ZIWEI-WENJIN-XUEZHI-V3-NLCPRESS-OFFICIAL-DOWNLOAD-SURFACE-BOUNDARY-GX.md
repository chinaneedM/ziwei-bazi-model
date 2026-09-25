# Fusion Chart Historical Provenance Audit R1 — Batch 12GX

## 《文津学志》第三辑：国家图书馆出版社第一方 TXT / 目录附件下载面

Status: **FIRST-PARTY NLCPRESS PRODUCT ID 4396 DIRECTLY REVIEWED / ISBN 978-7-5013-4085-9 CLOSED / OFFICIAL “图书文件下载（TXT）” AND “目录附件下载” LABELS EXPOSED / UNDERLYING ATTACHMENT URLS NOT EXPOSED IN REVIEWED TEXT INTERFACE / NO ENDPOINT GUESSING OR AUTH BYPASS / ARTICLE BYLINE-PAGES-BODY STILL UNRESOLVED / ZERO PRODUCT OR GENEALOGY CHANGE**

## 1. Why this batch matters

12GQ closed the formal existence of `《〈冀淑英文集〉补遣》` from a published TOC. 12GU then closed three exact Japanese physical holdings. The stronger next route is now first-party: the National Library of China Press itself exposes downloadable resources for the exact third volume.

## 2. First-party product identity

The directly reviewed publisher page `https://www.nlcpress.com/ProductView.aspx?Id=4396` shows:

```text
文津学志（第三辑）
编著者：国家图书馆善本特藏部
ISBN：978-7-5013-4085-9
出版时间：2010-05-25
版次：B1
印刷时间：2010-05-01
印次：Y1
丛书名：文津学志
中图分类：G255.1
```

## 3. Official related-download surface

The same page directly prints under `相关下载`:

```text
图书文件下载（TXT）
目录附件下载
```

So the official TXT and TOC attachment surfaces are directly exposed by the first-party product page.

## 4. Access firewall

The reviewed text interface does not expose the underlying attachment URLs as selectable link objects. No path was guessed and no endpoint was enumerated.

```text
DIRECT_ATTACHMENT_URL = UNRESOLVED_IN_REVIEWED_INTERFACE
ATTACHMENT_BYTES = NOT_RECOVERED
LOGIN_ATTEMPTED = false
TOKEN_OR_COOKIE_REUSE = false
ENDPOINT_GUESSING = false
```

A download label is not treated as downloaded evidence.

## 5. Article-level status

The product page's `编著者 国家图书馆善本特藏部` is volume-level responsibility and cannot be promoted to the byline of each article.

```text
《〈冀淑英文集〉补遣》 AUTHOR = UNRESOLVED
PAGE RANGE = UNRESOLVED
BODY = NOT_REVIEWED
```

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

1. Resolve the public first-party attachment URL behind product 4396's `目录附件下载` or `图书文件下载（TXT）` without guessing or bypassing access controls.
2. Once an official attachment is directly accessible, inspect it first for the supplement article byline/page range.
3. Continue direct 2004 p.335 / neighboring pages / final `《編后記》`.
4. Continue direct 1997 pp.446–449 archival collation.

Research record: `docs/research/ZIWEI-WENJIN-XUEZHI-V3-NLCPRESS-OFFICIAL-DOWNLOAD-SURFACE-BOUNDARY-R1.json`.
