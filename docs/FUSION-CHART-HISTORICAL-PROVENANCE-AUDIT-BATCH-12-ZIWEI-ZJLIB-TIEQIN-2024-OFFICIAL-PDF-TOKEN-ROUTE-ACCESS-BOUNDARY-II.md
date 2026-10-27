# Fusion Chart Historical Provenance Audit R1 — Batch 12II

## 浙江图书馆 2024 铁琴铜剑楼论文官方 PDF 令牌路由边界：下载契约成立，但当前三类 source-emitted 路由均未产出 PDF 字节

Status: **ZJLIB FIRST-PARTY ARTICLE SURFACE CLOSED / OFFICIAL PDF DISPLAY OBSERVED / DOWNLOAD FRONTEND CONTRACT CLOSED / PDF + PDF_CN + PDF_MOBILE PREFLIGHT STATUS=1 / EXACT SOURCE-EMITTED TOKEN ROUTES TESTED / ALL RETURN SAME 3241-BYTE SERVER HTTP404 WRAPPER / NO PDF MAGIC / NO FULLTEXT REVIEW / NO SHOPPING OR PAYMENT FLOW / FID070 IDENTITY FIREWALL PRESERVED / ZERO PRODUCT CHANGE**

## 1. Why Batch 12II exists

Batch 12IH 已把 2011 p.197 与 1951 pp.221–233 的 NDL 远隔复制路径闭合到“政策层可申请、账号费用动作未执行”。公开免费路线仍值得优先检查，因为浙江图书馆主办的《图书馆研究与工作》2024年第7期公开列出蔡成普、李静《郑振铎与铁琴铜剑楼藏书捐献》，并在文章页显示 PDF(549 KB)。

本批只回答一个访问问题：**官网自己当前发出的 PDF 下载契约，能否在不登录、不购买、不付款的前提下直接产出 PDF 字节？**

## 2. First-party article identity

官方文章与期次表面直接闭合：

```text
title = 郑振铎与铁琴铜剑楼藏书捐献
authors = 蔡成普 / 李静
journal = 图书馆研究与工作
year / issue = 2024 / 7
printed start page = 46
publication date = 2024-07-10
article id = 1783
public surface = PDF(549 KB)
```

官方入口：

- `https://bjb.zjlib.cn/CN/Y2024/V0/I7/46`
- `https://bjb.zjlib.cn/CN/lexeme/showArticleByLexeme.do?articleID=1783`
- `https://bjb.zjlib.cn/CN/Y2024/V0/I7`

“页面显示 PDF”只证明官网公开下载意图/入口存在，不等于本项目已经取得 PDF 字节。

## 3. Official front-end contract

官网 `download_cn.js` 的 `lsdy1()` 先向 `/CN/article/showArticleFile.do` POST：

```text
attachType = PDF | PDF_CN | PDF_Mobile
id = 1783
json = true
```

当前三类预检均返回 `status=1`，并分别发出临时 token 路由：

```text
/CN/PDF/1783?token=<ephemeral>
/CN/PDF_CN/1783?token=<ephemeral>
/CN/PDF_Mobile/1783?token=<ephemeral>
```

`downloadPdfTarget="_self"`。官网 `common_cn.js` 的 `mag_request()` 默认创建 HTML form，以 POST 提交；在 PDF 分支没有额外 hidden data。本批不持久化临时 token 值。

## 4. Exact-head route probe

Exact-head research run:

```text
commit = 0907f5508cee8d41825db6fa5c9c926ff3314e27
tree = 3d01cf0f7f7ef8c19f3272fc20eebde2739ea811
workflow run = 36683181763
job = 109782990476
artifact = 11082164368
artifact digest = sha256:854e88d6cd0a1225f5995d6fcd811165cfca9c50d86964614cc28c4dadb1d796
```

按官网真实 helper 语义逐一提交三个与各自 `attachType` 配对的 source-emitted 路由，结果完全一致：

