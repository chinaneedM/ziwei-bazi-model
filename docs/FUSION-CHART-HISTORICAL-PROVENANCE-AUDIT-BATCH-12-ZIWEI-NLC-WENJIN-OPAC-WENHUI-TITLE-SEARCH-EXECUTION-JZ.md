# Fusion Chart Historical Provenance Audit R1 — Batch 12JZ

## 国家图书馆文津 / OPAC《文汇报》题名检索执行与 item 候选边界

Status: **12JX CONTRACT EXECUTION CALIBRATED / WENJIN POSITIVE CONTROL PASS / OPAC POSITIVE CONTROL PASS / BROAD WENHUI POSITIVE / WENJIN EXACT 60Y+61Y ZERO SCOPED / OPAC EXACT-LONG-TITLE NEGATIVE NOT AUTHORIZED / 2004 COMPUTER-FILE CANDIDATE / 1951 SUPPLEMENT CANDIDATE / DIRECT TARGET PAGES NOT REVIEWED / ZERO PRODUCT IMPACT**

### 1. 正控

只使用 12JX 第一方 GET 合同。《史记》在文津返回 HTTP 200 且显式显示约 67000 个结果；OPAC 也回显查询词并进入多库结果页。两条合同均通过执行级正控。

### 2. 文津《文汇报》

`文汇报60年报纸光盘` 与 `文汇报61年全文数据光盘` 均显式 `resultCount=0` / “没有找到”。此负结果只限当前文津全部字段检索，不等于 OPAC 无馆藏，也不否定 2003 捐赠报道。

宽题名 `文汇报` / `文匯報` 大量命中。首屏关键候选包括：1987 缩微文献；2004 点通数据有限公司《文汇报》计算机文件（电子出版物数据中心文汇出版社）；以及 1951《文汇报-副页》报纸记录。它们目前都只是 item 候选。

### 3. OPAC 边界

宽题名 `文汇报` 与 `文匯報` 均回显查询词，显示外文文献 117、中文及特藏文 246。两个长题名响应虽然 HTTP 200，却没有回显查询词，也没有可信零命中计数，因此不授权 `OPAC_NONHOLDING` 或长题名零结果结论。

### 4. 控制证据

- workflow: `.github/workflows/probe-batch-12jz-nlc-wenjin-opac-wenhui-title-search.yml`
- exact head: `a6c338a6e3cea1b0b484118dfe28d5523a1b84af`
- run/job/artifact: `36847667928 / 110321594775 / 11154276297`
- artifact digest: `sha256:72929d94b5e818503b3c37af6e15441e9d4858f067e144cdcc1a16f76d9740b4`

### 5. 防火墙

2004“计算机文件”不得自动等同 2003《文汇报60年报纸光盘》；1951“副页”不得自动等同 1951-08-18 目标页；当前目录元数据不得替代原页正文。

### 6. 项目影响与下一门

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 暂不新增边。下一门是只沿 source-emitted item/detail 控件闭合 2004 计算机文件和 1951 副页记录的 item identity，同时继续直接原页恢复。

Research record: `docs/research/ZIWEI-NLC-WENJIN-OPAC-WENHUI-TITLE-SEARCH-EXECUTION-R1.json`.
