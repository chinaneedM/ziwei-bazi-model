from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import fmean
from typing import Iterable


@dataclass(frozen=True)
class LatencySummary:
    count: int
    min_ms: float
    mean_ms: float
    p50_ms: float
    p95_ms: float
    p99_ms: float
    max_ms: float
    throughput_per_second: float

    def as_dict(self) -> dict[str, float | int]:
        return {
            "count": self.count,
            "min_ms": self.min_ms,
            "mean_ms": self.mean_ms,
            "p50_ms": self.p50_ms,
            "p95_ms": self.p95_ms,
            "p99_ms": self.p99_ms,
            "max_ms": self.max_ms,
            "throughput_per_second": self.throughput_per_second,
        }


def percentile(values: Iterable[float], percentile_value: float) -> float:
    rows = sorted(float(value) for value in values)
    if not rows:
        raise ValueError("percentile requires at least one value")
    if not 0.0 <= percentile_value <= 100.0:
        raise ValueError("percentile_value must be in [0, 100]")
    if len(rows) == 1:
        return rows[0]
    rank = (len(rows) - 1) * (percentile_value / 100.0)
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return rows[lower]
    fraction = rank - lower
    return rows[lower] + (rows[upper] - rows[lower]) * fraction


def summarize_latencies_ms(values: Iterable[float]) -> LatencySummary:
    rows = [float(value) for value in values]
    if not rows:
        raise ValueError("latency summary requires at least one sample")
    mean = fmean(rows)
    return LatencySummary(
        count=len(rows),
        min_ms=min(rows),
        mean_ms=mean,
        p50_ms=percentile(rows, 50.0),
        p95_ms=percentile(rows, 95.0),
        p99_ms=percentile(rows, 99.0),
        max_ms=max(rows),
        throughput_per_second=(1000.0 / mean if mean > 0.0 else float("inf")),
    )
