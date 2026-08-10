from __future__ import annotations

from datetime import timedelta, timezone
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate, SEXAGENARY_CYCLE, sexagenary_index
from fortune_training.bazi_chart.registries import STEM_POLARITY
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    BaziDayunState,
    BaziSex,
    TemporalHashBundle,
    TemporalIntegrityDiagnostic,
    TemporalIntegrityReport,
)
from .engine import (
    CHINA_STANDARD_TIME,
    _dayun_anniversary,
    realize_wenzhen_calendar_month_displacement_utc,
)
from .profile import (
    CONTINUOUS_CALENDAR_REALIZATION_RULE_SET,
    CONTINUOUS_INTERVAL_COORDINATE_POLICY,
    ResolvedBaziTemporalProfile,
    WENZHEN_CALENDAR_REALIZATION_RULE_SET,
    WENZHEN_INTERVAL_COORDINATE_POLICY,
)


INTEGRITY_ALGORITHM_ID = "BAZI-TEMPORAL-INTEGRITY-V1"
INTEGRITY_ALGORITHM_VERSION = "1.0.1"
HASH_ALGORITHM_ID = "BAZI-TEMPORAL-HASH-V1"
HASH_ALGORITHM_VERSION = "1.0.1"
DAY_MICROSECONDS = 86_400_000_000
SYMBOLIC_YEAR_MICROSECONDS = 360 * DAY_MICROSECONDS
SYMBOLIC_MONTH_MICROSECONDS = 30 * DAY_MICROSECONDS


def _diag(rows: list[TemporalIntegrityDiagnostic], code: str, path: str, detail: str) -> None:
    rows.append(TemporalIntegrityDiagnostic(code=code, path=path, detail=detail))


def _delta_microseconds(delta) -> int:
    return delta.days * DAY_MICROSECONDS + delta.seconds * 1_000_000 + delta.microseconds


