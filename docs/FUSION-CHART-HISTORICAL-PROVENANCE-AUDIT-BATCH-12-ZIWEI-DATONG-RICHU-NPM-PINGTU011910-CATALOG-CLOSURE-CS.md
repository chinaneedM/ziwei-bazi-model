# Batch 12CS — 故宫 `平圖011910`《大統日出分》明鈔本官方書目閉合

## Status

```text
NPM_DATONG_RICHU_PINGTU011910_CATALOG_IDENTITY=CLOSED
NPM_EDITION_DESCRIPTION=MING_WUSILAN_MANUSCRIPT
NPM_PUBLIC_DIGITIZATION_STATUS=UNDIGITIZED
DIRECT_PHYSICAL_PAGE_OBSERVED=false
DIRECT_NUMERIC_CELL_OBSERVED=false
SANMING_59_41_VOTE_INCREMENT=0
SANMING_FINGERPRINT_VOTE_INCREMENT=0
TRANSMISSION_IMPACT=NONE
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
CANDIDATE_COLLAPSE=NONE
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 1. Why this batch exists

Batch 12CQ rejected the shortcut from 楊瓚《閑中錄》北京精密晝夜值 to the 1578 《三命通會》59/41 table and returned the ancestry search to direct Datong/Tonggui evidence. Batch 12CR then deduplicated a Shidian Huqian route so platform duplication could not inflate witness counts.

The next target was an independently catalogued object titled `大統日出分`. Because the 1578 problem requires a pre-1578 or otherwise historically scoped morning/evening or sunrise table, the first task is to bind the object and its access status without pretending catalog metadata is page-text evidence.

## 2. Official NPM catalog binding

The National Palace Museum public rare-book search route directly exposes:

```text
TITLE=大統日出分一卷
IDENTIFIER=平圖011910
VOLUME_DISPLAY=平圖011910(第1冊)
EDITION_DESCRIPTION=明烏絲欄鈔本
DIGITIZATION_STATUS=未數位化
NCL_UNION_CATALOG_NUMBER_OBSERVED=6267
```

The official result also exposes a National Central Library union-catalog cross-reference. That link is a bibliographic bridge only; it does not prove that NPM and NCL hold the same physical copy.

## 3. Machine capture

The repaired public-route probe completed successfully:

```text
WORKFLOW_RUN=35251503927
ARTIFACT=10508739636
ARTIFACT_DIGEST=sha256:59a0f100b446c590d5f37b68d62415769ac3d0707106aff5f149353c8aab428e
ARTIFACT_NAME=npm-datong-richu-pingtu011910-catalog-closure-r3
PROBE_SCHEMA=NPM-DATONG-RICHU-PINGTU011910-PUBLIC-CATALOG-CLOSURE-R3
```

The first probe design incorrectly treated the lack of a usable detail/image route as an execution failure. The repaired probe instead closes what the official catalog actually proves and fails closed beyond that scope.

## 4. Evidence boundary

This batch establishes a materially useful source-horizon fact:

```text
An official NPM catalog record identifies an extant Ming-described manuscript object
called 大統日出分一卷 under 平圖011910.
```

It does **not** establish any of the following:

- a readable physical target leaf;
- a 59/41 value;
- a Nanjing geographic calibration;
- the Sanming intermediate/change-day fingerprint;
- exact work-composition date;
- exact copying date inside the broad Ming catalog attribution;
- direct parentage to 1578 《三命通會》;
- identity between the NPM physical object and the NCL union-catalog object.

The public catalog explicitly says `未數位化`, so absence of a page image is an access fact, not a negative textual finding.

## 5. Date firewall

```text
work composition date = unresolved
edition/copy description = 明烏絲欄鈔本, official NPM catalog
exact physical-copy date = unresolved within Ming attribution
digital surrogate = no public book-page surrogate observed; catalog says undigitized
```

No Ming date is silently sharpened to “securely pre-1578 physical copy” without additional codicological or bibliographic evidence.

## 6. Transmission adjudication

```text
TRANSMISSION_IMPACT=NONE
```

The manuscript identity is important for discovery, but no numerical/mechanical passage was observed. Therefore this batch adds no Sanming ancestry edge and no numeric vote. Catalog identity alone must not become `ATTESTS -> 59/41` or a direct-copy relation.

## 7. Product adjudication

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_CHANGE=NONE
NEW_RUNTIME_CANDIDATE=false
ALGORITHM_REOPEN=NONE
CANDIDATE_COLLAPSE=NONE
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Audit accounting is unchanged:

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
CUMULATIVE_IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
PROVENANCE_METADATA_DEFECTS=12/12_REPAIRED
```

## 8. Next gate

1. resolve the NCL union-catalog `6267` route and determine whether it leads to a distinct holding, reproduction, or readable copy;
2. search independent institutional holdings for `大統日出分`, `大統曆通軌`, and `大統曆日通軌`;
3. obtain source-bound physical pages containing morning/evening, sunrise/sunset, half-day, or equivalent numerical cells;
4. only then reconstruct the half-day curve and compare it point-by-point with the exact 1578 Sanming pp134–136 target, including intermediate/change-day fingerprints rather than extrema alone.

Research record:

`docs/research/ZIWEI-DATONG-RICHU-NPM-PINGTU011910-CATALOG-CLOSURE-R1.json`
