# Fusion Chart Historical Provenance Audit R1 — Batch 12IV

## 《赵万里文集》第1卷机构目录 HTML 边界：Google Books 公共 HTML 可绑定书名/ISBN，但无电子书且卷次元数据冲突

Status: **GOOGLE BOOKS PUBLIC HTML 200 / TARGET TITLE + ISBN OBSERVED / NO EBOOK / NO P197 / GOOGLE DISPLAYED VOLUME-3-526P CONFLICT QUARANTINED / HATHITRUST 403 / WORLDCAT 429+403 / LOC EXACT-QUERY ZERO ROUTE ONLY / STANFORD SEARCH SHELL NO TARGET / PRINCETON CHALLENGE / ZERO PRODUCT CHANGE**

### 1. 目标

Batch 12IU 已关闭 CiNii 发出的日本机构 OPAC 内容增强面，但 2011《赵万里文集》第1卷 p.197 仍未直接取得。12IV 改用已闭合的稳定标识：

- ISBN `9787501346653`
- OCLC `775628715`
- LCCN `2011426732`

探测公开 Google Books HTML、HathiTrust、WorldCat、Library of Congress、Stanford SearchWorks 与 Princeton Catalog，仅做匿名 GET 与有限内容分类。

### 2. 控制探针

Probe commit: `33e5f05400d1d2877f3934728e919f65bfb29317`

Workflow run: `36735868424`

Artifact: `11106488630`

Artifact digest: `sha256:b8d1d67465db34adcfd6be1463fa3e8aa62ee9dc79ee5c2aabb153256e2a2154`

### 3. Google Books 公共 HTML：API 429 之外的新有效路由

精确 ISBN VID 路线：

`https://books.google.com/books?vid=ISBN9787501346653`

当前 HTTP 200，页面可见：

- 目标书名《趙万里文集》；
- ISBN `9787501346653`；
- 国家图书馆出版社 / 2011；
- 页面明确显示“未提供电子书”。

页面没有：

- literal p.197；
- 瞿济苍 / 凤起 / 旭初；
- 《永乐大典》目标词；
- 六十二种；
- preview / full view / read online 等实际页级入口。

因此 Google Books API 先前的 429 并不等于 Google Books 全部公共表面不可用；但当前可用 HTML 仍没有 p.197。

### 4. Google Books 元数据冲突防火墙

同一 HTML 上，ISBN `9787501346653` 与书名同时出现，但书目信息区还显示“第3卷”与“526页”。

项目已由国家图书馆出版社 Product 5325、Open Library edition、CiNii/日本机构 OPAC 多条路线把该 ISBN 锁定为**第1卷**。因此 12IV 的 Google Books “第3卷 / 526页”只能记为外部聚合元数据冲突：

`GOOGLE_BOOKS_VOLUME_METADATA_CONFLICT = QUARANTINED`

不得用它覆盖第1卷身份，不新增 provenance defect 计数，也不得把同一 ISBN 下的 Google 聚合显示当作独立实体卷本。

### 5. 其他路线

- HathiTrust exact ISBN：HTTP 403，访问边界，无负面文本权重。
- WorldCat ISBN search：HTTP 429；OCLC direct title route：HTTP 403。两者均未裁决内容。
- LOC Books/Printed Material JSON exact LCCN / exact ISBN：HTTP 200，但当前结果列表为空。仅关闭当前 LOC web-search 路由，不能外推“美国国会图书馆绝无该书”。
- Stanford ISBN search：HTTP 200，但返回的当前搜索壳未绑定目标书名/ISBN。
- Princeton：HTTP 200 后重定向至 challenge 页面；未绕过。

### 6. 项目裁决

Direct 2011 p.197 继续为 `NOT_REVIEWED`。

本批次不：

- 新增规则候选；
- 修改 Matrix 198 / 166；
- 修改 17/17 provenance repair；
- 重开排盘算法；
- 改变 transmission graph。

### 7. 下一门

停止重复当前 Google Books ISBN HTML、HathiTrust、WorldCat、LOC、Stanford ISBN 搜索壳及 Princeton challenge 路线，除非响应状态或链接对象改变。下一优先级转向：

1. 新的合法页级/机构数字对象路线以直接取得 2011 p.197；
2. `wwck195109.pdf` 或等价 1951 第9期开放对象；
3. 冀淑英《古籍善本十五讲》第九讲 / 第10–11讲直接页码证据。

Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENJI-V1-INSTITUTIONAL-CATALOG-HTML-BOUNDARY-R1.json`.
