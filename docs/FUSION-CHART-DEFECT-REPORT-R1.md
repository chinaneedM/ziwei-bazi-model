# Fusion Chart Defect Report R1

## Current disposition

```text
CONFIRMED_IMPLEMENTATION_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

No acceptance failure has yet produced evidence sufficient to classify a deterministic chart rule as an `IMPLEMENTATION_DEFECT`.

## Acceptance tooling defects

### ACC-R1-ORACLE-001 — latency probe contaminated by tracemalloc

- Classification: `TEST_ORACLE_DEFECT`
- Evidence: packaged Windows receipt from workflow `33862090610` showed operation latency measured while Python `tracemalloc` was active.
- Disposition: latency and memory probes are now separated; the memory probe is excluded from latency samples.
- Algorithm reopen: **No**.

### ACC-R1-ORACLE-002 — post-exit Windows working-set sample returned zero

- Classification: `TEST_ORACLE_DEFECT`
- Evidence: the same receipt recorded `process_peak_working_set_bytes=0` and zero cold-start working-set samples, which is not a physically meaningful process-memory baseline.
- Disposition: the workflow now polls `WorkingSet64` while the EXE is alive and keeps the observed maximum.
- Algorithm reopen: **No**.

The first packaged performance receipt is retained as calibration evidence but is not accepted as the formal R1 performance baseline.

## Required classifications

| Classification | Meaning | May reopen algorithm? |
| --- | --- | --- |
| `IMPLEMENTATION_DEFECT` | Implementation contradicts explicit canonical/profile contract or deterministic replay evidence | Yes, locally and only with evidence |
| `EXPECTED_PROFILE_DIFFERENCE` | Different documented profile/default produces a different legitimate result | No |
| `DISPUTED_CANDIDATE` | Multiple methods are intentionally retained without a winner | No |
| `REFERENCE_DIFFERENCE` | Wenmo/Wenzhen or another reference differs | No |
| `TEST_ORACLE_DEFECT` | Test expectation, fixture, harness or measurement is wrong | No |
| `UNRESOLVED` | Evidence is insufficient to classify safely | No |

## Report fields for every future failure

Each defect entry must bind: defect ID, capability ID, case ID/random seed/index, exact source SHA, workflow/run receipt, observed result, expected contract, classification, canonical/reference evidence, reproduction command, and whether an algorithm reopen was authorized.

Reference differential tooling is structurally unable to emit `IMPLEMENTATION_DEFECT`; escalation from a reference mismatch requires a separate evidence review.
