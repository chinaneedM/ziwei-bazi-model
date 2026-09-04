from __future__ import annotations

import random
import time
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .harness import AcceptanceHarness, DEFAULT_ACCEPTANCE_LOCATIONS
from .invariants import (
    combined_invariant_violations,
    deterministic_resolution_signature,
)
from .metrics import summarize_latencies_ms


RANDOM_REPLAY_SCHEMA = "FUSION-CHART-DETERMINISTIC-RANDOM-REPLAY-R1"
DEFAULT_SEED = 20260904
START = datetime(1971, 1, 1, 0, 0, 0)
END = datetime(2035, 12, 31, 23, 59, 59)
SPAN_SECONDS = int((END - START).total_seconds())


def deterministic_random_cases(
    count: int,
    *,
    seed: int = DEFAULT_SEED,
    start_index: int = 0,
) -> list[tuple[datetime, Any, str]]:
    if count < 1:
        raise ValueError("count must be positive")
    if start_index < 0:
        raise ValueError("start_index must be non-negative")
    rng = random.Random(seed)
    rows: list[tuple[datetime, Any, str]] = []
    for index in range(start_index + count):
        local = START + timedelta(seconds=rng.randrange(SPAN_SECONDS + 1))
        location = DEFAULT_ACCEPTANCE_LOCATIONS[
            rng.randrange(len(DEFAULT_ACCEPTANCE_LOCATIONS))
        ]
        sex = "MALE" if rng.getrandbits(1) == 0 else "FEMALE"
        if index >= start_index:
            rows.append((local, location, sex))
    return rows


def run_random_replay(
    repository_root: Path,
    *,
    samples: int,
    seed: int = DEFAULT_SEED,
    start_index: int = 0,
    max_failure_examples: int = 20,
) -> dict[str, Any]:
    harness = AcceptanceHarness(repository_root)
    statuses: Counter[str] = Counter()
    first_latencies_ms: list[float] = []
    replay_latencies_ms: list[float] = []
    deterministic_mismatch_count = 0
    invariant_failure_count = 0
    execution_error_count = 0
    deterministic_mismatches: list[dict[str, object]] = []
    invariant_failures: list[dict[str, object]] = []
    execution_errors: list[dict[str, object]] = []

    started = time.perf_counter()
    for offset, (local, location, sex) in enumerate(
        deterministic_random_cases(
            samples,
            seed=seed,
            start_index=start_index,
        )
    ):
        index = start_index + offset
        case_identity = {
            "index": index,
            "local": local.isoformat(),
            "place": location.place,
            "timezone_id": location.timezone_id,
            "sex": sex,
        }
        try:
            birth = harness.birth(local, location)
            t0 = time.perf_counter()
            first = harness.resolve_combined(birth, sex=sex)
            t1 = time.perf_counter()
            second = harness.resolve_combined(birth, sex=sex)
            t2 = time.perf_counter()
            first_latencies_ms.append((t1 - t0) * 1000.0)
            replay_latencies_ms.append((t2 - t1) * 1000.0)
            statuses[first.status] += 1

            first_signature = deterministic_resolution_signature(first)
            second_signature = deterministic_resolution_signature(second)
            if first != second or first_signature != second_signature:
                deterministic_mismatch_count += 1
                if len(deterministic_mismatches) < max_failure_examples:
                    deterministic_mismatches.append(
                        {
                            **case_identity,
                            "first_signature": first_signature,
                            "second_signature": second_signature,
                            "first_manifest_hash": first.manifest_hash,
                            "second_manifest_hash": second.manifest_hash,
                        }
                    )
            violations = combined_invariant_violations(first)
            if violations:
                invariant_failure_count += 1
                if len(invariant_failures) < max_failure_examples:
                    invariant_failures.append(
                        {**case_identity, "violations": list(violations)}
                    )
        except Exception as exc:
            execution_error_count += 1
            if len(execution_errors) < max_failure_examples:
                execution_errors.append(
                    {
                        **case_identity,
                        "exception_type": type(exc).__name__,
                        "detail": str(exc),
                    }
                )

    elapsed = time.perf_counter() - started
    completed = samples - execution_error_count
    status = (
        "PASS"
        if deterministic_mismatch_count == 0
        and invariant_failure_count == 0
        and execution_error_count == 0
        else "FAIL"
    )
    return {
        "schema": RANDOM_REPLAY_SCHEMA,
        "status": status,
        "seed": seed,
        "start_index": start_index,
        "end_index_exclusive": start_index + samples,
        "requested_samples": samples,
        "completed_samples": completed,
        "status_counts": dict(sorted(statuses.items())),
        "deterministic_mismatch_count": deterministic_mismatch_count,
        "invariant_failure_count": invariant_failure_count,
        "execution_error_count": execution_error_count,
        "deterministic_mismatch_examples": deterministic_mismatches,
        "invariant_failure_examples": invariant_failures,
        "execution_error_examples": execution_errors,
        "failure_examples_capped_at": max_failure_examples,
        "first_resolution_latency": summarize_latencies_ms(
            first_latencies_ms
        ).as_dict()
        if first_latencies_ms
        else None,
        "replay_resolution_latency": summarize_latencies_ms(
            replay_latencies_ms
        ).as_dict()
        if replay_latencies_ms
        else None,
        "elapsed_seconds": elapsed,
        "samples_per_second": (samples / elapsed if elapsed > 0.0 else None),
        "projected_100000_seconds": (
            elapsed * (100000.0 / samples) if samples > 0 else None
        ),
        "failure_classification_required": True,
        "algorithm_reopen_policy": "IMPLEMENTATION_DEFECT_WITH_EXPLICIT_EVIDENCE_ONLY",
    }
