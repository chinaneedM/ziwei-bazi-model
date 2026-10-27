# Fusion Chart Historical Provenance Audit R1 — Batch 12LN

## 全国报刊索引：第一方应用脚本 `/search...` 路由盘点

Status: **2 SEARCH LITERALS ONLY / BOTH OBJECT DETAIL / NO FREE-TEXT SEARCH ROUTE ON REVIEWED SURFACE / NO ROUTE INVOKED / NO TARGET QUERY / ZERO PRODUCT IMPACT**

12LM 已证明 `/common/hints` 可匿名执行但返回空列表。12LN 因而不继续盲试 endpoint，而是静态扫描同一公开页面的 inline scripts 与 source-emitted 第一方应用脚本。

控制 run `36886453562` / job `110450892439` 在 exact head `e25f7c19046f90661f796128f901d129201d0a62` 上成功。页面共有 39 个 source-emitted 外链脚本，其中 6 个被归为第一方应用脚本；对 inline + 这些应用脚本进行 `/search...` literal inventory 后，只得到：

- `/search/detail/`
- `/search/picDetail/`

两者都来自购物车 item：

```text
/search/detail/{item.dataId}/{item.laId}/{item.laId}
/search/picDetail/{item.dataId}/{item.laId}/{item.laId}
```

未观察到 search-named application function，也没有自由文本或列表搜索 route literal。

因此只能裁决：

```text
REVIEWED_NEWS_SURFACE_FREE_TEXT_SEARCH_ROUTE = NOT_OBSERVED
DETAIL_ROUTES = OBJECT_ID_DRIVEN
SITE_WIDE_SEARCH_ABSENCE = NOT_AUTHORIZED
```

下一门 12LO 改查 source-emitted `productTree.js` 与页面的产品树初始化代码。理由是数据库检索入口可能由产品/资源节点动态生成，而不是以 `/search...` 字面常量出现。12LO 仍只做静态 route/navigation contract，不点击产品、不发目标词。

控制证据：workflow `.github/workflows/probe-batch-12ln-cnbksy-application-search-route-inventory.yml`; run/job/artifact `36886453562 / 110450892439 / 11173764426`; artifact digest `sha256:8d7cab17e5407b61579d2bc31cfabf4761b13c5b7ee698abe2c11c7bb0d3c675`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-APPLICATION-SEARCH-ROUTE-INVENTORY-R1.json`.
