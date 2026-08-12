from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fortune_training.bazi_classical_effect_constraint_graph.models import (
    BaziClassicalEffectConstraintGraphResolution,
)
from fortune_training.bazi_classical_effect_semantic_candidate.models import (
    BaziClassicalEffectSemanticCandidateProjectionResolution,
)
from fortune_training.bazi_classical_final_effect_candidate_envelope.models import (
    BaziClassicalFinalEffectCandidateEnvelopeResolution,
)
from fortune_training.bazi_classical_non_selecting_participant_allocation.models import (
    BaziClassicalNonSelectingParticipantAllocationResolution,
)
from fortune_training.bazi_classical_resolver_admission.models import (
    BaziClassicalResolverAdmissionResolution,
)
from fortune_training.bazi_classical_semantic_closure_governance.models import (
    BaziClassicalSemanticMechanismClosureGovernanceResolution,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .integrity import (
    build_expected_indexes,
    expected_fragment_projection,
    replay_unit7_resolution,
    resolution_effect_hash_bundle,
    validate_resolution_effect_envelope,
)
from .models import (
    BaziClassicalResolutionEffectDispositionResolution,
    ClassicalResolutionEffectDispositionEnvelope,
    SourceRecordResolutionEffectCandidateSet,
)
from .profile import ClassicalResolutionEffectDispositionProfile


class BaziClassicalResolutionEffectDispositionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziClassicalResolutionEffectDispositionRequest:
    source_effect_constraint_resolution: BaziClassicalEffectConstraintGraphResolution
    source_resolver_admission_resolution: BaziClassicalResolverAdmissionResolution
    source_semantic_candidate_resolution: BaziClassicalEffectSemanticCandidateProjectionResolution
    source_mechanism_closure_resolution: BaziClassicalSemanticMechanismClosureGovernanceResolution
    source_allocation_resolution: BaziClassicalNonSelectingParticipantAllocationResolution
    source_final_effect_resolution: BaziClassicalFinalEffectCandidateEnvelopeResolution
    resolution_effect_profile: ClassicalResolutionEffectDispositionProfile


def _source_record_sets(
    source_final_envelope: Any,
    fragment_projections: tuple[Any, ...],
) -> tuple[SourceRecordResolutionEffectCandidateSet, ...]:
    by_source_fragment = {
        row.source_final_fragment_id: row for row in fragment_projections
    }
    if len(by_source_fragment) != len(fragment_projections):
        raise BaziClassicalResolutionEffectDispositionError(
            "DUPLICATE_UNIT8_SOURCE_FINAL_FRAGMENT_ID",
            str(len(fragment_projections)),
        )
    rows = []
    for source_set in source_final_envelope.source_record_candidate_sets:
        selected = tuple(
            by_source_fragment[fragment_id]
            for fragment_id in source_set.final_fragment_ids
        )
        candidate_projection_ids = tuple(
            candidate_id
            for fragment in selected
            for candidate_id in fragment.candidate_projection_ids
        )
        disposition_ids = tuple(
            disposition_id
            for fragment in selected
            for disposition_id in fragment.resolution_effect_disposition_ids
        )
        set_id = "CLASSICAL_RESOLUTION_EFFECT_SOURCE_RECORD_SET:" + object_sha256({
            "source_final_candidate_set_id": source_set.source_record_candidate_set_id,
            "source_final_fragment_ids": source_set.final_fragment_ids,
            "fragment_projection_ids": tuple(
                row.fragment_projection_id for row in selected
            ),
            "candidate_projection_ids": candidate_projection_ids,
            "resolution_effect_disposition_ids": disposition_ids,
        })
        rows.append(SourceRecordResolutionEffectCandidateSet(
            source_record_candidate_set_id=set_id,
            source_final_candidate_set_id=source_set.source_record_candidate_set_id,
            source_layer=source_set.source_layer,
            source_occurrence_id=source_set.source_occurrence_id,
            source_final_fragment_ids=source_set.final_fragment_ids,
            fragment_projection_ids=tuple(row.fragment_projection_id for row in selected),
            candidate_projection_ids=candidate_projection_ids,
            resolution_effect_disposition_ids=disposition_ids,
        ))
    return tuple(rows)


def _project_envelope(
    source_final_envelope: Any,
    profile: ClassicalResolutionEffectDispositionProfile,
) -> ClassicalResolutionEffectDispositionEnvelope:
    fragment_projections = tuple(
        expected_fragment_projection(fragment, profile)
        for fragment in source_final_envelope.fragment_envelopes
    )
    source_sets = _source_record_sets(source_final_envelope, fragment_projections)
    candidate_projections = tuple(
        candidate
        for fragment in fragment_projections
        for candidate in fragment.candidate_projections
    )
    effect_index, occurrence_index, closure_index = build_expected_indexes(
        candidate_projections
    )
    projection_ids = tuple(row.candidate_projection_id for row in candidate_projections)
    disposition_ids = tuple(
        disposition_id
        for row in candidate_projections
        for disposition_id in row.resolution_effect_disposition_ids
    )
    lineage = (
        *source_final_envelope.lineage_binding_keys,
        f"SOURCE_FINAL_EFFECT_FACT:{source_final_envelope.hashes.fact_hash}",
        f"SOURCE_FINAL_EFFECT_COMPUTATION:{source_final_envelope.hashes.computation_hash}",
        f"RESOLUTION_EFFECT_DISPOSITION_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )
    hashes = resolution_effect_hash_bundle(
        source_final_envelope,
        fragment_projections,
        source_sets,
        effect_index,
        occurrence_index,
        closure_index,
        projection_ids,
        disposition_ids,
        lineage,
        profile,
    )
    integrity = validate_resolution_effect_envelope(
        source_final_envelope,
        fragment_projections,
        source_sets,
        effect_index,
        occurrence_index,
        closure_index,
        projection_ids,
        disposition_ids,
        lineage,
        profile,
        hashes,
    )
    if integrity.status != "PASS":
        raise BaziClassicalResolutionEffectDispositionError(
            "RESOLUTION_EFFECT_DISPOSITION_INTEGRITY_FAILED",
            ";".join(f"{row.code}:{row.path}" for row in integrity.diagnostics),
        )
    envelope_id = "CLASSICAL_RESOLUTION_EFFECT_DISPOSITION_ENVELOPE:" + object_sha256({
        "source_final_effect_envelope_id": source_final_envelope.final_effect_envelope_id,
        "source_final_effect_fact_hash": source_final_envelope.hashes.fact_hash,
        "fact_hash": hashes.fact_hash,
    })
    return ClassicalResolutionEffectDispositionEnvelope(
        resolution_effect_envelope_id=envelope_id,
        source_final_effect_envelope_id=source_final_envelope.final_effect_envelope_id,
        source_final_effect_fact_hash=source_final_envelope.hashes.fact_hash,
        source_final_effect_computation_hash=source_final_envelope.hashes.computation_hash,
        source_allocation_envelope_id=source_final_envelope.source_allocation_envelope_id,
        source_mechanism_closure_envelope_id=(
            source_final_envelope.source_mechanism_closure_envelope_id
        ),
        source_semantic_projection_envelope_id=(
            source_final_envelope.source_semantic_projection_envelope_id
        ),
        source_admission_envelope_id=source_final_envelope.source_admission_envelope_id,
        source_effect_envelope_id=source_final_envelope.source_effect_envelope_id,
        lineage_binding_keys=lineage,
        fragment_projections=fragment_projections,
        source_record_candidate_sets=source_sets,
        effect_channel_index=effect_index,
        source_occurrence_index=occurrence_index,
        local_closure_index=closure_index,
        projected_candidate_projection_ids=projection_ids,
        projected_resolution_effect_disposition_ids=disposition_ids,
        disposition_semantic_scope=profile.disposition_semantic_scope,
        candidate_global_truth_semantics=profile.candidate_global_truth_semantics,
        global_operability_semantics=profile.global_operability_semantics,
        candidate_selection_semantics=profile.candidate_selection_semantics,
        candidate_coexistence_semantics=profile.candidate_coexistence_semantics,
        candidate_exclusivity_semantics=profile.candidate_exclusivity_semantics,
        candidate_conflict_semantics=profile.candidate_conflict_semantics,
        precedence_semantics=profile.precedence_semantics,
        priority_semantics=profile.priority_semantics,
        winner_loser_semantics=profile.winner_loser_semantics,
        global_relation_effect_state_semantics=(
            profile.global_relation_effect_state_semantics
        ),
        execution_readiness_semantics=profile.execution_readiness_semantics,
        resolution_failure_semantics=profile.resolution_failure_semantics,
        reversal_reappearance_semantics=profile.reversal_reappearance_semantics,
        attenuation_grade_semantics=profile.attenuation_grade_semantics,
        participant_allocation_semantics=profile.participant_allocation_semantics,
        participant_path_selection_semantics=(
            profile.participant_path_selection_semantics
        ),
        inferred_slot_instance_compatibility=(
            profile.inferred_slot_instance_compatibility
        ),
        source_narrative_execution=profile.source_narrative_execution,
        graph_mutation_fixpoint_semantics=profile.graph_mutation_fixpoint_semantics,
        fragment_selection_semantics=profile.fragment_selection_semantics,
        cross_outer_composition=profile.cross_outer_composition,
        cross_source_composition=profile.cross_source_composition,
        cartesian_expansion=profile.cartesian_expansion,
        final_classical_verdict_semantics=profile.final_classical_verdict_semantics,
        raw_relation_immutability_contract=profile.raw_relation_immutability_contract,
        algorithm_versions={"resolution_effect_disposition": profile.algorithm_version},
        integrity=integrity,
        hashes=hashes,
    )


class BaziClassicalResolutionEffectDispositionEngine:
    schema = "BAZI-CLASSICAL-RESOLUTION-EFFECT-DISPOSITION-RESULT-R1"
    typed_schema = "BAZI-CLASSICAL-RESOLUTION-EFFECT-DISPOSITION-TYPED-RESOLUTION-R1"

    def resolve_typed(
        self,
        request: BaziClassicalResolutionEffectDispositionRequest,
    ) -> BaziClassicalResolutionEffectDispositionResolution:
        try:
            profile = request.resolution_effect_profile.validate()
            for status, code in (
                (request.source_effect_constraint_resolution.status, "UPSTREAM_EFFECT_RESOLUTION_NOT_RESOLVED"),
                (request.source_resolver_admission_resolution.status, "UPSTREAM_ADMISSION_RESOLUTION_NOT_RESOLVED"),
                (request.source_semantic_candidate_resolution.status, "UPSTREAM_SEMANTIC_RESOLUTION_NOT_RESOLVED"),
                (request.source_mechanism_closure_resolution.status, "UPSTREAM_MECHANISM_RESOLUTION_NOT_RESOLVED"),
                (request.source_allocation_resolution.status, "UPSTREAM_ALLOCATION_RESOLUTION_NOT_RESOLVED"),
                (request.source_final_effect_resolution.status, "UPSTREAM_FINAL_EFFECT_RESOLUTION_NOT_RESOLVED"),
            ):
                if status not in {"RESOLVED", "MULTI_CANDIDATE"}:
                    raise BaziClassicalResolutionEffectDispositionError(code, status)
            if not replay_unit7_resolution(
                request.source_effect_constraint_resolution,
                request.source_resolver_admission_resolution,
                request.source_semantic_candidate_resolution,
                request.source_mechanism_closure_resolution,
                request.source_allocation_resolution,
                request.source_final_effect_resolution,
            ):
                raise BaziClassicalResolutionEffectDispositionError(
                    "UPSTREAM_UNIT7_FULL_RESOLUTION_REPLAY_MISMATCH",
                    "supplied Unit 7 resolution differs from exact frozen-profile replay",
                )
            rows = []
            seen_lineages: set[tuple[str, str]] = set()
            for source_final_envelope in request.source_final_effect_resolution.candidates:
                lineage = (
                    source_final_envelope.hashes.fact_hash,
                    source_final_envelope.hashes.computation_hash,
                )
                if lineage in seen_lineages:
                    raise BaziClassicalResolutionEffectDispositionError(
                        "UPSTREAM_UNIT7_OUTER_LINEAGE_PROJECTED_MORE_THAN_ONCE",
                        f"{lineage[0]}:{lineage[1]}",
                    )
                seen_lineages.add(lineage)
                rows.append(_project_envelope(source_final_envelope, profile))
            candidates = tuple(rows)
            return BaziClassicalResolutionEffectDispositionResolution(
                schema=self.typed_schema,
                status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
                candidates=candidates,
                events=("AMBIGUOUS_UPSTREAM_LINEAGES_PRESERVED",)
                if len(candidates) > 1
                else (),
                diagnostics=(),
            )
        except (BaziClassicalResolutionEffectDispositionError, KeyError, ValueError) as exc:
            code = getattr(
                exc,
                "diagnostic_code",
                "CLASSICAL_RESOLUTION_EFFECT_DISPOSITION_FAILED",
            )
            return BaziClassicalResolutionEffectDispositionResolution(
                self.typed_schema,
                "FAILED",
                (),
                (),
                (f"{code}:{exc}",),
            )

    def resolve(self, request: BaziClassicalResolutionEffectDispositionRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "resolution_effect_profile": json_value(request.resolution_effect_profile),
            "candidates": json_value(typed.candidates),
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }
