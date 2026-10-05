# Fusion Chart Historical Provenance Audit R1 — Batch 12MW

## 三方四正：机械坐标、语境训诂与软件封装

Status: **R4 DECOMPOSED / MODERN SCHOOL GEOMETRY SUPPORTED / EARLIEST DEFINITION OPEN / NO ALGORITHM REOPEN**

`HPA-STRUCT-004` 的初始 inventory 标签虽为 `HISTORICALLY_SUPPORTED`，但引文、年代和流派栏均待核验，也未进入 audited IDs。本批保留整行旧快照，将 R4 总体记为现代组合；新增 `HPA-STRUCT-013` 坐标规则与 `HPA-STRUCT-014` 工程身份规则。这是首次正式范围裁决，不推翻既有 R4 已完成历史判定，也不新增缺陷编号。

### 1. 现代讲义支持的坐标

王亭之《中州派紫微斗数初级讲义》的公开传录，在“对命盘之基本认识”第 10 条给出子宫例：本宫子，三合伙伴辰、申，对宫午。相邻条目有不同简写：三方可指含本宫的三合组，也可指本宫以外的两个伙伴；四正可在句中缩指补入的对宫。应由明确例子与句法决定范围，不能只按“三”“四”的字面数字计数。

| 机械对象 | 相对坐标 | 当前 R4 对象 |
|---|---|---|
| 本宫 | 0 | frame origin |
| 三合伙伴 | +4、+8 | trine partner pair |
| 含本宫三合组 | 0、+4、+8 | trine group |
| 对宫 | +6 | opposition axis |
| 四宫整体 | 0、+4、+6、+8 | frame 的四宫并集 |

“左右隔三宫”以三个间隔宫解释，目标位移为四格；明确子宫例排除直接套用 ±3。传录邻章以“三会局”称申子辰等四组，本批只按所列成员桥接到三合坐标，不能把所有“三会”都改名为“三合”，也未裁决该字形是 OCR、排印还是原文用词。

坐标匹配支持 `HPA-STRUCT-013=SUPPORTED_BUT_SCHOOL_SPECIFIC`，只说明这份现代中州传录支持当前机械范围，不声明各派都采用相同术语定义。未引入吉凶、强弱、冲动或预测含义。

### 2. 古籍术语见证与年代缺口

现代整理/传录《捷览》的《定男女竹罗三限》《斗数发微论》，以及维基文库《全书》卷一对应赋论，可见三方、四正用语。所审片段未逐一列出四宫地址，因此不能由术语出现就证明完整 R4 定义，更不能由托名作者或网页年代倒推宋代起源。

1581《捷览》版本身份沿用既有书目审计；本批没有取得新影印目标页。南阳堂公开 PDF 地址返回 403，不作为原文不存在的证据。星侨目录核对了现代讲义书名、作者、出版社及 334 页；传录页码流为 224 页，二者具体印次尚未绑定。作品形成、刊印、实物与数字层年代均保留未决，不把本次访问日期当数字化日期。

### 3. 软件封装与既有 S04 修正

R4 的六个去重对宫轴、四个三合组、十二个主题 frame、稳定键、R2 父 hash、不可变 schema 与中性引用属于现代工程约定，`HPA-STRUCT-014=MODERN_COMPATIBILITY_ONLY`。源文件 hash 能确认字节身份，不能证明历史权威。

Issue #194 已对 S04 后六行作前缀修正，旧冲突行仍逐字保留。本批依据当前有效优先级回放，不重新修改 S04，不把旧项目整理表冲突升级成古籍异说。

### 4. 回放、账本与后续门

独立列出十二宫名表，对实际 compiler 回放全部 **12 个旋转 × 12 个主题宫＝144 个 frame**，检查三合伙伴、对宫、坐标、组引用及计数；跨旋转合计 72 个轴对象、48 个三合组对象。输入为合成 R2 几何，不能宣称是 144 个本命历法盘。既有 R2/R4 完整链路与冻结源测试另行运行。

Matrix **212→214 rows、192→195 audited、10 missing-product rows**；来源缺陷 **18/18**，排盘算法缺陷、重开与候选折叠均 **0**。R4 全部源码、schema 与 S04 blob 逐一锁定不变。没有新实体见证或已证直接承袭，`TRANSMISSION_IMPACT=NONE`；本批训诂桥接保存在研究记录，不虚增传承边。

下一门 **12MX：R6 气数位**。R4 最早完整定义与具体版本、12MV 岁前异名与将前早期出处继续保留。原《文物》1951 恢复支路维持暂停，三项直接原文目标仍未审读。

研究记录：`docs/research/ZIWEI-R4-SOURCE-PHILOLOGY-SCOPE-AUDIT-R1.json`。
回放记录：`docs/research/evidence/batch-12mw/r4-geometry-replay.json`。

来源：[现代讲义传录](https://pdfcoffee.com/-3994-pdf-free.html)、[讲义书目](https://www.ncc.com.tw/books/goods.php?id=4718)、[《捷览》整理传录](https://shixingji.club/public/ziweidoushujielan)、[《全书》卷一传录](https://zh.wikisource.org/zh/紫微斗數全書/卷一)。传录均不替代物理字形权威。

验证：新增 5 项、既有 R4 12 项、S04 修正 6 项专项测试通过；全量 1907 项测试通过，通用 verify、五项门禁、凭证检查及工作台/HTTP 两项冒烟均通过。发布后仍须核对新 HEAD 的全部 push 工作流与主 CI 完整测试步骤。
