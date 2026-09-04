# Fusion Chart Performance Baseline R1

## Status

```text
SOURCE_PERFORMANCE_BASELINE_R1=PASS
WINDOWS_PACKAGED_PERFORMANCE_BASELINE_R1=PASS
DETERMINISTIC_REPLAY_10000=PASS
DETERMINISTIC_REPLAY_100000=SKIPPED_PERFORMANCE_BUDGET
SOAK_RESOURCE_ACCEPTANCE_R1=PASS
DETERMINISTIC_REPLAY_MISMATCH_COUNT=0
DETERMINISTIC_REPLAY_INVARIANT_FAILURE_COUNT=0
DETERMINISTIC_REPLAY_EXECUTION_ERROR_COUNT=0
```

Evidence source SHA: `0b20a9cf6e058f096582e09b72142077399e1ac3`  
Dedicated workflow run: `33867682199` — **SUCCESS**

No arbitrary latency pass/fail threshold was invented. These measurements are reproducibility baselines tied to the exact GitHub Actions runner class and source SHA.

## Source baseline — Ubuntu / Python 3.12

| Operation | P50 | P95 | Throughput | tracemalloc peak |
| --- | ---: | ---: | ---: | ---: |
| Cold process + harness + one Combined resolve | 827.456 ms | 831.930 ms | 1.207/s | n/a |
| Bazi natal/application | 6.073 ms | 6.188 ms | 164.318/s | 1,756,014 B |
| Ziwei natal/application | 265.054 ms | 270.712 ms | 3.792/s | 8,198,439 B |
| Combined natal | 480.521 ms | 490.439 ms | 2.073/s | 8,567,077 B |
| Target Flow | 648.724 ms | 659.696 ms | 1.540/s | 8,565,304 B |
| Fusion R2 | 1,362.971 ms | 1,379.215 ms | 0.734/s | 8,907,566 B |

The source cold-process number includes Python/script startup, acceptance-harness initialization and one Combined resolve; it is not the same scope as the packaged EXE loopback-ready probe.

## Windows packaged EXE baseline — FortuneChart 0.2.5

Exact packaged receipt source commit: `0b20a9cf6e058f096582e09b72142077399e1ac3`.

| Operation | P50 | P95 | Throughput | tracemalloc peak |
| --- | ---: | ---: | ---: | ---: |
| Cold start to loopback ready | 569.551 ms | 616.406 ms | n/a | n/a |
| Bazi natal/application | 8.945 ms | 9.259 ms | 111.184/s | 1,756,111 B |
| Ziwei natal/application | 358.460 ms | 369.021 ms | 2.800/s | 8,198,919 B |
| Combined natal | 671.713 ms | 681.571 ms | 1.495/s | 8,567,859 B |
| Target Flow | 873.944 ms | 887.245 ms | 1.139/s | 8,567,350 B |
| Fusion R2 | 1,828.731 ms | 1,854.624 ms | 0.546/s | 8,909,106 B |

Cold-start working-set samples were 40,026,112 B, 41,230,336 B and 41,328,640 B. The benchmark process peak working set was 58,978,304 B.

## Deterministic replay baseline

```text
requested_samples=10000
completed_samples=10000
shard_count=10
deterministic_mismatch_count=0
invariant_failure_count=0
execution_error_count=0
status_counts.RESOLVED_BOTH=9999
status_counts.UNCERTAINTY_PRESENT=1
elapsed_compute_seconds=16169.081978079
max_shard_elapsed_seconds=1775.034117533
projected_100k_parallel_wall_seconds=8875.170587665
```

The 100k escalation gate required a projected parallel wall time <= 3,600 seconds. The measured projection was about 8,875 seconds, so the 100k job was correctly skipped. This is a capacity decision, not a correctness failure.

## Soak/resource baseline

The accepted soak ran 1,000 HTTP Combined resolutions and every tenth iteration also resolved Target Flow and Fusion R2, for 100 cross-system temporal probes. A separate bounded tracemalloc phase completed 20/20 memory-probe iterations.

```text
status=PASS
completed_iterations=1000
elapsed_seconds=1570.838879495
iterations_per_second=0.636602526875
errors=0
target_flow_fusion_probe_count=100
memory_probe_completed_iterations=20
thread_delta=0
fd_delta=0
server_thread_alive_after_shutdown=false
rss_baseline_bytes=38871040
rss_long_loop_checkpoint_range_bytes=59768832..63451136
rss_after_bounded_memory_probe_bytes=84180992
tracemalloc_current_delta_bytes=309818
tracemalloc_peak_bytes=16792508
```

The long-loop RSS checkpoints are the primary R1 trend baseline. The post-memory-probe RSS is recorded separately because Python allocator/tracing behavior can retain arenas after the bounded probe. R1 does not invent a memory-leak threshold from a single runner observation; future regression work should compare steady-state checkpoint slopes/ranges against this baseline.

## Environment binding

Source measurements use the dedicated Ubuntu GitHub Actions runner with Python 3.12. Packaged measurements use `windows-latest` from the final emitted `FortuneChart-windows-x64.zip`. These are reproducibility baselines, not claims about every user PC.
