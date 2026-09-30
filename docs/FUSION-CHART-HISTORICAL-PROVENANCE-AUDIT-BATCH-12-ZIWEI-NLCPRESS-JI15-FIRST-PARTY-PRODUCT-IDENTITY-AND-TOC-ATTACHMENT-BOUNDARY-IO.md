# Fusion Chart Historical Provenance Audit R1 — Batch 12IO

## 国家图书馆出版社第一方产品身份恢复：Product 4660 闭合；目录附件与第九讲页码仍未解析

Status: **FIRST-PARTY PUBLISHER PRODUCT IDENTITY CLOSED / SOURCE-EMITTED PRODUCT ID 4660 / ISBN + AUTHOR + DATE CLOSED / CATALOG ATTACHMENT URL UNRESOLVED / RID=2 TARGET NONLISTING IS ROUTE-SCOPED ONLY / CHAPTER 9 PAGINATION UNRESOLVED / NO INTERPOLATION / ZERO PRODUCT CHANGE**

### 1. 第一方 ProductList 契约与目标定位

国家图书馆出版社公开 `ProductList.aspx` 的 ASP.NET 翻页契约已经用页面自身的 `PageNavigator1$LinkButton_Go` / `PageNavigator1$txt_PageGo` 正控校准。600 页列表的远距页码跳转均精确返回请求页；随后按出版年月逐级缩窄，不猜测商品 ID。

2009-07 窗口最终落在第 361 页。该页源码直接给出：

- `ProductView.aspx?Id=4660`
- 《冀淑英古籍善本十五讲》
- 作者冀淑英

因此 `4660` 是出版社 source-emitted 产品标识，不是枚举推测。

### 2. Product 4660 第一方书目身份

出版社产品页 `https://www.nlcpress.com/ProductView.aspx?Id=4660` 返回 HTTP 200，并直接闭合：

- 书名：《冀淑英古籍善本十五讲》
- 责任说明：冀淑英著、李文洁插图
- ISBN：`978-7-5013-4063-7`
- 出版日期：`2009-07-29`
- 版次：`B1`
- 印刷日期：`2009-07-01`
- 印次：`Y1`
- 定价：48.00 元
- 中图分类：`G256.22`

产品介绍把该书说明为根据冀淑英在国家图书馆的讲座整理、全书十五讲，并明确提到铁琴铜剑楼等藏书体系。这个介绍可以作为**现代第一方书目/内容概述**，但不是第九讲页码或正文的直接页证。

### 3. “目录附件下载”语义校准

同一产品页“相关下载”区实际 HTML 为两种不同状态：

- `Booktext`：`javascript:__doPostBack('Booktext','')`，标注“图书文件下载（TXT）”；
- `CatalogPrecisFile`：仅渲染 `<a id="CatalogPrecisFile">目录附件下载</a>`，没有 `href`。

进一步源码审计没有发现 `CatalogPrecisFile` 的脚本赋值，也没有匹配的隐藏附件字段。因此“目录附件下载”只能保留为**字面通用标签/占位观察**，不能提升为 product 4660 已存在可取目录附件对象的证据。

本批次没有触发 `Booktext`，没有取得整书 TXT。

### 4. 出版社公共资源中心反向核对

第一方 `DownLoadList.aspx?Rid=2`（“目录及部分内容页”）当前为 1 页、1 条记录，唯一项目是《〈中国图书馆馆史〉（全四册）综合索引》（`DownloadView.aspx?RId=87`）。目标书名、作者和 ISBN 均未列出。

该结果只证明**当前公开 Rid=2 路线没有列出目标**；它不证明产品本地附件不存在，也不证明历史上从未提供过目录文件。

### 5. 第九讲页码裁决

第九讲标题《铁琴铜剑楼藏书的收购入藏》继续保持既有结构身份，但：

- 精确页码：`UNRESOLVED`
- 直接第九讲正文：`NOT_REVIEWED`
- 第 10 / 11 讲精确页码：`UNRESOLVED`
- 线性插值、比例插值、借邻近锚点倒推：全部禁止

此前六点分页校准不因本批次第一方产品身份闭合而获得额外插值权。

### 6. 安全与证据防火墙

本批次没有登录、购买、付费、验证码绕过、TLS 绕过、猜测产品 ID，也没有调用整书 TXT 或公共资源下载按钮。Product 4660 的第一方身份闭合，不能外推为第九讲页证。

FID070 / 1951 引文对象防火墙保持不变：宋刻《春秋左传注疏》不得与 FID070“元刻元印十行本”折叠；确切瞿氏捐赠批次/日期及 `3368→3288` 因果机制仍未解析。

### 7. 项目影响

- Matrix：198 行
- audited：166 行
- MISSING_FROM_PRODUCT：10
- provenance metadata defects：17 / 17 repaired
- chart algorithm defects：0
- algorithm reopen：0
- candidate collapse：0
- transmission graph：`NONE`
- runtime / product change：无

### 8. 下一门

不再重复无 `href` 的 `CatalogPrecisFile` 或当前 Rid=2 非列出路线，除非出版社源码后续直接给出附件 URL/对象。最高优先级继续：

1. 第九讲直接页/带页码目录，以及第 10 / 11 讲精确分页；
2. 2011《赵万里文集》第1卷 p.197 的合法公开直页/预览；
3. `wwck195109.pdf` 的权威/开放对象恢复，先绑定字节、哈希与分页，再校勘 1951 pp.221–233。

Research record: `docs/research/ZIWEI-NLCPRESS-JI15-FIRST-PARTY-PRODUCT-IDENTITY-AND-TOC-ATTACHMENT-BOUNDARY-R1.json`.