| attachType | route family | transport | content-type | bytes | body SHA-256 | result |
|---|---|---:|---|---:|---|---|
| PDF | `/CN/PDF/1783` | 200 | `text/html;charset=UTF-8` | 3241 | `9c47ea7957afef955da0248c47be6a49c274287abcbe061a7710d7bcbb9ca999` | server HTTP404 wrapper |
| PDF_CN | `/CN/PDF_CN/1783` | 200 | `text/html;charset=UTF-8` | 3241 | same | server HTTP404 wrapper |
| PDF_Mobile | `/CN/PDF_Mobile/1783` | 200 | `text/html;charset=UTF-8` | 3241 | same | server HTTP404 wrapper |

HTML 标题为 `HTTP404 无法找到页面`，正文说明没有找到所访问页面。三个响应都不是 `%PDF-`；`selected_pdf` 为空。

因此这里的 “200” 是 HTTP 传输层状态，不能覆盖正文语义。当前公开路由边界应记为：

```text
OFFICIAL_PUBLIC_DOWNLOAD_CONTRACT_OBSERVED
+
SOURCE_EMITTED_TOKEN_ROUTES_TESTED
+
CURRENT_ROUTE_MATERIALIZATION = SERVER_HTTP404_WRAPPER_HTML
+
DIRECT_PDF_BYTES = NOT_RECOVERED
```

## 5. What this does not prove

本批**不**证明：

1. 浙江图书馆不存在该 PDF；
2. PDF 永久不可访问；
3. 文章全文已经被审阅；
4. 服务器的其他账号态、馆内态或后台路径与公开匿名路径相同；
5. 任何购买/付费路径应该被执行。

本批没有调用购物、购物车或付款 endpoint；没有登录账户；没有产生费用。

## 6. FID070 and object-identity firewall

该 2024 论文是高价值的机构主办学术来源与线索载体，但本批没有取得其 PDF 全文，所以不能借本轮把集合级叙述升级成目标对象事实。

继续保持：

```text
1951 quoted member = 宋刻《春秋左传注疏》
FID070 physical adjudication = 元刻元印十行本

same physical object = UNRESOLVED
same-object collapse = FORBIDDEN

FID070 exact Qu donation batch/date = UNRESOLVED
3368 -> 3288 causal mechanism = UNRESOLVED
```

## 7. Adjudication

本批的净增量是**官方公开访问路径边界**，不是历史对象证据：

- 浙江图书馆 2024 文章身份与公开 PDF 显示：CLOSED；
- 当前官网前端下载契约：CLOSED；
- 三类 source-emitted token route：TESTED；
- 当前公开 PDF materialization：CLOSED_NO_PDF_BYTES_OBSERVED_ON_TESTED_SOURCE_EMITTED_TOKEN_ROUTES；
- direct article full text increment：0；
- product / runtime / transmission-genealogy change：0。

## 8. Project accounting

保持不变：Matrix 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT；provenance defects 17/17 repaired；chart algorithm defects 0；algorithm reopens 0；candidate collapses 0；deterministic product **CLOSED**。

## 9. Highest next gate

1. 不再重复同一浙江 token 路由族，把优先级返回 2011 p.197 / 1951 pp.221–233 的合法直接页获取。
2. 并行继续冀淑英《冀淑英古籍善本十五讲》第九讲《铁琴铜剑楼藏书的收购入藏》的权威页码/直接正文定位。
3. FID070 的确切瞿氏入藏批次、日期，以及 `3368→3288` 因果机制继续等待目标级档案、卡片、校改单、准备记录或显式 crosswalk。
4. 若公开直接页持续关闭，NDL 注册用户有偿复制仍是明确的账号/费用依赖 fallback；没有用户明确授权，不登录、不申请、不传身份、不付款。

Research record: `docs/research/ZIWEI-ZJLIB-TIEQIN-2024-OFFICIAL-PDF-TOKEN-ROUTE-ACCESS-BOUNDARY-R1.json`.
