from __future__ import annotations

from datetime import datetime, timedelta

from .models import TimePrecision


SAMPLING_ALGORITHM_ID = "TEMPORAL-UNCERTAINTY-SAMPLING-V1"
SAMPLING_ALGORITHM_VERSION = "1.0.0"


def sample_wall_times(
    center: datetime,
    effective_uncertainty_seconds: int,
) -> tuple[datetime, ...]:
    """Return the deterministic point samples used by temporal coordinate resolvers."""

    if center.tzinfo is not None:
        raise ValueError("sample center must be a naive wall-clock datetime")
    if effective_uncertainty_seconds < 0:
        raise ValueError("effective_uncertainty_seconds must be non-negative")
    if effective_uncertainty_seconds == 0:
        return (center,)

    start = center - timedelta(seconds=effective_uncertainty_seconds)
    end = center + timedelta(seconds=effective_uncertainty_seconds)
    span_seconds = (end - start).total_seconds()
    step_seconds = 60 if span_seconds <= 86_400 else max(3600, int(span_seconds / 1998))
    rows = {start, center, end}
    cursor = start.replace(second=0, microsecond=0) + timedelta(minutes=1)
    if step_seconds >= 3600:
        cursor = start.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    while cursor < end and len(rows) < 2001:
        rows.add(cursor)
        cursor += timedelta(seconds=step_seconds)
    return tuple(sorted(rows))


def point_sample_precision(precision: TimePrecision) -> TimePrecision:
    """Normalize a sampled point while preserving the source interval semantics upstream."""

    return TimePrecision.EXACT_SECOND if precision is TimePrecision.APPROXIMATE else precision
