#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gc
import json
import os
import threading
import time
import tracemalloc
from pathlib import Path
from urllib.request import Request, urlopen

from fortune_training.combined_chart_application.workbench_local_app import (
    build_workbench_server,
)
from fortune_training.fusion_chart_acceptance import (
    AcceptanceHarness,
    AcceptanceLocation,
)


SOAK_SCHEMA = "FUSION-CHART-SOAK-RESOURCE-ACCEPTANCE-R1"
MEASUREMENT_MODE = "LOW_OVERHEAD_RSS_CHECKPOINTS_PLUS_BOUNDED_TRACEMALLOC"


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


def _fd_count() -> int | None:
    path = Path("/proc/self/fd")
    if not path.is_dir():
        return None
    try:
        return len(list(path.iterdir()))
    except OSError:
        return None


def _rss_bytes() -> int | None:
    path = Path("/proc/self/status")
    if not path.is_file():
        return None
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("VmRSS:"):
                fields = line.split()
                return int(fields[1]) * 1024
    except (OSError, ValueError, IndexError):
        return None
    return None


def _base_payload() -> dict[str, object]:
    return {
        "birth_datetime": "1994-05-17T14:30:00",
        "birth_place": "Beijing",
        "latitude": 39.9042,
        "longitude": 116.4074,
        "timezone_id": "Asia/Shanghai",
        "sex": "MALE",
        "precision": "EXACT_SECOND",
        "uncertainty_seconds": 0,
        "ziwei_daxian_count": 12,
        "ziwei_daxian_frame_id": None,
        "ziwei_annual_year": 2025,
        "ziwei_minor_limit_age": None,
        "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
        "bazi_dayun_count": 12,
        "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
    }


def _post(base_url: str) -> None:
    body = json.dumps(_base_payload(), separators=(",", ":")).encode()
    request = Request(
        base_url + "/api/resolve",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))
    if result.get("combined_resolution", {}).get("integrity", {}).get("status") != "PASS":
        raise RuntimeError("soak HTTP resolve integrity did not PASS")


