# Fusion Chart Historical Provenance Audit R1 — Batch 12LR

## 全国报刊索引：“使用帮助”动态调用点静态闭合

Status: **ACTIVE HELP POST CALLSITES SOURCE-CLOSED / LEGACY AJAX COMMENTED / NO ROUTE INVOKED / NO QUERY / ZERO PRODUCT IMPACT**

控制 run `36889506247` / job `110461242047` / artifact `11176381258` 在 exact head `7d5477c31baa20999304624191e67fa45b78479d` 上仅匿名重取第一方 `/portal/footCategory?id=61` 并做静态调用点分析；页面返回 HTTP 200、43709 bytes、SHA-256 `93ba3392726bf038e9163a51508eb67aebd097c8a52c2c93cac164db62b795ee`。

活动代码已经闭合三条 `bksy.post`：`/portal/footCategory/footerList?id=61` + `{}` 用于装载帮助树；`/portal/footCategory/findNews?id=61` + `{}` 用于初始化标题/正文；`/portal/footCategory/findNews` + `{id:treeNode.id}` 用于点击树节点后装载对应标题/正文。结合 Batch 12LL，三者继承 `POST + URL query _csrf + jQuery normal form serialization` 的传输语义。

旧 `$.ajax` 代码块整段为 line comment；其中 `/news/listTree?id=nc.id` 与重复的 `footerList?id=61` 只属于注释遗留，不能被提升为当前活动接口。特别要区分：`footerList?id=61` 同时存在一个活动 `bksy.post` 调用和一个注释中的旧 AJAX literal，不能把整个 route 误判为“已注释”。

12LR 没有执行任何候选 route，没有提交赵万里/文汇报或其他目标词，也没有登录、注册、绕过 ESA 或记录 CSRF/凭据。它只把 12LQ 的“候选 literal”升级为可复现的静态调用契约。

下一门 12LS 只执行最小活动分支：同一匿名 session 内，以页面 `_csrf` 仅用于请求 query，向 `/portal/footCategory/footerList?id=61` 发送空对象 POST，盘点返回 JSON 的树节点 ID/名称/父子结构；本门不得调用两个 `findNews` 路径。只有拿到第一方树 ID 后，才可决定后续具体帮助节点内容。

控制证据：workflow `.github/workflows/probe-batch-12lr-cnbksy-help-dynamic-callsite-contract.yml`; run/job/artifact `36889506247 / 110461242047 / 11176381258`; artifact digest `sha256:deaabd53c1c66d0bd96990a913dca6c39ecc122a6cb894ebc4af3915e2415014`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-HELP-DYNAMIC-CALLSITE-CONTRACT-R1.json`.
