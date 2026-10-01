# Fusion Chart Historical Provenance Audit R1 — Batch 12JL

## 1997《文汇报史略》精确书目对象与公开预览边界

Status: **EXACT 1997 BOOK IDENTITY CLOSED / OPENLIBRARY OCAID NULL / GOOGLE SOURCE-EMITTED OBJECT FOLLOWED / NO IN-BOOK CONTRACT / NO SNIPPET OR FULL VIEW / CINII 202 EMPTY TRANSPORT BOUNDARY / NO 1951 TEXT REVIEWED / ZERO PRODUCT IMPACT**

### 1. 目标

12JK 保留了 1951-08-18 上海《文汇报》与《文物参考资料》第9期之间的首刊/重刊关系为未决。12JL 检查报社内部编写的 1997《文汇报史略：1949.6–1966.5》是否存在合法公开的可检索/可预览数字对象。

### 2. 精确书目身份

Open Library exact ISBN 路线返回：

```text
ISBN10 = 7805314705
edition = OL61042343M
work = OL44697053W
publish_date = 1997
pagination = 3, 2, 330 p.
ocaid = null
```

Google Books exact-ISBN 页面也直接显示目标书名、ISBN 与 1997，并 source-emit 对象：

```text
4bmRAAAACAAJ
```

因此 1997 版书目身份在现代多源书目层关闭。

### 3. Google source-emitted 对象

控制性探针只跟随 exact-ISBN 页面自己发出的对象 ID，没有猜对象。

对象页：

- HTTP 200；
- 80,616 bytes；
- SHA-256 `549ac31d448eafe9becba0a6d48a8d353fe38d8a4cdfd6d31cac6ec8cc28355d`；
- title / ISBN / 1997 均重新绑定；
- forms = 0；
- source-emitted `SearchWithinVolume` candidates = 0；
- snippet marker = false；
- full-view marker = false；
- configured 1951 target terms = false。

exact-ISBN 页面唯一带 `q=` 的链接实际上是 Google library-link → WorldCat OCLC `1462561249`，不得误判为书内搜索。

### 4. Open Library 与 CiNii 边界

Open Library 的 `ocaid=null` 只说明当前记录没有关联 Internet Archive scan，不能证明全球没有数字副本。

CiNii exact CRID 在控制 runner 返回 HTTP 202 / 0 bytes。它只能记作当前传输边界，不能作为书目不存在或全文不存在的负证据。

### 5. 控制性探针

- workflow: `.github/workflows/probe-batch-12jl-wenhui-history-1997-public-preview.yml`
- exact head: `f8362f44fdbe6f25955fcdd7ead5cccbeca2d480`
- run: `36831227298`
- job: `110268058311`
- artifact: `11146734959`
- digest: `sha256:c80467b1ab681402842ca99ba2539f35beb0589dc4aefe6aa1f018ca200d7a7c`

### 6. 证据防火墙

```text
modern newspaper-history bibliography != 1951 newspaper page
Google book object != scan
WorldCat library-link q= != in-book search
no snippet marker != text absent from physical book
OpenLibrary ocaid=null != global scan nonexistence
CiNii HTTP202 empty != negative bibliographic evidence
metadata target-term absence != book-text absence
```

### 7. 当前裁决

```text
1997 book identity
  = CLOSED_AT_MULTI_SOURCE_MODERN_BIBLIOGRAPHIC_LEVEL

Public linked scan
  = NOT_OBSERVED

Google in-book contract
  = NOT_OBSERVED

Public page-level preview
  = NOT_OBSERVED

Direct Wenhui 1951-08-18
  = NOT_REVIEWED

Direct Wenwu pp.221-233
  = NOT_REVIEWED

Direct 2011 Wenji p.197
  = NOT_REVIEWED

FIRST_PUBLICATION_STATUS
  = UNRESOLVED

WENHUI_TO_WENWU_RELATIONSHIP
  = UNRESOLVED
```

### 8. 项目影响

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；chart algorithm defects 0；algorithm reopen 0；candidate collapse 0。无 runtime、产品或 transmission graph 修改；`TRANSMISSION_IMPACT=NONE`。

### 9. 下一门

继续三条直接页级路线：

1. 上海《文汇报》1951-08-18 原页；
2. 《文物参考资料》1951年第9期 pp.221–233；
3. 2011《赵万里文集》第1卷 p.197。

只有取得直接历史文本后，才进入段落级校勘与首刊—重刊关系判断。

Research record: `docs/research/ZIWEI-WENHUI-SHILUE-1997-PUBLIC-PREVIEW-BOUNDARY-R1.json`.
