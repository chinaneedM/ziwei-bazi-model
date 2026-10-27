# Fusion Chart Historical Provenance Audit R1 — Batch 12BA

## 《張果星宗大全》SOAS / NCL 1593 元数据与 Morrison 1797 重刻本来源链校勘

Status: **NCL 1593 DATE SEMANTICS NARROWED TO ORIGINAL-PUBLICATION-YEAR-FROM-PREFACE / MORRISON RM65 -> RM c.41.c.1 DIRECTLY BRIDGED / RM c.41.c.1 INVENTORIED AS 1797 ONE-BOUND-ITEM REPRINT / NCL mirr0000375 -> RM c.41.c.1 HIGH-CONFIDENCE BUT NOT FORMALLY CLOSED / NO EARLY PHYSICAL-WITNESS VOTE / ZERO TARGET-TEXT OR HAI-GLYPH VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Why this batch exists

After Batch 12AZ identified another nominal 1594 route, the next external search surfaced a National Central Library (Taiwan) Chinese Rare Books Union Catalog record for a SOAS holding dated Wanli guisi / 1593. Read mechanically, that record could be mistaken for an independent surviving 1593 physical copy and incorrectly inflate the early-witness count.

BA audits the **date semantics and physical-object identity** before any such vote is permitted.

## 2. NCL union-catalog record: what the 1593 field actually means

The official NCL record `mirr0000375` gives:

```text
title=新編評註通玄先生張果星宗大全
responsibility=陸位輯校; 囗繼美參閱; 唐謙鋟梓
extent=十卷
place=金陵[南京]
catalog_date=明萬曆癸巳[1593]
quantity=1 v.
holder=英國倫敦大學亞非學院圖書館
note=原刊行年據韋環序
```

The note is decisive for metadata interpretation:

```text
原刊行年據韋環序
```

Accordingly the 1593 value is an **original-publication-year inference from the Wei Huan preface**. It is not, by itself, evidence that the extant SOAS physical object was impressed in 1593.

```text
NCL_1593 = ORIGINAL_EDITION_DATE_LOCATOR
NCL_1593 != DIRECT_PHYSICAL_IMPRESSION_DATE_PROOF
```

## 3. Morrison manuscript catalogue: RM no. 65

Andrew C. West's edited transcription of Morrison's own 1824 manuscript catalogue, SOAS MS 80823, includes:

```text
title=張果老星宗
catalog_number=65
extent=5 vols.
comment=Astrological, Taou sect
```

This establishes the early Morrison collection inventory identity, but not the print date.

## 4. Direct bridge: RM 65 -> current SOAS callmark RM c.41.c.1

The Morrison catalogue-number index explicitly maps:

```text
065 | 《張果老星宗》 (Chang) [65] | RM c.41.c.1 [65]
```

Thus:

```text
MORRISON_RM65_TO_RM_C41C1=RESOLVED
```

This is a direct catalogue-number/callmark bridge, not a title-similarity inference.

## 5. UCL shelfmark inventory: the identified object is dated 1797

The nineteenth-century UCL shelfmark index records:

```text
UCL shelfmark=L.g.9
inventory number=1
title=張果星宗命格大全
date=1797
bound item count=1
current SOAS callmark=RM c.41.c.1
```

This also explains why the early Morrison manuscript catalogue can say `5 vols.` while the later record says one item: the later catalogue is inventorying the Western-bound physical item. The apparent extent mismatch is therefore no longer a reason to split the provenance chain into two independent works.

## 6. SOAS/Morrison edition classification

The Morrison Collection description, based on the 1998 SOAS catalogue, places this title explicitly among:

```text
Qing dynasty reprints of Ming editions, made using recarved printing blocks
```

and describes it as:

```text
新編評註通玄先生張果星宗大全 — 1797 reprint of circa 1593 edition
```

The Morrison object is therefore classified as:

```text
RM c.41.c.1 = 1797 QING REPRINT OF CIRCA-1593 EDITION
```

It must **not** be promoted to a genuine surviving 1593 impression merely because the NCL union record carries a 1593 original-publication field.

## 7. NCL mirr0000375 versus RM c.41.c.1: identity status

The convergence is strong:

- same institution: SOAS;
- same work/title family;
- NCL quantity: `1 v.`;
- Morrison chain ends at one bound physical item `RM c.41.c.1`;
- NCL's 1593 date is explicitly original-publication metadata, fully compatible with a later reprint.

But the reviewed NCL record does **not** expose either:

```text
RM c.41.c.1
RM 65
```

Therefore the exact object crosswalk is intentionally not overclaimed:

```text
NCL_mirr0000375_TO_RM_c.41.c.1 = HIGH_CONFIDENCE_BUT_NOT_FORMALLY_CLOSED
```

This distinction prevents both false certainty and false double-counting.

## 8. Witness accounting

BA authorizes:

```text
EARLY_1593_PHYSICAL_WITNESS_INCREMENT=0
LATER_REPRINT_PHYSICAL_LINEAGE_CONTROL_INCREMENT=1
INDEPENDENT_TARGET_TEXT_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
```

No target leaf from `RM c.41.c.1` has been directly collated. The 1797 object is currently a **bibliographic/recensional control**, not a target-text vote.

NCL and Morrison must not be counted as two independent physical witnesses.

## 9. Relation to the genuine 1594 physical witness

The direct 1594 NIJL/Tohoku physical witness from Batch 12AW remains unaffected. A separate CiNii/Tohoku record for the Wanli-22 / 1594 Zhou-shi Wenguang copy directly distinguishes physical imprint evidence from preface-date evidence: its face/title metadata supports 1594, while its preface ends in Wanli guisi / 1593.

This is exactly why BA keeps these date axes separate:

```text
PREFACE_DATE
ORIGINAL_PUBLICATION_DATE
PHYSICAL_IMPRESSION_DATE
LATER_REPRINT_DATE
```

They cannot be collapsed into a single `year` field for provenance adjudication.

## 10. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

The BA correction is bibliographic. It supplies no missing mechanical bridge `upper/night Zi -> Hai branch`.

## 11. Accounting

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

BA is a preventive scope adjudication; it repairs no previously registered project provenance defect and changes no Matrix count.

## 12. Durable artifact

```text
docs/research/ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-R1.json
```

## 13. Next gate

1. Seek a first-party SOAS item-level record or image route explicitly binding `RM c.41.c.1`; if target pages become available, collate the target leaf directly without OCR.
2. Do not reuse NCL `mirr0000375` as an independent 1593 physical witness vote.
3. Continue searching for genuinely independent 1593/1594 material witnesses whose physical print date and target leaf can both be directly bound.
