# Fusion Chart Historical Provenance Audit R1 — Batch 12NI

## HPA-ZT-016 Self/inward transformation direction：自化／向心化方向来源、术语与 formalization gate 审计

Status: **AUDITED / NOT_YET_FORMALIZED RETAINED / MODERN SCHOOL WITNESSES SCOPED / NO SELECTOR RELEASE / NO ALGORITHM REOPEN**

本批审计 `HPA-ZT-016`。结论不是“方向不存在”，而是：当前证据可以确认现代自化方向方法族与相关术语真实存在，却还不足以把任何一套 `same/opposite palace -> outward/inward` 关系发布成唯一、版本化、可重放的确定性 selector。

### 1. 当前产品已经知道什么

已发布的 palace-stem transformation topology 可以确定性生成十二宫 × 四化 = 48 条目标拓扑，并把每一条归为：

- `SAME_PALACE`
- `OPPOSITE_PALACE`
- `OTHER_PALACE`

这些是几何事实，不是方向语义。

现有产品和测试继续明确禁止：

- `SAME_PALACE -> OUTWARD_DISSIPATION`
- `OPPOSITE_PALACE -> INWARD_RECEPTION`

Workbench 也不得自行生成 `OUTWARD_DISSIPATION / INWARD_RECEPTION` 或 `SELF_* / OPPOSITE_*` 方向标签。

### 2. S08 能证明什么、不能证明什么

S08 项目研究语料保留：

`SOURCE_FAMILY_ID=S08-SRC-ZHONGZHOU-TRANSFORMATION`

`SOURCE_ORIGINAL_FILENAME=中州派四化曜.txt`

并在归一化层定义：

- `SELF_TRANSFORMATION_DIRECTION_ENUM=OUTWARD_DISSIPATION|INWARD_RECEPTION`
- `SELF_TRANSFORMATION_KIND_ENUM=SELF_*|OPPOSITE_*`

但这不能直接作为历史/流派 selector 权威。原因有二：

1. S08 按当前研究政策属于 **project research corpus**，不是因文件名而天然正确；
2. S08 自己保留 `FINAL_RELEASE_RUNTIME_PROOF_STATUS=NOT_PROVEN`，而且在已恢复 RAW 中，本批未找到能直接闭合 `向心力 / 離心力 / 視同自化 / 本宫宫干 / 对宫宫干` 的精确 selector 词组。

因此“项目归一化枚举存在”与“来源已经证明机械方向公式”必须分开。

### 3. 许铨仁现代方法族：存在，但还不能直接编码

2013 再版《紫微斗數命理學正解(一)》的公开书目可确认：

- 作者：許銓仁；
- 340 页；
- 第三章包含“飛宮四化象理念闡微與理則詮釋”；
- 紧接“自化理念之闡微及象的分類與總彙”。

这证明现代出版物中确有系统化的飞宫/自化方法，但公开书目没有暴露目标页正文。

许铨仁监制的公开教学站可进一步确认现代“欽天四化”教学身份；仍未在公开索引面直接取得目标 selector 原文。

一个标为许铨仁高级班第27集的**二手录音文字整理**则明确写出：

- “自化与视同自化（离心力与向心力）”；
- “A宫自化相当于离心力”；
- “A宫视同自化……相当于向心力”。

这对定位方法非常重要，但它仍是二手转写：原录音、图示中的 A/A″ 坐标与纸本/讲义页没有在本批独立绑定，所以不能直接升格为 release-grade selector。

### 4. 训诂与术语冲突

当前现代资料至少出现两种命名结构：

1. `自化 = 离心`，`视同自化 = 向心`；
2. 把 `向心自化 / 离心自化 / 视同自化` 写成三个并列类别。

所以：

`DIFFERENT_WORDING_SAME_MECHANICAL_RULE`

目前**不能**直接宣告成立；也不能把所有“向心”“视同”“对宫化入”无条件合并。

必须先闭合：

- 原始 source palace；
- source palace stem；
- target star；
- target palace；
- same/opposite 判断；
- 箭头/方向的语义；
- `自化` 与 `视同自化` 的名称桥；
- 时间层作用域；
- 版本/流派归属。

### 5. 为什么本批不新增候选

当前不是“两套完整可执行 selector 已经对立”，而是：

- 一套项目归一化对象模型；
- 一组现代流派的书目与教学身份；
- 一个有价值但未完成原始对象校验的二手转写；
- 现代网络资料存在术语拆分差异。

此时贸然新增 `SAME->OUTWARD / OPPOSITE->INWARD` candidate，会把“有线索”伪装成“机械规则已经闭合”。

因此本批：

- 不新增 runtime selector；
- 不新增 direction candidate family；
- 不选 winner；
- 不修改 48 条 topology；
- 不修改四化表；
- 不重开确定性产品。

### 6. 审计结论

`HPA-ZT-016=NOT_YET_FORMALIZED`，但该行现在已经是**完成审计后的未决状态**，不是“尚未研究”。

Matrix rows **220**；audited **212→213**；missing-product rows **10**。Provenance defects 保持 **29/29**；chart algorithm defects / reopens / candidate collapses 均为 **0**。

只有在取得 edition-bound 目标页、原始录音/讲义图示或等强度的一手 school manual，并能完整重放 selector 后，才允许把方向从 `NOT_YET_FORMALIZED` 升级为 source-scoped candidate 或 released fact。

### 7. Transmission impact

`transmission_impact=DEFERRED_NO_EDGE`。

本批已经把许铨仁/欽天四化现代方法族从“泛称现代说法”缩小到具体作者、出版物与教学体系，但没有证据证明 S08 的 `中州派四化曜.txt` 直接来自许铨仁体系，也没有闭合“向心/视同自化”术语的唯一传承关系。因此不制造传承边。

下一门 **12NJ：HPA-COMB-001 Shared time credential**。

研究记录：`docs/research/ZIWEI-SELF-INWARD-TRANSFORMATION-DIRECTION-SOURCE-SCOPE-AUDIT-R1.json`。  
证据记录：`docs/research/evidence/batch-12ni/ziwei-self-inward-transformation-direction-source-scope.json`。
