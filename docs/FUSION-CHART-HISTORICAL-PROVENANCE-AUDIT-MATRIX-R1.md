# Fusion Chart Historical Provenance Audit Matrix R1

## State

```text
FUSION_CHART_HISTORICAL_PROVENANCE_AUDIT_R1=IN_PROGRESS
HISTORICAL_PROVENANCE_INVENTORY=COMPLETE
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

Baseline branch: `agent/fusion-chart-core-r1-20260822`  
Baseline HEAD: `9bf1f4f82d5c43b40fad29bd3d0a210fae4ed9ec`  
Baseline tree: `3a83f5da19144a448371686311ea66cdf5ccb8e8`

This stage audits **why every deterministic chart-affecting rule exists, which text/school/version supports it, how competing methods differ, and whether the released implementation actually matches its cited source**. It does not reopen a closed algorithm merely because a historical audit has started.

## Matrix contract

Machine-readable source of truth: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json`.

Every row carries:

- rule ID and module/system;
- current implementation and current profile;
- primary source route;
- verbatim quote slot and exact source location;
- historical period/version slot;
- later witnesses and school attribution;
- competing methods;
- implementation-match result;
- confidence;
- audit status;
- proposed action;
- explicit algorithm-reopen authorization, which is **false for every inventory row at creation**.

The initial inventory contained **107 rule/field families**. After Batches 01–08B and explicit splitting of historically distinct candidate families, the current machine-readable inventory contains **159 rows**, with **118 audited rows**. It intentionally keeps unresolved source work explicit rather than converting uncertainty into a chart defect. The current audit ledger records **7 confirmed provenance metadata defects repaired or quarantined at the provenance layer, 0 chart algorithm defects, 0 algorithm reopens, and 1 source-scoped historical candidate runtime resolver**.

## Research-corpus authority

S00–S19 are now explicitly classified as the **project research corpus**, not as
infallible historical authority. The repository path `sources/canonical/` retains
its legacy storage/freeze meaning only. For historical claims, each S00–S19 rule
must be traced to the underlying witness it actually contains or cites, and that
witness remains externally auditable.

Accordingly:

- an S-number alone cannot close a historical claim;
- internal transcription, attribution and normalization can be wrong;
- a stronger edition-specific or bibliographic witness may refine or contradict
  the project corpus;
- conflicting historical witnesses remain scoped candidates rather than being
  collapsed to whichever rule happened to be in S00–S19 first;
- modern software remains compatibility evidence only.

The governing policy is
`docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md`.

## Allowed audit statuses

- `HISTORICALLY_SUPPORTED`
- `SUPPORTED_BUT_SCHOOL_SPECIFIC`
- `DISPUTED_MULTIPLE_CANDIDATES`
- `MODERN_COMPATIBILITY_ONLY`
- `SOURCE_INSUFFICIENT`
- `IMPLEMENTATION_REVIEW_REQUIRED`
- `MISSING_FROM_PRODUCT`
- `NOT_YET_FORMALIZED`

## Reopen gate

A deterministic rule may be locally reopened only when all of the following are bound in the matrix:

1. exact primary or high-quality historical evidence;
2. edition/date/location and verbatim text;
3. school attribution and competing-method classification;
4. a reproducible mismatch between that rule and the released implementation;
5. defect scope limited to the affected rule/profile;
6. forward-only source/profile/tests/docs change.

Reference-product differences alone cannot authorize a reopen.

## Initial inventory findings

- Time/Calendar contains both modern astronomical/civil standards and doctrinal charting policies. These must not be conflated.
- Bazi late-Zi, Xiaoyun and several support/anchor questions are explicitly candidate-shaped and remain unranked.
- Bazi Dayun has a canonical-oriented profile plus a separately named Wenzhen compatibility realization; the compatibility profile is not historical authority.
- Ziwei production currently binds several `WENMO_DEFAULT_*` rule-set identities. Historical audit must determine, row by row, whether those bindings represent source-supported school rules, compatibility-only calibration, or a profile-labeling debt.
- Ziwei dynamic Kui/Yue preserves strict-source and Wenmo-compatible candidates; Tianma remains case-method-only.
- Ziwei flow-hour and self/inward transformation direction remain unresolved rather than fabricated.
- Structural R1/R2 are neutral computational geometry; historical claims start only when named source semantics are attached downstream.
- Combined Fusion/lineage/hashing are software provenance mechanisms, not classical doctrine.

## Module order

Historical research proceeds in evidence-risk order:

1. Time / Calendar doctrine-vs-modern-standard separation.
2. Bazi natal core + Dayun + Xiaoyun.
3. ShenSha source-by-source audit.
4. Ziwei natal stars / minor stars / dignity / four transformations.
5. Ziwei temporal layers and dynamic auxiliaries.
6. Structural R1–R8.
7. Combined Fusion lineage closure.
8. Final missing-product scan against audited historical rule families.

