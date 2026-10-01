# Fusion Chart Historical Provenance Audit R1 — Batch 12KX

## NCPSsd secure-detail 隐藏字段合同：详情请求参数完全闭合

Status: **11 SOURCE-EMITTED CONTROLS / id=1002462903 / type=journalArticle / typename=中文期刊文章 / pageType=1 / NOT BASE64 / DETAIL-DATA POST NOT EXECUTED / ZERO PRODUCT IMPACT**

12KW 已从安全详情壳直接发出的 `articleinfo.js` 恢复中文期刊详情 API，但尚缺服务端实际填入的隐藏字段。12KX 只重放既已闭合的赵万里结果查询和 source-derived secure-detail GET，然后读取脚本明确引用的 hidden controls；不调用详情数据 API。

安全详情壳直接发出：

```text
ftl_urlId       = 1002462903
ftl_urlType     = journalArticle
ftl_urlTypename = 中文期刊文章
ftl_urlPagetype = ""
ftl_urlNav      = 1
```

另外 `ftl_urlSynUpdateType / ftl_urlBarcodenum / ftl_urlyulan / prpYears / prpNum` 均为空，`qkCoverImageHost=https://ft.ncpssd.cn/image/get/qwcover`。

`id/type/typename` 三项都不是 Base64，因此 `articleinfo.js` 的“三项同时 Base64 才解码”分支不触发；值保持原样。由于 `ftl_urlPagetype=""`，客户端表达式将 `pageType` 解析为 `1`。

由 12KW + 12KX 共同闭合的下一请求只有：

```json
{"lngid":"1002462903","type":"中文期刊文章","pageType":1}
```

目标 endpoint 为 `POST /articleinfoHandler/getjournalarticletable`，content type 为 `application/json; charset=utf-8`。12KX 本身没有执行该 POST，也没有登录、阅读或下载。

控制证据：workflow `.github/workflows/probe-batch-12kx-ncpssd-secure-shell-hidden-contract.yml`; exact head `166f672a0366dce8eef8f9c49a8c586d8918fed6`; run/job/artifact `36867694113 / 110387236499 / 11163794065`; artifact digest `sha256:094d43a117ad9f7c13e7b51a09029e6f908a737535dbf6d50a98e8ec77b9542b`。

下一门 12KY：只发送上述已闭合 JSON 请求，盘点第一方详情返回的书目信息与是否仅“发出” pdf/read 元数据；禁止跟随任何全文、阅读、下载、登录、收藏或用户接口。

Matrix 继续 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 不变。

Research record: `docs/research/ZIWEI-NCPSSD-SECURE-SHELL-HIDDEN-CONTRACT-R1.json`.
