# Fusion Chart Historical Provenance Audit R1 — Batch 12JA

## 《赵万里文集》第1卷 Google Books：精确 ISBN 页自发对象 `swWenQAACAAJ` 实为“第3卷”聚合冲突，禁止用于 p.197

Status: **EXACT ISBN HTML HTTP200 / SOURCE-EMITTED OBJECT swWenQAACAAJ / ISBN PRESENT / GOOGLE OBJECT DISPLAYS 第3卷 / NO INBOOK Q CONTRACT / NO ALTERNATE / VOLUME-1 IDENTITY REMAINS CONTROLLED BY NLCPRESS + NDL + OPENLIBRARY + JAPAN OPACS / P197 NOT REVIEWED / ZERO PRODUCT CHANGE**

### 1. What changed

Batch 12IV 只知道 Google Books ISBN HTML 表面显示“第3卷 / 526页”，与第一卷身份冲突；当时没有追它自己发出的对象链接。

12JA 从精确 ISBN 页面 `9787501346653` 重新解析 source-emitted links，直接得到真实对象：

`swWenQAACAAJ`

这是 Google 页面自己发出的 about / content / buy / export 对象 ID，不是猜测。

### 2. Object adjudication

跟随 `swWenQAACAAJ` 后：

- ISBN 9787501346653 仍出现；
- 页面显示 **第 3 卷**；
- 显示未提供电子书；
- 没有 source-emitted 书内 `q=` 搜索契约；
- 没有 source-emitted alternate object；
- 没有 p.197 或配置的瞿氏/六十二种/永乐大典等目标词直接页证。

因此这不是“找到第一卷数字对象”，而是把原来的聚合冲突升级为：

`SOURCE_EMITTED_GOOGLE_OBJECT_METADATA_CONFLICT_QUARANTINED`

### 3. Controlling volume identity

ISBN 9787501346653 的第一卷身份继续由更高质量链控制：

- 国家图书馆出版社 Product 5325：《赵万里文集·第一卷》；
- NDL：UM11-C247，504页；
- Open Library：OL30454631M，`v. <1>`；
- CiNii NCID BB08679512 + Kansai/Kyoto/NIJL 第一卷绑定。

Google 的 `swWenQAACAAJ` 不得覆盖这些独立控制。

### 4. p.197 firewall

`swWenQAACAAJ`：

- 不得作为第一卷 witness；
- 不得作为 p.197 witness；
- 不得因为 ISBN 相同就跨卷归并；
- 当前没有 q= 契约，所以不执行猜测式书内搜索。

Direct 2011 p.197 remains **NOT_REVIEWED**.

### 5. Accounting

Matrix 198 / audited 166 / MISSING_FROM_PRODUCT 10; provenance defects 17/17; chart algorithm defects 0; reopen 0; candidate collapse 0.

No product, runtime-rule, candidate or genealogy-topology change.

Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENJI-V1-GOOGLE-BOOKS-SOURCE-EMITTED-OBJECT-CONFLICT-R1.json`.
