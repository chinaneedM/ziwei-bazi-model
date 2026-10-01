# Fusion Chart Historical Provenance Audit R1 — Batch 12LF

## 全国报刊索引：匿名公开检索面 412 边界

Status: **ROOT 412 / HOME 412 / SEARCH SURFACE NOT RETRIEVED / NO QUERY / NO LOGIN / WAF-vs-AUTH UNRESOLVED / ZERO PRODUCT IMPACT**

上海图书馆公开资料确认《全国报刊索引》是其主管的信息服务体系，历史报纸资源覆盖到 1951 年；因此它是上海《文汇报》1951-08-18 线索值得校准的第一方体系之一。但 12LF 不提交赵万里查询，只尝试读取公开首页。

GitHub 匿名 runner 对：

```text
https://www.cnbksy.com/
https://www.cnbksy.com/home
```

均返回 HTTP 412 / `text/html; charset=utf-8`。由于正常搜索 HTML 未取得，form / search link / script 合同均无法闭合。

此时禁止直接推断“412 = 机构 IP 权限墙”。它也可能是 WAF、浏览器校验或其他前置条件。下一门只解析 412 页面及同域公开可访问的活动详情页，先分类边界，不提交任何目标查询。

控制证据：workflow `.github/workflows/probe-batch-12lf-cnbksy-public-search-surface.yml`; exact head `a86ec5731b5ab1a797bce2d7208d2dc06fad8eb6`; run/job `36877911774 / 110421993332`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。

Research record: `docs/research/ZIWEI-CNBKSY-PUBLIC-SEARCH-SURFACE-R1.json`.
