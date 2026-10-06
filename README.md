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

最新规则审计闭环为 **Batch 12PA**：12OZ 的 1384/1385、1479/1480 四个闰法张力已被“**闰在年前**”民用年归属分支解释。1569 周相本 `推閏餘分法` 的闰余阈值继续作为 primary source-scoped 规则；《明史》卷35只作为后出 received placement bridge，规定 `朔策−閏餘` 除以 `月閏=9062.82` 后整数商 0 或 1 时归为“年前”。1385 的余差 4481.91 因而归到 civil 1384，1480 的余差 8574.66 归到 civil 1479；明实录传统分别直接记洪武十七年、成化十五年闰十月。四个 tension 因此不是 D1 精度或 primary 闰余公式缺陷。但全明公式层共有 **15 个**“年前”候选标签，尚未全部做民用年史料校验，所以 G09 继续 OPEN、历史 calendar runtime 继续 fail-closed。Matrix 222/222，MISSING_FROM_PRODUCT=4，provenance defect=45/45 repaired。下一门 **12PB** 将校验 15 个候选并移除 research generator 的固定 k=2 民用年起点捷径。

```text
FUSION_CHART_HISTORICAL_PROVENANCE_AUDIT_R1=IN_PROGRESS
HISTORICAL_PROVENANCE_INVENTORY=COMPLETE
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

第一版确定性融合排盘已经进入规则历史考据与流派审计阶段。当前通过 Historical Provenance Audit Matrix 逐项绑定当前实现、Profile、主要来源、原文位置、时代/版本、后续见证、流派归属、竞争方法、实现一致性与处置状态。S00–S19 现明确定位为**项目研究语料 / 冻结内部资料**，并非天然正确或不可推翻的历史权威；`sources/canonical/` 只保留旧架构中的存储/冻结含义，不代表 epistemic truth。S00–S19 中的转录、归属、现代整理、流派范围与结论本身都必须接受外部原始版本、received text、书目与流派证据的反向审计。文墨天机与问真八字继续只作为现代实现/兼容性 witness。研究权威规则见 `docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md`。

初版矩阵只建立审计账本，不重开任何已 CLOSED 的确定性算法。只有明确的一手/高质量历史证据与可复现实现不一致同时成立，才允许对对应 rule/profile 做局部 forward-only reopen。机器可读矩阵、人工说明和门禁分别见 `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json`、`docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md` 与 `scripts/verify-fusion-chart-historical-provenance-audit-r1.py`。

截至 Batch 12Q，Matrix 为 198 个 rule/field families、166 行完成实审；HISTORICALLY_SUPPORTED=88，SUPPORTED_BUT_SCHOOL_SPECIFIC=18，当前 `MISSING_FROM_PRODUCT`=10，累计 identified missing candidate families=14，historical candidate extensions=6，candidate registries/runtime resolvers=3/3，chart algorithm defect=0，algorithm reopen=0，provenance defect=9/9 repaired。11B–11P 的历史历法、明大统历、1673 小川本、G894 与《世宗实录》校勘边界全部保持不变。11Q–11U 已依次收口 G893 的 GitHub-hosted 图像访问边界、战前馆藏连续性、1908/[1912-1920] 目录阴性控制与 1940 贵重书目录正面身份绑定；1940《奎章閣貴重圖書目錄》直接记录 `授時曆立成 = 圖書番號 893 = 1冊`，故现行 `授時曆立成 / 奎貴893 / GK00893_00` 的 catalog-item continuity 维持 `RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL`，1930 普通主序号 893 的数字捷径继续被直接证伪。11V 实测当前预存 M/F PDF 路径为 `CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED`；11W 又从《中国科技史料》官方期刊门户直接绑定李银姬、景冰 1998 专文的 official record/abstract，但全文仍由 CNKI 承载且没有目标图版。11X 现进一步直接确认官方复制服务本身：G893 详情页明确暴露复制申请入口并记录 `M/F73-102-37-A`，馆方公告明确说明微缩胶卷复制在申请/审批后以扫描 PDF 上传官网，通常两周内处理（延迟另行通知），非会员复制列表又记录自 2024-02-01 起由邮寄纸本改为官网公开微缩扫描 PDF。该路径尚未实际提交、审批或履约，整册/选页范围及费用均不得猜测；因此六个 G893 控制继续全部 `PENDING_DIRECT_TARGET_PAGE`。另外，Batch 08B 已完成考据的 `HPA-ZTEMP-004/006` 现已通过 `ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-REGISTRY-R1` 产品化为显式 `PRESERVED_NOT_SELECTED` 候选：1581《捷览》日锚定流时按各时间标准独立绑定父流日并进入 hash/full-replay；中州闰月只输出前半/后半月归属与十五/十六切分不重置约束，闰月流日起点宫位仍保持 fail-closed。Batch 12A 又完成《紫微斗數全書》南陽堂七卷本直接影印校勘：公开 PDF SHA-256 `32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7`，卷五 PDF p.320《論人生時要審的確》直接可见「上五刻屬昨夜亥時、下五刻屬今日子時」。这既不能验证 S01 所称「子時乃一日之始，當從新日計」精确引文，也不能被简化成现代 23:00 换日；它反而揭示了一个当前 runtime 不能表达的半子时亥/子支重分类候选，现登记为 `HPA-ZDATE-006=MISSING_FROM_PRODUCT`，但上/下五刻的现代时钟映射及跨版本范围尚未闭合，因此不重开默认算法。Batch 12B 进一步完成“十刻/上五刻/下五刻”的时制训诂：《三命通会·论时刻》直接把子时上半置于夜半前/昨日、下半置于夜半后/今日，并说明一时八大刻二小刻；《日知录·百刻》继续解释“每时十刻”并非十个等长刻。国立天文台资料只用于把固定十二辰刻翻译为现代坐标：子刻约 23:00–01:00、正子为午夜，因此上下半约为 23:00–24:00 / 00:00–01:00。此翻译不替紫微选择民用时、平太阳时或真太阳时。识典转录与影印本的上五刻/下五刻一致，而维基文库的上午刻/下午刻保留为转录差异。`HPA-ZDATE-006` 继续 `MISSING_FROM_PRODUCT`，计数不变。Batch 12C 又完成独立《全书》版本路线图：心一堂官方说明把 2017 影印本（ISBN 9789888266944）绑定到虚白庐藏明末清初文光堂木刻的敦化堂、继述堂两本，另从《捷览》官方出版说明绑定清中期文诚堂《紫微斗数全书》为独立校本路线；文盛堂与继述堂相似性仅保留为二手线索。研究 workflow run 34120317222 / artifact 10017909080 未取得任何目标页——博客来商品及 13 个试读图均 403，Google Books API 为 429，保存试读图数量为 0。因此“亥时”跨物理版本稳定性仍未闭合，不能靠出版社说明或现代转录推定。Batch 12D 又把 2017 心一堂合校影印本精确绑定到 Google Play/Books volume `aIRbDgAAQBAJ`：公开全文索引把《論人生時要審的確》定位到 `PT165`，并返回“上五刻/下五刻/亥時”索引文本，与南阳堂直接影印读法一致；但该层只是搜索索引文本，不是物理字形。Google 官方 Embedded Viewer 虽接受跳转 `PT165`，实际截图仍是不可预览占位且最终 page id 为 PT166，没有显示目标古籍页；因此也不能判断该页来自敦化堂还是继述堂。星易公开 7 张样图亦已逐张目验，没有目标页；孔夫子图片路径跳登录，未绕过认证。由此 `HPA-ZDATE-006` 继续 `MISSING_FROM_PRODUCT`，`亥時` 跨物理版本稳定性继续未闭合，计数及算法状态不变。Batch 12E 又新增一条独立的清经纶堂版本路线：上海图书馆官方 linked-data 把 `新鋟希夷陳先生紫微斗數全書四卷` 绑定为 `清經綸堂刻本 / 子30814110 / instance 1pjr6vy1ffsq3l1y`；公开 metadata 没有直接暴露 IIIF、manifest、itemId 或 dhapi 页图对象，当前古籍及 pdfview 匿名入口为 HTTP 412，因此没有猜 itemId、没有登录、没有复用 token、没有枚举页码。韩国金曜拍卖 `BBAA18036` 又独立公开一套约 19 世纪 `經綸堂梓行 / 合4冊` 实物本，research run `34124948029` / artifact `10019806060` 解出 36 个内嵌 JPEG 出现项，去重为 8 张实物照片并全部人工目验；书衣题签可直接辨认 `陳希夷先生著 / 紫微斗數 / 經綸堂梓行`，但八张都不是《論人生時要審的確》。因此经纶堂实体版本身份已加强，`亥時` 跨物理版本稳定性仍未闭合，`HPA-ZDATE-006` 继续 `MISSING_FROM_PRODUCT`，计数及算法状态不变。Batch 12F 又把 12E 之后已经提交的探测统一审判收口：南开大学图书馆外部资源页直接把“辽宁省图书馆古籍书目查询”绑定到辽宁馆旧 `gj` 路线，但清文诚堂《全书》之辽宁馆藏仍只有二手书目定位，当前辽宁官方页面超时，故不冒充官方馆藏记录；大连图书馆则直接公开一条民国上海 `廣益書局 / 石印本 / 四卷 / 四冊一函` 的《(新鐫希夷陳先生)紫微鬥數全書》书目记录，工作流保存的 6 张所谓图片已全部人工目验，实际都是网站 logo/分隔线等 UI 素材而非古籍页。其公开 GET 书目表单虽已按正常参数查询 14 次，但返回页不反映检索词，因此也禁止据此做“没有其他版本”的阴性结论。Google Books `rZRcCwAAQBAJ` 的 PT176 又直接给出编辑校勘说明，明确文诚堂《紫微斗数全书》（文本斗数全书）被用于《捷览》异文校勘；但该层仍只是编辑/搜索索引证据，没有把《論人生時要審的確》目标段或“亥”字直接绑定到文诚堂实体页。故 `HPA-ZDATE-006` 仍为 `MISSING_FROM_PRODUCT`，跨物理版本“亥”字稳定性继续 `UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES`，计数和算法状态均不变。Batch 12G 又把另一条《紫微斗數全集》传统纳入训诂与版本审计：心一堂官方说明及 Google Books `rZRcCwAAQBAJ` 的 PT176/PT177 直接绑定清连元阁《紫微斗数全集》为《捷览》校勘/补缺底本，PT205 还证明该编辑层确会标注《全集》异文；DestinyNet received transcription 的《全集·五凶神》则保留“子有十刻、上五刻属昨夜、下五刻属今夜子”的平行文字。但这只是现代转录，且其文字没有直接写“上半属亥时”，因此不能与南阳堂《全书》的亥支重分类机械等同。针对《全集》目标句的精确索引查询为零不能作阴性证明，而短词“子有十刻”返回 PT88 却不含检索词，明确按索引错配处理。故 12G 不新增候选、不改变计数、不重开算法，下一证据门槛仍是连元阁或其他《全集》实体目标页。Batch 12H 又把日本明刊《全书》路线推进到馆藏实体与正式影印层：日本国立公文书馆公开索引直接绑定 `新鋟希夷陳先生紫微斗数全書 / 子０６０－０００１ / 紅葉山文庫 / 刊本:明 / 2冊 / 公開`，第一册数字对象为 `4468520`；但 GitHub runner 对官方 file/item/img 及 JSON/RDF 路线全部返回 403，因此只判为云执行环境访问边界。山东大学《子海珍本编·日本卷》则直接说明这部七卷《全书》系据内阁文库藏明刊本影印，形成正式影印替代路线。成大陈昭吟论文的版本表把该日本《全书》放在书林棲和堂/南阳堂谱系，并把另一《全集》线索指向金陵益轩唐谦；但东洋文库现行 `VII-3-157` 官方书目又把相关《全集》对象标为鈔本/寫本，故两者之间的实物传承桥仍保持未决，禁止直接合并。12H 仍没有直接读到日本本《論人生時要審的確》目标页，不新增候选、不重开算法。Batch 12I 随后把 12H 之后已经提交的探测统一做了证据去重与定位审判：Batch 12A 南阳堂镜像与 NAAJ/内阁文库路线高度支持为同一物理副本/数字化谱系，故不得再当作第二份独立“亥时”实体见证；Google Books `kxdy0QEACAAJ` 只闭合 2016 七卷《全书》的书目对象，尚未锁定《子海珍本編·海外卷·日本：內閣文庫》15册中的具体分册和目标页；潘国森 `RISpDgAAQBAJ` 只加强文光堂/敦化堂/继述堂版本定位，未找到 late-Zi 目标段；识典 run `34138050721` / artifact `10024763004` 虽能访问已知目标页/API，却返回 0 个图像 URL、0 张图像，故不提升实体字形权威。12I 不新增候选、不改变 198/166/10/14 计数、不重开算法。Batch 12J 随后把广益书局路线从 12F 的官方馆藏书目推进到公开实体照片层：research run `34140027356` / artifact `10025522997` 保存商品页及四张实物 JPEG，人工无 OCR 目验可直接读到封签/内题的 `校正紫薇斗數全書 / 紫薇斗數全書 / 上海廣益書局印行`，并确认四册实物；但四图均不是《論人生時要審的確》目标页，因此没有新增“亥时”实体见证。实体照片的 `薇` 与大连馆/NCKU 书目层常用的 `微` 分层保留，尚不得静默归一后断言完全同版；成大版本谱系又把广益本视为据榮和堂版付印，并把榮和堂/南阳堂归入同一建阳出版源头大类，所以未来取得广益目标页时，它属于重要的后出实体传承校勘，但不能仅凭“另一套实体书”就当作完全独立文本谱系的一票。12J 仍不新增候选、不改变 198/166/10/14 计数、不重开算法；更高价值目标继续是文光堂、经纶堂、文诚堂或连元阁的直接目标页。确定性排盘核心继续 CLOSED。Batch 12K 又专门审判了 2017 心一堂文光堂合校影印本 `aIRbDgAAQBAJ` 的 PT165 底本归属问题：run `34174455835` / artifact `10036772401` 保存三民公开的 8 张原彩试阅页并重跑索引。八图均为真实影印页，人工无 OCR 目验在第 4、6 张可见明显朱色校记，但没有一张是《論人生時要審的確》；出版方虽说明继述堂本有朱墨点校，公开样图却没有逐页注明底本，因此不得把红色批点机械当成继述堂身份。更关键的是，最新索引把 `敦化堂/敦化堂藏板` 命中 PT10/PT11，而 `繼述堂藏板` 同样命中 PT10；目标段仍在 PT165。这证明堂号索引命中属于前置出版/编辑说明层，不能拿页码位置当作底本切换边界。故 PT165 继续严格记为 `UNRESOLVED_DUNHUATANG_VS_JISHUTANG`：其索引文字可以继续旁证“上五刻属昨夜亥時、下五刻属今日子時”，但不能冒充敦化堂或继述堂某一实体目标页，更不能算成两套底本各自独立的一票。12K 不新增候选、不改变 198/166/10/14 计数、不重开算法。 确定性排盘核心继续 CLOSED。Batch 12L 又审判了公开的学林出版社《康节说易全书·紫微斗数》陈明点校本。该 345 页 PDF 的封面/前置页直接证明它是现代横排简体排印，而非另一套古刻影印；目录把卷三目标篇《论人生日时要审的确》标为印刷页 151。有限页码复核进一步直接证明 PDF p165 = 印刷 p151，人工无 OCR 目验该页确实写有 `上五刻属昨夜亥时、下五刻属今日子时`。因此这条资料可作为现代 received-text 传承旁证，说明该读法在现代整理层继续流传；但它不增加任何古刻实体字形见证，也不能拿简体字、现代标点或镜像 PDF 去证明敦化堂/继述堂等版本。12L 不新增候选、不改变 198/166/10/14 计数、不重开算法。 确定性排盘核心继续 CLOSED。Batch 12M 把《全集》late-Zi 研究从现代转录推进到同治九年明经阁实体副本谱系：公开 v.1 图像直接绑定 `一簑古 523.5 J562b` 并可见 `同治九年新鐫 / 飛星紫微斗數 / 陳希夷先生著 / 羊城明經閣板`；盘多啦公开 v.4 预览又直接显示首尔大学奎章阁水印、`523.5 J562b V.4` 与 0001–0005 页，已进入卷四《太微賦總括》等早段，但尚未到《五凶神》。盘多啦、神机阁、Scribd 均按同一 SNU 一蓑文库数字化谱系去重，不得按镜像站数量重复计票；Scribd 无登录浏览器只到 CAPTCHA，未绕过；Kyudb 在 GitHub runner 上于 TLS 阶段 reset，只记执行环境访问边界。韩国学中央研究院 Sillokwiki 另独立记录汉阳大学图书馆藏 6卷6册、1870、明经阁木板本《新刻合倂十八飛星策天紫微斗數全集》，形成更有价值的第二实体副本路线，但其目标页尚未取得。故 12M 仍不新增“亥”字实体见证、不新增候选、不改变 198/166/10/14 计数、不重开算法。 确定性排盘核心继续 CLOSED。Batch 12N 又把 12M 中仅由韩国学中央研究院书目定位的汉阳大学馆藏提升为汉阳大学图书馆官方一手实体记录：公开 UI/API 直接绑定卷4 biblio `484926`、item `872523`、条码 `HOM000001861`、索书号 `133.3 진412ㅅ v.4`，并明确 `木板本 / 羊城明經閣 / 同治九年(1870)`、`6卷6冊` 与版式 `四周單邊、12行24字、頭註、上內向黑魚尾`。详情页自然请求的 `/resources` 接口又直接返回 HTTP 200 + `success.noRecord`，因此当前公开目录没有为该卷返回数字资源对象；这不能外推成“从未数字化”或“目标文不存在”。汉阳与 SNU 现可确认是不同馆藏实体路线，但在取得汉阳卷4《五凶神》目标页之前仍不能算独立文字/字形一票。12N 不新增候选、不改变 198/166/10/14 计数、不重开算法。Batch 12O 又把 post-12N 探测统一收口：高丽大学图书馆第一方记录 `CAT000000737166` 直接绑定另一套《新刻合倂十八飛星策天紫微斗數全集》为 `[刊寫地未詳] : 江左書林, [刊寫年未詳]` 的中国木板本、`6卷6冊`，并在中央图书馆/汉籍室以 `대학원 C10 B8 1–6` / 登记号 `465000245–465000250` 成套收藏且可阅不可外借。该馆藏在物理对象层独立于 SNU/Hanyang，但尚未取得《五凶神》目标页，因此独立文字/亥字票仍为 0；高丽大学古籍归档检索只作为访问面控制，不据非命中推断不存在。SNU 公开分享页已绑定一簑古卷四文件名但未打开预览；汉阳保管书库/原文申请页面也未证明适用于该古籍，且未提交任何申请。12O 不新增候选、不改变 198/166/10/14 计数、不重开算法。 Batch 12P 继续把独立版本线索与正文证据严格分开：Hanauction 第229回公开历史列表把 lot 134 / 稳定对象 `102923` 绑定为拍卖方描述的 `味經堂藏板` 清版木板本《新刻合倂十八飛星紫微斗數全集》6卷6册完帙，并直接渲染 `102923S.JPG` 实物缩略图；该图仅能作为低分辨率实体版本定位，不足以读取《五凶神》或“亥”字。`ac_num` 在复跑中由 120 变为 117，因此已从稳定身份中排除；商业拍卖描述也不升级为机构目录、精确刊年或文本谱系证明。12P 不新增规则候选，不改变 198/166/10/14，不重开算法。Batch 12Q 将 KOSTMA 东洋文库 TOYO_1646、Scribd 与佛珠公开预览严格分层：KOSTMA 当前第一方记录明确把 `Ⅶ-3-157 / TOYO_1646` 记为笔写本 1册100张，当前精确图片仅为 134×150 封面；Scribd 停在 CAPTCHA 且未绕过；佛珠 6 张公开预览已逐张目验，均非《五凶神》目标页。12Q 不增加独立‘亥’字票、不新增候选、不改变 198/166/10/14、不重开算法。最新历史批次见 `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-KOSTMA-TOYO1646-MANUSCRIPT-AND-SCRIBD-FOZHU-ACCESS-CONTROLS-Q.md`；候选产品化说明见 `docs/ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-PRODUCTIZATION-R1.md`。

为避免长对话触发上下文限制导致工作断层，仓库现建立固定跨对话机制：`docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 定义新对话启动顺序，`docs/PROJECT-CURRENT-STATE-R1.json` 保存机器可读当前阶段/批次/计数/下一工作重点，`scripts/verify-project-continuity-state-r1.py` 在 CI 中强制校验它与 Historical Audit Matrix 一致。新对话不再依赖旧聊天总结或旧 SHA，只需先读取 GitHub 远端最新 HEAD，再按该协议恢复工作。

