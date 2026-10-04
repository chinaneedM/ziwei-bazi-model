# Fusion Chart Historical Provenance Audit R1 — Batch 12MN

## 目标层纳音、旬空、十二长生：继承身份投影分解

Status: **HPA-BAZI-FLOW-004 DECOMPOSED / HPA-BAZI-FLOW-008..010 AUDITED / CHART ALGORITHM UNCHANGED**

本批不把“大运→小运候选→流年→流月→流日→流时”的现代软件组合倒推成古籍原有的统一七层教义，而是把 HPA-BAZI-FLOW-004 拆成三个可独立追溯的只读身份投影：纳音、旬空、十二长生。历史权威仍由已经审结的 HPA-BAZI-006/007/008 各自承担，动态层只是合法目标干支的现代消费者。

### 三个继承边界

| 子规则 | 运行时锚点 | 继承父规则 | 本批禁止推出 |
| --- | --- | --- | --- |
| HPA-BAZI-FLOW-008 纳音 | 目标合法干支 | HPA-BAZI-006 | 强弱、吉凶、事件、层级特权 |
| HPA-BAZI-FLOW-009 旬空 | 目标合法干支所属六旬 | HPA-BAZI-007 | 空亡吉凶、应期、事件解释 |
| HPA-BAZI-FLOW-010 十二长生 | 本命日主→目标支；目标干→目标支，两视图分开 | HPA-BAZI-008 | 把阶段名直接等同旺衰、用神、格局或预测 |

现行 `temporal_classical_annotation` 在任何组件运行前先要求目标值属于六十甲子；因此 120 个干支笛卡尔组合中的 60 个非法奇偶组合不会进入纳音/旬空/十二长生投影。十二长生的 `day_master_twelve_growth` 继续使用真实本命日主，`self_twelve_growth` 则使用目标干自身；两者不是可互换锚点。两套小运候选继续并存且不选赢家，未进入正式大运时也不伪造大运干支。

### 重放范围

新增独立继承审计测试，不用运行时源码生成第二套古籍“权威表”，而是检查动态消费者是否逐项等于已审父 API：

- 10 个本命日主 × 60 个合法目标干支 = 600 个直接注记坐标；
- 同一 600 个坐标各展开 7 个已解析槽位（大运、两套小运候选、年、月、日、时）= 4,200 个动态注记；
- 纳音、旬空、本命日主十二长生、目标自身十二长生分别完成 4,800 次父 API 对照（600 直接 + 4,200 槽位）；
- 10 个本命日主 × 60 个非法干支 = 600 次前置拒绝控制；
- 另保留未入大运与两套小运候选控制。

本批新增 5 项审计测试。提交创建之前不存在该提交自己的 exact-head CI，因此研究记录明确把该状态写为 `PENDING_BY_DEFINITION`；推送后的 GitHub Actions 才是该提交的远端验证事实源，本文不拿前一提交的 CI 冒充本批 CI。

### profile 描述同步

运行时 `BAZI-TEMPORAL-CLASSICAL-ANNOTATION-PROJECTION-R1` 自 Batch 11A 后已经是 `1.0.2`，但 HPA-BAZI-FLOW-004 的 Matrix 描述仍停在 `1.0.1`。本批把描述同步到实际值。根因就是已经计入的 `PROV-DEFECT-009`（隐藏干顺序从 FactHash 转为 computation lineage 时发生的 profile bump），所以这里是同一修复的下游账本同步，不再人为制造第二个 provenance defect。运行时源码、schema、hash 算法与排盘坐标均不修改。

### 历史与传承判定

三条子规则都只在“继承已审身份规则的现代动态投影”范围内判为 `HISTORICALLY_SUPPORTED`。这个状态不声称古典文献已经定义今天的软件七槽接口，也不声称所有流派对十二长生方向/语义完全一致。任何真正的替代 profile 仍必须按来源、版本与学派单独建候选，不能因本批重放而折叠。

`TRANSMISSION_IMPACT=NONE`：没有新增物理见证、版本祖先关系、抄传边或学派继承边，传承图不改。

Matrix 从 198 / 169 / 10 变为 **201 / 173 / 10**；provenance metadata defects 仍为 **17/17**，chart algorithm defect / algorithm reopen / candidate collapse 仍为 **0**。确定性排盘核心继续 CLOSED。

下一门 **12MO**：审计 HPA-BAZI-FLOW-005 Temporal ShenSha target projection，逐个神煞家族核对本命/来源锚点与目标坐标，保留来源和候选差异，不从身份投影偷渡“激活、吉凶、应期”语义。

研究记录：`docs/research/BAZI-TEMPORAL-CLASSICAL-IDENTITY-PROJECTION-AUDIT-R1.json`。重放摘要：`docs/research/evidence/batch-12mn/projection-replay.json`。
