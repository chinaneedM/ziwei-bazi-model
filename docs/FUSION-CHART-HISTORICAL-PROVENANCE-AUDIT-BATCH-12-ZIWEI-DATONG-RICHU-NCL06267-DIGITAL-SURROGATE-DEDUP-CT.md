# Batch 12CT — NCL-06267《大統日出分》既有数字替身去重闭合

## Status

```text
NCL_6267_FOLLOWUP_PUBLIC_FACSIMILE=RESOLVED
ACQUIRED_OBJECT=NCL-06267 大統日出分
ACQUIRED_PDF_SHA256=0d3ed2b54f92b5eb2f11e5d06babebcc177e04ec5b8c7168b56f1fb25f94797d
SAME_PDF_AS_BATCH_12CG=true
INDEPENDENT_PHYSICAL_WITNESS_INCREMENT=0
INDEPENDENT_RECENSION_VOTE_INCREMENT=0
SANMING_59_41_VOTE_INCREMENT=0
SANMING_CHANGE_FINGERPRINT_VOTE_INCREMENT=0
NPM_PINGTU011910_EQUALS_NCL06267_PHYSICAL_COPY=NOT_PROVED
TRANSMISSION_IMPACT=NONE
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
CANDIDATE_COLLAPSE=NONE
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 1. Why this batch exists

Batch 12CS bound the National Palace Museum catalog object `平圖011910 / 大統日出分一卷 / 明烏絲欄鈔本 / 未數位化` and observed an NCL union-catalog cross-reference numbered `6267`. Because the NPM public route exposes no book-page surrogate, 12CS correctly left the next gate at a readable NCL or otherwise independent physical witness.

The follow-up pipeline resolved the public NCL-06267 facsimile through Wikimedia Commons, downloaded the original PDF, installed an explicit PDF rendering dependency, and rendered all 21 pages without using OCR as glyph or numerical authority. The decisive result is not a new table reading. It is an exact deduplication result against an earlier completed batch.

## 2. Current acquisition gate

```text
WORKFLOW_RUN=35255298130
HEAD=a8cfadb7272054507a4b3ab282d853fda13cab73
ARTIFACT=10511369697
ARTIFACT_NAME=ncl06267-datong-richu-physical-dedup-r5
ARTIFACT_DIGEST=sha256:a5d094101fd86265654938bbf07bdfe796a9e643b34f5aa97a2aeeb1ffb2f355
PDF_PAGES=21
RENDERED_PAGES=21
OCR_USED_FOR_GLYPH_OR_NUMERIC_CLAIMS=false
WORKFLOW_RESULT=SUCCESS
```

The acquired PDF hashes to:

```text
0d3ed2b54f92b5eb2f11e5d06babebcc177e04ec5b8c7168b56f1fb25f94797d
```

The workflow now fails closed unless that hash agrees with the already registered Batch 12CG NCL-06267 object.

## 3. Exact deduplication against Batch 12CG

Batch 12CG already directly reviewed:

```text
SOURCE_ID=EXT-NCL-DATONG-RICHU-NCL06267
TITLE=NCL-06267 大統日出分
WORKFLOW_RUN=34869676923
ARTIFACT=10358685142
PDF_SHA256=0d3ed2b54f92b5eb2f11e5d06babebcc177e04ec5b8c7168b56f1fb25f94797d
PDF_PAGES=21
```

That earlier batch directly established the daily table structure `晨分 / 日出分 / 半晝分 / 日入分 / 昏分` and replayed selected direct numerical points against the 1578 Sanming integer-ke ladder. The present PDF is byte-identical to that already counted object.

Therefore:

```text
same digital object = yes
new independent physical witness = no
new recension vote = no
new 59/41 vote = no
new intermediate/change-day vote = no
new direct-parentage edge = no
```

A second route to the same bytes cannot increase historical weight.

## 4. Institutional/physical-copy firewall

This result must not be overstated.

Batch 12CS proved that the NPM catalog exposes an object `平圖011910` and an NCL union-catalog cross-reference. Batch 12CT proves that the **newly acquired NCL/Commons PDF** is the same digital object already reviewed as NCL-06267 in Batch 12CG.

It does **not** prove:

```text
NPM 平圖011910 physical manuscript = NCL-06267 physical holding
```

The NPM object is catalogued as `明烏絲欄鈔本` and publicly undigitized. No codicological, page-image or shelfmark-level evidence in this batch identifies the two institutional physical objects as one and the same copy. The deduplication relation is therefore deliberately limited to the NCL digital surrogate route.

## 5. Relationship to the Sanming ancestry problem

The historical target remains the exact 1578 《三命通會》 physical seasonal table closed in Batch 12CP. That target includes not only the summer-solstice `59/41` pair but also a distinctive stepped fingerprint and intra-term change instructions such as the Dahan and Yushui secondary states.

Batch 12CG already showed that NCL-06267 belongs to a 1380s Nanjing Datong daily numerical table family whose continuous curve can mechanically span the Sanming integer range. But it did not prove:

- direct copying from the surviving NCL object to Wan Minying;
- the exact pre-1578 textual parent;
- the exact quantization/rounding rule;
- the exact Sanming change-day fingerprint.

Because Batch 12CT supplies no new independent object, none of those open questions advances by evidence count.

## 6. Transmission and product adjudication

```text
TRANSMISSION_IMPACT=NONE
```

No new graph node or ancestry edge is required merely for reacquiring an already represented digital object. The existing Batch 12CG NCL source/table-family evidence remains controlling.

For product scope:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_RUNTIME_CANDIDATE=false
RUNTIME_WINNER=false
CANDIDATE_COLLAPSE=false
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Audit accounting is unchanged:

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
CUMULATIVE_IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_CHART_ALGORITHM_DEFECTS=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
```

## 7. Next gate

The NCL-06267 route is now closed as a duplicate for witness-count purposes. Do not spend another research cycle treating a mirror or alternate URL to this exact PDF as a new witness.

Highest-value next targets are:

1. an **independent physical or independently descended readable witness** of `大統曆通軌 / 大統曆日通軌 / 大統日出分` carrying `晨昏分` or mechanically equivalent numerical cells;
2. securely pre-1578 Nanjing/Datong evidence that reproduces **both** the `59/41` cap and the 1578 Sanming intermediate/change-day fingerprint, or explicitly states a quantization rule that deterministically produces that fingerprint;
3. continued independent work on the Fullbook `上五刻 -> 昨夜亥時` lineage and historical time-coordinate binding, without conflating that branch problem with the seasonal-table ancestry search.

Research record:

`docs/research/ZIWEI-DATONG-RICHU-NCL06267-DIGITAL-SURROGATE-DEDUP-R1.json`
