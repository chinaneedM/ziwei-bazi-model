# Fusion Chart Historical Provenance Audit R1 — Batch 12LO

## 全国报刊索引：productTree.js 通用树导航合同与失败探针修订

Status: **SUPERSEDED VOLATILE-SEED FAILURE / REPAIRED PRODUCTTREE GET 200 / GENERIC CALLER-SUPPLIED TREE URL / ONLY FIXED PRODUCT DETAIL ROUTE / NO SEARCH DATA ENDPOINT / NO TARGET QUERY / ZERO PRODUCT IMPACT**

12LN 没有在第一方 application scripts 中找到新的自由文本检索 route，因此 12LO 转向 source-emitted `productTree.js`，检查资源/产品树是否能给出固定数据库或检索数据 endpoint。

首个 run `36886976335` / job `110452667879` 在真正读取 productTree.js 前失败：它要求实时 seed 页面再次发出“信息动态”导航，而该次动态响应没有该标签。这个失败只说明前置依赖易变，**不授权任何负面来源结论**。

修正版 run `36887246786` / job `110453592855` 在 exact head `827d83970f61851e72b4dfc927b786cd6ccd3b1c` 上改为使用前批次已 source-closed 的精确 URL，并成功得到：

- `productTree.js?version=V20241206`：HTTP 200，3913 bytes，SHA-256 `9ff4fd3fbe01987a483576c1bfc36920ed18ee0f1584db7c6dcd17181e56ce0c`；
- source-closed navigation page：HTTP 302，因此本次没有 page-level product-tree inline 初始化上下文。

脚本本体闭合为：

```text
initProductTree(url, ...) -> bksy.get(url, null, callback)
initProductTreeUnselect(url, ...) -> bksy.get(url, null, callback)
fixed route = /product/detail/{treeNode.id}
```

也就是说，产品树数据 URL 由调用方提供；脚本自身没有固定 product/resource/search 数据接口。唯一固定业务路由只是 PREPARE 叶节点打开 `/product/detail/{id}`。

所以 12LO 不再沿产品树猜 endpoint。当前更直接的 source-closed 入口，是 12LJ 完整 seed-links 已抓到的：

```text
href=/search
label=普通检索
```

下一门 12LP 直接匿名 GET 该空搜索页，不加 query string、不提交任何词，只读取真实搜索表单合同。

控制证据：修正版 workflow `.github/workflows/probe-batch-12lo-cnbksy-product-tree-navigation-contract.yml`; run/job/artifact `36887246786 / 110453592855 / 11174663900`; artifact digest `sha256:dbb3f4f6a8c6b89cc78c146fc7029663365a50a4652acaa0ba134fc1c7544481`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-PRODUCT-TREE-NAVIGATION-CONTRACT-R1.json`.
