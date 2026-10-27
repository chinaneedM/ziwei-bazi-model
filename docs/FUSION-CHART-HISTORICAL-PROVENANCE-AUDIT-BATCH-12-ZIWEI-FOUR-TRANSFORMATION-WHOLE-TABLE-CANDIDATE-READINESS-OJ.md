# Historical Provenance Audit — Batch 12OJ

## Scope

Batch ID: `BATCH-12-ZIWEI-FOUR-TRANSFORMATION-WHOLE-TABLE-CANDIDATE-READINESS-OJ`

Target: `HPA-ZIWEI-014` — competing Four-Transformation table families.

12OJ closes **candidate readiness**, not product selection. The rule remains `MISSING_FROM_PRODUCT` until the divergent whole-table candidates have an explicit read-only public product surface.

## Three complete table identities

The existing 1581 Jielan table is complete and target-identical to production `S08_CURRENT_40_ASSIGNMENT_R1`. It remains historically source-scoped even though its 40 targets are the same.

12OJ adds two genuinely divergent **whole-table** candidates.

### Received Fullbook — Shidian source-scoped recension

Candidate:

`RECEIVED-FULLBOOK-SHIDIAN-V3-FOUR-TRANSFORMATION-R1`

The received verse yields:

- 戊: 贪狼 / 太阴 / 右弼 / 天机
- 庚: 太阳 / 武曲 / 天同 / 天相
- 壬: 天梁 / 紫微 / 天府 / 武曲

Compared with production, only three cells differ:

- 庚化科: 太阴 -> 天同
- 庚化忌: 天同 -> 天相
- 壬化科: 左辅 -> 天府

The Shidian witness is deliberately source-scoped. Other received Fullbook surfaces have different Geng readings, so this candidate is **not** labelled a universal Fullbook table.

### Zhongzhou — Wang Tingzhi

Candidate:

`ZHONGZHOU-WANGTINGZHI-FOUR-TRANSFORMATION-R1`

S01 direct atoms `ZZZA-A-0391..0395` give the complete table. Compared with production:

- 戊化科: 右弼 -> 太阳
- 庚化科: 太阴 -> 天府
- 壬化科: 左辅 -> 天府

All other cells remain table-bound to the same Zhongzhou source family.

## Runtime candidate firewall

New internal registry:

`ZIWEI-FOUR-TRANSFORMATION-HISTORICAL-CANDIDATES-R1@1.0.0`

Resolver:

`ZIWEI-FOUR-TRANSFORMATION-SOURCE-SCOPED-CANDIDATE-RUNTIME-R1@1.0.0`

Rules:

- `selection_status=PRESERVED_NOT_SELECTED`
- `whole_table_only=true`
- `cell_level_hybridization_allowed=false`

A caller must choose one source family and one heavenly stem. There is no API for selecting individual cells from different families.

## Matrix result

`HPA-ZIWEI-014` remains **MISSING_FROM_PRODUCT**.

The reason has narrowed: complete deterministic candidates now exist internally, but there is not yet a read-only public candidate API/Workbench table-family surface.

Accounting after 12OJ:

- Matrix: **222/222 audited**
- current MISSING_FROM_PRODUCT: **7**
- historical candidate extensions: **13**
- candidate registries / runtime resolvers: **4 / 4**
- provenance defects: **43 / 43 repaired**
- production default / candidate winner / algorithm reopen: **unchanged / none / 0**

## Next

**12OK — productize the two whole-table Four-Transformation candidates as read-only source-scoped candidate profiles without changing production S08.**
