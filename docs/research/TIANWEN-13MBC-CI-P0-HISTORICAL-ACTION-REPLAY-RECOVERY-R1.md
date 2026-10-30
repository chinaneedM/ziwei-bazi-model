# 天问 13MBc｜高优先级 CI 原史料回放续修

13MBb exact-HEAD 全量 CI 的 175 步首次报错在 `verify-ncl03130-solar-p73-technical-headings-13ef.py`，原因仍为旧批次验证把历史 D30 标签要求保存在实时 `next_action`。从现行 CI 剩余脚本中逐项核实到同型依赖，前向修复：

- 13EF–13EU 的旧 D1–D6、四分、初度、NULL 和 D30 文本改由 `historical_action_view(issue)` 从已有历史快照证明；
- 13EV–13EY 的韩方、馆藏及原像来源限定标签以同样方式追认；13FA–13FB 的 GK05553/GK5553 只验证曾有证据登记；
- 未放宽被独立检验的原图 SHA、像素位置、版本边界和未知数值归零门禁，亦不改动实时 `TW-OPEN-0005.next_action`；
- 本工作单元只修复 CI 兼容，不发明新历史证据、降低原古籍权限、关闭风险，或重开确定性排盘。

研究状态仍沿用 13MA / state v1.965.0；当前 BSB 第一册章三十五原叶的数行没有被定位或裁决。以修复后 exact-HEAD Actions 为验收依据。
