# Fusion Chart Historical Provenance Audit R1 — Batch 12LS

## 全国报刊索引：“使用帮助”目录树第一方 ID 闭合

Status: **HELP TREE POST HTTP 200 / FOUR FIRST-PARTY NODE IDS CLOSED / NO SEARCH-FIELD NODE / NO FINDNEWS / NO QUERY / ZERO PRODUCT IMPACT**

控制 run `36891525616` / job `110468062390` / artifact `11176896635` 在 exact head `f5a8c7c2c6d7e3c7fe2631e91f8496fdfb5309a3` 上，按 12LR 已闭合的活动调用只执行 `POST /portal/footCategory/footerList?id=61`，payload 为空对象；同一匿名 session 的页面 `_csrf` 仅进入请求 query，未记录其值。

返回 HTTP 200 `application/json;charset=UTF-8`，195 bytes，SHA-256 `bad8c69f3448f4b0c6a534d675eca1f5cdbf40964f20ecea15794243c45e38a0`，JSON 为 4 个对象。第一方目录树精确为：`61 使用帮助 (pId=0)`；子节点 `64 包库用户常见问题`、`81 镜像用户常见问题`、`161 用户手册下载`（均 `pId=61`）。

这四个节点中没有“普通检索 / 高级检索 / 专业检索”帮助节点。因此 12LQ 页面导航中出现的检索模式标签，不能被反向绑定到 64/81/161，也不能把这些 ID 猜成检索字段说明。当前证据只闭合帮助目录身份。

12LS 没有调用任何 `findNews` 路径，没有跟随 161 或其他节点，也没有提交赵万里、文汇报或其他检索词。下一门 12LT 按页面自身活动 `init()` 的真实执行顺序，只调用 `POST /portal/footCategory/findNews?id=61` + 空对象，盘点根“使用帮助”的 JSON 标题/正文、可见文本及其 source-emitted links；链接一律不跟随。

控制证据：workflow `.github/workflows/probe-batch-12ls-cnbksy-help-tree-contract.yml`; run/job/artifact `36891525616 / 110468062390 / 11176896635`; artifact digest `sha256:716f2b808a6e4f5d5e800220f0f3ce6e975355499ffe257a55fa3cedc9279dc0`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-HELP-TREE-CONTRACT-R1.json`.