- **Batch 12R (Toyo Bunko VII-3-157 detail/provenance tension):** first-party source-emitted POST targetids `502596` (寫本) and `471894` (鈔本) are now bound by exact detail-page hashes, while physical multiplicity remains unresolved and is not double-counted. NCKU 2021's `金陵益軒唐謙梓` / June-1942 scholarly provenance statement is preserved as secondary genealogy, not as proof of a printed Toyo witness or as target-glyph authority. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with zero new Hai-glyph votes and no algorithm reopen. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TOYO-VII3-157-FIRST-PARTY-DETAIL-AND-SCHOLARLY-PROVENANCE-TENSION-R.md`.

- **Batch 12S (Toyo Bunko Media Repository public search control):** first-party source-emitted general and `東洋文庫コレクション item_set_id=42942` searches were hardened against query-echo/search-self-link false positives. Run `34221594363` / artifact `10053963935` executes five target terms in both scopes; all ten HTTP-200 result pages visibly show `0 件` and expose no concrete item/document resource objects. This is only a current public repository access boundary, not a no-digitization or target-text-absence claim. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; 198/166/10/14 and all algorithm invariants remain unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TOYO-MEDIA-REPOSITORY-PUBLIC-SEARCH-ROUTE-CONTROL-S.md`.


- **Batch 12T (Naikaku/National Archives Nanyangtang provenance bridge):** direct re-review of the Batch 12A 527-page facsimile reads the old cover label `漢 / 子六十 / 一五八五六 / 全二` and `南陽堂較梓`, strongly converging with NAJ `子060-0001` / `2冊` / Ming / Red-Leaves lineage. The explicit legacy-registration `15856 -> 子060-0001` crosswalk remains unobserved, so this is a high-confidence provenance convergence and dedup closure, not a new independent textual vote or an official-NAJ target-page capture. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT and all algorithm invariants are unchanged.


- **Batch 12U (Naikaku 1971 revised-catalog crosswalk route):** NDL now provides a fixed official acquisition identity for `改訂 内閣文庫漢籍分類目録` (UP111-59 / bib `000001237342` / PID `12282052` / DOI `10.11501/12282052`), while Minna Search confirms an uncorrected OCR derivative behind legitimate access controls. A National Archives 2009 catalog-method article confirms that the revised catalog has a document-name list, but no reviewed public surface directly states `15856 -> 子060-0001`. The crosswalk therefore remains fail-closed; HPA-ZDATE-006 and all deterministic-product invariants are unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NAIKAKU-1971-REVISED-CATALOG-CROSSWALK-ACCESS-ROUTE-U.md`.


