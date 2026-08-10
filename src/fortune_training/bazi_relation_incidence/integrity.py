from __future__ import annotations

from dataclasses import fields
from datetime import timezone
from itertools import combinations
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .generation import (
    DISJOINT,
    SHARED_PARTICIPANT,
    RelationIncidenceSnapshotInputs,
    _participant_map,
    _released_relation_rows,
    _seasonal_roles,
    _snapshot_fact_payload,
    _support_touch_ids,
    build_relation_incidence_context,
)
from .models import (
    BaziRelationIncidenceContext,
    IncidenceHashBundle,
    IncidenceIntegrityDiagnostic,
    IncidenceIntegrityReport,
)
from .profile import ResolvedBaziRelationIncidenceProfile


INTEGRITY_ALGORITHM_ID = "BAZI-RELATION-INCIDENCE-INTEGRITY-V1"
INTEGRITY_ALGORITHM_VERSION = "1.0.0"
HASH_ALGORITHM_ID = "BAZI-RELATION-INCIDENCE-HASH-V1"
HASH_ALGORITHM_VERSION = "1.0.0"

PROHIBITED_EFFECT_FIELDS = {
    "activated",
    "reactivated",
    "suppressed",
    "cancelled",
    "rescued",
    "released",
    "conflicting",
    "competing",
    "interacting",
    "binding",
    "effective",
    "dominant",
    "strength",
    "pressure",
    "weight",
    "priority",
    "winner",
    "loser",
    "transformation_succeeded",
    "transformation_success",
}


def _diag(rows, code: str, path: str, detail: str) -> None:
    rows.append(IncidenceIntegrityDiagnostic(code=code, path=path, detail=detail))


