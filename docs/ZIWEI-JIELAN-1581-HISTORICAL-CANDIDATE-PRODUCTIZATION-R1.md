# Ziwei Jielan 1581 Historical Candidate Productization R1

Status: **CLOSED FOR READ-ONLY SOURCE-SCOPED NATAL CANDIDATE VISIBILITY / NO PRODUCTION WINNER CHANGE**

This document records productization only. Historical authority remains the existing Jielan audit rows and source-bound registry; this release does not create a new historical winner.

## 1. Public candidate identity

```text
candidate_api=ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATE-API-R1@1.0.0
rule_set=ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATES-R1@1.1.0
runtime_resolver=ZIWEI-JIELAN-1581-SOURCE-SCOPED-CANDIDATE-RUNTIME-R1@1.0.0
selection_status=PRESERVED_NOT_SELECTED
```

The package root exports the registry/runtime identities and resolver. `/api/profiles` advertises the read-only candidate profile with its registry hash and Workbench endpoint.

## 2. Released fact whitelist

Only three already-audited natal facts are exposed:

- `kui_yue` — Jielan 1581 Kui/Yue source family;
- `fire_bell` — Jielan 1581 Fire/Bell start family plus birth-hour replay;
- `mingzhu` — Jielan 1581 birth-year-branch Mingzhu basis.

The product surface deliberately excludes dignity normalization, Zi/Wu Shenzhu arbitration, Four-Transformation candidate selection, rings/limits and every other resolver fact not selected by Batch 12OH.

## 3. Exact source binding

`POST /api/ziwei-jielan-1581-candidate` derives its inputs from the exact validated Ziwei application bundle. The response binds the combined manifest hash, Ziwei bundle hash, natal fact/computation hashes, registry hash and candidate runtime hash.

The browser receives facts; it does not contain branch tables, modulo arithmetic or placement formulas.

## 4. Non-selection firewall

The Workbench is read-only. It has no control that makes the candidate the production chart, no winner/rank semantics, and no mutation of `build_production_ziwei_profile`.

```text
production_winner_selected=false
production_profile_changed=false
candidate_selection=PRESERVED_NOT_SELECTED
```

## 5. Audit accounting

Productization closes three previously discovered `MISSING_FROM_PRODUCT` rows without changing cumulative discovery history.

```text
TOTAL_MATRIX_ROWS=222
AUDITED_ROWS=222
CUMULATIVE_IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CURRENT_MISSING_FROM_PRODUCT_ROWS=7
HISTORICAL_CANDIDATE_EXTENSION_COUNT=11
HISTORICAL_CANDIDATE_REGISTRY_COUNT=3
HISTORICAL_CANDIDATE_RUNTIME_RESOLVER_COUNT=3
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=43
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=43
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

Production deterministic closure remains unchanged.