- **Batch 12V (Naikaku 1971 public page-access boundary):** exact NDL item API PID `12282052` exposes 405 page/content objects. PID-scoped NDL Lab searches for eight target terms return zero hits and the Lab full-text JSON route returns 403; separately, run `34234090185` tests 32 API-emitted page JPEG paths and every request returns 401 unauthenticated. This closes only the tested public/unauthenticated routes, not the target entry or whole catalog. The `15856 -> 子060-0001` crosswalk remains fail-closed; HPA-ZDATE-006, 198/166/10/14 and all deterministic-product invariants are unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NAIKAKU-1971-PUBLIC-PAGE-ACCESS-BOUNDARY-V.md`.


- **Batch 12W (SNU Quark v4 + Fozhu N16991 public route controls):** normal public Quark UI navigation enumerates 49/49 files and binds the exact SNU Ilsa Mingjingge 1870 volume-4 PDF object at visible size 31.5M, but the Web surface yields no direct PDF viewer/target page and no PDF bytes were acquired. Separately, six source-emitted Fozhu N16991 old-print previews were directly reviewed without OCR; none contains `五凶神` or the target late-Zi passage. The Fozhu set is byte-distinct from Batch 12Q but its physical/scan independence is unresolved, so no independent textual vote is added. HPA-ZDATE-006, 198/166/10/14 and all deterministic-product invariants remain unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SNU-QUARK-V4-AND-FOZHU16991-PUBLIC-ROUTE-CONTROLS-W.md`.

- **Batch 12X (Jiwen 1982/1999 + Dayuan 2012 copy-text routes):** 集文公開頁 binds 周祖勇's claimed privately held Qing Tongzhi-9 woodblock-reprint six-volume copy to the 1982/1999 reproduction route, while 大元 2012 exposes a 434-page handwritten copy-text route with public internal samples. The public directory surface `五神` is not silently normalized to `五凶神`; no direct target page or independent Hai-glyph witness is added. HPA-ZDATE-006 and 198/166/10/14 remain unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JIWEN-1982-1999-AND-DAYUAN-2012-COPY-TEXT-ROUTES-X.md`.

- **Batch 12Y (NCC Jiwen/Dayuan direct samples + Kamo access control):** NCC source-emitted samples for Jiwen id `995` and Dayuan id `7346` were directly reviewed without OCR. Jiwen sample spreads directly establish old-print facsimile nature; Dayuan samples directly bind handwritten copy-text pages including 30–31, 160–161 and 394–395. None is the volume-four `五凶神` target page. Exact-head Kamo run `34242503503` / artifact `10062627609` timed out on all three public routes and therefore records only a runner access boundary, not content absence. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; 198/166/10/14 and all algorithm invariants remain unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NCC-JIWEN-DAYUAN-DIRECT-SAMPLE-REVIEW-AND-KAMO-ACCESS-CONTROL-Y.md`.

- **Batch 12Z (Korea CNTS Springgang manuscript direct late-Zi collation):** National Digital Library of Korea object `CNTS-00047996572` / `KOL200100663` is now directly collated from its 153-page public-domain physical scan. The cover reads `秘傳紫微 / 春岡藏`; PDF p124 contains both `五神天殤天使奏書直符將軍` and `凡五凶神…`, proving those are different phrase roles in one manuscript passage rather than a simple missing-character correction. PDF p125 directly reads `子有十刻上五刻屬昨夜下五刻屬今夜` with no `亥` in the exact target span. This upgrades the non-Hai previous/current-night transmission to direct physical manuscript evidence and proves Nanyangtang Fullbook's explicit `昨夜亥時` is not universal across the broader received Ziwei transmission. `HPA-ZDATE-006` remains source-scoped and `MISSING_FROM_PRODUCT`; 198/166/10/14 and all algorithm invariants remain unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-KOREA-CNTS-ZIWEIDOUSHUFANGSHU-DIRECT-LATE-ZI-COLLATION-Z.md`.

- **Batch 12AA (Hui County Museum official illustrated-catalog route):** National Library Press's 2025 Hui County Museum ancient-book catalog officially binds `《新鋟希夷陳先生紫微斗數全書四卷》` at directory p233 and describes representative original-book imagery for each selected title. The public TXT route exposes only metadata/description/directory text, so no p233 image, target late-Zi glyph, or independent Hai vote is claimed. Duplicate Kumyo/Liaoning/Nanyangtang routes and Buybook access boundaries remain quarantined. `HPA-ZDATE-006`, 198/166/10/14 and all algorithm invariants remain unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-HUIXIAN-MUSEUM-OFFICIAL-ILLUSTRATED-CATALOG-ROUTE-AA.md`.

- **Batch 12AB (Jingshutang Artron physical imprint route):** Artron/Taihe Jiacheng 2017 Lot *2036 exposes an exact source-emitted 1018×903 physical photograph (SHA-256 `44c0369f078d27894579b10208f8906ed3592a814a2bc8d58a8f2760090a9685`). Direct no-OCR review reads the title page as `陳希夷先生著 / 紫微斗數全書 / 經述堂藏板`, establishing a previously unregistered `經述堂` physical imprint route distinct in observed glyphs from `繼述堂` and `經綸堂`. The photograph does not show `《論人生時要審的確》`; Kongfz object picture routes tested in the same probe redirect to login and were not bypassed. Zero textual/Hai-glyph votes are added; `HPA-ZDATE-006`, 198/166/10/14 and all algorithm invariants remain unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JINGSHUTANG-ARTRON-PHYSICAL-IMPRINT-ROUTE-AB.md`.

- **Batch 12AC (Wenguang PT165 public Viewer-response closure):** For Heart-One 2017 combined Wenguangtang facsimile `aIRbDgAAQBAJ`, exact public probes close a previously ambiguous route: `jscmd=run` returns HTTP 200 with an empty body, while `PT164/PT165/PT166 jscmd=click3` return only a 209-page metadata array. `PT165` is present as `{pid: PT165, flags: 8, order: 165}`, but no source-emitted image URL is returned and no target glyph is displayed. SearchWithinVolume's Hai reading therefore remains index-text evidence only, not physical glyph authority. Zero textual/Hai votes are added; `HPA-ZDATE-006`, 198/166/10/14 and all algorithm invariants remain unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENGUANG-PT165-PUBLIC-VIEWER-RESPONSE-CLOSURE-AC.md`.

- **Batch 12AD (Sanfenge/Quark volume-four route):** Sanfenge provider source directly binds article `212163` to `紫薇术紫薇斗数全书卷4.pdf` and Quark share `6956a639be12`, plus article `212173` to the four-volume file and share `9f7f6a4e7730`. Both public Quark URLs return HTTP 200 initial SPA shells but expose no filename/PDF bytes there; edition/imprint and target leaf remain unobserved. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; 198/166/10/14 and all algorithm invariants remain unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SANFENGE-QUARK-VOLUME4-PUBLIC-SHARE-ROUTE-AD.md`.

- **Batch 12AE (Republic Huiwentang/Jinzhang routes):** a Kongfz source-emitted physical title photo directly reads `上海會文堂書局印行`; `《重刊術藏》` binds a Republic Jinzhang lithographic Fullbook to volume 59/page 333; reviewed Artron set photos expose no direct Jinzhang imprint or late-Zi target leaf, and Jinyuan's modern TOC only locates `論人生時要審的確` at p175. Zero target-text/Hai votes; `HPA-ZDATE-006`, 198/166/10/14 and all algorithm invariants remain unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-REPUBLIC-HUIWENTANG-JINZHANG-ROUTES-AE.md`.

- **Batch 12AF (Guangyi/Yulgok direct late-Zi collation):** Yulgok's first-party tree/viewer directly binds four books `B005_01_B00320_001..004`; image `001_004` reads `上海廣益書局印行`, and image `003_003` directly shows `卷三 / 論人生時要審的確 / 如子時有十刻上五刻屬昨夜亥時下五刻屬今日子時`. This supplies a second direct Fullbook physical-edition `亥` witness after Nanyangtang, while stemmatic independence/global all-edition stability are not claimed. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; 198/166/10/14 and algorithm invariants remain unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-GUANGYI-YULGOK-DIRECT-LATE-ZI-COLLATION-AF.md`.

- **Batch 12AG (Jiaojingshanfang/Hanauction physical-edition provenance):** exact 2012 and 2026 Hanauction records bind Shanghai Jiaojingshanfang `《改良紫微斗數全書》` as a four-juan/four-book lithographic physical-edition route. The 2012 exact detail page emits two 300×225 JPEG objects, but they have not been directly visually adjudicated for the late-Zi target leaf; NCKU scholarly genealogy places the Jiaojingshanfang late edition on the Baohutang-derived line. Zero target-text/Hai votes; `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; 198/166/10/14 and all algorithm invariants remain unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JIAOJINGSHANFANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-AG.md`.


- **Batch 12AH (Jiaojingshanfang/Hanauction detail-photo visual adjudication):** direct no-OCR review of the two Batch-12AG 300×225 hashes plus archived browser HTML shows they are 第65回 auction-event scenery/video thumbnails (auction-room scene and presenter), not lot-173 target-object/detail photos. `PROV-DEFECT-010` repairs that evidence-scope misclassification forward-only while preserving the exact 2012/2026 Jiaojingshanfang auction-row provenance. Zero target-text/Hai votes; `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; Matrix remains 198/166/10/14; provenance defects are 10 confirmed / 10 repaired; chart algorithm defect/reopen/collapse remain 0. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JIAOJINGSHANFANG-HANAUCTION-DETAIL-PHOTO-VISUAL-ADJUDICATION-AH.md`.


