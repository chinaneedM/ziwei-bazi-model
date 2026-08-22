# 半自动命理推理训练系统

本系统不是修改基础大模型参数，而是建立一套可审计的外部推理系统：冻结S00–S19为知识底座，把真实选择题按主题与推理能力分类；失败复盘只产生不含答案映射的通用模型思路，并在后续不同案例中检验。

## 核心训练规则

- 少于 5 题必须全对；5题及以上达到向上取整的80%记为该轮通过。该阈值只描述本轮表现，不代表整个模型成熟。
- 每个新案例只计一次严格首次盲测；闭环后进入下一新案例。
- 失败后必须完成通用复盘，只更新`model-learning/`，并把本案加入间隔复训队列。
- 至少隔开5个新案例后才可复训；复训只验证修复，不计首次盲测或晋级证据。
- 晋级门是3个不同首次盲测案例连续达标，任一新案失败则归零。
- 第二轮以后不是新的首次盲测准确率，但仍必须重新推理、先冻结、后揭盲。
- 每个案例先冻结一次选项前 `blind_chart_model`，同案所有题共享；每题再完成语义原子化、紫微与八字独立封卷、具体证据账本、全选项比较、反转测试、置信度分解和跨题一致性检查。
- 每道题必须在揭盲前填写 `question_profile`：主题、人物、时间、现实终点、推理能力、来源路线及实际采用的规则。
- 只有预测前明确列入 `applied_rule_ids` 的规则，才会因该题结果获得支持或反证；无关题目不计证据。
- 规则至少在3个不同的后续案例中获得3次支持且支持率达到80%，才从候选状态提升为内部 `VALIDATED`。这仍是题库内经验状态，不等于科学定律。
- 每完成25道严格首次盲测题自动执行短维护；每100道执行中期维护。连续低分、Top2过低、过度自信、规则过量、复训不改善或近期流程故障会提前触发异常维护。维护不计训练证据，也不修改S00–S19。
- 每题先按主题路由，再最多调用6条`model-learning`规则。该上限不限制S00–S19证据数量，也不是检索停止条件。规则必须分为决定性、辅助性与反证；只有去掉后会改变Top1的决定性规则才获得主要验证证据。
- 失败不自动增加规则：执行门、测量、校准、权重、范围、合并、退休、测试和待验证假设都可形成修正；只有`NEW_GENERAL_RULE`增加规则目录。

## 两层运行权威

1. `sources/canonical/`：S00–S19 冻结原典。训练中只读，由 `sources/canonical-manifest.json` 哈希锁定。
2. `model-learning/`：模型自己的通用推理规则。不得包含案例编号、题号、答案字母、选项位置、选项原句或案例专属映射。

外部/项目来源不是运行依赖，项目文件和 File Library 中的 S00–S19 不允许运行时读取。正式唯一权威是 Git `main` 的 `sources/canonical/` 与锁定清单；`sources/canonical/` 被改动时仓库验证会直接失败。

## 题级学习结构

`config/question-taxonomy.json` 定义四类语义标签和推理能力标签。Chat 根据题干、选项和无答案盘面在预测前自动分类，用户不需要人工整理。

`training/state.json`保存当前案例、轮次及连续达标数；`training/learning-ledger.json`只保存不含答案映射的汇总诊断，不作为换案门禁，也不进入预测上下文。

失败产生的通用规则在下一轮按其适用范围启用；规则状态只表示证据强弱，不决定当前案例能否继续。

`training/maintenance-state.json`保存维护里程碑，`training/maintenance-reports/`保存不含答案映射的维护报告，`training/replay-effectiveness.json`单独记录复训相对首次盲测的改善或退化。被更完整规则接替的旧规则保留审计记录，但不再装入运行上下文。

## 每案闭环

1. Chat预测阶段的唯一首次仓库读取必须是
   `main/chat-input/prediction-access-contract.json`；执行其中的默认拒绝契约后，
   才可用GitHub单文件读取访问`training/state.json`、`chat-input/current.json`、
   `sources/canonical/`、当前模型发布实际引用文件及必要配置。File Library、附件、
   历史上传、Personal Context、仓库搜索、旧训练对象和答案对象均被拒绝。
