# Fusion Chart Historical Provenance Audit R1 — Batch 12MO

## 八字动态神煞：来源范围保持与现代 target-match 边界

Status: **HPA-BAZI-FLOW-005 AUDITED AS MODERN_COMPATIBILITY_ONLY / SOURCE CANDIDATES PRESERVED / CLASSICAL TEMPORAL APPLICABILITY NOT ADJUDICATED**

本批处理的不是“哪些神煞在流年、流月一定成立”这种断法问题，而是更窄的工程问题：现有动态神煞 sidecar 是否在跨时间层匹配时，原样保留已经审计过的来源候选锚点、目标值、落柱范围、候选状态和来源坐标。

### 裁决

HPA-BAZI-FLOW-005 从 `IMPLEMENTATION_REVIEW_REQUIRED` 闭合为 `MODERN_COMPATIBILITY_ONLY`。上游 HPA-SHENSHA-001..021 各自承担历史身份与流派证据；本层只做现代工程 target-match，每个命中继续显式保存 `temporal_applicability_status=NOT_CLASSICALLY_ARBITRATED`。

### 穷举重放

实时 `BAZI-CLASSICAL-SHENSHA-FACTS-R1@1.7.1` 代表性目录含 38 个 source candidates：32 个单目标候选、6 个结构排除；其中 4 个 `ONLY_DAY` 候选只能进入 DAILY。对全部 60 个合法目标干支，各展开 DAYUN、两套 XIAOYUN、ANNUAL、MONTHLY、DAILY、HOURLY 七槽，共 420 槽、12,000 次候选×层级评估。每个输出 match 必须逐字段等于 source candidate。

另对 60 个非法干支组合做 fail-closed 控制；PRE_DAYUN 不制造目标干支，两套小运候选不选赢家。

### Batch 03 下游描述同步

运行时 ShenSha registry 已为 `1.7.1`，但 Matrix 21 条上游神煞和 ShenSha facts 文档仍残留共享 `1.7.0` 描述。天德双来源范围候选已经在 Batch 03 计入历史候选扩展；垣城 `S12:YHZP-CH-016`→`S11:YHZP-CH-015` 已是 `PROV-DEFECT-003`。12MO 只同步下游描述，不重复增加 provenance defect。

### 禁止外推

本批不授权吉凶、旺衰、神煞“激活”、应期、事件或预测，也不替上游争议候选选赢家。结构型神煞若未来支持动态结构匹配，必须另建结构模型，不能降格为单干支命中。

运行时算法文件不修改；`TRANSMISSION_IMPACT=NONE`。Matrix 保持 201 rows，audited rows 173→**174**；missing-product 仍 10，provenance defects **17/17**，chart algorithm defects / reopens / candidate collapses **0**。

下一门 **12MP**：HPA-BAZI-FLOW-006 Structural Context target projection，审计中性结构事实与后起解释性学派的边界。

研究记录：`docs/research/BAZI-TEMPORAL-SHENSHA-SOURCE-SCOPE-PROJECTION-AUDIT-R1.json`。重放契约：`docs/research/evidence/batch-12mo/projection-replay.json`。
