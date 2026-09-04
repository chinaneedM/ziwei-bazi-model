#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from fortune_training.fusion_chart_acceptance.harness import (
    AcceptanceHarness,
    AcceptanceLocation,
)
from fortune_training.fusion_chart_acceptance.metrics import summarize_latencies_ms
from fortune_training.fusion_chart_acceptance.performance import (
    benchmark_source_runtime,
)


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


def _cold_worker(repository_root: Path) -> int:
    harness = AcceptanceHarness(repository_root)
    birth = harness.birth(
        __import__("datetime").datetime(1994, 5, 17, 14, 30),
        AcceptanceLocation("Beijing", 39.9042, 116.4074, "Asia/Shanghai"),
    )
    resolution = harness.resolve_combined(birth)
    print(
        json.dumps(
            {"status": resolution.integrity.status, "manifest_hash": resolution.manifest_hash},
            sort_keys=True,
        )
    )
    return 0


def _cold_start_samples(repository_root: Path, iterations: int) -> dict[str, object]:
    durations: list[float] = []
    script = Path(__file__).resolve()
    for _ in range(iterations):
        started = time.perf_counter()
        completed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--repository-root",
                str(repository_root),
                "--cold-worker",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        duration = (time.perf_counter() - started) * 1000.0
        payload = json.loads(completed.stdout.strip().splitlines()[-1])
        if payload.get("status") != "PASS":
            raise RuntimeError("cold worker did not PASS")
        durations.append(duration)
    return summarize_latencies_ms(durations).as_dict()


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark source fusion-chart runtime")
    parser.add_argument("--repository-root", type=Path, default=_root())
    parser.add_argument("--iterations", type=int, default=7)
    parser.add_argument("--cold-start-iterations", type=int, default=3)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--cold-worker", action="store_true")
    args = parser.parse_args()
    root = args.repository_root.resolve()
    if args.cold_worker:
        return _cold_worker(root)

    payload = benchmark_source_runtime(root, iterations=args.iterations)
    payload["cold_start_process"] = _cold_start_samples(
        root, args.cold_start_iterations
    )
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(text, encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
