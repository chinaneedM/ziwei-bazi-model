# 半自动命理预测训练系统

这是从零重建后的单一训练流程。训练单位是**一个完整案例**，不是整组案例，也不是固定次数的回放。每轮对该案例的全部选择题作答；轮次没有上限。

## 唯一达标规则

- 少于 5 道选择题：必须全部答对。
- 5 道选择题：至少答对 4 道（80%）。
- 多于 5 道选择题：至少答对向上取整的 80%。
- 一轮达标后不换题；同一案例必须连续 3 轮都达标，才进入下一案例。
- 任一轮未达标，连续达标计数立即归零。完成复盘并激活通用知识修正后，再开同一案例的新一轮。
- 不存在“最多训练 5 次”或任何其他轮次上限。

## 每轮闭环

1. `start`：绑定当前案例、当前 S00–S19 基线和累计知识修正，创建全新的未揭盲轮次。
2. 独立预测：只读取案例输入、来源库和已经激活的通用知识修正；不得读取答案或以前的详细揭盲记录。
3. `freeze`：冻结本轮全部选择，冻结后不可修改。
4. `score`：冻结后才允许解密答案并评分。仓库内只保存汇总分数，详细对照必须输出到仓库外。
5. 未达标：复盘错误原因，形成不含案例答案映射的通用知识修正，用 `learn` 激活后回到第 1 步。
6. 达标但未连续 3 次：直接对同一案例开启新的独立轮次。
7. 连续 3 次达标：系统自动切换到下一案例。

同一案例的第二轮及以后属于**训练拟合验证**，不冒充新的首次盲测准确率。每轮仍必须使用新的轮次目录、重新作答并先冻结后评分。

## 当前干净基线

- 来源：`sources/active/` 中恰好一份 S00–S19。
- 例题：`examples/DEV-GROUP-002/cases/` 中 5 个无答案案例。
- 初始状态：`training/state.json`，从例题 1、连续达标 0 次开始。
- 政策：`config/training-policy.json`。
- 答案：只允许加密文件进入 `answer-vault/encrypted/`；明文答案与密钥禁止进入仓库。

## 使用

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
fortune-train learn ROUND-001 /tmp/general-learning-patch.json LEARNING-001
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

答案明文格式只用于一次性加密，且文件必须位于仓库外：

```json
{
  "case_id": "DEV-EXAMPLE-001",
  "answers": [
    {"question_id": "Q1", "correct_option": "A"}
  ]
}
```

评分有两种安全入口：冻结后临时提供仓库外的可信答案文件；或者先生成密钥并安全保管，再加密每个案例答案：

```bash
fortune-train keygen
FORTUNE_ANSWER_KEY='...' fortune-train encrypt-answer DEV-EXAMPLE-001 /tmp/DEV-EXAMPLE-001.answers.json
```

`keygen` 只把密钥打印到终端，不写入仓库。加密答案不是强制；如果答案仍在原压缩包或独立答案仓库，评分时用 `--answer-file` 即可。两种方式都只会在预测冻结之后读取答案。

## 验证

```bash
make verify
make test
```

`verify` 检查 20 份来源文件的哈希、5 份案例的无答案性、政策和状态一致性。`--require-answers` 只用于选择“预置加密答案”模式时的严格检查。持续集成只保留一个工作流，运行相同检查与测试。
