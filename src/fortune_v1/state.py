from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, utc_now


DEV_TRANSITIONS = {
    "INGESTED": {"NORMALIZED"},
    "NORMALIZED": {"ANSWER_ISOLATED"},
    "ANSWER_ISOLATED": {"INPUT_VALIDATED"},
    "INPUT_VALIDATED": {"BASELINE_PREDICTED", "GROUP_HOLD"},
    "BASELINE_PREDICTED": {"PREDICTION_FROZEN"},
    "PREDICTION_FROZEN": {"GRADED"},
    "GRADED": {"DIAGNOSED", "CASE_FAIL"},
    "DIAGNOSED": {"PATCH_CANDIDATE_CREATED", "DEV_PASS", "CASE_FAIL", "GROUP_HOLD"},
    "PATCH_CANDIDATE_CREATED": {"RETESTING", "GROUP_HOLD"},
    "RETESTING": {"DEV_PASS", "CASE_FAIL", "GROUP_HOLD", "PATCH_CANDIDATE_CREATED"},
    "DEV_PASS": set(), "CASE_FAIL": set(), "GROUP_HOLD": set(),
}

FROZEN_TRANSITIONS = {
    "FROZEN_BLOCK_OPEN": {"RUNNING"},
    "RUNNING": {"CLOSED_PENDING_EVALUATION"},
    "CLOSED_PENDING_EVALUATION": {"EVALUATED_CLOSED"},
    "EVALUATED_CLOSED": set(),
}

RELEASE_TRANSITIONS = {
    "CANDIDATE": {"DEV_PASS"},
    "DEV_PASS": {"REGRESSION_PASS"},
    "REGRESSION_PASS": {"FROZEN_EVAL_PASS"},
    "FROZEN_EVAL_PASS": {"RELEASED"},
    "RELEASED": set(),
}

MACHINES = {"DEV": DEV_TRANSITIONS, "FROZEN_EVAL": FROZEN_TRANSITIONS, "RELEASE": RELEASE_TRANSITIONS}


@dataclass(frozen=True)
class StateEvent:
    sequence: int
    machine: str
    object_id: str
    from_state: str | None
    to_state: str
    at: str
    evidence: dict[str, Any]


def transition(log_path: str | Path, machine: str, object_id: str, to_state: str,
               evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    if machine not in MACHINES:
        raise FortuneError(f"unknown state machine: {machine}", status="UNKNOWN_STATE_MACHINE")
    path = Path(log_path)
    log = read_json(path) if path.exists() else {"schema": "STATE-LOG-V1", "events": []}
    relevant = [e for e in log["events"] if e["machine"] == machine and e["object_id"] == object_id]
    current = relevant[-1]["to_state"] if relevant else None
    states = MACHINES[machine]
    if current is None:
        initial = next(iter(states))
        if to_state != initial:
            raise FortuneError(f"initial state must be {initial}", status="INVALID_STATE_TRANSITION")
    elif to_state not in states[current]:
        raise FortuneError(f"invalid transition {current} -> {to_state}", status="INVALID_STATE_TRANSITION")
    event = StateEvent(
        sequence=len(log["events"]) + 1,
        machine=machine,
        object_id=object_id,
        from_state=current,
        to_state=to_state,
        at=utc_now(),
        evidence=evidence or {},
    )
    log["events"].append(event.__dict__)
    atomic_write_json(path, log, overwrite=True)
    return event.__dict__

