# Fusion Chart Historical Provenance Audit R1 — Batch 12JT

## 国家图书馆 source-emitted OPAC / 电子报纸 HTTP 路由与协议校准

Status: **FIRST-PARTY SOURCE-EMITTED HTTP ROUTES CLOSED / HTTP REACHABLE / HTTPS COMPARISON TIMEOUT / ELECTRONIC-NEWSPAPER SEARCH FIELDS OBSERVED / NO FORM SUBMISSION / NO TARGET QUERY / ITEM ID UNRESOLVED / ZERO PRODUCT IMPACT**

### 1. 为什么必须做协议校准

12JS 只确认当前 NLC 页面存在馆藏目录、数字资源和光盘服务语境。12JT 直接解析当前 NLC 首页 href，发现国图实际发出的 OPAC 与电子报纸资源链接均为 HTTP，而不是 HTTPS。

因此此前把 source-emitted URL 自动升级为 HTTPS 再观察 timeout，不能直接代表原始公共路线不可达。本批把 HTTP 原路与 HTTPS 对照分开测试。

### 2. Source-emitted 路由

NLC 首页对象：HTTP 200 / 70,374 bytes / SHA-256 `7b00972aa48455db32714445aa637ee70a62a615341892aaee9fe97778e5f4d8`，解析 166 个链接。

直接发出：

- `http://opac.nlc.cn/` 及 login-session 链；
- `http://read.nlc.cn/outRes/outResList?type=电子报纸`。

### 3. HTTP / HTTPS 对照

OPAC HTTP root：200 / 318 bytes / SHA-256 `999e28e32e671494ad7a97c0a46446f192c8767264adca9d068ef0c3f4fe2a68`。该 root 响应没有表单、输入或链接。

电子报纸 HTTP：200 / 404,829 bytes / SHA-256 `b8991f6d96bb95e8fba6dff11866ece8b146ee097fa902d9afb25b0c7d7856cf`。页面暴露 `type`、`urlType`、`searchName`、`ourReswords` 字段和搜索按钮。

两条 HTTPS 对照均 ConnectTimeout。因此：SOURCE_EMITTED_HTTP_REACHABLE=true；HTTPS_COMPARISON_REACHABLE=false。不得反过来把 HTTPS timeout 外推成 NLC 公共路由整体不可达。

### 4. 目标题名边界

电子报纸 landing page 本身没有 文汇报 / 文匯報 / 文汇报60年报纸光盘 / 文汇报61年全文数据光盘 token。但这只是未执行搜索的 landing page，不具备目录阴性证据权重。

本批没有提交 `searchName` / `ourReswords`，因为尚未直接审读页面脚本如何把用户输入转换为 public query contract。

### 5. 控制记录

Controlling run `36844080482` / job `110309901228` / artifact `11152368933` / digest `sha256:dc4f1f29fe9cff4c640b6ba34a29c7e0eab3c7a7fb20f22daaab6ef5c2c334d2`。

前一 corrected run `36843786769` 只用于发现 source-emitted href；因只测试 HTTPS，不用于最终协议裁决。

### 6. 项目影响与下一门

没有登录、读者账号、注册、表单提交、目标查询、私有端点猜测或 TLS 绕过。Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects 0；reopen 0；candidate collapse 0。

下一步先恢复电子报纸页面关于 `searchName` / `ourReswords` 的客户端检索契约；只有契约明确后，才允许匿名公开目标题名检索。直接《文汇报》1951-08-18、《文物参考资料》pp.221-233、2011《赵万里文集》第1卷 p.197 仍为 NOT_REVIEWED。

Research record: `docs/research/ZIWEI-NLC-SOURCE-EMITTED-OPAC-ELECTRONIC-NEWSPAPER-HTTP-ROUTE-CALIBRATION-R1.json`.
