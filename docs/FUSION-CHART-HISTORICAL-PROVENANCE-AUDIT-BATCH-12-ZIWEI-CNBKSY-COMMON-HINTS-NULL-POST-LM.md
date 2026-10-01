# Fusion Chart Historical Provenance Audit R1 — Batch 12LM

## 全国报刊索引：匿名 `/common/hints` null-payload 实测

Status: **SOURCE-CLOSED POST EXECUTED / HTTP 200 JSON [] / 0 HINT ITEMS / NO TARGET TERM / NO LOGIN / ZERO PRODUCT IMPACT**

12LL 已闭合 `searchHint -> bksy.post("/common/hints", null)` 的实际 HTTP 合同。12LM 首次执行这条 application request，但严格限定为：

- 同一匿名 session；
- 页面自己发出的 CSRF；
- CSRF 只在 runner 内临时使用，不写入任何输出；
- null/empty payload；
- 不提交赵万里、文汇报或任何目标词。

控制 run `36885859818` / job `110448859960` 在 exact head `81da897ed3e448a075c2f7c39ab965838cbdf347` 上成功。

响应：

```text
HTTP = 200
Content-Type = application/json;charset=UTF-8
Server = ESA
Bytes = 2
SHA-256 = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
JSON = []
Item count = 0
```

因此：

```text
COMMON_HINTS_ROUTE = OPERATIONAL_ANONYMOUSLY
ANONYMOUS_HINT_ITEMS = 0
TARGET_LOCATOR = NOT_OBTAINED
TARGET_ABSENCE_INFERENCE = FORBIDDEN
```

空提示列表只说明该匿名上下文没有返回提示项，不能推断数据库没有文汇报、没有赵万里文章，或没有 1951-08-18 页。

下一门 12LN 转向同一公开页面 source-emitted 的第一方应用脚本，静态盘点所有 `/search...` 路由及参数构造；仍然“只发现、不执行”。

控制证据：workflow `.github/workflows/probe-batch-12lm-cnbksy-common-hints-null-post.yml`; run/job/artifact `36885859818 / 110448859960 / 11174726972`; artifact digest `sha256:daa64849ff045f2555cd696bcf23f07b62edb12e1007df87f770f5c1ae4d7aa7`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-COMMON-HINTS-NULL-POST-R1.json`.