def _write_receipt(path: Path | None, payload: dict[str, object]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def _resource_checkpoint(
    *,
    completed_iterations: int,
    started: float,
) -> dict[str, object]:
    return {
        "completed_iterations": completed_iterations,
        "elapsed_seconds": time.perf_counter() - started,
        "thread_count": threading.active_count(),
        "fd_count": _fd_count(),
        "rss_bytes": _rss_bytes(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fusion chart soak/resource leak acceptance")
    parser.add_argument("--repository-root", type=Path, default=_root())
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--memory-probe-iterations", type=int, default=20)
    parser.add_argument("--checkpoint-every", type=int, default=100)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    if args.iterations < 1:
        raise SystemExit("--iterations must be positive")
    if args.memory_probe_iterations < 1:
        raise SystemExit("--memory-probe-iterations must be positive")
    if args.checkpoint_every < 1:
        raise SystemExit("--checkpoint-every must be positive")

    root = args.repository_root.resolve()
    harness = AcceptanceHarness(root)
    location = AcceptanceLocation("Beijing", 39.9042, 116.4074, "Asia/Shanghai")
    birth = harness.birth(__import__("datetime").datetime(1994, 5, 17, 14, 30), location)
    target = harness.target(__import__("datetime").datetime(2026, 8, 18, 12, 0), location)

    baseline_threads = threading.active_count()
    baseline_fds = _fd_count()
    gc.collect()
    baseline_rss = _rss_bytes()

    server = build_workbench_server(root, port=0)
    host, port = server.server_address[:2]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://{host}:{port}"

    errors: list[str] = []
    checkpoints: list[dict[str, object]] = []
    completed_iterations = 0
    target_flow_fusion_probe_count = 0
    memory_probe_completed_iterations = 0
    memory_start = None
    memory_end = None
    memory_peak = None
    started = time.perf_counter()

    def checkpoint_payload(status: str) -> dict[str, object]:
        rss_values = [
            int(row["rss_bytes"])
            for row in checkpoints
            if row.get("rss_bytes") is not None
        ]
        return {
            "schema": SOAK_SCHEMA,
            "status": status,
            "measurement_mode": MEASUREMENT_MODE,
            "requested_iterations": args.iterations,
            "completed_iterations": completed_iterations,
            "target_flow_fusion_probe_interval": 10,
            "target_flow_fusion_probe_count": target_flow_fusion_probe_count,
            "checkpoint_every": args.checkpoint_every,
            "resource_checkpoints": checkpoints,
            "rss_baseline_bytes": baseline_rss,
            "rss_peak_checkpoint_bytes": max(rss_values) if rss_values else baseline_rss,
            "memory_probe_requested_iterations": args.memory_probe_iterations,
            "memory_probe_completed_iterations": memory_probe_completed_iterations,
            "tracemalloc_current_start_bytes": memory_start,
            "tracemalloc_current_end_bytes": memory_end,
            "tracemalloc_current_delta_bytes": (
                memory_end - memory_start
                if memory_start is not None and memory_end is not None
                else None
            ),
            "tracemalloc_peak_bytes": memory_peak,
            "memory_growth_classification": "OBSERVATIONAL_BASELINE_R1",
            "errors": errors,
            "pid": os.getpid(),
        }

    _write_receipt(args.receipt, checkpoint_payload("RUNNING"))
    try:
        for index in range(args.iterations):
            _post(base_url)
            completed_iterations = index + 1
            if index % 10 == 0:
                flow = harness.resolve_target_flow(birth, target)
                fusion = harness.resolve_fusion_r2(birth, target)
                target_flow_fusion_probe_count += 1
                if flow.integrity.status != "PASS" or fusion.integrity.status != "PASS":
                    raise RuntimeError("target-flow/fusion R2 soak integrity failed")
            if completed_iterations % args.checkpoint_every == 0:
                checkpoints.append(
                    _resource_checkpoint(
                        completed_iterations=completed_iterations,
                        started=started,
                    )
                )
                _write_receipt(args.receipt, checkpoint_payload("RUNNING"))

        tracemalloc.start()
        gc.collect()
        memory_start, _ = tracemalloc.get_traced_memory()
        try:
            for index in range(args.memory_probe_iterations):
                _post(base_url)
                memory_probe_completed_iterations = index + 1
                if index % 5 == 0:
                    flow = harness.resolve_target_flow(birth, target)
                    fusion = harness.resolve_fusion_r2(birth, target)
                    if flow.integrity.status != "PASS" or fusion.integrity.status != "PASS":
                        raise RuntimeError("bounded memory probe integrity failed")
            gc.collect()
            memory_end, memory_peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
    except Exception as exc:
        errors.append(f"{type(exc).__name__}:{exc}")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=10)

    elapsed = time.perf_counter() - started
    gc.collect()
    final_threads = threading.active_count()
    final_fds = _fd_count()
    final_rss = _rss_bytes()
    thread_delta = final_threads - baseline_threads
    fd_delta = (
        final_fds - baseline_fds
        if baseline_fds is not None and final_fds is not None
        else None
    )
    rss_delta = (
        final_rss - baseline_rss
        if baseline_rss is not None and final_rss is not None
        else None
    )

    checkpoints.append(
        {
            "completed_iterations": completed_iterations,
            "elapsed_seconds": elapsed,
            "thread_count": final_threads,
            "fd_count": final_fds,
            "rss_bytes": final_rss,
            "phase": "AFTER_SERVER_SHUTDOWN",
        }
    )
    status = "PASS"
    if (
        errors
        or completed_iterations != args.iterations
        or memory_probe_completed_iterations != args.memory_probe_iterations
        or thread.is_alive()
        or thread_delta != 0
    ):
        status = "FAIL"
    if fd_delta is not None and fd_delta > 2:
        status = "FAIL"

    payload = checkpoint_payload(status)
    payload.update(
        {
            "iterations": args.iterations,
            "elapsed_seconds": elapsed,
            "iterations_per_second": (
                args.iterations / elapsed if elapsed > 0 else None
            ),
            "server_thread_alive_after_shutdown": thread.is_alive(),
            "thread_count_before": baseline_threads,
            "thread_count_after": final_threads,
            "thread_delta": thread_delta,
            "fd_count_before": baseline_fds,
            "fd_count_after": final_fds,
            "fd_delta": fd_delta,
            "rss_current_start_bytes": baseline_rss,
            "rss_current_end_bytes": final_rss,
            "rss_current_delta_bytes": rss_delta,
        }
    )
    _write_receipt(args.receipt, payload)
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