- **Batch 12AI (Ziwei late-Zi historical time-coordinate narrowing):** exact-head probe `34322850489` / artifact `10092539912` binds Ming received institutional timekeeping to a local observational astronomical family: daytime sundial/true-Sun, nighttime stellar observation, clepsydra supplementary, and explicit geographic dependence. USNO is used only to translate a calibrated local sundial to modern apparent solar time; this does **not** select apparent solar time as the Ziwei natal runtime winner. Fullbook clock-regime inheritance, nighttime equivalence and birthplace/locality binding remain unresolved. `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`, runtime binding is `PARTIALLY_NARROWED_NOT_CLOSED`, Matrix remains 198/166/10/14, provenance defects 10/10, and chart algorithm defect/reopen/collapse remain 0. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-LATE-ZI-HISTORICAL-TIME-COORDINATE-NARROWING-AI.md`.


- **Batch 12AJ (Fullbook 羅經 timekeeping semantics):** Nanyangtang and Guangyi/Yulgok physical target pages directly agree on `如天氣陰雨之際必須羅經以定真確時候若差訛則命不凖矣`. Final decisive probe `34325691911` / artifact `10093682981` promotes Xu Guangqi et al. `《新法算書》`卷一 as the primary/near-primary Ming calendar-bureau technical control: 日晷=day, 星晷=night, 正線羅經=meridian direction, 行漏=inclement-weather supplement, with an explicit warning that exclusive compass use can create timing error. `《皇明經世文編》` is the same memorial transmission and is not double-counted; Ming `《羅經頂門針》` independently anchors 羅經 in magnetic-needle/directional semantics. Thus the Fullbook sentence does **not** directly mean “use true/apparent solar time”; `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT` and no algorithm is reopened. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-FULLBOOK-LUOJING-TIMEKEEPING-SEMANTICS-AJ.md`.


- **Batch 12AK (Gaohou Mengqiu operational bridge):** Waseda first-party physical scan of 徐朝俊《高厚蒙求》 (嘉慶12-14[1807-1809], call no. `ニ05 02158`) directly demonstrates the later instrument stack: p143 `羅經平晷` embeds compass orientation in a shadow-reading sundial; p195 `鐘表圖說自序` distinguishes daytime sundial, nighttime star/moon instruments, and cloudy/dark clock fallback, explicitly saying `所以辨子亥定支干`. This is a Qing-Jiaqing **later operational bridge only**, not a Ming Fullbook clock specification and not a true/apparent-solar runtime winner. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; no algorithm reopen. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-GAOHOU-MENGQIU-OPERATIONAL-BRIDGE-AK.md`.


- **Batch 12AL (Korea CNTS full target-section re-collation):** direct no-OCR re-review of the already-counted Korean manuscript `《紫微斗數方書》` (CNTS `00047996572`) shows p125 ends the birth-hour form `子有十刻上五刻屬昨夜下五刻屬今夜` and immediately changes topic; p126 is already a different limit-period surface. Thus the Fullbook's following `陰雨—羅經` clause is not present at this target location. This proves broader-transmission non-universality only: it does **not** make the Fullbook clause an interpolation or the Korean copy an error. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; no algorithm reopen. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-KOREA-CNTS-FULL-TARGET-SECTION-RECOLLATION-AL.md`.


- **Batch 12AM (《人子須知》 early-Ming Luojing/gnomon semantic bridge):** exact-head research run `34332573715` / artifact `10096390533` binds a 510-page GGZBCK411 facsimile (SHA-256 `80de366d62066bf73046834771a43976fdf353de6ea1704d06c46dfa568a44ba`). Commons labels the composite 隆慶三年刊 / 萬曆十一年梅墅石渠閣補刊本; CiNii `BB17866565` independently corroborates the 梅墅石渠閣 / 萬暦11 [1583] edition family but is not claimed as the same copy. Direct no-OCR review: p414 `三昧論有引`, p415 `正針縫針`, p416 `臬測以景針以氣故不能符` and `推七政之纏次皆准於臬`. This is an early-Ming shushu mechanical-semantic control, not Ziwei doctrine: compass/needle orientation remains distinct from gnomon/shadow astronomical reference and is not a standalone clock or true/apparent-solar runtime field. Fullbook `陰雨—羅經` time generation therefore remains unresolved; `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`, 198/166/10/14 and all deterministic-product invariants remain unchanged. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-RENZI-XUZHI-LUOJING-GNOMON-BRIDGE-AM.md`.


- **Batch 12AN (《完孝錄》 time-mountain bridge):** CText resource `437415` directly emits target physical locator `file=100720&page=144`; Shidian ROUTER_DATA identifies 國家圖書館 / 內府明萬曆35年刻本 and maps the target semantic section to source-emitted PageIds around global pp5607-5611. The chapter maps time sectors to mountain sectors and anchors the calculation to `太陽到處`, `逐時逐刻考驗` and `考星躔`. This explains how a 24-direction plate can carry a temporal coordinate without making the magnetic needle a clock. Target image bytes remain unavailable, so no glyph-critical correction such as `四十四山 -> 二十四山` is authorized. Fullbook inclement-weather time acquisition remains unresolved; `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`, with no runtime winner or algorithm reopen. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WANXIAOLU-TIME-MOUNTAIN-BRIDGE-AN.md`.

### Historical provenance audit — Batch 12AO

Batch 12AO completed a source-emitted five-page traversal of the current Tianji public transcription for the 1581 《新刻纂集紫微斗數捷覽》 (declared 246 chapters / 67,533 characters). Birth-time material is present, but configured Fullbook inclement-weather / 羅經 terminology is not attested on that complete current public transcription surface. This does not authorize a negative claim about the physical 1581 print, an interpolation claim, runtime winner, candidate collapse, or algorithm reopen. The reviewed Nanyangtang + Guangyi Fullbook physical clause remains source-scoped and real; cloudy/rainy current-time acquisition remains unresolved. Evidence: docs/research/ZIWEI-JIELAN-INCLEMENT-TIME-ACQUISITION-R1.json.


### Historical provenance audit — Batch 12AP

Batch 12AP repairs `PROV-DEFECT-011` without reopening chart algorithms. Batch 12AO's five Tianji aggregate pagination pages remain a valid finite nonattestation surface, but Google Books Jielan volume `rZRcCwAAQBAJ` source-emits PT49 for `陰雨` under `論十二生時難定訣`; therefore the prior transmission-level extrapolation is retracted. PT49 physical glyphs remain unobserved despite direct review of source-emitted PT47/PT48 facsimile pages and NCC/Heart-One public samples. The Fullbook-style `羅經—真確時候` cloudy/rainy current-time chain remains unresolved, so `HPA-ZDATE-006=MISSING_FROM_PRODUCT`, with no runtime winner, candidate collapse or algorithm reopen. Provenance defects are now 11 confirmed / 11 repaired. Evidence: `docs/research/ZIWEI-JIELAN-BIRTH-TIME-CHAPTER-SCOPE-CORRECTION-R1.json`.


### Historical provenance audit — Batch 12AQ

Batch 12AQ resolves the 1581 Jielan bibliographic-imprint conflict by returning to the printed 《中國古籍善本書目·子部三》 scan. Direct no-OCR review of PDF p40 shows 《新刻纂集紫微斗數捷覽四卷》 as catalog item 4051 and reads `明萬曆九年金陵書坊王洛川刻本`. The search-surface `王德川` / `4052` reading is rejected as OCR/table-alignment error; item 4052 is the adjacent 《上官拜命玉曆大全不分卷》. Taiwan NCL independently attests an unrelated Ming Jinling `王氏洛川` edition string, strengthening the bookseller-name identity without implying same-copy provenance. Repository imprint metadata remains unchanged and no new provenance defect is counted. Anhui holding stays locator-only; PT49 physical glyphs and the Fullbook cloudy/rainy time-acquisition chain remain open. Evidence: `docs/research/ZIWEI-JIELAN-BIBLIOGRAPHIC-IMPRINT-RECONCILIATION-R1.json`.


### Historical provenance audit — Batch 12AR

Batch 12AR closes the reviewed public Google Books / Google Play preview route for Jielan PT49 without promoting index OCR to glyph authority. The public Play reader directly source-emits a signed PT49 image URL; the same route returns a genuine PT48 facsimile positive control, but PT49 and PT50 return the identical visible `image not available` placeholder. English accessible mode returns 403 and the source-emitted new-Books route redirects to classic Books without a PT49 image object. The iRead runner timeout is execution-environment access-boundary only. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; 198/166/10/14 and provenance 11/11 remain unchanged. Evidence: `docs/research/ZIWEI-JIELAN-PT49-PUBLIC-PREVIEW-ACCESS-BOUNDARY-R1.json`.


## Progress — Batch 12NM

HPA-COMB-005 Shared target → Ziwei projection is audited as **MODERN_COMPATIBILITY_ONLY**. The shared projection binds the existing target-candidate identity and hashes, then replays Ziwei's own calendar/date-boundary rules; it is not a historical doctrine layer.

**PROV-DEFECT-032** repairs stale Matrix provenance: the old source scope stopped at R1.10, while current runtime also exposes separately source-scoped 1581 day-anchored flow-hour and Zhongzhou leap-month candidates. Their historical authority remains upstream and both stay `PRESERVED_NOT_SELECTED`.

Matrix220/217/10, provenance32/32, chart algorithm defects/reopens/candidate collapses0. No runtime or candidate-selection change. `transmission_impact=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-COMBINED-SHARED-TARGET-ZIWEI-PROJECTION-AUDIT-NM.md`. Research record: `docs/research/COMBINED-SHARED-TARGET-ZIWEI-PROJECTION-AUDIT-R1.json`.


## Progress — Batch 12NN

HPA-COMB-006 Combined Target Flow Fusion R2 is audited as **MODERN_COMPATIBILITY_ONLY**. R2 remains additive identity/status/hash composition over already released target-coordinate, BaZi target-flow and Ziwei selector projection outputs; it does not introduce a new placement rule or historical cross-system doctrine.

**PROV-DEFECT-033** replaces the Matrix's pending quote/document-only provenance with the live R2 composer, local endpoint, read-only Workbench and replay/uncertainty tests. `RESOLVED/UNCERTAINTY_PRESENT` remains a multiplicity/status signal, never a doctrinal winner.

Matrix220/218/10, provenance33/33, chart algorithm defects/reopens/candidate collapses0. No runtime or candidate-selection change. `transmission_impact=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-COMBINED-TARGET-FLOW-FUSION-R2-AUDIT-NN.md`. Research record: `docs/research/COMBINED-TARGET-FLOW-FUSION-R2-AUDIT-R1.json`.


## Progress — Batch 12NO

HPA-COMB-007 Resolved profile / RuleSet / algorithm lineage is audited as **MODERN_COMPATIBILITY_ONLY**. Runtime Profile/RuleSet/Algorithm identities remain reproducible software computation lineage; they are not historical source, edition, school or transmission authority.

