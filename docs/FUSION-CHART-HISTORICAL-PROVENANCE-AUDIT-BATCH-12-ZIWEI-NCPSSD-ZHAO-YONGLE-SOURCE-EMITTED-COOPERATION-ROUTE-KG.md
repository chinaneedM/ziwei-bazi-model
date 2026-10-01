# Fusion Chart Historical Provenance Audit R1 — Batch 12KG

## NCPSsd source-emitted CooperationUser 路由：匿名 SSO / 账号边界

Status: **NLC SOURCE-EMITTED URI FOLLOWED / HTTP→HTTPS REDIRECT CLOSED / FINAL HTTP200 / COOPERATION AUTH BRIDGE / NO ARTICLE METADATA / NO PDF OR FULLTEXT URL / NLC SSO ROUTES PRESENT / NO LOGIN / NO FORM SUBMISSION / DIRECT 1951 PAGES NOT REVIEWED / ZERO PRODUCT IMPACT**

12KF 的国家图书馆文津详情页直接发出一个 NCPSsd `CooperationUser.aspx` URI。12KG 只跟随该原样 URI 及服务器真实重定向，不解码后另行请求内部 articleinfo，不猜 provider identifier。

原始 HTTP URI 返回 302，唯一重定向到同一路径 HTTPS 版本；最终 HTTP 200 / 15,630 bytes / SHA-256 `8566a299bdf36b03fcdc19990be8c361eaa852d4bd9ca157dd4d3e291333c390`。

最终页面是国家图书馆与国家哲学社会科学文献中心之间的合作认证桥：源码包含 NLC SSO ticket/login 路由和“没有权限访问当前资源 / 用户账号不存在 / 没有可访问的资源列表 / 令牌不能空 / 令牌不存在”等状态处理，但没有赵万里题名/作者元数据、文章详情、PDF、全文或下载 URL。

页面模板存在看似用户名/初始密码的示例文本。项目把它严格视作页面模板内容，不当作授权凭据，不登录、不提交表单、不访问 SSO ticket/login。

因此裁决为：

```text
NCPSSD_COOPERATION_ROUTE = ANONYMOUS_SSO_ACCOUNT_BOUNDARY
ARTICLE_PAGE_REACHED = FALSE
DIRECT_1951_TEXT = NOT_REVIEWED
```

控制证据：
- workflow: `.github/workflows/probe-batch-12kg-ncpssd-zhao-yongle-source-emitted-route.yml`
- exact head: `ace6538dcca178aa8919463ad2f76ceef3f8d766`
- run / job / artifact: `36857003478 / 110351771726 / 11158129541`
- artifact digest: `sha256:50cf88454dcd9465914e99f36354bb315e88e0d5f3100b6a8f8946ecc8e112b5`

Matrix 继续 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 不变。

下一门 12KH 转向 NCPSsd 自身公开首页/公开搜索面，只解析第一方 form、字段和脚本，不提交查询；先恢复匿名搜索合同，再决定是否可合法执行题名检索。

Research record: `docs/research/ZIWEI-NCPSSD-ZHAO-YONGLE-SOURCE-EMITTED-COOPERATION-ROUTE-R1.json`.
