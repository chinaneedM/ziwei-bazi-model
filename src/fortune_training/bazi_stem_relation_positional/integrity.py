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
    NATAL_PILLAR,
    TEMPORAL_FRAME,
    _snapshot_fact_payload,
    build_stem_relation_positional_context,
)
from .models import (
    BaziStemRelationPositionalContext,
    PositionalHashBundle,
    PositionalIntegrityDiagnostic,
    PositionalIntegrityReport,
)
from .profile import ResolvedBaziStemRelationPositionalProfile


INTEGRITY_ALGORITHM_ID = "BAZI-STEM-RELATION-POSITIONAL-INTEGRITY-V1"
INTEGRITY_ALGORITHM_VERSION = "1.0.0"
HASH_ALGORITHM_ID = "BAZI-STEM-RELATION-POSITIONAL-HASH-V1"
HASH_ALGORITHM_VERSION = "1.0.0"

PROHIBITED_SEMANTIC_FIELDS = {
    "near", "far", "blocked", "unblocked", "intervened", "engaged",
    "not_engaged", "pairing_success", "pairing_failure", "first_claim",
    "priority", "competes", "winner", "loser", "wins", "loses",
    "transformed", "not_transformed", "activated", "suppressed",
    "cancelled", "released", "strength", "root_grade", "prediction",
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
        "stem": row.stem,
        "element": row.element,
        "polarity": row.polarity,
        "participant_layer": row.participant_layer,
        "source_frame_id": row.source_frame_id,
        "raw_position_token": row.raw_position_token,
        "position_domain": row.position_domain,
        "natal_pillar_ordinal": row.natal_pillar_ordinal,
        "is_natal_day_master_participant": row.is_natal_day_master_participant,
        "source_upstream_fact_hash": row.source_upstream_fact_hash,
        "source_incidence_reference_ids": list(row.source_incidence_reference_ids),
    }


def _pair_fact(row) -> dict[str, Any]:
    return {
        "positional_fact_id": row.positional_fact_id,
        "source_relation_reference_id": row.source_relation_reference_id,
        "source_relation_id": row.source_relation_id,
        "source_semantic_relation_id": row.source_semantic_relation_id,
        "source_relation_type": row.source_relation_type,
        "source_relation_family": row.source_relation_family,
        "participant_instance_ids": list(row.participant_instance_ids),
        "participant_position_reference_ids": list(row.participant_position_reference_ids),
        "position_domain_pair": list(row.position_domain_pair),
        "natal_linear_order_comparable": row.natal_linear_order_comparable,
        "natal_pillar_ordinals": list(row.natal_pillar_ordinals),
        "natal_ordinal_distance": row.natal_ordinal_distance,
        "intervening_natal_visible_stem_instance_ids": list(
            row.intervening_natal_visible_stem_instance_ids
        ),
        "contains_natal_day_master_participant": row.contains_natal_day_master_participant,
        "natal_day_master_participant_instance_ids": list(
            row.natal_day_master_participant_instance_ids
        ),
        "source_incidence_snapshot_id": row.source_incidence_snapshot_id,
        "source_incidence_snapshot_fact_hash": row.source_incidence_snapshot_fact_hash,
        "source_incidence_fact_hash": row.source_incidence_fact_hash,
    }


def stem_relation_positional_fact_projection(
    context: BaziStemRelationPositionalContext,
) -> dict[str, Any]:
    return {
        "snapshot": _snapshot_fact(context.snapshot),
        "participant_position_references": [
            _participant_fact(row) for row in context.participant_position_references
        ],
        "stem_pair_positional_facts": [
            _pair_fact(row) for row in context.stem_pair_positional_facts
        ],
    }


