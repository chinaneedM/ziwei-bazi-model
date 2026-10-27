# Ziwei Jielan Dignity Historical Candidate Productization R1

Status: **CLOSED FOR READ-ONLY SOURCE-LEXEME VISIBILITY / NO PRODUCTION DIGNITY CHANGE**

This document records productization only. Historical authority remains Batch 12OM (CH70 raw source lexemes) and Batch 12ON (CH69↔CH70 cell cross-collation).

## Contract

```text
candidate_api=ZIWEI-JIELAN-1581-DIGNITY-HISTORICAL-CANDIDATE-API-R1@1.0.0
registry=ZIWEI-JIELAN-1581-DIGNITY-LEXEME-CANDIDATES-R1@1.0.0
candidate=JIELAN-1581-DIGNITY-CH70-SOURCE-LEXEME-R1
runtime_resolver=ZIWEI-JIELAN-1581-DIGNITY-LEXEME-RUNTIME-R1@1.0.0
cross_collation=ZIWEI-JIELAN-1581-DIGNITY-CH69-CH70-CROSS-COLLATION-R1@1.0.0
selection_status=PRESERVED_NOT_SELECTED
endpoint=/api/ziwei-jielan-1581-dignity-candidate
```

The endpoint returns 300 CH70 source-lexeme rows and 300 CH69↔CH70 cross-collation rows, plus the frozen relation-count summary.

## Exact chart binding

The sidecar is resolved from the same validated combined request and returns the combined manifest hash, Ziwei bundle hash, natal FactHash / ComputationHash, registry hash, candidate runtime hash and cross-collation hash.

The historical dignity rows themselves do not depend on the natal birth input; the chart binding exists so every Workbench evidence panel is attached to one exact resolved product state and cannot be confused with another run.

## Browser boundary

The Workbench renders backend-returned fields only:

- display name;
- branch;
- CH70 raw source lexemes;
- CH69 raw parallel lexemes;
- relation classification;
- unresolved-source note when present.

The browser contains no source table constants, no source-local polarity rules, no gloss-normalization engine, no modern dignity grade conversion and no winner control.

## Non-selection firewall

```text
production_grade_mapping_present=false
ch69_used_to_fill_ch70=false
ch70_used_to_overwrite_ch69=false
production_winner_selected=false
production_profile_changed=false
chart_algorithm_reopened=false
```

Product visibility is evidence inspection, not historical arbitration.

## Accounting

`HPA-ZIWEI-018` leaves `MISSING_FROM_PRODUCT` because the audited historical candidate now has a complete internal representation, source cross-collation and explicit read-only product surface.

```text
TOTAL_MATRIX_ROWS=222
AUDITED_ROWS=222
CURRENT_MISSING_FROM_PRODUCT_ROWS=5
HISTORICAL_CANDIDATE_EXTENSION_COUNT=14
HISTORICAL_CANDIDATE_REGISTRY_COUNT=5
HISTORICAL_CANDIDATE_RUNTIME_RESOLVER_COUNT=5
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=43
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=43
ALGORITHM_REOPEN_COUNT=0
```
