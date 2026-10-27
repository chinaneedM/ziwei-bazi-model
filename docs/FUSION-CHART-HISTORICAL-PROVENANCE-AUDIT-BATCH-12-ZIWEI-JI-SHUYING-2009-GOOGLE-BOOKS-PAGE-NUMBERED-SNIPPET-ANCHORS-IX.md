# Fusion Chart Historical Provenance Audit R1 — Batch 12IX

## 《冀淑英古籍善本十五讲》Google Books 页码化目录与书内摘录：第9讲 133–162 直接闭合，第10/11讲起始页直接闭合

Status: **EXACT ISBN PUBLIC HTML 200 / GOOGLE BOOK ID SOURCE-EMITTED / TWO LIBRARY-DIGITIZED SURROGATE DISPLAYS / PAGE-NUMBERED IN-BOOK SEARCH ACTIVE / CH9 START P133 DIRECT / CH9 CONTENT P162 DIRECT / CH10 START P163 DIRECT / CH11 START P179 DIRECT / CH11 CONTENT P188 DIRECT / CH12 START P189 DIRECT / NO FULL EBOOK / NO RAW BOOK BODY ARCHIVED / ZERO PRODUCT CHANGE**

### 1. 目标

Batch 12IW 关闭了当前 Stanford 匿名记录路线。12IX 回到 Google Books 的精确 ISBN 页面，但只沿页面自身发出的公开对象 ID、`output=html_text` 与书内 `q=` 搜索合同推进，不猜对象 ID，不调用登录、购买或复制服务。

精确版本：

- 冀淑英《古籍善本十五讲》
- 国家图书馆出版社，2009
- ISBN `9787501340637`
- 241 页

### 2. 控制探针

Controlling commit: `3aa0d43d9c5bef848520e2a6c39605a323015a86`

Workflow run: `36743418611`

Artifacts:

- public HTML: `11111496279`, digest `sha256:15772fbd315d9cd739ffbb892c4f701d6fdbe27af18258e7ee2e7c5352b8555f`
- source-emitted follow-up: `11111771034`, digest `sha256:1162c1f03ef67fd11b9f6ab802a0655991991249d0aebba1fe41912ca710ea34`
- targeted in-book search: `11111581167`, digest `sha256:01196e9f08189e7efe5517df348a12adac93aa586f563d7cadaf32656bf190a9`

### 3. Google Books 对象与数字化来源

精确 ISBN 页面 HTTP 200，直接显示书名、作者、出版社、2009、241页和 ISBN，同时明确“未提供电子书”。

页面自身发出主对象 `k4MzlCiOPIcC`。该显示记录注明来源为加利福尼亚大学、数字化日期 2022-04-18。

页面还发出“其他版本”对象 `8vHm2Qj1JO8C`，同样绑定该 ISBN / 241页；其显示记录注明来源为伊利诺伊大学厄巴纳-尚佩恩分校、数字化日期 2025-07-16。

这些是 Google Books 当前公开聚合/数字化来源显示，不等于取得大学本地仓储对象，也不授权下载整书。

### 4. 页码化目录直接闭合

对对象 `k4MzlCiOPIcC` 使用页面自己已经发出的书内搜索 `q=` 合同后，精确章节题名与目录摘录直接给出：

- 第8讲《快雪堂分馆与杨守敬藏书》：p.119
- 第9讲《铁琴铜剑楼藏书的收购入藏》：**p.133**
- 第10讲《吴梅、朱偰、赵元方的捐赠》：**p.163**
- 第11讲《涵芬楼藏书》：**p.179**
- 第12讲《周叔弢先生与北京图书馆的深厚渊源》：**p.189**
- 第13讲《潘氏宝礼堂》：p.201
- 第14讲《刘少山等藏书家的捐赠》：p.209
- 第15讲《邢之襄、陈清华先生的捐书》：p.223
- 后记：p.239

这不是按六点锚点插值，而是 Google Books 当前对象直接返回的页码化目录文本。

### 5. 第9讲直接页内控制

书内查询进一步把第9讲正文闭合到多个打印页：

- “铁琴铜剑楼”命中 p.133 / 134 / 138；
- 瞿济苍命中 p.134 / 138 / 140；
- 瞿凤起命中 p.138 / 140 / **162**；
- 瞿旭初命中 p.134；
- “捐赠”命中 p.139，并在该页直接描述铁琴铜剑楼收购分三批、卖书同时配合捐赠；
- p.140 直接显示第一批 304 种出售并随之捐赠 52 种的叙述；
- p.162 仍直接出现瞿凤起及后续乡邦文献捐赠内容。

由于第9讲题名页为 p.133，第9讲内容在 p.162 仍直接可见，而第10讲题名页直接为 p.163，所以：

`Chapter 9 printed span = 133–162 DIRECTLY CLOSED`

这是页码与相邻章节标题共同闭合，不是线性/比例插值。

### 6. 第10、11讲分页裁决

第10讲：

- 精确题名直接起于 p.163；
- 吴梅查询直接命中 p.163 / 164 / 165；
- 朱偰直接命中 p.165；
- 赵元方直接命中 p.171；
- 第11讲直接起于 p.179。

因此第10讲**起始页 p.163 已直接闭合**；目录相邻关系把其结构区间约束为 `[163,179)`，但本批没有直读 p.178，因此不把“p.178 有第10讲正文”写成直接事实。

第11讲：

- 精确题名直接起于 p.179；
- 涵芬楼查询直接命中 p.179 / 186 / **188**；
- 第12讲目录直接起于 p.189。

因此第11讲打印跨度 **179–188** 可以直接闭合。

### 7. 证据防火墙

本批取得的是 Google Books 当前公开的**页码化摘录与目录文本**，不是整书扫描下载。因此：

- 不声称取得完整 241 页；
- 不保存或提交整书正文；
- 不把 Google Books 聚合对象等同于原始大学馆藏数字对象；
- 不把搜索未命中的词解释为书内绝对不存在；
- 不用目录相邻起始页冒充未直读页的正文证据。

### 8. 项目影响

本批显著升级了《十五讲》的现代页码证据层，但不改变确定性排盘算法、候选赢家、Matrix 行数、provenance defect 计数或 transmission topology。

当前会计仍为：

`198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 17/17 provenance repairs / 0 chart algorithm defects / 0 reopen / 0 candidate collapse`

### 9. 下一门

第9讲页码获取任务从“UNRESOLVED”升级为 **133–162 DIRECTLY CLOSED**；第10讲起始页 p.163、第11讲 179–188、第12讲 p.189 均已闭合。

后续最高价值不再重复这些章节页码搜索，而应：

1. 用已取得的第9讲直接页级摘录校勘铁琴铜剑楼 1950/1953 三批交易细节与既有现代引文链；
2. 继续直接取得 2011《赵万里文集》第1卷 p.197；
3. 继续恢复 `wwck195109.pdf` 或等价 1951 第9期开放对象并校勘 pp.221–233。

Research record: `docs/research/ZIWEI-JI-SHUYING-2009-GOOGLE-BOOKS-PAGE-NUMBERED-SNIPPET-ANCHORS-R1.json`.
