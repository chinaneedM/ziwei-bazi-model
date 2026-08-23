from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import TYPE_CHECKING

from fortune_training.calendar_foundation import (
    five_rats_hour_pillar,
    sexagenary_day_pillar,
)

from .models import Address, Placement, TransformationActivation
from .registries import address
from .temporal import MonthlyFrame
from .transformations import TransformationGenerator

if TYPE_CHECKING:
    from .profile import ResolvedZiweiCalculationProfile


ZIWEI_TARGET_DAILY_HOURLY_ALGORITHM_ID = "ZIWEI-TARGET-DAILY-HOURLY-R1"
ZIWEI_TARGET_DAILY_HOURLY_ALGORITHM_VERSION = "1.1.0"

DAILY_RULE_ID = "S10-FLOW-MONTH-FIRST-DAY-FORWARD-R1"
DAILY_SOURCE_REFS = ("S10:ZZTERM-P-0274", "S10:ZZTERM-P-0275", "S10:ZZTERM-P-0277")
HOURLY_RULE_ID = "S10-CASE-FIVE-RATS-HOUR-CANDIDATE-R1"
HOURLY_SOURCE_REFS = ("S10:ZZTERM-P-0316", "S10:ZZTERM-P-0317")
TIME_STANDARD_CONFLICT_REF = "S01:ZZZA-CF-002"
ZI_HOUR_DATE_CONFLICT_REF = "S01:ZZZA-CF-001"
LUOYANG_TIME_SOURCE_REFS = ("S01:ZZZA-PR-004", "S01:ZZZA-A-0027")
LUOYANG_LONGITUDE_DEGREES = 112 + 26 / 60
DAILY_TRANSFORMATION_SOURCE_REFS = (
    "S10:ZZTERM-P-0277",
    "S10:ZZTERM-P-0278",
    "S01:ZZZA-CF-008",
)
HOURLY_TRANSFORMATION_SOURCE_REFS = (
    "S10:ZZTERM-P-0317",
    "S01:ZZZA-CF-008",
)


@dataclass(frozen=True)
class ZiweiTargetDailyFrame:
    frame_id: str
    parent_monthly_frame_id: str
    effective_gregorian_date: date
    effective_lunar_day: int
    day_ganzhi: str
    active_address: Address
    transformation_status: str
    transformation_rule_set_id: str | None
    transformation_rule_set_version: str | None
    transformations: tuple[TransformationActivation, ...]
    transformation_source_refs: tuple[str, ...]
    rule_id: str = DAILY_RULE_ID
    source_refs: tuple[str, ...] = DAILY_SOURCE_REFS


@dataclass(frozen=True)
class ZiweiTargetHourlyMethodCandidate:
    candidate_id: str
    time_standard: str
    source_local_datetime: datetime
    ziwei_day_boundary_policy: str
    effective_gregorian_date: date
    day_ganzhi: str
    hour_branch: str
    hour_ganzhi: str
    frame_status: str
    active_address: Address | None
    transformation_status: str
    transformation_rule_set_id: str | None
    transformation_rule_set_version: str | None
    transformations: tuple[TransformationActivation, ...]
    transformation_source_refs: tuple[str, ...]
    rule_id: str = HOURLY_RULE_ID
    authority_status: str = "CASE_METHOD_ONLY_NOT_GLOBAL_RULE"
    source_refs: tuple[str, ...] = (
        HOURLY_SOURCE_REFS
        + LUOYANG_TIME_SOURCE_REFS
        + (TIME_STANDARD_CONFLICT_REF, ZI_HOUR_DATE_CONFLICT_REF)
    )


