from __future__ import annotations

from datetime import date, datetime, timedelta

from fortune_training.calendar_foundation import five_rats_hour_pillar
from fortune_training.util import object_sha256

from .registries import EARTHLY_BRANCHES, branch_index


ZIWEI_TEMPORAL_HISTORICAL_CANDIDATE_API_ID = (
    "ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-API-R1"
)
ZIWEI_TEMPORAL_HISTORICAL_CANDIDATE_API_VERSION = "1.1.0"
TEMPORAL_HISTORICAL_CANDIDATE_SELECTION_STATUS = "PRESERVED_NOT_SELECTED"

JIELAN_1581_DAY_ANCHORED_FLOW_HOUR_METHOD_ID = (
    "JIELAN-1581-DAY-ANCHORED-FLOW-HOUR-R1"
)
JIELAN_1581_DAY_ANCHORED_FLOW_HOUR_SOURCE_ID = "EXT-ZIWEI-JIELAN-1581"
JIELAN_1581_DAY_ANCHORED_FLOW_HOUR_SOURCE_REFS = (
    "EXT-ZIWEI-JIELAN-1581:CH54:安流年斗君法",
)
JIELAN_1581_DAY_ANCHORED_FLOW_HOUR_AUTHORITY_STATUS = (
    "EARLY_PRINT_DAY_ANCHORED_FLOW_HOUR_GEOMETRY_ONLY"
)

ZHONGZHOU_LEAP_MONTH_HALF_SPLIT_METHOD_ID = (
    "ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1"
)
ZHONGZHOU_LEAP_MONTH_HALF_SPLIT_SOURCE_ID = "EXT-WANGTINGZHI-ZHONGZHOU-CHUJI"
ZHONGZHOU_LEAP_MONTH_HALF_SPLIT_SOURCE_REFS = (
    "EXT-WANGTINGZHI-ZHONGZHOU-CHUJI",
    "S10:ZZTERM-P-0274",
    "S10:ZZTERM-P-0280",
    "S10:ZZTERM-P-0281",
)
ZHONGZHOU_LEAP_MONTH_HALF_SPLIT_AUTHORITY_STATUS = (
    "SOURCE_CLOSED_MODERN_ZHONGZHOU_SCHOOL_METHOD"
)

_SUPPORTED_TIME_STANDARDS = frozenset(
    {
        "ZHONGZHOU_LUOYANG_MEAN_SOLAR_TIME",
        "LOCAL_APPARENT_SOLAR_TIME",
    }
)
_SUPPORTED_DAY_BOUNDARIES = frozenset({"MIDNIGHT", "ZI_START_23"})
_SUPPORTED_CALENDAR_DATE_POLICIES = frozenset(
    {"LOCAL_SOLAR_DATE_INDEXED", "ABSOLUTE_CALENDAR"}
)


def _advance_branch(start_branch: str, offset: int) -> str:
    return EARTHLY_BRANCHES[(branch_index(start_branch) + offset) % 12]


def _effective_gregorian_date(
    local_datetime: datetime,
    reported_civil_date: date,
    ziwei_calendar_date_policy: str,
    ziwei_day_boundary_policy: str,
) -> date:
    if local_datetime.tzinfo is not None:
        raise ValueError("source_local_datetime must be a naive local clock reading")
    if ziwei_calendar_date_policy not in _SUPPORTED_CALENDAR_DATE_POLICIES:
        raise ValueError(
            f"unsupported Ziwei calendar-date policy: {ziwei_calendar_date_policy}"
        )
    if ziwei_day_boundary_policy not in _SUPPORTED_DAY_BOUNDARIES:
        raise ValueError(
            f"unsupported Ziwei day-boundary policy: {ziwei_day_boundary_policy}"
        )
    effective = (
        local_datetime.date()
        if ziwei_calendar_date_policy == "LOCAL_SOLAR_DATE_INDEXED"
        else reported_civil_date
    )
    if ziwei_day_boundary_policy == "ZI_START_23" and local_datetime.hour == 23:
        effective = local_datetime.date() + timedelta(days=1)
    return effective


