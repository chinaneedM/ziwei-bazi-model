# Fusion Chart Historical Provenance Audit R1 — Batch 12NO

## HPA-COMB-007 Resolved profile / RuleSet / algorithm lineage

Status: **MODERN COMPATIBILITY ONLY / SOFTWARE-LINEAGE BOUNDARY CONFIRMED / PROVENANCE REPAIRED / NO ALGORITHM REOPEN**

本批审计 `HPA-COMB-007`：联合盘中的 Profile / RuleSet / Algorithm lineage 究竟表示什么，以及它与历史文本、版本、流派和传承谱之间应如何连接。

### 1. Runtime lineage 的实际语义

`CombinedChartApplicationResolution` 携带：

- combined profile；
- Ziwei calculation / application / presentation profiles；
- BaZi natal / temporal / application profiles；
- subsystem bundles；
- shared-time credential；
- candidate lineage；
- `manifest_hash`；
- integrity report。

`combined_manifest_payload()` 直接绑定 combined profile identity/algorithm/semantics 与六个 subsystem `profile_id/profile_version`；同时绑定 shared-time credential、candidate lineage、subsystem bundle hashes/errors 和 composition status。

`validate_combined_resolution()` 再验证 profile contract、shared-policy contract、subsystem replay/profile equality binding、candidate/time lineage 以及 ManifestHash。

因此这里的 lineage 是：**这一次确定性排盘究竟使用了哪一个可重放、可验证的计算快照。**

### 2. RuleSet / Algorithm 由 profile validator 约束

Ziwei 与 BaZi 的 resolved profile validators 会校验：

- Profile ID/version；
- RuleSet ID/version；
- Algorithm ID/version；
- calendar/time policy registry version；
- profile-specific compatibility constraints。

例如 BaZi temporal 的 WenZhen compatibility profile 明确把 `calendar_realization_source_class` 标成 `THIRD_PARTY_COMPATIBILITY_WITNESS`。稳定的 Profile ID 并不会把兼容性见证提升为古典权威。

### 3. Workbench 只展示后端已验证快照

Workbench 的“已解析计算身份 / 规则版本”面板只消费已有 `/api/resolve` 返回值：

- combined integrity 必须 `PASS`；
- `manifest_hash` 必须存在；
- 浏览器不维护平行的 profile/rule registry；
- 浏览器不选择 doctrine winner；
- 浏览器不从显示标签推导规则身份。

因此 presentation 层没有产生新的规则身份。

### 4. Software lineage 与 historical lineage 必须分开

当前研究治理已经明确：

```text
Matrix = rule-centric audit ledger
Graph  = lineage-centric evidence network
```

Historical Provenance Matrix、external-source registry 与 Transmission Genealogy Graph 负责：

- 文本；
- 版本；
- physical/digital witness；
- passage；
- 人物；
- 流派；
- 地域；
- 传承边；
- 历史证据强度。

Runtime Profile/RuleSet/Algorithm lineage 负责：

- reproducible computation identity；
- exact version snapshot；
- software integrity/replay。

二者应显式交叉引用，但不能合并为一个 ID namespace。

### 5. PROV-DEFECT-034

Matrix 原先：

- `source_quote=PENDING_VERBATIM_EXTRACTION`；
- `proposed_action=Extend lineage to historical source edition/school IDs during this audit stage.`

第二项会把 software computation provenance 与 historical transmission provenance 混为一体，并可能造成“一个稳定 runtime profile ID = 某一历史流派/版本权威”的错误语义。

确认：

`PROV-DEFECT-034=HPA_COMB_007_PROPOSED_ACTION_CONFLATED_RUNTIME_COMPUTATION_LINEAGE_WITH_HISTORICAL_SOURCE_EDITION_SCHOOL_LINEAGE`

修复为：

- Runtime Profile/RuleSet/Algorithm IDs 保持软件计算身份；
- 历史 edition/school/source/transmission IDs 留在 Matrix / source registry / genealogy graph；
- 两边通过明确 cross-reference 连接，而不是把历史身份塞进 runtime ID；
- compatibility profile 保持 compatibility witness，除非另有历史证据独立支持。

同时将 source quote 补为：

> Profile identity means only: this exact resolved chart used this versioned rule snapshot.

### 6. 裁决

`HPA-COMB-007=MODERN_COMPATIBILITY_ONLY`。

Matrix rows **220**；audited **218→219**；missing-product rows **10**。Provenance defects **33→34 confirmed / 33→34 repaired**。Chart algorithm defects / reopens / candidate collapses 均为 **0**。

`transmission_impact=NONE`：本批没有新增文本—人物—流派传承边，只澄清软件 lineage 与历史 lineage 的边界。

下一门：**12NP — HPA-COMB-008 Fact / computation / view / manifest hashes**。

研究记录：`docs/research/COMBINED-RESOLVED-PROFILE-RULE-ALGORITHM-LINEAGE-AUDIT-R1.json`。  
审计证据：`docs/research/evidence/batch-12no/combined-resolved-profile-rule-algorithm-lineage.json`。
