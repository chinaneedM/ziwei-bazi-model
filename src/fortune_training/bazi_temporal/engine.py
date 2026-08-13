from __future__ import annotations

from calendar import monthrange
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate, SEXAGENARY_CYCLE, sexagenary_index
from fortune_training.bazi_chart.registries import STEM_POLARITY
from fortune_training.calendar_foundation import SolarTermEngine
from fortune_training.calendar_foundation.models import json_value

from .models import (
    BaziDayunState,
    BaziSex,
    BaziTemporalCandidate,
    BaziTemporalResolution,
    DayunDirectionResolution,
    DayunFrame,
    JiaoyunResolution,
    PreDayunFrame,
    SymbolicLuckAge,
)
from .profile import (
    ANCHOR_RULE_SET_ID,
    ANCHOR_RULE_SET_VERSION,
    DAYUN_SEQUENCE_RULE_SET_ID,
    DAYUN_SEQUENCE_RULE_SET_VERSION,
    DIRECTION_RULE_SET_ID,
    DIRECTION_RULE_SET_VERSION,
    SYMBOLIC_AGE_RULE_SET_ID,
    SYMBOLIC_AGE_RULE_SET_VERSION,
    CONTINUOUS_CALENDAR_REALIZATION_RULE_SET,
    CONTINUOUS_DAYUN_BOUNDARY_RULE_SET,
    CONTINUOUS_INTERVAL_COORDINATE_POLICY,
    ResolvedBaziTemporalProfile,
    WENZHEN_CALENDAR_REALIZATION_RULE_SET,
    WENZHEN_DAYUN_BOUNDARY_RULE_SET,
    WENZHEN_INTERVAL_COORDINATE_POLICY,
)


DAY_MICROSECONDS = 86_400_000_000
SYMBOLIC_YEAR_MICROSECONDS = 360 * DAY_MICROSECONDS
SYMBOLIC_MONTH_MICROSECONDS = 30 * DAY_MICROSECONDS
CHINA_STANDARD_TIME = timezone(timedelta(hours=8), name="UTC+08:00")
WENZHEN_MIXED_CLOCK_ANCHOR_RESELECTION_REF = (
    "ENGINEERING:WENZHEN_MIXED_CLOCK_JIE_ANCHOR_RESELECTION_R1"
)


class BaziTemporalGenerationError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziTemporalRequest:
    candidate: BaziChartCandidate
    sex: BaziSex
    profile: ResolvedBaziTemporalProfile
    dayun_count: int = 12


def _timedelta_microseconds(value: timedelta) -> int:
    return (
        value.days * DAY_MICROSECONDS
        + value.seconds * 1_000_000
        + value.microseconds
    )


def _add_gregorian_years_utc(value: datetime, years: int) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Dayun boundary datetime must be timezone-aware")
    value = value.astimezone(timezone.utc)
    target_year = value.year + years
    try:
        return value.replace(year=target_year)
    except ValueError:
        # Operational rule for a Feb-29 anniversary in a non-leap target year.
        if value.month == 2 and value.day == 29:
            return value.replace(year=target_year, day=28)
        raise


def _add_calendar_months_clamped(value: datetime, months: int) -> datetime:
    """Add one combined month displacement, clamping only at the destination."""

    absolute_month = value.year * 12 + (value.month - 1) + months
    target_year, target_month_zero = divmod(absolute_month, 12)
    target_month = target_month_zero + 1
    target_day = min(value.day, monthrange(target_year, target_month)[1])
    return value.replace(year=target_year, month=target_month, day=target_day)


def realize_wenzhen_calendar_month_displacement_utc(
    birth_utc: datetime,
    symbolic_age: SymbolicLuckAge,
) -> datetime:
    """Realize Wenzhen R1 symbolic components on a fixed China clock.

    Years and months are first unified into one month displacement.  Days and
    the sub-day residual are applied afterwards.  The returned microsecond is
    an engine realization; A7--A11 do not certify it as Wenzhen UI truth.
    """

    if birth_utc.tzinfo is None or birth_utc.utcoffset() is None:
        raise ValueError("Wenzhen calendar realization birth must be timezone-aware")
    china_birth = birth_utc.astimezone(CHINA_STANDARD_TIME)
    month_displacement = symbolic_age.years_360 * 12 + symbolic_age.months_30
    displaced = _add_calendar_months_clamped(china_birth, month_displacement)
    realized = displaced + timedelta(
        days=symbolic_age.days,
        microseconds=symbolic_age.residual_microseconds,
    )
    return realized.astimezone(timezone.utc)


