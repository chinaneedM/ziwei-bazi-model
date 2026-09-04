# Fusion Chart Historical Provenance Audit R1 — Batch 10B

## Excluded Bazi relation families: 方/三会, 破, 半合/拱合, 座下自化/暗合

Status: **AUDITED / THREE NEW SOURCE-CLOSED CANDIDATE GAPS / MODERN PARTIAL-TRINE QUARANTINED / NO ALGORITHM REOPEN**

## 1. 方 / 三会 is a philological bridge

《三命通会》卷六《属象》 explicitly groups 寅卯辰 as eastern Wood, 巳午未 southern Fire, 申酉戌 western Metal and 亥子丑 northern Water. Later commentary calls the same three-member directional groups 方/三会.

The wording differs but membership, direction and element geometry are the same. This is `DIFFERENT_WORDING_SAME_MECHANICAL_RULE`, not evidence for merging the family with 三合.

Runtime currently lacks this family: `MISSING_FROM_PRODUCT`.

## 2. Break is historically split

《五行精纪》引《李虚中书》 gives only four break pairs: 卯午、丑辰、子酉、未戌, and explicitly says 寅申巳亥 have no break because of their combinations.

Later six-break tables add 寅亥 and 巳申. Cross-system 六壬 tables cannot be used to make that later Bazi table classical by analogy.

Therefore:

- early four-break method = source-closed missing candidate;
- later six-break = disputed/later family, not a unique historical winner.

## 3. Half-trine / arched-trine

《三命通会》 is explicit that a three-combination bureau missing one branch does not form the completed bureau. Modern Bazi practice separately names center-containing pairs 半合 and outer pairs 拱合, but the historical audit has not closed an equivalent early rule table and its strength/adjacency conditions vary.

Thus current complete-trine runtime is correct. The modern partial relation taxonomy remains `MODERN_COMPATIBILITY_ONLY`, not part of the historical raw core.

## 4. 座下自化 / 干支暗合

《三命通会》 already lists 壬午、丁亥、戊子、甲午、辛巳、癸巳 as 座下自化. Later 《命理探源》 explicitly explains the same family as 干支暗合.

Mechanically, the visible stem combines with a hidden stem in its own branch according to the ordinary five-stem-combination table. Runtime already has all primitive hidden-stem identities but does not emit this relation.

This is a source-closed missing candidate. Productization must record the relation occurrence only and must not automatically assert 化.

## 5. Productization boundary

Do not bolt these relations directly into `BAZI-RAW-RELATION-CLASSICAL-CORE-R1`. First build one explicit source-scoped candidate sidecar capable of:

- arity 2 branch relations (early break);
- arity 3 directional groups;
- arity 4 four-earth bureau;
- same-pillar visible-stem ↔ hidden-stem relation participants;
- independent source/profile identity and no default selection.

## 6. Accounting

```text
TOTAL_MATRIX_ROWS=186
TOTAL_AUDITED_ROWS=153
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
IDENTIFIED_MISSING_CANDIDATE_FAMILY_COUNT=12
```
