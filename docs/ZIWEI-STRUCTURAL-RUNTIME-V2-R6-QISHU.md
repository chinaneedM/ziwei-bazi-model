# Ziwei Structural Runtime V2-R6 — 气数位

R6 是 R2 相对十二宫框架上的只读、source-backed 投影层。唯一几何定义为 `relative_ordinal=9`、`clockwise_offset=4`；R6 不重新计算宫位，也不修改 R3–R5。

## S04-QS 冻结映射

`S04-QS-01..12` 依次为：命→官禄、兄弟→田宅、夫妻→福德、子女→父母、财帛→命、疾厄→兄弟、迁移→夫妻、交友/奴仆→子女、官禄→财帛、田宅→疾厄、福德→迁移、父母→交友/奴仆。

运行时沿用仓库 V1/R2 的 canonical designation ID，因此 S04 的“交友宫”在当前排盘域中绑定为 `SERVANTS_FRIENDS`，不创建新 designation。

## 边界

S04 定义气数位只表示“现实承接”，不是成功宫、失败宫、评分宫或终点宫。R6 因而只输出气数位置事实、固定承接说明与 `S04-QS-*` provenance，不根据禄权科忌、煞、冲动等生成结果判断，也不赋值 `RESULT_*` 角色；后者仍由后续合法证据层处理。

R6 的 FactHash 绑定 R2 FactHash，ComputationHash 同时绑定 R2 ComputationHash、冻结 R6 profile 与 time layer。当前仅支持 `NATAL`。
