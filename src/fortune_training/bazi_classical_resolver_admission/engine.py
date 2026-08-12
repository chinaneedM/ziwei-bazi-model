from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fortune_training.bazi_chart_bound_classical_interaction_projection.models import (
    BaziChartBoundClassicalInteractionProjectionResolution,
)
from fortune_training.bazi_chart_source_pattern_binding.models import (
    BaziChartSourcePatternBindingResolution,
)
from fortune_training.bazi_classical_effect_constraint_graph.models import (
    BaziClassicalEffectConstraintGraphResolution,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .dependency import (
    NeutralDependencyMaterializationError,
    dependency_blocker_ids,
    normalize_neutral_dependency_materialization,
)
from .integrity import (
    admission_hash_bundle,
    match_projection_outer,
    replay_effect_envelope,
    validate_admission_envelope,
)
from .models import (
    BaziClassicalResolverAdmissionResolution,
    ClassicalFragmentResolverAdmissionProjection,
    ClassicalResolverAdmissionEnvelopeCandidate,
    SourceRecordResolverAdmissionCandidateSet,
)
from .profile import (
    ClassicalInteractionResolverAdmissionProfile,
    ClassicalSourceSemanticProfile,
)


class BaziClassicalResolverAdmissionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziClassicalResolverAdmissionRequest:
    source_binding_resolution: BaziChartSourcePatternBindingResolution
    source_projection_resolution: BaziChartBoundClassicalInteractionProjectionResolution
    source_effect_constraint_resolution: BaziClassicalEffectConstraintGraphResolution
    source_semantic_profile: ClassicalSourceSemanticProfile
    admission_profile: ClassicalInteractionResolverAdmissionProfile


def _unique_strings(rows: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(rows))


def _unresolved_classical_requirements(fragment: Any) -> tuple[str, ...]:
    return _unique_strings([
        requirement
        for node in fragment.effect_constraint_nodes
        for requirement in node.constraint.unresolved_classical_semantic_requirements
    ])


def _bundle_by_binding(source_projection_outer: Any) -> dict[str, Any]:
    rows = {row.binding_candidate_id: row for row in source_projection_outer.bundles}
    if len(rows) != len(source_projection_outer.bundles):
        raise BaziClassicalResolverAdmissionError(
            "SOURCE_PROJECTION_BINDING_ID_DUPLICATE", str(len(source_projection_outer.bundles))
        )
    return rows


def project_fragment_admission(
    source_effect_envelope: Any,
    fragment: Any,
    source_projection_bundle: Any,
    source_profile: ClassicalSourceSemanticProfile,
    admission_profile: ClassicalInteractionResolverAdmissionProfile,
) -> ClassicalFragmentResolverAdmissionProjection:
    if fragment.binding_candidate_id != source_projection_bundle.binding_candidate_id:
        raise BaziClassicalResolverAdmissionError(
            "FRAGMENT_PROJECTION_BUNDLE_BINDING_MISMATCH", fragment.binding_candidate_id
        )
    if fragment.source_occurrence_id != source_projection_bundle.source_occurrence_id:
        raise BaziClassicalResolverAdmissionError(
            "FRAGMENT_PROJECTION_BUNDLE_SOURCE_OCCURRENCE_MISMATCH", fragment.fragment_id
        )
    if fragment.structural_binding_class != source_projection_bundle.structural_binding_class:
        raise BaziClassicalResolverAdmissionError(
            "FRAGMENT_STRUCTURAL_BINDING_CLASS_REPLAY_MISMATCH", fragment.fragment_id
        )
    if (
        fragment.source_scope_compatibility
        != source_projection_bundle.source_scope_compatibility.source_scope_compatibility
    ):
        raise BaziClassicalResolverAdmissionError(
            "FRAGMENT_SOURCE_SCOPE_COMPATIBILITY_REPLAY_MISMATCH", fragment.fragment_id
        )
    if (
        fragment.residual_unresolved_structural_constraint_ids
        != source_projection_bundle.residual_unresolved_structural_constraint_ids
    ):
        raise BaziClassicalResolverAdmissionError(
            "FRAGMENT_RESIDUAL_STRUCTURAL_CONTEXT_REPLAY_MISMATCH", fragment.fragment_id
        )
    if (
        fragment.source_unresolved_graph_requirements
        != source_projection_bundle.source_unresolved_graph_requirements
    ):
        raise BaziClassicalResolverAdmissionError(
            "FRAGMENT_SOURCE_GRAPH_PROVENANCE_REPLAY_MISMATCH", fragment.fragment_id
        )

    materialization = normalize_neutral_dependency_materialization(
        source_projection_bundle.neutral_observation_bundle
    )
    partition_match = (
        fragment.source_layer == source_profile.source_layer
        and fragment.source_occurrence_id in source_profile.member_source_occurrence_ids
    )
    blockers: list[str] = []
    if not partition_match:
        blockers.append("SOURCE_SEMANTIC_PARTITION_MISMATCH")
        admission_status = "PRESERVED_OUTSIDE_PROFILE"
    else:
        if fragment.structural_binding_class == "PARTIAL_EXACT_BINDING_ENUMERATION":
            blockers.append("STRUCTURAL_BINDING_PARTIAL")
        elif fragment.structural_binding_class not in admission_profile.allowed_structural_binding_classes:
            raise BaziClassicalResolverAdmissionError(
                "UNRELEASED_STRUCTURAL_BINDING_CLASS", fragment.structural_binding_class
            )
        for constraint_id in fragment.residual_unresolved_structural_constraint_ids:
            blockers.append(f"RESIDUAL_STRUCTURAL_CONSTRAINT:{constraint_id}")
        if fragment.source_scope_compatibility == "CROSS_LAYER_EXTENSION_UNRESOLVED":
            blockers.append("CROSS_LAYER_EXTENSION_UNRESOLVED")
        elif fragment.source_scope_compatibility not in admission_profile.allowed_scope_compatibility_classes:
            raise BaziClassicalResolverAdmissionError(
                "UNRELEASED_SOURCE_SCOPE_COMPATIBILITY", fragment.source_scope_compatibility
            )
        blockers.extend(dependency_blocker_ids(materialization))
        admission_status = "ADMITTED" if not blockers else "PRESERVED_NOT_ADMITTED"

    unresolved_requirements = _unresolved_classical_requirements(fragment)
    projection_id = "CLASSICAL_RESOLVER_ADMISSION:" + object_sha256({
        "source_envelope_id": source_effect_envelope.envelope_id,
        "source_fragment_id": fragment.fragment_id,
        "source_semantic_partition_id": source_profile.partition_id,
        "neutral_observation_bundle_id": source_projection_bundle.neutral_observation_bundle.observation_bundle_id,
        "admission_blocker_ids": tuple(blockers),
        "admission_status": admission_status,
    })
    return ClassicalFragmentResolverAdmissionProjection(
        admission_projection_id=projection_id,
        source_envelope_id=source_effect_envelope.envelope_id,
        source_envelope_fact_hash=source_effect_envelope.hashes.fact_hash,
        source_envelope_computation_hash=source_effect_envelope.hashes.computation_hash,
        source_fragment_id=fragment.fragment_id,
        source_fragment_fact_hash=fragment.hashes.fact_hash,
        source_fragment_computation_hash=fragment.hashes.computation_hash,
        binding_candidate_id=fragment.binding_candidate_id,
        source_occurrence_id=fragment.source_occurrence_id,
        source_layer=fragment.source_layer,
        source_semantic_profile_id=source_profile.profile_id,
        source_semantic_partition_id=source_profile.partition_id,
        partition_match=partition_match,
        structural_binding_class=fragment.structural_binding_class,
        source_scope_compatibility=fragment.source_scope_compatibility,
        residual_unresolved_structural_constraint_ids=fragment.residual_unresolved_structural_constraint_ids,
        neutral_observation_bundle_id=source_projection_bundle.neutral_observation_bundle.observation_bundle_id,
        required_neutral_primitives=source_projection_bundle.neutral_observation_bundle.required_neutral_primitives,
        dependency_materialization_evidence=materialization,
        unresolved_classical_semantic_requirements=unresolved_requirements,
        source_unresolved_graph_requirements_provenance=fragment.source_unresolved_graph_requirements,
        admission_blocker_ids=tuple(blockers),
        admission_status=admission_status,
    )


def _record_sets(source_effect_envelope: Any, fragment_admissions: tuple[Any, ...]) -> tuple[SourceRecordResolverAdmissionCandidateSet, ...]:
    admission_by_fragment = {row.source_fragment_id: row for row in fragment_admissions}
    if len(admission_by_fragment) != len(fragment_admissions):
        raise BaziClassicalResolverAdmissionError(
            "DUPLICATE_SOURCE_FRAGMENT_ADMISSION", str(len(fragment_admissions))
        )
    rows: list[SourceRecordResolverAdmissionCandidateSet] = []
    for partition in source_effect_envelope.source_layer_partitions:
        for source_set in partition.source_record_candidate_sets:
            if (
                source_set.member_selection_semantics != "NOT_RELEASED"
                or source_set.member_coexistence_semantics != "NOT_RELEASED"
                or source_set.member_exclusivity_semantics != "NOT_RELEASED"
            ):
                raise BaziClassicalResolverAdmissionError(
                    "UPSTREAM_SOURCE_RECORD_SET_SEMANTICS_OVERRESOLVED",
                    source_set.source_record_candidate_set_id,
                )
            rows.append(SourceRecordResolverAdmissionCandidateSet(
                source_record_candidate_set_id=source_set.source_record_candidate_set_id,
                source_layer=source_set.source_layer,
                source_occurrence_id=source_set.source_occurrence_id,
                source_fragment_ids=source_set.fragment_ids,
                admission_projection_ids=tuple(
                    admission_by_fragment[fragment_id].admission_projection_id
                    for fragment_id in source_set.fragment_ids
                ),
            ))
    return tuple(rows)


def _project_envelope(
    source_effect_envelope: Any,
    source_projection_outer: Any,
    request: BaziClassicalResolverAdmissionRequest,
) -> ClassicalResolverAdmissionEnvelopeCandidate:
    if not replay_effect_envelope(
        source_effect_envelope,
        source_projection_outer,
        request.source_binding_resolution,
    ):
        raise BaziClassicalResolverAdmissionError(
            "UPSTREAM_EFFECT_ENVELOPE_REPLAY_MISMATCH", source_effect_envelope.envelope_id
        )
    bundle_by_binding = _bundle_by_binding(source_projection_outer)
    fragment_admissions = tuple(
        project_fragment_admission(
            source_effect_envelope,
            fragment,
            bundle_by_binding[fragment.binding_candidate_id],
            request.source_semantic_profile,
            request.admission_profile,
        )
        for fragment in source_effect_envelope.fragments
    )
    record_sets = _record_sets(source_effect_envelope, fragment_admissions)
    admitted = tuple(row.source_fragment_id for row in fragment_admissions if row.admission_status == "ADMITTED")
    preserved = tuple(row.source_fragment_id for row in fragment_admissions if row.admission_status == "PRESERVED_NOT_ADMITTED")
    outside = tuple(row.source_fragment_id for row in fragment_admissions if row.admission_status == "PRESERVED_OUTSIDE_PROFILE")
    lineage_binding_keys = (
        *source_effect_envelope.lineage_binding_keys,
        f"SOURCE_EFFECT_FACT:{source_effect_envelope.hashes.fact_hash}",
        f"SOURCE_EFFECT_COMPUTATION:{source_effect_envelope.hashes.computation_hash}",
        f"SOURCE_SEMANTIC_PROFILE:{request.source_semantic_profile.profile_id}:{request.source_semantic_profile.profile_version}",
        f"RESOLVER_ADMISSION_PROFILE:{request.admission_profile.profile_id}:{request.admission_profile.profile_version}",
    )
    hashes = admission_hash_bundle(
        source_effect_envelope,
        fragment_admissions,
        record_sets,
        admitted,
        preserved,
        outside,
        lineage_binding_keys,
        request.source_semantic_profile,
        request.admission_profile,
    )
    integrity = validate_admission_envelope(
        source_effect_envelope,
        source_projection_outer,
        request.source_binding_resolution,
        fragment_admissions,
        record_sets,
        admitted,
        preserved,
        outside,
        lineage_binding_keys,
        request.source_semantic_profile,
        request.admission_profile,
        hashes,
    )
    if integrity.status != "PASS":
        raise BaziClassicalResolverAdmissionError(
            "RESOLVER_ADMISSION_INTEGRITY_FAILED",
            ";".join(f"{row.code}:{row.path}" for row in integrity.diagnostics),
        )
    admission_envelope_id = "CLASSICAL_RESOLVER_ADMISSION_ENVELOPE:" + object_sha256({
        "source_effect_envelope_id": source_effect_envelope.envelope_id,
        "source_effect_fact_hash": source_effect_envelope.hashes.fact_hash,
        "admission_fact_hash": hashes.fact_hash,
    })
    return ClassicalResolverAdmissionEnvelopeCandidate(
        admission_envelope_id=admission_envelope_id,
        source_effect_envelope_id=source_effect_envelope.envelope_id,
        source_effect_fact_hash=source_effect_envelope.hashes.fact_hash,
        source_effect_computation_hash=source_effect_envelope.hashes.computation_hash,
        source_projection_fact_hash=source_effect_envelope.source_projection_fact_hash,
        source_projection_computation_hash=source_effect_envelope.source_projection_computation_hash,
        source_binding_fact_hash=source_effect_envelope.source_binding_fact_hash,
        source_binding_computation_hash=source_effect_envelope.source_binding_computation_hash,
        lineage_binding_keys=lineage_binding_keys,
        fragment_admissions=fragment_admissions,
        source_record_candidate_sets=record_sets,
        admitted_fragment_ids=admitted,
        preserved_not_admitted_fragment_ids=preserved,
        preserved_outside_profile_fragment_ids=outside,
        fragment_selection_semantics="NOT_RELEASED",
        cross_outer_composition="NOT_RELEASED",
        cartesian_expansion="NOT_RELEASED",
        raw_relation_immutability_contract=request.admission_profile.raw_relation_immutability_contract,
        transition_separation_contract=request.admission_profile.transition_separation_contract,
        algorithm_versions={"admission": request.admission_profile.algorithm_version},
        integrity=integrity,
        hashes=hashes,
    )


class BaziClassicalResolverAdmissionEngine:
    schema = "BAZI-CLASSICAL-RESOLVER-ADMISSION-RESULT-R1"
    typed_schema = "BAZI-CLASSICAL-RESOLVER-ADMISSION-TYPED-RESOLUTION-R1"

    def resolve_typed(
        self,
        request: BaziClassicalResolverAdmissionRequest,
    ) -> BaziClassicalResolverAdmissionResolution:
        try:
            request.source_semantic_profile.validate()
            request.admission_profile.validate()
            if request.source_binding_resolution.status not in {"RESOLVED", "MULTI_CANDIDATE"}:
                raise BaziClassicalResolverAdmissionError(
                    "UPSTREAM_BINDING_NOT_RESOLVED", request.source_binding_resolution.status
                )
            if request.source_projection_resolution.status not in {"RESOLVED", "MULTI_CANDIDATE"}:
                raise BaziClassicalResolverAdmissionError(
                    "UPSTREAM_PROJECTION_NOT_RESOLVED", request.source_projection_resolution.status
                )
            if request.source_effect_constraint_resolution.status not in {"RESOLVED", "MULTI_CANDIDATE"}:
                raise BaziClassicalResolverAdmissionError(
                    "UPSTREAM_EFFECT_CONSTRAINT_NOT_RESOLVED", request.source_effect_constraint_resolution.status
                )
            rows = []
            seen_effect_lineages: set[tuple[str, str]] = set()
            for source_effect_envelope in request.source_effect_constraint_resolution.candidates:
                lineage = (
                    source_effect_envelope.hashes.fact_hash,
                    source_effect_envelope.hashes.computation_hash,
                )
                if lineage in seen_effect_lineages:
                    raise BaziClassicalResolverAdmissionError(
                        "UPSTREAM_EFFECT_OUTER_LINEAGE_PROJECTED_MORE_THAN_ONCE",
                        f"{lineage[0]}:{lineage[1]}",
                    )
                seen_effect_lineages.add(lineage)
                source_projection_outer = match_projection_outer(
                    source_effect_envelope, request.source_projection_resolution
                )
                rows.append(_project_envelope(
                    source_effect_envelope, source_projection_outer, request
                ))
            candidates = tuple(rows)
            return BaziClassicalResolverAdmissionResolution(
                schema=self.typed_schema,
                status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
                candidates=candidates,
                events=("AMBIGUOUS_UPSTREAM_LINEAGES_PRESERVED",) if len(candidates) > 1 else (),
                diagnostics=(),
            )
        except (
            BaziClassicalResolverAdmissionError,
            NeutralDependencyMaterializationError,
            KeyError,
            ValueError,
        ) as exc:
            code = getattr(exc, "diagnostic_code", "CLASSICAL_RESOLVER_ADMISSION_FAILED")
            return BaziClassicalResolverAdmissionResolution(
                self.typed_schema, "FAILED", (), (), (f"{code}:{exc}",)
            )

    def resolve(self, request: BaziClassicalResolverAdmissionRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "source_semantic_profile": json_value(request.source_semantic_profile),
            "admission_profile": json_value(request.admission_profile),
            "candidates": json_value(typed.candidates),
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }
