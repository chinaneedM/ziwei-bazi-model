# 107例答案导入与正式控制器激活

## 固定顺序

1. 在仓库外准备一份`FORTUNE-ANSWER-BATCH-V2`明文答案批次。
2. 使用与GitHub Actions Secret `FORTUNE_ANSWER_KEY`相同的密钥执行原子导入。
3. 校验107个加密信封都可解密、案例和题目一一对应。
4. 激活`FORMAL-DEVELOPMENT-001`控制器。
5. 执行不揭盲演练；只检查安全启动包，不启动、冻结或评分任何轮次。

任一步失败都不得开放预测。

## 答案批次格式

明文文件必须位于仓库外，且只接受完整107例：

```json
{
  "schema": "FORTUNE-ANSWER-BATCH-V2",
  "corpus_id": "FORTUNE-CASE-BANK-107-V1",
  "cases": [
    {
      "case_id": "CASE-001",
      "answers": [
        {"question_id": "Q1", "correct_option": "A"}
      ]
    }
  ]
}
```

每例的`answers`必须覆盖该案例全部题目且只能使用该题已有选项。上例只是结构示范，
不是正式答案。

若原题本身没有任何正确选项，只允许使用以下严格结构；该题仍需完成预测与冻结，
但不进入正确率分母、达标门槛或学习证据：

```json
{
  "question_id": "Q3",
  "scoring_status": "UNSCORED",
  "reason_code": "NO_VALID_OPTION"
}
```

正式批次汇总为511题，其中510题可评分、1题不计分。题库允许每题为连续的
`A–D`或`A–E`选项；当前共有29道五选题。

## 控制器命令

```bash
fortune-train import-answer-batch /outside/trusted-answers.json
fortune-train verify-formal-answers
fortune-train activate-formal
fortune-train rehearse-formal
```

日常操作不要求用户接触密钥。仓库提供两步所有者工作流：

1. `[ANSWER IMPORT] BOOTSTRAP`：GitHub Actions使用现有Secret生成一次性公开传输钥，
   私钥只以加密形式进入公共仓库。
2. Work使用公开传输钥把仓库外答案批次封装为认证密文并上传。
3. `[ANSWER IMPORT] FINALIZE`：Actions在临时运行器内解密、校验、生成107个正式
   Fernet信封、激活控制器并完成不揭盲演练；随后删除一次性传输材料。

因此，用户只需提供完整答案原件；不需要把Secret粘贴到Chat、安装`gh`或运行命令。

导入成功后，仓库只新增Fernet密文、哈希和不含答案映射的汇总计数，不写入明文答案。正式控制器只使用开发集
的63个干净首次盲测案例；历史揭盲的CASE-001和来源暴露的CASE-029不会进入首次盲测。
首个安全启动案例是CASE-002，推荐轮次为`FORMAL-ROUND-001`。
