from __future__ import annotations

from datetime import datetime, timedelta

from .models import TargetTemporalInput


def sample_target_wall_times(target_input: TargetTemporalInput) -> tuple[datetime, ...]:
    """Materialize the deterministic wall-time samples bound by target lineage."""
    uncertainty = target_input.effective_uncertainty_seconds
    center = target_input.reported_local_datetime
    if uncertainty == 0:
        return (center,)
    start = center - timedelta(seconds=uncertainty)
    end = center + timedelta(seconds=uncertainty)
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
