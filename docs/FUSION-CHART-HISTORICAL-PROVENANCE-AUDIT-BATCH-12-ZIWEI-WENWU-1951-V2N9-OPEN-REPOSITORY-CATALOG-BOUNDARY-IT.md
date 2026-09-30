# Fusion Chart Historical Provenance Audit R1 — Batch 12IT

## 《文物参考资料》1951年第9期开放仓储检索边界：IA / Open Library / Wikimedia 零命中；Google / Hathi 未裁决

Status: **INTERNET ARCHIVE EXACT TITLE/YEAR=0 / EXACT FILENAME=0 / EXACT ARTICLE=0 / OPEN LIBRARY=0 / COMMONS=0 / WIKISOURCE=0 / GOOGLE BOOKS 429 UNRESOLVED / HATHITRUST 403 UNRESOLVED / WWCK195109 BYTES NOT RECOVERED / ZERO PRODUCT CHANGE**

### 1. 目标

Batch 12IS 已关闭当前 NDL Digital provider 路线。12IT 把同一个目标移到主流公开数字仓储目录，只找可验证的开放对象 ID，不调用商业下载。

目标仍为：

- 《文物参考资料》1951年第9期
- 文件名定位 `wwck195109.pdf`
- 赵万里《永乐大典展览的意义——一九五一年八月北京图书馆举办》
- pp.221–233

### 2. Internet Archive

Advanced Search 三个独立查询均 HTTP 200：

- 精确刊名 + 1951：0
- 精确文件名 `wwck195109.pdf`：0
- 精确文章名：0

这里只能关闭当前 IA 元数据检索面，不能证明 IA 永远没有未索引对象。

### 3. Open Library / Wikimedia

- Open Library：刊名 + 1951，HTTP 200，0
- Wikimedia Commons 文件命名空间：文件名或刊名，HTTP 200，0
- 中文维基文库：文章名或刊名，HTTP 200，0

同样只具当前检索路由的负证据，不外推全球不存在。

### 4. 两条未裁决路线

Google Books 返回 HTTP 429，明确为查询配额耗尽；因此**不得记为零命中**。

HathiTrust 测试的公开 catalog export 路线返回 HTTP 403；因此**不得记为零命中**，也不得绕过访问控制。

### 5. 对 wwck195109.pdf 的裁决

当前仍只有商业 manifest 层面的文件名与 9.73 MB 显示值。没有：

- 开放对象 ID
- 合法公开下载来源
- PDF 字节
- SHA-256
- 页数
- 扫描来源/完整性证明

所以 `wwck195109.pdf` 继续只是 discovery locator，不是正文证据。

### 6. 项目状态

Matrix 198 / audited 166 / MISSING_FROM_PRODUCT 10 / provenance defects 17/17 repaired / chart algorithm defects 0 / reopen 0 / candidate collapse 0。产品与 transmission graph 均不变。

### 7. 下一门

停止重复同一 IA/Open Library/Wikimedia 查询；Google Books 与 HathiTrust 仅在正常公开路由可用时重试。优先继续机构开放对象、2011《赵万里文集》p.197，以及冀淑英第九讲/第10–11讲直接页码证据。

Research record: `docs/research/ZIWEI-WENWU-1951-V2N9-OPEN-REPOSITORY-CATALOG-BOUNDARY-R1.json`.
