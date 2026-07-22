# 半自动命理推理训练系统

本系统不是通过重复例题修改大模型参数，而是建立一套可审计的外部推理系统：冻结 S00–S19 为知识底座，把真实选择题按主题与推理能力自动分类；揭盲后只产生不含答案映射的候选通用规则，再由未来不同案例中的相关题目验证。

## 核心训练规则

- 每个案例只允许一轮计分的 `FIRST_BLIND` 预测。
- 少于 5 题必须全对；5题及以上达到向上取整的80%记为该轮通过。该阈值只描述本轮表现，不代表整个模型成熟。
- 通过后立即进入下一未揭盲案例。
- 未通过时先生成候选通用规则，再进入下一案例；不在原案例上连续刷分。
- 同案回放可以另作诊断，但永不计入首次盲测准确率或规则验证。
- 每道题必须在揭盲前填写 `question_profile`：主题、人物、时间、现实终点、推理能力、来源路线及实际采用的规则。
- 只有预测前明确列入 `applied_rule_ids` 的规则，才会因该题结果获得支持或反证；无关题目不计证据。
- 规则至少在3个不同的后续案例中获得3次支持且支持率达到80%，才从候选状态提升为内部 `VALIDATED`。这仍是题库内经验状态，不等于科学定律。

## 两层运行权威

1. `sources/canonical/`：S00–S19 冻结原典。训练中只读，由 `sources/canonical-manifest.json` 哈希锁定。
2. `model-learning/`：模型自己的通用推理规则。不得包含案例编号、题号、答案字母、选项位置、选项原句或案例专属映射。

项目中上传的 S00–S19 只是 Git 原典的只读检索镜像；S02 `(8)` 禁用，S02 `(9)` 有效。`sources/canonical/` 被改动时仓库验证会直接失败。

## 题级学习结构

`config/question-taxonomy.json` 定义四类语义标签和推理能力标签。Chat 根据题干、选项和无答案盘面在预测前自动分类，用户不需要人工整理。

`training/learning-ledger.json` 只保存汇总证据：各主题/推理能力的首次盲测题数、Top1、Top2，以及规则在不同案例中的支持和反证计数。该文件不进入预测上下文，不含正确答案映射。

规则生命周期：

- `CANDIDATE`：由一次失败提出，尚无未来案例证据。
- `PROVISIONAL`：已在后续相关题中使用，但证据不足。
- `VALIDATED`：达到跨案例内部验证门槛。
- `CHALLENGED`：应用结果未达到支持率门槛，需要修订边界。
- `RETIRED`：停止使用。

## 每案闭环

1. Chat 只读取 `chat-input/current.json`；该文件内嵌当前未揭盲案例、标签表、当前模型规则和冻结原典清单。
2. Chat 对每题先分类，再完成紫微与八字独立推理、选项比较、最强反证和置信度。
3. 预测冻结后用户揭盲；Chat 输出完整 `TRAINING-ISSUE-PACKET-V2`。
4. 用户把整份 JSON 粘贴到“无 Work 训练提交单”。
5. GitHub 自动冻结、用加密答案复核评分、更新题级统计。
6. 未通过时自动校验并加入候选规则；无论通过与否，闭环完成后都进入下一未揭盲案例。

详细操作见 `docs/CHAT-WORK-RUNBOOK.md` 与 `docs/NO-WORK-ISSUE-RELAY.md`。
整体架构、来源梳理、第二阶段知识工程、覆盖缺口和后续实施顺序分别见 `docs/MODEL-ARCHITECTURE-V3.md`、`docs/SOURCE-KNOWLEDGE-MAP.md`、`docs/KNOWLEDGE-ENGINEERING-PHASE2.md`、`docs/CASE-COVERAGE-REPORT.md` 与 `docs/IMPLEMENTATION-ROADMAP-V3.md`。公共资料发布边界见 `docs/PUBLIC-RELEASE-SAFETY.md`。

## 答案隔离

答案只允许以 `answer-vault/encrypted/<CASE_ID>.json.fernet` 保存；密钥只存在 GitHub Actions Secret。预测冻结前不得解密。仓库内不保存逐题正确选项；详细对照只写到仓库外的临时文件。

## 当前迁移状态

- 107例、511题已完成统一入库；107例全部通过输入门，例题98已由用户补传的完整原文修复。
- 例题1保留为已揭盲历史；`ROUND-002`属于同案回放，不计独立证据。
- 例题29有两个选项原文已经出现在S01方法说明中，只能作开发参考，不计首次盲测。
- 当前干净首次盲测日程为：开发63例、阶段验证21例、最终保留21例。
- 新案例答案尚未导入：0/107。系统状态为`DATASET_FROZEN_AWAITING_ANSWER_IMPORT`，不会开放预测。
- 原通用复盘已转换为5条带适用范围的候选规则，等待未来匹配案例验证。

## 控制器

```bash
python -m pip install -e .
fortune-train verify
fortune-train case-bank-verify
fortune-train case-bank-report
fortune-train status
fortune-train report
```

案例库未激活前不得执行`start`。激活后的冻结、评分和失败学习仍由Chat＋GitHub Issue通道调用控制器，不要求用户手工运行命令。

控制器内部的失败学习命令为：

```bash
fortune-train learn ROUND-003 /tmp/model-learning-rules.json MODEL-LEARNING-003
```

预测的每一行除 `top1`、`top2`、`reasoning`、`evidence` 外，还必须包含：

```json
{
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
```

## 验证

```bash
make verify
make test
```

验证覆盖冻结原典、答案隔离、模型发布链、题级标签、规则证据账本、一次性首次盲测状态机、安全 Chat 输入包以及 Issue 自动闭环。
