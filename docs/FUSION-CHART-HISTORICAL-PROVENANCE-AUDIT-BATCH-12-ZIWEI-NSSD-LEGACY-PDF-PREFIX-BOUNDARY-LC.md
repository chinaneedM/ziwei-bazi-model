# Fusion Chart Historical Provenance Audit R1 — Batch 12LC

## NSSD legacy pdfurl：首 4KB 判定为失效域名出售页

Status: **SOURCE-EMITTED URL / RANGE STREAM GET / MAX 4096 BYTES / HTTP200 TEXT-HTML / %PDF ABSENT / DOMAIN-FOR-SALE LANDING PAGE / NO FULL BODY DOWNLOAD / DEAD ACCESS ROUTE / ZERO PRODUCT IMPACT**

12LB 已证明旧 `nssd.org` 地址 HEAD 只返回 HTML。12LC 只对同一原样 URL 发出一次：

```text
GET
Range: bytes=0-4095
stream=True
```

最多读取 4096 bytes 后立即关闭连接。

结果：

```text
HTTP status       = 200
content-type      = text/html; charset=utf-8
content-range     = null
redirect          = none
bytes read        = 4096
%PDF signature    = false
HTML prefix       = true
page title        = www.nssd.org-官网首页
domain-for-sale   = observed
```

因此 12KY 中的 `pdfurl=http://www.nssd.org/articles/article_down.aspx?id=1002462903` 只能保留为**历史遗留字段**，现在不是赵万里文章的公开 PDF 路线。项目不再围绕它继续尝试。

控制证据：workflow `.github/workflows/probe-batch-12lc-nssd-legacy-pdf-prefix-boundary.yml`; exact head `ed600be4b4b848303033359964e6185e38699ba7`; run/job/artifact `36875343203 / 110413211107 / 11169125431`; artifact digest `sha256:4560091348aa323c6b7b704a37f600116b210ff92cf08e4f94b41a187e997368`。

下一门回到 primary-text 候选。2011《赵万里文集》第1卷 p.197 的 NDL 对象身份、馆藏号和目标页已全部闭合，优先检查其公开目录是否直接发出数字对象、在线阅览或复制资格信号；不登录、不提交复制申请。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。

Research record: `docs/research/ZIWEI-NSSD-LEGACY-PDF-PREFIX-BOUNDARY-R1.json`.
