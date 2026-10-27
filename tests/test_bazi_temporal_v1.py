from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    BaziTemporalSeed,
    bazi_foundation_v1_profile,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    BaziTemporalEngine,
    BaziTemporalRequest,
    bazi_temporal_v1_continuous_profile,
    validate_dayun_state,
)
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]


class BaziTemporalV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chart_engine = BaziChartFoundation.from_repository(ROOT)
        cls.chart_profile = bazi_foundation_v1_profile(cls.chart_engine.time_calendar.policy_registry)
        cls.temporal = BaziTemporalEngine()
        cls.temporal_profile = bazi_temporal_v1_continuous_profile()

    @staticmethod
    def beijing(local: datetime, **kwargs) -> BirthInput:
        return BirthInput(
            reported_local_datetime=local,
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
            **kwargs,
        )

    def chart_candidate(self, local: datetime, **kwargs):
        resolved = self.chart_engine.resolve_typed(
            BaziChartRequest(
                birth=self.beijing(local, **kwargs),
                profile=self.chart_profile,
            )
        )
        self.assertEqual(1, len(resolved.candidates))
        return resolved.candidates[0]

    def test_a6_sex_changes_direction_not_natal_chart(self):
        candidate = self.chart_candidate(datetime(2025, 2, 7, 10, 10))
        self.assertEqual(("乙巳", "戊寅"), tuple(row.ganzhi for row in candidate.chart.pillars[:2]))

        male = self.temporal.resolve_typed(
            BaziTemporalRequest(candidate, BaziSex.MALE, self.temporal_profile, dayun_count=3)
        )
        female = self.temporal.resolve_typed(
            BaziTemporalRequest(candidate, BaziSex.FEMALE, self.temporal_profile, dayun_count=3)
        )
        self.assertEqual("RESOLVED", male.status)
        self.assertEqual("RESOLVED", female.status)
        self.assertEqual(candidate.hashes.fact_hash, male.candidates[0].state.upstream_natal_fact_hash)
        self.assertEqual(candidate.hashes.fact_hash, female.candidates[0].state.upstream_natal_fact_hash)
        self.assertEqual("REVERSE", male.candidates[0].state.direction.direction)
        self.assertEqual("FORWARD", female.candidates[0].state.direction.direction)
        self.assertEqual("丁丑", male.candidates[0].state.dayun_frames[0].ganzhi)
        self.assertEqual("己卯", female.candidates[0].state.dayun_frames[0].ganzhi)

    def test_a1_dayun_sequence_remains_month_pillar_based_despite_dst_hour_difference(self):
        candidate = self.chart_candidate(datetime(1990, 6, 15, 12, 0))
        self.assertEqual(("庚午", "壬午", "辛亥", "癸巳"), tuple(row.ganzhi for row in candidate.chart.pillars))
        result = self.temporal.resolve_typed(
            BaziTemporalRequest(candidate, BaziSex.MALE, self.temporal_profile, dayun_count=8)
        )
        self.assertEqual("RESOLVED", result.status)
        state = result.candidates[0].state
        self.assertEqual("FORWARD", state.direction.direction)
        self.assertEqual(
            ("癸未", "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅"),
            tuple(frame.ganzhi for frame in state.dayun_frames),
        )

    def test_symbolic_three_and_half_day_interval_is_one_year_two_months(self):
        candidate = self.chart_candidate(datetime(2025, 2, 7, 10, 10))
        birth = datetime(2025, 2, 7, 2, 10, tzinfo=timezone.utc)
        synthetic_seed = BaziTemporalSeed(
            seed_id="BAZI-TEMPORAL-SEED:" + "a" * 64,
            source_time_branch_index=0,
            sample_reported_local_datetime=datetime(2025, 2, 7, 10, 10),
            birth_utc=birth,
            local_apparent_solar_datetime=datetime(2025, 2, 7, 9, 50),
            previous_jie_name="START_OF_SPRING",
            previous_jie_utc=birth - timedelta(days=3, hours=12),
            next_jie_name="AWAKENING_OF_INSECTS",
            next_jie_utc=birth + timedelta(days=26),
            input_uncertainty_seconds_each_side=0,
            time_calendar_policy_registry_version=self.chart_profile.time_calendar_policy_registry_version,
        )
        synthetic_candidate = replace(candidate, temporal_seeds=(synthetic_seed,), branch_indices=(0,))
        result = self.temporal.resolve_typed(
            BaziTemporalRequest(synthetic_candidate, BaziSex.MALE, self.temporal_profile, dayun_count=2)
        )
        self.assertEqual("RESOLVED", result.status)
        jiaoyun = result.candidates[0].state.jiaoyun
        self.assertEqual("PREVIOUS_JIE", jiaoyun.anchor_kind)
        self.assertEqual(1, jiaoyun.symbolic_age.years_360)
        self.assertEqual(2, jiaoyun.symbolic_age.months_30)
        self.assertEqual(0, jiaoyun.symbolic_age.days)
        self.assertEqual(0, jiaoyun.symbolic_age.residual_microseconds)
        self.assertEqual(birth + timedelta(days=420), jiaoyun.first_transition_utc)

    def test_pre_dayun_and_dayun_frames_are_contiguous_half_open_intervals(self):
        candidate = self.chart_candidate(datetime(2025, 2, 7, 10, 10))
        result = self.temporal.resolve_typed(
            BaziTemporalRequest(candidate, BaziSex.MALE, self.temporal_profile, dayun_count=4)
        )
        state = result.candidates[0].state
        self.assertEqual(state.jiaoyun.birth_utc, state.pre_dayun.start_utc)
        self.assertEqual(state.jiaoyun.first_transition_utc, state.pre_dayun.end_utc)
        self.assertEqual(state.pre_dayun.end_utc, state.dayun_frames[0].start_utc)
        self.assertTrue(all(frame.interval_semantics == "START_INCLUSIVE_END_EXCLUSIVE" for frame in state.dayun_frames))
        for left, right in zip(state.dayun_frames, state.dayun_frames[1:]):
            self.assertEqual(left.end_utc, right.start_utc)
        self.assertEqual("PASS", validate_dayun_state(state, candidate, self.temporal_profile).status)

    def test_time_uncertainty_that_keeps_natal_chart_can_change_dayun_boundary(self):
        candidate = self.chart_candidate(datetime(2025, 2, 7, 10, 10), uncertainty_seconds=120)
        self.assertGreater(len(candidate.temporal_seeds), 1)
        result = self.temporal.resolve_typed(
            BaziTemporalRequest(candidate, BaziSex.MALE, self.temporal_profile, dayun_count=2)
        )
        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertGreater(len(result.candidates), 1)
        transitions = {row.state.jiaoyun.first_transition_utc for row in result.candidates}
        self.assertEqual(len(result.candidates), len(transitions))
        self.assertIn("TIME_UNCERTAINTY_CHANGED_DAYUN_BOUNDARIES", result.events)

    def test_exact_jie_tie_fails_closed(self):
        candidate = self.chart_candidate(datetime(2025, 2, 7, 10, 10))
        seed = candidate.temporal_seeds[0]
        tie_seed = replace(
            seed,
            seed_id="BAZI-TEMPORAL-SEED:" + "b" * 64,
            birth_utc=seed.previous_jie_utc,
        )
        tie_candidate = replace(candidate, temporal_seeds=(tie_seed,), branch_indices=(0,))
        result = self.temporal.resolve_typed(
            BaziTemporalRequest(tie_candidate, BaziSex.MALE, self.temporal_profile, dayun_count=2)
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any(item.startswith("EXACT_JIE_TIE_UNRESOLVED:") for item in result.diagnostics))

    def test_temporal_hashes_are_deterministic(self):
        candidate = self.chart_candidate(datetime(2025, 2, 7, 10, 10))
        request = BaziTemporalRequest(candidate, BaziSex.MALE, self.temporal_profile, dayun_count=3)
        first = self.temporal.resolve_typed(request)
        second = self.temporal.resolve_typed(request)
        self.assertEqual(first, second)
        self.assertEqual(first.candidates[0].hashes, second.candidates[0].hashes)

    def test_continuous_realization_is_explicitly_engineering_not_classical_truth(self):
        profile = self.temporal_profile
        self.assertEqual("MODERN_CONTINUOUS_RATIO_120X", profile.calendar_realization_rule_set)
        self.assertEqual("ENGINEERING_INTERPOLATION", profile.calendar_realization_source_class)
        self.assertEqual("FAIL_CLOSED", profile.exact_jie_tie_policy)


if __name__ == "__main__":
    unittest.main()
