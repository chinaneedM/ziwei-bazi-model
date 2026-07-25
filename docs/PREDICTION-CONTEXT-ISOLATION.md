# 正式预测上下文隔离门禁

正式预测使用`config/prediction-tool-policy.json`与
`FORMAL-PREDICTION-ACCESS-CONTRACT-V1`。策略是默认拒绝、失败关闭。

预测阶段唯一允许的工具类型是`GITHUB_FETCH_FILE`，且仓库必须是
`chinaneedM/ziwei-bazi-model`、引用必须是`main`。可读范围由当前
`training/state.json`动态解析：

- `training/state.json`
- `chat-input/current.json`
- `sources/canonical/`及其冻结manifest
- 当前`current_model_release`文件及该发布实际引用的patch
- 当前推理核心、运行治理和必要配置

以下来源和操作硬性禁止：

- File Library、聊天附件、历史上传
- Personal Context、跨对话记忆、旧回复
- 仓库搜索、目录枚举、提交、历史、差异或旧分支读取
- 旧预测、旧揭盲、旧诊断、评分、复盘、learning-ledger
- answer-vault、答案映射、答案密钥及其他答案相关对象

任何违规都必须在预测与`start_round`之前终止。活动案例转为污染开发参考，
对应轮次记录为`PRE-FREEZE_CONTAMINATED_NOT_EXECUTED`；不得冻结、评分、
计入首次盲测、加入学习证据或保存预测方向。

`fortune-train verify`会校验策略完整性、动态白名单、当前Chat输入包和状态一致性。
回归测试同时覆盖允许路径以及File Library、附件、Personal Context、旧模型发布、
训练历史、答案对象和非`main`引用的拒绝行为。
