from __future__ import annotations

from typing import Any

from .integrity import validate_resolution_effect_envelope as _validate_base_envelope
from .models import (
    ResolutionEffectDispositionHashBundle,
    ResolutionEffectDispositionIntegrityDiagnostic,
    ResolutionEffectDispositionIntegrityReport,
)
from .profile import ClassicalResolutionEffectDispositionProfile


def expected_lineage_binding_keys(
    source_final_envelope: Any,
    profile: ClassicalResolutionEffectDispositionProfile,
) -> tuple[str, ...]:
    return (
        *source_final_envelope.lineage_binding_keys,
        f"SOURCE_FINAL_EFFECT_FACT:{source_final_envelope.hashes.fact_hash}",
        f"SOURCE_FINAL_EFFECT_COMPUTATION:{source_final_envelope.hashes.computation_hash}",
        f"RESOLUTION_EFFECT_DISPOSITION_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )


def validate_resolution_effect_envelope(
    source_final_envelope: Any,
    fragment_projections: tuple[Any, ...],
    source_record_candidate_sets: tuple[Any, ...],
    effect_channel_index: tuple[Any, ...],
    source_occurrence_index: tuple[Any, ...],
    local_closure_index: tuple[Any, ...],
    projected_candidate_projection_ids: tuple[str, ...],
    projected_resolution_effect_disposition_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ClassicalResolutionEffectDispositionProfile,
    hashes: ResolutionEffectDispositionHashBundle,
) -> ResolutionEffectDispositionIntegrityReport:
    base = _validate_base_envelope(
        source_final_envelope,
        fragment_projections,
        source_record_candidate_sets,
        effect_channel_index,
        source_occurrence_index,
        local_closure_index,
        projected_candidate_projection_ids,
        projected_resolution_effect_disposition_ids,
        lineage_binding_keys,
        profile,
        hashes,
    )
    diagnostics = list(base.diagnostics)
    expected_lineage = expected_lineage_binding_keys(source_final_envelope, profile)
    if lineage_binding_keys != expected_lineage:
        diagnostics.append(
            ResolutionEffectDispositionIntegrityDiagnostic(
                "UNIT8_LINEAGE_BINDING_REPLAY_MISMATCH",
                "lineage_binding_keys",
                "Unit 8 lineage keys differ from exact Unit 7 hashes and frozen Unit 8 profile replay",
            )
        )
    return ResolutionEffectDispositionIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
