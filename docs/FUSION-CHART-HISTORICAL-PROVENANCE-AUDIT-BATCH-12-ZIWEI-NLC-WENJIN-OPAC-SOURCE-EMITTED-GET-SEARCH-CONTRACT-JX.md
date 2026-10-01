# Fusion Chart Historical Provenance Audit R1 — Batch 12JX

## 国家图书馆“文津搜索 / OPAC”第一方 JavaScript GET 检索合同闭合

Status: **FIRST-PARTY CLIENT SCRIPT CLOSED / WENJIN GET CONTRACT CLOSED / OPAC GET CONTRACT CLOSED / 12JG+12JW NONOBSERVATION REFINED NOT INVALIDATED / NO TARGET QUERY / ZERO PRODUCT IMPACT**

### 1. 目标

12JG 与 12JW 在当时检查的 HTML / OPAC 根页面层没有取得具名参数，因此“不猜参数”的裁决保持有效。12JX 继续沿国家图书馆页面自己发出的客户端脚本恢复可复现合同。

### 2. 第一方合同

资源搜索页 `https://www.nlc.cn/web/ziyuansousuo/index.shtml` 为 HTTP 200 / 40,920 bytes / SHA-256 `5ee279212c918dd3340e726a98399541c05ece2ab54a67038b4cc5ae9a317e0b`，并 source-emit `index.main.js?v=1212`。该脚本为 2,278 bytes / SHA-256 `89714aa2de74ff6f170bb33590b945ff3c41b3377864f0fcd6579fb51bbc575c`。

脚本 `searchFn` 直接定义两条 GET：文津使用 `query` + `actualQuery`，并固定 `searchType=2 / docType=全部 / isGroup=isGroup / targetFieldLog=全部字段 / fromHome=true`；OPAC 使用 `request` 并固定 `func=find-m / find_code=WRD / FIND_BASE=NLC01,NLC09`。参数来自 NLC 第一方 source-emitted JavaScript，不是项目猜测。

### 3. 前向修订边界

`12JG/12JW` 的旧观察不删除：它们分别证明 HTML/根页未直接暴露合同。12JX 新增此前未审读的客户端脚本层，因此把“当前公开合同”从未观察/未决推进为已闭合，而不是把旧传输事实改写。

### 4. 控制证据

- workflow: `.github/workflows/probe-batch-12jx-nlc-wenjin-client-search-contract.yml`
- head: `3062fdc5d9ae6cc9c97af7c2cfe7fe8748f54b1a`
- run/job/artifact: `36847389376 / 110320682834 / 11153204934`
- artifact digest: `sha256:5a0644d8eb6a297b32e5ccb79036593abda06597f3bed389ed81fece3d3d45a9`

本批不提交目标题名、人物或日期查询。

### 5. 项目影响与下一门

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 无变化。下一步只使用这两个第一方 GET 合同做正控与《文汇报》题名探针。

Research record: `docs/research/ZIWEI-NLC-WENJIN-OPAC-SOURCE-EMITTED-GET-SEARCH-CONTRACT-R1.json`.
