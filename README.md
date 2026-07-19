# 半自动命理预测训练系统

这是从零重建后的单案例循环训练系统。它只做一件事：把一个真实案例当作未揭盲题反复训练，直到同一案例连续 3 轮达标，再进入下一案例。单题训练次数没有上限。

## 唯一达标规则

- 少于 5 道选择题：必须全部答对。
- 5 道选择题：至少答对 4 道（80%）。
- 多于 5 道选择题：至少答对向上取整的 80%。
- 达标后不立即换题；同一案例必须连续 3 轮达标。
- 任一轮未达标，连续达标次数立即归零；必须先复盘并激活模型修正，再重练同一案例。
- 不存在“最多 5 次”或任何其他轮次上限。

## 来源库只有一个运行权威

原算命项目中的来源库**不要删除**。它是只读原始档案，也可在 Chat 中作为 Git 冻结原典的快速检索镜像；它不是第二套可修改来源库，不能覆盖 Git 状态或模型发布。当前提供的两个 S02 中，只有 `(9)` 与 Git 原典一致，`(8)` 必须移出项目或明确忽略。

训练只读取 Git 仓库中的两层内容：

1. `sources/canonical/`：Git 版 S00–S19 冻结原典。用户经验和古书知识在训练期间不改写，`sources/canonical-manifest.json`用哈希锁定它们。
2. `model-learning/`：模型自己的思路、知识运用方法、执行步骤和待验证新假设。揭盲复盘后只更新这一层。

因此不存在“两套来源库冲突”：Git 是权威，项目文件只是只读镜像；下一轮的有效训练输入始终是“同一份冻结原典 + 最新模型发布”。如果任何 Git 冻结原典被改动，`verify`会直接失败，不能偷偷重新生成锁文件放行。

## 每轮闭环

1. `start`：绑定当前案例、冻结原典哈希和当前模型发布，建立新轮次。
2. 独立预测：只读取当前无答案案例、Git 冻结原典和已激活模型修正。
3. `freeze`：冻结本轮全部首选、次选和理由；冻结后不可修改。
4. `score`：冻结后才读取答案并评分；仓库只保存汇总成绩，逐题答案对照输出到仓库外。
5. 未达标：复盘错误思路或执行缺口，形成不含案例答案映射的模型修正，用 `learn` 激活。
6. 达标但未连续 3 次：对同一案例开启新的独立轮次。
7. 连续 3 次达标：系统自动切换到下一案例。

同一案例第二轮及以后是训练拟合验证，不冒充新的首次盲测准确率，但仍必须重新推理并严格先冻结、后评分。

## 公共仓库中的答案

不需要私人答案仓库。答案可以和系统放在同一个公共仓库，但只能以 `answer-vault/encrypted/<CASE_ID>.json.fernet` 的加密形式保存；解密密钥不能进入仓库。

明文答案一旦进入公共仓库，模型在预测前就可能读到，所谓“未揭盲”将失去可信度。因此控制器会拒绝仓库内的明文答案。当前 5 个案例尚未装入官方加密答案，不能凭空编造；正式评分前需从用户保存的原答案文件生成一次加密文件。

## Chat 与 Work 的真实分工

- Chat 模式：读取项目上下文、完成命理预测、揭盲后复盘、整理候选模型修正。
- Work/Codex：验证并写入模型修正、运行控制器、提交 Git、更新公共仓库。

Chat 模式本身没有 GitHub 插件和仓库写入能力，因此不能保证在纯 Chat 中直接修改 Git。为节省 Work 用量，日常推理放在 Chat；预测完成后只切换一次 Work，由同一个 Work 操作完成冻结、评分，以及未达标时的复盘、落库和发布。项目中的旧 R17 指令必须完整替换为 `docs/PROJECT-MAIN-PROMPT-R1.txt`，不能与新指令叠加。详细操作见 `docs/CHAT-WORK-RUNBOOK.md`。

Work 额度用尽时可改用 `docs/NO-WORK-ISSUE-RELAY.md`：Chat 在揭盲复盘后生成一张不含答案的训练提交单，用户粘贴到 GitHub Issue；仓库自动用加密答案复核评分，更新连续达标状态，并在失败时激活通用模型修正。

## 当前干净基线

- 冻结原典：`sources/canonical/` 中恰好一份 S00–S19。
- 模型基线：`model-learning/releases/MODEL-BASELINE-001.json`，初始没有补丁。
- 例题：`examples/DEV-GROUP-002/cases/` 中 5 个无答案案例。
- 初始状态：`training/state.json`，从例题 1、连续达标 0 次开始。
- 政策：`config/training-policy.json`、`config/source-policy.json`和`config/answer-policy.json`。

## 控制器命令

```bash
python -m pip install -e .
fortune-train verify
fortune-train status
fortune-train start ROUND-001
fortune-train freeze ROUND-001 /tmp/ROUND-001.predictions.json
fortune-train score ROUND-001 --answer-file /tmp/DEV-EXAMPLE-001.answers.json --review-output /tmp/ROUND-001.review.json
```

未达标后：

```bash
fortune-train learn ROUND-001 /tmp/model-learning-patch.json MODEL-LEARNING-001
fortune-train start ROUND-002
```

预测文件格式：

```json
{
  "case_id": "DEV-EXAMPLE-001",
  "round_id": "ROUND-001",
  "predictions": [
    {"question_id": "Q1", "top1": "A", "top2": "B", "reasoning": "..."}
  ]
}
```

模型修正文件必须是通用思路，不能包含案例编号、题号、答案字母或选项原句：

```json
{
  "learning_type": "REASONING_STRATEGY",
  "related_source_libraries": ["S03", "S17"],
  "principles": [
    {
      "statement": "通用判断规则",
      "applicability": "适用条件",
      "limits": "限制",
      "counterexamples": "反例",
      "capability_ceiling": "能力上限",
      "source_basis": "所依据的原典模块和推理依据"
    }
  ]
}
```

答案明文格式只用于仓库外的一次性加密或冻结后评分：

```json
{
  "case_id": "DEV-EXAMPLE-001",
  "answers": [
    {"question_id": "Q1", "correct_option": "A"}
  ]
}
```

生成加密答案：

```bash
fortune-train keygen
FORTUNE_ANSWER_KEY='...' fortune-train encrypt-answer DEV-EXAMPLE-001 /tmp/DEV-EXAMPLE-001.answers.json
```

`keygen`只显示密钥，不写入仓库。评分器只在预测冻结后解密。

## 验证

```bash
make verify
make test
```

`verify`检查 20 份冻结原典的哈希、来源权威、模型发布链、5 份案例的无答案性、训练政策和状态一致性。`--require-answers`只在 5 份官方加密答案都装入后使用。持续集成只保留一个工作流，运行相同检查与测试。
