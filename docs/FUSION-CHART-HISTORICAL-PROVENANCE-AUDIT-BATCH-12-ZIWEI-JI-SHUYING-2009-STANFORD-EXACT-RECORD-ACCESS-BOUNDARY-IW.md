# Fusion Chart Historical Provenance Audit R1 — Batch 12IW

## 冀淑英《古籍善本十五讲》Stanford 精确记录访问边界：静态前端壳 + headless Request Rejected，不授权目录/页码负证据

Status: **STANFORD RECORD LOCATOR 8440171 / STATIC HTTP 200 FRONTEND SHELL / HEADLESS REQUEST REJECTED / NO SOURCE-EMITTED MARC-EXPORT LINK RECOVERED / CHAPTER-9 PAGE RANGE STILL UNRESOLVED / ZERO PRODUCT CHANGE**

### 1. 目标

Batch 12IJ–12IM 已建立 2009《冀淑英古籍善本十五讲》的多点页码校准，但第九讲《铁琴铜剑楼藏书的收购入藏》的精确起止页与直接正文仍未取得；第10–11讲的精确页码也仍是最高价值辅助门之一。

12IW 针对公开检索定位到的 Stanford SearchWorks record `8440171`，只测试精确记录 URL 的匿名静态 GET、同一 URL 的 headless Chrome 正常渲染，以及页面自己发出的 MARC / RIS / citation / export 等链接。不猜接口，不登录，不绕过站点拒绝页。

### 2. 控制探针

第一阶段 commit: `6037af39592024511120ac1fdd5665083a53a555`

最终控制 commit: `550b40b00008b94caa1e3b213c17f5a85f17fc74`

最终 workflow run: `36737151825`

Job: `109961739855`

Artifacts:

- static: `11107378330`, digest `sha256:9f1a960a008fe774300e527cda769d3cd5c94d1bfbac45e432cb94fa64b2d643`
- rendered: `11108240128`, digest `sha256:c4db51da277a05267695b70c30b5bde9cdc73ad614533028fa27dcf94f9b535d`

### 3. 静态 GET

精确 URL `https://searchworks.stanford.edu/view/8440171` 返回 HTTP 200，但当前 GitHub runner 得到的仅是 5101-byte 前端壳，SHA-256 `1edc8025a708c24dd3ee4ff800b250784c565e1fa47a1d1b78233b54905323c3`。页面文本未直接绑定目标书名、ISBN 或 241p；只出现 1 个 href，并没有页面自己发出的 MARC / RIS / EndNote / citation / export / JSON 内容链接。

这只能证明当前静态传输没有拿到书目正文，不能证明 Stanford 记录本身没有这些字段。

### 4. Headless 渲染

同一 URL 使用正常 headless Chrome 渲染后：

- return code = 0；
- DOM = 336 bytes；
- SHA-256 = `0510e1f4e37ae5c9432affeda5c59b75dd6be61c26beaee40f85a7ce2c0ca0ee`；
- 页面可见文本是 Stanford 的 `Request Rejected` 拒绝页；
- target title / ISBN / Chapter 9–11 / 目录 / Contents 均未进入可用 DOM；
- source-emitted href = 0。

因此这是明确的**当前执行环境访问边界**。不得使用该拒绝页把“未观察到目录/页码”升级为书目内容不存在。

### 5. 搜索索引定位与第一方内容的防火墙

公开搜索索引可定位到 SearchWorks record `8440171`，并显示该记录对应《冀淑英古籍善本十五讲》及 `[1], 241 p.`。但本批机器探针没有从 Stanford 第一方页面本身复现这些字段。

因此 `SEARCH_INDEX_LOCATOR != DIRECT_FIRST_PARTY_RECORD_CONTENT`。record ID 可继续作为 discovery locator；不能把搜索引擎摘要当作 Stanford 目录正文，也不能据此推导第九讲页码。

### 6. 项目裁决

- Chapter 9 exact page range = `UNRESOLVED`
- Chapter 9 direct text = `NOT_REVIEWED`
- Chapter 10/11 exact pagination = `UNRESOLVED`
- 不做线性/比例插值
- 不新增候选
- 不修改 198 / 166 / 10
- 不改变 17/17 provenance repair
- 不重开算法

### 7. 下一门

停止重复当前 Stanford runner 静态/Chrome 路线，除非站点响应或来源自带链接发生变化。继续寻找第九讲的页码化目录、直接扫描或权威引用；第10/11讲起始页的权威引文；2011《赵万里文集》第1卷 p.197；以及 1951年第9期的合法开放页级对象。

Research record: `docs/research/ZIWEI-JI-SHUYING-2009-STANFORD-EXACT-RECORD-ACCESS-BOUNDARY-R1.json`.
