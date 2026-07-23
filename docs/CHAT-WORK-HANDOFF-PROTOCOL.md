# Chat→Work 机器交接协议

## 目标

跨模式切换不再依赖对话记忆。每轮冻结预测先写入一个无答案的 GitHub 交接 Issue，Work 仅依据当前安全启动包与该交接凭证继续评分。

## 唯一凭证

标题：

```
[PREDICTION HANDOFF] <ROUND_ID> <CASE_ID>
```

正文：

```json
{
  "schema": "CHAT-WORK-PREDICTION-HANDOFF-V1",
  "binding": {
    "case_id": "<current case>",
    "round_id": "<recommended round>",
    "evaluation_kind": "FIRST_BLIND or SPACED_REPLAY",
    "model_release": "<current model release>",
    "current_case_sha256": "<from current.json>",
    "current_model_release_sha256": "<from current.json>",
    "canonical_source_manifest_sha256": "<from current.json>",
    "effective_model_input_sha256": "<from current.json>"
  },
  "predictions": []
}
```

`predictions`必须是 Chat 已公开冻结的完整逐题数组。交接 Issue 不得包含答案、评分、复盘、预期 PASS/FAIL 或学习补丁。

## Work 接受门禁

Work 必须同时满足以下条件才可评分：

1. `main/chat-input/current.json`仍指向同一案例、轮次和模型；
2. 只有一个对应的开放交接 Issue；
3. Schema、案例、轮次、评估类型、模型发布及全部绑定哈希相同；
4. 题目覆盖完整且每题只出现一次；
5. Top1/Top2、理由、证据、反证、置信度、`question_profile`及`rule_attribution`齐全；
6. `evidence`无重复且均存在于同题`source_routes`；
7. 不存在答案、评分或学习字段。

任一项失败必须在答案访问和评分之前停止。禁止使用 Personal Context、聊天摘要或旧回复补齐冻结预测。

## 单次 Work 接管

Chat 创建唯一交接 Issue 并返回编号后，用户只需切换一次 Work。Work 在同一会话中：

1. 生成一次性 RSA 公私钥，只把公钥提交给 `handoff-score-probe`；
2. 工作流临时冻结并用仓库 Secret 解密评分，不提交任何状态；
3. 逐题复核以该次公钥加密后回传，公开 Issue 只保存密文和无答案汇总；
4. Work 解密复核；PASS 直接生成正式提交，FAIL 在同一会话完成通用复盘和学习补丁；
5. 创建唯一 `[TRAINING ROUND]` Issue，等待正式控制器验证、提交 `main`，随后关闭交接 Issue。

一次性私钥不得进入 Issue、仓库、Actions 日志或长期文件。交接 Issue 必须已经是控制器标准预测格式，不能在揭盲后补写 `question_profile`、`rule_attribution`、改变 Top1/Top2 或重做推理。

`rule_attribution`必须把每个`applied_rule_id`恰好归入`decisive_rule_ids`、`supporting_rule_ids`或`counterevidence_rule_ids`之一，并填写`decision_changed`。每题最多使用6条范围匹配规则；`CHALLENGED`规则只能作为反证。

创建Issue时应直接使用`chat_work_handoff_contract.handoff_payload_template`，只填入已冻结的`predictions`，不得手工重抄绑定哈希。

## 训练提交字段

`TRAINING-ISSUE-PACKET-V2`只允许：

- `schema`
- `round_id`
- `case_id`
- `predictions`
- `expected_result`
- FAIL 时的`learning_release_id`和`learning_patch`

`evaluation_kind`、`accuracy`、`correct_count`、`top2_coverage`、`learning_release`、`next_case_id`、`next_status`都是结果字段，严禁回填输入。PASS 严禁携带任何学习字段。

## 回收

训练成功发布后关闭交接 Issue，并在结果中互相链接。无效或过期交接只关闭，不进入训练统计。
