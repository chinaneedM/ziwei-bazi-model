# Fusion Chart Historical Provenance Audit R1 — Batch 12KL

## NCPSsd 首页 route-literal：正式结果路由首次直接出现

Status: **74 SEARCH-RELATED LITERALS / 12 AJAX-NAV EXPRESSIONS / 20 SOURCE-EMITTED ARTICLELIST HOT LINKS / RESULT ROUTE = /Literature/articlelist / PARAMETER NAMES search+searchname / NEW-TERM ENCODING NOT YET CLOSED / NO ROUTE FOLLOW / NO QUERY / ZERO PRODUCT IMPACT**

12KI 与 12KJ 都没有找到 Basicsearch() 的函数定义，但 12KL 改从同一首页源码枚举直接写出的 route literal，取得新的第一方事实。

当前首页仍为 HTTP 200、198,008 bytes、SHA-256 19823cf7d2d3a89bd3f86081b113f779507ebe45acb86273fd961b537b056544。源码中共有 74 条搜索相关 literal 与 12 条 AJAX/navigation expression。

最重要的是：首页直接发出 20 条热词结果链接，统一采用：

    /Literature/articlelist
    sType=0
    search=<opaque emitted value>
    searchname=<opaque emitted value>
    nav=0
    nav=0
    showBack=true

因此正式结果路由族已经不再未知：/Literature/articlelist 是第一方首页直接发出的结果页面路径，search 与 searchname 也是第一方直接发出的参数名。

但 12KL 仍不生成赵万里目标查询。原因是 search/searchname 当前只知道是页面发出的编码值，尚未把任意新词如何生成这两个参数正式闭合。

已观察到的 POST /searchHandler/getautocomplete 继续只归类为 autocomplete，不与 /Literature/articlelist 混淆。

控制证据：workflow .github/workflows/probe-batch-12kl-ncpssd-home-route-literals.yml；exact head fe36617667b396b94b32ce5498b9ea3980b367af；run/job/artifact 36861820187 / 110367617670 / 11161209833；artifact digest sha256:468ef29a508351dcb3c5c8deb2f9126a0c2099ee70fb2517d583ab1d668f39ea。

下一门 12KM：对 20 条首页原生 /Literature/articlelist 链接逐条解码 search/searchname，从解码文本取得热词，按观察出的模板重建并 Base64 编码，再与原始参数逐字节比较。只有全部 round-trip 成功，才允许后续生成新的目标查询。

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 不变。

Research record: docs/research/ZIWEI-NCPSSD-HOME-ROUTE-LITERAL-CONTRACT-R1.json.
