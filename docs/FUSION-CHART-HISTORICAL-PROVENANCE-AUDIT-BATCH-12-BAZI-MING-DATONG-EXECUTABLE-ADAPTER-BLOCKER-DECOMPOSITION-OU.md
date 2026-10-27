# Fusion Chart Historical Provenance Audit R1 — Batch 12OU

## Ming Datong executable-adapter blocker decomposition

Status: **BLOCKER DECOMPOSITION CLOSED / GENERAL MING DATONG ADAPTER STILL FAIL-CLOSED / NO RUNTIME OR MATRIX STATUS CHANGE**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
HPA_DAYUN_CAL_002=MISSING_FROM_PRODUCT
MING_DATONG_GENERAL_EXECUTABLE_ADAPTER=CERTIFICATION_BLOCKED
RUNTIME_SELECTION_AUTHORIZED=NO
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

## 1. Why this batch exists

12OT moved the active queue back to `HPA-DAYUN-CAL-002`. The historical evidence is already deep enough that “the Ming calendar is not yet researched” is no longer a useful description. The remaining uncertainty must be separated into independent certification gates so later research does not repeatedly reopen already-closed layers or accidentally turn a target-year success into a universal calendar engine.

12OU therefore creates a machine-auditable blocker ledger. It changes no production algorithm and selects no historical runtime profile.

Research record: `docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json`.

## 2. Four source-scoped gates are already closed

The following are not current generic blockers:

1. **D1 conjunction method** — the 1569 Zhou Xiang facsimile and a Ming Datong worked example support the corresponding lunar `遲/疾行度` divisor; the Qing-compiled `定限度` wording remains a later received variant rather than an equal production candidate.
2. **Internal day/clock coordinate** — Ming calendrical event time is represented on the source-internal `子正` / 100-ke coordinate. This remains a calendrical-astronomy fact, not a Bazi/Ziwei rollover rule.
3. **1569 table-generation precision** — the primary table ledgers close distinct stage-scoped fixed-point operators. A single global rounding rule is directly rejected.
4. **1578 target-year month structure** — source-derived D1 replay matches twelve Wanli-6 month starts plus the next-year first-month anchor at day resolution, while the exact same-year Qintianjian physical almanac closes all twelve month identity / large-small labels with zero mismatch.

These closures remain deliberately scoped. None alone authorizes a general historical calendar runtime.

## 3. Five independent gates still block a general adapter

### 3.1 Qishuo geographic reference

The internal `子正` coordinate is closed; its geographic realization is not. Nanjing, Beijing/Dadu, and a module-specific mixed-geography model remain preserved but unselected.

The existing critical cases make a simplistic longitude answer impossible:

- 1462 shows that a physical same-year almanac can disagree with both the reign record and later tables, while agreeing with D1.
- 1495 is far enough from the day boundary that a Beijing–Nanjing longitude shift cannot explain the one-day conflict.
- 1497 is extremely boundary-sensitive, but that sensitivity cannot identify the historical meridian by itself.
- 1581 has D1, the reign record and a surviving physical almanac converging.

The 1521 Zhu Yu memorial materially supports **mixed location-dependent parameters inside Ming Datong practice**, because it explicitly criticizes use of Nanjing sunrise fractions in the computational workflow. It still does not define the qishuo small-remainder meridian. Therefore `MING_DATONG_QISHUO_GEOGRAPHIC_REFERENCE=UNRESOLVED` remains mandatory.

### 3.2 Dynamic interpolation / D1 precision

The 1569 primary table-generation precision map is closed only for those table stages. The 1596 Datong example is a local dynamic precision control; it is not enough to define universal interpolation, carry, truncation or rounding widths for all years and boundary cases.

### 3.3 Invalid target-date policy

The classical Dayun family requires realization on the historical lunisolar calendar, but the reviewed evidence does not yet specify what an executable adapter must do when the target day number does not exist in a small month.

Until a direct rule is bound, the adapter must not silently clamp, roll forward, roll backward, or borrow a Gregorian invalid-date policy.

### 3.4 Intercalary-month identity and traversal

The Ming source explicitly requires leap-month correction, but that statement is not yet a complete executable rule for regular versus intercalary duplicate-month identity, target-month selection when the same numbered month occurs twice, traversal through the inserted leap month, or preservation of intercalary identity in later arithmetic.

Modern calendar-library behavior is not historical authority for these choices.

### 3.5 Multi-year leap generalization

The 1578 month chain is a strongly certified target-year oracle, not proof that the repository can generate arbitrary Ming years. General certification requires multi-year month/leap production, including intercalary years and boundary-sensitive new moons, under the same source-scoped arithmetic.

## 4. Two later gates are dependency-blocked

`ADD_CALENDAR_YEARS` and Bazi runtime/product integration are not independent research shortcuts.

Historical ten-year recurrence must inherit the same certified calendar regime and the same invalid-date / intercalary semantics. `BaziTemporalEngine` must remain disconnected from an executable historical profile until those source gates close.

The current fail-closed result therefore remains correct:

`UNRESOLVED_NO_CERTIFIED_HISTORICAL_CALENDAR_ADAPTER`.

## 5. Important decomposition consequence

Qishuo geography and Dayun calendar-addition semantics are **different research fronts**. They can be investigated in parallel, but they meet again before general runtime certification.

Likewise, unresolved qishuo geography does **not** erase the direct 1578 physical month-page result. It prevents generalizing that target-year closure into an arbitrary-year exact-event generator.

This distinction is the main closure of 12OU.

## 6. Accounting / invariants

No Matrix status changes.

- Matrix: **222 / 222 audited**
- current `MISSING_FROM_PRODUCT`: **4**
- provenance defects: **45 / 45 repaired**
- historical candidate extensions: **14**
- candidate registries/runtime resolvers: **5 / 5**
- chart algorithm defects: **0**
- algorithm reopens: **0**
- candidate collapses: **0**
- production default changed: **NO**
- transmission graph edge change: **NONE**

## 7. Next batch

**12OV — Ming/Sanming classical calendar-addition edge semantics.**

Audit invalid target-day behavior and regular/intercalary duplicate-month identity/traversal against direct or near-primary evidence. If the source does not close either edge, record that non-certification explicitly; do not invent a clamp/roll policy and do not substitute a modern Chinese-calendar library. After that, proceed to the dynamic D1 precision / multi-year leap gates.

