# Fusion Chart Historical Provenance Audit R1 — Batch 12MA

## 全国报刊索引：专业检索页面 ESA 边界

Status: **PROFESSIONAL ROUTE SOURCE-CONFIRMED / HTTP 412 ESA / APPLICATION SURFACE NOT RETRIEVED / NO QUERY / NO BYPASS / ZERO PRODUCT IMPACT**

控制 run `37021666728` / job `110886009080` / artifact `11233786634` 在 exact head `8597c768c127144534a346d39c218e94461df69c` 上只执行一项动作：从已闭合的第一方导航 `专业检索=/search/special` 出发，对 `https://www.cnbksy.com/search/special` 做一次匿名、无 query parameter、禁止 redirect 的 GET。

返回为 HTTP 412 / `text/html; charset=utf-8` / server `ESA`，2418 bytes，SHA-256 `3a3fb4f8f92ef234e97b025b2643dc792e7a48902be30fd3a8c2894ac980b3e0`。静态面为：form=0、`_csrf` meta=false、external script=1、inline script=3、visible text length=0；`专业检索/Solr/ALL/TI/JTI/PTI/ADTI/检索/验证码/登录/访问受限` 可见文本计数均为 0。

因此只能裁决：专业检索 route 的存在已由第一方页面直接证明，但匿名 raw-HTTP 无法取得真正 application surface；这与此前普通检索 `/search` 的 ESA/browser-precondition 边界一致。412 仍不得被偷换成“没有检索”“没有目标数据”或已证明必须机构 IP。

12MA 没有提交赵万里、文汇报、1951-08-18 或任何目标词，没有提交表单、没有调用搜索 API、没有登录注册，也没有尝试绕过 ESA。下一门 12MB 只测试同样由第一方页面直接输出的 `高级检索=/search/advance`。若 ordinary / professional / advanced 三个文本检索页面均闭合在 ESA 412，则停止继续钻取 CNBKSY raw-HTTP 搜索页，回到其他合法 page-level recovery 路线。

控制证据：workflow `.github/workflows/probe-batch-12ma-cnbksy-professional-search-surface.yml`; run/job/artifact `37021666728 / 110886009080 / 11233786634`; artifact digest `sha256:8d6ea085f1cd72896b9892fd3fa67bdc80e496c7f59cd529f81822c0533845bd`.

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-PROFESSIONAL-SEARCH-ESA-BOUNDARY-R1.json`.
