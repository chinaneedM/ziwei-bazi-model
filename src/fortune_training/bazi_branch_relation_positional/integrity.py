from __future__ import annotations

from dataclasses import fields
from datetime import timezone
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_relation_incidence import BaziRelationIncidenceCandidate
from fortune_training.bazi_structural import BaziStructuralCandidate
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .generation import (
    IN_SCOPE_RELATION_TYPES,
    NATAL_PILLAR,
    TEMPORAL_FRAME,
    build_branch_relation_positional_context,
)
from .models import (
    BaziBranchRelationPositionalContext,
    PositionalHashBundle,
    PositionalIntegrityDiagnostic,
    PositionalIntegrityReport,
)
from .profile import ResolvedBaziBranchRelationPositionalProfile


INTEGRITY_ALGORITHM_ID = "BAZI-BRANCH-RELATION-POSITIONAL-INTEGRITY-V1"
INTEGRITY_ALGORITHM_VERSION = "1.0.0"
HASH_ALGORITHM_ID = "BAZI-BRANCH-RELATION-POSITIONAL-HASH-V1"
HASH_ALGORITHM_VERSION = "1.0.0"

PROHIBITED_SEMANTIC_FIELDS = {
    "near", "far", "adjacent", "remote", "blocked", "blocking",
    "intervening_effect", "engaged", "operable", "precedence", "priority",
    "winner", "loser", "allocation", "activated", "suppressed", "released",
    "strength", "severity", "classical_order", "source_interaction_pattern",
    "classical_assertion_binding", "final_relation_outcome", "prediction",
}


def _diag(rows, code: str, path: str, detail: str) -> None:
    rows.append(PositionalIntegrityDiagnostic(code=code, path=path, detail=detail))


