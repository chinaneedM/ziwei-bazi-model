# Fusion Chart Historical Provenance Audit R1 — Batch 12JP

## 上海图书馆 / 全国报刊索引当前开放 API 契约与 APIKey 鉴权边界

Status: **CURRENT OFFICIAL API DOC CLOSED / ENDPOINT LIVE / APIKEY REQUIRED / NO KEY USED / NO TARGET QUERY / 1951 INSIDE DECLARED DATABASE PERIOD / ZERO PRODUCT IMPACT**

### 1. 目标

12JC 当时只能看到 CNBKSY 匿名网页入口 HTTP 412，未观察到公开搜索契约。12JP 重新检查上海图书馆当前开放数据体系，回答当前是否存在官方 source-emitted API 契约，以及能否在没有合法 APIKey 时继续目标检索。

### 2. 当前官方契约

上海图书馆当前开放数据页直接提供 2026《全国报刊索引开放数据接口（API）说明书》。说明书明确给出：

```text
https://data.cnbksy.com/competitionSearch?key=[参数1]&searchContent=[参数2]
```

并明确 APIKey 来自参赛注册后发送到注册邮箱。2025 官方数据介绍同时把《中国近代报纸数字文献全库》标为 1850–1952、4000余份中英文报纸；因此 1951 落在声明时间范围内，但这不证明《文汇报》1951-08-18 已收录。

### 3. 控制探针

- workflow: `.github/workflows/probe-batch-12jp-cnbksy-current-open-api-auth-boundary.yml`
- exact head: `a8c94cb9e6d2d884f36d35c88b4749d76f08b0c2`
- run: `36835297124`
- job: `110281139580`
- artifact: `11149230659`
- digest: `sha256:ba99886b0530d83d9ae9badb267ca01510315901eff56d6f70cac99120a9bcc4`

当前 endpoint 裸请求为 HTTP 200 / JSON；按说明书示例格式但空 key 请求为 HTTP 500 / JSON。没有使用 key，没有注册、登录或发邮件，也没有提交赵万里/文汇报/文物参考资料目标词。

### 4. 裁决

```text
CURRENT_OFFICIAL_API_DOCUMENTATION = CLOSED
OFFICIAL_API_ENDPOINT = LIVE
APIKEY_REQUIRED = true
AUTHORIZED_APIKEY_AVAILABLE = false
TARGET_QUERY_SUBMITTED = false
TARGET_PRESENCE_OR_ABSENCE = UNRESOLVED
DIRECT_1951_PAGE = NOT_REVIEWED
```

必须保持：数据库年份覆盖 != 特定报纸收录；endpoint 存活 != 可无授权查询；空 key 错误 != 零结果；API 元数据命中 != 原页审读。

### 5. 项目影响

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects 0；reopen 0；candidate collapse 0。无 runtime、产品或 transmission graph 修改。

### 6. 下一门

不制造或猜测 APIKey。若未来用户明确授权并合法提供 key，再按官方 contract 检索；当前继续公开直接页级恢复上海《文汇报》1951-08-18、《文物参考资料》pp.221–233 和 2011《赵万里文集》第1卷 p.197。

Research record: `docs/research/ZIWEI-CNBKSY-CURRENT-OPEN-API-AUTH-BOUNDARY-R1.json`.
