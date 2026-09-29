# Fusion Chart Historical Provenance Audit R1 — Batch 12IH

## NDL 直接页远隔复制政策边界：p.197 与 1951 pp.221–233 从资格未判推进到“政策层可申请 / 账号费用门槛未执行”

Status: **NDL OFFICIAL REMOTE-COPY POLICY REVIEWED / GENERAL PAPER-HOLDING SERVICE ROUTE CLOSED / 2011 P197 LOCATOR COMPLETE / 1951 ISSUE9 PP221–233 LOCATOR COMPLETE / OLD PERIODICAL SINGLE-ARTICLE WHOLE-COPY RULE CONFIRMED / REGISTERED USER + PAID SERVICE REQUIRED / NO LOGIN / NO REQUEST / NO PAYMENT / NO PAGE BYTES / DIRECT PAGES STILL NOT REVIEWED / ZERO PRODUCT CHANGE**

## 1. Why Batch 12IH exists

Batch 12HG 已把两个高价值直接页目标绑定到 NDL 实物馆藏，但当时对象级远隔复制资格仍记为 `NOT_ADJUDICATED`。Batch 12IG 又把现代引文桥升级到浙江图书馆官方期刊 PDF，同时明确：真正的下一层证据仍是 2011 `《赵万里文集》第1卷 p.197` 与 1951 `《文物参考资料》第9期 pp.221–233` 的直接页面。

本批不再增加馆藏数量，而是复核 NDL 当前官方复制规则，判断这两个已经精确定位的纸质馆藏目标是否存在合法远隔复制路径，以及路径在何处开始需要用户账号、费用与外部操作。

## 2. NDL official remote-copy service

官方规则页：

- `https://ndlsearch.ndl.go.jp/help/remotecopy`
- `https://www.ndl.go.jp/copy/copyright`

NDL 当前官方说明把馆藏资料列为远隔复制的一般对象，但排除若干特殊载体；服务需要注册利用者，并属于有偿服务。申请前还必须能精确指定希望复制的位置。

对本项目最重要的是两个目标的定位信息已经满足官方要求：

```text
2011 book:
  title = 趙萬里文集 第1卷
  call = UM11-C247
  NDLBibID = 023434359
  target = p.197

1951 serial:
  title = 文物参考资料
  call = Z8-AC150
  held range = 2(7)-2(12) 1951
  issue = 9
  article = 永乐大典展览的意义——一九五一年八月北京图书馆举办
  pages = 221–233
```

因此，“申请时无法描述要哪一页/哪一篇”的障碍已经不存在。

## 3. Copy-scope control

NDL 著作权说明的服务规则区分图书与期刊：一般图书原则上只能复制著作物的一部分；论文集/分担著作按各独立作品计算；已过“相当期间”的期刊，单篇论文/文章可以整篇复制。

本批只作服务政策层判断：

```text
2011 p.197:
  one-page target
  -> compatible with a partial-copy request at the general policy layer
  -> final staff acceptance remains untested

1951 issue-9 article pp.221–233:
  sufficiently old periodical article
  -> whole-article copying is permitted by the NDL service rule
  -> final item/order processing remains untested
```

这里不作著作权保护期终结/公版判断。项目只记录 NDL 自身当前服务规则允许的复制范围。

## 4. Account / fee boundary

本批没有执行任何外部账户动作：未登录 NDL；未注册或修改图书馆账号；未提交远隔复制申请；未传输身份证明；未选择邮寄或 PDF 交付；未产生费用；未取得任何目标页字节。

```text
policy-layer eligibility
= CLOSED

exact item request execution
= LOGIN_AND_FEE_GATED / NOT EXECUTED

2011 p.197 direct text
= NOT_REVIEWED

1951 pp.221–233 direct text
= NOT_REVIEWED
```

“可以申请”绝不能被写成“已经看过页面”。

## 5. Evidence and object-identity firewall

Batch 12IG 的对象防火墙继续原样有效：

```text
1951 quoted member = 宋刻《春秋左传注疏》
FID070 physical adjudication = 元刻元印十行本

same physical object
= UNRESOLVED

same-object collapse
= FORBIDDEN
```

复制政策的闭合不会为 FID070 的捐赠批次、捐赠日期或 `3368 -> 3288` 因果机制增加任何证据。

## 6. Adjudication

本批的实质增量只有访问状态：NDL general remote-copy policy route = CLOSED；2011 p.197 与 1951 pp.221–233 的 policy eligibility = CLOSED_AT_GENERAL_SERVICE_LAYER；direct page evidence increment = 0；account/payment action = 0。

## 7. Project accounting

保持不变：Matrix 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT；provenance defects 17/17 repaired；chart algorithm defects 0；algorithm reopens 0；candidate collapses 0；deterministic product **CLOSED**。Transmission genealogy 无节点、边或对象同一性变化。

## 8. Highest next gate

1. 继续寻找公开、合法、可直接读取的 2011 p.197 或 1951 pp.221–233；不再堆叠重复馆藏。
2. 并行继续冀淑英《冀淑英古籍善本十五讲》第九讲的权威页码/直接正文定位。
3. 若公开直接页仍无法取得，则 NDL 注册用户有偿复制已成为明确的下一项账号/费用依赖动作；在用户明确授权以前，不登录、不提交、不付款。

Research record: `docs/research/ZIWEI-NDL-DIRECT-PAGE-REMOTE-COPY-POLICY-BOUNDARY-R1.json`.
