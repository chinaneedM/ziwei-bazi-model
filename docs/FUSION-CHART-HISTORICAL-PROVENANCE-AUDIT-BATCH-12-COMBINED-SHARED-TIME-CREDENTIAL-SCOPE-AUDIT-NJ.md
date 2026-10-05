# Fusion Chart Historical Provenance Audit R1 — Batch 12NJ

## HPA-COMB-001 Shared time credential：共享物理时间、独立术数规则与分层 provenance 边界

Status: **MODERN COMPATIBILITY ONLY / ONE PROVENANCE SCOPE DEFECT REPAIRED / NO HASH OR ALGORITHM CHANGE / NO HISTORICAL DOCTRINE CLAIM**

本批审计 `HPA-COMB-001`。对象是紫微＋八字联合排盘的共享时间凭证架构，不是任何古籍命理规则。

### 1. 共享的是什么

`validate_shared_policy_contract()` 的设计意图非常明确：

> Unify physical time facts without collapsing system-specific conventions.

联合层要求两边使用同一 policy registry version 与同一 civil ambiguous-time policy，从而确保同一墙钟输入解析成同一组物理时间候选。实际共享内容包括 UTC、offset/fold、地方平太阳时、地方视太阳时、历法事实及节气坐标。

但以下规则仍分别属于紫微与八字：

- 紫微 calendar-date / leap-month / day-boundary；
- 八字 year/month/day boundary、late-Zi hour-stem 等政策；
- 两套规则快照分别保存在 `selected_policies.ziwei` 与 `selected_policies.bazi`。

因此“共享时间底座”不等于“统一换日法”或“统一历法规则”。

### 2. credential hash 的真实边界

当前 `shared_time_credential` 的 `fact_hash` 直接绑定：

- birth；
- 两子系统时间解析 status；
- input interval；
- realization hashes；
- unresolved samples。

其 `computation_hash` 直接绑定：

- credential schema；
- `fact_hash`；
- policy registry version；
- `selected_policies`；
- realizations。

它并**不直接包含每个紫微/八字子系统的全部 algorithm ID/version 或全部 profile version**。

### 3. 完整联合 provenance 在更高层补全

这不是运行时缺陷。完整联合 provenance 本来就是分层的。

`combined_manifest_payload()` 继续绑定：

- combined profile ID/version；
- combined algorithm ID/version；
- 紫微 calculation/application/presentation profile ID/version；
- 八字 natal/temporal/application profile ID/version；
- 完整 shared time credential；
- candidate lineage；
- 两个子系统 bundle hash 或明确 subsystem error。

因此 credential 负责“共享时间事实 + policy snapshot”，manifest 与 subsystem bundle 负责更高层算法/profile lineage。

### 4. PROV-DEFECT-030

原 `docs/ZIWEI-BAZI-SHARED-TIME-CREDENTIAL-R1.md` 将 credential `computation_hash` 描述为“绑定全部规则版本”，超过实际 hash payload 的直接作用域。

确认：

`PROV-DEFECT-030=SHARED_TIME_CREDENTIAL_COMPUTATION_HASH_SCOPE_OVERSTATED_AS_BINDING_ALL_RULE_VERSIONS`

修复为：

- `SHARED_TIME_CREDENTIAL_HASH_SCOPE=SHARED_FACTS_PLUS_POLICY_SNAPSHOT`
- `FULL_COMBINED_PROVENANCE_SCOPE=MANIFEST_PLUS_SUBSYSTEM_BUNDLES`

本批不改 credential schema、不改任何 hash 算法、不改候选、不改排盘结果。

### 5. 回归边界

现有回归已覆盖：

- 紫微 `ZI_START_23` 与八字 `MIDNIGHT` 同时存在；
- 八字 `CLASSICAL_CONTINUOUS` 晚子时策略不被紫微覆盖；
- DST fold / uncertainty 下共享物理时间分支保持一致；
- credential / lineage 篡改会 fail closed；
- combined full replay 的 credential / manifest / subsystem hashes 可稳定重放。

### 6. 结论与记账

`HPA-COMB-001=MODERN_COMPATIBILITY_ONLY`。

Matrix rows **220**；audited **213→214**；missing-product rows **10**。Provenance defects **29→30 confirmed / 29→30 repaired**；chart algorithm defects / reopens / candidate collapses 均为 **0**。

`transmission_impact=NONE`。共享时间凭证与联合 manifest hashing 是现代软件组合架构，不建立古籍、版本、人物、流派或师承传承边。

下一门 **12NK：HPA-COMB-002 Independent Ziwei/Bazi date/calendar policy preservation**。

研究记录：`docs/research/COMBINED-SHARED-TIME-CREDENTIAL-SCOPE-AUDIT-R1.json`。  
证据记录：`docs/research/evidence/batch-12nj/combined-shared-time-credential-scope.json`。
