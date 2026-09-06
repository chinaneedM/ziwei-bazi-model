\nKRDB《高麗史》卷五十二的原图链路现已完成 L114 单点裁决：viewer `kr_052_1116.jpg` 直接显示一百十四至一百十六限，L114 日率为 `九日三四八九`；故 KRDB `types=o` 的 `九日二四八九` 已由其自身原图裁决为数据库转录错误，不再计作跨版本异文。该结论只作用于 L114，不替代奎貴893 独立早期见证，也不改变任何排盘算法。\n# 半自动命理推理训练系统

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

桌面呈现已进入 **Desktop Productization R1**：在不重开任何已闭合确定性算法的前提下，新的 presentation-only product shell 把既有 Workbench 重组为“本命总览 / 时运联动 / 融合视图 / 专业审计”四个工作区；基础出生资料保持主操作，地点/时区/时间精度/Profile 收入高级设置，ManifestHash、RuleSet、Algorithm 与 provenance 下沉到审计区。实现与边界见 `docs/FUSION-CHART-DESKTOP-PRODUCTIZATION-R1.md`。

生成后的 Windows `FortuneChart.exe` 也会验证该 Product Shell 的静态 schema 标记以及 CSS/JavaScript 资源后再执行确定性联合排盘 smoke，防止源码已经产品化而最终 ZIP 仍意外携带旧 Workbench 外壳。

桌面 Product Shell 的首个稳定版本 `0.2.5` 已正式发布，绑定 source commit `2b6b836879700a2ff8f20d75c7d7af76dc867b1a`。真实 0.2.4 → 0.2.5 在线更新、完整目录替换与受控失败回滚已在 `windows-latest` 校准通过；版本提升只改变 Windows 分发身份，不重开任何已闭合排盘算法。最终仍只剩真实用户 Windows 桌面的默认浏览器/可视交互验收。

联合排盘现在生成共享时间凭证与候选分支联动哈希；它统一时区、UTC、真太阳时和节气事实，但保留紫微与八字各自的换日、历法及晚子时规则，不允许一方规则覆盖另一方。设计与完整性门禁见 `docs/ZIWEI-BAZI-SHARED-TIME-CREDENTIAL-R1.md`。

八字候选视图现已补充旬空与日主十二长生事实注记，并将其纳入视图哈希；两者仅作身份展示，不生成旺衰或吉凶结论。冻结口径、来源与语义边界见 `docs/BAZI-XUNKONG-TWELVE-GROWTH-R1.md`。

八字候选视图同时补充胎元、命宫、身宫与每柱“自坐”十二长生；古籍中的三百日前胎元异法以未选择 profile 保留，默认结果不会覆盖异本，也不会影响紫微自己的换日与历法口径。详见 `docs/BAZI-DERIVED-COORDINATES-R1.md`。

紫微流年帧现已补充斗君／正月宫坐标，并纳入时限事实哈希、完整性复算和 SVG 宫位标记；算法只读取紫微自己的农历生月与出生时支。详见 `docs/ZIWEI-DOUJUN-R1.md`。

紫微大限、流年和常规流月现按各层来源干分别生成禄存、擎羊、陀罗动态位置事实；同名星曜按原局／大限／流年／流月保持独立身份，并进入哈希、完整性复算、视图与 SVG，不输出力量或吉凶结论。详见 `docs/ZIWEI-TEMPORAL-MOVING-AUXILIARIES-R1.md`。

八字小运现按古籍同时保留“时柱起、年性别定顺逆”与“男丙寅女壬申固定起点”两套候选，不静默选边；两套都只输出虚岁干支坐标。详见 `docs/BAZI-XIAOYUN-CANDIDATES-R1.md`。

八字神煞事实注册表以 S11《渊海子平》稳定原文段落为权威，现发布天乙、禄神、驿马、华盖、月德、月德合、天德、天厨、福星、太极、三奇、天赦、学堂、金舆、羊刃。年干、日干、月令、纳音与落柱范围按来源分别保存；争议候选不隐式合并，三奇附加条件不伪装为已裁决，也不输出吉凶断语。详见 `docs/BAZI-SHENSHA-FACTS-R1.md`。

