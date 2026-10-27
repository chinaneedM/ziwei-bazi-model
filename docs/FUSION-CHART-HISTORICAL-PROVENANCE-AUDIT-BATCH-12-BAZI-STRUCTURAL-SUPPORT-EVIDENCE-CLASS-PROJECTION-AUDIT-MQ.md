# Fusion Chart Historical Provenance Audit R1 — Batch 12MQ

## 八字 Structural Support：证据类别与“根/强弱”语义防火墙

Status: **HPA-BAZI-FLOW-007 AUDITED AS MODERN_COMPATIBILITY_ONLY / EVIDENCE CLASSES PRESERVED / NO ROOT OR STRENGTH VERDICT**

12MQ 审计的是 `BAZI-STRUCTURAL-SUPPORT-FOUNDATION-R1@1.0.0` 及其 target-flow projection。结论不是“古籍存在这一完整 Support 对象”，而是：现代软件把已审藏干、亲和、同五行 identity、exact exposure 与动态 occurrence 组合成两个中性 evidence classes，并明确拒绝把它们升级为通根强弱结论。

### 1. 两类 evidence 不是两个流派赢家

- `EXACT_HIDDEN_STEM_MATCH`：可见干与支内藏干字符完全相同，必须保留 upstream exposure links。
- `SAME_ELEMENT_HIDDEN_SUPPORT`：只保留同五行但不同干的 hidden identities；exact identity 必须先扣除，且不得制造 exposure。

两类可以同时存在，不互相覆盖、排序或选 winner。它们也不是两套等待裁决的历史学校。

### 2. 月令与活动流月引用分离

`NATAL_MONTH_COMMAND` 固定绑定本命 `MONTH.BRANCH`；`ACTIVE_FLOW_SOLAR_MONTH` 绑定当前 Flow `MonthlyFrame` 与 Structural `MONTHLY` occurrence。两套 scoped candidate IDs 独立生成，目标月份变化不得重写本命月令引用。任何 role membership 都不等于得令、通根、旺衰或强弱。

### 3. 回放与边界

新增审计测试覆盖四个已发布 discrimination targets：PRE_DAYUN、节前一瞬、节令 exact instant、重复字符 occurrence。每个 Support candidate 必须能回溯到 upstream affinity fact；exact 类必须回溯 exposure link，same-element 类必须没有 exposure link。重复字符依 occurrence ID 分离；PRE_DAYUN 不制造 Dayun evidence；Xiaoyun/Daily/Hourly 仍在 released coverage 之外。

内部规则名 `BAZI-ROOT-SUPPORT-EVIDENCE-CANDIDATE-R1` 仅是现代 identifier，不据此授权 ROOT/NO_ROOT、主次根、强弱、权重、grade、score、rank、winner、格局、用神、调候或预测。

运行时算法、schema 与 hash 版本不变；`TRANSMISSION_IMPACT=NONE`。Matrix 保持 201 rows，audited rows 175→**176**；missing-product 仍 10，provenance defects **17/17**，chart algorithm defects / reopens / candidate collapses **0**。

下一门 **12MR**：HPA-BAZI-FLOW-001 + HPA-COMB-004 unified target timeline composition。

研究记录：`docs/research/BAZI-STRUCTURAL-SUPPORT-EVIDENCE-CLASS-PROJECTION-AUDIT-R1.json`。回放摘要：`docs/research/evidence/batch-12mq/projection-replay.json`。