class ZiweiTargetTemporalEngine:
    """Build source-bounded target daily facts and non-selected hourly candidates."""

    algorithm_id = ZIWEI_TARGET_DAILY_HOURLY_ALGORITHM_ID
    algorithm_version = ZIWEI_TARGET_DAILY_HOURLY_ALGORITHM_VERSION

    def __init__(self, transformation_generator: TransformationGenerator | None = None) -> None:
        self.transformations = transformation_generator or TransformationGenerator()

    def _activate_transformations(
        self,
        profile: "ResolvedZiweiCalculationProfile",
        placements: tuple[Placement, ...],
        source_stem: str,
        *,
        source_layer: str,
        context_id: str,
    ) -> tuple[str, tuple[TransformationActivation, ...]]:
        if profile.transformation_rule_set_id is None:
            return "PROFILE_TRANSFORMATIONS_DISABLED", ()
        if (
            profile.transformation_rule_set_id != self.transformations.rule_set_id
            or profile.transformation_rule_set_version != self.transformations.rule_set_version
        ):
            raise ValueError("unsupported Ziwei target transformation rule-set binding")
        return (
            "PROFILE_RULE_SET_RESOLVED",
            self.transformations.activate(
                source_stem,
                placements,
                source_layer=source_layer,
                context_id=context_id,
            ),
        )

    @staticmethod
    def effective_gregorian_date(
        local_datetime: datetime,
        ziwei_day_boundary_policy: str,
    ) -> date:
        if local_datetime.tzinfo is not None:
            raise ValueError("local_datetime must be a naive local clock reading")
        if ziwei_day_boundary_policy not in {"MIDNIGHT", "ZI_START_23"}:
            raise ValueError(f"unsupported Ziwei day-boundary policy: {ziwei_day_boundary_policy}")
        effective = local_datetime.date()
        if ziwei_day_boundary_policy == "ZI_START_23" and local_datetime.hour == 23:
            effective += timedelta(days=1)
        return effective

    def daily_frame(
        self,
        monthly_frame: MonthlyFrame,
        *,
        effective_gregorian_date: date,
        effective_lunar_day: int,
        profile: "ResolvedZiweiCalculationProfile",
        placements: tuple[Placement, ...],
    ) -> ZiweiTargetDailyFrame:
        if not 1 <= effective_lunar_day <= 30:
            raise ValueError("effective_lunar_day must be in [1, 30]")
        active = address(monthly_frame.active_address.index + effective_lunar_day - 1)
        frame_id = f"DAY:{effective_gregorian_date.isoformat()}"
        day_ganzhi = sexagenary_day_pillar(effective_gregorian_date)
        transformation_status, transformations = self._activate_transformations(
            profile,
            placements,
            day_ganzhi[0],
            source_layer="DAY",
            context_id=frame_id,
        )
        return ZiweiTargetDailyFrame(
            frame_id=frame_id,
            parent_monthly_frame_id=monthly_frame.frame_id,
            effective_gregorian_date=effective_gregorian_date,
            effective_lunar_day=effective_lunar_day,
            day_ganzhi=day_ganzhi,
            active_address=active,
            transformation_status=transformation_status,
            transformation_rule_set_id=profile.transformation_rule_set_id,
            transformation_rule_set_version=profile.transformation_rule_set_version,
            transformations=transformations,
            transformation_source_refs=DAILY_TRANSFORMATION_SOURCE_REFS,
        )

    def hourly_method_candidates(
        self,
        *,
        target_utc: datetime,
        local_apparent_solar_datetime: datetime,
        ziwei_day_boundary_policy: str,
        profile: "ResolvedZiweiCalculationProfile",
        placements: tuple[Placement, ...],
    ) -> tuple[ZiweiTargetHourlyMethodCandidate, ...]:
        if target_utc.tzinfo is None or target_utc.utcoffset() is None:
            raise ValueError("target_utc must be timezone-aware")
        luoyang_mean_solar_datetime = (
            target_utc.astimezone(timezone.utc).replace(tzinfo=None)
            + timedelta(seconds=LUOYANG_LONGITUDE_DEGREES * 240)
        )
        rows: list[ZiweiTargetHourlyMethodCandidate] = []
        for time_standard, local_datetime in (
            ("ZHONGZHOU_LUOYANG_MEAN_SOLAR_TIME", luoyang_mean_solar_datetime),
            ("LOCAL_APPARENT_SOLAR_TIME", local_apparent_solar_datetime),
        ):
            effective_date = self.effective_gregorian_date(
                local_datetime,
                ziwei_day_boundary_policy,
            )
            hour_ganzhi = five_rats_hour_pillar(local_datetime, effective_date)
            candidate_id = f"{HOURLY_RULE_ID}:{time_standard}"
            transformation_status, transformations = self._activate_transformations(
                profile,
                placements,
                hour_ganzhi[0],
                source_layer="HOUR_CANDIDATE",
                context_id=candidate_id,
            )
            rows.append(
                ZiweiTargetHourlyMethodCandidate(
                    candidate_id=candidate_id,
                    time_standard=time_standard,
                    source_local_datetime=local_datetime,
                    ziwei_day_boundary_policy=ziwei_day_boundary_policy,
                    effective_gregorian_date=effective_date,
                    day_ganzhi=sexagenary_day_pillar(effective_date),
                    hour_branch=hour_ganzhi[1],
                    hour_ganzhi=hour_ganzhi,
                    frame_status="ACTIVE_ADDRESS_NOT_GENERATED_CASE_METHOD_ONLY",
                    active_address=None,
                    transformation_status=(
                        "CASE_METHOD_" + transformation_status
                    ),
                    transformation_rule_set_id=profile.transformation_rule_set_id,
                    transformation_rule_set_version=profile.transformation_rule_set_version,
                    transformations=transformations,
                    transformation_source_refs=HOURLY_TRANSFORMATION_SOURCE_REFS,
                    source_refs=(
                        HOURLY_SOURCE_REFS
                        + LUOYANG_TIME_SOURCE_REFS
                        + (TIME_STANDARD_CONFLICT_REF, ZI_HOUR_DATE_CONFLICT_REF)
                    ),
                )
            )
        return tuple(rows)
