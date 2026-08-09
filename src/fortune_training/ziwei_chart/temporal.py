from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .models import (
    Address,
    AddressAttribute,
    DesignationBinding,
    NatalChartState,
    Placement,
    Sex,
    TransformationActivation,
)
from .registries import PALACE_DESIGNATIONS, address, branch_index, sexagenary_for_year
from .transformations import TransformationGenerator

if TYPE_CHECKING:
    from .profile import ResolvedZiweiCalculationProfile


TEMPORAL_ALGORITHM_ID = "ZIWEI-TEMPORAL-FRAMES-V1"
TEMPORAL_ALGORITHM_VERSION = "1.0.0"
S10_CURRENT_TEMPORAL_RULE_SET_ID = "S10_CURRENT_TEMPORAL_R1"
S10_CURRENT_TEMPORAL_RULE_SET_VERSION = "1.0.0"

DAXIAN_SOURCE_REFS = ("S10:中州派动态坐标生成补充:大限",)
ANNUAL_SOURCE_REFS = ("S10:中州派动态坐标生成补充:流年太岁与斗君",)
MINOR_LIMIT_SOURCE_REFS = ("S10:中州派动态坐标生成补充:小限",)

YANG_STEMS = {"甲", "丙", "戊", "庚", "壬"}
MINOR_AGE_ONE_START_BY_YEAR_BRANCH = {
    "寅": "辰", "午": "辰", "戌": "辰",
    "亥": "丑", "卯": "丑", "未": "丑",
    "申": "戌", "子": "戌", "辰": "戌",
    "巳": "未", "酉": "未", "丑": "未",
}


class TemporalGenerationError(ValueError):
    def __init__(self, diagnostic_code: str) -> None:
        super().__init__(diagnostic_code)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class TemporalNatalContext:
    ziwei_birth_year: int
    ziwei_birth_year_stem: str
    ziwei_birth_year_branch: str
    bureau_number: int
    bureau_element: str
    life_address: Address
    address_attributes: tuple[AddressAttribute, ...]
    placements: tuple[Placement, ...]
    sex: Sex

    @classmethod
    def from_natal_chart(
        cls,
        ziwei_birth_year: int,
        sex: Sex,
        chart: NatalChartState,
    ) -> "TemporalNatalContext":
        structure = chart.structure
        return cls(
            ziwei_birth_year=ziwei_birth_year,
            ziwei_birth_year_stem=structure.ziwei_birth_year_stem,
            ziwei_birth_year_branch=structure.ziwei_birth_year_branch,
            bureau_number=structure.bureau.number,
            bureau_element=structure.bureau.element,
            life_address=structure.life_address,
            address_attributes=structure.address_attributes,
            placements=chart.placements,
            sex=sex,
        )


@dataclass(frozen=True)
class DaxianFrame:
    frame_id: str
    index: int
    nominal_age_start: int
    nominal_age_end: int
    absolute_year_start: int
    absolute_year_end: int
    active_address: Address
    active_palace_ganzhi: str
    designation_overlay: tuple[DesignationBinding, ...]
    source_stem: str
    transformations: tuple[TransformationActivation, ...]
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class AnnualFrame:
    frame_id: str
    absolute_year: int
    nominal_age: int
    year_stem: str
    year_branch: str
    active_address: Address
    active_palace_ganzhi: str
    designation_overlay: tuple[DesignationBinding, ...]
    parent_daxian_frame_id: str | None
    transformations: tuple[TransformationActivation, ...]
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class MinorLimitFrame:
    frame_id: str
    nominal_age: int
    active_address: Address
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class ZiweiTemporalState:
    rule_set_id: str
    rule_set_version: str
    algorithm_id: str
    algorithm_version: str
    daxian_direction: str
    first_daxian_nominal_age: int
    daxian_frames: tuple[DaxianFrame, ...]
    annual_frames: tuple[AnnualFrame, ...]
    minor_limit_frames: tuple[MinorLimitFrame, ...]


