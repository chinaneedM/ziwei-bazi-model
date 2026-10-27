# Fusion Chart Historical Provenance Audit R1 — Batch 12KO

## NCPSsd articlelist 动态结果 API 合同定位

Status: **RESULT-SPECIFIC SCRIPT FOUND / articlelist.js SHA CLOSED / MAIN RESULT ENDPOINT SOURCE-EMITTED / REQUEST FIELD NAMES CLOSED / RESPONSE total+rows BINDINGS CLOSED / RUNTIME INITIAL VALUES STILL OPEN / API NOT EXECUTED / NO TARGET QUERY / ZERO PRODUCT IMPACT**

12KN 证明 /Literature/articlelist 返回 HTTP 200 结果壳页但不服务端渲染结果。12KO 只解析该壳页与 source-emitted scripts。

结果页新增第一方脚本 https://www.ncpssd.cn/js/web/Literature/articlelist.js，SHA-256 d5d3ea90d14a6bf0cb58ca77625e2e0f1852b7ddf565175e671d51a4e5fb0bee。

脚本直接定义 search(search,pageIndex,pageSize,order,ajaxKeys)，主结果请求发送到 /searchHandler/search。请求字段：search、pageNum、pageSize、sort、sType、ajaxKeys、customShowCondition；其中 sType=getUrlParam("sType")，customShowCondition=searchname。

返回值按 data.data 读取，total 作为总量，rows 作为结果行。searchcount() 使用同一 endpoint，但固定 pageNum=1、pageSize=1、sort=null。

同一脚本还定义详情跳转 /Literature/secure/articleinfo?params=<encryptedUrl>&pageUrl=<current URL>，params 必须来自结果行 encryptedUrl，禁止猜 item identifier。

本批没有执行任何新发现的动态 endpoint。下一门只抽取 articlelist.js 的页面初始化、URL 解码和首次 search 调用链，把 pageSize、order、ajaxKeys 与 search/searchname 运行时值闭合。

控制证据：workflow .github/workflows/probe-batch-12ko-ncpssd-articlelist-result-shell-contract.yml；exact head b28e5e9ceefe4757ba3ee67e8ec59a57ca0d1e27；run/job/artifact 36863343149 / 110372692954 / 11162327250；artifact digest sha256:48d9be125c829130465920ffd52eb382b8985cc9b19bdbcb6aa5cf9a324d4729。

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 不变。

Research record: docs/research/ZIWEI-NCPSSD-ARTICLELIST-DYNAMIC-RESULT-CONTRACT-R1.json.
