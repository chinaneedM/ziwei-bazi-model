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
    build_expected_source_record_candidate_sets,
    expected_fragment_projection,
    replay_unit7_resolution,
    reversal_reappearance_effect_hash_bundle,
)
from .models import (
    BaziClassicalReversalReappearanceEffectDispositionResolution,
    ClassicalReversalReappearanceEffectDispositionEnvelope,
)
from .profile import ClassicalReversalReappearanceEffectDispositionProfile
from .strict_integrity import (
    expected_lineage_binding_keys,
    validate_reversal_reappearance_effect_envelope,
)


class BaziClassicalReversalReappearanceEffectDispositionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziClassicalReversalReappearanceEffectDispositionRequest:
    source_effect_constraint_resolution: BaziClassicalEffectConstraintGraphResolution
    source_resolver_admission_resolution: BaziClassicalResolverAdmissionResolution
    source_semantic_candidate_resolution: BaziClassicalEffectSemanticCandidateProjectionResolution
    source_mechanism_closure_resolution: BaziClassicalSemanticMechanismClosureGovernanceResolution
    source_allocation_resolution: BaziClassicalNonSelectingParticipantAllocationResolution
    source_final_effect_resolution: BaziClassicalFinalEffectCandidateEnvelopeResolution
    reversal_reappearance_effect_profile: ClassicalReversalReappearanceEffectDispositionProfile


