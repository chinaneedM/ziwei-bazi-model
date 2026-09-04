# Ziwei Structural Runtime V2-R7 — 一六共宗

R7 是 R2 相对十二宫框架上的只读、source-backed 命名关系投影。唯一几何定义为 `relative_ordinal=6`、`clockwise_offset=7`；R7 不重新计算宫位，也不修改 R3–R6。

## S04 来源闭合

R7 绑定 S04 技法索引 `HL_ONE_SIX_COMMON_ROOT`。`HL-C-0008-04/05` 明确定义命宫逆数第六位为疾厄宫并命名为“一六共宗”；`HL-C-0314-04..06` 以财帛为本宫、田宅为第六位，证明该关系按论事本宫的相对第六位使用。运行时因此只读取 R2 每个本宫的 ordinal 6 事实，并保持冻结 V1 宫序。

十二个有向身份映射依次为：命→疾厄、兄弟→迁移、夫妻→交友/奴仆、子女→官禄、财帛→田宅、疾厄→福德、迁移→父母、交友/奴仆→命、官禄→兄弟、田宅→夫妻、福德→子女、父母→财帛。仓库 canonical ID 中“交友/奴仆”继续使用 `SERVANTS_FRIENDS`。

## 边界

S04 的技法索引明确冻结 `direct_event_permission=NO` 与 `direct_endpoint_permission=NO`。R7 因而只输出 `DIRECTED_RELATIVE_SIXTH_PALACE_IDENTITY_ONLY`，不把关系直接解释为同强度、同吉凶、同事件、同终点或任一结果判断，也不读取星曜、四化、煞曜或动态层来生成结论。

R7 的 FactHash 绑定 R2 FactHash，ComputationHash 同时绑定 R2 ComputationHash、冻结 R7 profile、S04 source/technique/clause lineage 与 time layer。当前仅支持 `NATAL`。
