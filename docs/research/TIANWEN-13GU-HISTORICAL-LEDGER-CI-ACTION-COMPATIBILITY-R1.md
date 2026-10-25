# 13GU — 恢复旧源页门禁与当前行动的交接兼容性

## 新 HEAD 上的直接故障

13GS `e0847b1` 原图几何专项验证成功。随后 13GT `f10a8b9` 恢复部分检查（例如 13GE、13GG），但旧 13FZ/13GF/13FL/13FM/13FN/13FO 等精确 HEAD 工作流继续失败：其旧验证器在当前 `TW-OPEN-0005.next_action` 中查找历史源范围字面锚点，例如 “13FZ CURRENT ACTION:”、 “ARCHIVED 13GF PRIOR ACTION”、国图/奎章阁/GK 多书目范围与 D1–D6 六点列表，而 13GT 的简短现行行动说明只承载最新几何任务。另外，13BJ 检查要求当前行动的末次已登记 `ISSUE_REVISION` 记录与行动前缀一致。

## 本次非破坏性恢复

- 现行任务仍在 `13GU CURRENT ACTION:` 顶部明确书写：下一步人工复核 NLC 源页十四日日期、四分与初度栏、原末字、y822 以下和相邻技术栏；必要时走馆方批准的高分辨率原件。
- 将原已留存于 13GT 历史事件 `previous_next_action` 的完整 13GR 历史作用域**逐字附在现行动作末尾**，并显式标成 **ARCHIVED SOURCE-SCOPED HISTORICAL GATES / NOT NEW FINDINGS**。它们不可再视作本轮的新发现或开启旧源独立复本投票。这不是恢复旧研究优先级，而是维持原有机器兼容合同。
- 将本轮动作更名与完整先前 13GT 动作以标准追加 `ISSUE_REVISION` + `revision_id=TW-OPEN-0005-13GU-...` 留存，避免历史版本断链。此前 13GS 与 13GT 事件只追加不覆写。
- 状态号、遗漏审阅 checkpoint 与当前研究焦点同步到 `1.850.0`。保留十一项风险、Matrix 222/222、来源 761、传承谱 252/238、确定性 R1 CLOSED。

未获得新的原字、单位、原叶与物理证本。原 NLC D9 / D14 / D30 均 NULL；D5 〇/五与 G893 六组仍 OPEN；13EI RETRACTED；无候选坍缩或算法重开。必须以本次 exact-HEAD Actions 的实际结果决定 CI 是否闭合。
