# Historical Provenance Audit — Batch 12OF

## Scope

Batch ID: `BATCH-12-ZIWEI-TIANSHOU-BODY-BASIS-EARLY-PRINT-CLOSURE-OF`

Target: `HPA-ZMINOR-008` — TianShou Body/Life basis conflict.

This batch asks a narrow question: is there actually a source-scoped Life-palace TianShou method that competes with the production Body-palace method?

## Early-print control

The repository already treats `EXT-ZIWEI-JIELAN-1581` as an early extant Ziwei print witness, with the 1581 edition identity independently corroborated by the Shanghai Library catalog witness `EXT-SHANGHAI-LIB-JIELAN-1581`.

Jielan chapter 35, `安天才天寿台辅封诰星诀`, is explicit:

> 命宫起子天才顺，身宫起子天寿堂。

The distinction is repeated by two worked examples:

- 甲子: Life in 寅 -> TianCai in 寅; **Body in 午 -> TianShou in 午**.
- 乙丑: TianCai advances one palace from Life; **TianShou advances one palace from Body**, 午 -> 未.

This is stronger than a single ambiguous label. The mnemonic and both examples independently separate TianCai/Life from TianShou/Body.

## Repository extraction control

The current S01 extracted atoms are internally consistent:

- `ZZZA-A-0830`: 身宫起子天寿堂;
- `ZZZA-A-0831`: use Body-palace branch as the 子 position;
- `ZZZA-A-0833`: determine the Body-palace branch;
- `ZZZA-A-0834`: advance from Body by the birth-year branch.

No extracted atom reviewed in this batch supplies a Life-palace TianShou rule.

The old normalized route `ZZZA-PR-042` nevertheless appended “来源正文/表头基础字段冲突需保留”. Earlier Batch 07 therefore treated TianShou as a Body/Life dispute. That conflict note is not currently bound to a quoted, located second source side.

## Independent operational discriminator

The frozen Wenmo discriminator remains useful as compatibility evidence, not historical authority.

For 1992-06-10 14:00:

- Life = 亥
- Body = 丑
- birth-year branch = 申
- observed TianShou = 酉

Body-basis yields 酉. Life-basis yields 未. The operational product therefore already matches the early-print Body-basis rule.

## Adjudication

**PROV-DEFECT-042** is repaired forward-only.

The defect is not a chart algorithm error. It is an audit/provenance overclaim: an unlocated Life-basis “candidate” was preserved without a bound source.

12OF therefore:

1. upgrades `HPA-ZMINOR-008` from `DISPUTED_MULTIPLE_CANDIDATES` to `HISTORICALLY_SUPPORTED`;
2. records Body-palace origin + birth-year branch offset as the historically attested rule geometry;
3. removes the unbound Life-basis candidate from the current Matrix;
4. leaves the R4 production algorithm unchanged;
5. leaves old Batch 07 documents untouched as historical audit snapshots.

This does **not** assert that no Life-basis tradition can exist anywhere. It states only that no such source-scoped method is presently identified in the reviewed evidence and therefore it must not be manufactured as a candidate.

## Result

After 12OF:

- Matrix remains **222 / 222 audited**
- HISTORICALLY_SUPPORTED: **98**
- DISPUTED_MULTIPLE_CANDIDATES: **28**
- SOURCE_INSUFFICIENT: **11**
- current MISSING_FROM_PRODUCT: **10**
- provenance defects: **42 / 42 repaired**
- historical candidate extensions: **8**
- chart algorithm defects / reopens / candidate collapses: **0 / 0 / 0**

No production coordinate or default changes.

## Next

**12OG — HPA-ZMINOR-007 TianChu competing stem tables and source closure.**

Research record: `docs/research/ZIWEI-TIANSHOU-BODY-BASIS-EARLY-PRINT-CLOSURE-R1.json`.
