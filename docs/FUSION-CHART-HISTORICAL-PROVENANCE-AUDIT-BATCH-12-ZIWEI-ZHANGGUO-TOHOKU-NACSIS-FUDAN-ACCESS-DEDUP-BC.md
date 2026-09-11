# Fusion Chart Historical Provenance Audit R1 — Batch 12BC

## 《張果星宗大全》东北大学 NACSIS 1594 馆藏 crosswalk、复旦访问路径与独立见证去重校勘

Status: **TOHOKU NACSIS WANLI-22 HOLDING METADATA BOUND / BATCH-12AW DUPLICATE-VOTE FIREWALL ENFORCED / EXACT NIJL-BID-TO-ACCESSION CROSSWALK NOT FORMALLY CLOSED / FUDAN OBJECT-LEVEL APPOINTMENT ROUTE ESTABLISHED / FUDAN PUBLIC TARGET IMAGE NOT OBTAINED / SPECIAL-DOCUMENT REPRODUCTION ONLY CASE-BY-CASE / NO REQUEST SUBMITTED / CHONGQING EXACT-1594 CLAIM REMAINS SECONDARY LOCATOR / ZERO NEW TARGET-TEXT OR HAI-GLYPH VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Why this batch exists

Batch 12BB established a first-party Fudan physical holding dated only `明萬曆間` and left two high-value routes: obtain a target leaf from Fudan, or find another genuinely independent exact 1593/1594 physical witness. Subsequent discovery surfaced NACSIS/CiNii record `BD05367609`, which at first glance looked like a new exact-1594 Tohoku witness.

BC tests that apparent increment against the already-collated Batch 12AW NIJL/Tohoku witness before any vote is counted, and separately records the current first-party access path for Fudan `rb2314`.

## 2. NACSIS/CiNii bibliographic control

CiNii Books / NACSIS-CAT record:

```text
NCID=BD05367609
title=新編評註通玄先生張果星宗大全
responsibility=陸位輯校
publication=周氏文光, 萬暦22 [1594]
extent=5冊
size=24.4×15.4cm
holding count=1
holding=東北大学 附属図書館本館
巻之1-2=01793921822
巻之3-4=01793921831
巻之5-6=01793921849
巻之7-8=01793921857
巻之9-10=01793921865
```

The same record also reports `序末に萬暦癸巳`, cover dating `萬暦閼逢敦牂(甲午)`, and `周氏文光新梓`.

These details are materially stronger than a generic title/date search result because they bind the edition to one Tohoku holding and five volume-level registration numbers.

## 3. Critical dedup firewall against Batch 12AW

Batch 12AW already directly collated:

```text
provider=National Institute of Japanese Literature / Tohoku University Library
BID=100238879
title=新編評註通玄先生張果星宗大全
date=萬曆22 / 1594
canvas count=439
target canvas=195
```

The NACSIS record and AW therefore converge on title, exact Wanli-22/1594 dating, and the Tohoku institutional holding family. However, the reviewed public metadata does **not** explicitly state:

```text
NIJL BID 100238879 == Tohoku registration 01793921822..01793921865
```

Accordingly BC records:

```text
EXACT_PHYSICAL_ACCESSION_CROSSWALK=HIGH_CONFIDENCE_NOT_FORMALLY_CLOSED
DUPLICATE_VOTE_FORBIDDEN=true
INDEPENDENT_EXACT_1594_MATERIAL_WITNESS_INCREMENT=0
INDEPENDENT_TARGET_TEXT_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
```

This is intentionally conservative. A missing explicit accession crosswalk is not permission to count the same institutional edition lineage twice.

## 4. Fudan first-party access route for rb2314

Fudan's current ancient-book service page states that rare books use an appointment service: readers should reserve one working day in advance and provide title, call number and case/volume count. The Ancient Book Reading Room is closed-stack and in-library reading; first-time outside readers require identity documentation and an introduction letter.

The target identifiers remain:

```text
call number=rb2314
resource book no=FDU01001127121
catalogueId=34053686
barcode=AB0613271-80
location=复旦大学 / 光华楼古籍书库
```

Current document-delivery policy says ancient books, microfilm and other special documents are supplied only **case by case**. That general policy does not establish that this exact target is reproducible, digitized, free, or remotely deliverable.

Therefore:

```text
FUDAN_OBJECT_LEVEL_APPOINTMENT_ROUTE=ESTABLISHED
FUDAN_PUBLIC_TARGET_IMAGE_OBTAINED=false
FUDAN_TARGET_SPECIFIC_REPRODUCTION_ELIGIBILITY=UNRESOLVED
FUDAN_REPRODUCTION_REQUEST_SUBMITTED=false
TARGET_LEAF_OBTAINED=false
```

No email, booking, copying request or other external action was submitted in this batch.

## 5. Chongqing locator remains locator-scoped

A secondary rare-book union-catalog transcription describes a Chongqing Library target-title holding as a Wanli-22 / 1594 printed copy in six volumes. Chongqing Library's own public site confirms a large ancient-book collection, but the reviewed first-party surfaces do not expose an exact target-title item record or target leaf.

Thus:

```text
CHONGQING_SECONDARY_EXACT_1594_LOCATOR=true
CHONGQING_FIRST_PARTY_EXACT_TARGET_ITEM_BOUND=false
CHONGQING_TARGET_LEAF_OBTAINED=false
INDEPENDENT_EXACT_1594_WITNESS_INCREMENT=0
```

Do not convert a secondary locator plus a first-party general collection description into a first-party target holding claim.

## 6. Effect on HPA-ZDATE-006

BC adds access and identity precision only. It does not add the missing historical mechanical edge:

```text
upper/night Zi -> Hai branch
```

Therefore:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

## 7. Accounting

```text
ROW_COUNT=198
AUDITED_ROW_COUNT=166
MISSING_FROM_PRODUCT=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_PROVENANCE_DEFECTS=11
REPAIRED_PROVENANCE_DEFECTS=11
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

No Matrix count changes are authorized.

## 8. Durable artifact

```text
docs/research/ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-R1.json
```

## 9. Next gate

1. Prefer a **publicly obtainable target leaf** from a genuinely independent exact 1593/1594 physical copy. Jangseogak remains independently cataloged but its target leaf is still not publicly obtained.
2. Continue first-party item-level pursuit of the Chongqing/Weifang locators; do not promote secondary exact-year claims without item metadata or object bytes.
3. Fudan `rb2314` is now an explicit external-action boundary: a target-specific appointment/reproduction inquiry may be pursued only with user authorization and whatever identity/contact information the provider requires.
4. Keep the separate Fullbook cloudy/rain current-time acquisition chain open; do not conflate that unresolved mechanism with late-Zi witness counting.