**PROV-DEFECT-034** corrects the prior proposal to merge historical edition/school IDs into runtime lineage. Historical authority remains evidence-scoped in the Historical Provenance Matrix, external-source registry and Transmission Genealogy Graph, with explicit cross-references rather than an ID-namespace merger.

Matrix220/219/10, provenance34/34, chart algorithm defects/reopens/candidate collapses0. No runtime/profile/schema/hash/rule/candidate/algorithm change. `transmission_impact=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-COMBINED-RESOLVED-PROFILE-RULE-ALGORITHM-LINEAGE-AUDIT-NO.md`. Research record: `docs/research/COMBINED-RESOLVED-PROFILE-RULE-ALGORITHM-LINEAGE-AUDIT-R1.json`.


## Progress — Batch 12NP

HPA-COMB-008 Fact / computation / view / manifest hashes is audited as **MODERN_COMPATIBILITY_ONLY**. Runtime fact/computation/view/bundle/manifest/lineage hashes remain domain-scoped deterministic integrity identities; structural hash consistency is strengthened by full replay, which rejects locally rehashed upstream tampering.

Historical PDF/page/image/artifact checksums and edition/catalog IDs remain evidence-object provenance. They can identify exactly what was reviewed but do not by themselves prove historical date, authorship, transmission, school authority or doctrinal correctness.

**PROV-DEFECT-035** clarifies this namespace boundary and replaces the pending/non-specific Matrix source binding. No runtime/schema/hash/rule/candidate/algorithm change.

Matrix **220/220 audited**, current missing-product rows **10**, provenance **35/35**, chart algorithm defects/reopens/candidate collapses **0**. `transmission_impact=NONE`.

Next: **12NQ** post-audit reconciliation of the 10 current `MISSING_FROM_PRODUCT` rows against live runtime/product surfaces, starting with HPA-ZT-015.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-COMBINED-FACT-COMPUTATION-VIEW-MANIFEST-HASH-AUDIT-NP.md`. Research record: `docs/research/COMBINED-FACT-COMPUTATION-VIEW-MANIFEST-HASH-AUDIT-R1.json`.


## Progress — Batch 12NQ

Post-audit reconciliation keeps **HPA-ZT-015 Leap-month temporal frames** at `MISSING_FROM_PRODUCT`, but narrows the remaining gap.

The Zhongzhou half-split candidate is already productized and visible as `PRESERVED_NOT_SELECTED`; the still-missing scope is the complete leap-month temporal frame/day-one flow-day origin and daily active-address geometry. Ordinary monthly/daily projection therefore remains fail-closed.

**PROV-DEFECT-036** removes the obsolete action to implement a candidate that already exists. Matrix220/220/10, provenance36/36, chart algorithm defects/reopens/candidate collapses0. No runtime change.

Next: **12NR** reconciliation of the three Jielan 1581 source-scoped runtime candidates still marked missing from user-selectable product surfaces.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-POST-AUDIT-MISSING-PRODUCT-RECONCILIATION-LEAP-MONTH-NQ.md`.


## Progress — Batch 12NR

Post-audit reconciliation confirms that **HPA-ZIWEI-015 / 016 / 022** remain `MISSING_FROM_PRODUCT`. Jielan 1581 Kui/Yue, Fire/Bell and Mingzhu facts already exist in a deterministic source-scoped internal resolver with `PRESERVED_NOT_SELECTED`, but the resolver is not wired into package-root/public candidate-profile API or Workbench selection.

No new provenance defect was found; the existing Matrix gap descriptions remain materially correct. Matrix220/220/10, provenance36/36, chart algorithm defects/reopens/candidate collapses0. No runtime or production-default change.

Next: **12NS** reconciliation of competing Four-Transformation families and the Jielan historical dignity normalization/product boundary.

## Progress — Batch 12NS

Post-audit reconciliation confirms that **HPA-ZIWEI-014 competing Four-Transformation table families** and **HPA-ZIWEI-018 Jielan historical dignity table** both remain `MISSING_FROM_PRODUCT`, but their partial internal coverage is now stated precisely.

For Four Transformations, Jielan 1581 is already preserved in `ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATES-R1@1.1.0` and the source-scoped resolver; regression tests prove its complete ten-stem target table exactly equals current `S08_CURRENT_40_ASSIGNMENT_R1`. That does **not** close the row: the genuinely divergent received-Fullbook/Zhongzhou families still lack complete source-bound selectable candidate profiles and Workbench/API table-family selection. **PROV-DEFECT-037** repairs the stale wording that failed to distinguish this partial internal source-family coverage.

For dignity, the Jielan registry/resolver already preserves CH69/CH70 as `SOURCE_TABLE_PRESENT_NORMALIZATION_PENDING` with `runtime_normalized=false`. Production remains the distinct `OPERATIONAL-ZIWEI-DIGNITY-R4@4.0.0`; no source-faithful Jielan historical cell table has been normalized or exposed as a selectable profile. **PROV-DEFECT-038** updates the stale Matrix registry identity from Jielan `1.0.0` to live `1.1.0` without coercing ambiguous historical wording into the modern seven-grade scale.

Matrix220/220/10; provenance38/38; chart algorithm defects/reopens/candidate collapses0. No runtime/schema/hash/rule/candidate-selection/production-default change. `transmission_impact=NONE`.

Next: **12NT** — reconcile HPA-ZDATE-006 Nanyangtang Fullbook ten-ke Zi/Hai split natal birth-hour candidate against the live time-coordinate runtime/product surfaces and current source-scoped acquisition boundary.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-POST-AUDIT-FOUR-TRANSFORMATION-DIGNITY-PRODUCT-BOUNDARY-RECONCILIATION-NS.md`. Research record: `docs/research/ZIWEI-FOUR-TRANSFORMATION-DIGNITY-PRODUCT-BOUNDARY-RECONCILIATION-R1.json`.

## Progress — Batch 12NT

Post-audit reconciliation confirms **HPA-ZDATE-006 Nanyangtang Fullbook ten-ke Zi/Hai split natal birth-hour candidate** remains `MISSING_FROM_PRODUCT`.

The current natal runtime still maps local-apparent-solar **23:00..00:59 uniformly to Zi** in `NatalStructureGenerator._hour_branch_index`. `ResolvedZiweiCalculationProfile` has no natal hour-branch reclassification policy, and the time/calendar registry exposes only Ziwei calendar-date and life/body leap-month policy dimensions. Production still uses one frozen Ziwei calculation profile.

The existing historical temporal-candidate API does not close this gap: its Jielan candidate is target **flow-hour** geometry and its Zhongzhou candidate is **leap-month month assignment**. Neither is a natal upper-half-Zi→Hai branch candidate, the package root exports no Nanyangtang resolver, the combined local request exposes no Ziwei historical natal-candidate selector, and Workbench has no Nanyangtang late-Zi selector.

The historical evidence is stronger than the original Batch 12A snapshot but still does not authorize runtime selection. Nanyangtang and Guangyi directly attest the explicit Hai wording and generic upper/lower-half orientation is closed; however explicit Hai is not universal across the broader received Ziwei transmission, and the source-scoped runtime time-standard / inclement-current-time binding remains unresolved.

No new provenance defect was found. The current Matrix description is materially correct; existing `PROV-DEFECT-010` remains the already repaired Batch 12AH auction-media scope defect. Matrix220/220/10; provenance38/38; chart algorithm defects/reopens/candidate collapses0. No runtime/schema/hash/rule/candidate-selection/production-default change. `transmission_impact=NONE`.

Next: **12NU** — reconcile HPA-DAYUN-CAL-002 / 003 / 004 historical Jiaoyun calendarization and ten-year recurrence candidates against the live historical-calendar adapter contract and product surfaces.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-POST-AUDIT-NANYANGTANG-LATE-ZI-NATAL-CANDIDATE-PRODUCT-SURFACE-RECONCILIATION-NT.md`. Research record: `docs/research/ZIWEI-NANYANGTANG-LATE-ZI-NATAL-CANDIDATE-PRODUCT-SURFACE-RECONCILIATION-R1.json`.

## Progress — Batch 12NU

Post-audit reconciliation confirms **HPA-DAYUN-CAL-002 / 003 / 004** all remain `MISSING_FROM_PRODUCT`.

The repository does have a real historical-calendar boundary: `HISTORICAL-CHINESE-CALENDAR-ADAPTER-CONTRACT-R1` registers **Ming Datong** and **Qing Shixian** contexts, exposes `REALIZE_DAYUN_HANDOVER` and `ADD_CALENDAR_YEARS`, and fail-closes with `UNRESOLVED_NO_CERTIFIED_HISTORICAL_CALENDAR_ADAPTER`. But this contract is not wired into `BaziTemporalEngine`; the released engine/profile/product surface still supports only continuous and Wenzhen compatibility profiles, both with modern Gregorian operational realization.

For **HPA-DAYUN-CAL-002**, the Ming descriptor and fail-closed contract are genuine partial infrastructure, but no certified Ming arithmetic adapter, historical temporal profile or product selector exists.

For **HPA-DAYUN-CAL-003**, **PROV-DEFECT-039** was confirmed and repaired. The previous Matrix wording said the adapter contract “preserves the unresolved regime”; in fact the live registry has no Republican/Qianli descriptor. The contract vocabulary can accommodate such a future regime, but the Qianli method currently exists only as a Matrix/source candidate, not a registered historical-calendar runtime context.

For **HPA-DAYUN-CAL-004**, `ADD_CALENDAR_YEARS` and the no-Gregorian-substitution firewall exist at the contract layer, but actual Dayun recurrence in `BaziTemporalEngine` still has only `PROLEPTIC_GREGORIAN_10Y_UTC_ANNIVERSARY` and `PROLEPTIC_GREGORIAN_10Y_CHINA_STANDARD_ANNIVERSARY` branches.

All **10 current MISSING_FROM_PRODUCT rows now have explicit post-audit product-surface reconciliation**. Matrix220/220/10; provenance39/39; chart algorithm defects/reopens/candidate collapses0. No runtime/schema/hash/rule/candidate-selection/production-default change. `transmission_impact=NONE`.

