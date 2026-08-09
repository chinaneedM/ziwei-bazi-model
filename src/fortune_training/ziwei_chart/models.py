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


@dataclass(frozen=True)
class GenerationStep:
    operation: str
    inputs: dict[str, Any]
    outputs: dict[str, Any]
    algorithm_id: str
    algorithm_version: str


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
    algorithm_versions: dict[str, str] = field(default_factory=dict)
