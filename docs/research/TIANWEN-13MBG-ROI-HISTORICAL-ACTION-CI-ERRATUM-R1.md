# 天问 13MBG｜13JN–13JP 数字原图 ROI 校验与历史待办字段修复

## 触发证据
GitHub `07a5944342dd8227c7d2de330262e353dc223b64` 精确 HEAD 上，`clean-training-system` run `41072845197` 总计执行 6115 项单元测试，恰有 3 项失败：
- `test_tianwen_13jn_gk5553_roi_replay_erratum.py` 要求 live next_action 含 13JM、13JN；
- `test_tianwen_13jo_gk5553_original_roi_replay.py` 要求 live next_action 含 13JN、13JM；
- `test_tianwen_13jp_gk5553_five_original_roi_replay.py` 要求 live next_action 含 13JJ、13JN、13JO。

这三个历史批次的源文件、`source_refs`、`current_focus`、`history[*].revision_id` 均保留，当前 `next_action` 合法推进到 `13MA`，不能为了旧测试通过而恢复旧任务文字。

## 修改边界

只将上述 3 个旧批次测试里的回顾性 `next_action` 文本断言替换为 `historical_action_view(issue)`，此函数仅从 live current action、现存不可变 `previous_next_action` 快照与既有历史 revision_id 读取标签。完整保留 prior image SHA 校验、裁剪像素范围、伪造数值/证人否定测试、历史修订 ID 核验以及 `CLOSED` 约束。新增独立精确测试 workflow，配合 parent-ledger 与 project continuity 校验。

科研等级未变：13JM 的 12 个坏 ROI 坐标仍不被追认；13JO 的 6 张原图 12 ROI 与 13JP 的 5 张原图 10 ROI 按各自校验记录处理；不得据此增加独立物理传本或六目标数值胜出。该提交不改研究状态、算法、Matrix 或传承图谱。下一事项仍为 13MA BSB 卷三十五原叶位置和原字。