def _instant_fact(value) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("incidence fact instant must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _participant_reference_fact(row) -> dict[str, Any]:
    return {
        "instance_id": row.instance_id,
        "participant_kind": row.participant_kind,
        "value": row.value,
        "participant_layer": row.participant_layer,
        "source_frame_id": row.source_frame_id,
        "source_upstream_fact_hash": row.source_upstream_fact_hash,
        "source_ganzhi": row.source_ganzhi,
    }


def _snapshot_fact(row) -> dict[str, Any]:
    return {
        "snapshot_id": row.snapshot_id,
        "snapshot_fact_hash": row.snapshot_fact_hash,
        "target_utc": _instant_fact(row.target_utc),
        "upstream_natal_fact_hash": row.upstream_natal_fact_hash,
        "upstream_temporal_fact_hash": row.upstream_temporal_fact_hash,
        "source_temporal_candidate_indices": sorted(
            row.source_temporal_candidate_indices
        ),
        "source_temporal_seed_ids": sorted(row.source_temporal_seed_ids),
        "upstream_flow_fact_hash": row.upstream_flow_fact_hash,
        "upstream_structural_fact_hash": row.upstream_structural_fact_hash,
        "upstream_support_fact_hash": row.upstream_support_fact_hash,
        "active_dayun_kind": row.active_dayun_kind,
        "active_dayun_source_frame_id": row.active_dayun_source_frame_id,
        "annual_frame_id": row.annual_frame_id,
        "monthly_frame_id": row.monthly_frame_id,
        "raw_relation_ids": sorted(row.raw_relation_ids),
    }


def _relation_occurrence_fact(row) -> dict[str, Any]:
    return {
        "reference_id": row.reference_id,
        "relation_id": row.relation_id,
        "semantic_relation_id": row.semantic_relation_id,
        "relation_type": row.relation_type,
        "relation_family": row.relation_family,
        "participant_instance_ids": list(row.participant_instance_ids),
        "participant_layers": list(row.participant_layers),
        "participant_provenance": [
            _participant_reference_fact(item)
            for item in row.participant_provenance
        ],
        "relation_scope": row.relation_scope,
        "orientation": row.orientation,
        "arity": row.arity,
        "nominal_transformation_element": row.nominal_transformation_element,
        "nominal_transformation_semantics": row.nominal_transformation_semantics,
        "source_occurrence_kind": row.source_occurrence_kind,
        "source_upstream_fact_hash": row.source_upstream_fact_hash,
    }


def _participant_incidence_fact(row) -> dict[str, Any]:
    return {
        "incidence_fact_id": row.incidence_fact_id,
        "participant_instance_id": row.participant_instance_id,
        "participant_kind": row.participant_kind,
        "value": row.value,
        "participant_layer": row.participant_layer,
        "source_frame_id": row.source_frame_id,
        "source_ganzhi": row.source_ganzhi,
        "relation_ids": sorted(row.relation_ids),
        "relation_count": row.relation_count,
        "support_evidence_candidate_ids": sorted(
            row.support_evidence_candidate_ids
        ),
        "seasonal_role_ids": list(row.seasonal_role_ids),
        "seasonal_role_reference_ids": list(row.seasonal_role_reference_ids),
        "source_participant_fact_hash": row.source_participant_fact_hash,
        "source_relation_fact_hashes": sorted(row.source_relation_fact_hashes),
        "source_support_fact_hash": row.source_support_fact_hash,
        "snapshot_id": row.snapshot_id,
        "snapshot_fact_hash": row.snapshot_fact_hash,
    }


def _pair_topology_fact(row) -> dict[str, Any]:
    return {
        "pair_fact_id": row.pair_fact_id,
        "relation_ids": list(row.relation_ids),
        "topology_kind": row.topology_kind,
        "shared_participant_instance_ids": sorted(
            row.shared_participant_instance_ids
        ),
        "left_only_participant_instance_ids": sorted(
            row.left_only_participant_instance_ids
        ),
        "right_only_participant_instance_ids": sorted(
            row.right_only_participant_instance_ids
        ),
        "participant_layer_provenance": [
            _participant_reference_fact(item)
            for item in row.participant_layer_provenance
        ],
        "source_snapshot_id": row.source_snapshot_id,
        "source_snapshot_fact_hash": row.source_snapshot_fact_hash,
    }


def relation_incidence_fact_projection(
    context: BaziRelationIncidenceContext,
) -> dict[str, Any]:
    return {
        "snapshot": _snapshot_fact(context.snapshot),
        "relation_occurrences": [
            _relation_occurrence_fact(row) for row in context.relation_occurrences
        ],
        "participant_incidence_facts": [
            _participant_incidence_fact(row)
            for row in context.participant_incidence_facts
        ],
        "relation_pair_topology_facts": [
            _pair_topology_fact(row)
            for row in context.relation_pair_topology_facts
        ],
    }


def relation_incidence_hash_bundle(
    context: BaziRelationIncidenceContext,
    natal: BaziChartCandidate,
    chain: RelationIncidenceSnapshotInputs,
    source_flow_candidate_indices: tuple[int, ...],
    source_structural_candidate_indices: tuple[int, ...],
    source_support_candidate_indices: tuple[int, ...],
    source_temporal_candidate_indices: tuple[int, ...],
    source_temporal_seed_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ResolvedBaziRelationIncidenceProfile,
) -> IncidenceHashBundle:
    fact_hash = object_sha256(relation_incidence_fact_projection(context))
    computation_hash = object_sha256({
        "fact_hash": fact_hash,
        "upstream_computation_hashes": {
            "natal": natal.hashes.computation_hash,
            "flow": chain.flow.hashes.computation_hash,
            "structural": chain.structural.hashes.computation_hash,
            "support": chain.support.hashes.computation_hash,
        },
        "source_candidate_indices": {
            "flow": sorted(source_flow_candidate_indices),
            "structural": sorted(source_structural_candidate_indices),
            "support": sorted(source_support_candidate_indices),
            "temporal": sorted(source_temporal_candidate_indices),
        },
        "source_temporal_seed_ids": sorted(source_temporal_seed_ids),
        "lineage_binding_keys": list(lineage_binding_keys),
        "resolved_incidence_profile": json_value(profile),
        "algorithm_versions": dict(sorted(context.algorithm_versions.items())),
        "rule_and_source_lineage": [
            {
                "rule_set_id": context.snapshot.rule_set_id,
                "rule_set_version": context.snapshot.rule_set_version,
                "source_refs": sorted(context.snapshot.source_refs),
            }
        ] + [
            {
                "source_relation_rule_set_id": row.source_relation_rule_set_id,
                "source_relation_rule_set_version": row.source_relation_rule_set_version,
                "reference_rule_set_id": row.reference_rule_set_id,
                "reference_rule_set_version": row.reference_rule_set_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in context.relation_occurrences
        ] + [
            {
                "rule_set_id": row.rule_set_id,
                "rule_set_version": row.rule_set_version,
                "support_touch_rule_set_id": row.support_touch_rule_set_id,
                "support_touch_rule_set_version": row.support_touch_rule_set_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in context.participant_incidence_facts
        ] + [
            {
                "rule_set_id": row.rule_set_id,
                "rule_set_version": row.rule_set_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in context.relation_pair_topology_facts
        ],
        "hash_algorithm": f"{HASH_ALGORITHM_ID}@{HASH_ALGORITHM_VERSION}",
    })
    return IncidenceHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=HASH_ALGORITHM_ID,
        algorithm_version=HASH_ALGORITHM_VERSION,
    )


def validate_relation_incidence_context(
    context: BaziRelationIncidenceContext,
    natal: BaziChartCandidate,
    chain: RelationIncidenceSnapshotInputs,
    source_flow_candidate_indices: tuple[int, ...],
    source_structural_candidate_indices: tuple[int, ...],
    source_support_candidate_indices: tuple[int, ...],
    source_temporal_candidate_indices: tuple[int, ...],
    source_temporal_seed_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ResolvedBaziRelationIncidenceProfile,
    hashes: IncidenceHashBundle | None = None,
) -> IncidenceIntegrityReport:
    diagnostics: list[IncidenceIntegrityDiagnostic] = []
    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "PROFILE_INVALID", "profile", str(exc))

    if (
        context.snapshot.target_utc.tzinfo is None
        or context.snapshot.target_utc.utcoffset() is None
    ):
        _diag(
            diagnostics,
            "INVALID_TARGET_INSTANT",
            "snapshot.target_utc",
            "timezone-aware instant required",
        )
    elif (
        context.snapshot.target_utc.astimezone(timezone.utc)
        != chain.flow.context.target_utc.astimezone(timezone.utc)
    ):
        _diag(
            diagnostics,
            "TARGET_FLOW_MISMATCH",
            "snapshot.target_utc",
            context.snapshot.target_utc.isoformat(),
        )

    if (context.profile_id, context.profile_version) != (
        profile.profile_id,
        profile.profile_version,
    ):
        _diag(
            diagnostics,
            "PROFILE_BINDING_MISMATCH",
            "profile_id",
            context.profile_id,
        )

    upstream_expected = {
        "upstream_natal_fact_hash": natal.hashes.fact_hash,
        "upstream_natal_computation_hash": natal.hashes.computation_hash,
        "upstream_temporal_fact_hash": chain.flow.context.upstream_temporal_fact_hash,
        "upstream_flow_fact_hash": chain.flow.hashes.fact_hash,
        "upstream_flow_computation_hash": chain.flow.hashes.computation_hash,
        "upstream_structural_fact_hash": chain.structural.hashes.fact_hash,
        "upstream_structural_computation_hash": chain.structural.hashes.computation_hash,
        "upstream_support_fact_hash": chain.support.hashes.fact_hash,
        "upstream_support_computation_hash": chain.support.hashes.computation_hash,
    }
    for field_name, expected_value in upstream_expected.items():
        if getattr(context.snapshot, field_name) != expected_value:
            _diag(
                diagnostics,
                "UPSTREAM_HASH_BINDING_MISMATCH",
                f"snapshot.{field_name}",
                str(getattr(context.snapshot, field_name)),
            )
    if (
        chain.flow.integrity.status != "PASS"
        or chain.structural.integrity.status != "PASS"
        or chain.support.integrity.status != "PASS"
    ):
        _diag(
            diagnostics,
            "UPSTREAM_INTEGRITY_FAILED",
            "snapshot",
            "Flow/Structural/Support",
        )
    if (
        chain.flow.context.upstream_natal_fact_hash != natal.hashes.fact_hash
        or chain.structural.context.upstream_natal_fact_hash
        != natal.hashes.fact_hash
        or chain.support.context.upstream_natal_fact_hash != natal.hashes.fact_hash
    ):
        _diag(
            diagnostics,
            "NATAL_LINEAGE_MISMATCH",
            "snapshot",
            natal.hashes.fact_hash,
        )
    if (
        chain.structural.context.upstream_flow_fact_hash
        != chain.flow.hashes.fact_hash
        or chain.support.context.upstream_flow_fact_hash
        != chain.flow.hashes.fact_hash
        or chain.support.context.upstream_structural_fact_hash
        != chain.structural.hashes.fact_hash
    ):
        _diag(
            diagnostics,
            "UPSTREAM_LINEAGE_MISMATCH",
            "snapshot",
            "Flow/Structural/Support chain does not bind",
        )
    temporal_hashes = {
        chain.flow.context.upstream_temporal_fact_hash,
        chain.structural.context.upstream_temporal_fact_hash,
        chain.support.context.upstream_temporal_fact_hash,
        context.snapshot.upstream_temporal_fact_hash,
    }
    if len(temporal_hashes) != 1:
        _diag(
            diagnostics,
            "TEMPORAL_LINEAGE_MISMATCH",
            "snapshot.upstream_temporal_fact_hash",
            str(sorted(temporal_hashes)),
        )

    expected_flow_indices = tuple(sorted(
        chain.source_flow_candidate_indices or (chain.flow_index,)
    ))
    expected_structural_indices = tuple(sorted(
        chain.source_structural_candidate_indices or (chain.structural_index,)
    ))
    expected_support_indices = tuple(sorted(
        chain.source_support_candidate_indices or (chain.support_index,)
    ))
    candidate_lineage_checks = (
        (
            "FLOW_CANDIDATE_LINEAGE_MISMATCH",
            "source_flow_candidate_indices",
            tuple(sorted(source_flow_candidate_indices)),
            expected_flow_indices,
        ),
        (
            "STRUCTURAL_CANDIDATE_LINEAGE_MISMATCH",
            "source_structural_candidate_indices",
            tuple(sorted(source_structural_candidate_indices)),
            expected_structural_indices,
        ),
        (
            "SUPPORT_CANDIDATE_LINEAGE_MISMATCH",
            "source_support_candidate_indices",
            tuple(sorted(source_support_candidate_indices)),
            expected_support_indices,
        ),
    )
    for code, path, actual, expected in candidate_lineage_checks:
        if actual != expected:
            _diag(diagnostics, code, path, str(actual))

    request_candidate_groups = (
        chain.request_flow_candidates,
        chain.request_structural_candidates,
        chain.request_support_candidates,
    )
    if any(request_candidate_groups) and not all(request_candidate_groups):
        _diag(
            diagnostics,
            "UPSTREAM_REQUEST_CANDIDATE_SET_INCOMPLETE",
            "candidate_lineage",
            "Flow/Structural/Support request candidates must be supplied together",
        )
    elif all(request_candidate_groups):
        from .engine import (
            BaziRelationIncidenceGenerationError,
            _validated_support_lineage,
        )

        for support_index in expected_support_indices:
            try:
                validated = _validated_support_lineage(
                    natal,
                    chain.flow.context.target_utc,
                    chain.request_flow_candidates,
                    chain.request_structural_candidates,
                    chain.request_support_candidates,
                    support_index,
                )
            except BaziRelationIncidenceGenerationError as exc:
                _diag(
                    diagnostics,
                    "UPSTREAM_CANDIDATE_LINEAGE_INVALID",
                    f"source_support_candidate_indices[{support_index}]",
                    f"{exc.diagnostic_code}:{exc}",
                )
                continue
            replayed = (
                validated.flow_indices,
                validated.structural_indices,
                validated.temporal_indices,
                validated.seed_ids,
            )
            expected_replayed = (
                expected_flow_indices,
                expected_structural_indices,
                tuple(sorted(chain.support.source_temporal_candidate_indices)),
                tuple(sorted(chain.support.source_temporal_seed_ids)),
            )
            if replayed != expected_replayed:
                _diag(
                    diagnostics,
                    "UPSTREAM_CANDIDATE_LINEAGE_REPLAY_MISMATCH",
                    f"source_support_candidate_indices[{support_index}]",
                    "Support/Structural/Flow complete lineage does not replay",
                )
            request_support = chain.request_support_candidates[support_index]
            if (
                request_support.hashes != chain.support.hashes
                or request_support.context != chain.support.context
            ):
                _diag(
                    diagnostics,
                    "SUPPORT_COMPLETE_CONTRACT_REPLAY_MISMATCH",
                    f"source_support_candidate_indices[{support_index}]",
                    request_support.hashes.fact_hash,
                )

    expected_indices = tuple(sorted(chain.support.source_temporal_candidate_indices))
    expected_seeds = tuple(sorted(chain.support.source_temporal_seed_ids))
    if tuple(sorted(source_temporal_candidate_indices)) != expected_indices:
        _diag(
            diagnostics,
            "TEMPORAL_CANDIDATE_LINEAGE_MISMATCH",
            "source_temporal_candidate_indices",
            str(source_temporal_candidate_indices),
        )
    if tuple(sorted(source_temporal_seed_ids)) != expected_seeds:
        _diag(
            diagnostics,
            "TEMPORAL_SEED_LINEAGE_MISMATCH",
            "source_temporal_seed_ids",
            str(source_temporal_seed_ids),
        )
    expected_keys = (
        f"TEMPORAL_FACT:{chain.flow.context.upstream_temporal_fact_hash}",
        f"FLOW_FACT:{chain.flow.hashes.fact_hash}",
        f"FLOW_COMPUTATION:{chain.flow.hashes.computation_hash}",
        f"STRUCTURAL_FACT:{chain.structural.hashes.fact_hash}",
        f"STRUCTURAL_COMPUTATION:{chain.structural.hashes.computation_hash}",
        f"SUPPORT_FACT:{chain.support.hashes.fact_hash}",
        f"SUPPORT_COMPUTATION:{chain.support.hashes.computation_hash}",
        *(f"FLOW_CANDIDATE_INDEX:{item}" for item in expected_flow_indices),
        *(
            f"STRUCTURAL_CANDIDATE_INDEX:{item}"
            for item in expected_structural_indices
        ),
        *(f"SUPPORT_CANDIDATE_INDEX:{item}" for item in expected_support_indices),
        *(f"TEMPORAL_CANDIDATE_INDEX:{item}" for item in expected_indices),
        *(f"TEMPORAL_SEED:{item}" for item in expected_seeds),
    )
    if lineage_binding_keys != expected_keys:
        _diag(
            diagnostics,
            "LINEAGE_BINDING_KEYS_REPLAY_MISMATCH",
            "lineage_binding_keys",
            "exact upstream lineage keys do not replay",
        )

    expected_relation_ids = tuple(
        row.relation_id for _, row in _released_relation_rows(natal, chain.structural)
    )
    expected_snapshot_payload = _snapshot_fact_payload(
        natal, chain, expected_relation_ids
    )
    expected_snapshot_hash = object_sha256(expected_snapshot_payload)
    if context.snapshot.raw_relation_ids != expected_relation_ids:
        _diag(
            diagnostics,
            "SNAPSHOT_RELATION_REPLAY_MISMATCH",
            "snapshot.raw_relation_ids",
            "must equal released Natal plus Structural relation IDs",
        )
    if context.snapshot.snapshot_fact_hash != expected_snapshot_hash:
        _diag(
            diagnostics,
            "SNAPSHOT_FACT_HASH_MISMATCH",
            "snapshot.snapshot_fact_hash",
            context.snapshot.snapshot_fact_hash,
        )
    if (
        context.snapshot.snapshot_id
        != f"RELATION_INCIDENCE_SNAPSHOT:{expected_snapshot_hash}"
    ):
        _diag(
            diagnostics,
            "SNAPSHOT_ID_MISMATCH",
            "snapshot.snapshot_id",
            context.snapshot.snapshot_id,
        )

    participants = _participant_map(natal, chain.flow, chain.structural)
    relation_by_id = {
        row.relation_id: row for row in context.relation_occurrences
    }
    if len(relation_by_id) != len(context.relation_occurrences):
        _diag(
            diagnostics,
            "DUPLICATE_RELATION_OCCURRENCE_REFERENCE",
            "relation_occurrences",
            "relation IDs must be unique",
        )
    if tuple(sorted(relation_by_id)) != expected_relation_ids:
        _diag(
            diagnostics,
            "RELATION_OCCURRENCE_REFERENCE_SET_MISMATCH",
            "relation_occurrences",
            "one reference per released relation occurrence required",
        )
    for index, row in enumerate(context.relation_occurrences):
        path = f"relation_occurrences[{index}]"
        if row.arity != len(row.participant_instance_ids):
            _diag(diagnostics, "RELATION_ARITY_MISMATCH", path, row.relation_id)
        if tuple(item.instance_id for item in row.participant_provenance) != row.participant_instance_ids:
            _diag(
                diagnostics,
                "RELATION_PARTICIPANT_PROVENANCE_ORDER_MISMATCH",
                path,
                row.relation_id,
            )
        for participant in row.participant_provenance:
            if participants.get(participant.instance_id) != participant:
                _diag(
                    diagnostics,
                    "RELATION_PARTICIPANT_REFERENCE_MISMATCH",
                    path,
                    participant.instance_id,
                )
        if row.nominal_transformation_element is not None and row.nominal_transformation_semantics != "NOMINAL_TARGET_ONLY_NOT_TRANSFORMATION_SUCCESS":
            _diag(
                diagnostics,
                "NOMINAL_TRANSFORMATION_SEMANTICS_INVALID",
                path,
                row.relation_id,
            )
        if row.nominal_transformation_element is None and row.nominal_transformation_semantics is not None:
            _diag(
                diagnostics,
                "SPURIOUS_NOMINAL_TRANSFORMATION_SEMANTICS",
                path,
                row.relation_id,
            )

    incidence_by_id = {
        row.participant_instance_id: row
        for row in context.participant_incidence_facts
    }
    if len(incidence_by_id) != len(context.participant_incidence_facts):
        _diag(
            diagnostics,
            "DUPLICATE_PARTICIPANT_INCIDENCE_FACT",
            "participant_incidence_facts",
            "participant instance IDs must be unique",
        )
    expected_active_participants = {
        participant_id
        for relation in context.relation_occurrences
        for participant_id in relation.participant_instance_ids
    }
    if set(incidence_by_id) != expected_active_participants:
        _diag(
            diagnostics,
            "PARTICIPANT_INCIDENCE_COVERAGE_MISMATCH",
            "participant_incidence_facts",
            "exact active relation participant set required",
        )
    support_ids = {
        row.candidate_id
        for row in chain.support.context.support_evidence_candidates
    }
    for index, row in enumerate(context.participant_incidence_facts):
        path = f"participant_incidence_facts[{index}]"
        participant = participants.get(row.participant_instance_id)
        if participant is None:
            _diag(
                diagnostics,
                "PARTICIPANT_REFERENCE_MISSING",
                path,
                row.participant_instance_id,
            )
            continue
        expected_relations = tuple(sorted(
            relation.relation_id
            for relation in context.relation_occurrences
            if row.participant_instance_id in relation.participant_instance_ids
        ))
        if row.relation_ids != expected_relations:
            _diag(
                diagnostics,
                "PARTICIPANT_RELATION_MEMBERSHIP_MISMATCH",
                path,
                row.participant_instance_id,
            )
        if row.relation_count != len(expected_relations):
            _diag(
                diagnostics,
                "PARTICIPANT_RELATION_DEGREE_MISMATCH",
                path,
                str(row.relation_count),
            )
        expected_support = _support_touch_ids(row.participant_instance_id, chain)
        if row.support_evidence_candidate_ids != expected_support:
            _diag(
                diagnostics,
                "SUPPORT_TOUCH_REPLAY_MISMATCH",
                path,
                row.participant_instance_id,
            )
        if not set(row.support_evidence_candidate_ids) <= support_ids:
            _diag(
                diagnostics,
                "SUPPORT_TOUCH_REFERENCE_MISSING",
                path,
                row.participant_instance_id,
            )
        expected_role_ids, expected_role_refs = _seasonal_roles(
            row.participant_instance_id, chain
        )
        if (
            row.seasonal_role_ids != expected_role_ids
            or row.seasonal_role_reference_ids != expected_role_refs
        ):
            _diag(
                diagnostics,
                "SEASONAL_ROLE_TOUCH_REPLAY_MISMATCH",
                path,
                row.participant_instance_id,
            )
        participant_payload = (
            row.participant_kind,
            row.value,
            row.participant_layer,
            row.source_frame_id,
            row.source_ganzhi,
            row.source_participant_fact_hash,
        )
        expected_payload = (
            participant.participant_kind,
            participant.value,
            participant.participant_layer,
            participant.source_frame_id,
            participant.source_ganzhi,
            participant.source_upstream_fact_hash,
        )
        if participant_payload != expected_payload:
            _diag(
                diagnostics,
                "PARTICIPANT_PAYLOAD_MISMATCH",
                path,
                row.participant_instance_id,
            )

    expected_pairs = tuple(combinations(sorted(relation_by_id), 2))
    pair_by_relations = {
        row.relation_ids: row for row in context.relation_pair_topology_facts
    }
    if len(pair_by_relations) != len(context.relation_pair_topology_facts):
        _diag(
            diagnostics,
            "DUPLICATE_RELATION_PAIR_TOPOLOGY",
            "relation_pair_topology_facts",
            "each unordered pair must occur once",
        )
    if tuple(sorted(pair_by_relations)) != expected_pairs:
        _diag(
            diagnostics,
            "RELATION_PAIR_COVERAGE_MISMATCH",
            "relation_pair_topology_facts",
            f"expected {len(expected_pairs)} unordered pairs",
        )
    for index, row in enumerate(context.relation_pair_topology_facts):
        path = f"relation_pair_topology_facts[{index}]"
        if tuple(sorted(row.relation_ids)) != row.relation_ids:
            _diag(
                diagnostics,
                "RELATION_PAIR_NOT_CANONICAL",
                path,
                str(row.relation_ids),
            )
        left = relation_by_id.get(row.relation_ids[0])
        right = relation_by_id.get(row.relation_ids[1])
        if left is None or right is None or left.relation_id == right.relation_id:
            _diag(
                diagnostics,
                "RELATION_PAIR_REFERENCE_INVALID",
                path,
                str(row.relation_ids),
            )
            continue
        left_ids = set(left.participant_instance_ids)
        right_ids = set(right.participant_instance_ids)
        shared = tuple(sorted(left_ids & right_ids))
        left_only = tuple(sorted(left_ids - right_ids))
        right_only = tuple(sorted(right_ids - left_ids))
        expected_kind = SHARED_PARTICIPANT if shared else DISJOINT
        if row.topology_kind != expected_kind:
            _diag(
                diagnostics,
                "PAIR_TOPOLOGY_KIND_MISMATCH",
                path,
                row.topology_kind,
            )
        if (
            row.shared_participant_instance_ids != shared
            or row.left_only_participant_instance_ids != left_only
            or row.right_only_participant_instance_ids != right_only
        ):
            _diag(
                diagnostics,
                "PAIR_TOPOLOGY_SET_REPLAY_MISMATCH",
                path,
                str(row.relation_ids),
            )
        expected_provenance = tuple(
            participants[instance_id]
            for instance_id in sorted(left_ids | right_ids)
        )
        if row.participant_layer_provenance != expected_provenance:
            _diag(
                diagnostics,
                "PAIR_PARTICIPANT_PROVENANCE_MISMATCH",
                path,
                str(row.relation_ids),
            )
        if (
            row.source_snapshot_id != context.snapshot.snapshot_id
            or row.source_snapshot_fact_hash != context.snapshot.snapshot_fact_hash
        ):
            _diag(
                diagnostics,
                "PAIR_SNAPSHOT_BINDING_MISMATCH",
                path,
                row.pair_fact_id,
            )

    if chain.flow.context.active_dayun_kind == "PRE_DAYUN" and any(
        row.participant_layer == "DAYUN"
        for row in context.participant_incidence_facts
    ):
        _diag(
            diagnostics,
            "PRE_DAYUN_FAKE_INCIDENCE_PARTICIPANT",
            "participant_incidence_facts",
            "PRE_DAYUN cannot produce a Dayun occurrence",
        )

    for collection_name, collection in (
        ("relation_occurrences", context.relation_occurrences),
        ("participant_incidence_facts", context.participant_incidence_facts),
        ("relation_pair_topology_facts", context.relation_pair_topology_facts),
    ):
        for index, row in enumerate(collection):
            present_fields = {field.name.lower() for field in fields(row)}
            prohibited = present_fields & PROHIBITED_EFFECT_FIELDS
            if prohibited:
                _diag(
                    diagnostics,
                    "CLASSICAL_EFFECT_FIELD_PRESENT",
                    f"{collection_name}[{index}]",
                    ",".join(sorted(prohibited)),
                )

    try:
        expected_context = build_relation_incidence_context(
            natal, chain, profile
        )
    except (ValueError, KeyError) as exc:
        _diag(diagnostics, "INCIDENCE_REPLAY_FAILED", "context", str(exc))
        expected_context = None
    if expected_context is not None:
        replay_checks = (
            ("SNAPSHOT_REPLAY_MISMATCH", "snapshot"),
            ("RELATION_OCCURRENCE_REPLAY_MISMATCH", "relation_occurrences"),
            ("PARTICIPANT_INCIDENCE_REPLAY_MISMATCH", "participant_incidence_facts"),
            ("RELATION_PAIR_TOPOLOGY_REPLAY_MISMATCH", "relation_pair_topology_facts"),
            ("INCIDENCE_ALGORITHM_VERSION_MISMATCH", "algorithm_versions"),
        )
        for code, field_name in replay_checks:
            if getattr(context, field_name) != getattr(expected_context, field_name):
                _diag(
                    diagnostics,
                    code,
                    field_name,
                    "deterministic incidence replay mismatch",
                )

    if hashes is not None:
        expected_hashes = relation_incidence_hash_bundle(
            context,
            natal,
            chain,
            source_flow_candidate_indices,
            source_structural_candidate_indices,
            source_support_candidate_indices,
            source_temporal_candidate_indices,
            source_temporal_seed_ids,
            lineage_binding_keys,
            profile,
        )
        if hashes != expected_hashes:
            _diag(
                diagnostics,
                "INCIDENCE_HASH_REPLAY_MISMATCH",
                "hashes",
                hashes.fact_hash,
            )

    return IncidenceIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=INTEGRITY_ALGORITHM_ID,
        algorithm_version=INTEGRITY_ALGORITHM_VERSION,
    )
