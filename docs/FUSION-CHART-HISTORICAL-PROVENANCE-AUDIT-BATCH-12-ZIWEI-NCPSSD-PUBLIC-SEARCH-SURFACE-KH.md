# Fusion Chart Historical Provenance Audit R1 — Batch 12KH

## NCPSsd 匿名公开搜索 UI 与执行合同边界

Status: **CN/ORG PUBLIC ROOT HTTP200 / IDENTICAL OBJECT / BASIC SEARCH CONTROL OBSERVED / BASICSEARCH() SOURCE-EMITTED / ADVANCED SEARCH CONTROLS OBSERVED / NO HTML FORM / EXECUTION ENDPOINT NOT YET CLOSED / NO QUERY / ZERO PRODUCT IMPACT**

12KG 已把国图合作认证路线关闭在 SSO 边界。12KH 改走 NCPSsd 自身公开入口，不登录、不使用合作桥。

`https://www.ncpssd.cn/` 与 `https://www.ncpssd.org/` 均返回 HTTP 200、198,008 bytes，SHA-256 都是 `19823cf7d2d3a89bd3f86081b113f779507ebe45acb86273fd961b537b056544`，当前是同一首页对象。

页面直接发出基本检索控件：`text_search`、`but_search onclick=Basicsearch()`、`hidSearchType=0`、`hidSearchValue=0`、`select_type=TS`；HTML form count = 0。

还发出 `AdvancedSearch()`、`Search_text()`、`qkSearchCondition()`、`Search_GJ()`、`waiwen_search()` 等高级检索入口。KH 抓取的外部第一方脚本主要是通用库，没有闭合 `Basicsearch()` 的实际跳转 URL/参数。

裁决：`PUBLIC_SEARCH_UI_SURFACE=CLOSED`；`EXECUTABLE_SEARCH_CONTRACT=UNRESOLVED`；`QUERY_SUBMITTED=FALSE`。不得因为有搜索框就猜 endpoint 或参数。

控制证据：workflow `.github/workflows/probe-batch-12kh-ncpssd-public-search-contract.yml`；exact head `62454c60273cadc3c266e718342f61e1ca902225`；run/job/artifact `36857797158 / 110354359450 / 11160325519`；artifact digest `sha256:a8609e084df0258ccd979fb84de5256411a3798dedfda25f7fae367010580cd1`。

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。

下一门 12KI 专门抽取首页内联 JavaScript 的 `Basicsearch/AdvancedSearch/Search_text` 等函数体，只有源码直接给出 URL 与字段映射后，才允许下一批真正提交赵万里题名查询。

Research record: `docs/research/ZIWEI-NCPSSD-PUBLIC-SEARCH-SURFACE-R1.json`.