Next: **12NV** — prioritize the remaining unresolved historical statuses: 30 `DISPUTED_MULTIPLE_CANDIDATES`, 11 `SOURCE_INSUFFICIENT`, and 1 `NOT_YET_FORMALIZED`; then continue the highest-value evidence closure without collapsing candidates.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-POST-AUDIT-DAYUN-HISTORICAL-CALENDAR-CANDIDATE-PRODUCT-SURFACE-RECONCILIATION-NU.md`. Research record: `docs/research/BAZI-DAYUN-HISTORICAL-CALENDAR-CANDIDATE-PRODUCT-SURFACE-RECONCILIATION-R1.json`.

## Progress — Batch 12NV

With all 10 current `MISSING_FROM_PRODUCT` rows now product-surface reconciled, the remaining Historical Audit work was re-ranked rather than treated as a flat unresolved queue.

Current unresolved historical-status inventory: **30 `DISPUTED_MULTIPLE_CANDIDATES` / 11 `SOURCE_INSUFFICIENT` / 1 `NOT_YET_FORMALIZED`**. The priority rule is now explicit: **active production output with insufficient historical provenance outranks behavior that is already fail-closed or absent from runtime**. Broad parent rows already decomposed into child rows are not selected for duplicate re-audit, and disputed candidate families are not collapsed merely to reduce status counts.

The highest-priority next target is **HPA-ZIWEI-023 — Zi/Wu Shenzhu Fire/Bell textual composite**. Strict QS correctly throws `QS_SHENZHU_ZI_WU_TEXTUAL_AMBIGUITY`, while production Wenmo resolves Zi/Wu to Fire. The 1581 Jielan historical registry explicitly preserves `TEXTUAL_COMPOSITE_FIRE_BELL_NOT_UNIQUELY_ARBITRATED` from CH32 and its source-scoped resolver selects no winner. This creates a higher active-output provenance risk than fail-closed HPA-ZT-016.

Next tiers are HPA-ZIWEI-026 Jiangqian temporal/source scope, HPA-ZMINOR-020 standalone Feilian identity collision, then the active month-table source gaps HPA-ZMINOR-023/024/025/026. HPA-ZT-016 remains important but runtime currently emits no inward/outward direction, so its immediate deterministic-output risk is lower.

No Matrix status, runtime, candidate selection, production default, provenance count or transmission graph changed. Matrix220/220/10; provenance39/39; algorithm defects/reopens/candidate collapses0.

Next: **12NW — HPA-ZIWEI-023 Zi/Wu Shenzhu Fire/Bell evidence closure**. A Fire or Bell winner remains forbidden unless edition/source/commentary evidence actually closes it.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-UNRESOLVED-HISTORICAL-STATUS-PRIORITIZATION-NV.md`. Research record: `docs/research/HISTORICAL-UNRESOLVED-STATUS-PRIORITIZATION-R1.json`.

## Progress — Batch 12NW

HPA-ZIWEI-023 **Zi/Wu Shenzhu Fire/Bell textual composite** remains `SOURCE_INSUFFICIENT`.

The 1581 Jielan source still reads `子午生人铃火宿` and then glosses Zi/Wu as `火铃为身主`; the received Fullbook corpus likewise preserves `火玲/火铃` composite wording. Nothing in those source surfaces uniquely selects Fire. Public modern commentary does not close the gap: one editorial surface calls `火玲星` the base reading and Fire the common reading, while another current rules surface maps Zi/Wu to Bell. These are modern interpretation/compatibility surfaces, not Ming textual arbitration.

The repository boundary is now explicit. Strict QS continues to raise `QS_SHENZHU_ZI_WU_TEXTUAL_AMBIGUITY`; the Jielan sidecar keeps `TEXTUAL_COMPOSITE_FIRE_BELL_NOT_UNIQUELY_ARBITRATED` and `winner_selected=false`; production still maps Zi/Wu to Fire. Existing Wenmo role fixtures do **not** independently test Zi/Wu Shenzhu: the role fixture observes a Si-year Tianji binding, while Zi-year fixtures only discriminate the separately placed Fire/Bell stars.

**PROV-DEFECT-040** repaired a documentation/provenance-scope overclaim: `WenmoDefaultRoleGenerator` previously described the full table as matching Wenmo's default convention without identifying the unverified Zi/Wu branch pair. The runtime docstring/comment now records Zi/Wu Fire as an operational compatibility default inherited from S01 normalization, not historical closure or independently observed Wenmo compatibility.

No role value, source_refs tuple, rule-set identity, fact/computation hash, candidate selection or chart algorithm changed. Matrix220/220/10; provenance40/40; chart algorithm defects/reopens/candidate collapses0. `transmission_impact=NONE`.

Next: **12NX — HPA-ZIWEI-026 Jiangqian temporal/source-scope evidence closure**.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZI-WU-SHENZHU-FIRE-BELL-EVIDENCE-CLOSURE-NW.md`. Research record: `docs/research/ZIWEI-ZI-WU-SHENZHU-FIRE-BELL-EVIDENCE-CLOSURE-R1.json`.

## Progress — Batch 12NX

`HPA-ZIWEI-026` **Jiangqian twelve-member trine-wang ring and temporal/source scope** remains `SOURCE_INSUFFICIENT`.

The runtime boundary is now explicit: `RING.JIANGQIAN12` is a natal fact. `ZiweiChartFoundation` passes `structure.ziwei_birth_year_branch` into `WenmoDefaultRingGenerator.jiangqian()`, which applies the four trine-wang anchors and the fixed twelve-member forward order. No annual-target ring is currently materialized.

Historical/received evidence requires a separate temporal-scope distinction. The 1581 Jielan line has an explicitly titled `定流年太岁所值凶星图` chapter whose 驿马 rule is computed from the year-branch trine; this closes an early Ziwei **flow-year related shensha context**, but the reviewed public chapter does not contain the complete Jiangqian twelve-member sequence. A modern Zhongzhou received manual does preserve the complete `将星三合起旺地...指背咸池月煞亡` sequence, and modern derived rule surfaces apply the same geometry both to birth-year and flow-year branches.

Therefore natal and annual use are **distinct temporal applications, not mutually exclusive winner candidates**. The existence of the annual layer does not authorize rewriting the natal ring, while the natal product does not erase annual practice. The unresolved gate is narrower: an edition-bound early complete twelve-member Jiangqian passage plus explicit scope instruction remains unclosed.

No new provenance defect was confirmed because Batch 12MV already required separately sourced annual-target implementation. Provenance remains 40/40. No runtime/profile/schema/hash/rule/candidate/chart-algorithm change; Matrix 220/220 audited / 10 current missing; chart algorithm defects/reopens/candidate collapses 0. `transmission_impact=NONE`.

Next: **12NY — HPA-ZMINOR-020 standalone Feilian identity collision**, preserving identity boundaries among Boshi 飞廉, year-branch 蜚廉 and same-coordinate facts.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JIANGQIAN-TEMPORAL-SOURCE-SCOPE-EVIDENCE-CLOSURE-NX.md`. Research record: `docs/research/ZIWEI-JIANGQIAN-TEMPORAL-SOURCE-SCOPE-CLOSURE-R1.json`.

## Progress — Batch 12NY

`HPA-ZMINOR-020` **standalone 蜚廉 birth-year-branch table vs 博士十二神 飞/蜚廉 identity** is upgraded from `SOURCE_INSUFFICIENT` to `HISTORICALLY_SUPPORTED` for the standalone placement geometry.

The current `STAR.FEILIAN` table matches the premodern received year-deity rule **12/12**. Cao Zhengui's `历事明原` Feilian passage explicitly cites `广圣历` for the table; the 1713 `御定星历考原` repeats the same twelve positions; the Qing `钦定协纪辨方书` again repeats them and explains the reverse traversal through trine 生/旺/墓 states. The Songshi bibliography separately records Miao Rui's `新删定广圣历` in two juan, but the exact cited recension remains unresolved and is not treated as directly reviewed rule text.

Identity remains fail-closed. `STAR.FEILIAN` is keyed by birth-year branch. `RING.BOSHI12.FEILIAN` is ordinal 6 from Lucun, hence the Lucun-opposite palace regardless of ring direction. Across all 60 legal Jiazi, only 甲子、乙丑、庚午、辛未 happen to share coordinates. Same/variant glyph or coordinate coincidence does not merge the two facts.

The transmission graph now records the premodern calendrical Feilian rule family, explicit Guangshengli citation layer, Qing transmission witnesses, and a disproved same-mechanical-rule edge against the Ziwei Boshi member. What remains open is the **Ziwei adoption path**, not the standalone geometry.

No runtime/profile/rule-set/hash/candidate change and no algorithm reopen. Matrix remains 220/220 audited / 10 current missing; provenance defects 40/40; chart algorithm defects/reopens/candidate collapses 0. Status distribution becomes HISTORICALLY_SUPPORTED 95 and SOURCE_INSUFFICIENT 10.

Next: **12NZ — HPA-ZMINOR-023 month Jieshen/Yuejie provenance**, preserving the month-table identity separately from year-based 解神/年解.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-STANDALONE-FEILIAN-HISTORICAL-IDENTITY-CLOSURE-NY.md`. Research record: `docs/research/ZIWEI-STANDALONE-FEILIAN-HISTORICAL-IDENTITY-CLOSURE-R1.json`.

## Progress — Batch 12NZ

`HPA-ZMINOR-023` **month-based 解神 / 月解** is upgraded from `SOURCE_INSUFFICIENT` to `HISTORICALLY_SUPPORTED` for its month geometry.

The current table `正二申、三四戌、五六子、七八寅、九十辰、十一十二午` matches premodern received calendrical tradition **12/12**. `历事明原` defines 解神 as a month deity and attributes the table to `历例`; the 1713 `御定星历考原` and Qing `钦定协纪辨方书` preserve a clean exact table, while `协纪辨方书` also supplies the opposing-yang-branch mechanical explanation. The Lishimingyuan public transcription has OCR noise, so it is not used alone for glyph adjudication.

Identity remains separated from `HPA-ZMINOR-006`: received Ziwei also has a year-based 解神 rule, represented in the product as `STAR.NIANJIE / 年解`. Month 解神 is keyed by lunar month; year 解神 is keyed by birth-year branch. The product label 年解 is a modern disambiguation label and is not back-projected as fixed ancient terminology.

The transmission graph now records the month Jieshen rule family, explicit `总要历` / `历例` citation layers, three premodern/Qing transmission passages, parallel coexistence with the year rule, and a DISPROVED same-mechanical-rule non-edge. Exact cited-source identities and the Ziwei adoption route remain open.

No runtime/profile/rule-set/hash/candidate change and no algorithm reopen. Matrix 220/220 audited / 10 current missing; provenance defects 40/40; chart algorithm defects/reopens/candidate collapses 0. Status distribution becomes HISTORICALLY_SUPPORTED 96 and SOURCE_INSUFFICIENT 9.

Next: **12OA — HPA-ZMINOR-024 Tianwu lunar-month table**. First mechanically test whether the premodern phrase `常居月建前二辰` reproduces the runtime four-palace table; same-name evidence alone is insufficient.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-MONTH-JIESHEN-HISTORICAL-IDENTITY-CLOSURE-NZ.md`. Research record: `docs/research/ZIWEI-MONTH-JIESHEN-HISTORICAL-IDENTITY-CLOSURE-R1.json`.


## Progress — Batch 12OA

`HPA-ZMINOR-024` **Tianwu lunar-month table** remains `SOURCE_INSUFFICIENT`.

Premodern same-name Tianwu is now mechanically separated from the current Ziwei rule. `历事明原`, the 1713 `御定星历考原`, and Qing `钦定协纪辨方书` preserve Tianwu as a calendrical month deity with `常居月建前二辰`. The Xingli Kaoyuan neighborhood disambiguates that phrase through explicit Fude examples as month-build branch plus two positions.

