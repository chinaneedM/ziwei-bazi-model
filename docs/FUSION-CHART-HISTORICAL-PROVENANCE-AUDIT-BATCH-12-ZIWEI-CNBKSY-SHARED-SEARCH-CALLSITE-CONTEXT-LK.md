# Fusion Chart Historical Provenance Audit R1 — Batch 12LK

## 全国报刊索引：shared search call-site 参数语义闭合

Status: **COMMON-HINTS CALLSITE CLOSED / NULL PAYLOAD AT CALLSITE / DETAIL ROUTES ARE CART OBJECT ROUTES / TRANSPORT IMPLEMENTATION STILL OPEN / NO POST / NO TARGET QUERY / ZERO PRODUCT IMPACT**

12LJ 发现 `/common/hints`、`/search/detail/`、`/search/picDetail/` 等共享脚本路线，但未闭合它们的调用参数。12LK 只重新读取同一公开 seed 与其 source-emitted “信息动态”页面，截取这些 token 周围的静态调用代码；没有执行任何新路线。

控制 run `36884632716` / job `110444683909` 在 exact head `ca62dc9074dc04f4bffc410d8b8f2170217d2ff5` 上成功。

### `/common/hints`

直接静态上下文为：

`searchHint(fields, hideclass) -> bksy.post("/common/hints", null, callback)`

callback 将返回值直接作为 `conditions`，再对调用方传入的 field selectors 绑定 typeahead；匹配发生在浏览器本地 `substringMatcher(conditions)` 中。

因此当前可确定：

- endpoint literal：`/common/hints`；
- call-site payload：`null`；
- 该 helper 调用本身不发送用户检索词；
- 返回值用途：本地提示词条件集合；
- **尚未闭合**：`bksy.post` 对 `null` 的实际 HTTP method/body/content-type/dataType 实现。

### `/search/detail/` / `/search/picDetail/`

这两条路由来自购物车内容：

- text：`/search/detail/{item.dataId}/{item.laId}/{item.laId}`
- image：`/search/picDetail/{item.dataId}/{item.laId}/{item.laId}`

所以它们是已有 object identifier 驱动的详情页路由，**不是自由文本检索入口**。

### 信息动态筛选

`/portal/newsCategoryBrowse/listPortal` 再次被 jqGrid 代码闭合为 site-news JSON 列表接口，`postData` 来自 `title/startDate/endDate` 表单；继续与历史报纸数据库检索隔离。

```text
COMMON_HINTS_CALLSITE = CLOSED
COMMON_HINTS_PAYLOAD_AT_CALLSITE = NULL
COMMON_HINTS_HTTP_TRANSPORT = OPEN
DETAIL_ROUTES = OBJECT_ID_DRIVEN_NOT_FREE_TEXT_SEARCH
TARGET_QUERY = NOT_SUBMITTED
```

下一门 12LL 只在同页面 source-emitted scripts 中定位 `bksy.post` / `bksy.jsonPost` 的实现，先闭合 method/body/content-type/dataType；仍不执行 `/common/hints`。

控制证据：workflow `.github/workflows/probe-batch-12lk-cnbksy-shared-search-callsite-context.yml`; run/job/artifact `36884632716 / 110444683909 / 11173687084`; artifact digest `sha256:a0ef4c32000ee750948c5f9a60b7ebdf9645862a204b4d2ead00af874b0bddbd`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-SHARED-SEARCH-CALLSITE-CONTEXT-R1.json`.