2. Chat 先建立选项前全盘模型，再对每题完成双轨独立封卷、证据账本、全选项比较、真实反转和分解置信度。
3. Chat交接必须原样携带安全启动包生成的`prediction_access_execution_receipt`；它绑定独立契约哈希、唯一首读路径、空的契约前读取列表和固定后续读取顺序。收据缺失或不一致时，预检与Work接收端会在启动轮次、冻结和评分前失败关闭。
4. 完整预测冻结且 binding 与访问收据验证通过后，Chat 进入
   `POST_PREDICTION_HANDOFF`，仅可调用一次 `GITHUB_CREATE_ISSUE`。等价的归一化与
   完整预检在 GitHub controller 中执行；Chat 和用户都无需安装 `gh`、克隆仓库或
   运行 Python/终端命令。
5. 预测冻结后用户揭盲；Chat 输出完整 `TRAINING-ISSUE-PACKET-V3`。
6. 用户把整份 JSON 粘贴到“无 Work 训练提交单”。
7. GitHub 自动冻结、用加密答案复核评分、更新题级统计。
8. 未通过时跨案连续次数归零，校验并激活通用候选规则后进入下一新案，同时排入间隔复训；通过时累加不同新案连续次数。
9. 每轮闭环后控制器自动检查固定里程碑与异常触发器；到期时先完成维护、生成报告，再恢复下一案例。

详细操作见 `docs/CHAT-WORK-RUNBOOK.md` 与 `docs/NO-WORK-ISSUE-RELAY.md`。
整体架构、来源梳理、第二阶段状态、覆盖缺口和后续实施顺序分别见 `docs/MODEL-ARCHITECTURE-V3.md`、`docs/SOURCE-KNOWLEDGE-MAP.md`、`docs/PHASE2-CURATION-AND-MODEL-STATUS-20260723.md`、`docs/CASE-COVERAGE-REPORT.md` 与 `docs/IMPLEMENTATION-ROADMAP-V3.md`。公共资料发布边界见 `docs/PUBLIC-RELEASE-SAFETY.md`。
107例答案的原子导入、无密钥暴露传输、正式控制器切换和不揭盲演练见
`docs/FORMAL-ACTIVATION-RUNBOOK.md`。

## 答案隔离

答案只允许以 `answer-vault/encrypted/<CASE_ID>.json.fernet` 保存；密钥只存在 GitHub Actions Secret。预测冻结前不得解密。仓库内不保存逐题正确选项；详细对照只写到仓库外的临时文件。

## 当前迁移状态

- 107例、511题已完成统一入库；107例全部通过输入门，例题98已由用户补传的完整原文修复。
- 旧控制器中的例题1已完成两轮：`ROUND-001`失败、`ROUND-002`通过，因此按R1迁移后的连续达标数为1/3，不能标记完成。
- 例题29有两个选项原文已经出现在S01方法说明中，只能作开发参考，不计首次盲测。
- 当前干净首次盲测日程为：开发62例、阶段验证21例、最终保留21例；
  CASE-060与CASE-102因冻结前上下文污染仅保留为开发参考。
- 新案例答案尚未导入：0/107。系统状态为`DATASET_FROZEN_AWAITING_ANSWER_IMPORT`，不会开放预测。
- 原通用复盘已转换为5条带适用范围的候选规则，等待未来匹配案例验证。

## 控制器

```bash
python -m pip install -e .
./scripts/bootstrap-work-env.sh --check
python scripts/check-no-github-credentials.py
fortune-train verify
fortune-handoff-preflight --help  # GitHub controller/Work维护使用；CHAT与用户不运行
fortune-train case-bank-verify
fortune-train case-bank-report
fortune-train status
fortune-train report
fortune-train maintenance-status
fortune-train maintenance-run
```

