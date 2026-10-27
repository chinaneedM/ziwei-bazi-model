# Fusion Chart Historical Provenance Audit R1 — Batch 12KZ

## NCPSsd 赵万里详情对象 scalar inventory：1951年第9期 221–233 页闭合

Status: **SAME CLOSED DETAIL POST / IDENTICAL RESPONSE SHA / PAGES 221–233 / PUBLISHDATE 1951-09-01 / ABSTRACT+KEYWORDS CLOSED / NO NEW ENDPOINT / ZERO PRODUCT IMPACT**

12KY 已恢复 101-key 第一方详情对象，但当时选择器用了 `beginPage/endPage`，而实际 key 为 lower-case。12KZ 不发现也不执行任何新 endpoint，只重放同一个已经闭合的详情 POST。

本批直接取得：

```text
beginpage    = 221
endpage      = 233
publishdate  = 1951-09-01
source       = nssd
firstwriter  = 趙萬里
vol          = 0
volumn       = 1951
processdate  = 2014-05-26
```

同时返回中文摘要与关键词。响应仍为与 KY 完全相同的 2426-byte object，SHA-256 `90f093e92044908b8e16a0dc8147f408e875565a9bc82ccbddebc38c5a666243`。

结合 12KY：

```text
title      = 永樂大典展覽的意義——一九五一年八月北京圖書舘舉辦
author     = 趙萬里
label      = 文物
year       = 1951
issue      = 9
pages      = 221–233
pagecount  = 13
ISSN       = 0511-4772
```

这一 year/issue/pages bundle 与 12KE/KF 的国家图书馆文津记录、12JK 的国家图书馆官方综述完全对齐。当前只剩载体名层面的历史/现代 crosswalk：1951 原期由独立书目控制写作《文物参考资料》，而现代数据库把同一记录显示为“文物”。

KZ 没有跟随 `pdfurl`、`qkEncryptedUrl` 或任何阅读/下载/登录/收藏/用户接口。

控制证据：workflow `.github/workflows/probe-batch-12kz-ncpssd-zhao-detail-scalar-inventory.yml`; exact head `78090cb6aa8a186b0cc157e5fd0ff67a85a02c34`; run/job/artifact `36870170475 / 110395607091 / 11166187855`; artifact digest `sha256:8645f60140f9835a5ef32a32c76d649eb1e2a859f45c3fc1e3cdba1ac7c42e31`。

下一门 12LA：用 CiNii 前后继 serial record 与文物出版社官方发展史直接校准《文物参考资料》→《文物》的改名关系；不再依赖题名相似度推断。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 无新增边。

Research record: `docs/research/ZIWEI-NCPSSD-ZHAO-DETAIL-SCALAR-INVENTORY-R1.json`.
