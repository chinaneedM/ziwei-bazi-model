# Fusion Chart Historical Provenance Audit R1 — Batch 12HR

## 国图 FID070 当前 SYS / UID 检索桥

Status: **CURRENT NLC META SEARCH DIRECTLY RECOVERS A 32冊 RARE-BOOK CANDIDATE = UID `UCS01003868188` / SYS `002838237` / HOLDING DOC NUMBER `002838237` / SEARCH-RESULT-LEVEL CROSSWALK TO FID070 IS HIGH-CONFIDENCE / 905s AND PHYSICAL SHELFMARK REMAIN UNRESOLVED / 3368↔3388 SUCCESSION AND EXACT QU ACCESSION BATCH REMAIN UNRESOLVED / ZERO PRODUCT OR MATRIX CHANGE**

## 1. Why this batch exists

Batch 12HQ left the current National Library of China machine identifier unresolved. The broad title retry workflow was therefore intended to recover current records without inventing a `3388 -> 03388` identity.

The workflow itself ended as `cancelled`, but that cancellation occurred **after** the search phase had succeeded and printed the returned current NLC records into the GitHub Actions log. The later detail loop attempted too many candidates and exhausted the job timeout.

## 2. Direct current NLC search result

The decisive returned record is:

```text
UID = UCS01003868188
SYS = 002838237
题名 = 附釋音春秋左傳註疏
卷数 = 六十卷
责任者 = (晉)杜預注 / (唐)孔穎達疏 / (唐)陸德明釋文
册数 = 32冊
文献类型 = 善本
年代字段 = 1271
holding = 国家图书馆
holding URL embedded doc_number = 002838237
```

The immediately adjacent same-title rare-book control is:

```text
UID = UCS01003868187
SYS = 002838236
册数 = 15冊
年代字段 = 1279 / 0960
```

This adjacent control is important: the current index is not returning one undifferentiated title record. It distinguishes at least two physical/bibliographic objects, and the 32冊 record is the one that matches the already closed FID070 32-fascicle object fingerprint.

## 3. Crosswalk adjudication

Existing closed evidence for FID `412004000070` already binds:

```text
附釋音春秋左傳註疏六十卷
32冊
国家图书馆
1959 printed number 3368
1987 book number 3388
FID 412004000070
```

The current record independently supplies the same title/60-juan/32冊/NLC rare-book fingerprint plus live machine fields `UID` and `SYS`.

Therefore the forward-only status is:

```text
CURRENT_NLC_UID = UCS01003868188
CURRENT_NLC_SYS = 002838237
SYS_UID_CROSSWALK = HIGH_CONFIDENCE_AT_CURRENT_SEARCH_RESULT_AND_PRIOR_32CE_OBJECT_FINGERPRINT_LEVEL
CURRENT_905S = UNRESOLVED
CURRENT_PHYSICAL_SHELFMARK = UNRESOLVED
```

This is deliberately narrower than claiming a full holdings-level closure. The job did not successfully finish the detail loop, so unobserved 905 fields are not backfilled or guessed.

## 4. Why the cancelled job is still usable evidence

The job log directly contains the completed HTTP search response and the target row before the later timeout sequence begins. The cancellation therefore means:

```text
SEARCH_OUTPUT_OBSERVED = true
DETAIL_LOOP_COMPLETED = false
ARTIFACT_UPLOAD_COMPLETED = false
```

A cancelled job is not treated as a successful end-to-end probe. It is used only for the already emitted direct search result.

## 5. Identifier firewall remains active

The following layers remain distinct:

```text
1959 printed number 3368
1987 book number 3388
digital FID 412004000070
current NLC UID UCS01003868188
current NLC SYS 002838237
current 905s / physical shelfmark UNRESOLVED
03388 SEARCH HYPOTHESIS ONLY
```

No automatic zero-padding, arithmetic offset, or catalog-renumbering mechanism is inferred.

## 6. Product and transmission consequence

This batch changes no deterministic chart rule, no runtime candidate, no Matrix row, and no transmission-genealogy topology.

Accounting remains:

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance defects = 14 / 14 repaired
confirmed chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```

## 7. Next gate

1. directly retrieve detail/holding metadata for `UCS01003868188 / SYS 002838237`, prioritizing 905s or equivalent physical call-number/shelfmark;
2. recover direct documentation for the 1959 `3368` -> 1987 `3388` catalog succession mechanism;
3. recover the exact Qu donation/accession batch/date for the FID070 object;
4. continue Zhang Lijuan 2018 full-text retrieval for a stronger identifier/detail bridge.
