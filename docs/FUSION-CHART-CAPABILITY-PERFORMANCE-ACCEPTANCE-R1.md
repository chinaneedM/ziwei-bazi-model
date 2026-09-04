# Fusion Chart Capability & Performance Acceptance R1

## State

```text
FUSION_CHART_CAPABILITY_PERFORMANCE_ACCEPTANCE_R1=ACCEPTED
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
REFERENCE_IMPLEMENTATION_AUTHORITY=FALSE
```

R1 validates the already-closed deterministic Ziwei + Bazi fusion chart product. It does not add chart fields, choose disputed doctrine winners, or reopen canonical algorithms merely to make a test pass.

## Failure classification gate

Every failure is classified as exactly one of:

- `IMPLEMENTATION_DEFECT`
- `EXPECTED_PROFILE_DIFFERENCE`
- `DISPUTED_CANDIDATE`
- `REFERENCE_DIFFERENCE`
- `TEST_ORACLE_DEFECT`
- `UNRESOLVED`

Only an `IMPLEMENTATION_DEFECT` backed by explicit canonical/replay evidence may authorize a local algorithm reopen. Reference-implementation disagreement alone is never sufficient.

## Test layers

1. **Golden Case Corpus** — civil time/DST, true-solar date crossing, lunar/leap month, late-Zi policies, Li Chun, Bazi Dayun and Ziwei Daxian/minor-limit sequences.
2. **Temporal Boundary Torture** — second-level checks around DST gaps/folds, 23:00/midnight, solar-term switching, leap-month entry and true-solar cross-day stability.
3. **Replay/property invariants** — fixed-seed random Combined resolutions recomputed exactly and checked for manifest/hash, shared-time, candidate-lineage, 12-palace, four-pillar and temporal-sequence invariants.
4. **Reference differential** — Wenmo/Wenzhen snapshots remain comparison inputs only and never become canonical authority automatically.
5. **Performance** — source and emitted Windows EXE measure cold start and Ziwei/Bazi/Combined/Target Flow/Fusion R2 latency, P50/P95/P99, throughput and memory evidence.
6. **Soak/resource stability** — repeated loopback HTTP resolution plus Target Flow/Fusion R2 probes check server shutdown, thread/fd stability, RSS checkpoints and a bounded tracemalloc memory probe.

## Final execution evidence

The accepted execution is bound to:

- source SHA: `0b20a9cf6e058f096582e09b72142077399e1ac3`;
- dedicated workflow: `33867682199` — **SUCCESS**;
- clean-training-system workflow: `33867682181` — **SUCCESS**;
- exact-head Windows application version: `0.2.5`.

### Deterministic replay

The merged 10k receipt reported:

```text
DETERMINISTIC_REPLAY_10000=PASS
COMPLETED_SAMPLES=10000
DETERMINISTIC_MISMATCH_COUNT=0
INVARIANT_FAILURE_COUNT=0
EXECUTION_ERROR_COUNT=0
STATUS_COUNTS=RESOLVED_BOTH:9999,UNCERTAINTY_PRESENT:1
SHARD_COUNT=10
MAX_SHARD_ELAPSED_SECONDS=1775.034117533
PROJECTED_100K_PARALLEL_WALL_SECONDS=8875.170587665
```

All 10 shards passed. The single `UNCERTAINTY_PRESENT` case is an intentional temporal-status branch and replayed deterministically with its invariants intact.

The 100k stage was **SKIPPED_PERFORMANCE_BUDGET**, not failed: the measured projection of about 8,875 seconds exceeded the configured 3,600-second escalation budget.

### Soak/resource acceptance

The corrected soak completed:

- 1,000/1,000 HTTP Combined resolutions;
- 100 periodic Target Flow + Fusion R2 integrity probes;
- 20/20 bounded tracemalloc memory probes;
- zero recorded errors;
- thread delta = 0;
- file-descriptor delta = 0;
- loopback server thread stopped cleanly.

RSS checkpoints during the 100–1,000 iteration long loop stayed approximately 59.8–63.5 MB. The final process RSS after the bounded memory probe was approximately 84.2 MB; this is retained as an observational R1 baseline, not misclassified as either proof of a leak or proof of zero memory retention.

## Acceptance conclusion

```text
CONFIRMED_IMPLEMENTATION_DEFECT_COUNT=0
TEST_ORACLE_DEFECT_COUNT=3
UNRESOLVED_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```

Three acceptance-harness/measurement defects were found and repaired. None authorized or caused a deterministic astrology-rule change. The deterministic chart product remains CLOSED.

The machine-readable scope/status registry is `docs/FUSION-CHART-CAPABILITY-MATRIX-R1.json`. Performance evidence is in `docs/FUSION-CHART-PERFORMANCE-BASELINE-R1.md`; failure classification is in `docs/FUSION-CHART-DEFECT-REPORT-R1.md`.