def _instant_fact(value) -> str:
    """Canonical UTC instant representation used inside temporal FactHash."""

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("temporal fact instant must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def validate_dayun_state(
    state: BaziDayunState,
    candidate: BaziChartCandidate,
    profile: ResolvedBaziTemporalProfile,
) -> TemporalIntegrityReport:
    diagnostics: list[TemporalIntegrityDiagnostic] = []
    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "PROFILE_INVALID", "profile", str(exc))

    if state.upstream_natal_fact_hash != candidate.hashes.fact_hash:
        _diag(diagnostics, "UPSTREAM_NATAL_HASH_MISMATCH", "upstream_natal_fact_hash", state.upstream_natal_fact_hash)
    if state.profile_id != profile.profile_id or state.profile_version != profile.profile_version:
        _diag(diagnostics, "TEMPORAL_PROFILE_BINDING_MISMATCH", "profile_id", state.profile_id)
    if state.algorithm_versions.get("temporal") != profile.algorithm_version:
        _diag(
            diagnostics,
            "TEMPORAL_ALGORITHM_VERSION_MISMATCH",
            "algorithm_versions.temporal",
            str(state.algorithm_versions.get("temporal")),
        )

    year_rows = [row for row in candidate.chart.stems if row.position == "YEAR"]
    if len(year_rows) != 1:
        _diag(diagnostics, "INVALID_YEAR_STEM", "direction", "expected one YEAR stem")
    else:
        year_stem = year_rows[0].stem
        polarity = STEM_POLARITY[year_stem]
        expected_forward = (
            polarity == "YANG" and state.direction.sex is BaziSex.MALE
        ) or (
            polarity == "YIN" and state.direction.sex is BaziSex.FEMALE
        )
        expected_direction = "FORWARD" if expected_forward else "REVERSE"
        if (
            state.direction.year_stem != year_stem
            or state.direction.year_stem_polarity != polarity
            or state.direction.direction != expected_direction
        ):
            _diag(diagnostics, "DIRECTION_REPLAY_MISMATCH", "direction", expected_direction)

    seed_by_id = {seed.seed_id: seed for seed in candidate.temporal_seeds}
    seed = seed_by_id.get(state.jiaoyun.temporal_seed_id)
    if seed is None:
        _diag(diagnostics, "TEMPORAL_SEED_MISSING", "jiaoyun.temporal_seed_id", state.jiaoyun.temporal_seed_id)
    else:
        if state.direction.direction == "FORWARD":
            expected_anchor_kind = "NEXT_JIE"
            expected_anchor_name = seed.next_jie_name
            expected_anchor = seed.next_jie_utc
        else:
            expected_anchor_kind = "PREVIOUS_JIE"
            expected_anchor_name = seed.previous_jie_name
            expected_anchor = seed.previous_jie_utc

        if profile.interval_coordinate_policy == CONTINUOUS_INTERVAL_COORDINATE_POLICY:
            expected_delta = (
                expected_anchor - seed.birth_utc
                if state.direction.direction == "FORWARD"
                else seed.birth_utc - expected_anchor
            )
        elif profile.interval_coordinate_policy == WENZHEN_INTERVAL_COORDINATE_POLICY:
            birth_clock = seed.local_apparent_solar_datetime.replace(tzinfo=None)
            jie_china_clock = expected_anchor.astimezone(CHINA_STANDARD_TIME).replace(tzinfo=None)
            expected_delta = (
                jie_china_clock - birth_clock
                if state.direction.direction == "FORWARD"
                else birth_clock - jie_china_clock
            )
        else:
            expected_delta = timedelta(microseconds=-1)
            _diag(
                diagnostics,
                "UNSUPPORTED_INTERVAL_COORDINATE_POLICY",
                "jiaoyun.interval_coordinate_policy",
                profile.interval_coordinate_policy,
            )
        expected_raw = _delta_microseconds(expected_delta)
        if state.jiaoyun.anchor_kind != expected_anchor_kind:
            _diag(diagnostics, "JIAOYUN_ANCHOR_KIND_MISMATCH", "jiaoyun.anchor_kind", expected_anchor_kind)
        if state.jiaoyun.anchor_jie_name != expected_anchor_name or state.jiaoyun.anchor_jie_utc != expected_anchor:
            _diag(diagnostics, "JIAOYUN_ANCHOR_MISMATCH", "jiaoyun.anchor_jie_utc", expected_anchor_name)
        if state.jiaoyun.birth_utc != seed.birth_utc:
            _diag(diagnostics, "JIAOYUN_BIRTH_INSTANT_MISMATCH", "jiaoyun.birth_utc", seed.seed_id)
        if state.jiaoyun.raw_interval_microseconds != expected_raw:
            _diag(diagnostics, "JIAOYUN_INTERVAL_MISMATCH", "jiaoyun.raw_interval_microseconds", str(expected_raw))

        expected_total = expected_raw * 120
        years, remainder = divmod(expected_total, SYMBOLIC_YEAR_MICROSECONDS)
        months, remainder = divmod(remainder, SYMBOLIC_MONTH_MICROSECONDS)
        days, residual = divmod(remainder, DAY_MICROSECONDS)
        symbolic = state.jiaoyun.symbolic_age
        if (
            symbolic.total_symbolic_microseconds != expected_total
            or symbolic.years_360 != years
            or symbolic.months_30 != months
            or symbolic.days != days
            or symbolic.residual_microseconds != residual
        ):
            _diag(diagnostics, "SYMBOLIC_AGE_REPLAY_MISMATCH", "jiaoyun.symbolic_age", str(expected_total))
        if profile.calendar_realization_rule_set == CONTINUOUS_CALENDAR_REALIZATION_RULE_SET:
            expected_transition = seed.birth_utc + timedelta(microseconds=expected_total)
        elif profile.calendar_realization_rule_set == WENZHEN_CALENDAR_REALIZATION_RULE_SET:
            expected_transition = realize_wenzhen_calendar_month_displacement_utc(
                seed.birth_utc,
                symbolic,
            )
        else:
            expected_transition = seed.birth_utc
            _diag(
                diagnostics,
                "UNSUPPORTED_CALENDAR_REALIZATION_RULE",
                "jiaoyun.calendar_realization_rule_set",
                profile.calendar_realization_rule_set,
            )
        if state.jiaoyun.first_transition_utc != expected_transition:
            _diag(diagnostics, "FIRST_TRANSITION_MISMATCH", "jiaoyun.first_transition_utc", expected_transition.isoformat())

    if state.jiaoyun.interval_coordinate_policy != profile.interval_coordinate_policy:
        _diag(
            diagnostics,
            "INTERVAL_COORDINATE_POLICY_MISMATCH",
            "jiaoyun.interval_coordinate_policy",
            profile.interval_coordinate_policy,
        )
    if state.jiaoyun.interval_granularity_rule_set != profile.interval_granularity_rule_set:
        _diag(
            diagnostics,
            "INTERVAL_GRANULARITY_RULE_MISMATCH",
            "jiaoyun.interval_granularity_rule_set",
            profile.interval_granularity_rule_set,
        )
    if state.jiaoyun.calendar_realization_rule_set != profile.calendar_realization_rule_set:
        _diag(
            diagnostics,
            "CALENDAR_REALIZATION_RULE_MISMATCH",
            "jiaoyun.calendar_realization_rule_set",
            profile.calendar_realization_rule_set,
        )

    if state.pre_dayun.start_utc != state.jiaoyun.birth_utc or state.pre_dayun.end_utc != state.jiaoyun.first_transition_utc:
        _diag(diagnostics, "PRE_DAYUN_BOUNDARY_MISMATCH", "pre_dayun", "must span birth to first Jiaoyun")
    if state.pre_dayun.interval_semantics != profile.interval_semantics:
        _diag(diagnostics, "PRE_DAYUN_INTERVAL_SEMANTICS_MISMATCH", "pre_dayun.interval_semantics", profile.interval_semantics)

    month_rows = [row for row in candidate.chart.pillars if row.position == "MONTH"]
    if len(month_rows) != 1:
        _diag(diagnostics, "INVALID_MONTH_PILLAR", "dayun_frames", "expected one MONTH pillar")
    else:
        month_index = sexagenary_index(month_rows[0].ganzhi)
        step = 1 if state.direction.direction == "FORWARD" else -1
        for expected_index, frame in enumerate(state.dayun_frames, 1):
            path = f"dayun_frames[{expected_index - 1}]"
            if frame.index != expected_index:
                _diag(diagnostics, "DAYUN_INDEX_MISMATCH", path, str(frame.index))
            expected_ganzhi_index = (month_index + step * expected_index) % 60
            if frame.sexagenary_index != expected_ganzhi_index or frame.ganzhi != SEXAGENARY_CYCLE[expected_ganzhi_index]:
                _diag(diagnostics, "DAYUN_GANZHI_MISMATCH", path, SEXAGENARY_CYCLE[expected_ganzhi_index])
            expected_start = _dayun_anniversary(
                state.jiaoyun.first_transition_utc,
                (expected_index - 1) * 10,
                profile,
            )
            expected_end = _dayun_anniversary(
                state.jiaoyun.first_transition_utc,
                expected_index * 10,
                profile,
            )
            if frame.start_utc != expected_start or frame.end_utc != expected_end:
                _diag(diagnostics, "DAYUN_BOUNDARY_MISMATCH", path, f"{expected_start.isoformat()}->{expected_end.isoformat()}")
            if frame.interval_semantics != profile.interval_semantics:
                _diag(diagnostics, "DAYUN_INTERVAL_SEMANTICS_MISMATCH", path, frame.interval_semantics)
            if not frame.source_refs:
                _diag(diagnostics, "MISSING_PROVENANCE", f"{path}.source_refs", frame.frame_id)
        for left, right in zip(state.dayun_frames, state.dayun_frames[1:]):
            if left.end_utc != right.start_utc:
                _diag(diagnostics, "DAYUN_GAP_OR_OVERLAP", "dayun_frames", f"{left.frame_id}->{right.frame_id}")

    if not state.direction.source_refs or not state.jiaoyun.source_refs or not state.jiaoyun.symbolic_age.source_refs:
        _diag(diagnostics, "MISSING_PROVENANCE", "temporal", "direction/Jiaoyun/symbolic age require source refs")

    return TemporalIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=INTEGRITY_ALGORITHM_ID,
        algorithm_version=INTEGRITY_ALGORITHM_VERSION,
    )