def _instant_fact(value) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("positional fact instant must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _snapshot_fact(row) -> dict[str, Any]:
    return {
        "snapshot_id": row.snapshot_id,
        "snapshot_fact_hash": row.snapshot_fact_hash,
        "source_incidence_snapshot_id": row.source_incidence_snapshot_id,
        "source_incidence_snapshot_fact_hash": row.source_incidence_snapshot_fact_hash,
        "source_incidence_fact_hash": row.source_incidence_fact_hash,
        "source_natal_fact_hash": row.source_natal_fact_hash,
        "source_temporal_fact_hash": row.source_temporal_fact_hash,
        "source_flow_fact_hash": row.source_flow_fact_hash,
        "source_structural_fact_hash": row.source_structural_fact_hash,
        "source_support_fact_hash": row.source_support_fact_hash,
        "target_utc": _instant_fact(row.target_utc),
        "profile_id": row.profile_id,
        "profile_version": row.profile_version,
    }


def _participant_fact(row) -> dict[str, Any]:
    return {
        "reference_id": row.reference_id,
        "participant_instance_id": row.participant_instance_id,
        "branch": row.branch,
        "element_affiliation": row.element_affiliation,
        "participant_layer": row.participant_layer,
        "source_frame_id": row.source_frame_id,
        "raw_position_token": row.raw_position_token,
        "position_domain": row.position_domain,
        "natal_pillar_ordinal": row.natal_pillar_ordinal,
        "source_upstream_fact_hash": row.source_upstream_fact_hash,
        "source_incidence_reference_ids": list(row.source_incidence_reference_ids),
    }


def _relation_fact(row) -> dict[str, Any]:
    return {
        "positional_fact_id": row.positional_fact_id,
        "source_relation_reference_id": row.source_relation_reference_id,
        "source_relation_id": row.source_relation_id,
        "source_semantic_relation_id": row.source_semantic_relation_id,
        "source_relation_type": row.source_relation_type,
        "source_relation_family": row.source_relation_family,
        "participant_instance_ids": list(row.participant_instance_ids),
        "participant_position_reference_ids": list(row.participant_position_reference_ids),
        "raw_position_tokens": list(row.raw_position_tokens),
        "position_domains": list(row.position_domains),
        "participant_layers": list(row.participant_layers),
        "source_frame_ids": list(row.source_frame_ids),
        "source_orientation": row.source_orientation,
        "source_arity": row.source_arity,
        "all_participants_natal_pillar": row.all_participants_natal_pillar,
        "natal_pillar_ordinals": list(row.natal_pillar_ordinals),
        "source_occurrence_kind": row.source_occurrence_kind,
        "source_occurrence_upstream_fact_hash": row.source_occurrence_upstream_fact_hash,
        "source_relation_rule_set_id": row.source_relation_rule_set_id,
        "source_relation_rule_set_version": row.source_relation_rule_set_version,
        "source_incidence_snapshot_id": row.source_incidence_snapshot_id,
        "source_incidence_snapshot_fact_hash": row.source_incidence_snapshot_fact_hash,
        "source_incidence_fact_hash": row.source_incidence_fact_hash,
    }


def branch_relation_positional_fact_projection(
    context: BaziBranchRelationPositionalContext,
) -> dict[str, Any]:
    return {
        "snapshot": _snapshot_fact(context.snapshot),
        "participant_position_references": [
            _participant_fact(row) for row in context.participant_position_references
        ],
        "branch_relation_positional_facts": [
            _relation_fact(row) for row in context.branch_relation_positional_facts
        ],
    }


def branch_relation_positional_hash_bundle(
    context: BaziBranchRelationPositionalContext,
    incidence: BaziRelationIncidenceCandidate,
    source_incidence_candidate_indices: tuple[int, ...],
    source_flow_candidate_indices: tuple[int, ...],
    source_structural_candidate_indices: tuple[int, ...],
    source_support_candidate_indices: tuple[int, ...],
    source_temporal_candidate_indices: tuple[int, ...],
    source_temporal_seed_ids: tuple[str, ...],
    source_incidence_lineage_binding_keys: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ResolvedBaziBranchRelationPositionalProfile,
) -> PositionalHashBundle:
    fact_hash = object_sha256(branch_relation_positional_fact_projection(context))
    snapshot = context.snapshot
    computation_hash = object_sha256({
        "fact_hash": fact_hash,
        "upstream_computation_hashes": {
            "natal": snapshot.source_natal_computation_hash,
            "flow": snapshot.source_flow_computation_hash,
            "structural": snapshot.source_structural_computation_hash,
            "support": snapshot.source_support_computation_hash,
            "incidence": incidence.hashes.computation_hash,
        },
        "source_candidate_indices": {
            "incidence": sorted(source_incidence_candidate_indices),
            "flow": sorted(source_flow_candidate_indices),
            "structural": sorted(source_structural_candidate_indices),
            "support": sorted(source_support_candidate_indices),
            "temporal": sorted(source_temporal_candidate_indices),
        },
        "source_temporal_seed_ids": sorted(source_temporal_seed_ids),
        "source_incidence_lineage_binding_keys": list(source_incidence_lineage_binding_keys),
        "lineage_binding_keys": list(lineage_binding_keys),
        "resolved_positional_profile": json_value(profile),
        "algorithm_versions": dict(sorted(context.algorithm_versions.items())),
        "rule_and_source_lineage": [
            {
                "rule_set_id": row.rule_set_id,
                "rule_set_version": row.rule_set_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in (
                context.snapshot,
                *context.participant_position_references,
                *context.branch_relation_positional_facts,
            )
        ],
        "hash_algorithm": f"{HASH_ALGORITHM_ID}@{HASH_ALGORITHM_VERSION}",
    })
    return PositionalHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=HASH_ALGORITHM_ID,
        algorithm_version=HASH_ALGORITHM_VERSION,
    )


def validate_branch_relation_positional_context(
    context: BaziBranchRelationPositionalContext,
    natal: BaziChartCandidate,
    structural: BaziStructuralCandidate,
    incidence: BaziRelationIncidenceCandidate,
    source_incidence_candidate_indices: tuple[int, ...],
    source_flow_candidate_indices: tuple[int, ...],
    source_structural_candidate_indices: tuple[int, ...],
    source_support_candidate_indices: tuple[int, ...],
    source_temporal_candidate_indices: tuple[int, ...],
    source_temporal_seed_ids: tuple[str, ...],
    source_incidence_lineage_binding_keys: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ResolvedBaziBranchRelationPositionalProfile,
    hashes: PositionalHashBundle | None = None,
    request_incidence_candidates: tuple[BaziRelationIncidenceCandidate, ...] = (),
) -> PositionalIntegrityReport:
    diagnostics: list[PositionalIntegrityDiagnostic] = []
    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "PROFILE_INVALID", "profile", str(exc))
    if incidence.integrity.status != "PASS" or structural.integrity.status != "PASS":
        _diag(diagnostics, "UPSTREAM_INTEGRITY_FAILED", "snapshot", "Structural/Incidence integrity must pass")

    lineage_checks = (
        ("source_flow_candidate_indices", source_flow_candidate_indices, incidence.source_flow_candidate_indices),
        ("source_structural_candidate_indices", source_structural_candidate_indices, incidence.source_structural_candidate_indices),
        ("source_support_candidate_indices", source_support_candidate_indices, incidence.source_support_candidate_indices),
        ("source_temporal_candidate_indices", source_temporal_candidate_indices, incidence.source_temporal_candidate_indices),
        ("source_temporal_seed_ids", source_temporal_seed_ids, incidence.source_temporal_seed_ids),
        ("source_incidence_lineage_binding_keys", source_incidence_lineage_binding_keys, incidence.lineage_binding_keys),
    )
    for path, actual, expected in lineage_checks:
        if tuple(actual) != tuple(expected):
            _diag(diagnostics, "LINEAGE_REPLAY_MISMATCH", path, str(actual))
    expected_binding_keys = (
        f"INCIDENCE_FACT:{incidence.hashes.fact_hash}",
        f"INCIDENCE_COMPUTATION:{incidence.hashes.computation_hash}",
        *(f"INCIDENCE_CANDIDATE_INDEX:{index}" for index in source_incidence_candidate_indices),
        *incidence.lineage_binding_keys,
    )
    if lineage_binding_keys != expected_binding_keys:
        _diag(diagnostics, "LINEAGE_BINDING_KEYS_REPLAY_MISMATCH", "lineage_binding_keys", "complete incidence lineage must be retained")
    if not source_incidence_candidate_indices or tuple(sorted(set(source_incidence_candidate_indices))) != source_incidence_candidate_indices:
        _diag(diagnostics, "INCIDENCE_CANDIDATE_INDEX_INVALID", "source_incidence_candidate_indices", str(source_incidence_candidate_indices))
    if request_incidence_candidates:
        for index in source_incidence_candidate_indices:
            if index >= len(request_incidence_candidates) or request_incidence_candidates[index] != incidence:
                _diag(diagnostics, "INCIDENCE_CANDIDATE_MULTIPLICITY_REPLAY_MISMATCH", f"source_incidence_candidate_indices[{index}]", "complete upstream candidate does not replay")

    try:
        expected = build_branch_relation_positional_context(natal, structural, incidence, profile)
    except (ValueError, KeyError) as exc:
        _diag(diagnostics, "POSITIONAL_REPLAY_FAILED", "context", str(exc))
        expected = None
    if expected is not None:
        if context.snapshot != expected.snapshot:
            _diag(diagnostics, "SNAPSHOT_REPLAY_MISMATCH", "snapshot", context.snapshot.snapshot_id)
        expected_refs = {row.participant_instance_id: row for row in expected.participant_position_references}
        actual_refs = {row.participant_instance_id: row for row in context.participant_position_references}
        if len(actual_refs) != len(context.participant_position_references) or set(actual_refs) != set(expected_refs):
            _diag(diagnostics, "PARTICIPANT_POSITION_COVERAGE_MISMATCH", "participant_position_references", "exact participant occurrence identities required")
        for participant_id in sorted(set(actual_refs) & set(expected_refs)):
            actual = actual_refs[participant_id]
            target = expected_refs[participant_id]
            if (actual.raw_position_token, actual.participant_layer, actual.source_frame_id) != (target.raw_position_token, target.participant_layer, target.source_frame_id):
                _diag(diagnostics, "PARTICIPANT_POSITION_REPLAY_MISMATCH", participant_id, actual.raw_position_token)
            if (actual.position_domain, actual.natal_pillar_ordinal) != (target.position_domain, target.natal_pillar_ordinal):
                _diag(diagnostics, "NATAL_ORDINAL_REPLAY_MISMATCH", participant_id, str(actual.natal_pillar_ordinal))
            if actual != target:
                _diag(diagnostics, "PARTICIPANT_REFERENCE_REPLAY_MISMATCH", participant_id, actual.reference_id)

        expected_facts = {row.source_relation_reference_id: row for row in expected.branch_relation_positional_facts}
        actual_facts = {row.source_relation_reference_id: row for row in context.branch_relation_positional_facts}
        if len(actual_facts) != len(context.branch_relation_positional_facts) or set(actual_facts) != set(expected_facts):
            _diag(diagnostics, "SOURCE_RELATION_REPLAY_MISMATCH", "branch_relation_positional_facts", "one-to-one in-scope Incidence replay required")
        for reference_id in sorted(set(actual_facts) & set(expected_facts)):
            actual = actual_facts[reference_id]
            target = expected_facts[reference_id]
            if actual.participant_instance_ids != target.participant_instance_ids or actual.source_orientation != target.source_orientation or actual.source_arity != target.source_arity:
                _diag(diagnostics, "ORDER_ARITY_ORIENTATION_REPLAY_MISMATCH", reference_id, actual.source_relation_id)
            if (actual.raw_position_tokens, actual.position_domains, actual.participant_layers, actual.source_frame_ids, actual.natal_pillar_ordinals) != (target.raw_position_tokens, target.position_domains, target.participant_layers, target.source_frame_ids, target.natal_pillar_ordinals):
                _diag(diagnostics, "POSITION_TUPLE_REPLAY_MISMATCH", reference_id, actual.source_relation_id)
            if actual != target:
                _diag(diagnostics, "RELATION_POSITIONAL_FACT_REPLAY_MISMATCH", reference_id, actual.positional_fact_id)
        if context.algorithm_versions != expected.algorithm_versions:
            _diag(diagnostics, "POSITIONAL_ALGORITHM_VERSION_MISMATCH", "algorithm_versions", str(context.algorithm_versions))

    source_types = {
        row.relation_type for row in incidence.context.relation_occurrences
        if row.relation_type in IN_SCOPE_RELATION_TYPES
    }
    actual_types = {row.source_relation_type for row in context.branch_relation_positional_facts}
    if actual_types != source_types:
        _diag(diagnostics, "RELEASED_RELATION_TYPE_COVERAGE_MISMATCH", "branch_relation_positional_facts", str(actual_types))
    for row in context.participant_position_references:
        if row.position_domain == TEMPORAL_FRAME and row.natal_pillar_ordinal is not None:
            _diag(diagnostics, "TEMPORAL_NATAL_ORDINAL_FABRICATED", row.reference_id, str(row.natal_pillar_ordinal))
        if row.position_domain == NATAL_PILLAR and row.natal_pillar_ordinal is None:
            _diag(diagnostics, "NATAL_ORDINAL_MISSING", row.reference_id, row.raw_position_token)
    for row in context.branch_relation_positional_facts:
        if not row.all_participants_natal_pillar and row.natal_pillar_ordinals:
            _diag(diagnostics, "CROSS_DOMAIN_NATAL_ORDINAL_FABRICATED", row.positional_fact_id, row.source_relation_id)
        if row.source_arity != len(row.participant_instance_ids) or len(row.participant_position_reference_ids) != row.source_arity:
            _diag(diagnostics, "VARIABLE_ARITY_ALIGNMENT_MISMATCH", row.positional_fact_id, row.source_relation_id)
        if row.source_relation_type == "BRANCH_CHUAN" and ("HARM" in row.source_semantic_relation_id or row.source_relation_family != "BRANCH_CHUAN"):
            _diag(diagnostics, "CHUAN_HARM_SEMANTIC_LEAKAGE", row.positional_fact_id, row.source_semantic_relation_id)

    for collection_name, collection in (
        ("participant_position_references", context.participant_position_references),
        ("branch_relation_positional_facts", context.branch_relation_positional_facts),
    ):
        for index, row in enumerate(collection):
            present = {field.name.lower() for field in fields(row)}
            prohibited = present & PROHIBITED_SEMANTIC_FIELDS
            if prohibited:
                _diag(diagnostics, "CLASSICAL_SEMANTIC_FIELD_PRESENT", f"{collection_name}[{index}]", ",".join(sorted(prohibited)))

    if hashes is not None:
        expected_hashes = branch_relation_positional_hash_bundle(
            context,
            incidence,
            source_incidence_candidate_indices,
            source_flow_candidate_indices,
            source_structural_candidate_indices,
            source_support_candidate_indices,
            source_temporal_candidate_indices,
            source_temporal_seed_ids,
            source_incidence_lineage_binding_keys,
            lineage_binding_keys,
            profile,
        )
        if hashes != expected_hashes:
            _diag(diagnostics, "POSITIONAL_HASH_REPLAY_MISMATCH", "hashes", hashes.fact_hash)

    return PositionalIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=INTEGRITY_ALGORITHM_ID,
        algorithm_version=INTEGRITY_ALGORITHM_VERSION,
    )