def resolve_jielan_1581_day_anchored_flow_hour_candidate(
    *,
    parent_daily_frame_id: str,
    parent_daily_effective_gregorian_date: date,
    parent_daily_active_branch: str,
    source_local_datetime: datetime,
    reported_civil_date: date,
    ziwei_calendar_date_policy: str,
    ziwei_day_boundary_policy: str,
    time_standard: str,
) -> dict[str, object]:
    """Resolve the 1581 day-anchored flow-hour geometry without selecting it.

    The caller must supply the daily parent resolved under the same time-standard
    clock and Ziwei day-boundary policy. A mismatched parent date is rejected
    instead of silently reusing one daily palace across orthogonal time standards.

    This resolver intentionally does not project Zhongzhou dynamic auxiliaries or
    transformation tables into the 1581 candidate.
    """

    if not parent_daily_frame_id:
        raise ValueError("parent_daily_frame_id must be non-empty")
    branch_index(parent_daily_active_branch)
    if time_standard not in _SUPPORTED_TIME_STANDARDS:
        raise ValueError(f"unsupported time standard: {time_standard}")

    effective_date = _effective_gregorian_date(
        source_local_datetime,
        reported_civil_date,
        ziwei_calendar_date_policy,
        ziwei_day_boundary_policy,
    )
    if parent_daily_effective_gregorian_date != effective_date:
        raise ValueError(
            "parent daily frame date does not match the supplied time-standard clock"
        )

    hour_ganzhi = five_rats_hour_pillar(source_local_datetime, effective_date)
    hour_branch = hour_ganzhi[1]
    active_branch = _advance_branch(
        parent_daily_active_branch,
        branch_index(hour_branch),
    )

    payload: dict[str, object] = {
        "schema": "ZIWEI-JIELAN-1581-DAY-ANCHORED-FLOW-HOUR-CANDIDATE-R1",
        "api_id": ZIWEI_TEMPORAL_HISTORICAL_CANDIDATE_API_ID,
        "api_version": ZIWEI_TEMPORAL_HISTORICAL_CANDIDATE_API_VERSION,
        "method_id": JIELAN_1581_DAY_ANCHORED_FLOW_HOUR_METHOD_ID,
        "selection_status": TEMPORAL_HISTORICAL_CANDIDATE_SELECTION_STATUS,
        "source_id": JIELAN_1581_DAY_ANCHORED_FLOW_HOUR_SOURCE_ID,
        "source_refs": JIELAN_1581_DAY_ANCHORED_FLOW_HOUR_SOURCE_REFS,
        "authority_status": JIELAN_1581_DAY_ANCHORED_FLOW_HOUR_AUTHORITY_STATUS,
        "time_standard": time_standard,
        "time_standard_authority": "ORTHOGONAL_INPUT_NOT_AUTHORIZED_BY_JIELAN_1581",
        "source_local_datetime": source_local_datetime.isoformat(),
        "reported_civil_date": reported_civil_date.isoformat(),
        "ziwei_calendar_date_policy": ziwei_calendar_date_policy,
        "ziwei_day_boundary_policy": ziwei_day_boundary_policy,
        "effective_gregorian_date": effective_date.isoformat(),
        "parent_daily_frame_id": parent_daily_frame_id,
        "parent_daily_effective_gregorian_date": (
            parent_daily_effective_gregorian_date.isoformat()
        ),
        "parent_daily_active_branch": parent_daily_active_branch,
        "hour_branch": hour_branch,
        "hour_ganzhi": hour_ganzhi,
        "active_address_branch": active_branch,
        "mechanics": {
            "zi_hour_anchor": "PARENT_DAILY_ACTIVE_ADDRESS",
            "later_hours": "FORWARD_BY_HOUR_BRANCH_ORDINAL_FROM_ZI",
        },
        "downstream_cross_school_projection_status": (
            "NOT_APPLIED_BY_THIS_SOURCE_SCOPED_GEOMETRY_API"
        ),
    }
    return {
        **payload,
        "candidate_hash": object_sha256(payload),
    }


