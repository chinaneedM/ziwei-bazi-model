# Fusion Chart Historical Provenance Audit R1 — Batch 12LJ

## 全国报刊索引：公开索引新闻页 → source-emitted 信息动态合同

Status: **PUBLICLY INDEXED FIRST-PARTY SEED 200 / SOURCE-EMITTED NAVIGATION 200 / NEWS FILTER CONTRACT CLOSED / SHARED SEARCH ROUTES DISCOVERED BUT NOT FOLLOWED / NO TARGET QUERY / ZERO PRODUCT IMPACT**

12LI 已穷尽公开活动页本身的静态合同。12LJ 改用公开搜索引擎已经索引到的第一方 CNBKSY 页面：

`https://www.cnbksy.com/portal/newsCategoryBrowse/newsContent?id=202`

该 URL 本身返回 HTTP 200，并 source-emits “信息动态” → `/portal/newsCategoryBrowse`。12LJ 只跟随这一条页面自己发出的导航，不猜路径。

控制 run `36880973426` / job `110432320720` 在 exact head `138782e377ddcc68a369eefe956edd3982bfd98a` 上成功：

- seed：HTTP 200，41404 bytes，SHA-256 `ecfdd4f39f861143ff1efd7ebbea03814ab8b29064fea7c1517769026d49d3e0`；
- source-emitted 信息动态页：HTTP 200，42741 bytes，SHA-256 `8648badbfe1c751170a90797d40e05aab968fa93483cfe5102ecb27e74ee985b`。

信息动态页直接暴露一张 POST 表单，无显式 action，字段为：

- `title`
- `startDate`
- `endDate`

页面专属 inline script 发出：

- `/portal/newsCategoryBrowse/listPortal`
- `/portal/newsCategoryBrowse/newsContent`

这套合同只能认定为 **站点“信息动态”新闻筛选**，不能当成《中国近代报纸资源全库》或历史报纸正文检索合同。

同一页面的共享 inline script 另行发出：

- `/common/hints`
- `/search/detail/`
- `/search/picDetail/`
- 以及 cart / login / account / fulltext-request 等路线。

其中 `/common/hints` 与 `searchHint/findMatches` 语义，以及 `/search/detail/` / `/search/picDetail/`，构成新的**静态候选检索链**；12LJ 尚未执行这些路线，也未闭合参数合同。

```text
NEWS_FILTER_CONTRACT = CLOSED
NEWS_FILTER_EQ_HISTORICAL_NEWSPAPER_SEARCH = FALSE
SHARED_SEARCH_ROUTE_CANDIDATES = SOURCE_EMITTED_NOT_FOLLOWED
TARGET_QUERY = NOT_SUBMITTED
```

下一门 12LK 仅静态提取上述 shared route 周围的调用点和参数构造代码，先闭合参数合同，再决定任何后续 GET/POST 是否有证据授权。

控制证据：workflow `.github/workflows/probe-batch-12lj-cnbksy-indexed-news-navigation-contract.yml`; run/job/artifact `36880973426 / 110432320720 / 11171282570`; artifact digest `sha256:858825c80e60875936f2f2c5933d567fbb9781dc11f4b58fd9a0ef72a1a06a30`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-INDEXED-NEWS-NAVIGATION-CONTRACT-R1.json`.
