# Fusion Chart Historical Provenance Audit R1 — Batch 12MZ

## R8 邻宫：双侧物理几何、古代夹法前史与现代结果语义防火墙

Status: **R8 DECOMPOSED / MODERN ZHONGZHOU GENERIC NEIGHBOR GEOMETRY SUPPORTED / PREMODERN SPECIFIC FLANK PATTERNS ATTESTED / NO ALGORITHM REOPEN**

本批审计真正对象是 `HPA-STRUCT-008 = R8 邻宫 bilateral geometry`。12MY 的 next-gate/current-focus 曾误写成“R8 太极点/主题宫 composition”；Matrix 与 runtime 自始未错。本批以 `PROV-DEFECT-019` forward-only 记录并修复该研究元数据错误，保留 12MY 历史快照而不回写历史批次。

`HPA-STRUCT-008` 初始 inventory 标签为 `HISTORICALLY_SUPPORTED`，但来源原文、年代、流派与现代工程边界未审。本批保留旧行快照，将父规则拆为 `HPA-STRUCT-019`（邻宫双侧坐标）与 `HPA-STRUCT-020`（现代工程语义闭包）。

### 1. 现代中州派直接定义通用“邻宫”

S05 恢复母本的中州派基础术语来源写明“邻宫”，并定义为本宫两侧相邻的两个宫垣；子宫作为本宫时，丑、亥即为邻宫。现代王亭之《中州派紫微斗数初级讲义》公开传录与《安星法及推断实例》received text 都保存同一术语体系；后者把“相夹”另外定义为两星曜分别位于本宫两个邻宫。

这直接支持**通用几何关系**，但证据属于现代中州派学校材料，不能倒推为所有紫微流派共同术语。因此 `HPA-STRUCT-019=SUPPORTED_BUT_SCHOOL_SPECIFIC`。

### 2. 古代《全书》有“夹”法，但不等于已证明通用“邻宫”定义

《紫微斗数全书》received text 有“夹贵格”“夹败格”“三夹命凶六夹吉”等明确的夹法传统，说明用两侧星曜形成“夹”的观念并非现代创造。

然而，本批已审的仓库明代《全书》来源层没有找到可直接等同于现代中州派“邻宫＝任一本宫左右两侧”的通用定义；公开 received 文本的具体夹格也不能自动扩张成一条抽象的十二宫 bilateral API 规则。因此古代夹法只作为**历史前史/语义邻接见证**，不作为 R8 通用 term/coordinate 的直接古代来源，也不建立“《全书》→王亭之术语表”的传抄边。

### 3. R8 坐标与 144 旋转回放

R8 对每个局部本宫取两个 R2 事实：

- 逆时针邻宫：`relative_ordinal=2`、相对角色 `SIBLINGS`、物理 `clockwise_offset=11`；
- 顺时针邻宫：`relative_ordinal=12`、相对角色 `PARENTS`、物理 `clockwise_offset=1`。

这里的 SIBLINGS/PARENTS 是**相对于当前本宫的角色标签**，不是永久固定成本命兄弟宫/父母宫。本宫每旋转一次，两侧角色与物理地址一起旋转。

独立命名宫表回放 **12 个命宫物理旋转 × 12 个本宫＝144 个 bilateral facts / 288 个 neighbor endpoints**，全部与 runtime 一致。子位实例严格得到亥、丑两侧物理邻宫。

### 4. “邻宫存在”不等于“夹宫/夹格成立”

现代中州派文本把“邻宫”作为位置定义，把“相夹”作为进一步的星曜条件关系；古代《全书》也有具体夹贵/夹败格。当前 R8 刻意只保留 `BILATERAL_ADJACENT_PALACE_GEOMETRY_ONLY`：

- `flank_semantics_permission=False`
- `direct_event_permission=False`
- `direct_endpoint_permission=False`
- `direct_score_permission=False`

因此“有两个邻宫”不能直接推出“某夹格成立”，更不能推出吉凶、强度、评分或事件。NATAL-only、R2 hash binding、schema/integrity 和上述 permission firewall 均属于现代工程合同，记为 `HPA-STRUCT-020=MODERN_COMPATIBILITY_ONLY`。

### 5. PROV-DEFECT-019

12MY 已完成内容本身针对 R7 正确，但其最后一条 next gate 把 `HPA-STRUCT-008` 错写为“R8 太极点/主题宫 composition”。当前 Matrix 行、R8 文件路径和 product closure 均明确它是“R8 邻宫 bilateral geometry”。本批不改 12MY 历史文档，而在 current state、12MZ research record、README 与门禁中建立 superseding correction。

这属于研究/连续性元数据错误，不是 chart algorithm defect。Provenance metadata defects **18/18→19/19**；算法缺陷、算法重开、候选折叠继续为 0。

### 6. 账本与下一门

Matrix **218→220 rows、201→204 audited、10 missing-product rows**。R8 runtime、S04/S05 相关来源字节与 R8 说明文档冻结不改。

本批不新增传承边：古代具体夹法和现代中州派通用“邻宫”定义之间没有直接传抄/师承证据，`TRANSMISSION_IMPACT=NONE`。

下一门 **12NA：HPA-STRUCT-001 R1 neutral Z12 topology**，随后再审 R2 relative-palace frame；完成 Structural R1–R8 的剩余两条基础现代层后，再回到 Matrix 中其它未审现代组合项。

研究记录：`docs/research/ZIWEI-R8-ADJACENT-PALACE-SOURCE-PHILOLOGY-SCOPE-AUDIT-R1.json`。  
回放记录：`docs/research/evidence/batch-12mz/r8-adjacent-palace-geometry-replay.json`。
