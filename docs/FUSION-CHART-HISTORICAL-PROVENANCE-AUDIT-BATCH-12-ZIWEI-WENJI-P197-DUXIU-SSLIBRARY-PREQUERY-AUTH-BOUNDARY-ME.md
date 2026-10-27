# Fusion Chart Historical Provenance Audit R1 — Batch 12ME

## 《赵万里文集》第一卷 p.197：读秀 / SSLibrary 查询前认证边界

Status: **NEW PLATFORM FAMILY TESTED / SSLIBRARY PRE-QUERY LOGIN REDIRECT / DUXIU IP+ACCOUNT AUTH GATE / NO TARGET QUERY / NO P.197 REVIEW / NO ABSENCE CLAIM / ZERO PRODUCT IMPACT**

12MD 已确认浙江图书馆 2026 年官方期刊对象属于 12IG 同一证据载体，不能重复计票。12ME 因此转向此前仓库未测试的读秀 / 超星汇雅平台族，目标不是绕过认证，而是先判断是否存在匿名、source-emitted 的合法检索合同，可以进一步定位 2011《赵万里文集》第一卷 / ISBN 9787501346653。

### SSLibrary

exact-head run `37175159409` / job `111356154814` / artifact `11292524671`，artifact digest `sha256:461f1cc7c0acc16e7bb283365745cc851e3b91d5e78b71dce49132b58d4388f0`。

- `https://www.sslibrary.com/` → HTTP 302 → `/entry/login`；
- 该 hop → HTTP 302 → `/user/login/showlogin`；
- 在允许跟随的公开链上未恢复 form、same-host source-emitted script 或匿名 search contract；
- 未提交书名/ISBN 查询。

裁决：`CLOSED_AS_PREQUERY_AUTH_REDIRECT_BOUNDARY`。这只描述当前 runner 的公开访问边界，**不是目标书不存在的证据**。

### 读秀

exact-head run `37175296972` / job `111356561245` / artifact `11293245695`，artifact digest `sha256:819fd12ed264cabfaeaded6f86132b5d752574bfd21c47b862e710d0dc4cfea8`。

- `https://edu.duxiu.com/` → HTTP 302 → `/login.jsp`；
- login page HTTP 200 / 18,764 bytes / SHA-256 `e081a0a390703c7f576ad2c1ccc0604e79ae3c1137552411115392ca53ab0196`；
- 页面明确表示当前 runner IP 不在服务范围，需要账号登录，并显示机构用户、个人/读秀卡、CARSI 与验证码等认证控件；
- 未提交书名/ISBN 查询，未登录，未尝试 CAPTCHA、CARSI 或机构认证。

裁决：`CLOSED_AS_PREQUERY_IP_ACCOUNT_AUTH_BOUNDARY`。

### 总裁决

```text
SSLIBRARY_ANONYMOUS_TARGET_QUERY = NOT_AUTHORIZED_FROM_CURRENT_CONTRACT
DUXIU_ANONYMOUS_TARGET_QUERY = NOT_AUTHORIZED_FROM_CURRENT_CONTRACT
TARGET_BOOK_PRESENCE_OR_ABSENCE = NOT_ADJUDICATED
DIRECT_2011_WENJI_P197 = NOT_REVIEWED
LOGIN_OR_AUTH_BYPASS = FORBIDDEN
EVIDENCE_VOTE_INCREMENT = 0
TRANSMISSION_IMPACT = NONE_ACCESS_BOUNDARY_ONLY
```

12ME 不改变任何排盘规则、候选规则、传承图结论或矩阵计数。下一门 12MF 将公开检索优先级转向更强的一手目标：赵万里 1951《〈永乐大典〉展览的意义》，历史载体《文物参考资料》vol.2 no.9 pp.221–233 的**新开放/机构级直页对象路线**。既有 NLC Wenjin/NCPSsd 登录/SSO边界不得绕过；NDL 付费/中介复制仍需用户明确授权。

2011《赵万里文集》第一卷 p.197 与上海《文汇报》1951-08-18 保持平行未闭合，不因本批次降格为“不存在”。

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。

Research record: `docs/research/ZIWEI-WENJI-P197-DUXIU-SSLIBRARY-PREQUERY-AUTH-BOUNDARY-R1.json`.