No winner is selected for a genuinely disputed school rule solely to simplify product output.


## Progress through Batch 07A

- Batch 01: Time / Dayun / Xiaoyun.
- Batch 02: Bazi natal / derived foundations; repaired Twelve-Growth and NaYin provenance metadata.
- Batch 03: Bazi ShenSha; repaired Yuancheng lineage and preserved source-scoped variants.
- Batch 04: Ziwei early-print core; registered the 1581 Jielan candidate family and isolated historically distinct Kui/Yue, Fire/Bell, dignity and Four-Transformation families.
- Batch 05: Ziwei roles / limits / rings; distinguished Jielan birth-year Mingzhu from received-Fullbook Life-palace Mingzhu, kept Zi/Wu Shenzhu unresolved, verified Daxian/Xiaoxian/Boshi geometry, repaired stale Jielan registry-version lineage, and added a source-scoped deterministic candidate runtime that remains `PRESERVED_NOT_SELECTED`.
- Batch 06: Ziwei natal foundations; promoted Life/Body placement, the twelve-palace sequence, Five-Tigers palace stems and the Life-palace NaYin bureau chain to direct received-text support, while quarantining the normalized Fullbook attribution for the 23:00 day-boundary sentence until edition/facsimile evidence closes it.
- Batch 07A: Ziwei minor-star decomposition; split eight independent minor-star families out of the broad R4 bundle. TianKu/TianXu, HongLuan/TianXi, LongChi/FengGe, TaiFu/FengGao, TianXing/TianYao and the year-based TianDe/JieShen geometry are directly received-text supported; TianChu and TianShou remain disputed candidates.
- Batch 07B: Ziwei early-print minor-star closure; added eleven granular families bound to the 1581 《新刻纂集紫微斗数捷览》 witness: TianGuan/TianFu, TianKong, Xun void-pair geometry, JieLu KongWang/JieKong, GuChen/GuaSu, JieSha, HuaGai, the TaoHuaSha→XianChi geometry/name bridge, DaHao, PoSui and TianCai. All eleven current placement geometries match the scoped witness; XunKong main/sub display ordering remains explicitly outside the 1581 claim, and TianShou remains disputed under 07A.
- Batch 07C: completed rule-family decomposition of the operational minor-star R4 bundle. LongDe is mechanically supported by the 1581 TaiSui-12 sequence; YueDe is a genuine historical split (巳-start family vs received-Fullbook 子-start family); standalone FeiLian plus month JieShen/YueJie, TianWu, TianYue and YinSha remain SOURCE_INSUFFICIENT rather than being upgraded from modern repetition. HPA-ZIWEI-008 therefore leaves IMPLEMENTATION_REVIEW_REQUIRED and becomes a fully decomposed SOURCE_INSUFFICIENT parent summary, with no chart-algorithm reopen.
- Batch 08A: Ziwei dynamic auxiliaries A; decomposed flowing LuCun/QingYang/TuoLuo, Chang/Qu, Kui/Yue and Tianma by temporal layer and authority class. Annual 流禄流羊流陀 has a received-Fullbook witness; Daxian/finer flowing-star rules and 流昌流曲/运马/流马 are explicitly Zhongzhou-school methods bound to Wang Tingzhi's modern manual. Wenmo Kui/Yue remains compatibility-only. The misleading runtime label CANONICAL_SOURCE_TABLE was repaired to S01_STRICT_PROJECT_CORPUS_METHOD with no coordinate or selection change (PROV-DEFECT-007).
- Batch 08B: Ziwei temporal frames B; applied the formal 训诂 method to distinguish wording identity from mechanical identity. Flow-year TaiSui palace, Five-Tigers month Ganzhi and flow-day palace geometry are historically supported. The 1581 Jielan `日上起子时` day-anchored hour method is source-closed but missing from runtime; the current fixed-branch hour method remains a separate Zhongzhou case method. Zhongzhou leap-month `1–15 previous month / 16–end next month, day sequence continuous` is now a source-closed `MISSING_FROM_PRODUCT` candidate rather than `SOURCE_INSUFFICIENT`. No algorithm reopen.

The 1581 edition identity is independently corroborated by Shanghai Library linked-data instance `EXT-SHANGHAI-LIB-JIELAN-1581` (子4051; 明万历九年金陵书坊王洛川刻本). This is a bibliographic witness, not a substitute for chapter/facsimile rule-text collation.

## Cross-chat continuity

Long-running audit state is persisted in `docs/PROJECT-CURRENT-STATE-R1.json` and restored according to `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`. CI runs `scripts/verify-project-continuity-state-r1.py` so Matrix progress, completed batches, defect counts and non-negotiable invariants cannot drift from the handoff state unnoticed.