def _dayun_anniversary(
    value: datetime,
    years: int,
    profile: ResolvedBaziTemporalProfile,
) -> datetime:
    if profile.dayun_boundary_rule_set == CONTINUOUS_DAYUN_BOUNDARY_RULE_SET:
        return _add_gregorian_years_utc(value, years)
    if profile.dayun_boundary_rule_set == WENZHEN_DAYUN_BOUNDARY_RULE_SET:
        china_value = value.astimezone(CHINA_STANDARD_TIME)
        target_year = china_value.year + years
        try:
            realized = china_value.replace(year=target_year)
        except ValueError:
            if china_value.month != 2 or china_value.day != 29:
                raise
            realized = china_value.replace(year=target_year, day=28)
        return realized.astimezone(timezone.utc)
    raise ValueError(f"unsupported Dayun boundary rule: {profile.dayun_boundary_rule_set}")


def _wenzhen_mixed_clock_delta(seed, anchor: datetime, direction: str) -> timedelta:
    birth_clock = seed.local_apparent_solar_datetime.replace(tzinfo=None)
    jie_china_clock = anchor.astimezone(CHINA_STANDARD_TIME).replace(tzinfo=None)
    return (
        jie_china_clock - birth_clock
        if direction == "FORWARD"
        else birth_clock - jie_china_clock
    )


def _select_jiaoyun_anchor(
    seed,
    direction: DayunDirectionResolution,
    profile: ResolvedBaziTemporalProfile,
) -> tuple[str, str, datetime, timedelta, bool]:
    """Select the Jiaoyun Jie in the interval profile's own ordering coordinate.

    Shared Time/Calendar seeds deliberately carry UTC-adjacent Jie boundaries.
    That ordering is already correct for the continuous profile.  The Wenzhen
    compatibility profile compares a birthplace apparent-solar wall clock to a
    China-standard Jie wall clock; immediately around a Jie, that mixed-clock
    ordering can be the opposite of UTC ordering.  Only in that compatibility
    profile, step one Jie when the upstream UTC-adjacent candidate falls on the
    wrong side of the declared interval coordinate.
    """

    birth = seed.birth_utc.astimezone(timezone.utc)
    if direction.direction == "FORWARD":
        anchor_kind = "NEXT_JIE"
        anchor_name = seed.next_jie_name
        anchor = seed.next_jie_utc.astimezone(timezone.utc)
    else:
        anchor_kind = "PREVIOUS_JIE"
        anchor_name = seed.previous_jie_name
        anchor = seed.previous_jie_utc.astimezone(timezone.utc)

    if profile.interval_coordinate_policy == CONTINUOUS_INTERVAL_COORDINATE_POLICY:
        delta = anchor - birth if direction.direction == "FORWARD" else birth - anchor
        return anchor_kind, anchor_name, anchor, delta, False

    if profile.interval_coordinate_policy != WENZHEN_INTERVAL_COORDINATE_POLICY:
        raise BaziTemporalGenerationError(
            "UNSUPPORTED_INTERVAL_COORDINATE_POLICY",
            profile.interval_coordinate_policy,
        )

    delta = _wenzhen_mixed_clock_delta(seed, anchor, direction.direction)
    if _timedelta_microseconds(delta) >= 0:
        return anchor_kind, anchor_name, anchor, delta, False

    solar_terms = SolarTermEngine()
    if direction.direction == "FORWARD":
        _, replacement = solar_terms.adjacent_terms(anchor, jie_only=True)
    else:
        replacement, _ = solar_terms.adjacent_terms(
            anchor - timedelta(microseconds=1),
            jie_only=True,
        )
    anchor_name = replacement.name
    anchor = replacement.utc_instant.astimezone(timezone.utc)
    delta = _wenzhen_mixed_clock_delta(seed, anchor, direction.direction)
    return anchor_kind, anchor_name, anchor, delta, True


