#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from fortune_training.fusion_chart_acceptance.random_replay import (
    DEFAULT_SEED,
    run_random_replay,
)


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


def _write(path: Path | None, payload: dict[str, object]) -> None:
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if path is None:
        print(text, end="")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic random replay/property-invariant acceptance runner"
    )
    parser.add_argument("--repository-root", type=Path, default=_root())
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--escalate-to", type=int, default=0)
    parser.add_argument("--max-projected-seconds", type=float, default=3600.0)
    args = parser.parse_args()

    first = run_random_replay(
        args.repository_root.resolve(),
        samples=args.samples,
        seed=args.seed,
        start_index=args.start_index,
    )
    payload: dict[str, object] = {
        "schema": "FUSION-CHART-DETERMINISTIC-REPLAY-ACCEPTANCE-R1",
        "status": first["status"],
        "base_run": first,
        "escalation": {
            "requested_samples": args.escalate_to,
            "decision": "NOT_REQUESTED",
            "projected_seconds": first["projected_100000_seconds"],
            "max_projected_seconds": args.max_projected_seconds,
        },
    }
    if (
        args.start_index == 0
        and args.escalate_to > args.samples
        and first["status"] == "PASS"
        and first["elapsed_seconds"] > 0
    ):
        projected = first["elapsed_seconds"] * (
            float(args.escalate_to) / float(args.samples)
        )
        payload["escalation"] = {
            "requested_samples": args.escalate_to,
            "decision": (
                "RUN"
                if projected <= args.max_projected_seconds
                else "NOT_ESCALATED_PERFORMANCE_GATE"
            ),
            "projected_seconds": projected,
            "max_projected_seconds": args.max_projected_seconds,
        }
        if projected <= args.max_projected_seconds:
            escalated = run_random_replay(
                args.repository_root.resolve(),
                samples=args.escalate_to,
                seed=args.seed,
            )
            payload["escalated_run"] = escalated
            if escalated["status"] != "PASS":
                payload["status"] = "FAIL"

    _write(args.receipt, payload)
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
