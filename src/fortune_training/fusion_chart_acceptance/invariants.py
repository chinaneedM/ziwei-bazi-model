from __future__ import annotations

from typing import Any

from fortune_training.calendar_foundation.models import json_value
from fortune_training.combined_chart_application import (
    combined_manifest_hash,
    validate_combined_resolution,
)
from fortune_training.util import object_sha256


def _sha256_like(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value.lower())
    )


def deterministic_resolution_signature(resolution: Any) -> str:
    return object_sha256(json_value(resolution))


def combined_invariant_violations(resolution: Any) -> tuple[str, ...]:
    """Check product-level invariants without re-deriving canonical astrology rules."""

    diagnostics: list[str] = []

    replay = validate_combined_resolution(resolution)
    if replay.status != "PASS":
        diagnostics.extend(f"COMBINED_REPLAY:{row}" for row in replay.diagnostics)
    if resolution.integrity != replay:
        diagnostics.append("COMBINED_EMBEDDED_INTEGRITY_MISMATCH")
    if not _sha256_like(resolution.manifest_hash):
        diagnostics.append("COMBINED_MANIFEST_HASH_SHAPE")
    elif resolution.manifest_hash != combined_manifest_hash(resolution):
        diagnostics.append("COMBINED_MANIFEST_HASH_REPLAY")
    if not resolution.shared_time_credential:
        diagnostics.append("SHARED_TIME_CREDENTIAL_EMPTY")
    if not resolution.candidate_lineage:
        diagnostics.append("CANDIDATE_LINEAGE_EMPTY")

    ziwei = resolution.ziwei_bundle
    if ziwei is not None:
        if not _sha256_like(ziwei.bundle_hash):
            diagnostics.append("ZIWEI_BUNDLE_HASH_SHAPE")
        structure = ziwei.candidate.chart.structure
        designations = structure.designation_bindings
        if len(designations) != 12:
            diagnostics.append(f"ZIWEI_DESIGNATION_COUNT:{len(designations)}")
        designation_indexes = {row.address.index for row in designations}
        if designation_indexes != set(range(12)):
            diagnostics.append("ZIWEI_DESIGNATION_ADDRESS_COVERAGE")
        if not ziwei.candidate.chart.placements:
            diagnostics.append("ZIWEI_PLACEMENTS_EMPTY")
        daxian = ziwei.temporal_state.daxian_frames
        if not daxian:
            diagnostics.append("ZIWEI_DAXIAN_EMPTY")
        elif len({row.frame_id for row in daxian}) != len(daxian):
            diagnostics.append("ZIWEI_DAXIAN_FRAME_ID_DUPLICATE")
        minor = ziwei.temporal_state.minor_limit_frames
        if not minor:
            diagnostics.append("ZIWEI_MINOR_LIMIT_EMPTY")
        elif len({row.nominal_age for row in minor}) != len(minor):
            diagnostics.append("ZIWEI_MINOR_LIMIT_AGE_DUPLICATE")

    bazi = resolution.bazi_bundle
    if bazi is not None:
        if not _sha256_like(bazi.source_fact_hash):
            diagnostics.append("BAZI_SOURCE_FACT_HASH_SHAPE")
        if not _sha256_like(bazi.view_hash):
            diagnostics.append("BAZI_VIEW_HASH_SHAPE")
        if not _sha256_like(bazi.bundle_hash):
            diagnostics.append("BAZI_BUNDLE_HASH_SHAPE")
        if not bazi.candidates:
            diagnostics.append("BAZI_CANDIDATES_EMPTY")
        for index, candidate in enumerate(bazi.candidates):
            if not _sha256_like(candidate.natal_fact_hash):
                diagnostics.append(f"BAZI_NATAL_FACT_HASH_SHAPE:{index}")
            if not _sha256_like(candidate.temporal_fact_hash):
                diagnostics.append(f"BAZI_TEMPORAL_FACT_HASH_SHAPE:{index}")
            if not _sha256_like(candidate.view_hash):
                diagnostics.append(f"BAZI_CANDIDATE_VIEW_HASH_SHAPE:{index}")
            pillars = candidate.view.get("pillars", ())
            if len(pillars) != 4:
                diagnostics.append(f"BAZI_PILLAR_COUNT:{index}:{len(pillars)}")
            positions = [str(row.get("position", "")) for row in pillars]
            if len(set(positions)) != len(positions):
                diagnostics.append(f"BAZI_PILLAR_POSITION_DUPLICATE:{index}")
            for pindex, row in enumerate(pillars):
                ganzhi = row.get("ganzhi")
                if not isinstance(ganzhi, str) or len(ganzhi) != 2:
                    diagnostics.append(
                        f"BAZI_PILLAR_GANZHI_SHAPE:{index}:{pindex}:{ganzhi}"
                    )

    present = int(ziwei is not None) + int(bazi is not None)
    if present == 2 and resolution.status not in {"RESOLVED_BOTH", "UNCERTAINTY_PRESENT"}:
        diagnostics.append(f"COMBINED_STATUS_WITH_BOTH:{resolution.status}")
    if present == 1 and resolution.status != "PARTIAL":
        diagnostics.append(f"COMBINED_STATUS_WITH_ONE:{resolution.status}")
    if present == 0 and resolution.status != "FAILED":
        diagnostics.append(f"COMBINED_STATUS_WITH_NONE:{resolution.status}")

    return tuple(diagnostics)


def require_combined_invariants(resolution: Any) -> None:
    diagnostics = combined_invariant_violations(resolution)
    if diagnostics:
        raise AssertionError(";".join(diagnostics))
