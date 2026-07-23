# GitHub Issue 自动训练通道

> 当前通道在107例答案完成加密导入并切换案例库控制器前保持停用；不得用旧5例状态继续提交。

该通道不消耗ChatGPT Work额度。Chat负责当前案例预测、揭盲复盘和生成提交单；GitHub Actions负责冻结、用加密答案复核、更新跨案连续达标数，失败时激活通用规则并加入间隔复训队列，然后切换到下一新案。

## 每案操作

1. 新开Chat，使用 `docs/CHAT-WORK-RUNBOOK.md` 中的固定预测口令。
2. Chat冻结全部预测后，在同一对话提供答案字母串。
3. 要求Chat生成 `TRAINING-ISSUE-PACKET-V2`。
4. 打开：<https://github.com/chinaneedM/ziwei-bazi-model/issues/new?template=training-round.md>
5. 在正文框按 `Ctrl+A`、`Ctrl+V` 粘贴整份JSON。
6. 保持标题以 `[TRAINING ROUND]` 开头，直接提交。

## V2提交单结构

每道预测必须带有揭盲前冻结的标签：

```json
{
  "schema": "TRAINING-ISSUE-PACKET-V2",
  "round_id": "ROUND-003",
  "case_id": "当前安全包中的案例ID",
  "predictions": [
    {
      "question_id": "Q1",
      "top1": "A",
      "top2": "B",
      "reasoning": "冻结的完整理由与最强反证",
      "evidence": ["S04", "S08", "S16", "S17"],
      "strongest_counterevidence": "最强竞争项及其成立条件",
      "confidence": 72,
      "question_profile": {
        "topic_tags": ["MARRIAGE_RELATIONSHIP"],
        "subject_tags": ["SPOUSE_PARTNER"],
        "time_scope_tags": ["CURRENT_STATUS"],
        "endpoint_tags": ["RELATIONSHIP_STATUS"],
        "reasoning_skill_tags": ["SUBJECT_ENTITY_ROUTING", "RELATIONSHIP_SEQUENCE"],
        "source_routes": ["S04", "S08", "S16", "S17"],
        "applied_rule_ids": []
      }
    }
  ],
  "expected_result": "PASS"
}
```

失败轮必须在最外层增加 `learning_release_id` 和V2规则补丁：

```json
{
  "learning_release_id": "MODEL-LEARNING-003",
  "learning_patch": {
    "learning_type": "REASONING_STRATEGY",
    "rules": [
      {
        "rule_id": "RULE-SEMANTIC-NAME-001",
        "topic_tags": ["MARRIAGE_RELATIONSHIP"],
        "reasoning_skill_tags": ["EVENT_ENDPOINT_CLOSURE"],
        "source_routes": ["S04", "S16", "S17"],
        "statement": "通用规则陈述",
        "applicability": "适用条件",
        "limits": "限制",
        "counterexamples": "反例",
        "capability_ceiling": "能力上限",
        "source_basis": "来源依据",
        "trigger_conditions": "触发条件",
        "decision_procedure": "决策步骤",
        "stop_conditions": "停止条件"
      }
    ]
  }
}
```

上面两个片段只是结构说明。实际操作时只复制Chat生成的一个完整JSON，不要手工拼接或修改。

## GitHub自动执行

- 只接受仓库所有者创建的训练Issue；
- 确认当前案例尚未完成且没有其他活动轮次；
- 验证每题标签均来自固定taxonomy；
- 验证 `applied_rule_ids` 在预测前已经存在；
- 冻结预测后才解密答案；
- 复核PASS/FAIL并记录题级汇总；
- 失败时拒绝含案例答案映射的规则；
- 失败时连续次数归零并保持当前案例；
- 通过时连续次数加1，达到3次才完成案例；
- 不修改 `sources/canonical/`；
- 运行完整验证与测试；
- 刷新当前或下一案例的`chat-input/current.json`；
- 留下不含答案的结果并关闭Issue。

## 出错处理

- Issue成功并自动关闭：本轮闭环完成；按日程进入下一新案或已到期的间隔复训案。
- Issue失败：仓库不会提交半成品。根据Actions错误重新让Chat输出完整V2 JSON，再新建一张Issue。
- 不要在预测前上传答案，也不要把答案或密钥放入Issue。
