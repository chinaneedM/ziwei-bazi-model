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
    TemporalAuxiliaryActivation,
    TemporalAuxiliaryCandidateSet,
    TransformationActivation,
)
from .registries import (
    HEAVENLY_STEMS,
    PALACE_DESIGNATIONS,
    YEAR_STEM_TO_YIN_START_STEM,
    address,
    branch_index,
    sexagenary_for_year,
    stem_index,
)
from .transformations import TransformationGenerator
from .temporal_auxiliary import TemporalAuxiliaryGenerator

if TYPE_CHECKING:
    from .profile import ResolvedZiweiCalculationProfile


TEMPORAL_ALGORITHM_ID = "ZIWEI-TEMPORAL-FRAMES-V1"
TEMPORAL_ALGORITHM_VERSION = "1.5.0"
S10_CURRENT_TEMPORAL_RULE_SET_ID = "S10_CURRENT_TEMPORAL_R1"
S10_CURRENT_TEMPORAL_RULE_SET_VERSION = "1.5.0"

DAXIAN_SOURCE_REFS = ("S10:中州派动态坐标生成补充:大限",)
ANNUAL_SOURCE_REFS = ("S10:中州派动态坐标生成补充:流年太岁与斗君",)
DOUJUN_SOURCE_REFS = (
    "S01:ZZQS-A-1935",
    "S10:ZZZA-A-1127",
    "S10:ZZZA-A-1128",
)
DOUJUN_RULE_ID = "S10-SUIJIAN-REVERSE-BIRTH-MONTH-FORWARD-BIRTH-HOUR-R1"
MONTHLY_SOURCE_REFS = (
    "S10:ZZZA-A-1123",
    "S10:ZZZA-A-1127",
    "S10:ZZZA-A-1128",
)
MONTHLY_RULE_ID = "S10-DOUJUN-FIRST-MONTH-FORWARD-TWELVE-R1"
MONTH_GANZHI_RULE_ID = "FIVE-TIGERS-YEAR-STEM-MONTH-GANZHI-R1"
REGULAR_MONTH_CALENDAR_SCOPE = "REGULAR_LUNAR_MONTH_COORDINATE"
LEAP_MONTH_POLICY_STATUS = "UNRESOLVED_NOT_GENERATED"
MINOR_LIMIT_SOURCE_REFS = ("S10:中州派动态坐标生成补充:小限",)
DAXIAN_AUXILIARY_SOURCE_REFS = ("S10:ZZTERM-TIME-04", "S10:ZZTERM-P-0125")
ANNUAL_AUXILIARY_SOURCE_REFS = ("S10:ZZQS-A-2039", "S10:ZZTERM-P-0127")
MONTHLY_AUXILIARY_SOURCE_REFS = ("S10:ZZTERM-TIME-10", "S10:ZZTERM-P-0304")

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
    natal_month_coordinate: int
    birth_hour_branch: Address

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
            natal_month_coordinate=structure.natal_month_coordinate,
            birth_hour_branch=structure.birth_hour_branch,
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
    auxiliary_activations: tuple[TemporalAuxiliaryActivation, ...]
    transformations: tuple[TransformationActivation, ...]
    source_refs: tuple[str, ...]
    auxiliary_candidate_sets: tuple[TemporalAuxiliaryCandidateSet, ...] = ()


@dataclass(frozen=True)
class AnnualFrame:
    frame_id: str
    absolute_year: int
    nominal_age: int
    year_stem: str
    year_branch: str
    active_address: Address
    active_palace_ganzhi: str
    doujun_address: Address
    doujun_rule_id: str
    designation_overlay: tuple[DesignationBinding, ...]
    parent_daxian_frame_id: str | None
    auxiliary_activations: tuple[TemporalAuxiliaryActivation, ...]
    transformations: tuple[TransformationActivation, ...]
    source_refs: tuple[str, ...]
    auxiliary_candidate_sets: tuple[TemporalAuxiliaryCandidateSet, ...] = ()


