# Fusion Chart Historical Provenance Audit R1 — Batch 12LP

## 全国报刊索引：普通检索 /search 的 ESA 前置边界

Status: **ORDINARY SEARCH ROUTE SOURCE-CONFIRMED / RAW GET HTTP 412 ESA / APPLICATION FORM NOT EXPOSED / NO QUERY / NO ESA BYPASS / ZERO PRODUCT IMPACT**

12LO 已证明 productTree.js 只是通用 caller-supplied URL 树加载器。12LP 因而直接使用 12LJ 完整 first-party seed-links 已抓到的 href=/search、label=普通检索，只做匿名 GET，不加 query string、不提交表单、不发送赵万里/文汇报或任何目标词。

控制 run `36887835713` / job `110455577866` 在 exact head `ab0135072b42c859087b1dc28bf335f534c3127f` 上成功，结果：HTTP 412；content-type `text/html; charset=utf-8`；server `ESA`；2461 bytes；SHA-256 `391ddee6ecb570a5439f2ff05cafd72605e10459e86ceaec489f76d8943d9764`。

该 412 页面没有 application search form、button、href 或 CSRF meta；只发出一个 ESA 外链脚本和三个 inline challenge block。

因此当前边界必须写成：普通检索入口存在，但匿名 raw HTTP 对 application surface 被 ESA/browser precondition 挡住。不得推断 search absence、target absence 或 institutional-IP requirement，也不得绕过 ESA。

下一门 12LQ 不尝试绕过 ESA，而使用同一第一方页面 source-emitted 的 `/portal/footCategory?id=61`（使用帮助），从官方公开帮助文本侧闭合普通/高级/专业检索字段与操作语义。

控制证据：workflow `.github/workflows/probe-batch-12lp-cnbksy-ordinary-search-surface.yml`; run/job/artifact `36887835713 / 110455577866 / 11175521408`; artifact digest `sha256:f11d84d84e8816a8a6141a4b9ddd31581a0f71fab28f7328dc76d487b7420eaa`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-ORDINARY-SEARCH-ESA-BOUNDARY-R1.json`.
