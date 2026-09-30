# Fusion Chart Historical Provenance Audit R1 — Batch 12IP

## 国家图书馆出版社 Product 4660 Booktext 第一方附件闭合：739 字节载荷不是可用十五讲目录/正文

Status: **FIRST-PARTY BOOKTEXT RESPONSE CLOSED / HTTP 200 ATTACHMENT / 739 BYTES / GB18030 382 NORMALIZED CHARACTERS / TARGET TITLE + CATALOG MARKER PRESENT / CH9-CH12-CH15 EXACT TITLES ABSENT / CHAPTER PAGINATION UNRESOLVED / RAW TEXT NOT LOGGED OR SAVED / ZERO PRODUCT CHANGE**

### 1. 为什么重新检查 Booktext

Batch 12IO 已经闭合国家图书馆出版社 Product 4660 的第一方产品身份，并确认页面存在 source-emitted `Booktext` ASP.NET postback；12IO 当时刻意不触发它，因此该入口究竟返回整书、目录、简介还是占位对象仍未判定。

本批次只解决这个访问对象边界，不把现代出版社下载表面提升为历史文本权威。

### 2. 先做零正文读取的响应元数据探测

修复工作流自身的 Python 引号错误后，metadata-only probe 在不读取 POST 响应体、不跟随重定向的条件下得到：

- HTTP：`200 OK`
- Content-Type：`application/octet-stream`
- Content-Length：`739`
- Content-Disposition：修复响应头编码后指向 `冀淑英古籍善本十五讲.txt`
- redirect：否
- response body read：否
- download bytes read：0

这一步直接证明当前公开 `Booktext` postback 会发出一个附件响应，但 739 字节的声明长度已经明显不足以支持“当前返回完整 241 页书稿”的推定。

### 3. 4 KiB 上限内的完整小载荷分类

由于服务器声明对象只有 739 字节，后续 probe 设置硬上限 `4096` 字节；只有声明长度不超过上限才读取。实际完整读取：

- bytes：739
- SHA-256：`c79284ab5f39ed7b8b48e8b1071b008990c583314455c7abf00699cd1fe4d1d3`
- encoding：GB18030
- normalized chars：382
- 原始文本写入日志：否
- 原始文本保存到 artifact：否

模式分类结果：

- 目标书名：有
- “目录”标记：有
- “第九讲/第9讲”标记：无
- 第九讲《铁琴铜剑楼藏书的收购入藏》：无
- 第十讲《吴梅、朱偰、赵元方的捐赠》：无
- 第十一讲《涵芬楼藏书》：无
- 第十二讲《周叔弢先生与北京图书馆的深厚渊源》：无
- 第十五讲《国家图书馆藏〈永乐大典〉概述》：无

因此，本批次只授权一个**当前载荷作用域**结论：Product 4660 的公开 Booktext 返回的是一个很小的书目/简介式 TXT 对象，不是可用于解析十五讲章节边界的正文或带页码目录。不能把“目录”一词本身解释成完整目录存在。

### 4. 分页与正文裁决

本批次没有取得新的页码锚点：

- Chapter 9 exact page range：`UNRESOLVED`
- Chapter 9 direct text：`NOT_REVIEWED`
- Chapter 10/11 exact pagination：`UNRESOLVED`
- 六点既有分页锚点继续禁止线性、比例或邻近插值

当前 Booktext 路线在 payload hash / length / response contract 不变化时不再重复。

### 5. 证据、安全与版权防火墙

- 不登录
- 不购买、不付费
- 不绕过验证码、权限或 TLS
- 不猜 Product ID
- metadata-only 阶段不读取响应体
- 小载荷阶段以 4 KiB 为硬上限
- 不在日志或仓库保存载荷原文
- 不把现代出版社访问对象提升为古籍/历史规则权威

FID070 / 1951 对象防火墙不变：宋刻引文对象不得折叠为已经物理裁决为元刻元印十行本的 FID070；确切瞿氏捐赠批次/日期及 `3368→3288` 因果机制仍未解析。

### 6. 项目影响

- Matrix：198 行
- audited：166 行
- MISSING_FROM_PRODUCT：10
- provenance metadata defects：17 / 17 repaired
- chart algorithm defects：0
- algorithm reopen：0
- candidate collapse：0
- transmission graph：`NONE`
- runtime / product change：无

### 7. 下一门

1. 继续寻找第九讲直接页/带页码目录，或第 10 / 11 讲精确分页；Booktext 当前 hash/长度不变则停止重复。
2. 继续 2011《赵万里文集》第1卷 p.197 的合法公开直页/预览。
3. 继续 `wwck195109.pdf` 的权威/开放对象恢复，先绑定字节、哈希与分页，再校勘 1951 pp.221–233。

Research record: `docs/research/ZIWEI-NLCPRESS-JI15-FIRST-PARTY-BOOKTEXT-BOUNDED-PAYLOAD-BOUNDARY-R1.json`.