@dataclass(frozen=True)
class MonthlyFrame:
    frame_id: str
    absolute_year: int
    lunar_month: int
    month_stem: str
    month_branch: str
    month_ganzhi: str
    active_address: Address
    designation_overlay: tuple[DesignationBinding, ...]
    parent_annual_frame_id: str
    monthly_rule_id: str
    month_ganzhi_rule_id: str
    calendar_scope: str
    leap_month_policy_status: str
    auxiliary_activations: tuple[TemporalAuxiliaryActivation, ...]
    transformations: tuple[TransformationActivation, ...]
    source_refs: tuple[str, ...]
    auxiliary_candidate_sets: tuple[TemporalAuxiliaryCandidateSet, ...] = ()


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
    monthly_frames: tuple[MonthlyFrame, ...] = ()


class ZiweiTemporalEngine:
    """Generate Daxian, Annual and Minor-Limit frames without mutating natal facts."""

    rule_set_id = S10_CURRENT_TEMPORAL_RULE_SET_ID
    rule_set_version = S10_CURRENT_TEMPORAL_RULE_SET_VERSION
    algorithm_id = TEMPORAL_ALGORITHM_ID
    algorithm_version = TEMPORAL_ALGORITHM_VERSION

    def __init__(
        self,
        transformation_generator: TransformationGenerator | None = None,
        auxiliary_generator: TemporalAuxiliaryGenerator | None = None,
    ) -> None:
        self.transformations = transformation_generator or TransformationGenerator()
        self.auxiliaries = auxiliary_generator or TemporalAuxiliaryGenerator()

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
                    auxiliary_activations=self.auxiliaries.activate(
                        source_stem,
                        source_layer="DAXIAN",
                        context_id=frame_id,
                        temporal_source_refs=DAXIAN_AUXILIARY_SOURCE_REFS,
                    ),
                    transformations=self._activate_transformations(
                        profile,
                        source_stem,
                        context.placements,
                        source_layer="DAXIAN",
                        context_id=frame_id,
                    ),
                    source_refs=DAXIAN_SOURCE_REFS,
                    auxiliary_candidate_sets=(
                        self.auxiliaries.kui_yue_candidate_set(
                            source_stem,
                            source_layer="DAXIAN",
                            context_id=frame_id,
                            temporal_source_refs=DAXIAN_AUXILIARY_SOURCE_REFS,
                        ),
                    ),
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
        doujun = self.doujun_address(context, year_branch)
        frame_id = f"ANNUAL:{absolute_year}"
        return AnnualFrame(
            frame_id=frame_id,
            absolute_year=absolute_year,
            nominal_age=nominal_age,
            year_stem=year_stem,
            year_branch=year_branch,
            active_address=active,
            active_palace_ganzhi=f"{active_stem}{active.branch}",
            doujun_address=doujun,
            doujun_rule_id=DOUJUN_RULE_ID,
            designation_overlay=self._designation_overlay(active),
            parent_daxian_frame_id=self._parent_daxian(nominal_age, daxian_frames),
            auxiliary_activations=self.auxiliaries.activate(
                year_stem,
                source_layer="ANNUAL",
                context_id=frame_id,
                temporal_source_refs=ANNUAL_AUXILIARY_SOURCE_REFS,
            ),
            transformations=self._activate_transformations(
                profile,
                year_stem,
                context.placements,
                source_layer="ANNUAL",
                context_id=frame_id,
            ),
            source_refs=ANNUAL_SOURCE_REFS + DOUJUN_SOURCE_REFS,
            auxiliary_candidate_sets=(
                self.auxiliaries.kui_yue_candidate_set(
                    year_stem,
                    source_layer="ANNUAL",
                    context_id=frame_id,
                    temporal_source_refs=ANNUAL_AUXILIARY_SOURCE_REFS,
                ),
            ),
        )

    @staticmethod
    def doujun_address(context: TemporalNatalContext, annual_branch: str) -> Address:
        """Return the annual 正月 address without interpreting its quality.

        流年岁建起正月，逆数至本生月，再从该宫起子顺数至本生时。
        Both counts are inclusive, hence their zero-based offsets are month-1
        and the birth-hour branch index respectively.
        """

        if not 1 <= context.natal_month_coordinate <= 12:
            raise ValueError("natal_month_coordinate must be in [1, 12]")
        return address(
            branch_index(annual_branch)
            - (context.natal_month_coordinate - 1)
            + context.birth_hour_branch.index
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
    def month_ganzhi(year_stem: str, lunar_month: int) -> tuple[str, str]:
        """Return a regular lunar month's Ganzhi by the Five-Tigers rule."""

        if not 1 <= lunar_month <= 12:
            raise ValueError("lunar_month must be in [1, 12]")
        try:
            first_month_stem = YEAR_STEM_TO_YIN_START_STEM[year_stem]
        except KeyError as exc:
            raise ValueError(f"unsupported year stem: {year_stem}") from exc
        month_stem = HEAVENLY_STEMS[(stem_index(first_month_stem) + lunar_month - 1) % 10]
        month_branch = address(2 + lunar_month - 1).branch
        return month_stem, month_branch

    def monthly_frame(
        self,
        context: TemporalNatalContext,
        profile: "ResolvedZiweiCalculationProfile",
        annual: AnnualFrame,
        lunar_month: int,
    ) -> MonthlyFrame:
        month_stem, month_branch = self.month_ganzhi(annual.year_stem, lunar_month)
        active = address(annual.doujun_address.index + lunar_month - 1)
        frame_id = f"MONTH:{annual.absolute_year}:{lunar_month}"
        return MonthlyFrame(
            frame_id=frame_id,
            absolute_year=annual.absolute_year,
            lunar_month=lunar_month,
            month_stem=month_stem,
            month_branch=month_branch,
            month_ganzhi=f"{month_stem}{month_branch}",
            active_address=active,
            designation_overlay=self._designation_overlay(active),
            parent_annual_frame_id=annual.frame_id,
            monthly_rule_id=MONTHLY_RULE_ID,
            month_ganzhi_rule_id=MONTH_GANZHI_RULE_ID,
            calendar_scope=REGULAR_MONTH_CALENDAR_SCOPE,
            leap_month_policy_status=LEAP_MONTH_POLICY_STATUS,
            auxiliary_activations=self.auxiliaries.activate(
                month_stem,
                source_layer="MONTH",
                context_id=frame_id,
                temporal_source_refs=MONTHLY_AUXILIARY_SOURCE_REFS,
            ),
            transformations=self._activate_transformations(
                profile,
                month_stem,
                context.placements,
                source_layer="MONTH",
                context_id=frame_id,
            ),
            source_refs=MONTHLY_SOURCE_REFS,
            auxiliary_candidate_sets=(
                self.auxiliaries.kui_yue_candidate_set(
                    month_stem,
                    source_layer="MONTH",
                    context_id=frame_id,
                    temporal_source_refs=MONTHLY_AUXILIARY_SOURCE_REFS,
                ),
            ),
        )

    def monthly_frames(
        self,
        context: TemporalNatalContext,
        profile: "ResolvedZiweiCalculationProfile",
        annual_frames: tuple[AnnualFrame, ...],
    ) -> tuple[MonthlyFrame, ...]:
        return tuple(
            self.monthly_frame(context, profile, annual, lunar_month)
            for annual in annual_frames
            for lunar_month in range(1, 13)
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
        monthly_years: tuple[int, ...] = (),
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
        if len(monthly_years) != len(set(monthly_years)):
            raise ValueError("monthly_years must be unique")
        annual_by_year = {frame.absolute_year: frame for frame in annual}
        try:
            selected_annual = tuple(annual_by_year[year] for year in monthly_years)
        except KeyError as exc:
            raise ValueError(f"monthly year is outside generated annual range: {exc.args[0]}") from exc
        monthly = self.monthly_frames(context, profile, selected_annual)
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
            monthly_frames=monthly,
            minor_limit_frames=minor,
        )