def stem_relation_positional_hash_bundle(
    context: BaziStemRelationPositionalContext,
    incidence: BaziRelationIncidenceCandidate,
    source_incidence_candidate_indices: tuple[int, ...],
    source_flow_candidate_indices: tuple[int, ...],
    source_structural_candidate_indices: tuple[int, ...],
    source_support_candidate_indices: tuple[int, ...],
    source_temporal_candidate_indices: tuple[int, ...],
    source_temporal_seed_ids: tuple[str, ...],
    source_incidence_lineage_binding_keys: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ResolvedBaziStemRelationPositionalProfile,
) -> PositionalHashBundle:
    fact_hash = object_sha256(stem_relation_positional_fact_projection(context))
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
        "source_incidence_lineage_binding_keys": list(
            source_incidence_lineage_binding_keys
        ),
        "lineage_binding_keys": list(lineage_binding_keys),
        "resolved_positional_profile": json_value(profile),
        "algorithm_versions": dict(sorted(context.algorithm_versions.items())),
        "rule_and_source_lineage": [
            {
                "rule_set_id": context.snapshot.rule_set_id,
                "rule_set_version": context.snapshot.rule_set_version,
                "source_refs": sorted(context.snapshot.source_refs),
            },
            *(
                {
                    "rule_set_id": row.rule_set_id,
                    "rule_set_version": row.rule_set_version,
                    "source_refs": sorted(row.source_refs),
                }
                for row in context.participant_position_references
            ),
            *(
                {
                    "rule_set_id": row.rule_set_id,
                    "rule_set_version": row.rule_set_version,
                    "source_refs": sorted(row.source_refs),
                }
                for row in context.stem_pair_positional_facts
            ),
        ],
        "hash_algorithm": f"{HASH_ALGORITHM_ID}@{HASH_ALGORITHM_VERSION}",
    })
    return PositionalHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=HASH_ALGORITHM_ID,
        algorithm_version=HASH_ALGORITHM_VERSION,
    )


