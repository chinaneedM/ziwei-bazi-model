# Fusion Chart Historical Provenance Audit R1 — Batch 12LY

## 全国报刊索引：专业检索 4.3 正文媒体范围修复与字段代码直读

Status: **TOC-SCOPE DEFECT REPAIRED / TRUE 4.3 MEDIA = 6 / FIELD CODES VISUALLY COLLATED / NO OCR / NO LIVE QUERY / ZERO PRODUCT IMPACT**

首轮 12LY run `36894975137` / job `110479567906` / artifact `11179041729` 虽执行成功，但其 substring 搜索先命中目录块 `body_index=1` 中的“4.3 专业检索”，从而把目录后至正文 4.4 前的 59 张图错误归入 4.3。该 run 现明确标记为 superseded，不作为专业检索局部媒体范围的控制证据。

修复 run `37018829441` / job `110876339613` / artifact `11232711441` 在 exact head `94436ea5c40fa3a688e7bde3e57fa76f746a0931` 上改为“精确规范化标题 + 必须位于 `4. 高级功能` 之后”的范围规则。正文标题位置被稳定闭合为：`4. 高级功能=179`、`4.3 专业检索=195`、`4.4 检索结果可视化=213`。真正 4.3 范围仅含 rId62–rId67 六张 PNG，全部 1265×616。

六图逐张直接目验、未使用 OCR。正文页签的通用代码直接可见 `ALL=全字段 / TI=题名 / PD=时间 / JTI=刊名/报名`；图片页签通用代码为 `ALL / PTI=图片标题 / FAP=图片责任者 / PD / JTI`；广告页签通用代码为 `ALL / ADTI=广告标题 / ADPB=广告发布者 / JTI`。各资源类型的 NOD/NATI/BC/SNTI/NOP/ACOL/NCT、ISS/VO/CLC/AB/CT、CAP/AT/ACOL、SL/ADPR、FXJG/YEAR/CBGJ/ZRZ/NRTY/ZTC/TSCT 等代码亦按截图逐项记录在 machine research JSON 中；`测试` 行只显示空标签对应 `TEST`，禁止擅自补名。

后三张截图把组合语法直接示例为：`ALL: 鲁迅` → `ALL: 鲁迅 AND TI: 鲁迅先生` → `ALL: 鲁迅 AND TI: 鲁迅先生 AND JTI: 铁报`。OOXML 正文叙述却写“提名：鲁迅先生，刊名/报名：轶报”；因此 `题名/提名` 与 `铁报/轶报` 两处现代手册内部不一致均原样保留，不静默统一。

12LY 只校勘官方 2024 新平台用户手册及其截图，不执行任何专业检索，不提交赵万里/文汇报目标词，不登录、不注册。此批属于现代 operational evidence，不改变历史 Matrix、传承谱或确定性排盘。

控制证据：repaired workflow `.github/workflows/probe-batch-12ly-cnbksy-professional-section-media-map.yml`; run/job/artifact `37018829441 / 110876339613 / 11232711441`; artifact digest `sha256:f46145373e738aeb21161535afcef9e1e575a545a855143cbf1237fd2869f7f6`.

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-PROFESSIONAL-SECTION-MEDIA-MAP-R1.json`.
