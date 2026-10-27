# Fusion Chart Historical Provenance Audit R1 — Batch 12PD

## GK12437 qishuo locality-operator audit

Status: **COMPLETE PHYSICAL METHOD BLOCK DIRECTLY REVIEWED / EXPLICIT LOCALITY OPERATOR NOT ATTESTED IN SCOPE / MD-G03 STILL OPEN / HISTORICAL RUNTIME FAIL-CLOSED**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
HPA_DAYUN_CAL_002=MISSING_FROM_PRODUCT
GK12437_QISHUO_METHOD_BLOCK=001A_TO_005B_DIRECT_VISUAL_REVIEW
GK12437_QISHUO_POSITIVE_CONTROLS=求經朔分_AND_求定朔及望分
EXPLICIT_LOCALITY_OR_LICHA_OPERATOR_IN_REVIEWED_BLOCK=NOT_ATTESTED
MD_G03_QISHUO_GEOGRAPHIC_REFERENCE=OPEN_BLOCKING_GENERAL_ADAPTER
RUNTIME_SELECTION_AUTHORIZED=NO
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

## 1. Why this batch exists

12PC closed MD-G09 source-scoped and returned the active queue to MD-G03. The repository already possessed a complete Kyujanggak physical capture of `GK12437_00 / 奎貴12437 / 大統曆日通軌`, but that capture had previously been used mainly to control day/night-table attribution. 12PD reuses the same source-bound physical artifact to answer a narrower question: **does its qishuo method itself contain an explicit locality correction?**

This is deliberately a negative-evidence audit. It is not a meridian-selection batch.

## 2. Physical scope and positive controls

Workflow `35317924654` / artifact `10536220506` contains all 78 viewer pages. Direct no-OCR review binds the pre-table constants/method block to viewer pages `001a-005b`; `006a` is already the opening numerical 立成 table.

Decisive visible controls include:

- `002b`: **求冬至分** and **求經朔分**;
- `004b`: **求遲疾差分**, **求加減差分**, and **求定朔及望分**;
- `005a`: continuation of the 定朔/望 arithmetic, followed by **求四季土王用事**;
- `006a`: **大統立成卷上 / 大陽冬至前後二象盈初縮末限**, confirming the method-to-table boundary.

The research record binds SHA-256 values for every page from `001a` through `006a`. OCR is not used for the final glyph/operator claim.

## 3. Locality-operator result

Across the complete reviewed method block `001a-005b`, no explicit step was observed that invokes a named place, meridian, `里差`, `地差`, `地里差`, `經度`, `大都`, `北京`, `南京`, `應天`, or `順天` when deriving 經朔/定朔.

The safe result is therefore only:

```text
GK12437_REVIEWED_QISHUO_METHOD_BLOCK_EXPLICIT_LOCALITY_OPERATOR
= NOT_ATTESTED
```

This is a **method-block-scoped physical negative**. It is stronger than a search-engine or OCR non-hit because the actual source-bound pages were visually reviewed, but it is still not proof of geographic neutrality.

## 4. What this does not prove

12PD does **not** authorize any of the following inferences:

- hidden/inherited meridian = absent;
- Dadu/Beijing = qishuo reference because Datong descends from Shoushi;
- Nanjing = qishuo reference because separate sunrise/daylength modules are Nanjing-scoped;
- the wider Tonggui component set contains no locality parameters;
- modern UTC+8, mean solar time, or apparent solar time can substitute for the historical coordinate.

In particular, the 1521 Zhu Yu complaint `推算曆數，用南京日出分杪，似相矛盾` remains evidence for mixed location-dependent modules, not a definition of 定朔小餘 geography.

## 5. MD-G03 adjudication

The result closes one subquestion and narrows the remaining one:

```text
EXPLICIT_LOCALITY_OPERATOR_SUBQUESTION=CLOSED_NEGATIVE_OBJECT_METHOD_BLOCK_SCOPE
IMPLICIT_OR_INHERITED_QISHUO_REFERENCE=UNRESOLVED
MD_G03=OPEN_BLOCKING_GENERAL_ADAPTER
```

The live Ming adapter ledger remains **5 CLOSED_SOURCE_SCOPED / 4 OPEN_BLOCKING_GENERAL_ADAPTER / 2 DEPENDENCY_BLOCKED**. G03, G05, G07 and G08 remain independent blockers; G10/G11 remain dependency-blocked.

No production algorithm, profile, default, candidate registry, runtime resolver or chart result changes.

## 6. Transmission-genealogy impact

12PD adds a passage-level node for the physically reviewed `GK12437` qishuo method block and a direct `ATTESTS` edge from the already-established physical-copy node. It does **not** assert that this Joseon copy is a direct parent of Zhou Xiang 1569 or any Ming official almanac, and it does not create a geographic-meridian ancestry edge.

## 7. Accounting

- Matrix: **222 / 222 audited**
- current `MISSING_FROM_PRODUCT`: **4**
- provenance defects: **45 / 45 repaired**
- historical candidate extensions: **14**
- candidate registries/runtime resolvers: **5 / 5**
- chart algorithm defects: **0**
- algorithm reopens: **0**
- candidate collapses: **0**

## 8. Next batch

**12PE — qishuo inherited-coordinate / named-place binding cross-collation.**

Cross-collate the qishuo constants, epoch and method lineage across Yuan Shoushi, early Datong/Tonggui, this `GK12437` witness and Zhou Xiang 1569. The target is a direct named-place or inherited-coordinate binding. Sunrise/daylength geography remains an explicitly forbidden proxy.

Research record: `docs/research/MING-DATONG-GK12437-QISHUO-LOCALITY-OPERATOR-AUDIT-R1.json`.
