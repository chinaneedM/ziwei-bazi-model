# 正式预测上下文隔离门禁

正式预测使用独立启动文件`chat-input/prediction-access-contract.json`中的
`FORMAL-PREDICTION-ACCESS-CONTRACT-V1`。它必须是任何仓库检索前唯一允许的首次读取；
契约执行后才允许读取状态、当前输入、模型和配置。策略是默认拒绝、失败关闭。

预测阶段唯一允许的工具类型是`GITHUB_FETCH_FILE`，且仓库必须是
`chinaneedM/ziwei-bazi-model`、引用必须是`main`。可读范围由当前
`training/state.json`动态解析：

- `training/state.json`
- `chat-input/prediction-access-contract.json`
- `chat-input/current.json`
- 与`current.json`哈希绑定的`chat-input/runtime-model.json`
- 冻结组装时才读取的`chat-input/prediction-row-template.json`
- `sources/canonical/`及其冻结manifest
- 当前`current_model_release`文件及该发布实际引用的patch
- 当前推理核心、运行治理和必要配置

外部/项目来源不需要也不允许运行时使用。`knowledge-workbench/`仅在构建时参与编译；
CHAT直接读取`chat-input/runtime-model.json`中的knowledge cards，不读取workbench。

以下来源和操作硬性禁止：

- File Library、聊天附件、历史上传
- Personal Context、跨对话记忆、旧回复
- 仓库搜索、目录枚举、提交、历史、差异或旧分支读取
- 旧预测、旧揭盲、旧诊断、评分、复盘、learning-ledger
- answer-vault、答案映射、答案密钥及其他答案相关对象

任何违规都必须在预测与`start_round`之前终止，对应轮次记录为
`PRE-FREEZE_CONTAMINATED_NOT_EXECUTED`；不得冻结、评分、计入首次盲测、
加入学习证据或保存预测方向。读取了答案、旧预测或其他会污染案例本身的对象时，
活动案例转为污染开发参考；仅违反“契约必须首先执行”的启动顺序且未泄露答案时，
只作废该轮并为同一案例生成新的干净轮次。

隔离必须通过强绑定控制器执行：

```bash
fortune-train quarantine-current FORMAL-ROUND-000 CASE-000
fortune-train invalidate-current-round FORMAL-ROUND-000 CASE-000
```

控制器仅在轮次、案例与当前`READY_FOR_ROUND`首次盲测完全一致且案例没有任何
训练效果时执行。它以单一事务更新开发分区、正式组、状态和Chat输入；验证失败
则全部回滚。远程操作使用仓库所有者创建的`[PREDICTION CONTAMINATION]` Issue，
正文可以是`PREDICTION-CONTAMINATION-REPORT-V1`四字段JSON，或以
`round_id/case_id/status/reason`四字段机器头开头、空行后附行政说明。仅启动顺序违规
可把`round_id`写为`RESOLVE_FROM_MAIN_CURRENT_ACTIVE_ROUND`，控制器会从本次检出的
`main/training/state.json`解析唯一当前轮次；真正的案例上下文污染仍必须提交显式轮次，
防止误隔离。自动流程不需要、不读取也不接受答案、预测方向或评分字段。

`fortune-train verify`会校验策略完整性、动态白名单、当前Chat输入包和状态一致性，
并验证运行模型与模板哈希、运行包字符预算、14项不可删减推理主题、无证据配额、
全选项比较和题级渐进检索路由。
回归测试同时覆盖允许路径以及File Library、附件、Personal Context、旧模型发布、
训练历史、答案对象和非`main`引用的拒绝行为。完整预测冻结后才可转换到
`POST_PREDICTION_HANDOFF`；该阶段只允许一次`GITHUB_CREATE_ISSUE`，其他Git写操作
继续默认拒绝。
