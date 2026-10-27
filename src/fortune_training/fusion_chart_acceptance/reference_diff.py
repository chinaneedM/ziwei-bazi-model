from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .taxonomy import DefectClass


@dataclass(frozen=True)
class ReferenceDifference:
    path: str
    local_value: Any
    reference_value: Any
    classification: DefectClass
    note: str


def _flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, Mapping):
        rows: dict[str, Any] = {}
        for key in sorted(value):
            path = f"{prefix}.{key}" if prefix else str(key)
            rows.update(_flatten(value[key], path))
        return rows
    if isinstance(value, (list, tuple)):
        rows = {}
        for index, item in enumerate(value):
            path = f"{prefix}[{index}]"
            rows.update(_flatten(item, path))
        if not value:
            rows[prefix] = []
        return rows
    return {prefix: value}


def compare_reference_snapshot(
    local: Mapping[str, Any],
    reference: Mapping[str, Any],
    *,
    disputed_paths: tuple[str, ...] = (),
    expected_profile_paths: tuple[str, ...] = (),
) -> tuple[ReferenceDifference, ...]:
    """Compare a reference implementation without treating it as authority.

    A mismatch is REFERENCE_DIFFERENCE by default. Explicitly documented
    profile paths and disputed candidates receive their own classifications.
    This helper intentionally has no path that emits IMPLEMENTATION_DEFECT.
    """

    left = _flatten(local)
    right = _flatten(reference)
    differences: list[ReferenceDifference] = []
    for path in sorted(set(left) | set(right)):
        local_value = left.get(path, "<MISSING>")
        reference_value = right.get(path, "<MISSING>")
        if local_value == reference_value:
            continue
        if path in disputed_paths:
            classification = DefectClass.DISPUTED_CANDIDATE
            note = "documented disputed method/candidate; no winner is selected"
        elif path in expected_profile_paths:
            classification = DefectClass.EXPECTED_PROFILE_DIFFERENCE
            note = "documented profile/default difference"
        else:
            classification = DefectClass.REFERENCE_DIFFERENCE
            note = "reference implementation differs; canonical evidence review required"
        differences.append(
            ReferenceDifference(
                path=path,
                local_value=local_value,
                reference_value=reference_value,
                classification=classification,
                note=note,
            )
        )
    return tuple(differences)
