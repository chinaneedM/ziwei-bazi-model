# Fusion Chart Historical Provenance Audit R1 — Batch 12NP

## HPA-COMB-008 Fact / computation / view / manifest hashes

Status: **MODERN COMPATIBILITY ONLY / HASH-DOMAIN BOUNDARY CONFIRMED / FULL-REPLAY FIREWALL CONFIRMED / PROVENANCE REPAIRED / NO ALGORITHM REOPEN**

本批审计 `HPA-COMB-008`：联合盘已发布的 FactHash / ComputationHash / ViewHash / BundleHash / ManifestHash / LineageHash 到底各自证明什么，以及它们与历史文献的 PDF/page/artifact SHA-256、edition/catalog identity 应如何分层。

### 1. Runtime hash 不是一个“万能真值哈希”

项目当前实现已经把不同语义域分开：

- shared-time `realization_hash`：单个合法物理时间 realization；
- shared-time `fact_hash`：出生输入、子系统时间解析状态、不确定区间、realization identities 等共享事实；
- shared-time `computation_hash`：credential schema + fact hash + policy registry/version + selected policies + realizations；
- `candidate_lineage.lineage_hash`：branch→Ziwei/BaZi candidate identity mapping；
- combined `manifest_hash`：combined profile/algorithm semantics、六个 subsystem profile identities、完整 shared credential、candidate lineage、两个 subsystem bundle identity/error 和 composition status；
- target-flow R1/R2 `source_fact_hash`：上游事实身份；
- target-flow R1/R2 `view_hash`：renderer-neutral target/status/view identity；
- target-flow R1/R2 `bundle_hash`：source/view hashes 加 computation/profile/algorithm identity 的聚合绑定。

这说明“fact / computation / view / aggregate”是不同 payload domain，不应压缩成单一的“这个结果是真的”。

### 2. 已发布 contract 明确区分事实与计算快照

Shared-time contract 明示：

`SHARED_TIME_CREDENTIAL_HASH_SCOPE=SHARED_FACTS_PLUS_POLICY_SNAPSHOT`

以及：

`FULL_COMBINED_PROVENANCE_SCOPE=MANIFEST_PLUS_SUBSYSTEM_BUNDLES`

因此 shared credential 的 computation hash 不是新的命理事实，而是“事实 + 选中的 policy snapshot”身份；完整联合 provenance 则继续由 manifest 与 subsystem bundles 补全。

### 3. Structural integrity 不等于 full replay

Combined base、target-flow、shared Ziwei projection 和 R2 都有 structural integrity 检查，但完整 replay 会从 request/upstream objects 重新解析。

现有 regressions 已证明可以构造这种情况：

1. 篡改一个格式完全合法的上游 hash / lineage identity；
2. 同步重算局部 lineage/source/view/bundle/manifest hash；
3. local structural integrity 仍可自洽；
4. full replay 重新执行原 service 后发现对象不相等并 fail closed。

R2 contract 直接写明：

> The structural validator verifies local consistency. Full replay recomputes the entire R2 result from the request and therefore rejects a locally rehashed mutation of an upstream binding.

所以 hash 是 deterministic integrity identity；对抗“自洽重哈希伪造”依赖 full replay，而不是 SHA-256 字符串本身。

### 4. Historical evidence checksum 属于另一命名空间

Historical external-source registry 已经保存大量：

- PDF SHA-256；
- page/image SHA-256；
- artifact ZIP SHA-256；
- response/HTML SHA-256；
- catalog / edition identifiers。

这些字段用于回答：“本批到底检查了哪个数字对象、哪张图、哪份下载物/响应”。

它们不能单独回答：

- 作品成书年代；
- 当前 physical copy 年代；
- 作者归属；
- 版本关系；
- 是否直接传承；
- 某流派是否唯一正统；
- 某规则是否历史上唯一正确。

历史权威仍必须经过 edition / wording / transmission / school / physical witness / competing evidence 的审计。

### 5. Runtime hash 与 evidence checksum 的连接方式

正确关系是：

```text
runtime rule/profile identity
        ↕ explicit audit cross-reference
Historical Provenance Matrix
        ↕
source / edition / passage / digital-object evidence
        ↕
evidence-object checksums + Transmission Genealogy Graph
```

而不是：

```text
historical PDF sha256
        ↓
inject into runtime FactHash
        ↓
therefore classical authority
```

如果历史审计最终证明 chart-affecting defect，仍须通过 algorithm-reopen gate、实现修改和 deterministic replay；增加 bibliographic checksum 本身绝不触发排盘事实变化。

### 6. PROV-DEFECT-035

Matrix 原先为：

- `source_quote=PENDING_VERBATIM_EXTRACTION`；
- `source_quote_location=README + engine integrity docs`；
- `proposed_action=Add historical-source bibliographic hashes/edition IDs without changing deterministic facts unless audited defect is proven.`

问题有两层：

1. source binding 太泛，不能审计具体 hash domain 与 replay contract；
2. proposed action 没明确说明 bibliographic/source checksum 应进入 historical evidence namespace，而不是 runtime deterministic hash namespace。

确认：

`PROV-DEFECT-035=HPA_COMB_008_PENDING_SOURCE_SCOPE_AND_ACTION_AMBIGUOUSLY_MIXED_RUNTIME_HASH_DOMAINS_WITH_HISTORICAL_EVIDENCE_CHECKSUMS`

修复为明确绑定 shared-time、combined manifest、target-flow/R2 hash contracts、full replay regressions 与 external-source registry，并要求 historical checksums 与 runtime hashes 通过审计 cross-reference 连接、不得 namespace merge。

### 7. 裁决与 Matrix 行审计完成

`HPA-COMB-008=MODERN_COMPATIBILITY_ONLY`。

Matrix rows **220**；audited **219→220**；当前 `MISSING_FROM_PRODUCT` rows **10**。Provenance defects **34→35 confirmed / 34→35 repaired**。Chart algorithm defects / reopens / candidate collapses 均为 **0**。

至此 Historical Provenance Matrix 的现有 220 行已 **220/220 audited**。这不等于整个历史研究结束：仍有 10 个当前标记为 `MISSING_FROM_PRODUCT` 的条目，需要与最新 runtime/product surfaces 再做一次 reconciliation，避免旧 Matrix 状态落后于后续 candidate productization。

`transmission_impact=NONE`：本批只澄清 runtime integrity hashes 与 historical evidence-object checksums 的边界，没有新增历史文本—人物—流派传承边。

下一门：**12NQ — 220/220 post-audit reconciliation of current MISSING_FROM_PRODUCT rows**。第一优先核对 `HPA-ZT-015`，因为后续已发布的 Zhongzhou leap-month historical candidate 可能使其旧状态过时。

研究记录：`docs/research/COMBINED-FACT-COMPUTATION-VIEW-MANIFEST-HASH-AUDIT-R1.json`。  
审计证据：`docs/research/evidence/batch-12np/combined-fact-computation-view-manifest-hashes.json`。