Replaying that mechanic gives `辰巳午未申酉戌亥子丑寅卯` for lunar months 1..12. Current `STAR.TIANWU` uses `巳申寅亥` repeated every four months. The tables match only in months 8 and 11 (**2/12**) and differ in the other ten months. The classical Tianwu homonym is therefore **disproved as the direct mechanical source** of the current Ziwei four-horse table.

This is source-domain closure, not an algorithm change. The historical calendrical Tianwu remains valid in its own tradition; the current Ziwei table still lacks an edition-bound premodern Ziwei placement witness. Same name and two coordinate coincidences do not authorize identity collapse.

No runtime/profile/rule-set/hash/candidate/default change and no algorithm reopen. Matrix remains 220/220 audited / 10 current missing; provenance defects 40/40; status distribution remains HISTORICALLY_SUPPORTED 96 / SOURCE_INSUFFICIENT 9 / DISPUTED_MULTIPLE_CANDIDATES 30 / NOT_YET_FORMALIZED 1.

Next: **12OB — HPA-ZMINOR-025 Tianyue lunar-month twelve-value table**, preserving the source-domain firewall against 天月德 / 天月德合 and other homonyms.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TIANWU-HOMONYM-MECHANICAL-SEPARATION-OA.md`. Research record: `docs/research/ZIWEI-TIANWU-HOMONYM-MECHANICAL-SEPARATION-R1.json`.


## Progress — Batch 12OB

`HPA-ZMINOR-025` **Tianyue lunar-month twelve-value table** remains `SOURCE_INSUFFICIENT`.

The current mnemonic `一犬二蛇三在龙，四虎五羊六兔宫，七猪八羊九在虎，十马冬犬腊寅中` is stable across modern Ziwei received material. A current open-source implementation reproduces the same table while explicitly marking the classical provenance as `古籍待考、后世悬曜增补`. These are useful modern compatibility witnesses, not premodern authority.

The source-domain firewall is explicit: `三命通会` Tian-De / Yue-De / Tian-Yue-De-He material belongs to a different shensha/day-selection rule family and is not merged with `STAR.TIANYUE_MOON` merely by lexical proximity.

No edition-bound premodern Ziwei exact-table witness was established in the reviewed public surfaces, so the row is not upgraded. This non-finding is scoped to the reviewed search surface and is not an absolute assertion that no earlier witness exists.

No runtime/profile/rule-set/hash/candidate/default change and no algorithm reopen. Matrix remains 220/220 audited / 10 current missing; provenance defects 40/40; status distribution remains HISTORICALLY_SUPPORTED 96 / SOURCE_INSUFFICIENT 9 / DISPUTED_MULTIPLE_CANDIDATES 30 / NOT_YET_FORMALIZED 1.

Next: **12OC — HPA-ZMINOR-026 Yinsha lunar-month six-value cycle**.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TIANYUE-MODERN-RECEIVED-SOURCE-BOUNDARY-OB.md`. Research record: `docs/research/ZIWEI-TIANYUE-MODERN-RECEIVED-SOURCE-BOUNDARY-R1.json`.


## Progress — Batch 12OC

`HPA-ZMINOR-026` **Yinsha lunar-month six-palace cycle** remains `SOURCE_INSUFFICIENT`.

The current cycle `正七寅、二八子、三九戌、四十申、五十一午、六十二辰` is stable in modern Ziwei received material. A modern open-source implementation reproduces the exact cycle and explicitly marks its provenance as `古籍待考、后世悬曜增补`. This is useful evidence for modern compatibility and source uncertainty, not premodern authority.

No qualifying premodern Ziwei exact-cycle witness was established in the reviewed public surfaces. Same-name Yinsha material from other systems remains outside this rule identity unless input dimension and placement mechanics can be bridged explicitly.

No runtime/profile/rule-set/hash/candidate/default change and no algorithm reopen. Matrix remains 220/220 audited / 10 current missing; provenance defects 40/40; status distribution remains HISTORICALLY_SUPPORTED 96 / SOURCE_INSUFFICIENT 9 / DISPUTED_MULTIPLE_CANDIDATES 30 / NOT_YET_FORMALIZED 1.

Next: **12OD — re-rank the remaining SOURCE_INSUFFICIENT / NOT_YET_FORMALIZED work queue after completing the active month-table provenance trio.**

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YINSHA-MODERN-RECEIVED-SOURCE-BOUNDARY-OC.md`. Research record: `docs/research/ZIWEI-YINSHA-MODERN-RECEIVED-SOURCE-BOUNDARY-R1.json`.


## Progress — Batch 12OD

After 12NZ–12OC, unresolved work is re-ranked rather than continued by row number. Current inventory remains **30 DISPUTED_MULTIPLE_CANDIDATES / 9 SOURCE_INSUFFICIENT / 1 NOT_YET_FORMALIZED**.

The remaining source-insufficient set is now mostly decomposed parents, recently source-bounded month rows, non-semantic display ordering, fail-closed/absent behavior, or rows already deeply audited in 12NW/12NX. Its marginal closure value is lower than active disputed production selections.

The next priority therefore shifts back to the disputed queue. **HPA-ZMINOR-022 YueDe** is selected first: production currently uses the Zi-year-Si-start family, while received Fullbook preserves a competing Zi-start family, and temporal scope still needs explicit typing. This is a compact, directly product-relevant candidateization problem.

Second tier: HPA-ZMINOR-008 TianShou Body/Life basis and HPA-ZMINOR-007 TianChu competing tables. High-impact late-Zi/date-boundary families remain important but already have extensive candidate preservation and historical-coordinate audits.

No Matrix status, runtime, default, candidate selection or algorithm changed.

Next: **12OE — HPA-ZMINOR-022 YueDe Si-start vs Zi-start historical families and natal/flow temporal candidate closure**.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-UNRESOLVED-HISTORICAL-STATUS-REPRIORITIZATION-OD.md`. Research record: `docs/research/HISTORICAL-UNRESOLVED-STATUS-REPRIORITIZATION-OD-R1.json`.


## Progress — Batch 12PB

All fifteen Ming Datong pre-year Runyu candidates are now bound to civil/regnal chronology. The research generator no longer assumes `k=2` is civil 正月: a civil year is the first regular month 1 through immediately before the next regular month 1, preserving late leap 11/leap 12 ownership. The oracle binds 1384 leap10, 1403 leap11, 1422 leap12, 1441 leap11, 1460 leap11, 1479 leap10, 1498 leap11, 1517 leap12, 1536 leap12, 1555 leap11, 1574 leap12, 1593 leap11, 1612 leap11, 1631 leap11 and 1642 leap11.

The 12PB harness checks 15 q=0/1 pre-year controls × 4 research precision profiles = 60 controls. Those controls all match. The full 1368–1644 rerun is profile-stable, but it exposes 10 remaining mismatches between a provisional quotient-based owner mapping and the final no-Zhongqi civil-year structure. Because the received rule explicitly allows `閏有進退` and makes `定朔無中氣` final, `MD-G09-MULTI-YEAR-LEAP-GENERALIZATION` remains open. No historical runtime is activated: G03/G05/G07/G08/G09 remain open and G10/G11 dependency-blocked, so `HPA-DAYUN-CAL-002` stays `MISSING_FROM_PRODUCT` and the fail-closed adapter remains mandatory.

No production algorithm/default/candidate selection changed; algorithm reopens/candidate collapses remain zero.

Next: **12PC — MD-G09 Runyu 進退 / 定朔無中氣 final-placement boundary**. The G03 physical qishuo evidence already acquired from the complete Kyujanggak `GK12437_00` witness is retained for the following batch.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-MING-DATONG-PREYEAR-LEAP-CIVIL-YEAR-GLOBAL-VALIDATION-PB.md`. Research record: `docs/research/MING-DATONG-PREYEAR-LEAP-CIVIL-YEAR-GLOBAL-VALIDATION-R1.json`.


## Progress — Batch 12PC

The final Runyu `進退` boundary is now source-scoped closed. All ten q=2 threshold labels are historically controlled: five retreat to the preceding civil year and five remain in the threshold-label year. The split disproves any universal q=2 ownership shortcut and confirms that the final owner must follow the old-Datong `定朔無中氣` structure.

The 12PC harness checks **40/40 q=2 profile-controls**, **102 Runyu threshold labels**, unique final owners, zero 1368–1644 profile-structural divergence and zero final-owner/existence mismatch through 1368–1643. `MD-G09-MULTI-YEAR-LEAP-GENERALIZATION` therefore closes source-scoped forward-only.

No historical runtime is activated. G03/G05/G07/G08 remain open and G10/G11 dependency-blocked; `HPA-DAYUN-CAL-002` remains `MISSING_FROM_PRODUCT`. No production algorithm/default/candidate selection changed.

Next: **12PD — MD-G03 qishuo geographic reference**, using the already re-acquired complete Kyujanggak `GK12437_00` physical method block.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-MING-DATONG-RUNYU-JINTUI-FINAL-PLACEMENT-PC.md`. Research record: `docs/research/MING-DATONG-RUNYU-JINTUI-FINAL-PLACEMENT-R1.json`.


## Progress — Batch 12PD

The already-acquired complete Kyujanggak `GK12437_00 / 大統曆日通軌` physical capture has now been reused for a direct, no-OCR qishuo locality-operator audit. Viewer `002b` visibly carries `求經朔分`; `004b-005a` carries `求定朔及望分`; `006a` is already the opening `大陽冬至前後二象盈初縮末限` table, fixing `001a-005b` as the complete reviewed pre-table method block.

Within that reviewed method block, no explicit named-place, `里差/地差`, longitude, Dadu/Beijing, Nanjing, Yingtian or Shuntian correction step is attested. This closes only the **explicit locality-operator subquestion**. It does not prove geographic neutrality, identify an implicit meridian, or authorize inheritance from Nanjing sunrise/daylength modules.

`MD-G03` therefore remains `OPEN_BLOCKING_GENERAL_ADAPTER`; the live ledger stays **5 closed / 4 open / 2 dependency-blocked**, `HPA-DAYUN-CAL-002` remains `MISSING_FROM_PRODUCT`, and the historical adapter remains fail-closed.

