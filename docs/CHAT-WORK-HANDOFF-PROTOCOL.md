# Chat→Work 机器交接协议 V2

跨模式切换不依赖对话记忆。Chat只读取当前`chat-input/current.json`，完成全部结构化推理后创建一个无答案交接 Issue；Work只依据当前安全包与这张唯一凭证继续。

## 唯一凭证

标题严格复制`chat_work_handoff_contract.issue_title`。正文直接使用机器生成的`handoff_payload_template`，Schema为`CHAT-WORK-PREDICTION-HANDOFF-V2`，包含：

- `binding`
- 选项前`blind_chart_model`
- `cross_question_consistency`
- 复训时的`replay_remediation`，首次盲测为`null`
- 完整`predictions`

不得手工填写哈希，不得省略内部推理结构，不得包含答案、评分、复盘、预期PASS/FAIL、学习补丁或密钥。

## Work接受门

Work在访问答案前必须验证：

1. `main/chat-input/current.json`仍指向相同案例、轮次、模型与评估类型；
2. 只有一个标题完全一致的开放交接Issue；
3. 全部绑定哈希一致；
4. 全案盲态模型不含选项原句或答案导向字段；
5. 每题均有语义原子化、紫微封卷、八字封卷、双轨裁决、证据账本、全选项矩阵、反转测试、置信组件和规则消融；
6. 同案所有题共享一个盲态模型并完成跨题一致性检查；
7. 不存在答案、评分或学习字段。

任一项失败必须在`start_round`之前停止，因此无效交接不会消费活动案例。禁止用Personal Context、聊天摘要或旧回复补齐字段。

## 正式训练提交

揭盲闭环使用`TRAINING-ISSUE-PACKET-V3`，在交接字段之外只允许：

- `expected_result`
- FAIL时的`learning_release_id`
- FAIL时的`MODEL-LEARNING-CORRECTION-V3`

结果字段严禁回填输入。PASS不得携带学习字段。FAIL先分类根因并选择修正类型；只有`NEW_GENERAL_RULE`能新增规则。

## 单次接管

Work用一次性RSA公钥取得私密评分结果，完成PASS提交，或在同一会话完成FAIL复盘与通用修正，再创建唯一训练Issue。一次性私钥不得进入Issue、仓库、Actions日志或长期文件。正式发布后关闭交接Issue。