案例库未激活前不得执行`start`。激活后的冻结、评分和失败学习仍由Chat＋GitHub Issue通道调用控制器，不要求用户手工运行命令。

正式化控制器提供以下封闭门禁：完整107例答案批次必须一次性校验并加密；GitHub
Actions只在临时运行器中接触明文；激活后安全包只开放62个开发集首次盲测案例，
CASE-001、CASE-029与CASE-060不计首次盲测。用户不需要接触或粘贴答案密钥。

控制器内部的失败学习命令为：

```bash
fortune-train learn ROUND-003 /tmp/model-learning-rules.json MODEL-LEARNING-003
```

预测使用`PREDICTION-WORKBOOK-V2`。用户可见摘要写入`public_summary`，完整内部结构必须包含：

```json
{
  "question_semantic_model": {},
  "ziwei_track_seal": {},
  "bazi_track_seal": {},
  "cross_track_arbitration": {},
  "evidence_ledger": [],
  "option_comparison_matrix": {},
  "adversarial_review": {},
  "confidence_components": {},
  "counterfactual_analysis": {},
  "question_profile": {
    "topic_tags": ["MARRIAGE_RELATIONSHIP"],
    "subject_tags": ["SPOUSE_PARTNER"],
    "time_scope_tags": ["CURRENT_STATUS"],
    "endpoint_tags": ["RELATIONSHIP_STATUS"],
    "reasoning_skill_tags": ["SUBJECT_ENTITY_ROUTING", "RELATIONSHIP_SEQUENCE"],
    "source_routes": ["S04", "S08", "S16", "S17"],
    "applied_rule_ids": []
  },
  "rule_attribution": {
    "decisive_rule_ids": [],
    "supporting_rule_ids": [],
    "counterevidence_rule_ids": [],
    "decision_changed": false
  }
}
```

`applied_rule_ids`必须恰好等于三类归因ID的并集，三类不得重叠。`CHALLENGED`规则只能进入`counterevidence_rule_ids`。决定性规则删除后必须真实改变Top1。总置信度不得超过输入、本命结构、人物、机制、时序、现实终点、双轨一致及Top1/Top2分离度中的最低项。

完整设计、Schema、冻结门、兼容方式和维护指标见`docs/REASONING-EXECUTION-LAYER-V2.md`。

## 验证

```bash
make verify
make test
```

验证覆盖冻结原典、答案隔离、模型发布链、题级标签、23张知识卡、失败学习、跨案三连门、间隔复训、维护里程碑、选项前全盘模型、双轨封卷、证据父链、全选项矩阵、反转测试、规则消融、置信度校准、安全Chat输入包以及Issue自动闭环。

## 排盘时间／历法底座

确定性的紫微＋八字共用 Time / Calendar Foundation R1 已纳入现有 Python
包，不属于 `model-learning`，也不修改冻结来源。其架构、Policy Registry、
AuditTrace、依赖审计、边界测试和开放问题见
`docs/TIME-CALENDAR-FOUNDATION-R1.md`。可用以下命令生成完整机器可读示例：

```bash
PYTHONPATH=src python scripts/time-calendar-example.py
```

## 紫微＋八字联合排盘工作台

当前日常联合排盘入口为 `fortune-chart-app`。它组合已发布的紫微三合交互、八字显式目标时点 flow 与显式 Shared Target → Ziwei Apply，不执行预测或训练。

联合排盘现在生成共享时间凭证与候选分支联动哈希；它统一时区、UTC、真太阳时和节气事实，但保留紫微与八字各自的换日、历法及晚子时规则，不允许一方规则覆盖另一方。设计与完整性门禁见 `docs/ZIWEI-BAZI-SHARED-TIME-CREDENTIAL-R1.md`。

真实机器启动、只读 smoke、浏览器验收步骤与问题留证格式见 `docs/COMBINED-WORKBENCH-REAL-MACHINE-CALIBRATION-R1.md`。安装后可先运行：

```bash
python scripts/combined-workbench-smoke.py
```
