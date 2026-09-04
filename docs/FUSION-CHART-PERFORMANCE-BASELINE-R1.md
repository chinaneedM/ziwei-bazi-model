# Fusion Chart Performance Baseline R1

## Status

```text
SOURCE_PERFORMANCE_BASELINE_R1=PENDING_EXECUTION_RECEIPT
WINDOWS_PACKAGED_PERFORMANCE_BASELINE_R1=PENDING_EXECUTION_RECEIPT
DETERMINISTIC_REPLAY_10000=RUNNING
DETERMINISTIC_REPLAY_100000=PERFORMANCE_GATED
SOAK_RESOURCE_ACCEPTANCE_R1=PENDING_EXECUTION_RECEIPT
```

No latency threshold is being invented before measurement. R1 first records reproducible baselines tied to the exact source commit and runner class; regressions can then be evaluated against measured evidence rather than an arbitrary target.

## Metrics

For source and packaged runtime the benchmark records:

- process cold start where available;
- Ziwei natal/application resolve;
- Bazi natal/application resolve;
- Combined natal resolve;
- Target Flow;
- Fusion R2;
- sample count, min/mean/P50/P95/P99/max;
- derived throughput;
- Python `tracemalloc` peak by operation;
- Windows process working-set evidence for packaged probes.

The deterministic replay receipt additionally records first-resolve and replay latency distributions, status counts, exact mismatch count, invariant-failure count, execution-error count, elapsed time, samples/second and projected 100k duration.

## Environment binding

Source measurements are produced by the dedicated Ubuntu GitHub Actions runner with Python 3.12. Packaged measurements are produced by `windows-latest` from the final emitted `FortuneChart-windows-x64.zip` at the exact workflow source SHA. These runner measurements are reproducibility baselines, not claims about every user PC.

## Pending result binding

This document remains pending until current acceptance receipts are available. It must be updated with exact workflow run IDs, source SHA, measured metrics and the 100k escalation decision. A performance failure does not authorize a canonical astrology-rule change.
