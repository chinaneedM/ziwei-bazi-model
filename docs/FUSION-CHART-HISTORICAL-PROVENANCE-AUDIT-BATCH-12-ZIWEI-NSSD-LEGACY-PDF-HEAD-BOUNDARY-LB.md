# Fusion Chart Historical Provenance Audit R1 — Batch 12LB

## NSSD legacy pdfurl：HEAD 边界

Status: **SOURCE-EMITTED URL / HEAD ONLY / HTTP200 TEXT-HTML / NO REDIRECT / NO PDF CONTENT-TYPE / NO BODY DOWNLOADED / PUBLIC PDF STATUS UNRESOLVED / ZERO PRODUCT IMPACT**

12KY 的 NCPSsd 第一方详情对象直接发出：

```text
http://www.nssd.org/articles/article_down.aspx?id=1002462903
```

12LB 不执行下载，只对这个**原样 source-emitted URL**做匿名 HEAD。

结果：

```text
status       = 200
content-type = text/html; charset=utf-8
location     = null
set-cookie   = absent
```

因此目前不能把该字段解释成匿名公开 PDF。它可能是 HTML 中转、旧站兼容页、错误页或其他边界；本批没有 GET、没有响应正文、没有登录。

下一门 12LC：只发一个 `Range: bytes=0-4095` 的匿名流式 GET，最多读取前 4096 bytes 后立即关闭。若服务器忽略 Range，也绝不继续读取整篇；只判断 `%PDF` 文件签名、HTML/认证边界或错误状态。

控制证据：workflow `.github/workflows/probe-batch-12lb-nssd-legacy-pdf-head-boundary.yml`; exact head `e09648684492d1af417eb0e9a728d03fa45b4552`; run/job/artifact `36874923001 / 110411776086 / 11167604568`; artifact digest `sha256:f4c22565823f284630e0f61949d017fc32a1d04a76564c0187bc66fd5a693d0b`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。

Research record: `docs/research/ZIWEI-NSSD-LEGACY-PDF-HEAD-BOUNDARY-R1.json`.
