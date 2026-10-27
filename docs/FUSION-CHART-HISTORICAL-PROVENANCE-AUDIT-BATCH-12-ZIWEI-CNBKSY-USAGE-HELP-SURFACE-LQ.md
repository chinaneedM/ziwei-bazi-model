# Fusion Chart Historical Provenance Audit R1 — Batch 12LQ

## 全国报刊索引：公开“使用帮助”表面与动态帮助候选

Status: **HELP PAGE HTTP 200 / SEARCH-MODE NAVIGATION CONFIRMED / FIELD-LEVEL HELP NOT RENDERED / DYNAMIC HELP ROUTES NOT YET AUTHORIZED / NO QUERY / ZERO PRODUCT IMPACT**

控制 run `36888840223` / job `110458979575` 在 exact head `fe6aa0848c23bd839295d9ac105d558924f83d8f` 上匿名读取第一方 source-emitted `/portal/footCategory?id=61`（使用帮助），返回 HTTP 200、43685 bytes、SHA-256 `b1eb40bfc76842b2d4cb4d33527cfbda52075b31ebd90aa93cd27b22699a8226`。

可见文本只有 179 字符，明确再次出现“文献检索 / 普通检索 / 高级检索 / 专业检索 / 图片检索”导航，但 `题名、作者、刊名、分类号、年份、期号、检索词、关键词、全文、逻辑、布尔` 均为 0 次。因此不能声称帮助页已经给出字段级检索说明。

页面 inline script 同时出现 `/portal/footCategory/findNews`、`/portal/footCategory/findNews?id=61`、`/portal/footCategory/footerList?id=61` 等候选，但现有摘要中包含注释掉的 AJAX 代码。12LQ 不执行任何候选。

下一门 12LR 只做静态注释状态与调用点分析：先确定哪些 route 是 active code、哪些只是 line/block/HTML comment，再闭合 method/data/callback；在此之前禁止调用。

控制证据：workflow `.github/workflows/probe-batch-12lq-cnbksy-usage-help-contract.yml`; run/job/artifact `36888840223 / 110458979575 / 11175557446`; artifact digest `sha256:814009359f6f745bd742b2e5bd1053e668f9be38da7f20ce34f3a6a27a34f55d`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-USAGE-HELP-SURFACE-R1.json`.
