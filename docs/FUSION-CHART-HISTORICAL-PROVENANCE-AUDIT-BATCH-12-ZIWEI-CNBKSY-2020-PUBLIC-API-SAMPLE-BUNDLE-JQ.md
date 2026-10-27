# Fusion Chart Historical Provenance Audit R1 — Batch 12JQ

## 上海图书馆 2020 全国报刊索引开放 API 说明书+样例公开包边界

Status: **FIRST-PARTY 2020 PUBLIC ZIP CLOSED / TWO PDF OBJECTS BOUND BY DIGEST / PDF BODY NOT REVIEWED / NO CREDENTIAL RECORDED OR USED / CURRENT 2026 APIKEY BOUNDARY PRESERVED / NO TARGET QUERY / ZERO PRODUCT IMPACT**

### 1. 目标

12JP 已经闭合当前 2026 CNBKSY API 契约：`competitionSearch` 存活，但官方说明要求注册取得 APIKey。12JQ 检查上海图书馆 2020 开放数据目录中仍公开存在的“全国报刊索引开放数据接口（API）说明书+样例”ZIP，目的只在确认历史公开分发链，不把历史样例误当作当前授权。

### 2. 第一方公开包

控制探针直接取得：

- URL: `https://opendata.library.sh.cn/2020/download/opendata/2020/%E5%85%A8%E5%9B%BD%E6%8A%A5%E5%88%8A%E7%B4%A2%E5%BC%95.zip`
- HTTP 200
- 230,672 bytes
- SHA-256 `202429192ac1eb96193595099efb585e3221cea1d89726758f521c50f3013d79`
- ZIP entries: 3（1 directory + 2 PDFs）

runner 日志中的旧式 ZIP 文件名按可逆 CP437-byte → GBK 归一化后，对应：

1. `2020上海图书馆开放数据竞赛-全国报刊索引开放数据接口（API）使用样例.pdf`
   - 224,440 bytes
   - SHA-256 `66ddfa18bb82f1207dbe5baae1062344cecd15e6a4759745827ed1c2c324cde9`
2. `2020上海图书馆开放数据竞赛上海图书馆开放数据应用开发竞赛-全国报刊索引开放数据接口（API）说明书.pdf`
   - 186,381 bytes
   - SHA-256 `61fadcda0a8617db389f4e8fbde05025a3ebed92a7b10584157b657cceb3f301`

### 3. 控制探针

- workflow: `.github/workflows/probe-batch-12jq-cnbksy-2020-public-api-sample-bundle.yml`
- exact head: `ac81d20ebfe94d7e2775f1da66fd406beec6aa31`
- run: `36836265483`
- job: `110284300861`
- artifact: `11149681093`
- artifact digest: `sha256:de809928034c1fcf97d7d1c7265a373ffd5a1b29f3e2d3a66ee4d7cc4fbdc784`

本 probe 只检查 ZIP 结构和对象摘要。两个 PDF 的正文未审读；任何样例 key/token/credential 值均未记录、保存、使用，也没有提交赵万里、文汇报或《文物参考资料》目标查询。

### 4. 裁决

```text
FIRST_PARTY_2020_PUBLIC_SAMPLE_BUNDLE = CLOSED
PDF_OBJECT_IDENTITY = CLOSED_BY_DIGEST
PDF_BODY_CONTRACT_DETAILS = NOT_REVIEWED
HISTORICAL_PUBLIC_SAMPLE = NOT_CURRENT_AUTHORIZATION
CURRENT_2026_APIKEY_BOUNDARY = CONTROLLING
CREDENTIAL_VALUE_RECORDED_OR_USED = false
TARGET_QUERY_SUBMITTED = false
TARGET_PRESENCE_OR_ABSENCE = UNRESOLVED
DIRECT_1951_PAGE = NOT_REVIEWED
```

必须保持：公开历史样例包 != 当前 API 授权；PDF 对象身份 != PDF 正文已审；历史样例 credential（若存在）不得推断、抄录或复用；API 文档 != 1951 原报页。

### 5. 项目影响

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects 0；reopen 0；candidate collapse 0。无 runtime、产品或 transmission graph 修改。

### 6. 下一门

12JP 的当前 2026 APIKey 规则继续控制任何目标查询。若后续需要研究 API 契约的历史演变，可只审 2020 PDF 文档正文并对凭据值做屏蔽，不得复用样例凭据。直接文本最高门仍是上海《文汇报》1951-08-18、《文物参考资料》pp.221–233 与 2011《赵万里文集》第1卷 p.197。

Research record: `docs/research/ZIWEI-CNBKSY-2020-PUBLIC-API-SAMPLE-BUNDLE-R1.json`.
