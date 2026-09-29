# Fusion Chart Historical Provenance Audit R1 — Batch 12IF

## Cambridge 1951《文物参考资料》独立原刊馆藏路线：卷2第9期明确包含，页级文本仍未取得

Status: **CAMBRIDGE FIRST-PARTY HOLDING / 文物参考资料 卷2 i–xii / CALL FB.252:14 / TARGET ISSUE 9 EXPLICITLY CONTAINED / NEEDHAM YEAR-RANGE ROW NOT DOUBLE-COUNTED / DIRECT PP221–233 NOT REVIEWED / ZERO PRODUCT CHANGE**

## 1. Target

当前需要直接校勘的赵万里原文为：

- 赵万里《永乐大典展览的意义——一九五一年八月北京图书馆举办》；
- 《文物参考资料》1951年第9期；
- 卷2；
- 页221–233。

这一书目信息已经由国家图书馆古籍馆刘鹏的研究综述直接确认。

## 2. Cambridge first-party holding

Cambridge University Library 的 `Chinese Periodicals` 一手联合馆藏页直接列：

```text
文物参考资料 / 北京 /
总1-6,8,卷2i-xii,总53-64,69-71,73-88,91-100 /
1950-58 / FB.252:14
```

`卷2 i–xii` 明确包含 1951 年卷2第1–12期，因此目标第9期无需推测即被馆藏范围包含。

12IF 的 GitHub 探针抓取该一手页面并验证：目标刊名、`FB.252:14`、`卷2i-xii` 三个控制同时存在。

## 3. Needham row is not double-counted

同一 Cambridge 联合目录还列一条 Needham Research Institute：

```text
文物参考资料 / 北京 / - / 1951-58 / NRI
```

这证明 Cambridge 体系内另有年度级馆藏线索，但没有显式列出各期缺佚。因此 12IF 不把它计算成第二个“第9期精确闭合”，避免把年度范围过度解释为逐期无缺。

## 4. Relation to existing routes

此前已有：

- NDL 原刊合订卷 `Z8-AC150`：`2(7)-2(12) 1951`，明确包含第9期；
- 龙谷大学 1986 影印本 `AN10296217 / 054/638`：覆盖 1951 年卷2。

12IF 新增的是**独立 Cambridge 原刊馆藏路线**，而不是新文章文本。

```text
independent original-periodical holding increment = 1
direct article text increment = 0
```

## 5. Access firewall

Cambridge 页面目前只闭合馆藏范围：

- 未取得 221–233 页页面；
- 未取得公开数字替代物；
- 未发送复制申请；
- 未执行馆员账号/身份动作；
- 未产生费用。

所以不能把“Cambridge 有这期”写成“我们已经校勘赵万里原文”。

## 6. Adjudication

```text
Cambridge 1951 vol.2 issue 9 physical route
= CLOSED

Needham exact issue-9 route
= NOT DOUBLE-COUNTED

Zhao Wanli pp.221–233 direct text
= NOT REVIEWED

2011 Zhao collected works p.197 direct text
= NOT REVIEWED

1951 Qu 62-title original wording direct collation
= NOT CLOSED

FID070 exact Qu donation batch/date
= UNRESOLVED

3368 -> 3288 causal mechanism
= UNRESOLVED
```

## 7. Highest next gate

下一步不再优先堆叠馆藏数量，而应升级证据层级：

1. 合法取得 1951 原刊第9期 221–233 页或可靠影印页；
2. 直接校勘 NDL 所藏 2011《赵万里文集》第1卷 p.197；
3. 直接校勘冀淑英《古籍善本十五讲》第九讲的 1950/1953 批次及注源；
4. 只有出现明确书名单、登录簿、索书号/书号或稳定对象指纹时，才把 FID070 绑定到具体瞿氏捐赠批次。

## 8. Project accounting

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance defects = 17 / 17 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```

Research record: `docs/research/ZIWEI-WENWU-CANKAO-CAMBRIDGE-1951-V2-HOLDING-ROUTE-R1.json`.
