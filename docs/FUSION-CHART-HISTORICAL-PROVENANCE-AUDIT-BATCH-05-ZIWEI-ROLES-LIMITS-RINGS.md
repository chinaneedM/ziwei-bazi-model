# Fusion Chart Historical Provenance Audit R1 — Batch 05

## Ziwei roles, limits and rings

Status: **AUDITED / FORWARD-ONLY CANDIDATE EXTENSION**

This batch continues the historical-provenance audit without reopening the closed
deterministic Fusion Chart Product R1.

Invariant states:

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

## 1. Source-control rule

Repository S00–S19 remains the canonical project corpus. External historical
materials are corroborating witnesses and bibliographic controls; they do not
silently override the repository rule identity.

For the 1581 witness used in Batch 04–05, edition identity is now independently
corroborated by the Shanghai Library rare-book linked-data record:

- title: 《新刻纂集紫微斗数捷览》四卷
- edition label: 明万历九年金陵书坊王洛川刻本
- temporal value: 明万历9年
- machine-readable begin year: 1581
- catalog identifier: 子4051
- registry ID: `EXT-SHANGHAI-LIB-JIELAN-1581`

This library-catalog witness is used for bibliographic identity only. Mechanical
rule claims still require chapter-level text or facsimile collation.

## 2. Audited rule families

Batch 05 closes or sharpens the following families:

| Matrix row | Rule family | Batch 05 conclusion |
|---|---|---|
| `HPA-ZIWEI-012` | 命主 / 身主 role identity | Real school/source split. Jielan uses birth-year branch for 命主 while received Fullbook production uses Life-palace branch. Preserve both identities; never merge lookup bases. |
| `HPA-ZIWEI-019` | 五局长生 | 1581 Jielan directly witnesses the existing five-bureau anchors and yin/yang-sex direction family. No algorithm reopen. |
| `HPA-ZIWEI-023` | 子午身主 | Source wording remains composite 火铃/铃火. No unique historical Fire-vs-Bell winner is source-closed. Keep fail-closed historical status. |
| `HPA-ZIWEI-024` | 博士十二神 | 1581 Jielan and received Fullbook witness the 12-member ring family anchored on 禄存 with yin/yang-sex direction. Existing geometry is not shown defective. |
| `HPA-ZT-001` | 大限方向 | 1581 Jielan supports 阳男阴女顺、阴男阳女逆. |
| `HPA-ZT-002` | 初限起岁 | First nominal age equals the bureau number. |
| `HPA-ZT-003` | 大限宫序 | Ten-year stepping and one-palace progression are directly replayable. |
| `HPA-ZT-008` | 小限 | 1581 Jielan supports the current age-one start table and male-forward / female-reverse direction family. |

## 3. 命主 is a genuine method-basis split

The important difference is not the lookup table values. The same sequence of
star names can appear under both source families while the **lookup key differs**:

- Jielan 1581: birth-year branch
- received Fullbook production profile: Life-palace branch

Therefore a cell-by-cell equality test is insufficient. Provenance must bind the
basis type as part of the algorithm identity.

The repository now preserves the Jielan basis separately under:

`ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATES-R1`

Selection state remains:

`PRESERVED_NOT_SELECTED`

No production default was changed.

## 4. 子午身主 remains unresolved on purpose

Both the 1581 Jielan witness and the received Fullbook family preserve a textual
Fire/Bell composite at 子、午. Current Wenmo-compatible production behavior uses
Fire, but this does **not** prove that Fire is the unique historical winner.

Therefore:

```text
HPA-ZIWEI-023=SOURCE_INSUFFICIENT
HISTORICAL_SHENZHU_ZI_WU_WINNER=NONE
```

This is an intentional authority boundary, not a missing implementation bug.

## 5. Daxian and Xiaoxian

The early-print witness supports the existing core Ziwei limit geometry strongly
enough that no algorithm reopen is authorized:

- Daxian first active address: Life palace
- first nominal age: bureau number
- step size: ten years
- palace progression: one address per Daxian
- Daxian direction: year-stem yin/yang × sex
- Minor-Limit age-one start table: existing 12-branch table
- Minor-Limit direction: male forward / female reverse

The audit therefore strengthens historical lineage rather than changing results.

## 6. Boshi ring

Batch 05 verifies the 12-member member order:

```text
博士 力士 青龙 小耗 将军 奏书
飞廉 喜神 病符 大耗 伏兵 官符
```

The source family anchors the ring at 禄存 and applies the same year-stem
yin/yang × sex direction class. Existing production naming may still contain
`WENMO_DEFAULT` identifiers for compatibility history; those identifiers must
not be interpreted as the historical origin of the ring.

## 7. Source-scoped runtime candidate resolver

A follow-up implementation adds:

`ZIWEI-JIELAN-1581-SOURCE-SCOPED-CANDIDATE-RUNTIME-R1@1.0.0`

It deterministically materializes the already source-closed Jielan facts for a
supplied year stem/branch, birth-hour branch, Life-palace branch, bureau and sex:

- four-transformation table row
- Kui/Yue pair
- Fire/Bell resolved branches
- TianShang/TianShi fixed geometry
- Changsheng anchor/direction
- Jielan Mingzhu birth-year basis
- Daxian rule identity
- Minor-Limit start/direction
- Boshi ring
- explicit unresolved dignity/Shenzhu states

Every result carries the Jielan registry hash and a per-input runtime hash.

This resolver is intentionally **sidecar-only**:

- it does not mutate `ResolvedZiweiCalculationProfile`;
- it is not a production-selected winner;
- it does not normalize the unresolved 1581 dignity table;
- it does not select Fire or Bell for the Zi/Wu Shenzhu ambiguity.

## 8. Product gaps after Batch 05

The historical audit still correctly keeps these as product gaps or unresolved
families until their full candidate-profile/API/UI contract is closed:

- competing Four-Transformation table families
- Jielan Geng-stem Kui/Yue candidate in the user-selectable product profile
- Jielan 巳酉丑 Fire/Bell candidate in the user-selectable product profile
- Jielan historical dignity table after edition collation/normalization
- Jielan Mingzhu birth-year-basis candidate in the user-selectable product profile
- Zi/Wu Shenzhu Fire/Bell winner remains source-insufficient

The newly added sidecar resolver is a prerequisite for productization; it is not
used to overclaim that these candidate-profile gaps are already closed.

## 9. Batch 05 verdict

```text
BATCH_05_ZIWEI_ROLES_LIMITS_RINGS=AUDITED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
PRODUCTION_DEFAULT_CHANGE_COUNT=0
HISTORICAL_CANDIDATE_RUNTIME_RESOLVER_COUNT=1
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

Next historical work should continue with the remaining Ziwei natal foundations
and dynamic/temporal rows, prioritizing source extraction before implementation.