class ZiweiTemporalEngine:
    """Generate Daxian, Annual and Minor-Limit frames without mutating natal facts."""

    rule_set_id = S10_CURRENT_TEMPORAL_RULE_SET_ID
    rule_set_version = S10_CURRENT_TEMPORAL_RULE_SET_VERSION
    algorithm_id = TEMPORAL_ALGORITHM_ID
    algorithm_version = TEMPORAL_ALGORITHM_VERSION

    def __init__(self, transformation_generator: TransformationGenerator | None = None) -> None:
        self.transformations = transformation_generator or TransformationGenerator()

    @staticmethod
    def _daxian_direction(year_stem: str, sex: Sex) -> int:
        is_yang = year_stem in YANG_STEMS
        forward = (is_yang and sex is Sex.MALE) or ((not is_yang) and sex is Sex.FEMALE)
        return 1 if forward else -1

    @staticmethod
    def _direction_name(direction: int) -> str:
        return "FORWARD" if direction == 1 else "REVERSE"

    @staticmethod
    def _address_stem_map(attributes: tuple[AddressAttribute, ...]) -> dict[int, str]:
        mapping: dict[int, str] = {}
        for row in attributes:
            if row.address.index in mapping:
                raise TemporalGenerationError("TEMPORAL_DUPLICATE_NATAL_ADDRESS_STEM")
            mapping[row.address.index] = row.stem
        if set(mapping) != set(range(12)):
            raise TemporalGenerationError("TEMPORAL_INCOMPLETE_NATAL_ADDRESS_STEMS")
        return mapping

    @staticmethod
    def _designation_overlay(active_life: Address) -> tuple[DesignationBinding, ...]:
        return tuple(
            DesignationBinding(designation_id, display_name, address(active_life.index - offset))
            for offset, (designation_id, display_name) in enumerate(PALACE_DESIGNATIONS)
        )

    @staticmethod
    def _transformations_enabled(profile: "ResolvedZiweiCalculationProfile") -> bool:
        return profile.transformation_rule_set_id is not None

    def _activate_transformations(
        self,
        profile: "ResolvedZiweiCalculationProfile",
        source_stem: str,
        placements: tuple[Placement, ...],
        *,
        source_layer: str,
        context_id: str,
    ) -> tuple[TransformationActivation, ...]:
        if not self._transformations_enabled(profile):
            return ()
        return self.transformations.activate(
            source_stem,
            placements,
            source_layer=source_layer,
            context_id=context_id,
        )

    def daxian_frames(
        self,
        context: TemporalNatalContext,
        profile: "ResolvedZiweiCalculationProfile",
        *,
        count: int = 12,
    ) -> tuple[DaxianFrame, ...]:
        if count <= 0:
            raise ValueError("Daxian count must be positive")
        if context.bureau_number not in {2, 3, 4, 5, 6}:
            raise ValueError("bureau_number must be one of 2,3,4,5,6")
        stems = self._address_stem_map(context.address_attributes)
        direction = self._daxian_direction(context.ziwei_birth_year_stem, context.sex)
        rows: list[DaxianFrame] = []
        for index in range(count):
            frame_index = index + 1
            active = address(context.life_address.index + direction * index)
            source_stem = stems[active.index]
            nominal_age_start = context.bureau_number + index * 10
            nominal_age_end = nominal_age_start + 9
            absolute_year_start = context.ziwei_birth_year + nominal_age_start - 1
            absolute_year_end = context.ziwei_birth_year + nominal_age_end - 1
            frame_id = f"DAXIAN:index={frame_index}"
            rows.append(
                DaxianFrame(
                    frame_id=frame_id,
                    index=frame_index,
                    nominal_age_start=nominal_age_start,
                    nominal_age_end=nominal_age_end,
                    absolute_year_start=absolute_year_start,
                    absolute_year_end=absolute_year_end,
                    active_address=active,
                    active_palace_ganzhi=f"{source_stem}{active.branch}",
                    designation_overlay=self._designation_overlay(active),
                    source_stem=source_stem,
                    transformations=self._activate_transformations(
                        profile,
                        source_stem,
                        context.placements,
                        source_layer="DAXIAN",
                        context_id=frame_id,
                    ),
                    source_refs=DAXIAN_SOURCE_REFS,
                )
            )
        return tuple(rows)

    @staticmethod
    def _parent_daxian(age: int, frames: tuple[DaxianFrame, ...]) -> str | None:
        for frame in frames:
            if frame.nominal_age_start <= age <= frame.nominal_age_end:
                return frame.frame_id
        return None

    def annual_frame(
        self,
        context: TemporalNatalContext,
        profile: "ResolvedZiweiCalculationProfile",
        absolute_year: int,
        daxian_frames: tuple[DaxianFrame, ...],
    ) -> AnnualFrame:
        nominal_age = absolute_year - context.ziwei_birth_year + 1
        if nominal_age < 1:
            raise ValueError("annual year predates Ziwei birth year")
        year_stem, year_branch = sexagenary_for_year(absolute_year)
        active = address(branch_index(year_branch))
        stems = self._address_stem_map(context.address_attributes)
        active_stem = stems[active.index]
        frame_id = f"ANNUAL:{absolute_year}"
        return AnnualFrame(
            frame_id=frame_id,
            absolute_year=absolute_year,
            nominal_age=nominal_age,
            year_stem=year_stem,
            year_branch=year_branch,
            active_address=active,
            active_palace_ganzhi=f"{active_stem}{active.branch}",
            designation_overlay=self._designation_overlay(active),
            parent_daxian_frame_id=self._parent_daxian(nominal_age, daxian_frames),
            transformations=self._activate_transformations(
                profile,
                year_stem,
                context.placements,
                source_layer="ANNUAL",
                context_id=frame_id,
            ),
            source_refs=ANNUAL_SOURCE_REFS,
        )

    def annual_frames(
        self,
        context: TemporalNatalContext,
        profile: "ResolvedZiweiCalculationProfile",
        daxian_frames: tuple[DaxianFrame, ...],
        *,
        max_nominal_age: int,
    ) -> tuple[AnnualFrame, ...]:
        if max_nominal_age < 1:
            raise ValueError("max_nominal_age must be positive")
        return tuple(
            self.annual_frame(
                context,
                profile,
                context.ziwei_birth_year + nominal_age - 1,
                daxian_frames,
            )
            for nominal_age in range(1, max_nominal_age + 1)
        )

    @staticmethod
    def minor_limit_frame(context: TemporalNatalContext, nominal_age: int) -> MinorLimitFrame:
        if nominal_age < 1:
            raise ValueError("nominal_age must be positive")
        try:
            start_branch = MINOR_AGE_ONE_START_BY_YEAR_BRANCH[context.ziwei_birth_year_branch]
        except KeyError as exc:
            raise ValueError(f"unsupported birth-year branch for Minor Limit: {context.ziwei_birth_year_branch}") from exc
        direction = 1 if context.sex is Sex.MALE else -1
        active = address(branch_index(start_branch) + direction * (nominal_age - 1))
        return MinorLimitFrame(
            frame_id=f"MINOR:age={nominal_age}",
            nominal_age=nominal_age,
            active_address=active,
            source_refs=MINOR_LIMIT_SOURCE_REFS,
        )

    def generate(
        self,
        context: TemporalNatalContext,
        profile: "ResolvedZiweiCalculationProfile",
        *,
        daxian_count: int = 12,
        max_nominal_age: int | None = None,
    ) -> ZiweiTemporalState:
        if profile.temporal_rule_set_id != self.rule_set_id:
            raise TemporalGenerationError("TEMPORAL_PROFILE_RULE_SET_MISMATCH")
        if profile.temporal_rule_set_version != self.rule_set_version:
            raise TemporalGenerationError("TEMPORAL_PROFILE_RULE_SET_VERSION_MISMATCH")
        if profile.temporal_algorithm_id != self.algorithm_id or profile.temporal_algorithm_version != self.algorithm_version:
            raise TemporalGenerationError("TEMPORAL_PROFILE_ALGORITHM_MISMATCH")

        daxian = self.daxian_frames(context, profile, count=daxian_count)
        default_max_age = daxian[-1].nominal_age_end
        max_age = default_max_age if max_nominal_age is None else max_nominal_age
        annual = self.annual_frames(context, profile, daxian, max_nominal_age=max_age)
        minor = tuple(self.minor_limit_frame(context, age) for age in range(1, max_age + 1))
        direction = self._daxian_direction(context.ziwei_birth_year_stem, context.sex)
        return ZiweiTemporalState(
            rule_set_id=self.rule_set_id,
            rule_set_version=self.rule_set_version,
            algorithm_id=self.algorithm_id,
            algorithm_version=self.algorithm_version,
            daxian_direction=self._direction_name(direction),
            first_daxian_nominal_age=context.bureau_number,
            daxian_frames=daxian,
            annual_frames=annual,
            minor_limit_frames=minor,
        )