Next: **12PE — cross-collate Shoushi → early Datong/Tonggui → GK12437 → Zhou Xiang 1569 qishuo constants/epoch/method lineage for a direct named-place or inherited-coordinate binding.**

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-MING-DATONG-GK12437-QISHUO-LOCALITY-OPERATOR-AUDIT-PD.md`. Research record: `docs/research/MING-DATONG-GK12437-QISHUO-LOCALITY-OPERATOR-AUDIT-R1.json`.

## Progress — Batch 12PE

Direct GK12437 pages 001a–002a now bind the 至元辛巳 epoch to the revised Tonggui response-constant state (氣應 550600 / 閏應 202050 / 轉應 130205 / 交應 260388).

《元史》卷54 explicitly separates 立元 from 諸應 by stating that the latter are 隨時推測、不用為元. 《明史》卷35 identifies Tonggui 閏/轉/交應 as 授時續定之數, while 《高麗史》卷51 preserves the same epoch with a mixed old/new response-constant recension.

Therefore the shortcut same 至元辛巳 epoch => same Dadu qishuo meridian is rejected. Dadu/Beijing remains possible but unproved; Nanjing remains possible but unproved; mixed module geography is strengthened but not selected.

MD-G03 stays open; live accounting remains 5 closed / 4 open / 2 dependency-blocked, and HPA-DAYUN-CAL-002 remains fail-closed.

Next: 12PF — observation-site / coordinate provenance of the revised 閏轉交應 layer.

Batch document: docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-MING-DATONG-SHOUSHI-QISHUO-EPOCH-RESPONSE-CONSTANT-LINEAGE-PE.md. Research record: docs/research/MING-DATONG-SHOUSHI-QISHUO-EPOCH-RESPONSE-CONSTANT-LINEAGE-R1.json.

## Progress — Batch 12PF

12PF follows the later tradition that Guo Shoujing revised 閏/轉/交應 after a Zhiyuan-31 fifth-month full-moon eclipse discrepancy. The trigger itself is preserved only in later received historical text and still carries no site label.

Yuan official evidence now closes a different but important point: the Shoushi observing system was not Dadu-only. In 1279 a 司天臺 was established at Dadu while Shangdu, Luoyang and other sites also received instruments and observing officials. In 1294 the emperor was at Shangdu during the target fifth month, when the chronicle also records astronomy-related rites at 司天臺 / 雲仙臺. Guo was 知太史院事 that year, but no reviewed Yuan source binds the eclipse observation or revised constants to either Dadu or Shangdu.

Therefore DADU_AS_UNIQUE_YUAN_OBSERVATION_SITE is rejected, while the actual 1294 revision site and qishuo geographic reference remain unresolved. MD-G03 stays open; live accounting remains 5 closed / 4 open / 2 dependency-blocked; HPA-DAYUN-CAL-002 remains fail-closed.

Next: 12PG — trace surviving quotations or catalog/excerpt evidence from 郭守敬《修改源流》《古今交食考》 and Yuan Taishiyuan records for the 1294 revision log/site.

Batch document: docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-MING-DATONG-1294-REVISED-YING-OBSERVATION-SITE-PROVENANCE-PF.md. Research record: docs/research/MING-DATONG-1294-REVISED-YING-OBSERVATION-SITE-PROVENANCE-R1.json.

## Progress — Batch 12PG

郭守敬 lost-work route is now bibliographically firewalled before quote hunting. 《元史》郭守敬傳 and 《千頃堂書目》 both give 《修改源流》一卷 and 《古今交食考》一卷; the later 《新元史》 alone gives 《修改源流》七卷, so seven juan is preserved only as a late variant.

《古今交食考》 is also a homonym trap: late-Ming 崇禎曆書 and 朱載堉 calendrical material use the same title for different works. Title-only matching is now forbidden.

No direct public text of Guo's two works was recovered on the reviewed horizon, and 並藏之官 is treated as historical custody rather than present-survival proof. No 1294 site evidence was gained; MD-G03 remains open and HPA-DAYUN-CAL-002 remains fail-closed.

Next: 12PH — hunt source-bound quotations/paraphrases explicitly traceable to Guo's lost works, especially 至元三十一年五月望 / 差天二刻 / 三應改定 and site/clock wording.

Batch document: docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-GUOSHOUJING-LOST-WORKS-BIBLIOGRAPHIC-SURVIVAL-CONTROL-PG.md. Research record: docs/research/GUOSHOUJING-LOST-WORKS-BIBLIOGRAPHIC-SURVIVAL-CONTROL-R1.json.

## Progress — Batch 12PH

Explicit source-marker searching did not recover a quotation from 郭守敬《修改源流》 or 郭氏《古今交食考》 for the Zhiyuan-31 three-response revision. 邢雲路, 《明史稿》 and 《明史》 preserve convergent later narratives, but the reviewed passages do not bind that narrative to either lost work and do not add an observation-site word.

Therefore CONTENT_SIMILARITY != LOST_WORK_QUOTATION is now an explicit provenance firewall. The repeated generic lost-work title route is parked unless materially new evidence appears.

MD-G03 remains OPEN_BLOCKING_GENERAL_ADAPTER; live accounting stays 5 closed / 4 open / 2 dependency-blocked; HPA-DAYUN-CAL-002 remains MISSING_FROM_PRODUCT and runtime remains fail-closed.

Next: 12PI — research-only diagnostic replay of source-bound official Ming almanac conjunction clock labels under inherited/no-shift, Dadu-Beijing and Nanjing geographic hypotheses.

Batch document: docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-GUOSHOUJING-LOST-WORK-QUOTATION-CHAIN-AUDIT-PH.md. Research record: docs/research/GUOSHOUJING-LOST-WORK-QUOTATION-CHAIN-AUDIT-R1.json.

## Progress — Batch 12PI

The 56 official-Ming-almanac conjunction-time controls have now been audited for geographic identifiability. D1 matches 56/56 source bins in the unshifted historical coordinate; mechanically applying the modern Beijing–Nanjing ~9.87-minute longitude delta leaves 22/56 matches in one direction and 17/56 in the other, with zero day-boundary crossings. The nearest sampled event is still about 17.28 minutes from 子正.

This does not select an unshifted/Beijing/Nanjing meridian. D1 and the printed bins share the same unknown historical coordinate, so internal fit can validate the algorithm but cannot identify the absolute geographic zero point.

MD-G03 remains open; HPA-DAYUN-CAL-002 stays MISSING_FROM_PRODUCT and runtime remains fail-closed.

Next: 12PJ — audit the feasibility and uncertainty of an independent absolute-time anchor (modern ephemeris/Delta-T/local apparent solar time or a primary site-bound astronomical observation).

Batch document: docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-MING-DATONG-QISHUO-GEOGRAPHIC-IDENTIFIABILITY-AUDIT-PI.md. Research record: docs/research/MING-DATONG-QISHUO-GEOGRAPHIC-IDENTIFIABILITY-AUDIT-R1.json.

## Progress — Batch 12PJ

Modern absolute-time anchoring is technically feasible for the Ming qishuo problem: JPL DE431 covers the full target period, and NASA's ~20-second ΔT uncertainty for 1300–1600 is far smaller than the ~592-second Beijing–Nanjing longitude signal.

The remaining blocker is historical clock semantics, not modern ephemeris precision. Apparent versus mean solar time can differ by as much as ~16 minutes, and the project has not source-closed whether Datong qishuo 子正/刻 is apparent solar, mean solar, calibrated clepsydra, or another conventional coordinate attached to a named longitude.

MD-G03 therefore remains open; HPA-DAYUN-CAL-002 remains MISSING_FROM_PRODUCT and runtime stays fail-closed.

Next: 12PK — direct historical audit of qishuo 子正/刻 absolute time-standard semantics.

Batch document: docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-MING-DATONG-QISHUO-ABSOLUTE-TIME-ANCHOR-FEASIBILITY-PJ.md. Research record: docs/research/MING-DATONG-QISHUO-ABSOLUTE-TIME-ANCHOR-FEASIBILITY-R1.json.

## Progress — Batch 12PK

Shoushi/Datong qishuo time semantics are now split into two layers. The internal layer is source-closed: 日周=10000 is converted into 12 shichen / 100-ke labels by `推發斂加時`, counted from 子正. The absolute realization layer remains open: the qishuo method does not directly identify this coordinate as local apparent solar time, local mean solar time, a measured clepsydra reading, or a named-longitude standard.

Shoushi separately has explicit locality-sensitive day/night and clepsydra machinery; Zhu Zaiyu's late-Ming critique also confirms Dadu-vs-Nanjing module geography. A cross-calendar positive control in Yuan-shi volume 56, the distinct 庚午元曆, explicitly applies `尋斯干城` + `里差` to new-moon remainders, demonstrating what an explicit geographic correction looks like without importing it into Shoushi/Datong.

MD-G03 remains open; HPA-DAYUN-CAL-002 remains MISSING_FROM_PRODUCT and runtime remains fail-closed.

Next: **12PL — Ming Qintianjian institutional almanac clock-standard / capital-binding audit**.

Batch document: docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-MING-DATONG-QISHUO-ZIZHENG-CLOCK-STANDARD-SEMANTICS-PK.md. Research record: docs/research/MING-DATONG-QISHUO-ZIZHENG-CLOCK-STANDARD-SEMANTICS-R1.json.


## Progress — Batch 12PL

Ming institutional evidence now closes a narrower question without overreaching. (萬曆)《大明會典》卷223 places official 譙樓漏刻/time service, eclipse 分秒時刻 reporting and annual 《大統曆》 production under the same 欽天監, and records 嘉靖七年「測晷以定氣朔」. This proves institutional coupling, not a single absolute time coordinate.

《明史》卷31 supplies the decisive firewall: after the capital moved to Shuntian, the day/night module continued using Yingtian values and even after a temporary Shuntian substitution could be restored to the older convention. Therefore CURRENT_CAPITAL != AUTOMATIC_REFERENCE_FOR_ALL_CALENDAR_TIME_MODULES.

MD-G03 remains open; HPA-DAYUN-CAL-002 remains MISSING_FROM_PRODUCT and runtime stays fail-closed. Modern ephemeris longitude fitting is still unauthorized.

Next: **12PM — audit the observation/clock semantics behind 嘉靖七年「測晷以定氣朔」 and related Qintianjian verification records for an explicit local-observation -> numerical 定朔/合朔 bridge.**

Batch document: docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-MING-DATONG-QINTIANJIAN-ALMANAC-CLOCK-CAPITAL-BINDING-PL.md. Research record: docs/research/MING-QINTIANJIAN-ALMANAC-CLOCK-CAPITAL-BINDING-R1.json.


## Progress — Batch 12PM

Jiajing observational evidence now closes another semantic boundary without inventing a meridian. 《明史·天文志》 records 嘉靖七年「立四丈木表以測晷影，定氣朔」 and immediately says the observatory system was 「一以元法為斷」. The safe inference is calendar calibration/verification purpose, not a direct gnomon-shadow -> 定朔 numeric conversion.

The Jiajing-2 Hua Xiang program independently places 合朔 among the outputs to be verified through year-long observatory measurement and record keeping. This confirms observational verification semantics but still exposes no local-clock/longitude operator for qishuo.

MD-G03 remains open; HPA-DAYUN-CAL-002 remains MISSING_FROM_PRODUCT; runtime and modern ephemeris meridian fitting stay fail-closed.

Next: **12PN — audit the Jingtai-1 lunar-eclipse record contrasting actual 卯正三刻 with the bureau prediction 辰初初刻, and determine whether the actual time is a contemporaneous observed capital-clock value suitable as an independent absolute anchor.**

Batch document: docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-MING-DATONG-QISHUO-GNOMON-OBSERVATION-BRIDGE-PM.md. Research record: docs/research/MING-DATONG-QISHUO-GNOMON-OBSERVATION-BRIDGE-R1.json.
