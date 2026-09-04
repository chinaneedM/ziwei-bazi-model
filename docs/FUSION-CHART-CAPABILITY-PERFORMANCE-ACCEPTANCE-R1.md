# Fusion Chart Capability & Performance Acceptance R1

## State

```text
FUSION_CHART_CAPABILITY_PERFORMANCE_ACCEPTANCE_R1=IN_PROGRESS
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
REFERENCE_IMPLEMENTATION_AUTHORITY=FALSE
```

This acceptance phase validates the already-closed deterministic Ziwei + Bazi fusion chart product. It does not add chart fields, choose disputed doctrine winners, or reopen canonical algorithms merely to make a test pass.

## Failure classification gate

Every failure must first be classified as exactly one of:

- `IMPLEMENTATION_DEFECT`
- `EXPECTED_PROFILE_DIFFERENCE`
- `DISPUTED_CANDIDATE`
- `REFERENCE_DIFFERENCE`
- `TEST_ORACLE_DEFECT`
- `UNRESOLVED`

Only an `IMPLEMENTATION_DEFECT` backed by explicit canonical/replay evidence may authorize a local algorithm reopen. Reference-implementation disagreement alone is never sufficient.

## Test layers

1. **Golden Case Corpus** — fixed cases for civil time/DST, true-solar date crossing, lunar/leap month, late-Zi policies, Li Chun, Bazi Dayun and Ziwei Daxian/minor-limit sequences.
2. **Temporal Boundary Torture** — second-level checks around DST gaps/folds, 23:00/midnight, solar-term switching, leap-month entry and true-solar cross-day stability.
3. **Replay/property invariants** — fixed-seed random Combined resolutions are recomputed exactly and checked for manifest/hash, shared-time, candidate-lineage, 12-palace, four-pillar and temporal-sequence invariants.
4. **Reference differential** — Wenmo/Wenzhen snapshots are comparison inputs only; differences are classified but never treated as canonical corrections automatically.
5. **Performance** — source and emitted Windows EXE measure cold start and Ziwei/Bazi/Combined/Target Flow/Fusion R2 latency, P50/P95/P99, throughput and memory evidence.
6. **Soak/resource stability** — repeated loopback HTTP resolution plus Target Flow/Fusion R2 checks thread, file-descriptor/socket shutdown and Python memory trend.

## Execution policy

The dedicated workflow is `.github/workflows/fusion-chart-capability-performance-r1.yml`. The normal Product R1 CI remains separate. The acceptance workflow first runs focused tests, then 10,000 deterministic random cases. It escalates to a full 100,000-case run only when the 10k measured runtime projects the 100k run within the configured performance budget.

The Windows job builds the exact current source commit into the portable ZIP, expands the emitted artifact, launches the packaged `FortuneChart.exe`, records process cold-start-to-loopback-ready samples, and runs the same operation benchmark from inside the packaged runtime.

## Current evidence

Focused Golden Corpus, Temporal Torture, differential-governance and metric utility tests passed in workflow run `33861911986` before its 10k stage began. Long-run deterministic replay, source baseline, soak, and exact-head Windows packaged performance remain execution evidence to be bound when their receipts complete.

The machine-readable scope/status registry is `docs/FUSION-CHART-CAPABILITY-MATRIX-R1.json`. Performance results are recorded in `docs/FUSION-CHART-PERFORMANCE-BASELINE-R1.md`; failure classification is recorded in `docs/FUSION-CHART-DEFECT-REPORT-R1.md`.