def temporal_fact_projection(state: BaziDayunState) -> dict[str, Any]:
    """JSON-safe canonical projection of Dayun facts.

    TemporalSeed identity is intentionally absent: equivalent seeds may support
    the same temporal fact state without changing its FactHash.
    """

    return {
        "upstream_natal_fact_hash": state.upstream_natal_fact_hash,
        "direction": {
            "direction": state.direction.direction,
            "year_stem": state.direction.year_stem,
            "year_stem_polarity": state.direction.year_stem_polarity,
            "sex": state.direction.sex.value,
        },
        "jiaoyun": {
            "anchor_kind": state.jiaoyun.anchor_kind,
            "anchor_jie_name": state.jiaoyun.anchor_jie_name,
            "anchor_jie_utc": _instant_fact(state.jiaoyun.anchor_jie_utc),
            "birth_utc": _instant_fact(state.jiaoyun.birth_utc),
            "raw_interval_microseconds": state.jiaoyun.raw_interval_microseconds,
            "symbolic_age": {
                "total_symbolic_microseconds": state.jiaoyun.symbolic_age.total_symbolic_microseconds,
                "years_360": state.jiaoyun.symbolic_age.years_360,
                "months_30": state.jiaoyun.symbolic_age.months_30,
                "days": state.jiaoyun.symbolic_age.days,
                "residual_microseconds": state.jiaoyun.symbolic_age.residual_microseconds,
            },
            "first_transition_utc": _instant_fact(state.jiaoyun.first_transition_utc),
            "interval_coordinate_policy": state.jiaoyun.interval_coordinate_policy,
            "interval_granularity_rule_set": state.jiaoyun.interval_granularity_rule_set,
            "calendar_realization_rule_set": state.jiaoyun.calendar_realization_rule_set,
        },
        "pre_dayun": {
            "start_utc": _instant_fact(state.pre_dayun.start_utc),
            "end_utc": _instant_fact(state.pre_dayun.end_utc),
            "interval_semantics": state.pre_dayun.interval_semantics,
        },
        "dayun_frames": [
            {
                "index": frame.index,
                "ganzhi": frame.ganzhi,
                "sexagenary_index": frame.sexagenary_index,
                "start_utc": _instant_fact(frame.start_utc),
                "end_utc": _instant_fact(frame.end_utc),
                "interval_semantics": frame.interval_semantics,
            }
            for frame in state.dayun_frames
        ],
    }


