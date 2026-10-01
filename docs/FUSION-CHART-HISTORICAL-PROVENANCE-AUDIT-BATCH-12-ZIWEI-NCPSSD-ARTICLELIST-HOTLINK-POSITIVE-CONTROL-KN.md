# Fusion Chart Historical Provenance Audit R1 — Batch 12KN

## NCPSsd /Literature/articlelist 首页原生热词正控：运输层成立、结果层动态化

Status: **EXACT SOURCE-EMITTED HOT LINK / HTTP200 / RESULT ROUTE TRANSPORT CLOSED / TERM NOT SERVER-RENDERED / NO ARTICLEINFO LINKS IN INITIAL HTML / SEMANTIC POSITIVE CONTROL STILL OPEN / NO TARGET QUERY / ZERO PRODUCT IMPACT**

12KM 已用 20/20 round-trip 闭合 articlelist 参数生成语法。12KN 不生成新词，而是重放首页原生“红楼梦”热词链接作为正控。

该 exact source-emitted route 返回 HTTP 200，最终 URL 仍是 /Literature/articlelist，响应 143,907 bytes，SHA-256 6c46f6861107b842d564adbf99c57baa6d80e806277638d2dc106bdc1743e905。

这证明 route transport 本身成立。但初始 HTML 中：红楼梦不可见；检索结果/搜索结果通用标记未观察到；articleinfo 详情链接为 0；仅“题名/关键词”UI 标记存在。

因此不能把 HTTP 200 壳页误判为“正控结果已显示”。当前最合理且受证据支持的解释是结果数据由二次动态请求加载，但其 API 合同尚未闭合。

下一门 12KO 只解析同一正控壳页及其 source-emitted scripts，恢复 AJAX/axios/fetch 数据端点、参数名与结果容器；不执行任何新发现的 API，也不提交赵万里目标查询。

控制证据：workflow .github/workflows/probe-batch-12kn-ncpssd-articlelist-hotlink-positive-control.yml；exact head 481207f0118d7d15f7dc157b4167f589074ac9fd；run/job/artifact 36862982889 / 110371489532 / 11162841396；artifact digest sha256:1c3d18188f7bf3445d1030cd40e97bf031ab85bac753b445cc046f5f23570e36。

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 不变。

Research record: docs/research/ZIWEI-NCPSSD-ARTICLELIST-HOTLINK-POSITIVE-CONTROL-R1.json.
