# Fusion Chart Historical Provenance Audit R1 — Batch 12NW

## Zi/Wu Shenzhu Fire/Bell evidence closure

Status: **SOURCE_INSUFFICIENT RETAINED / UNIQUE FIRE NOT CLOSED / PROV-DEFECT-040 REPAIRED / NO ALGORITHM REOPEN**

本批处理 `HPA-ZIWEI-023`。1581 `《新刻纂集紫微斗数捷览》` CH32 保留 `子午生人铃火宿`，并解释为 `子午年生人，则火铃为身主`；received `《紫微斗数全书》` 及 S01 raw line 同样保留 `火玲/火铃` 复合表达。因此 historical layer 能关闭“复合文字存在”，不能关闭“唯一 Fire”。

现代公开解释也不能充当古籍仲裁：一类编辑说明把底本 `火玲星` 解释为通行 Fire，另一当前规则面则把子午解释为 Bell。它们只证明现代解释并不统一。

S01 内部同时保存 raw `子午人火铃星` 和 normalized `子午 -> 火星`。由于 S01 是 project research corpus，不是不可错历史权威，production Fire 只能视为 operational compatibility default。

现有 Wenmo fixture 也没有独立关闭 Zi/Wu ROLE.SHENZHU。Zi-year cases 观察的是安火铃 placement；真正的 role-binding fixture 是巳年 `ROLE.SHENZHU=天机`。所以目前没有 dedicated Zi/Wu Wenmo role discriminator。

**PROV-DEFECT-040**：旧 `WenmoDefaultRoleGenerator` docstring 对整张表使用 “matching Wenmo's default convention” 的表述，对 Zi/Wu 分支过强。本批只把 docstring/comment 收窄为：Zi/Wu Fire 是继承 S01 normalization 的 operational compatibility default，不代表 historical arbitration，也不代表 independently observed Wenmo compatibility closure。

不修改 `WENMO_SHENZHU_BY_YEAR_BRANCH` 的值、RoleBinding `source_refs`、rule-set/version、algorithm version、fact/computation hash 或 production default。

HPA-ZIWEI-023 保持 `SOURCE_INSUFFICIENT`；strict QS 继续 fail-closed；Jielan sidecar 继续 `winner_selected=false`。

Accounting: Matrix 220/220; MISSING_FROM_PRODUCT 10; SOURCE_INSUFFICIENT 11; provenance defects 40/40; chart algorithm defects/reopens/candidate collapses 0. `transmission_impact=NONE`.

下一门：**12NX — HPA-ZIWEI-026 Jiangqian temporal/source-scope evidence closure**。

Research: `docs/research/ZIWEI-ZI-WU-SHENZHU-FIRE-BELL-EVIDENCE-CLOSURE-R1.json`  
Evidence: `docs/research/evidence/batch-12nw/ziwei-zi-wu-shenzhu-fire-bell-evidence-closure.json`