def _lineage_projection(state: BaziDayunState) -> dict[str, Any]:
    return {
        "profile_id": state.profile_id,
        "profile_version": state.profile_version,
        "algorithm_versions": dict(sorted(state.algorithm_versions.items())),
        "direction_rule": {
            "id": state.direction.rule_set_id,
            "version": state.direction.rule_set_version,
            "source_refs": sorted(state.direction.source_refs),
        },
        "symbolic_age_rule": {
            "id": state.jiaoyun.symbolic_age.rule_set_id,
            "version": state.jiaoyun.symbolic_age.rule_set_version,
            "source_refs": sorted(state.jiaoyun.symbolic_age.source_refs),
        },
        "jiaoyun_source_refs": sorted(state.jiaoyun.source_refs),
        "dayun_source_refs": sorted({ref for frame in state.dayun_frames for ref in frame.source_refs}),
    }


def temporal_hash_bundle(
    state: BaziDayunState,
    profile: ResolvedBaziTemporalProfile,
) -> TemporalHashBundle:
    fact_hash = object_sha256(temporal_fact_projection(state))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "resolved_profile": json_value(profile),
            "lineage": _lineage_projection(state),
            "hash_algorithm": f"{HASH_ALGORITHM_ID}@{HASH_ALGORITHM_VERSION}",
        }
    )
    return TemporalHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=HASH_ALGORITHM_ID,
        algorithm_version=HASH_ALGORITHM_VERSION,
    )
