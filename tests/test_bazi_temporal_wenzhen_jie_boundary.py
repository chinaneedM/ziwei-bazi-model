from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_application import (
    BaziApplicationRequest,
    BaziChartService,
    bazi_local_application_v1_profile,
)
from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    bazi_foundation_zi_start_23_r1_profile,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    BaziTemporalEngine,
    BaziTemporalRequest,
    bazi_temporal_v1_continuous_profile,
    bazi_temporal_wenzhen_china_compatibility_r1_profile,
)
from fortune_training.bazi_temporal.engine import (
    WENZHEN_MIXED_CLOCK_ANCHOR_RESELECTION_REF,
)
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]


class BaziTemporalWenzhenJieBoundaryR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chart_engine = BaziChartFoundation.from_repository(ROOT)
        cls.natal_profile = bazi_foundation_zi_start_23_r1_profile(
            cls.chart_engine.time_calendar.policy_registry
        )
        cls.wenzhen_profile = bazi_temporal_wenzhen_china_compatibility_r1_profile()
        cls.continuous_profile = bazi_temporal_v1_continuous_profile()
        cls.temporal_engine = BaziTemporalEngine()
        cls.application_service = BaziChartService.from_repository(ROOT)

    @classmethod
    def _birth(cls, hour: int, minute: int) -> BirthInput:
        return BirthInput(
            reported_local_datetime=datetime(2009, 2, 4, hour, minute),
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
        )

    @classmethod
    def _natal(cls, hour: int, minute: int):
        result = cls.chart_engine.resolve_typed(
            BaziChartRequest(
                birth=cls._birth(hour, minute),
                profile=cls.natal_profile,
            )
        )
        if result.status != "RESOLVED" or len(result.candidates) != 1:
            raise AssertionError(result)
        return result.candidates[0]

    def test_calibration_5_pair_resolves_across_start_of_spring_mixed_clock_inversion(self):
        before = self._natal(0, 40)
        after = self._natal(1, 0)
        self.assertEqual(
            ["戊子", "乙丑", "庚辰", "丙子"],
            [row.ganzhi for row in before.chart.pillars],
        )
        self.assertEqual(
            ["己丑", "丙寅", "庚辰", "丙子"],
            [row.ganzhi for row in after.chart.pillars],
        )

        before_result = self.temporal_engine.resolve_typed(
            BaziTemporalRequest(before, BaziSex.MALE, self.wenzhen_profile, dayun_count=3)
        )
        after_result = self.temporal_engine.resolve_typed(
            BaziTemporalRequest(after, BaziSex.MALE, self.wenzhen_profile, dayun_count=3)
        )
        self.assertEqual("RESOLVED", before_result.status, before_result.diagnostics)
        self.assertEqual("RESOLVED", after_result.status, after_result.diagnostics)

        before_state = before_result.candidates[0].state
        after_state = after_result.candidates[0].state
        self.assertEqual("FORWARD", before_state.direction.direction)
        self.assertEqual("NEXT_JIE", before_state.jiaoyun.anchor_kind)
        self.assertEqual("START_OF_SPRING", before_state.jiaoyun.anchor_jie_name)
        self.assertGreaterEqual(before_state.jiaoyun.raw_interval_microseconds, 0)
        self.assertNotIn(
            WENZHEN_MIXED_CLOCK_ANCHOR_RESELECTION_REF,
            before_state.jiaoyun.source_refs,
        )

        self.assertEqual("START_OF_SPRING", after.temporal_seeds[0].previous_jie_name)
        self.assertEqual("REVERSE", after_state.direction.direction)
        self.assertEqual("PREVIOUS_JIE", after_state.jiaoyun.anchor_kind)
        self.assertEqual("MINOR_COLD", after_state.jiaoyun.anchor_jie_name)
        self.assertGreaterEqual(after_state.jiaoyun.raw_interval_microseconds, 0)
        self.assertIn(
            WENZHEN_MIXED_CLOCK_ANCHOR_RESELECTION_REF,
            after_state.jiaoyun.source_refs,
        )
        self.assertEqual("PASS", after_result.candidates[0].integrity.status)

    def test_continuous_profile_keeps_utc_previous_jie_on_same_post_boundary_birth(self):
        after = self._natal(1, 0)
        result = self.temporal_engine.resolve_typed(
            BaziTemporalRequest(after, BaziSex.MALE, self.continuous_profile, dayun_count=3)
        )
        self.assertEqual("RESOLVED", result.status, result.diagnostics)
        state = result.candidates[0].state
        self.assertEqual("REVERSE", state.direction.direction)
        self.assertEqual("PREVIOUS_JIE", state.jiaoyun.anchor_kind)
        self.assertEqual("START_OF_SPRING", state.jiaoyun.anchor_jie_name)
        self.assertGreaterEqual(state.jiaoyun.raw_interval_microseconds, 0)
        self.assertNotIn(
            WENZHEN_MIXED_CLOCK_ANCHOR_RESELECTION_REF,
            state.jiaoyun.source_refs,
        )
        self.assertEqual("1.0.1", self.continuous_profile.algorithm_version)
        self.assertEqual("1.1.1", self.wenzhen_profile.algorithm_version)

    def test_bazi_application_resolves_calibration_5_post_boundary_input(self):
        bundle = self.application_service.resolve(
            BaziApplicationRequest(
                birth=self._birth(1, 0),
                sex=BaziSex.MALE,
                natal_profile=self.natal_profile,
                temporal_profile=self.wenzhen_profile,
                application_profile=bazi_local_application_v1_profile(),
                dayun_count=12,
            )
        )
        self.assertEqual("RESOLVED", bundle.status)
        self.assertEqual("PASS", bundle.integrity.status)
        self.assertEqual(1, len(bundle.candidates))
        dayun_view = bundle.candidates[0].view["dayun"]
        self.assertEqual("REVERSE", dayun_view["direction"])
        self.assertEqual("MINOR_COLD", dayun_view["jiaoyun"]["anchor_jie_name"])


if __name__ == "__main__":
    unittest.main()
