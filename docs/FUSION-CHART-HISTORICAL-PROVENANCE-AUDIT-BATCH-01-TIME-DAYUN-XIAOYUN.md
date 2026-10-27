# Historical Provenance Audit R1 — Batch 01: Time / Dayun / Xiaoyun

## Gate state

```text
BATCH_ID=BATCH-01-TIME-DAYUN-XIAOYUN
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ALGORITHM_REOPEN_AUTHORIZED_COUNT=0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

This batch is a source/provenance audit only. No deterministic generator, profile default, or candidate winner is changed.

## 1. Bazi day boundary and late Zi

The Ming `三命通会` Siku witness explicitly distinguishes the two halves of Zi hour around midnight. This is strong historical support for the released `MIDNIGHT` day boundary. It does **not** prove that every later school used the same rule, so `ZI_START_23` remains a named candidate rather than being deleted.

The separate late-Zi hour-stem question is less closed. A later received witness, `命理探源`, records a day-old/hour-new convention and points to `星平大成`. That is compatible with the current `CLASSICAL_CONTINUOUS` candidate, but the exact primary page and transmission genealogy are not yet closed. Therefore the candidate set remains disputed.

## 2. Bazi Dayun

The Ming `三命通会` witness supplies three mechanically relevant rules together:

- direction classes based on 阳男/阴女 versus 阴男/阳女;
- forward counting to the future Jie and reverse counting to the previous Jie;
- the three-days-to-one-year conversion, including finer elapsed-time discussion.

Results:

- Jie-anchor rule: historically supported by a strong Ming witness.
- Three-days/one-year symbolic ratio: historically supported by a strong Ming witness.
- Year-stem/sex binding: well supported by the Ming examples and received Zi Ping convention, but earlier genealogy and documented competing day-stem schools remain to be audited; it stays school-scoped rather than being declared universal.
- The repository's absolute-UTC/microsecond realization is still a **modern computational realization**. Historical support for the symbolic ratio does not retroactively make UTC or microseconds classical doctrine.

No Dayun algorithm reopen is authorized.

## 3. Bazi Xiaoyun

`三命通会` is especially important because one chapter preserves both methods that the repository already exposes as separate candidates:

- fixed male/female starting Ganzhi family;
- the 醉醒子 hour-pillar method whose direction is determined by year.

This directly validates the repository's no-winner architecture. Coexistence in a historical witness is positive evidence **for preserving candidates**, not evidence for arbitrarily selecting one.

No Xiaoyun algorithm reopen is authorized.

## 4. Ziwei leap-month Life/Body placement

Repository S01 and the external received text of `紫微斗数全书` agree that a leap month is treated as the following month for the scoped Life/Body placement rule. A later Republican-era lineage is also documented: `斗数宣微` (first edition 1935) is bibliographically attested, while a modern historical-method survey reports both a half-month split and a next-month alternative in that work.

The production profile currently selects `ZHONGZHOU_FIXED_15`, while the Fullbook method remains separately represented. Batch 01 therefore classifies the production choice as **school-specific**, not as the unique ancient rule. Because the implementation matches its declared profile and preserves the Fullbook candidate, this is not yet an implementation defect.

Before any production-default reconsideration, the exact 1935 primary page and the Zhongzhou transmission link must be verified.

## External evidence registry

See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json`.

Batch 01 external anchors:

- Chinese Text Project, `三命通会`卷二, Ming Wan Minying, digital base edition `钦定四库全书`.
- Wikisource `紫微斗数全书`卷二, used only to corroborate repository S01 wording.
- `斗数宣微` bibliographic record: Wang Caishan, 1935 first edition; exact method page pending primary verification.
- `命理探源` as a later night-Zi witness and pointer to `星平大成`; not used to fabricate an earlier date.

## Batch conclusion

```text
AUDITED_ROW_COUNT=9
CONFIRMED_IMPLEMENTATION_DEFECT_COUNT=0
ALGORITHM_REOPEN_AUTHORIZED_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

The first historical batch strengthens, rather than weakens, the current policy of independent subsystem rules and explicit candidates.
