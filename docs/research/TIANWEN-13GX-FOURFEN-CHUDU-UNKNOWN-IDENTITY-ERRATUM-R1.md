# 天问 13GX — 13GW「四分／初度」关系真假值的前瞻性认识论更正

## 发现的语义缺陷

13GW 源图题头范围校验为**单一电子替身上的暂读**：相邻两个竖栏视觉写作「四分」「初度」。13GW `inference_firewall.fourfen_chudu_are_mechanical_identical = false`，同时又写 `fourfen_chudu_relation_adjudicated = false`。

前一个 `false` 原设计意在阻止“证明两栏目机械等价”的无依据推广；但若被下游读取为“已经证明二者机械不等价”，就形成**未充分证明的否定结论**。这是数据语义问题，不是新发现的古籍文字。

## 前瞻性修复，不篡改已登记快照

- 保留 13GW 原始 JSON blob SHA `2e29de68387826e81d62ddaff6781e7a8a09a411` 及其所有源像素哈希、人工暂读、栏间距证据。
- 新建 13GX 有效叠加记录：`effective_fourfen_chudu_mechanical_identity = null`、`effective_fourfen_chudu_ancient_unit_identity = null`、`effective_relationship_status = UNADJUDICATED`。
- `false` 只解释为旧校验中的“不许无证合并”，**绝不是“有直接反证证伪等价”**。
- 不增支持边、不增排斥边、不新增原件见证；D14、D9、D30 古本数值与 D14 末字仍 NULL，D5「〇/五」、G893 六项目标 OPEN，13EI RETRACTED。
- 严格机器校验将防止有效关系被置成 `true` 或 `false`，或将未知误写为已建立的传承图非边。

保留图谱 252 节点、238 边、来源761、Matrix222/222、风险11、封版产品 CLOSED。下一步继续原印数字栏、源页日期/题头行位置及馆方获准高分辨率影像校勘；任何历史单位与机械等价/不等价都需要独立证据。
