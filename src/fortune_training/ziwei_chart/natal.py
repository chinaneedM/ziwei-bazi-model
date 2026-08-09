from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .models import AddressAttribute, DesignationBinding, GenerationStep, NatalStructureState
from .registries import (
    HEAVENLY_STEMS,
    PALACE_DESIGNATIONS,
    YEAR_STEM_TO_YIN_START_STEM,
    address,
    bureau_for_ganzhi,
    sexagenary_for_year,
    stem_index,
)


NATAL_STRUCTURE_ALGORITHM_ID = "ZIWEI-NATAL-STRUCTURE-V1"
NATAL_STRUCTURE_ALGORITHM_VERSION = "1.0.0"

MING_SHEN_SOURCE = ("S01:ZZZA-PR-008",)
PALACE_DESIGNATION_SOURCE = ("S01:ZZZA-PR-009",)
ADDRESS_STEM_SOURCE = ("S01:ZZZA-PR-010",)
BUREAU_SOURCE = ("S01:ZZZA-PR-010", "S01:ZZZA-PR-011")


@dataclass(frozen=True)
class NatalStructureInput:
    lunar_year: int
    lunar_month: int
    lunar_day: int
    is_leap_month: bool
    lunar_month_length_days: int
    local_apparent_solar_datetime: datetime
    life_body_leap_month_policy: str


class NatalStructureGenerator:
    @staticmethod
    def _natal_month_coordinate(value: NatalStructureInput) -> int:
        month = value.lunar_month
        if not value.is_leap_month:
            return month
        policy = value.life_body_leap_month_policy
        if policy == "FULLBOOK_NEXT_MONTH":
            return month % 12 + 1
        if policy == "ZHONGZHOU_FIXED_15":
            return month if value.lunar_day <= 15 else month % 12 + 1
        if policy == "CURRENT_MONTH":
            return month
        if policy == "TRUE_HALF_SPLIT":
            first_half_end = (value.lunar_month_length_days + 1) // 2
            return month if value.lunar_day <= first_half_end else month % 12 + 1
        raise ValueError(f"unsupported life/body leap-month policy: {policy}")

    @staticmethod
    def _hour_branch_index(local_apparent_solar_datetime: datetime) -> int:
        # 子 covers 23:00..00:59, 丑 01:00..02:59, ...
        return ((local_apparent_solar_datetime.hour + 1) // 2) % 12

    @staticmethod
    def _address_stems(year_stem: str) -> tuple[AddressAttribute, ...]:
        yin_start = YEAR_STEM_TO_YIN_START_STEM[year_stem]
        yin_start_index = stem_index(yin_start)
        rows: list[AddressAttribute] = []
        for addr_index in range(12):
            forward_offset_from_yin = (addr_index - 2) % 12
            stem = HEAVENLY_STEMS[(yin_start_index + forward_offset_from_yin) % 10]
            rows.append(AddressAttribute(address(addr_index), stem))
        return tuple(rows)

    def generate(self, value: NatalStructureInput) -> NatalStructureState:
        if not 1 <= value.lunar_month <= 12:
            raise ValueError("lunar_month must be in [1, 12]")
        if not 1 <= value.lunar_day <= 30:
            raise ValueError("lunar_day must be in [1, 30]")

        natal_month = self._natal_month_coordinate(value)
        month_anchor = address(2 + natal_month - 1)
        hour_branch = address(self._hour_branch_index(value.local_apparent_solar_datetime))
        life = address(month_anchor.index - hour_branch.index)
        body = address(month_anchor.index + hour_branch.index)

        year_stem, year_branch = sexagenary_for_year(value.lunar_year)
        attributes = self._address_stems(year_stem)
        life_stem = attributes[life.index].stem
        bureau = bureau_for_ganzhi(life_stem, life.branch)

        designations = tuple(
            DesignationBinding(designation_id, display_name, address(life.index - offset))
            for offset, (designation_id, display_name) in enumerate(PALACE_DESIGNATIONS)
        )

        trace = (
            GenerationStep(
                operation="compile_natal_month_coordinate",
                inputs={
                    "raw_lunar_month": value.lunar_month,
                    "lunar_day": value.lunar_day,
                    "is_leap_month": value.is_leap_month,
                    "month_length_days": value.lunar_month_length_days,
                    "policy": value.life_body_leap_month_policy,
                },
                outputs={"natal_month_coordinate": natal_month},
                algorithm_id=NATAL_STRUCTURE_ALGORITHM_ID,
                algorithm_version=NATAL_STRUCTURE_ALGORITHM_VERSION,
                source_refs=MING_SHEN_SOURCE,
            ),
            GenerationStep(
                operation="place_life_and_body",
                inputs={
                    "month_anchor": month_anchor.branch,
                    "birth_hour_branch": hour_branch.branch,
                },
                outputs={"life": life.branch, "body": body.branch},
                algorithm_id=NATAL_STRUCTURE_ALGORITHM_ID,
                algorithm_version=NATAL_STRUCTURE_ALGORITHM_VERSION,
                source_refs=MING_SHEN_SOURCE,
            ),
            GenerationStep(
                operation="bind_twelve_palace_designations",
                inputs={"life_address": life.branch},
                outputs={row.designation_id: row.address.branch for row in designations},
                algorithm_id=NATAL_STRUCTURE_ALGORITHM_ID,
                algorithm_version=NATAL_STRUCTURE_ALGORITHM_VERSION,
                source_refs=PALACE_DESIGNATION_SOURCE,
            ),
            GenerationStep(
                operation="generate_address_stems",
                inputs={"ziwei_birth_year_stem": year_stem},
                outputs={row.address.branch: row.stem for row in attributes},
                algorithm_id=NATAL_STRUCTURE_ALGORITHM_ID,
                algorithm_version=NATAL_STRUCTURE_ALGORITHM_VERSION,
                source_refs=ADDRESS_STEM_SOURCE,
            ),
            GenerationStep(
                operation="derive_five_element_bureau",
                inputs={
                    "ziwei_birth_year_stem": year_stem,
                    "life_address": life.branch,
                    "life_address_stem": life_stem,
                },
                outputs={
                    "life_palace_ganzhi": bureau.life_palace_ganzhi,
                    "nayin": bureau.nayin_name,
                    "bureau_element": bureau.element,
                    "bureau_number": bureau.number,
                },
                algorithm_id=NATAL_STRUCTURE_ALGORITHM_ID,
                algorithm_version=NATAL_STRUCTURE_ALGORITHM_VERSION,
                source_refs=BUREAU_SOURCE,
            ),
        )

        return NatalStructureState(
            ziwei_birth_year_stem=year_stem,
            ziwei_birth_year_branch=year_branch,
            raw_lunar_month=value.lunar_month,
            natal_month_coordinate=natal_month,
            lunar_birth_day=value.lunar_day,
            birth_hour_branch=hour_branch,
            month_anchor=month_anchor,
            life_address=life,
            body_address=body,
            designation_bindings=designations,
            address_attributes=attributes,
            bureau=bureau,
            trace=trace,
        )
