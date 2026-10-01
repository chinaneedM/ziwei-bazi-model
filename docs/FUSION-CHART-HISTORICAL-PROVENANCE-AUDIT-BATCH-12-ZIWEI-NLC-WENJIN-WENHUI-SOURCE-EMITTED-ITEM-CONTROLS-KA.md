# Fusion Chart Historical Provenance Audit R1 — Batch 12KA

## 国家图书馆文津《文汇报》候选条目 source-emitted item/detail 控件闭合

Status: **WENJIN RESULT ITEM CONTROLS DIRECTLY OBSERVED / RECORD IDS SOURCE-EMITTED / DATA SOURCE SOURCE-EMITTED / MAKEDETAILURL CONTRACT CLOSED / NO RECORD-ID GUESS / NO DETAIL EXECUTION IN KA / ZERO PRODUCT IMPACT**

### 1. 目标

12JZ 已从国家图书馆文津宽题名结果中定位两个高价值候选：2004 点通数据有限公司《文汇报》计算机文件，以及 1951《文汇报-副页》。12KA 只回答一件事：能否在不猜 record ID、dataSource 或详情端点的条件下，从第一方结果页本身恢复它们的 item/detail 控件。

### 2. 直接控件

文津“文汇报”结果页 HTTP 200 / 141,873 bytes / SHA-256 794b16327b6eb4211603b8aeb3659f6d3eb6bc2ec20117474f670b97d30775cd。

匹配结果行直接 source-emit：

- 2004 计算机文件：docId -7686431772105481921 / dataSource ucs01；
- 1951 文汇报-副页：docId -2284569176548744322 / dataSource ucs01。

同页 source-emitted 脚本 http://find.nlc.cn/js/resultList.js（SHA-256 90b95a7268acd8e44ad2b7ee00b0dd6364634108f6d2abc245a6b574ec727310）直接定义 makeDetailUrl，将详情 URL 组装为 /search/showDocDetails?docId=<id>&dataSource=<source>&query=<query>。

因此两条详情路径的 identifier 与参数来源已经闭合，不再属于猜测。

### 3. 防火墙

KA 只关闭“如何合法到达条目详情”，不把 catalog locator 当成历史文本，也不把 2004 记录提前等同于 2003 捐赠对象，更不把 1951 副页提前等同于上海 1951-08-18 原页。

### 4. 控制证据

- workflow: .github/workflows/probe-batch-12ka-nlc-wenjin-wenhui-item-controls.yml
- exact head: 2458941eddd8c3d063bb18e321f13b9ab7033525
- run / job / artifact: 36852114147 / 110335954125 / 11156211973
- artifact digest: sha256:067d0c5b82c075207a9392525c56d5ebc22663cbf84e73fdda5013505cd54c47

未登录、未用读者账号、未注册、未猜私有端点、未猜 record ID / dataSource、未提交状态变更请求。

### 5. 项目影响与下一门

Matrix 维持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 不变。

下一门是严格按上述 source-emitted docId/dataSource 执行两个详情 GET，并对 2004 光盘对象与 1951 副页对象做 item-level 身份裁决。

Research record: docs/research/ZIWEI-NLC-WENJIN-WENHUI-SOURCE-EMITTED-ITEM-CONTROLS-R1.json.
