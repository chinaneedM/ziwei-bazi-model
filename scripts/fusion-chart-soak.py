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


def main() -> int:
    parser = argparse.ArgumentParser(description="Fusion chart soak/resource leak acceptance")
    parser.add_argument("--repository-root", type=Path, default=_root())
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    root = args.repository_root.resolve()

    harness = AcceptanceHarness(root)
    location = AcceptanceLocation("Beijing", 39.9042, 116.4074, "Asia/Shanghai")
    birth = harness.birth(__import__("datetime").datetime(1994, 5, 17, 14, 30), location)
    target = harness.target(__import__("datetime").datetime(2026, 8, 18, 12, 0), location)

    baseline_threads = threading.active_count()
    baseline_fds = _fd_count()
    server = build_workbench_server(root, port=0)
    host, port = server.server_address[:2]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://{host}:{port}"

    errors: list[str] = []
    tracemalloc.start()
    gc.collect()
    memory_start, _ = tracemalloc.get_traced_memory()
    started = time.perf_counter()
    try:
        for index in range(args.iterations):
            _post(base_url)
            if index % 10 == 0:
                flow = harness.resolve_target_flow(birth, target)
                fusion = harness.resolve_fusion_r2(birth, target)
                if flow.integrity.status != "PASS" or fusion.integrity.status != "PASS":
                    raise RuntimeError("target-flow/fusion R2 soak integrity failed")
    except Exception as exc:
        errors.append(f"{type(exc).__name__}:{exc}")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=10)

    elapsed = time.perf_counter() - started
    gc.collect()
    memory_end, memory_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    final_threads = threading.active_count()
    final_fds = _fd_count()
    thread_delta = final_threads - baseline_threads
    fd_delta = (
        final_fds - baseline_fds
        if baseline_fds is not None and final_fds is not None
        else None
    )
    status = "PASS"
    if errors or thread.is_alive() or thread_delta != 0:
        status = "FAIL"
    if fd_delta is not None and fd_delta > 2:
        status = "FAIL"

    payload = {
        "schema": "FUSION-CHART-SOAK-RESOURCE-ACCEPTANCE-R1",
        "status": status,
        "iterations": args.iterations,
        "elapsed_seconds": elapsed,
        "iterations_per_second": args.iterations / elapsed if elapsed > 0 else None,
        "errors": errors,
        "server_thread_alive_after_shutdown": thread.is_alive(),
        "thread_count_before": baseline_threads,
        "thread_count_after": final_threads,
        "thread_delta": thread_delta,
        "fd_count_before": baseline_fds,
        "fd_count_after": final_fds,
        "fd_delta": fd_delta,
        "tracemalloc_current_start_bytes": memory_start,
        "tracemalloc_current_end_bytes": memory_end,
        "tracemalloc_current_delta_bytes": memory_end - memory_start,
        "tracemalloc_peak_bytes": memory_peak,
        "memory_growth_classification": "OBSERVATIONAL_BASELINE_R1",
        "pid": os.getpid(),
    }
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(text, encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
