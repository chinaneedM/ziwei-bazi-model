from __future__ import annotations

import gc
import time
import tracemalloc
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from .harness import AcceptanceHarness, AcceptanceLocation
from .metrics import summarize_latencies_ms


PERFORMANCE_RECEIPT_SCHEMA = "FUSION-CHART-SOURCE-PERFORMANCE-R1"


def _measure_callable(
    operation: Callable[[], object],
    *,
    iterations: int,
    warmups: int = 1,
) -> dict[str, Any]:
    if iterations < 1:
        raise ValueError("iterations must be positive")
    for _ in range(warmups):
        operation()
    # Latency and memory are measured in separate phases.  Running tracemalloc
    # during latency samples materially distorts this CPU-heavy pure-Python
    # workload and therefore is a test-oracle defect, not a product metric.
    durations: list[float] = []
    for _ in range(iterations):
        started = time.perf_counter()
        operation()
        durations.append((time.perf_counter() - started) * 1000.0)

    gc.collect()
    tracemalloc.start()
    operation()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        **summarize_latencies_ms(durations).as_dict(),
        "tracemalloc_peak_bytes": peak,
        "memory_probe_iterations": 1,
        "memory_probe_excluded_from_latency": True,
    }


def benchmark_runtime(
    repository_root: Path,
    *,
    iterations: int = 7,
    schema: str = PERFORMANCE_RECEIPT_SCHEMA,
) -> dict[str, Any]:
    harness = AcceptanceHarness(repository_root)
    beijing = AcceptanceLocation("Beijing", 39.9042, 116.4074, "Asia/Shanghai")
    birth = harness.birth(datetime(1994, 5, 17, 14, 30), beijing)
    target = harness.target(datetime(2026, 8, 18, 12, 0), beijing)

    operations = {
        "ziwei_natal_application": lambda: harness.resolve_ziwei(birth),
        "bazi_natal_application": lambda: harness.resolve_bazi(birth),
        "combined_natal": lambda: harness.resolve_combined(birth),
        "target_flow": lambda: harness.resolve_target_flow(birth, target),
        "fusion_r2": lambda: harness.resolve_fusion_r2(birth, target),
    }
    metrics = {
        name: _measure_callable(fn, iterations=iterations)
        for name, fn in operations.items()
    }
    return {
        "schema": schema,
        "status": "PASS",
        "iterations_per_operation": iterations,
        "metrics": metrics,
        "memory_metric_scope": "PYTHON_TRACEMALLOC_PEAK_PER_OPERATION",
        "latency_clock": "time.perf_counter",
    }


def benchmark_source_runtime(
    repository_root: Path,
    *,
    iterations: int = 7,
) -> dict[str, Any]:
    return benchmark_runtime(
        repository_root,
        iterations=iterations,
        schema=PERFORMANCE_RECEIPT_SCHEMA,
    )
