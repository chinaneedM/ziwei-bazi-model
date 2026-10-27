# Fusion Chart Historical Provenance Audit R1 — Batch 12IY

## 冀淑英第九讲直接交易时间线：三批混合转让直接闭合，304+52 与第二批123升格，第三批数字继续封锁

Status: **CH9 DIRECT PAGE-NUMBERED SNIPPETS / THREE-BATCH MIXED SALE+DONA­TION MODEL DIRECT / FIRST BATCH 304 SOLD + 52 DONATED DIRECT P140 / SECOND BATCH 123 SOLD DIRECT P143 / DING FUBAO SIX-BOOK INTERMEDIARY DIRECT P143 / THIRD BATCH PURCHASED-BOOK CHARACTER DIRECT P155 / THIRD-BATCH DATE+97+300PLUS NOT DIRECTLY CLOSED / ITEM 3482-3483 ROUTE UNRESOLVED / ZERO PRODUCT CHANGE**

### 1. 目标

Batch 12FP 把 1950–1953 三批数字保留在“二级转述待直读第9讲”层。Batch 12IX 已取得 Google Books 对象 `k4MzlCiOPIcC` 的页码化第9讲摘录，因此本批只解决一个问题：哪些旧转述可以升格为冀淑英第9讲直接页级事实，哪些仍不能。

### 2. 控制探针

- broad chronology probe: run `36744630435`, artifact `11112046784`, digest `sha256:9838f269e2be3f0bb08c4d10ded9453d3f28454894aeb3156c9ad01bbd832b55`
- exact transaction probe: commit `c5a3fe2a82ab83005095084e540f365a9c674be6`, run `36744770186`, job `109988032476`, artifact `11112376609`, digest `sha256:b3f48dc2b565c0b56ae892eeea26a5e38cf4c5e957f2bf55c36a217d248120c2`

两次探针都只使用 Batch 12IX 已证明由页面自身发出的 Google Books `id=k4MzlCiOPIcC&q=` 书内搜索合同。

### 3. 三批结构直接闭合

p.139 的书内摘录直接说明：

- 收购分为三批；
- 每一批卖出时同时伴随一批捐赠；
- 两种形式相互搭配；
- 大部分书属于卖给北京图书馆的部分；
- 捐赠从 1950 年开始。

p.155 直接出现“第三批买的书”，p.162 又直接回顾“三批书”已大体到馆。

因此，旧 12FP 的 `MIXED_TRANSFER_PROGRAM=CLOSED` 现在得到**冀淑英第9讲直接页级支持**，不再只依赖后人转述。

### 4. 第一批：304 + 52 直接升格

p.140 对第一批直接给出：

- 卖出 304 种；
- 随之捐赠 52 种。

这两项从 12FP 的 secondary recounting 升格为：

`FIRST_BATCH_304_SOLD + 52_DONATED = DIRECT_JI_CH9_PAGE_140`

当前摘录没有直接显示“1950-01-07”这一精确日期；精确字符串 `1950年1月7日` 在当前书内搜索返回 0。因此日期仍须由同时代日记/其他直接记录控制。

### 5. 第二批：123 直接升格

p.143 直接说明“过了一段时间”后，瞿氏又卖第二批 123 种。因此：

`SECOND_BATCH_123_SOLD = DIRECT_JI_CH9_PAGE_143`

但 `1950年3月` 精确字符串当前返回 0。故“1950-03”仍不从本批取得直接日期权重。

### 6. 丁福保六种中介路径直接复核

同一 p.143 上，在第一批之后、第二批之前的叙述直接出现：赵万里在上海联系丁福保方面，丁福保选择购买六种书并以其名义捐给北京图书馆。

这把 Batch 12HC 由 2020 NLC 展览叙述建立的：

`TIEQIN ORIGIN -> DING FUBAO PURCHASE -> DING FUBAO DONATION TO NLC`

升级为**冀淑英第9讲直接页级复核**。

仍未取得六种书的完整清单，因此不得把目标 3482/3483 卷塞入该中介路径。

### 7. 第三批：存在与“买书”直接，数字/日期不直接

p.155 直接出现“第三批买的书”，所以第三批的存在以及该段的购买/收购性质可直接闭合。

但是当前精确搜索：

- `1953年3月` = 0；
- `97种` = 0；
- `捐赠97种` = 0；
- `三百多种` 未形成第9讲精确可见词组/页码绑定。

因此 12FP 中“1953-03 / donation 97 / sale 300+”**不得整体升级**，继续保持 secondary recounting pending direct ledger/full-page collation。

### 8. 与其他统计口径不合并

本批不把这些直接数字与以下现代统计强行加减：

- NLC 2023：20 种 + 收购 190 种；
- Study Times 2026：1950-03 至 1954-04 四次合计 699 种；
- NLC 2020：700 多部；
- 赵万里 1951：另一捐赠口径中的 62 种。

这些来源的事件范围、统计对象和“捐献/转让/收购”口径不同；没有直接 accession ledger 前继续禁止算术归一化。

### 9. 目标卷防火墙

本批仍未在第9讲摘录中直接看到：

- 《铜壶漏箭制度》；
- 《准斋心制几漏图式》；
- 3482 / 3483；
- 03482 / 03483；
- 1823 黄丕烈/士礼居一册合订指纹。

所以目标卷属于哪一批、是购买还是捐赠、确切入藏日仍全部 `UNRESOLVED`。

### 10. 项目影响

这是历史来源权重升级，不是排盘规则修改。Matrix / 产品会计保持：

`198 / 166 / 10 / provenance 17 of 17 repaired / chart algorithm defects 0 / reopen 0 / candidate collapse 0`

### 11. 下一门

1. 用 p.139–155 已直接闭合的交易骨架去追第9讲引用来源、北图/NLC 入藏簿、收购清单与付款记录；
2. 优先搜索目标 3482/3483 或 1823 合订卷指纹在这些直接档案中的落点；
3. 第三批 `1953-03 / 97 / 300+` 继续待直接记录，不再从二级文章升级；
4. 平行继续 2011《赵万里文集》第1卷 p.197 与 1951《文物参考资料》第9期直接页。

Research record: `docs/research/ZIWEI-JI-SHUYING-2009-TIEQIN-DIRECT-TRANSACTION-CHRONOLOGY-R1.json`.
