# Fusion Chart Historical Provenance Audit R1 — Batch 12MB

## 全国报刊索引：高级检索页面 ESA 边界与文本检索支线停止

Status: **ADVANCED ROUTE SOURCE-CONFIRMED / HTTP 412 ESA / ORDINARY+PROFESSIONAL+ADVANCED TEXT-SEARCH BOUNDARY CLOSED / RAW-HTTP BRANCH STOPPED / NO QUERY / NO BYPASS / ZERO PRODUCT IMPACT**

控制 run `37022520964` / job `110888882297` / artifact `11233262837` 在 exact head `b8e0fb38cff11058fc874e6c5585291fc316f65e` 上只对第一方明确输出的 `高级检索=/search/advance` 做一次匿名、无 query parameter、禁止 redirect 的 GET。

返回 HTTP 412 / `text/html; charset=utf-8` / server `ESA`，2464 bytes，SHA-256 `ad3f22dbf7ca055c9f53b1cfbb17e06d8b1c2a6937facde89ab4f8a8a766d918`。静态面 form=0、`_csrf` meta=false、external script=1、inline script=3、visible text length=0；高级检索、题名、作者、文献来源、全字段、精确/模糊、与/或/非等可见文本均为 0。

与 12LP 的 `/search`、12MA 的 `/search/special` 合并后，当前第一方页面明确给出的普通/专业/高级三条**文本检索页面**都在匿名 raw-HTTP 下闭合为 ESA 412/browser-precondition 边界。这个结果只证明访问边界；禁止改写成“检索不存在”“目标不存在”或“已证明必须机构 IP”。

因此 CNBKSY raw-HTTP 文本检索支线正式停止，除非未来出现 materially new 的第一方访问机制。继续测试 sibling route 只会重复 WAF 边界，不再具有足够研究价值。

12MB 没有提交赵万里、文汇报、1951-08-18 或任何目标词，没有提交表单、没有登录/注册，也没有绕过 ESA。下一门 12MC 回到上海《文汇报》1951-08-18 primary-page 主线，只重新校准官方 `dzb.whb.cn` 电子报根页面：先看控制 runner 现在能否读取 root，以及 root 自己是否输出日期导航；禁止直接猜 1951 路径。

控制证据：workflow `.github/workflows/probe-batch-12mb-cnbksy-advanced-search-surface.yml`; run/job/artifact `37022520964 / 110888882297 / 11233262837`; artifact digest `sha256:64379d4e37675ae45a78f386a422d2d664b391dbe5982f9fa6d3418b06226e5f`.

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-ADVANCED-SEARCH-ESA-BOUNDARY-R1.json`.
