#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge deterministic replay shard receipts")
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("--expected-samples", type=int, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    rows: list[dict[str, Any]] = []
    for path in sorted(args.input_dir.rglob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        base = payload.get("base_run")
        if isinstance(base, dict) and base.get("schema") == "FUSION-CHART-DETERMINISTIC-RANDOM-REPLAY-R1":
            rows.append(base)
    if not rows:
        raise SystemExit("no deterministic replay shard receipts found")

    rows.sort(key=lambda row: int(row["start_index"]))
    expected_index = 0
    statuses: Counter[str] = Counter()
    completed = mismatches = invariant_failures = execution_errors = 0
    elapsed_compute_seconds = 0.0
    max_shard_elapsed_seconds = 0.0
    shard_summaries: list[dict[str, Any]] = []
    for row in rows:
        start = int(row["start_index"])
        end = int(row["end_index_exclusive"])
        if start != expected_index:
            raise SystemExit(
                f"replay shard coverage gap/overlap: expected {expected_index}, got {start}"
            )
        expected_index = end
        requested = int(row["requested_samples"])
        completed += int(row["completed_samples"])
        mismatches += int(row["deterministic_mismatch_count"])
        invariant_failures += int(row["invariant_failure_count"])
        execution_errors += int(row["execution_error_count"])
        statuses.update({str(k): int(v) for k, v in row["status_counts"].items()})
        elapsed = float(row["elapsed_seconds"])
        elapsed_compute_seconds += elapsed
        max_shard_elapsed_seconds = max(max_shard_elapsed_seconds, elapsed)
        shard_summaries.append({
            "start_index": start,
            "end_index_exclusive": end,
            "requested_samples": requested,
            "status": row["status"],
            "elapsed_seconds": elapsed,
            "samples_per_second": row["samples_per_second"],
            "first_resolution_latency": row["first_resolution_latency"],
            "replay_resolution_latency": row["replay_resolution_latency"],
        })

    if expected_index != args.expected_samples:
        raise SystemExit(
            f"replay shard coverage ended at {expected_index}, expected {args.expected_samples}"
        )
    status = (
        "PASS"
        if completed == args.expected_samples
        and mismatches == 0
        and invariant_failures == 0
        and execution_errors == 0
        and all(row["status"] == "PASS" for row in rows)
        else "FAIL"
    )
    shard_size = max(int(row["requested_samples"]) for row in rows)
    projected_100k_parallel_wall_seconds = (
        max_shard_elapsed_seconds * (5000.0 / shard_size)
    )
    payload = {
        "schema": "FUSION-CHART-DETERMINISTIC-REPLAY-MERGED-R1",
        "status": status,
        "requested_samples": args.expected_samples,
        "completed_samples": completed,
        "status_counts": dict(sorted(statuses.items())),
        "deterministic_mismatch_count": mismatches,
        "invariant_failure_count": invariant_failures,
        "execution_error_count": execution_errors,
        "shard_count": len(rows),
        "elapsed_compute_seconds": elapsed_compute_seconds,
        "max_shard_elapsed_seconds": max_shard_elapsed_seconds,
        "projected_100k_parallel_wall_seconds": projected_100k_parallel_wall_seconds,
        "shards": shard_summaries,
        "failure_classification_required": True,
        "algorithm_reopen_policy": "IMPLEMENTATION_DEFECT_WITH_EXPLICIT_EVIDENCE_ONLY",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
