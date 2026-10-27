# Ziwei Structural Runtime V2-R8 — 邻宫双侧几何

R8 是 R2 相对十二宫框架上的只读、source-backed 邻宫投影。每个本宫只产生一个双侧邻宫事实：逆时针邻宫取 R2 `relative_ordinal=2 / clockwise_offset=11`，顺时针邻宫取 R2 `relative_ordinal=12 / clockwise_offset=1`。R8 不重新计算宫位，也不修改 R3–R7。

## S04 来源闭合

R8 绑定 S04 `ZZTERM-P-0018`、`ZZTERM-L-0057/0058`、闭合关系 `ZZTERM-R-0057-0058` 与术语 `ZZTERM-PAL-04`。来源明确把邻宫定义为本宫两侧相邻的两个宫垣，并以子宫的丑、亥邻宫为机械示例。运行时只读取经过校验的 R2 相邻坐标，保持冻结 V1 宫序。

## 边界

S04 对该来源冻结 `direct_event_permission=NO`、`direct_endpoint_permission=NO`、`direct_score_permission=NO`。R8 因而只输出 `BILATERAL_ADJACENT_PALACE_GEOMETRY_ONLY`，不根据邻宫中的星曜、四化、煞曜或亮度判断“夹宫/夹格”是否成立，不生成组合强度、吉凶、事件、终点或评分。完整夹宫语义仍未激活。

R8 的 FactHash 绑定 R2 FactHash，ComputationHash 同时绑定 R2 ComputationHash、冻结 R8 profile、S04 source lineage 与 time layer。当前仅支持 `NATAL`。
