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

The initial inventory contained **107 rule/field families**. After Batches 01–07A and explicit splitting of historically distinct candidate families, the current machine-readable inventory contains **127 rows**, with **77 audited rows**. It intentionally keeps unresolved source work explicit rather than converting uncertainty into a chart defect. The current audit ledger records **5 confirmed provenance metadata defects repaired or quarantined at the provenance layer, 0 chart algorithm defects, 0 algorithm reopens, and 1 source-scoped historical candidate runtime resolver**.

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

The 1581 edition identity is independently corroborated by Shanghai Library linked-data instance `EXT-SHANGHAI-LIB-JIELAN-1581` (子4051; 明万历九年金陵书坊王洛川刻本). This is a bibliographic witness, not a substitute for chapter/facsimile rule-text collation.
