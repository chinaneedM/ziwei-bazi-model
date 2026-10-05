# Fusion Chart Historical Provenance Audit R1 — Batch 12NL

## HPA-COMB-003 Candidate lineage preservation

Status: **MODERN COMPATIBILITY ONLY / SOURCE-LINK REPAIRED / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

本批审计 `HPA-COMB-003`：联合盘在共享时间分支存在多候选时，是否保留每条候选的来源坐标、事实哈希与子系统候选身份，而不是静默选胜或合并。

### 1. Lineage 的实际主键

`candidate_lineage` 以 `source_time_branch_index` 为联动坐标。每条 lineage 行绑定：

- `shared_time_realization_hash`；
- `ziwei_natal_fact_hash`；
- `bazi_candidate_ids`；
- `LINKED_BOTH / ZIWEI_ONLY / BAZI_ONLY / UNBOUND` 状态。

整个表再与 `shared_time_computation_hash` 一起生成 `lineage_hash`。

因此 lineage 的职责是证明“哪个物理时间分支对应哪些子系统候选”，而不是对候选打分、排序或选出唯一赢家。

### 2. 多候选回归

DST fold 测试明确保留两个 civil folds 和两个不同的紫微 natal fact hash。

混合时间不确定性测试进一步保留 5 个 shared-time branches；这些分支映射到 2 个紫微事实候选，原始 branch→fact-hash 映射在 combined export 和 replay 中保持不变。

八字侧按 branch 收集 candidate IDs。实现中的 `sorted(set(candidate_ids))` 只规范化同一身份 ID 的重复引用，不授权把不同 candidate ID、不同 branch 或不同事实哈希合并成一个候选。

### 3. Full replay 防伪

完整 replay 不只检查 `lineage_hash` 的格式完整性。

测试会把一个紫微 fact hash 改成另一个格式合法的 64 位哈希，再重新计算 lineage hash 和 manifest hash；full replay 仍然拒绝该结果，并报告 candidate-lineage / manifest / application replay mismatch。

这证明 lineage 身份绑定不是“自洽哈希即可信”，而是必须与实际重算得到的候选集合一致。

### 4. PROV-DEFECT-031

Matrix 原先把 `HPA-COMB-003.source_quote_location` 指向：

`docs/COMBINED-RESOLVED-PROFILE-LINEAGE-R1.md`

该文档主旨是 profile / RuleSet / algorithm lineage，更直接对应 `HPA-COMB-007`。候选分支 lineage 的实际定义和门禁位于：

- `src/fortune_training/combined_chart_application/fusion_time.py`；
- `docs/ZIWEI-BAZI-SHARED-TIME-CREDENTIAL-R1.md`；
- focused multi-candidate / full-replay tests。

确认：

`PROV-DEFECT-031=HPA_COMB_003_SOURCE_LOCATION_CROSSED_WITH_PROFILE_RULE_ALGORITHM_LINEAGE_DOCUMENT`

本批仅修来源绑定，不改变候选、branch、hash、状态或 replay 算法。

### 5. 结论

`HPA-COMB-003=MODERN_COMPATIBILITY_ONLY`。

Matrix rows **220**；audited **215→216**；missing-product rows **10**。Provenance defects **30→31 confirmed / 30→31 repaired**；chart algorithm defects / reopens / candidate collapses 均为 **0**。

`transmission_impact=NONE`。

下一门：**12NM — HPA-COMB-005 Shared target → Ziwei projection**。

研究记录：`docs/research/COMBINED-CANDIDATE-LINEAGE-PRESERVATION-AUDIT-R1.json`。  
审计证据：`docs/research/evidence/batch-12nl/combined-candidate-lineage-preservation.json`。