def validate_stem_relation_positional_context(
    context: BaziStemRelationPositionalContext,
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
    profile: ResolvedBaziStemRelationPositionalProfile,
    hashes: PositionalHashBundle | None = None,
    request_incidence_candidates: tuple[BaziRelationIncidenceCandidate, ...] = (),
) -> PositionalIntegrityReport:
    diagnostics: list[PositionalIntegrityDiagnostic] = []
    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "PROFILE_INVALID", "profile", str(exc))

    if incidence.integrity.status != "PASS" or structural.integrity.status != "PASS":
        _diag(
            diagnostics,
            "UPSTREAM_INTEGRITY_FAILED",
            "snapshot",
            "Structural/Incidence integrity must pass",
        )
    snapshot = context.snapshot
    source_snapshot = incidence.context.snapshot
    expected_upstream = {
        "source_incidence_snapshot_id": source_snapshot.snapshot_id,
        "source_incidence_snapshot_fact_hash": source_snapshot.snapshot_fact_hash,
        "source_incidence_fact_hash": incidence.hashes.fact_hash,
        "source_incidence_computation_hash": incidence.hashes.computation_hash,
        "source_natal_fact_hash": natal.hashes.fact_hash,
        "source_natal_computation_hash": natal.hashes.computation_hash,
        "source_temporal_fact_hash": source_snapshot.upstream_temporal_fact_hash,
        "source_flow_fact_hash": source_snapshot.upstream_flow_fact_hash,
        "source_flow_computation_hash": source_snapshot.upstream_flow_computation_hash,
        "source_structural_fact_hash": structural.hashes.fact_hash,
        "source_structural_computation_hash": structural.hashes.computation_hash,
        "source_support_fact_hash": source_snapshot.upstream_support_fact_hash,
        "source_support_computation_hash": source_snapshot.upstream_support_computation_hash,
    }
    for name, expected in expected_upstream.items():
        if getattr(snapshot, name) != expected:
            _diag(
                diagnostics,
                "UPSTREAM_HASH_BINDING_MISMATCH",
                f"snapshot.{name}",
                str(getattr(snapshot, name)),
            )
    if snapshot.target_utc != source_snapshot.target_utc:
        _diag(diagnostics, "TARGET_REPLAY_MISMATCH", "snapshot.target_utc", str(snapshot.target_utc))
    expected_snapshot_hash = object_sha256(
        _snapshot_fact_payload(natal, structural, incidence)
    )
    if (
        snapshot.snapshot_fact_hash != expected_snapshot_hash
        or snapshot.snapshot_id
        != f"STEM_RELATION_POSITIONAL_SNAPSHOT:{expected_snapshot_hash}"
    ):
        _diag(
            diagnostics,
            "SNAPSHOT_IDENTITY_REPLAY_MISMATCH",
            "snapshot",
            snapshot.snapshot_id,
        )

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
        _diag(
            diagnostics,
            "LINEAGE_BINDING_KEYS_REPLAY_MISMATCH",
            "lineage_binding_keys",
            "complete incidence lineage must be retained",
        )
    if (
        not source_incidence_candidate_indices
        or tuple(sorted(set(source_incidence_candidate_indices)))
        != source_incidence_candidate_indices
    ):
        _diag(
            diagnostics,
            "INCIDENCE_CANDIDATE_INDEX_INVALID",
            "source_incidence_candidate_indices",
            str(source_incidence_candidate_indices),
        )
    if request_incidence_candidates:
        for index in source_incidence_candidate_indices:
            if index >= len(request_incidence_candidates) or request_incidence_candidates[index] != incidence:
                _diag(
                    diagnostics,
                    "INCIDENCE_CANDIDATE_MULTIPLICITY_REPLAY_MISMATCH",
                    f"source_incidence_candidate_indices[{index}]",
                    "complete upstream candidate does not replay",
                )

    try:
        expected_context = build_stem_relation_positional_context(
            natal, structural, incidence, profile
        )
    except (ValueError, KeyError) as exc:
        _diag(diagnostics, "POSITIONAL_REPLAY_FAILED", "context", str(exc))
        expected_context = None
    if expected_context is not None:
        expected_refs = {
            row.participant_instance_id: row
            for row in expected_context.participant_position_references
        }
        actual_refs = {
            row.participant_instance_id: row
            for row in context.participant_position_references
        }
        if set(expected_refs) != set(actual_refs):
            _diag(
                diagnostics,
                "PARTICIPANT_POSITION_COVERAGE_MISMATCH",
                "participant_position_references",
                "exact in-scope participant/reference pairs required",
            )
        for key in sorted(set(expected_refs) & set(actual_refs)):
            expected = expected_refs[key]
            actual = actual_refs[key]
            if actual.raw_position_token != expected.raw_position_token:
                _diag(diagnostics, "PARTICIPANT_POSITION_REPLAY_MISMATCH", str(key), actual.raw_position_token)
            if (
                actual.position_domain != expected.position_domain
                or actual.natal_pillar_ordinal != expected.natal_pillar_ordinal
            ):
                _diag(diagnostics, "NATAL_ORDINAL_REPLAY_MISMATCH", str(key), str(actual.natal_pillar_ordinal))
            if actual.is_natal_day_master_participant != expected.is_natal_day_master_participant:
                _diag(diagnostics, "DAY_MASTER_IDENTITY_REPLAY_MISMATCH", str(key), str(actual.is_natal_day_master_participant))
            if actual != expected:
                _diag(diagnostics, "PARTICIPANT_REFERENCE_REPLAY_MISMATCH", str(key), actual.reference_id)

        expected_pairs = {
            row.source_relation_reference_id: row
            for row in expected_context.stem_pair_positional_facts
        }
        actual_pairs = {
            row.source_relation_reference_id: row
            for row in context.stem_pair_positional_facts
        }
        if set(expected_pairs) != set(actual_pairs):
            _diag(
                diagnostics,
                "SOURCE_RELATION_REPLAY_MISMATCH",
                "stem_pair_positional_facts",
                "exact in-scope incidence relation references required",
            )
        for key in sorted(set(expected_pairs) & set(actual_pairs)):
            expected = expected_pairs[key]
            actual = actual_pairs[key]
            source_fields = (
                actual.source_relation_id,
                actual.source_semantic_relation_id,
                actual.source_relation_type,
                actual.source_relation_family,
                actual.participant_instance_ids,
                actual.participant_position_reference_ids,
            )
            expected_source_fields = (
                expected.source_relation_id,
                expected.source_semantic_relation_id,
                expected.source_relation_type,
                expected.source_relation_family,
                expected.participant_instance_ids,
                expected.participant_position_reference_ids,
            )
            if source_fields != expected_source_fields:
                _diag(diagnostics, "SOURCE_RELATION_REPLAY_MISMATCH", key, actual.source_relation_id)
            ordinal_fields = (
                actual.position_domain_pair,
                actual.natal_linear_order_comparable,
                actual.natal_pillar_ordinals,
                actual.natal_ordinal_distance,
            )
            expected_ordinal_fields = (
                expected.position_domain_pair,
                expected.natal_linear_order_comparable,
                expected.natal_pillar_ordinals,
                expected.natal_ordinal_distance,
            )
            if ordinal_fields != expected_ordinal_fields:
                _diag(diagnostics, "NATAL_ORDINAL_REPLAY_MISMATCH", key, str(ordinal_fields))
            if (
                actual.intervening_natal_visible_stem_instance_ids
                != expected.intervening_natal_visible_stem_instance_ids
            ):
                _diag(diagnostics, "INTERVENER_MEMBERSHIP_OR_ORDER_REPLAY_MISMATCH", key, str(actual.intervening_natal_visible_stem_instance_ids))
            day_master_fields = (
                actual.contains_natal_day_master_participant,
                actual.natal_day_master_participant_instance_ids,
            )
            expected_day_master_fields = (
                expected.contains_natal_day_master_participant,
                expected.natal_day_master_participant_instance_ids,
            )
            if day_master_fields != expected_day_master_fields:
                _diag(diagnostics, "DAY_MASTER_IDENTITY_REPLAY_MISMATCH", key, str(day_master_fields))
            if actual != expected:
                _diag(diagnostics, "PAIR_POSITIONAL_FACT_REPLAY_MISMATCH", key, actual.positional_fact_id)

        if context.snapshot != expected_context.snapshot:
            _diag(diagnostics, "SNAPSHOT_REPLAY_MISMATCH", "snapshot", snapshot.snapshot_id)
        if context.algorithm_versions != expected_context.algorithm_versions:
            _diag(diagnostics, "POSITIONAL_ALGORITHM_VERSION_MISMATCH", "algorithm_versions", str(context.algorithm_versions))

    for row in context.participant_position_references:
        if row.position_domain == TEMPORAL_FRAME and row.natal_pillar_ordinal is not None:
            _diag(diagnostics, "TEMPORAL_NATAL_ORDINAL_FABRICATED", row.reference_id, str(row.natal_pillar_ordinal))
        if row.position_domain == NATAL_PILLAR and row.natal_pillar_ordinal is None:
            _diag(diagnostics, "NATAL_ORDINAL_MISSING", row.reference_id, row.raw_position_token)
    for row in context.stem_pair_positional_facts:
        if not row.natal_linear_order_comparable and (
            row.natal_pillar_ordinals
            or row.natal_ordinal_distance is not None
            or row.intervening_natal_visible_stem_instance_ids
        ):
            _diag(diagnostics, "TEMPORAL_NATAL_DISTANCE_FABRICATED", row.positional_fact_id, row.source_relation_id)

    if source_snapshot.active_dayun_kind == "PRE_DAYUN" and any(
        row.raw_position_token == "DAYUN"
        for row in context.participant_position_references
    ):
        _diag(diagnostics, "PRE_DAYUN_FAKE_STEM_POSITION", "participant_position_references", "PRE_DAYUN cannot produce DAYUN.STEM")

    for collection_name, collection in (
        ("participant_position_references", context.participant_position_references),
        ("stem_pair_positional_facts", context.stem_pair_positional_facts),
    ):
        for index, row in enumerate(collection):
            present = {field.name.lower() for field in fields(row)}
            prohibited = present & PROHIBITED_SEMANTIC_FIELDS
            if prohibited:
                _diag(diagnostics, "CLASSICAL_SEMANTIC_FIELD_PRESENT", f"{collection_name}[{index}]", ",".join(sorted(prohibited)))

    if hashes is not None:
        expected_hashes = stem_relation_positional_hash_bundle(
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
