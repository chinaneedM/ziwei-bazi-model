# Fusion Chart Historical Provenance Audit R1 — Batch 12ID

## 《国学季刊》第十一期 ISBN 前向纠正：修复 12IC 的多条目页面相邻记录误绑定

Status: **PROV-DEFECT-017 CONFIRMED / ISSUE 11 = ISBN 9787209115001 / 2018-09 / 222 PAGES / ISSUE 12 = ISBN 9787209115018 / 2018-12 / 277 PAGES / NOPSS ISSUE-11 SEPTEMBER CONTROL CORROBORATED / 12IC FULLTEXT BOUNDARY PRESERVED / ZERO PRODUCT CHANGE**

## 1. Defect

Batch 12IC 对孔夫子店铺多商品列表页采用了页面级 needle co-occurrence。页面同时包含第十一期与相邻第十二期，因此错误地把第十二期的 `ISBN 9787209115018 / 2018-12` 归给了第十一期。

该问题属于项目研究元数据错误，而不是历史来源本身的错误：

`PROV-DEFECT-017 = PROJECT_PROVENANCE_METADATA_WRONG_ADJACENT_RECORD_BINDING`。

按项目既有 forward-only 原则，12IC 原批次保留为审计历史，不静默改写；当前 Registry / State / Matrix / verifier 由 12ID 前向纠正。

## 2. Direct item-level correction

孔夫子公开单品页 `https://book.kongfz.com/4639/9902968122/` 将以下字段绑定在同一第十一期对象上：

- 标题：`国学季刊 第十一期`；
- 目录含：`国图藏元刻十行本《附释音春秋左传注疏》`；
- 编者：杜泽逊；
- 出版社：山东人民出版社；
- ISBN：`9787209115001`；
- 出版时间：`2018-09`；
- 页数：`222`；
- 字数：`290千字`。

相邻第十二期单品页 `https://book.kongfz.com/4639/9902978870/` 则明确为：

- 标题：`国学季刊 第十二期`；
- ISBN：`9787209115018`；
- 出版时间：`2018-12`；
- 页数：`277`；
- 字数：`300千字`。

因此此前的 5018/2018-12 并非“第十一期冲突字段”，而是**第十二期的正确邻接记录**。

## 3. Official NOPSS corroboration

全国哲学社会科学工作办公室的官方项目报告继续作为文章身份的最高公开控制：

- 张丽娟；
- `国图藏元刻十行本《附释音春秋左传注疏》`；
- `《国学季刊》第十一期`；
- 山东人民出版社；
- `2018年9月`。

这与纠正后的孔夫子第十一期单品字段 `2018-09` 一致。

NOPSS 页面未给 ISBN，因此 9787209115001 当前只闭合到**直接公开零售单品级**，尚未升级为出版社/机构图书馆级书目权威。

## 4. Sanmin reclassification

三民页面将 `9787209115018` 标为第十二期，期号和 ISBN 与孔夫子第十二期单品页一致；其 `2019-05-01` 日期与孔夫子 `2018-12` 仍存在二级商业元数据时间差。

所以 12IC 所称“同 ISBN 在第十一/第十二期之间冲突”被撤销；当前仅保留**第十二期出版日期的二级商业元数据张力**。

## 5. What remains valid from 12IC

以下结论不受本次纠正影响：

- 全国社科办能够确认目标文章身份、作者、第十一期、山东人民出版社和 2018年9月；
- Google Books 未找到可用目标卷；
- Open Library 当前路线无阳性记录；
- Internet Archive 唯一 exact-title 命中已直接判定为无关太平天国文本对象的假阳性；
- 张丽娟文章全文仍未通过当前公开路线取得；
- `3368 -> 3288` 的对象级因果机制仍未解决。

## 6. Adjudication

```text
PROV-DEFECT-017
= CONFIRMED_AND_REPAIRED_FORWARD_ONLY

issue 11 public-item ISBN
= 9787209115001

issue 11 public-item date
= 2018-09

issue 11 public-item extent
= 222 pages

issue 12 public-item ISBN
= 9787209115018

issue 12 public-item date
= 2018-12

issue 11 publisher/institutional catalog binding
= UNRESOLVED

target article full text
= NOT RETRIEVED

3368 -> 3288 causal mechanism
= UNRESOLVED
```

## 7. Project accounting

本批只修复研究 provenance 元数据；不改变确定性排盘、候选、Matrix 行数或传承拓扑。

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance defects = 17 / 17 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```

Research record: `docs/research/ZIWEI-GUOXUEJIKAN11-ITEM-LEVEL-ISBN-FORWARD-CORRECTION-R1.json`.
