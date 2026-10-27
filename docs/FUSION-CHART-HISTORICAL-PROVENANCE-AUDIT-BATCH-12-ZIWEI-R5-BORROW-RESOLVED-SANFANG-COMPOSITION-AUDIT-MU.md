# Fusion Chart Historical Provenance Audit R1 — Batch 12MU

## R5 借星后三方四正：软件组合与上游历史权威分开

Status: **HPA-STRUCT-005 MODERN_COMPATIBILITY_ONLY / NO ALGORITHM REOPEN**

R5 把 R3 的借星成员结果与 R4 的三方四正命名身份连接为可查询视图。本批确认这层软件组合的规则和边界，不把整个组合认定为一条独立古法。

### 1. 两种身份分别保留

每个本命盘输出 12 个 frame、48 个 member reference，成员依次为 `SELF/+0`、`TRINE_PLUS_4/+4`、`OPPOSITION/+6`、`TRINE_PLUS_8/+8`。

R3 的 `structure_physical_key` 保留物理解析身份；R4 的 `axis_key/group_key` 保留命名结构身份。R5 不复制星曜或四化 payload，不再借星，不建立新轴或新组三方身份，也不把 frame 数量算成独立证据贡献。未能取得借星来源时，组合单元保持空来源引用。

### 2. 历史证据边界

R3 的中州派借星机械规则已在 12MT 分拆审计。R4 的 `HPA-STRUCT-004` 仍有初始 inventory 的 `HISTORICALLY_SUPPORTED` 标签，但尚未进入 `audited_row_ids`，其原文、年代/版本和流派归属仍待核查。本批不修改这一旧记录，也不以 R5 软件校验替它完成历史审计。

“三方四正”在这里是已发布 R4 的命名结构接口；`TRINE_PLUS_4/+8` 是现代坐标标签，不推出左/右合宫、强弱、格局或吉凶解释。两个上游规则的来源作用域随各自 computation lineage 保留，不虚构逐 member-reference 的 source-root atom 映射。

### 3. 机械回放与限制

采用 1994 年公历 12 个月、每月 17 日、12 个双时辰内的 00:30–22:30 时间点、男女两种输入，共 **288 个北京样本盘**。这是样本域覆盖，不是全部历法、出生日期或历史规则穷举。

共核对 **3456 个 frame、13824 个成员引用**，其中直接物理成员 11680、借星成员 2144。以原始地址模十二加法独立核对坐标，并分别比较 R3 物理键、R4 轴/组键、来源地址及上游对象不变性。双空/未知借星来源另用 composer 单元的合成 fixture 检查，不冒称有效本命盘全链路样本。

R5 重新计算上游存储事实的 hash、检查 profile/integrity 版本和同一 R2 lineage，拒绝旧 PASS/旧 hash 掩盖的篡改及跨盘组合。它没有从原始 BirthInput 独立重建 R3/R4：hash 一致性不等于新的一手来源或历史算法证明。支持时间层仍为 `NATAL`。

### 4. 主 CI 修复

启动提交 `e1c61924` 的主工作流 `37223018133` 有且仅有一个测试失败：流派限定规则总数被写死为 18，12MT 新增三条后实际为 21。测试现按矩阵行统计核对 inventory，保留旧批次的历史计数快照；不改排盘算法。

### 5. 账本与下一门

Matrix **210 rows、189→190 audited、10 missing-product rows**；来源缺陷维持 **18/18**；算法缺陷、算法重开、候选折叠均 **0**。R5 runtime/profile/schema/hash 不修改。没有新历史见证，`TRANSMISSION_IMPACT=NONE`，传承图不新增边。

下一门 **12MV**：剩余 `IMPLEMENTATION_REVIEW_REQUIRED` 行 `HPA-ZIWEI-011` 博士/将前/岁前三环，分开三套锚点、方向、时层与既有审计的覆盖范围；之后优先补 R4 的历史出处与训诂缺口。

原《文物》1951 恢复支路继续暂停，须有实质新增的合法访问路线才能重开；三项直接原文目标维持未审读。

研究记录：`docs/research/ZIWEI-R5-BORROW-RESOLVED-SANFANG-COMPOSITION-AUDIT-R1.json`。
回放记录：`docs/research/evidence/batch-12mu/composition-replay.json`。
