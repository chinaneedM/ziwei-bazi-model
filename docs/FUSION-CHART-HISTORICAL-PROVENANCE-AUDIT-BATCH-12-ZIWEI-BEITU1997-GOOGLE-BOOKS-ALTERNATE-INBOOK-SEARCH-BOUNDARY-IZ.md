# Fusion Chart Historical Provenance Audit R1 — Batch 12IZ

## 1997《北京图书馆馆史资料汇编（二）》Google Books alternate：可书内检索，但 pp.446–449 不可直接页码化；分词/同词异事假阳性必须隔离

Status: **PRIMARY BZ0M0gEACAAJ EXACT IDENTITY / NO INBOOK Q CONTRACT / SOURCE-EMITTED ALTERNATE RuGEAAAAIAAJ / ALTERNATE INBOOK Q CONTRACT DIRECTLY OBSERVED / NO USABLE PP446-449 PAGE NUMBERS / NO TARGET 3482-3483 DIRECT MATCH / 瞿氏=1932 瞿兑之 FALSE POSITIVE / 赵万里=STAFF RECORD COLLISION / QUOTED-PHRASE TOKENIZATION COLLISIONS / DIRECT PP446-449 STILL NOT REVIEWED / ZERO PRODUCT CHANGE**

### 1. Scope

Batch 12GO 已闭合 1997 书目身份为《北京图书馆馆史资料汇编（二）：1949—1966》；Batch 12GN 保留 NLC 2024 对 pp.446–449 的现代学术引文桥。

12IZ 只回答一个问题：**Google Books 公开对象能不能把 pp.446–449 直接打开或可靠页码化？**

答案：**不能。**

### 2. Primary object

精确书目对象 `BZ0M0gEACAAJ`：

- 书名/ISBN/1811页身份正确；
- 显示未提供电子书；
- 当前页面没有发出可用的书内 `q=` 契约；
- source-emitted `output=html_text` 路线返回 HTTP 403；
- source-emitted other-version 指向 `RuGEAAAAIAAJ`。

因此没有猜对象 ID，也没有猜私有端点。

### 3. Source-emitted alternate

`RuGEAAAAIAAJ`：

- 保持同一 1997 / ISBN 7501314195 书目身份；
- 当前公开页面**直接发出书内 q= 搜索链接**；
- 因而对目标词执行定向检索是合法、来源自发的；
- 但结果没有给出可用的印刷页码，无法把结果直接绑定到 pp.446–449。

### 4. False-positive controls

#### `瞿氏`

Google Books 返回 1 个结果，但片段实际是 **1932 年瞿兑之寄存本馆** 的馆史记录，不是常熟瞿氏铁琴铜剑楼 1949–1953 转让事件。

结论：`SURNAME_COLLISION_FALSE_POSITIVE`。

#### `赵万里`

返回 1 个结果，但片段是“赵万里字斐云、曾任善本部主任”等人事/职员记录，不是瞿氏交易记录。

结论：`PERSON_NAME_CONTEXT_COLLISION`。

#### `这些善本入藏本馆`

返回 5 个结果，但 bounded snippet 中**没有字面完整短语**，而是“善本”“入藏”等分词后的宽匹配，且出现早期京师图书馆等无关段落。

结论：`TOKENIZED_QUERY_FALSE_POSITIVE`。

#### `可为全国之冠`

返回 1 个结果，但片段是接管某馆时“藏书的丰富、建筑的科学化、保存图籍的方法，都为全国之冠”的一般馆史表述，不是 NLC 2024 引用的瞿氏善本入藏句。

结论：`PHRASE_FRAGMENT_CONTEXT_COLLISION`。

### 5. Target searches

当前 searchable alternate 对：

- 铁琴铜剑楼 / 鐵琴銅劍樓；
- 铜壶漏箭制度 / 銅壺漏箭制度；
- 准斋心制几漏图式 / 準齋心制幾漏圖式；
- 3482 / 3483 / 03482 / 03483；

均没有直接目标片段，也没有可用页码。

但由于 Google Books snippet/index coverage 不是完整全文，**0 结果不得升级为“书中不存在”**。

### 6. pp.446–449 adjudication

仍保持：

`NLC_2024_CITATION_BRIDGE = CLOSED`

`DIRECT_PP446_449_TEXT = NOT_REVIEWED`

`DIRECT_PP446_449_IMAGES = NOT_REVIEWED`

`EXACT_INTERNAL_DOCUMENT_IDENTITY = UNRESOLVED`

`EXACT_QUOTE_PAGE_WITHIN_446_449 = UNRESOLVED`

`GOOGLE_BOOKS_PAGE_LOCATOR = UNRESOLVED_NO_USABLE_PAGE_NUMBERS`

### 7. Target-item firewall

没有直接证据把 3482/3483 或 1823 黄丕烈/士礼居合装册绑定到购买、捐赠或某一批次。

所以：

`TARGET_BATCH_MEMBERSHIP = UNRESOLVED`

`TARGET_PURCHASE_ROUTE = NOT_SELECTED`

`TARGET_DONATION_ROUTE = NOT_SELECTED`

### 8. Product / accounting

Matrix 198 / audited 166 / MISSING_FROM_PRODUCT 10; provenance defects 17/17 repaired; chart algorithm defects 0; reopen 0; candidate collapse 0.

No deterministic runtime, rule, candidate, genealogy topology or product change.

### 9. Next gate

停止重复 Google Books 搜索计数；除非公开对象开始暴露印刷页码或直接页内容，否则转回 NDL / 东京都立中央图书馆的上册实体/复制路线，或寻找权威开放的 pp.446–449 页级替代对象。

Research record: `docs/research/ZIWEI-BEITU1997-GOOGLE-BOOKS-ALTERNATE-INBOOK-SEARCH-BOUNDARY-R1.json`.
