# Work 额度用尽时：GitHub Issue 自动训练通道

这个通道不调用 ChatGPT Work，也不要求用户运行 Git、`gh`、Python 或终端命令。Chat 负责预测和揭盲复盘；GitHub Actions 负责重新评分、校验、落库和更新训练状态。

## 一、只做一次的安全准备

仓库需要满足两项条件：

1. 5 个案例各有一个 `answer-vault/encrypted/<CASE_ID>.json.fernet` 加密答案文件。
2. 仓库 Settings → Secrets and variables → Actions 中存在名为 `FORTUNE_ANSWER_KEY` 的 Repository secret。

密钥只保存在 GitHub Secret 中，不放入项目指令、Chat、Issue、代码、提交记录或 Actions 日志。Issue 自动通道在缺少任一加密答案或密钥时会拒绝运行。

## 二、每轮实际操作

1. 在 Chat 中说“开始当前案例下一轮”，完成全部题目的预测。
2. 冻结预测后，再向 Chat 提供本轮正确答案，让 Chat 评分和复盘。
3. 对 Chat 说：

   > 生成 `TRAINING-ISSUE-PACKET-V1`。保留刚才冻结的全部 predictions；根据揭盲评分填写 expected_result。若失败，加入不含案例编号、题号、答案字母和选项原句的 learning_release_id 与 learning_patch；若通过，不得加入学习修正。只输出一个 JSON 代码块。

4. 打开：<https://github.com/chinaneedM/ziwei-bazi-model/issues/new?template=training-round.md>
5. 点击 Issue 正文框，按 `Ctrl+A` 全选，再按 `Ctrl+V` 粘贴 Chat 生成的整份 JSON。无需寻找占位符、保留标记或手工修改 JSON。
6. 标题默认以 `[TRAINING ROUND]` 开头，不需要改；直接点击 **Submit new issue**。
7. GitHub 自动执行以下动作：
   - 只接受仓库所有者创建的 `[TRAINING ROUND]` Issue；
   - 检查当前案例、轮次和预测完整性；
   - 先冻结预测，再用加密答案重新评分；
   - 核对 Chat 填写的 PASS/FAIL；
   - 失败时验证并激活通用模型修正；
   - 检查 S00–S19 未被改写并运行全部测试；
   - 只提交 `training/` 与 `model-learning/` 的允许内容；
   - 在 Issue 留下不含答案的结果并自动关闭。
   - 自动刷新 `chat-input/current.json`，为下一轮 Chat 提供不含旧预测的唯一安全入口。

## 三、提交单 JSON 格式

达标轮：

```json
{
  "schema": "TRAINING-ISSUE-PACKET-V1",
  "round_id": "ROUND-20260719-001",
  "case_id": "DEV-EXAMPLE-001",
  "predictions": [
    {
      "question_id": "Q1",
      "top1": "A",
      "top2": "B",
      "reasoning": "通用证据链",
      "evidence": ["S03", "S17"]
    }
  ],
  "expected_result": "PASS"
}
```

未达标轮还必须在同一个 JSON 的最外层增加：

```json
"learning_release_id": "MODEL-LEARNING-20260719-001",
"learning_patch": {
  "learning_type": "REASONING_STRATEGY",
  "related_source_libraries": ["S03", "S17"],
  "principles": [
    {
      "statement": "可推广判断规则",
      "applicability": "适用条件",
      "limits": "限制",
      "counterexamples": "反例",
      "capability_ceiling": "能力上限",
      "source_basis": "所依据的原典模块与推理理由"
    }
  ]
}
```

## 四、出错时怎么办

- Issue 留言显示成功并自动关闭：本轮已经写入 `main`，回到 Chat 说“读取 Git 最新状态，开始下一轮”。
- Issue 留言显示失败：本轮不会提交任何修改。打开留言中的 Actions 链接查看错误；通常是 JSON 格式、PASS/FAIL 不符、修正含案例答案映射，或首次密钥/加密答案尚未准备完成。
- 不要反复编辑同一个失败 Issue。修正 JSON 后重新创建一张新的训练提交单。

## 五、最简日常口令

预测已经输出后，用户只需在同一个 Chat 对话中说：

> 现在揭盲：在这里填写答案字母串。请评分、复盘，并在回复末尾生成可直接整份粘贴到“无 Work 训练提交单”的 `TRAINING-ISSUE-PACKET-V1` JSON。JSON 不得包含正确答案或密钥。

Chat 输出 JSON 后，点击代码块的复制按钮；到 GitHub Issue 正文中 `Ctrl+A`、`Ctrl+V`、提交即可。