八字目标时点现已组成“原局 → 大运 → 小运候选 → 流年 → 流月 → 流日 → 流时”的统一审计时间轴；每个有合法干支的时间层另按原局日主投影十神、藏干十神、纳音、旬空、日主十二长生与自坐十二长生，分别保存事实／计算哈希并由应用完整性路径独立复算。小运两法的注释仍是两个候选，交运前也不会伪造大运干支。目标时点还会只读投影已发布 Structural Context 所支持的大运／流年／流月完整中性事实面，包括帧绑定干支实例、藏干与十神、动态透干、干支亲和及原始关系，全部保留层级、父帧、规则、稳定来源、引用 ID 与独立哈希；Structural Support 同时作为独立下游 Projection 分列原局月令与当前流月，并保留精确藏干匹配／同五行支持候选及其亲和、透干、规则、来源和双哈希，不输出有根、强弱、权重或得令结论。小运／流日／流时明确不在该结构与支持版本覆盖范围。同一目标候选可显式投影到紫微大限、流年、常规流月、小限及只读流日事实。紫微各合法时间层按来源干分别保存四化、禄存／擎羊／陀罗及 S10 完整十干表所载流文昌／流文曲；流魁／流钺同时保存严格 S01 表与文墨兼容案例法两套未选择、独立哈希的候选，即使非辛干结果相同也不合并方法身份。流天马仅按 S10 已闭合的案例层保存为未选择候选：大限绑定大限命宫宫支，流年绑定流年地支，两者方法、来源和哈希独立，且不扩展到流月、流日或流时。流日另输出十二宫宫职。紫微流时因全局规则证据不足，仅在洛阳平太阳时／地方真太阳时两套未选择案例法候选内分别保存命宫、十二宫宫职、干支、动态辅助星及四化，不生成唯一或完整时盘。两系仍分别执行自己的历法与换日规则；小运门派不选边，紫微闰月不伪造常规月盘、流日盘或流日四化。详见 `docs/BAZI-TEMPORAL-CLASSICAL-ANNOTATIONS-R1.md`、`docs/BAZI-TARGET-FLOW-STRUCTURAL-PROJECTION-R1.md`、`docs/BAZI-TARGET-FLOW-STRUCTURAL-SUPPORT-PROJECTION-R1.md`、`docs/BAZI-ZIWEI-UNIFIED-TARGET-TIMELINE-R1.md` 与 `docs/S10-DYNAMIC-AUXILIARY-AUDIT-R1.md`。

共享目标时间到紫微的 Projection 现同时保存目标所对应的大限、流年与常规流月完整层事实：父帧、来源层、来源干、时限规则／算法身份、稳定来源、四化、禄存／擎羊／陀罗及层级双哈希。各层同名星曜保持独立 activation 身份；完整性验证从已发布源帧逐层复算，浏览器只读展示而不改写事实。大限前与闰月边界分别保持空层，不伪造不存在的帧。

共享目标时间到紫微的 Projection 另只读保存选中小限与原局博士、将前、岁前三环的交会；每环保留原锚点、方向、生成器、成员来源与独立双哈希，不按小限宫重起动态环。

真实机器启动、只读 smoke、浏览器验收步骤与问题留证格式见 `docs/COMBINED-WORKBENCH-REAL-MACHINE-CALIBRATION-R1.md`。安装后可先运行：

```bash
python scripts/combined-workbench-smoke.py
```

## Fusion Chart Product R1 收口状态

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
DESKTOP_PRODUCT_SHELL_R1=IMPLEMENTED
WINDOWS_BINARY_PLATFORM_ACCEPTANCE=PENDING_PLATFORM_ACCEPTANCE
AUTOMATED_TWO_VERSION_UPDATE_CALIBRATION=ACCEPTED
MANUAL_WINDOWS_BROWSER_ACCEPTANCE=PENDING
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

R1 的确定性排盘产品已经完成字段可见性、Workbench/desktop 运行契约、完整性/更新机制及 CI/release 门禁收口。Windows runner 会从最终 ZIP 启动两个 `.exe`，验证打包依赖、loopback health、确定性联合排盘及 updater 非变更启动；默认浏览器交互和真实两版本升级/回滚仍需单独平台验收，因此保持 `PENDING_PLATFORM_ACCEPTANCE`。该状态不会重开时间历法、八字本命/flow、紫微本命/Structural R1–R8 或 Combined Fusion R2。

所有 disputed candidates 继续保留多候选、不得选 winner；紫微离心/向心自化方向仍不得由现有宫干拓扑或结构几何推导。最终审计见 `docs/FUSION-CHART-PRODUCT-R1-FINAL-ACCEPTANCE-20260904.md`，Windows 剩余实机条件见 `docs/WINDOWS-BINARY-PLATFORM-ACCEPTANCE-R1.md`。


## Fusion Chart Capability & Performance Acceptance R1

