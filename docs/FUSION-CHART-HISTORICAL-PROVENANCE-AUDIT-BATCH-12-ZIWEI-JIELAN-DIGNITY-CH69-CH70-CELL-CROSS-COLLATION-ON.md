# Historical Provenance Audit — Batch 12ON

## Scope

Target: `HPA-ZIWEI-018` — 1581 Jielan historical dignity table.

12OM built a CH70 star-oriented raw-source-lexeme candidate. 12ON completes the missing parallel-source work: **cell-level cross-collation of CH69 and CH70 without converting either chapter into the production R4 dignity scale**.

## Method

CH70 remains the primary historical candidate. CH69 is a palace-oriented parallel witness only.

The comparison grid is 25 CH70 entities/groups × 12 branches = **300 cells**. Every cell is assigned one of seven evidence relations:

- `EXACT_LEXEME_OVERLAP`
- `SOURCE_EXPLICIT_EQUIVALENT`
- `SOURCE_LOCAL_POLARITY_CONFLICT`
- `ATTESTED_NON_EQUIVALENT_NO_DIRECT_GLOSS`
- `CH69_UNSTATED`
- `CH69_TEXT_UNRESOLVED`
- `CH70_UNSTATED`

The source-local polarity flag is only a coarse contradiction detector derived from source vocabulary. It is **not** a modern grade scale.

## Frozen result

| Relation | Cells |
| --- | ---: |
| exact raw lexeme overlap | 97 |
| direct source-explicit equivalence | 37 |
| source-local polarity conflict | 54 |
| both attested, no direct equivalence | 21 |
| CH69 unstated | 82 |
| CH69 text unresolved | 8 |
| CH70 unstated | 1 |
| **Total** | **300** |

The 8 CH69 unresolved cells are deliberately typed rather than repaired. Examples include singular `文` at 子, the unclear 丑 phrase `天哭羊陀火破祥`, the 辰 transcription token `午` that is not silently rewritten to `日`, and the truncated 寅 ending `曲与`.

## Important anomaly controls

Three cells show why the two chapters must remain parallel evidence rather than a merged table:

- 紫微午: CH69 has `庙`; CH70 has both `庙` and `平`. The CH70 conflict survives.
- 巨门丑: CH69 has `陷`; CH70 has both `局` and `陷`. The CH70 conflict survives.
- 天机巳: CH69 has `兴` (locally glossed as 入庙), while CH70 is unstated. CH69 **does not fill** the CH70 hole.

No transitive gloss chain is collapsed. No CH69 value overwrites CH70. No CH70 value overwrites CH69.

## Product boundary

The cross-collation layer is implemented in:

- `src/fortune_training/ziwei_chart/dignity_historical_cross_collation.py`
- `tests/test_ziwei_jielan_1581_dignity_ch69_ch70_cross_collation_r1.py`

The historical candidate remains `PRESERVED_NOT_SELECTED`. Production `OPERATIONAL-ZIWEI-DIGNITY-R4` is untouched.

Therefore `HPA-ZIWEI-018` remains `MISSING_FROM_PRODUCT`: the historical source candidate and CH69/CH70 reconciliation are now ready internally, but an explicit read-only product API / Workbench surface is still missing.

## Accounting

- Matrix: **222 / 222 audited**
- current MISSING_FROM_PRODUCT: **6**
- historical candidate extensions: **14**
- candidate registries / runtime resolvers: **5 / 5**
- provenance defects: **43 / 43**
- algorithm reopens: **0**

## Next

**12OO — expose the reconciled Jielan dignity source-lexeme candidate through a read-only product API / Workbench surface, preserving the no-grade-coercion firewall.**