def _project_envelope(
    source_final_envelope: Any,
    profile: ClassicalReversalReappearanceEffectDispositionProfile,
) -> ClassicalReversalReappearanceEffectDispositionEnvelope:
    fragment_projections = tuple(
        expected_fragment_projection(fragment, profile)
        for fragment in source_final_envelope.fragment_envelopes
    )
    source_sets = build_expected_source_record_candidate_sets(
        source_final_envelope,
        fragment_projections,
    )
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
        for disposition_id in row.reversal_reappearance_effect_disposition_ids
    )
    lineage = expected_lineage_binding_keys(source_final_envelope, profile)
    hashes = reversal_reappearance_effect_hash_bundle(
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
    integrity = validate_reversal_reappearance_effect_envelope(
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
        raise BaziClassicalReversalReappearanceEffectDispositionError(
            "REVERSAL_REAPPEARANCE_EFFECT_DISPOSITION_INTEGRITY_FAILED",
            ";".join(f"{row.code}:{row.path}" for row in integrity.diagnostics),
        )
    envelope_id = (
        "CLASSICAL_REVERSAL_REAPPEARANCE_EFFECT_DISPOSITION_ENVELOPE:"
        + object_sha256({
            "source_final_effect_envelope_id": source_final_envelope.final_effect_envelope_id,
            "source_final_effect_fact_hash": source_final_envelope.hashes.fact_hash,
            "fact_hash": hashes.fact_hash,
        })
    )
    return ClassicalReversalReappearanceEffectDispositionEnvelope(
        reversal_reappearance_effect_envelope_id=envelope_id,
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
        projected_reversal_reappearance_effect_disposition_ids=disposition_ids,
        disposition_semantic_scope=profile.disposition_semantic_scope,
        source_asserted_disposition=profile.source_asserted_disposition,
        source_assertion_subtype_split=profile.source_assertion_subtype_split,
        candidate_global_truth_semantics=profile.candidate_global_truth_semantics,
        global_target_relation_restored_state_semantics=(
            profile.global_target_relation_restored_state_semantics
        ),
        global_target_relation_active_in_force_state_semantics=(
            profile.global_target_relation_active_in_force_state_semantics
        ),
        prior_resolution_execution_semantics=(
            profile.prior_resolution_execution_semantics
        ),
        prior_resolution_failure_execution_semantics=(
            profile.prior_resolution_failure_execution_semantics
        ),
        interaction_chain_execution_semantics=(
            profile.interaction_chain_execution_semantics
        ),
        global_operability_semantics=profile.global_operability_semantics,
        candidate_applicability_semantics=profile.candidate_applicability_semantics,
        execution_readiness_semantics=profile.execution_readiness_semantics,
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
        algorithm_versions={
            "reversal_reappearance_effect_disposition": profile.algorithm_version
        },
        integrity=integrity,
        hashes=hashes,
    )


class BaziClassicalReversalReappearanceEffectDispositionEngine:
    schema = "BAZI-CLASSICAL-REVERSAL-REAPPEARANCE-EFFECT-DISPOSITION-RESULT-R1"
    typed_schema = (
        "BAZI-CLASSICAL-REVERSAL-REAPPEARANCE-EFFECT-DISPOSITION-TYPED-RESOLUTION-R1"
    )

    def resolve_typed(
        self,
        request: BaziClassicalReversalReappearanceEffectDispositionRequest,
    ) -> BaziClassicalReversalReappearanceEffectDispositionResolution:
        try:
            profile = request.reversal_reappearance_effect_profile.validate()
            for status, code in (
                (request.source_effect_constraint_resolution.status, "UPSTREAM_EFFECT_RESOLUTION_NOT_RESOLVED"),
                (request.source_resolver_admission_resolution.status, "UPSTREAM_ADMISSION_RESOLUTION_NOT_RESOLVED"),
                (request.source_semantic_candidate_resolution.status, "UPSTREAM_SEMANTIC_RESOLUTION_NOT_RESOLVED"),
                (request.source_mechanism_closure_resolution.status, "UPSTREAM_MECHANISM_RESOLUTION_NOT_RESOLVED"),
                (request.source_allocation_resolution.status, "UPSTREAM_ALLOCATION_RESOLUTION_NOT_RESOLVED"),
                (request.source_final_effect_resolution.status, "UPSTREAM_FINAL_EFFECT_RESOLUTION_NOT_RESOLVED"),
            ):
                if status not in {"RESOLVED", "MULTI_CANDIDATE"}:
                    raise BaziClassicalReversalReappearanceEffectDispositionError(code, status)
            if not replay_unit7_resolution(
                request.source_effect_constraint_resolution,
                request.source_resolver_admission_resolution,
                request.source_semantic_candidate_resolution,
                request.source_mechanism_closure_resolution,
                request.source_allocation_resolution,
                request.source_final_effect_resolution,
            ):
                raise BaziClassicalReversalReappearanceEffectDispositionError(
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
                    raise BaziClassicalReversalReappearanceEffectDispositionError(
                        "UPSTREAM_UNIT7_OUTER_LINEAGE_PROJECTED_MORE_THAN_ONCE",
                        f"{lineage[0]}:{lineage[1]}",
                    )
                seen_lineages.add(lineage)
                rows.append(_project_envelope(source_final_envelope, profile))
            candidates = tuple(rows)
            return BaziClassicalReversalReappearanceEffectDispositionResolution(
                schema=self.typed_schema,
                status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
                candidates=candidates,
                events=("AMBIGUOUS_UPSTREAM_LINEAGES_PRESERVED",)
                if len(candidates) > 1
                else (),
                diagnostics=(),
            )
        except (
            BaziClassicalReversalReappearanceEffectDispositionError,
            KeyError,
            ValueError,
        ) as exc:
            code = getattr(
                exc,
                "diagnostic_code",
                "CLASSICAL_REVERSAL_REAPPEARANCE_EFFECT_DISPOSITION_FAILED",
            )
            return BaziClassicalReversalReappearanceEffectDispositionResolution(
                self.typed_schema,
                "FAILED",
                (),
                (),
                (f"{code}:{exc}",),
            )

    def resolve(
        self,
        request: BaziClassicalReversalReappearanceEffectDispositionRequest,
    ) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "reversal_reappearance_effect_profile": json_value(
                request.reversal_reappearance_effect_profile
            ),
            "candidates": json_value(typed.candidates),
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }
