from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Sex(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


@dataclass(frozen=True)
class Address:
    index: int
    branch: str

    def __post_init__(self) -> None:
        if not 0 <= self.index < 12:
            raise ValueError("address index must be in [0, 11]")


@dataclass(frozen=True)
class DesignationBinding:
    designation_id: str
    display_name: str
    address: Address


@dataclass(frozen=True)
class AddressAttribute:
    address: Address
    stem: str


@dataclass(frozen=True)
class FiveElementBureau:
    element: str
    number: int
    life_palace_ganzhi: str
    nayin_name: str


@dataclass(frozen=True)
class Placement:
    entity_id: str
    display_name: str
    address: Address
    generator_id: str
    algorithm_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class DignityAnnotation:
    annotation_id: str
    annotation_type: str
    target_entity_id: str
    target_address: Address
    grade: str | None
    scale_id: str
    scale_version: str
    rule_set_id: str
    rule_set_version: str
    generator_id: str
    algorithm_version: str
    source_refs: tuple[str, ...]
    status: str = "GRADED"


@dataclass(frozen=True)
class TransformationActivation:
    activation_id: str
    transformation_type: str
    target_entity_id: str
    target_display_name: str
    target_address: Address
    source_layer: str
    source_stem: str
    context_id: str
    assignment_id: str
    mechanism_id: str
    generator_id: str
    algorithm_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class TemporalAuxiliaryActivation:
    activation_id: str
    entity_id: str
    display_name: str
    target_address: Address
    source_layer: str
    source_stem: str
    context_id: str
    rule_id: str
    generator_id: str
    algorithm_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class TemporalAuxiliaryMethodCandidate:
    candidate_id: str
    method_id: str
    authority_status: str
    activations: tuple[TemporalAuxiliaryActivation, ...]
    source_refs: tuple[str, ...]
    fact_hash: str
    computation_hash: str


@dataclass(frozen=True)
class TemporalAuxiliaryCandidateSet:
    candidate_set_id: str
    source_layer: str
    source_stem: str
    context_id: str
    entity_ids: tuple[str, ...]
    selection_status: str
    method_candidates: tuple[TemporalAuxiliaryMethodCandidate, ...]
    source_refs: tuple[str, ...]
    fact_hash: str
    computation_hash: str


@dataclass(frozen=True)
class RoleBinding:
    role_id: str
    display_name: str
    entity_id: str
    entity_display_name: str
    basis_type: str
    basis_value: str
    generator_id: str
    algorithm_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class RingMemberBinding:
    member_id: str
    display_name: str
    address: Address
    ordinal: int
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class RingInstance:
    ring_id: str
    display_name: str
    anchor_address: Address
    direction: str
    generator_id: str
    algorithm_version: str
    source_refs: tuple[str, ...]
    members: tuple[RingMemberBinding, ...]


@dataclass(frozen=True)
class GenerationStep:
    operation: str
    inputs: dict[str, Any]
    outputs: dict[str, Any]
    algorithm_id: str
    algorithm_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class NatalStructureState:
    ziwei_birth_year_stem: str
    ziwei_birth_year_branch: str
    raw_lunar_month: int
    natal_month_coordinate: int
    lunar_birth_day: int
    birth_hour_branch: Address
    month_anchor: Address
    life_address: Address
    body_address: Address
    designation_bindings: tuple[DesignationBinding, ...]
    address_attributes: tuple[AddressAttribute, ...]
    bureau: FiveElementBureau
    trace: tuple[GenerationStep, ...] = ()


@dataclass(frozen=True)
class NatalChartState:
    structure: NatalStructureState
    placements: tuple[Placement, ...]
    profile_id: str
    profile_version: str
    annotations: tuple[DignityAnnotation, ...] = ()
    transformations: tuple[TransformationActivation, ...] = ()
    role_bindings: tuple[RoleBinding, ...] = ()
    rings: tuple[RingInstance, ...] = ()
    algorithm_versions: dict[str, str] = field(default_factory=dict)
