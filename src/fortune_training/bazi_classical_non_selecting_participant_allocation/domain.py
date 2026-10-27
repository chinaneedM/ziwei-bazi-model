from __future__ import annotations

from typing import Any

from fortune_training.util import object_sha256

from .models import UnorderedExactInstanceSetPathCandidate
from .profile import (
    ALTERNATIVE_PATH_REQUIREMENT,
    PATH_CANDIDATE_KIND,
    SLOT_EQUIVALENCE_VALUES,
    ClassicalNonSelectingParticipantAllocationProfile,
)


class AllocationMultiplicityContractError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


def validate_multiplicity_reference(reference: Any) -> None:
    slots = tuple(reference.exchangeable_symbolic_slot_node_ids)
    runtime_ids = tuple(reference.exact_runtime_instance_ids)
    required = reference.required_symbolic_cardinality
    if not reference.multiplicity_constraint_id:
        raise AllocationMultiplicityContractError(
            "MISSING_MULTIPLICITY_CONSTRAINT_ID", "empty multiplicity constraint id"
        )
    if not slots or len(slots) != len(set(slots)):
        raise AllocationMultiplicityContractError(
            "INVALID_OR_DUPLICATE_SYMBOLIC_SLOT_IDS",
            reference.multiplicity_constraint_id,
        )
    if required <= 0:
        raise AllocationMultiplicityContractError(
            "NON_POSITIVE_REQUIRED_SYMBOLIC_CARDINALITY",
            reference.multiplicity_constraint_id,
        )
    if len(slots) != required:
        raise AllocationMultiplicityContractError(
            "REQUIRED_CARDINALITY_SYMBOLIC_SLOT_COUNT_MISMATCH",
            f"{reference.multiplicity_constraint_id}:{len(slots)}:{required}",
        )
    if len(runtime_ids) != len(set(runtime_ids)):
        raise AllocationMultiplicityContractError(
            "DUPLICATE_EXACT_RUNTIME_INSTANCE_IDS",
            reference.multiplicity_constraint_id,
        )
    if reference.slot_equivalence not in SLOT_EQUIVALENCE_VALUES:
        raise AllocationMultiplicityContractError(
            "UNKNOWN_SLOT_EQUIVALENCE",
            f"{reference.multiplicity_constraint_id}:{reference.slot_equivalence}",
        )
    if reference.alternative_path_requirement != ALTERNATIVE_PATH_REQUIREMENT:
        raise AllocationMultiplicityContractError(
            "ALTERNATIVE_PATH_PRESERVATION_CONTRACT_MISMATCH",
            f"{reference.multiplicity_constraint_id}:{reference.alternative_path_requirement}",
        )


def classify_allocation_domain(reference: Any) -> tuple[str, tuple[str, ...]]:
    validate_multiplicity_reference(reference)
    runtime_count = len(reference.exact_runtime_instance_ids)
    required = reference.required_symbolic_cardinality
    if runtime_count == required:
        return "EXACT_INSTANCE_SET_CARDINALITY_MATCH", ()
    if runtime_count > required:
        return (
            "EXACT_INSTANCE_POOL_REQUIRES_COMPATIBILITY_RELATION",
            (
                "SLOT_INSTANCE_COMPATIBILITY_RELATION_NOT_RELEASED",
                "SYNTHETIC_COMBINATORIAL_ENUMERATION_FORBIDDEN",
            ),
        )
    return (
        "INSUFFICIENT_EXACT_INSTANCE_CARDINALITY",
        ("INSUFFICIENT_EXACT_RUNTIME_INSTANCE_CARDINALITY",),
    )


def build_unordered_path_candidate(
    source_semantic_candidate_id: str,
    source_mechanism_proposal_id: str,
    reference: Any,
    profile: ClassicalNonSelectingParticipantAllocationProfile,
) -> UnorderedExactInstanceSetPathCandidate:
    classification, blockers = classify_allocation_domain(reference)
    if classification != "EXACT_INSTANCE_SET_CARDINALITY_MATCH" or blockers:
        raise AllocationMultiplicityContractError(
            "UNORDERED_PATH_CANDIDATE_NOT_MECHANICALLY_PERMITTED",
            reference.multiplicity_constraint_id,
        )
    path_candidate_id = "CLASSICAL_UNORDERED_EXACT_INSTANCE_SET_PATH_CANDIDATE:" + object_sha256({
        "source_semantic_candidate_id": source_semantic_candidate_id,
        "source_mechanism_proposal_id": source_mechanism_proposal_id,
        "multiplicity_constraint_id": reference.multiplicity_constraint_id,
        "exact_runtime_instance_ids": tuple(reference.exact_runtime_instance_ids),
        "exchangeable_symbolic_slot_node_ids": tuple(
            reference.exchangeable_symbolic_slot_node_ids
        ),
        "required_symbolic_cardinality": reference.required_symbolic_cardinality,
        "slot_equivalence": reference.slot_equivalence,
    })
    return UnorderedExactInstanceSetPathCandidate(
        path_candidate_id=path_candidate_id,
        path_candidate_kind=PATH_CANDIDATE_KIND,
        source_semantic_candidate_id=source_semantic_candidate_id,
        source_mechanism_proposal_id=source_mechanism_proposal_id,
        multiplicity_constraint_id=reference.multiplicity_constraint_id,
        exchangeable_symbolic_slot_node_ids=tuple(
            reference.exchangeable_symbolic_slot_node_ids
        ),
        exact_runtime_instance_ids=tuple(reference.exact_runtime_instance_ids),
        required_symbolic_cardinality=reference.required_symbolic_cardinality,
        slot_equivalence=reference.slot_equivalence,
        path_candidate_semantics=profile.path_candidate_semantics,
        slot_assignment_semantics=profile.slot_assignment_semantics,
        path_ordering_semantics=profile.path_ordering_semantics,
        compatibility_semantics=profile.compatibility_semantics,
        selection_semantics=profile.participant_path_selection_semantics,
    )
