# Fusion Chart Historical Provenance Audit R1 — Batch 12JG

## 2011《赵万里文集》第1卷 p.197：国家图书馆“文津搜索”公开搜索契约边界

Status: **NLC HOME HTTP200 / NLC RESOURCE SEARCH HTTP200 / FIRST-PARTY WENJIN ROUTE SOURCE-EMITTED / NO HTML FORM / NO NAMED QUERY PARAM / FIND ROOT TIMEOUT / SOURCE-EMITTED ROUTE HTTP500 / NO TARGET QUERY SUBMITTED / P197 NOT REVIEWED / ZERO PRODUCT CHANGE**

### 1. 目标

12JF 后最高优先级重新回到 2011《赵万里文集》第1卷 p.197。既有路线已经确认：

- NDL 精确纸本对象存在；
- NDL 远隔复制在一般政策层可行，但登录、请求、费用属于外部动作边界；
- 国家图书馆出版社产品页、Open Library、日本机构 OPAC、Google Books 当前公开面均未给出 p.197。

12JG 检查国家图书馆自身“文津搜索”是否存在可匿名、可复现、**不猜参数**的公开检索契约。

### 2. 控制性探针

- workflow: `.github/workflows/probe-batch-12jg-nlc-wenjin-public-search-contract.yml`
- exact head: `a9f0c31c4e8cdbeb4b984ea45d7abf1ac8a8b955`
- run: `36816684951`
- job: `110223169684`
- artifact: `11141249055`
- artifact digest: `sha256:6bc3cb1978f42e452b0845edd65839ac55aa67b4e866fa19b957126885ad1ec4`

探针只执行公开 GET、解析源页面实际发出的 URL / form / field；未登录、未提交账号动作、未付费、未绕过 CAPTCHA、未猜私有接口或查询参数。

### 3. 国家图书馆主页

`https://www.nlc.cn/web/`：

- HTTP 200；
- 70,374 bytes；
- SHA-256 `7b00972aa48455db32714445aa637ee70a62a615341892aaee9fe97778e5f4d8`；
- 直接 source-emit `http://find.nlc.cn/search/doSearch`，标记为“文津搜索”；
- 页面可见搜索输入框 placeholder = “请输入您要检索信息”；
- 但没有 HTML `<form>`；
- 输入框没有可复现的 `name` 参数。

因此“文津入口身份”已经由国家图书馆第一方页面闭合，但“查询参数契约”没有闭合。

### 4. 国家图书馆资源搜索页

`https://www.nlc.cn/web/ziyuansousuo/index.shtml`：

- HTTP 200；
- 40,920 bytes；
- SHA-256 `5ee279212c918dd3340e726a98399541c05ece2ab54a67038b4cc5ae9a317e0b`；
- 同样直接 source-emit `http://find.nlc.cn/search/doSearch`；
- 同样没有 HTML form。

两处第一方页面相互复核了 route identity，但没有补出参数名。

### 5. 文津执行边界

直接访问 `https://find.nlc.cn/` 在控制性 runner 上超时。

随后只访问国家图书馆页面**自己发出的原样 URL**：

`http://find.nlc.cn/search/doSearch`

结果 HTTP 500。

这里没有拼接书名、ISBN 或任意查询参数。因为没有 source-emitted named parameter，项目不自行猜 `q`、`query`、`keyword` 等字段。

因此：

- 没有执行“赵万里文集”查询；
- 没有执行“趙萬里文集”查询；
- 没有执行 ISBN `9787501346653` 查询；
- 不能记为零命中；
- 不能推断文津数据库没有该书；
- 更不能推断 p.197 不存在。

### 6. 对 p.197 的裁决

`direct_2011_p197 = NOT_REVIEWED`

12IG 的 2026 官方期刊引文仍只是“直接引到 [2]197 的高权威桥”，不是 2011 p.197 本身。12HG 的 NDL 纸本、12IH 的复制政策、12IR/12IU/12JA 的公开访问边界均保持原裁决。

### 7. 项目影响

无排盘算法变更，无候选合并，无 transmission graph 变更，无 Matrix 计数变化：

- Matrix 198；
- audited 166；
- MISSING_FROM_PRODUCT 10；
- provenance defects 17/17 repaired；
- chart algorithm defects 0；
- reopen 0；
- candidate collapse 0。

### 8. 下一门

最高优先级继续是**合法直接恢复 2011《赵万里文集》第1卷 p.197**。文津路线只有在第一方页面/源发出资源出现明确查询字段，或 source-emitted route 恢复成可用搜索页时再进入下一步；不猜参数。

并行继续 1951《文物参考资料》第9期 pp.221–233 / `wwck195109.pdf` provenance-bound 对象，以及 1997 pp.446–449 直接页。

Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENJI-V1-NLC-WENJIN-PUBLIC-SEARCH-CONTRACT-BOUNDARY-R1.json`.
