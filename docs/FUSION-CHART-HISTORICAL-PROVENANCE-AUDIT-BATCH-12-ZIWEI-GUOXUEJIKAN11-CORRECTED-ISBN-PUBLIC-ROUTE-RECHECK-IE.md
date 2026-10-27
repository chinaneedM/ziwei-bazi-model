# Fusion Chart Historical Provenance Audit R1 — Batch 12IE

## 《国学季刊》第十一期正确 ISBN 公共路线重检：Open Library / IA 无阳性，Google Books 429 限流，全文边界继续保留

Status: **CORRECTED ISBN 9787209115001 RECHECKED / GOOGLE BOOKS RATE_LIMITED_UNRESOLVED / OPEN LIBRARY NO POSITIVE RECORD / INTERNET ARCHIVE NO POSITIVE TARGET RECORD / PRIOR EXACT-TITLE IA FALSE POSITIVE RECONFIRMED / PUBLIC FULLTEXT NOT RETRIEVED / ZERO PRODUCT CHANGE**

## 1. Why this recheck is mandatory

Batch 12ID 通过 `PROV-DEFECT-017` 将《国学季刊》第十一期从错误邻接记录 `9787209115018 / 2018-12` 前向纠正为：

- ISBN `9787209115001`；
- 出版时间 `2018-09`；
- 222 页；
- 张丽娟目标文章确在目录中。

因此 12IC 中任何依赖旧 ISBN 的公共全文/书目路线都必须用正确 ISBN 重跑。

## 2. Google Books

GitHub Actions 12IE 探针同时测试：

- `isbn:9787209115001`；
- `"国学季刊" "第十一期"`；
- `intitle:国学季刊 第十一期`。

三次 Google Books API 请求均返回 `HTTP 429 Too Many Requests`。

所以当前正确表述只能是：

```text
Google Books corrected-ISBN route
= RATE_LIMITED_UNRESOLVED
```

`429` 既不是 0 命中，也不是不存在证据。12IC 里“Google Books 无候选”的旧表述不再作为纠正后 ISBN 的控制结论。

## 3. Open Library

正确 ISBN 路线结果：

- `/isbn/9787209115001.json` → HTTP 404；
- ISBN search → `numFound = 0`；
- `国学季刊 第十一期` title search → `numFound = 0`。

这只能闭合为“当前测试端点未观察到阳性记录”，不能推断该书不存在或没有其它数字副本。

## 4. Internet Archive

精确路线：

- `isbn:9787209115001` → `0`；
- `"9787209115001"` → `0`；
- `"国学季刊 第十一期"` → `0`。

宽泛 `"国学季刊" AND "第十一期"` 返回 151 个对象，但明显属于噪声索引面，不能作为目标对象候选集合。

完整目标文章题名再次返回唯一 identifier `3_20260926_202609`；该对象已在 12IC 直接审定为无关《太平军中的婚姻状况与两性关系探析…》文本，故仍为假阳性。

## 5. Adjudication

```text
corrected ISBN route recheck
= COMPLETED

Google Books
= RATE_LIMITED_UNRESOLVED

Open Library
= NO_POSITIVE_RECORD_OBSERVED

Internet Archive exact routes
= NO_POSITIVE_TARGET_RECORD_OBSERVED

target article public full text
= NOT RETRIEVED

issue-11 publisher/institutional catalog binding
= UNRESOLVED

3368 -> 3288 causal mechanism
= UNRESOLVED
```

因此，12IC 的核心“公开全文尚未取得”边界在 12ID 纠错后仍然成立；但其 Google Books 部分必须由 12IE 的限流边界取代，不能再写成确定的零命中。

## 6. Highest next gate

1. Google Books API 限流解除后，仅重试正确 ISBN / 第十一期题名，不重复无意义高频调用；
2. 继续寻找出版社或机构图书馆对 `《国学季刊》第十一期 / ISBN 9787209115001` 的稳定对象；
3. 获取张丽娟文章合法全文/直接页面，核查国图对象级索书号、旧新书号、编目史或更正说明；
4. 瞿氏捐赠/入藏精确年代与批次继续并行。

## 7. Project accounting

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance defects = 17 / 17 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```

Research record: `docs/research/ZIWEI-GUOXUEJIKAN11-CORRECTED-ISBN-PUBLIC-ROUTE-RECHECK-R1.json`.
