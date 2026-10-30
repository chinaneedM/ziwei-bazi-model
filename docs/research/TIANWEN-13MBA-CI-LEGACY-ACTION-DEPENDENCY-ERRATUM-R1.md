# 天问 13MBa｜13MB 兼容校验补遗

本次仅修复 CI 验证脚本/测试工作流，依据 13MB exact-HEAD 的失败日志：

- `13LP` 与 `13LV` 仍把旧批次标签绑定到实时 `next_action`，改为审计前向修订快照；
- `13ED` 的历史 D30 词面验证按不可变 `previous_next_action` 保留，仍独立验证本体原图 ROI SHA 和 `null` 历史数值；最新动作必须与当前状态版本和最后证据修订对应；
- 两个批量 `test_tianwen_13l*.py` 工作流本来没安装 `Pillow` 和 `beautifulsoup4`，补入依赖；
- 13MB 专用 workflow 启用 `fetch-depth: 2`，满足 `--check-parent` 原台账防回退校验；
- 13IS 负向测试改为直接伪造 `source_controls` 中的未决原始数值，必须 fail，而非删除已经不存在于 live 最新行动的历史用词。

以上不是新原字、版刻或历算闭合，不调整 Matrix、来源注册、传承谱、P0 状态，亦不更动闭合的排盘产品。
