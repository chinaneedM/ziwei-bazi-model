# Fusion Chart Historical Provenance Audit R1 — Batch 12IR

## 《赵万里文集·第一卷》第一方产品与公开预览边界：Product 5325 闭合，p.197 仍未直接取得

Status: **NLCPRESS PRODUCT 5325 SOURCE-EMITTED / ISBN 9787501346653 CLOSED / BOOKTEXT 464 BYTES NOT P197 / CATALOG HREF ABSENT / RID3 TARGET NONLISTING / OPENLIBRARY EXACT EDITION CLOSED / OCAID NULL / GOOGLE BOOKS RATE-LIMITED / IA EXACT ISBN ZERO / DIRECT 2011 P197 NOT REVIEWED / ZERO PRODUCT CHANGE**

### 1. 第一方产品定位

国家图书馆出版社公开 ProductList 按页面自身 ASP.NET 翻页契约继续检索，不猜商品 ID。第 315 页直接发出：

- `ProductView.aspx?Id=5325`
- 《赵万里文集·第一卷》

Product 5325 返回 HTTP 200，页面直接正控目标系列、第一卷标记和 ISBN `9787501346653`。因此 5325 是 source-emitted 产品身份，不是枚举得到的候选。

### 2. Product 5325 Booktext 与目录附件

产品页源码直接给出 `Booktext` postback：

`javascript:__doPostBack('Booktext','')`

同时 `CatalogPrecisFile` 继续只有元素身份，没有 `href`。

公开 Booktext POST 返回：

- HTTP 200
- `application/octet-stream`
- Content-Length 464
- 实际读取 464 bytes
- SHA-256 `6cc2f2aecebdbb31294bad9149075dba0aa0aa2bb2a9e778474fb44e9b43529e`
- GB18030
- 规范化后 245 字符

由于服务器声明长度小于 4 KiB，本批次只在硬上限内完成载荷分类，原始文本不写日志、不保存。分类结果：

- p.197 字面页码：无
- 《永乐大典》+“展览/展覽”目标组合：无
- “瞿 / 捐 / 六十二”捐赠目标组合：无

因此当前 Booktext 是小型产品文本对象，不是 p.197 直页，也不能替代 2011 实体页校勘。

### 3. 出版社电子书资源中心 Rid=3

Product 5325 页面还发出通用“电子书下载”入口 `DownLoadList.aspx?Rid=3`。当前公开资源中心：

- HTTP 200
- 1 页
- 目标书名：未列出
- ISBN：未列出
- `DownloadView.aspx` 对象数：0

这只关闭**当前 Rid=3 路线**；不证明历史上从未存在电子书或其他产品级对象。

### 4. Open Library 独立书目控制

Open Library 精确 ISBN 路线把 `9787501346653` 绑定到：

- edition `/books/OL30454631M`
- work `/works/OL22369963W`
- title `Zhao Wanli wen ji`
- pagination `v. <1>`
- 2011
- publisher `Guo jia tu shu guan chu ban she`
- edition `Di 1 ban`
- OCLC `775628715`
- LCCN `2011426732`

当前唯一 edition 的 `ocaid=null`、covers=null；没有观察到 Open Library 绑定的 Internet Archive 扫描/预览对象。该结论仍是当前 Open Library 对象状态，不是全球无数字副本声明。

Internet Archive 精确 ISBN 检索当前为 0；Google Books ISBN/title API 当前均 HTTP 429 `rateLimitExceeded`，后者没有任何“无书”证据价值。

### 5. p.197 裁决

直接 2011 p.197：`NOT_REVIEWED`。

已有证据层保持分离：

- Batch 12IG：浙江图书馆官方 2026 PDF 已直接闭合“引用到《赵万里文集：第一卷》p.197”的现代引文桥；
- Batch 12HG：NDL 精确纸本馆藏 UM11-C247 / NDLBibID 023434359 已闭合；
- Batch 12IH：NDL 远程复制是可行但需要账户/身份/费用的外部动作，必须显式授权。

本批次没有把出版社简介、Open Library MARC 或现代引文桥提升为 2011 p.197 本身。

### 6. 安全与证据防火墙

本批次没有登录、购买、付款、复制申请、身份传输、验证码/TLS 绕过，也没有猜测 Product ID。Booktext 仅因服务器声明 464 bytes 才在 4 KiB 上限内读取并分类；载荷原文不保存、不输出。

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

1. 当前 Product 5325 Booktext / CatalogPrecisFile / Rid=3 / Open Library 路线若对象状态不变化，不再重复。
2. 继续合法公开/机构直页发现 2011《赵万里文集》第1卷 p.197；NDL 付费复制仍需显式授权。
3. 继续 `wwck195109.pdf` 权威/开放对象恢复并先绑定字节、哈希、分页。
4. 只在新表面出现时继续冀淑英第九讲 / 第10-11讲页码恢复。

Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENJI-V1-NLCPRESS-OPENLIBRARY-PUBLIC-PREVIEW-BOUNDARY-R1.json`.
