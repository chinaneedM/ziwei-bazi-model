# Fusion Chart Historical Provenance Audit R1 — Batch 12IC

## 张丽娟 2018《国学季刊》第十一期：官方文章身份闭合，公开全文路线未闭合，ISBN/出版月商业元数据冲突保留

Status: **OFFICIAL NOPSS ARTICLE IDENTITY CONFIRMED / GUOXUE JIKAN ISSUE 11 CONFIRMED AT PROJECT-REPORT LEVEL / PUBLIC FULLTEXT NOT RETRIEVED / GOOGLE BOOKS NO POSITIVE ROUTE / OPEN LIBRARY NO POSITIVE ROUTE / INTERNET ARCHIVE EXACT-TITLE HIT FALSE POSITIVE / ISBN 9787209115018 ISSUE BINDING UNRESOLVED / PUBLICATION MONTH CONFLICT UNRESOLVED / ZERO PRODUCT CHANGE**

## 1. Controlling official citation

全国哲学社会科学工作办公室的《〈春秋左传〉校注及研究中期检查报告》直接列出：

- 文章：`国图藏元刻十行本《附释音春秋左传注疏》`；
- 作者：张丽娟；
- 载体：`《国学季刊》第十一期`；
- 出版社：山东人民出版社；
- 日期字段：`2018年9月`。

同一官方报告还概述了文章的核心版本学判断：国图铁琴铜剑楼旧藏十行本原著录为`元刻明修本`，张丽娟实物研究重新判为难得的`元刻元印十行本`，未见补版、修版痕迹。

这一层是当前文章身份与研究摘要的最高权威公开控制，但它不是文章全文，也没有在已审页面中公开目标馆藏的全部现代索书号/编目更正过程。

## 2. Public full-text route probes

### 2.1 Google Books / Open Library

12IC-r1 的 Google Books 查询没有返回可绑定《国学季刊》第十一期或目标文章的候选卷，因此没有可继续执行的 within-volume 查询。

12IC-r4 直接测试公开 ISBN 假设 `9787209115018`：

- Open Library ISBN endpoint → HTTP 404；
- `国学季刊 + 第十一期 + 张丽娟` 搜索 → `numFound = 0`。

这些结果只构成当前公共检索面的能力边界，**不得**推导“该期不存在”或“没有数字副本”。

### 2.2 Internet Archive

短语 `国图藏元刻十行本` 返回 27 个结果；更严格的完整文章题名返回 1 个结果。

对这个唯一 exact-title 命中继续解析对象后，其 identifier 为 `3_20260926_202609`，对象实际标题是《太平军中的婚姻状况与两性关系探析…》，subject 为`太平天国`，所列公开文本文件也属于该无关对象。

因此：

```text
IA exact-title hit = FALSE_POSITIVE_INDEX_MATCH
target article identity = NOT PROVED BY IA
public article fulltext = NOT RETRIEVED
```

## 3. Issue / ISBN / publication-date conflict

12IC-r5 把三个公开页面直接固化：

| source | observed public metadata | authority role |
|---|---|---|
| 全国社科办 | 第十一期 / 山东人民出版社 / 2018年9月 / 张丽娟目标文章 | 官方项目成果表与研究摘要控制 |
| 孔夫子旧书网 | 第十一期 / 目标文章列于目录 / ISBN 9787209115018 / 2018-12 | 商业零售书目定位器 |
| 三民网路书店 | 第十二期 / ISBN 9787209115018 / 2019-05-01 | 商业零售书目反证控制 |

同一个 ISBN 被商业来源分别绑定到第十一期与第十二期，因此不能用 `9787209115018` 静默完成第十一期的物理对象身份。

官方报告与孔夫子页面的出版月份也不一致：`2018年9月` vs `2018-12`。在获得出版社/图书馆级的具体期刊对象记录前，月份冲突保留为未决。

## 4. Adjudication

```text
article identity at official project-report level
= CONFIRMED

article container issue at official project-report level
= 《国学季刊》第十一期

public fulltext route
= UNRESOLVED_NO_PUBLIC_FULLTEXT_RETRIEVED

exact physical issue identity
= UNRESOLVED

ISBN 9787209115018 -> issue 11
= NOT AUTHORIZED

publication month reconciliation
= UNRESOLVED

exact 3368 -> 3288 causal mechanism
= UNRESOLVED
```

商业书目只能作为发现/冲突控制，不能反向覆盖官方项目报告，也不能提供未见文章页中的馆藏号、书号或编目过程。

## 5. Highest next gate

1. 获取出版社或机构图书馆对`《国学季刊》第十一期`的稳定书目对象，核实 ISBN、年月、页数；
2. 通过合法公开或机构路线取得张丽娟文章全文/直接页面；
3. 在全文中检查是否出现国图索书号、旧书号、编目史、更正依据等能够解释`3368→3288`的对象级信息；
4. 瞿氏捐赠/入藏精确批次与日期继续并行，不依赖全文路线。

## 6. Project boundary

本批不改变确定性排盘、候选、Matrix 行数、传承图拓扑或 provenance-defect 计数。

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance defects = 16 / 16 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```

Research record: `docs/research/ZIWEI-ZHANG-LIJUAN-GUOXUEJIKAN11-PUBLIC-FULLTEXT-ROUTE-BOUNDARY-R1.json`.
