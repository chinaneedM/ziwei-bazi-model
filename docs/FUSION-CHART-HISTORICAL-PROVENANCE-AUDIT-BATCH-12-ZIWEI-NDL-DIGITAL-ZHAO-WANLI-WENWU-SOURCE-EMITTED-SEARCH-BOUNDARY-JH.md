# Fusion Chart Historical Provenance Audit R1 — Batch 12JH

## NDL Digital Collection 第一方 source-emitted 搜索契约与静态结果层边界

Status: **OFFICIAL NDL CONTRACT CLOSED / POSITIVE CONTROL HTTP200 / ALL TARGETS HTTP200 / IDENTICAL 4,298-BYTE SPA SHELL / NO QUERY ECHO / NO RESULT COUNT / NO PID / NO SOURCE-EMITTED SCRIPT SRC / ZERO-RESULT AUTHORITY FORBIDDEN / P197 AND 1951 PAGES NOT REVIEWED**

### 1. 目标

12JG 后最高门仍是 2011《赵万里文集》第1卷 p.197；1951《文物参考资料》第9期 pp.221–233 是并行的更早原始文本层。12JH 检查国立国会图书馆 Digital Collection 是否存在第一方、匿名、可复现且不猜参数的搜索结果面。

### 2. 第一方搜索契约

NDL Reference Cooperative Database 官方页面 HTTP 200，并直接 source-emit `https://dl.ndl.go.jp/search/searchResult`，同时给出 `keywordFulltext`、`keyword`、`fulltext`、`materialTypeList` 等完整参数结构。搜索端点和参数名均非项目猜测。

### 3. 控制性探针

- workflow: `.github/workflows/probe-batch-12jh-ndl-digital-source-emitted-search.yml`
- exact head: `fb318d03892d5edb39815ade41988cc508bd2327`
- run: `36819382858`
- job: `110231432661`
- artifact: `11142424009`
- artifact digest: `sha256:26e3cd1c25d2a755d753feda03b6faef8c5c49c18f92975b5b4a47504d9bb1bc`

正控 `蒋介石` 与七个目标查询（《文物参考资料》两种字形、文章题名简繁、《赵万里文集》简繁、ISBN 9787501346653）全部 HTTP 200。

### 4. 校准失败而非零命中

八个查询全部返回完全相同的 4,298-byte HTML，SHA-256 均为 `9464957293e820db57d597624e2797b50402f0c3434d62d6de9d656f7a187b4f`。静态可见文本仅是 NDL Digital Collection 服务说明；没有 query echo、结果数、PID，也没有可跟随的 source-emitted external script src。

因此即使目标查询已经按官方参数契约执行，也没有一个经过正控校准的“结果面”。不得把当前静态 SPA 外壳解释成 0 results。

### 5. 裁决

- NDL Digital 第一方搜索 URL：CLOSED
- source-emitted 参数契约：CLOSED
- 匿名静态结果面：UNCALIBRATED_STATIC_SPA_SHELL
- 目标查询执行：YES
- 目标零结果：NOT ESTABLISHED
- 目标 absence：NOT ESTABLISHED
- PID / digital object：NOT RECOVERED
- direct 2011 p.197：NOT_REVIEWED
- direct 1951 pp.221–233：NOT_REVIEWED

### 6. 证据防火墙

HTTP 200 只说明静态壳成功返回；正控与目标完全相同，反而证明当前层不能承担结果裁决。没有 PID 就没有 source-emitted 对象可继续跟随；项目不猜内部 API。以后即使恢复书目/对象命中，也必须再审读页级内容后才能升级为直接文本证据。

### 7. 项目影响

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；chart algorithm defects 0；reopen 0；candidate collapse 0。无 runtime、transmission graph 或产品状态变化。

### 8. 下一门

继续新的合法 p.197 页级路线；并行继续 1951 pp.221–233 与 1997 pp.446–449。NDL Digital 当前静态壳不重复，除非其公开响应开始发出结果 payload、PID 或 source-emitted 数据/脚本契约。

Research record: `docs/research/ZIWEI-NDL-DIGITAL-ZHAO-WANLI-WENWU-SOURCE-EMITTED-SEARCH-BOUNDARY-R1.json`.
