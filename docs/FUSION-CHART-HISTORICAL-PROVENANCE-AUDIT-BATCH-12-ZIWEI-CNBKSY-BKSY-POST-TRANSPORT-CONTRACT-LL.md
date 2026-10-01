# Fusion Chart Historical Provenance Audit R1 — Batch 12LL

## 全国报刊索引：`bksy.post` 传输合同闭合

Status: **BKSY.POST TRANSPORT CLOSED / CSRF QUERY BINDING / POST + PARAMS / JSON RESPONSE / JSONPOST FIREWALLED / NO APPLICATION POST YET / NO TARGET QUERY / ZERO PRODUCT IMPACT**

12LK 已闭合 `searchHint(fields, hideclass) -> bksy.post("/common/hints", null, callback)`，但仍不知道 `bksy.post` 如何落到 HTTP。12LL 只读取同一公开页面 source-emitted scripts，不执行任何 application endpoint。

控制 run `36885241710` / job `110446759625` 在 exact head `71d4ecd07a8051b2220db46af9ec754f0e274793` 上成功。页面 source-emits 39 个外链脚本；其中：

`/public/common/js/common.js?version=V20241206`

直接定义：

- `bksy.post(url, params, callback, type, async, processData, unmask)`
- 将页面 `meta[name="_csrf"]` 的值追加到 URL query 的 `_csrf`；
- `type: "POST"`；
- `data: params`；
- `processData` 默认 true；
- `dataType` 默认 `json`；
- `async` 默认 true；
- **没有显式设置 contentType**。

同文件的 `bksy.jsonPost` 则是另一套 transport：

- POST；
- `contentType: application/json`；
- `data: JSON.stringify(params)`。

因此严禁把 `jsonPost` 行为套到 `searchHint` 上。

与 12LK 合并后，`/common/hints` 的应用调用合同已闭合到：

```text
METHOD = POST
URL = /common/hints?_csrf=<page-meta-token>
PARAMS = null
RESPONSE = json
TARGET_TERM = none
```

其中 CSRF 是匿名页面/session 的临时传输材料，后续若执行请求只能在 runner 内使用，**不得写入日志、artifact 或仓库**。

下一门 12LM 获准执行这一条、且仅这一条匿名 null-payload `/common/hints` POST；不发送赵万里、文汇报或任何目标关键词。

控制证据：workflow `.github/workflows/probe-batch-12ll-cnbksy-bksy-post-transport-contract.yml`; run/job/artifact `36885241710 / 110446759625 / 11174411314`; artifact digest `sha256:21c94d6f348874bf97c2c41650759a26ed51e0d9430b39048cf27be68358ec22`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-BKSY-POST-TRANSPORT-CONTRACT-R1.json`.