```text
FUSION_CHART_CAPABILITY_PERFORMANCE_ACCEPTANCE_R1=ACCEPTED
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

Fusion Chart Capability & Performance Acceptance R1 已正式收口。最终执行证据绑定 source SHA `0b20a9cf6e058f096582e09b72142077399e1ac3` 与 workflow `33867682199`：Golden/Temporal/Reference focused acceptance、source performance、Windows 最终 EXE performance、10,000 固定种子随机 deterministic replay 以及 1,000 次 HTTP/Target Flow/Fusion R2 soak 全部 PASS；10k 结果为 deterministic mismatch=0、invariant failure=0、execution error=0。100k 因实测并行投影约 8,875 秒超过预设 3,600 秒预算而按规则 skipped，不属于失败。reference implementation 的差异不能直接触发算法修改；本轮确认的 implementation defect=0、algorithm reopen=0。

验收总说明见 `docs/FUSION-CHART-CAPABILITY-PERFORMANCE-ACCEPTANCE-R1.md`，机器可读 capability matrix 见 `docs/FUSION-CHART-CAPABILITY-MATRIX-R1.json`，性能基线和 defect ledger 分别见 `docs/FUSION-CHART-PERFORMANCE-BASELINE-R1.md` 与 `docs/FUSION-CHART-DEFECT-REPORT-R1.md`。


## Fusion Chart Historical Provenance & School Audit R1

```text
FUSION_CHART_HISTORICAL_PROVENANCE_AUDIT_R1=IN_PROGRESS
HISTORICAL_PROVENANCE_INVENTORY=COMPLETE
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

第一版确定性融合排盘已经进入规则历史考据与流派审计阶段。当前通过 Historical Provenance Audit Matrix 逐项绑定当前实现、Profile、主要来源、原文位置、时代/版本、后续见证、流派归属、竞争方法、实现一致性与处置状态。S00–S19 现明确定位为**项目研究语料 / 冻结内部资料**，并非天然正确或不可推翻的历史权威；`sources/canonical/` 只保留旧架构中的存储/冻结含义，不代表 epistemic truth。S00–S19 中的转录、归属、现代整理、流派范围与结论本身都必须接受外部原始版本、received text、书目与流派证据的反向审计。文墨天机与问真八字继续只作为现代实现/兼容性 witness。研究权威规则见 `docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md`。

初版矩阵只建立审计账本，不重开任何已 CLOSED 的确定性算法。只有明确的一手/高质量历史证据与可复现实现不一致同时成立，才允许对对应 rule/profile 做局部 forward-only reopen。机器可读矩阵、人工说明和门禁分别见 `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json`、`docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md` 与 `scripts/verify-fusion-chart-historical-provenance-audit-r1.py`。

截至 Batch 11L，Matrix 仍为 197 个 rule/field families、165 行完成实审；HISTORICALLY_SUPPORTED=87，identified missing candidate families=13，chart algorithm defect=0，algorithm reopen=0，provenance defect=9/9 repaired。11B/11C 把大运真实交运历日与现代日历实现拆开并建立 fail-closed historical-calendar adapter contract；11D-11G 闭合明大统历一手方法源、1578 官方实录月朔 oracle、D1/迟疾行度生产算法与子正/100刻内部时间坐标；11H/11I 完成 1578 的 13/13 日级源算法重放与同年 NCL 06313 钦天监原历 12/12 月页直接影像校勘；11J 闭合 1569 主表的阶段化精度图并否定“全局统一舍入法”。11K/11L 进一步把 1673 小川正意《授時暦經立成》的 NDL 与九州大学两个独立馆藏分开做无 OCR 原图校勘：D16 在两个馆藏中均因表结构缺少独立日差/消息分型字段而保持不可直接比较，L114 均直接为 `九日三四八九`；九州本的 L8↔L159、L35↔L132、L67↔L101 同本控制建立了分栏位值训诂边界。九州本另见独立 `遲疾限行度` 表，其 L124 数值层与 1569 明本的捷法/倒数层严格对应：疾 `0.0797587`、遲 `0.0704164` 支持明本 raw `1.0281/1.1645` 的机械谱系，但这不是 raw `1.0281` 的直接字面影像。G893 早期实物目标页与更早传播成因仍未闭合；三个 Dayun calendarized candidate 继续 `MISSING_FROM_PRODUCT`，历史历法 runtime 仍保持 fail-closed。最新批次见 `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-OGAWA-1673-KYUSHU-COLLATION-L.md`。

为避免长对话触发上下文限制导致工作断层，仓库现建立固定跨对话机制：`docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 定义新对话启动顺序，`docs/PROJECT-CURRENT-STATE-R1.json` 保存机器可读当前阶段/批次/计数/下一工作重点，`scripts/verify-project-continuity-state-r1.py` 在 CI 中强制校验它与 Historical Audit Matrix 一致。新对话不再依赖旧聊天总结或旧 SHA，只需先读取 GitHub 远端最新 HEAD，再按该协议恢复工作。