def resolve_zhongzhou_leap_month_half_split_candidate(
    *,
    leap_lunar_year: int,
    leap_lunar_month: int,
    leap_lunar_day: int,
    previous_month_temporal_year: int,
    previous_month_number: int,
    previous_month_frame_id: str,
    previous_month_ganzhi: str,
    previous_month_active_branch: str,
    following_month_temporal_year: int,
    following_month_number: int,
    following_month_frame_id: str,
    following_month_ganzhi: str,
    following_month_active_branch: str,
) -> dict[str, object]:
    """Resolve Zhongzhou leap-month assignment without inventing day geometry.

    S10:ZZTERM-P-0280 closes the half split and the no-reset-at-half-split
    constraint. It does not by itself close the leap-month day-one origin.
    Therefore this API records month assignment and continuity semantics while
    deliberately emitting no derived leap-month daily active palace.
    """

    if leap_lunar_year < 1:
        raise ValueError("leap_lunar_year must be positive")
    if not 1 <= leap_lunar_month <= 12:
        raise ValueError("leap_lunar_month must be in [1, 12]")
    if not 1 <= leap_lunar_day <= 30:
        raise ValueError("leap_lunar_day must be in [1, 30]")
    if previous_month_temporal_year < 1:
        raise ValueError("previous-month temporal year must be positive")
    if previous_month_number != leap_lunar_month:
        raise ValueError("previous-month number must equal leap lunar month")

    expected_following_month = 1 if leap_lunar_month == 12 else leap_lunar_month + 1
    expected_following_year = (
        previous_month_temporal_year + 1 if leap_lunar_month == 12 else previous_month_temporal_year
    )
    if (
        following_month_number != expected_following_month
        or following_month_temporal_year != expected_following_year
    ):
        raise ValueError("following regular month is not the immediate successor")

    for frame_id in (previous_month_frame_id, following_month_frame_id):
        if not frame_id:
            raise ValueError("month frame ids must be non-empty")
    for ganzhi in (previous_month_ganzhi, following_month_ganzhi):
        if len(ganzhi) != 2:
            raise ValueError("month Ganzhi must be two characters")
    branch_index(previous_month_active_branch)
    branch_index(following_month_active_branch)

    if leap_lunar_day <= 15:
        segment = "PREVIOUS_MONTH"
        assigned = {
            "temporal_year": previous_month_temporal_year,
            "month": previous_month_number,
            "frame_id": previous_month_frame_id,
            "ganzhi": previous_month_ganzhi,
            "active_address_branch": previous_month_active_branch,
        }
    else:
        segment = "FOLLOWING_MONTH"
        assigned = {
            "temporal_year": following_month_temporal_year,
            "month": following_month_number,
            "frame_id": following_month_frame_id,
            "ganzhi": following_month_ganzhi,
            "active_address_branch": following_month_active_branch,
        }

    payload: dict[str, object] = {
        "schema": "ZIWEI-ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-CANDIDATE-R1",
        "api_id": ZIWEI_TEMPORAL_HISTORICAL_CANDIDATE_API_ID,
        "api_version": ZIWEI_TEMPORAL_HISTORICAL_CANDIDATE_API_VERSION,
        "method_id": ZHONGZHOU_LEAP_MONTH_HALF_SPLIT_METHOD_ID,
        "selection_status": TEMPORAL_HISTORICAL_CANDIDATE_SELECTION_STATUS,
        "source_id": ZHONGZHOU_LEAP_MONTH_HALF_SPLIT_SOURCE_ID,
        "source_refs": ZHONGZHOU_LEAP_MONTH_HALF_SPLIT_SOURCE_REFS,
        "authority_status": ZHONGZHOU_LEAP_MONTH_HALF_SPLIT_AUTHORITY_STATUS,
        "leap_lunar_year": leap_lunar_year,
        "leap_lunar_month": leap_lunar_month,
        "leap_lunar_day": leap_lunar_day,
        "segment": segment,
        "assigned_regular_month": assigned,
        "previous_regular_month": {
            "temporal_year": previous_month_temporal_year,
            "month": previous_month_number,
            "frame_id": previous_month_frame_id,
            "ganzhi": previous_month_ganzhi,
            "active_address_branch": previous_month_active_branch,
        },
        "following_regular_month": {
            "temporal_year": following_month_temporal_year,
            "month": following_month_number,
            "frame_id": following_month_frame_id,
            "ganzhi": following_month_ganzhi,
            "active_address_branch": following_month_active_branch,
        },
        "flow_day_continuity": {
            "half_split_reset": False,
            "direction": "FORWARD_CONTINUOUS",
            "daily_active_address_emitted": False,
            "daily_origin_semantics": "NOT_CLOSED_BY_THIS_MONTH_POLICY_API",
        },
        "downstream_projection_status": (
            "MONTH_ASSIGNMENT_CANDIDATE_ONLY_DAILY_GEOMETRY_REMAINS_FAIL_CLOSED"
        ),
    }
    return {
        **payload,
        "candidate_hash": object_sha256(payload),
    }
