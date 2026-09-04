# Fusion Chart Defect Report R1

## Final disposition

```text
CONFIRMED_IMPLEMENTATION_DEFECT_COUNT=0
TEST_ORACLE_DEFECT_COUNT=3
UNRESOLVED_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
ACCEPTANCE_EXECUTION_RUN=33867682199
```

The final acceptance run at source SHA `0b20a9cf6e058f096582e09b72142077399e1ac3` completed successfully. No acceptance evidence was sufficient to classify any deterministic chart rule as an `IMPLEMENTATION_DEFECT`.

## Acceptance tooling defects

### ACC-R1-ORACLE-001 — latency probe contaminated by tracemalloc

- Classification: `TEST_ORACLE_DEFECT`
- Evidence: packaged Windows receipt from workflow `33862090610` showed operation latency measured while Python `tracemalloc` was active.
- Disposition: latency and memory probes were separated; the memory probe is excluded from latency samples.
- Algorithm reopen: **No**.

### ACC-R1-ORACLE-002 — post-exit Windows working-set sample returned zero

- Classification: `TEST_ORACLE_DEFECT`
- Evidence: workflow `33862090610` recorded `process_peak_working_set_bytes=0` and zero cold-start working-set samples, which is not a physically meaningful process-memory baseline.
- Disposition: Windows now polls `WorkingSet64` while the EXE is alive and retains the observed maximum.
- Algorithm reopen: **No**.

The first packaged performance receipt is retained as calibration evidence but is not the formal R1 performance baseline.

### ACC-R1-ORACLE-003 — full-soak tracemalloc caused runner timeout

- Classification: `TEST_ORACLE_DEFECT`
- Evidence: workflow `33862724150`, soak job `100990609290`, ran until its 60-minute hard timeout and was cancelled without an engine exception or integrity failure.
- Root cause: the original soak kept Python `tracemalloc` active across all long-loop work, even though earlier calibration had already shown that tracing materially inflates CPU-heavy chart latency.
- Disposition: the 1,000-iteration HTTP soak and periodic Target Flow/Fusion R2 probes were retained. The corrected design uses low-overhead RSS/thread/fd checkpoints and a separate bounded tracemalloc probe, with checkpoint receipts during execution.
- Closure evidence: corrected soak job `101006155801` in workflow `33867682199` passed 1,000/1,000 HTTP iterations, 100 Target Flow/Fusion R2 probes, 20/20 memory probes, errors=0, thread delta=0 and fd delta=0.
- Algorithm reopen: **No**.

## Required classifications

| Classification | Meaning | May reopen algorithm? |
| --- | --- | --- |
| `IMPLEMENTATION_DEFECT` | Implementation contradicts explicit canonical/profile contract or deterministic replay evidence | Yes, locally and only with evidence |
| `EXPECTED_PROFILE_DIFFERENCE` | Different documented profile/default produces a different legitimate result | No |
| `DISPUTED_CANDIDATE` | Multiple methods are intentionally retained without a winner | No |
| `REFERENCE_DIFFERENCE` | Wenmo/Wenzhen or another reference differs | No |
| `TEST_ORACLE_DEFECT` | Test expectation, fixture, harness or measurement is wrong | No |
| `UNRESOLVED` | Evidence is insufficient to classify safely | No |

## Final acceptance interpretation

The 10,000 fixed-seed replay completed with zero deterministic mismatches, zero invariant failures and zero execution errors. Reference differentials remain non-authoritative. The three defects found during R1 all belong to the acceptance/measurement layer and do not authorize a canonical astrology-rule change.

Every future failure must still bind defect ID, capability ID, case ID/random seed/index, exact source SHA, workflow/run receipt, observed result, expected contract, classification, canonical/reference evidence, reproduction command and algorithm-reopen authorization.
