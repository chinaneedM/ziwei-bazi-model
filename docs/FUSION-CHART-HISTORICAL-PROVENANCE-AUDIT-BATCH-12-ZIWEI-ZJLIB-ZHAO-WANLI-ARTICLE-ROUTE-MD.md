# Fusion Chart Historical Provenance Audit R1 — Batch 12MD

## 浙江图书馆《图书馆研究与工作》2026年第4期赵万里文章路线复核与去重

Status: **FIRST-PARTY ARCHIVE→ISSUE ROUTE CLOSED / TARGET ARTICLE ANCHOR NOT EXPOSED ON REVIEWED ISSUE HTML / SAME OFFICIAL ARTICLE+PDF ALREADY CLOSED BY 12IG / DUPLICATE EVIDENCE VOTE +0 / NO PDF DOWNLOAD / ZERO PRODUCT IMPACT**

12MC 停止了上海《文汇报》官方电子报在当前 runner 上的重复超时支线。12MD 按既定门禁转向浙江图书馆主办《图书馆研究与工作》的官方过刊页，只先读取 `https://bjb.zjlib.cn/CN/archive_by_years`，再跟随该页 source-emitted 的 `2026 No. 4` 期次链接；不猜文章 ID，不执行账号/付费动作，也不下载 PDF。

exact-head probe run `37025054121` / job `110897449245` / artifact `11234512700`（head `121a7aa5d200ee66d98a0c2da356191f1ccaacd0` / tree `da079cf1d285337d8d5296156bc2b68fc49e1f43`）成功。过刊页 HTTP 200 / 64,415 bytes / SHA-256 `9a7503c31b8d4360a465dbcbf4c50e28de819f0209e1ddf118fe92554a2a59d2`，并直接发出 `https://bjb.zjlib.cn/CN/Y2026/V0/I4`。该期页面 HTTP 200 / 30,046 bytes / SHA-256 `2cac8afd9f72f67429fd97a149c9a593bd27bc13ec766614fbf81f14c41a4429`。

在 12MD 允许审查的该期静态 HTML 上：

- `赵万里`、`趙萬里`、`肖玲`、`赵万里与古籍保护` token 均为 0；
- Zhao/Xiao relevant anchors 为 0；
- 唯一 PDF-like anchor 为显示文字 `PDF全文`、href=`javascript:;`，它不是可直接绑定的 PDF object；
- 因此 12MD 没有跟随 article route，也没有跟随/下载 PDF。

这只能说明**该期被审查的静态 HTML 没有直接发出目标文章对象**，绝不构成“文章不存在”“该期不含该文”或任何全文缺失结论。

更重要的是，仓库现有 source registry 已经在 Batch 12IG 对**同一个浙江图书馆官方文章/PDF对象**完成了更强的直接绑定：article `/CN/Y2026/V0/I4/2`、PDF `/CN/PDF/1737`、PDF SHA-256 `2e0b9c1d59ccc95523b48144964cb8f528161c3b9201cb28da0cee41de9cd776`，并在 PDF p.92 无 OCR 绑定到 `[2]197` 引文桥。因此 12MD 不得把 archive→issue 的第二条发现路线重复计为独立学术见证，也无需重新下载相同 PDF。

裁决：

```text
ARCHIVE_TO_2026_NO4_ROUTE = CLOSED_FIRST_PARTY
TARGET_ARTICLE_ANCHOR_ON_REVIEWED_ISSUE_HTML = NOT_OBSERVED
STATIC_ZERO_TOKENS_AS_ARTICLE_ABSENCE = FORBIDDEN
SAME_OFFICIAL_ARTICLE_PDF_ALREADY_CLOSED_BY_12IG = true
DUPLICATE_EVIDENCE_VOTE_INCREMENT = 0
DIRECT_2011_WENJI_P197 = NOT_REVIEWED
DIRECT_1951_ORIGINAL = NOT_REVIEWED
TRANSMISSION_IMPACT = NONE_DEDUP_ROUTE_ONLY
```

下一门 12ME 回到真正未闭合的高价值目标：只寻找**新的、合法、公开或机构级的 2011《赵万里文集》第一卷 p.197 直页路线**。已有 NDL 付费/中介复制路径继续保持“需用户明确授权”的边界，不自动提交请求、身份信息或付款。1951《文物参考资料》vol.2 no.9 pp.221–233 与上海《文汇报》1951-08-18 继续作为平行 primary targets。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-ZJLIB-ZHAO-WANLI-ARTICLE-ROUTE-R1.json`.