class BaziTemporalEngine:
    schema = "BAZI-TEMPORAL-RESULT-V1"
    typed_schema = "BAZI-TEMPORAL-TYPED-RESOLUTION-V1"

    @staticmethod
    def resolve_direction(candidate: BaziChartCandidate, sex: BaziSex) -> DayunDirectionResolution:
        year_stems = [row for row in candidate.chart.stems if row.position == "YEAR"]
        if len(year_stems) != 1:
            raise BaziTemporalGenerationError("INVALID_YEAR_STEM", "expected exactly one YEAR stem")
        year_stem = year_stems[0].stem
        polarity = STEM_POLARITY[year_stem]
        forward = (
            polarity == "YANG" and sex is BaziSex.MALE
        ) or (
            polarity == "YIN" and sex is BaziSex.FEMALE
        )
        return DayunDirectionResolution(
            direction="FORWARD" if forward else "REVERSE",
            year_stem=year_stem,
            year_stem_polarity=polarity,
            sex=sex,
            rule_set_id=DIRECTION_RULE_SET_ID,
            rule_set_version=DIRECTION_RULE_SET_VERSION,
            source_refs=("S15",),
        )

    @staticmethod
    def _symbolic_age(raw_interval_microseconds: int) -> SymbolicLuckAge:
        if raw_interval_microseconds < 0:
            raise ValueError("raw Dayun interval must be non-negative")
        total = raw_interval_microseconds * 120
        years, remainder = divmod(total, SYMBOLIC_YEAR_MICROSECONDS)
        months, remainder = divmod(remainder, SYMBOLIC_MONTH_MICROSECONDS)
        days, residual = divmod(remainder, DAY_MICROSECONDS)
        return SymbolicLuckAge(
            total_symbolic_microseconds=total,
            years_360=years,
            months_30=months,
            days=days,
            residual_microseconds=residual,
            rule_set_id=SYMBOLIC_AGE_RULE_SET_ID,
            rule_set_version=SYMBOLIC_AGE_RULE_SET_VERSION,
            source_refs=("S15",),
        )

    @classmethod
    def _jiaoyun_for_seed(
        cls,
        seed,
        direction: DayunDirectionResolution,
        profile: ResolvedBaziTemporalProfile,
    ) -> JiaoyunResolution:
        birth = seed.birth_utc.astimezone(timezone.utc)
        previous = seed.previous_jie_utc.astimezone(timezone.utc)
        if birth == previous and profile.exact_jie_tie_policy == "FAIL_CLOSED":
            raise BaziTemporalGenerationError(
                "EXACT_JIE_TIE_UNRESOLVED",
                f"birth instant equals Jie boundary {seed.previous_jie_name}@{previous.isoformat()}",
            )

        anchor_kind, anchor_name, anchor, delta, reselected = _select_jiaoyun_anchor(
            seed,
            direction,
            profile,
        )
        if profile.interval_coordinate_policy == CONTINUOUS_INTERVAL_COORDINATE_POLICY:
            source_refs = ("S15", "ENGINEERING:MODERN_CONTINUOUS_RATIO_120X")
        elif profile.interval_coordinate_policy == WENZHEN_INTERVAL_COORDINATE_POLICY:
            source_refs = (
                "S15",
                "EXTERNAL_COMPATIBILITY:WENZHEN:A7-A11",
                "MODEL_INFERENCE:MIXED_APPARENT_SOLAR_TO_CHINA_STANDARD_CLOCK_R1",
                "PRECISION_CEILING:WENZHEN_UI_HOUR_ONLY",
            )
            if reselected:
                source_refs += (WENZHEN_MIXED_CLOCK_ANCHOR_RESELECTION_REF,)
        else:
            raise BaziTemporalGenerationError(
                "UNSUPPORTED_INTERVAL_COORDINATE_POLICY",
                profile.interval_coordinate_policy,
            )
        raw_microseconds = _timedelta_microseconds(delta)
        if raw_microseconds < 0:
            raise BaziTemporalGenerationError(
                "INVALID_JIE_ANCHOR_ORDER",
                f"negative interval after coordinate-consistent anchor selection for {seed.seed_id}",
            )

        symbolic = cls._symbolic_age(raw_microseconds)
        if profile.calendar_realization_rule_set == CONTINUOUS_CALENDAR_REALIZATION_RULE_SET:
            first_transition = birth + timedelta(microseconds=symbolic.total_symbolic_microseconds)
        elif profile.calendar_realization_rule_set == WENZHEN_CALENDAR_REALIZATION_RULE_SET:
            first_transition = realize_wenzhen_calendar_month_displacement_utc(birth, symbolic)
        else:
            raise BaziTemporalGenerationError(
                "UNSUPPORTED_CALENDAR_REALIZATION_RULE",
                profile.calendar_realization_rule_set,
            )
        return JiaoyunResolution(
            temporal_seed_id=seed.seed_id,
            direction=direction.direction,
            anchor_kind=anchor_kind,
            anchor_jie_name=anchor_name,
            anchor_jie_utc=anchor,
            birth_utc=birth,
            raw_interval_microseconds=raw_microseconds,
            symbolic_age=symbolic,
            first_transition_utc=first_transition,
            interval_coordinate_policy=profile.interval_coordinate_policy,
            interval_granularity_rule_set=profile.interval_granularity_rule_set,
            calendar_realization_rule_set=profile.calendar_realization_rule_set,
            source_refs=source_refs,
        )

    @staticmethod
    def _month_pillar(candidate: BaziChartCandidate) -> str:
        rows = [row for row in candidate.chart.pillars if row.position == "MONTH"]
        if len(rows) != 1:
            raise BaziTemporalGenerationError("INVALID_MONTH_PILLAR", "expected exactly one MONTH pillar")
        return rows[0].ganzhi

    @classmethod
    def _generate_state_for_seed(
        cls,
        candidate: BaziChartCandidate,
        seed,
        direction: DayunDirectionResolution,
        profile: ResolvedBaziTemporalProfile,
        dayun_count: int,
    ) -> BaziDayunState:
        if dayun_count < 1:
            raise BaziTemporalGenerationError("INVALID_DAYUN_COUNT", str(dayun_count))
        jiaoyun = cls._jiaoyun_for_seed(seed, direction, profile)
        pre_dayun = PreDayunFrame(
            frame_id=f"PRE_DAYUN:{seed.seed_id}",
            start_utc=jiaoyun.birth_utc,
            end_utc=jiaoyun.first_transition_utc,
            interval_semantics=profile.interval_semantics,
        )
        month_index = sexagenary_index(cls._month_pillar(candidate))
        step = 1 if direction.direction == "FORWARD" else -1
        frames: list[DayunFrame] = []
        for index in range(1, dayun_count + 1):
            start = _dayun_anniversary(
                jiaoyun.first_transition_utc,
                (index - 1) * 10,
                profile,
            )
            end = _dayun_anniversary(jiaoyun.first_transition_utc, index * 10, profile)
            ganzhi_index = (month_index + step * index) % 60
            ganzhi = SEXAGENARY_CYCLE[ganzhi_index]
            frames.append(
                DayunFrame(
                    frame_id=f"DAYUN:{index:02d}:{ganzhi}",
                    index=index,
                    ganzhi=ganzhi,
                    sexagenary_index=ganzhi_index,
                    start_utc=start,
                    end_utc=end,
                    interval_semantics=profile.interval_semantics,
                    source_refs=(
                        ("S15",)
                        if profile.interval_coordinate_policy == CONTINUOUS_INTERVAL_COORDINATE_POLICY
                        else ("S15", "EXTERNAL_COMPATIBILITY:WENZHEN:A7-A11")
                    ),
                )
            )
        return BaziDayunState(
            upstream_natal_fact_hash=candidate.hashes.fact_hash,
            direction=direction,
            jiaoyun=jiaoyun,
            pre_dayun=pre_dayun,
            dayun_frames=tuple(frames),
            profile_id=profile.profile_id,
            profile_version=profile.profile_version,
            algorithm_versions={
                "temporal": profile.algorithm_version,
                "direction": DIRECTION_RULE_SET_VERSION,
                "anchor": ANCHOR_RULE_SET_VERSION,
                "symbolic_age": SYMBOLIC_AGE_RULE_SET_VERSION,
                "dayun_sequence": DAYUN_SEQUENCE_RULE_SET_VERSION,
            },
        )

    def resolve_typed(self, request: BaziTemporalRequest) -> BaziTemporalResolution:
        profile = request.profile.validate()
        try:
            sex = request.sex if isinstance(request.sex, BaziSex) else BaziSex(request.sex)
        except ValueError:
            return BaziTemporalResolution(
                schema=self.typed_schema,
                status="FAILED",
                candidates=(),
                events=(),
                diagnostics=(f"INVALID_SEX:{request.sex}",),
            )
        try:
            direction = self.resolve_direction(request.candidate, sex)
            states = tuple(
                self._generate_state_for_seed(
                    request.candidate,
                    seed,
                    direction,
                    profile,
                    request.dayun_count,
                )
                for seed in request.candidate.temporal_seeds
            )
        except BaziTemporalGenerationError as exc:
            return BaziTemporalResolution(
                schema=self.typed_schema,
                status="FAILED",
                candidates=(),
                events=(),
                diagnostics=(f"{exc.diagnostic_code}:{exc}",),
            )

        # Import here to keep models/profile independent from integrity hashing.
        from .integrity import temporal_hash_bundle, validate_dayun_state

        unique: dict[str, dict[str, Any]] = {}
        for state in states:
            report = validate_dayun_state(state, request.candidate, profile)
            if report.status != "PASS":
                return BaziTemporalResolution(
                    schema=self.typed_schema,
                    status="FAILED",
                    candidates=(),
                    events=(),
                    diagnostics=tuple(f"INTEGRITY:{row.code}:{row.path}" for row in report.diagnostics),
                )
            hashes = temporal_hash_bundle(state, profile)
            key = hashes.fact_hash
            if key not in unique:
                unique[key] = {
                    "state": state,
                    "integrity": report,
                    "hashes": hashes,
                    "seed_ids": [state.jiaoyun.temporal_seed_id],
                }
            else:
                row = unique[key]
                if row["hashes"].computation_hash != hashes.computation_hash:
                    return BaziTemporalResolution(
                        schema=self.typed_schema,
                        status="FAILED",
                        candidates=(),
                        events=(),
                        diagnostics=("INTEGRITY:SAME_TEMPORAL_FACT_DIFFERENT_COMPUTATION_LINEAGE",),
                    )
                row["seed_ids"].append(state.jiaoyun.temporal_seed_id)

        candidates = tuple(
            BaziTemporalCandidate(
                source_temporal_seed_ids=tuple(row["seed_ids"]),
                state=row["state"],
                integrity=row["integrity"],
                hashes=row["hashes"],
            )
            for row in unique.values()
        )
        if not candidates:
            status = "FAILED"
            events = ()
            diagnostics = ("NO_TEMPORAL_SEEDS",)
        elif len(candidates) == 1:
            status = "RESOLVED"
            events = ()
            diagnostics = ()
        else:
            status = "MULTI_CANDIDATE"
            events = ("TIME_UNCERTAINTY_CHANGED_DAYUN_BOUNDARIES",)
            diagnostics = ()
        return BaziTemporalResolution(
            schema=self.typed_schema,
            status=status,
            candidates=candidates,
            events=events,
            diagnostics=diagnostics,
        )

    def resolve(self, request: BaziTemporalRequest) -> dict[str, Any]:
        """Return the stable machine-readable Dayun R1 envelope."""

        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "calculation_profile": json_value(request.profile),
            "sex": json_value(request.sex),
            "dayun_count": request.dayun_count,
            "upstream_natal_fact_hash": request.candidate.hashes.fact_hash,
            "candidates": [
                {
                    "source_temporal_seed_ids": list(row.source_temporal_seed_ids),
                    "state": json_value(row.state),
                    "integrity": json_value(row.integrity),
                    "hashes": json_value(row.hashes),
                }
                for row in typed.candidates
            ],
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }