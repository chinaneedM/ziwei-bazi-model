from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    bazi_foundation_v1_profile,
)
from fortune_training.bazi_flow import (
    BaziFlowEngine,
    BaziFlowRequest,
    flow_hash_bundle,
    validate_flow_context,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    BaziTemporalEngine,
    BaziTemporalRequest,
    bazi_temporal_v1_continuous_profile,
    bazi_temporal_wenzhen_china_compatibility_r1_profile,
)
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]
WENZHEN_FLOW_FIXTURE = json.loads(
    (ROOT / "tests" / "fixtures" / "bazi-flow-wenzhen-annual-month-r1.json").read_text(
        encoding="utf-8"
    )
)


class BaziFlowContextR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chart_engine = BaziChartFoundation.from_repository(ROOT)
        cls.chart_profile = bazi_foundation_v1_profile(
            cls.chart_engine.time_calendar.policy_registry
        )
        cls.temporal_engine = BaziTemporalEngine()
        cls.flow_engine = BaziFlowEngine(cls.chart_engine.time_calendar.bazi)
        cls.natal = cls._natal(datetime(2025, 2, 7, 10, 10))
        cls.continuous = cls.temporal_engine.resolve_typed(
            BaziTemporalRequest(
                cls.natal,
                BaziSex.MALE,
                bazi_temporal_v1_continuous_profile(),
                dayun_count=4,
            )
        )
        cls.wenzhen = cls.temporal_engine.resolve_typed(
            BaziTemporalRequest(
                cls.natal,
                BaziSex.MALE,
                bazi_temporal_wenzhen_china_compatibility_r1_profile(),
                dayun_count=4,
            )
        )
        if cls.continuous.status != "RESOLVED" or cls.wenzhen.status != "RESOLVED":
            raise RuntimeError("flow fixture requires resolved Dayun candidates")

    @classmethod
    def _natal(cls, local: datetime, **kwargs):
        result = cls.chart_engine.resolve_typed(
            BaziChartRequest(
                BirthInput(
                    reported_local_datetime=local,
                    birth_place="Beijing",
                    latitude=39.9042,
                    longitude=116.4074,
                    timezone_id="Asia/Shanghai",
                    **kwargs,
                ),
                cls.chart_profile,
            )
        )
        if len(result.candidates) != 1:
            raise RuntimeError(f"fixture requires one Natal candidate: {result.status}")
        return result.candidates[0]

    @classmethod
    def _resolve(cls, target: datetime, temporal=None, natal=None):
        natal = natal or cls.natal
        temporal = temporal or cls.continuous
        return cls.flow_engine.resolve_typed(
            BaziFlowRequest(
                natal_candidate=natal,
                temporal_candidates=temporal.candidates,
                target_utc=target,
                calculation_profile=cls.chart_profile,
            )
        )

    def test_exact_start_of_spring_activates_new_annual_and_yin_month(self):
        spring = self.chart_engine.time_calendar.solar_terms.term(2026, 315).utc_instant
        before = self._resolve(spring - timedelta(microseconds=1)).candidates[0].context
        exact = self._resolve(spring).candidates[0].context
        self.assertEqual("乙巳", before.annual_frame.ganzhi)
        self.assertEqual("丙午", exact.annual_frame.ganzhi)
        self.assertEqual("己丑", before.monthly_frame.ganzhi)
        self.assertEqual("庚寅", exact.monthly_frame.ganzhi)
        self.assertEqual(spring, exact.annual_frame.start_utc)
        self.assertEqual(spring, exact.monthly_frame.start_utc)

    def test_exact_monthly_jie_activates_new_month(self):
        jingzhe = self.chart_engine.time_calendar.solar_terms.term(2026, 345).utc_instant
        before = self._resolve(jingzhe - timedelta(microseconds=1)).candidates[0].context
        exact = self._resolve(jingzhe).candidates[0].context
        self.assertEqual("庚寅", before.monthly_frame.ganzhi)
        self.assertEqual("辛卯", exact.monthly_frame.ganzhi)
        self.assertEqual("AWAKENING_OF_INSECTS", exact.monthly_frame.start_jie_name)
        self.assertEqual(jingzhe, exact.monthly_frame.start_utc)

    def test_pre_dayun_to_dayun_01_boundary_is_half_open(self):
        temporal = self.continuous.candidates[0]
        transition = temporal.state.jiaoyun.first_transition_utc
        before = self._resolve(transition - timedelta(microseconds=1)).candidates[0].context
        exact = self._resolve(transition).candidates[0].context
        self.assertEqual("PRE_DAYUN", before.active_dayun_kind)
        self.assertIs(temporal.state.pre_dayun, before.active_dayun_frame)
        self.assertEqual("DAYUN", exact.active_dayun_kind)
        self.assertIs(temporal.state.dayun_frames[0], exact.active_dayun_frame)

    def test_later_dayun_transition_activates_new_frame(self):
        temporal = self.continuous.candidates[0]
        transition = temporal.state.dayun_frames[0].end_utc
        before = self._resolve(transition - timedelta(microseconds=1)).candidates[0].context
        exact = self._resolve(transition).candidates[0].context
        self.assertEqual(1, before.active_dayun_frame.index)
        self.assertEqual(2, exact.active_dayun_frame.index)

    def test_early_february_remains_prior_annual_pillar(self):
        target = datetime(2026, 2, 1, tzinfo=timezone.utc)
        context = self._resolve(target).candidates[0].context
        self.assertEqual(2025, context.annual_frame.pillar_year)
        self.assertEqual("乙巳", context.annual_frame.ganzhi)
        self.assertEqual("己丑", context.monthly_frame.ganzhi)

    def test_wenzhen_profile_reuses_shared_2026_annual_month_sequence(self):
        self.assertEqual(
            "THIRD_PARTY_COMPATIBILITY_WITNESS",
            WENZHEN_FLOW_FIXTURE["authority_class"],
        )
        self.assertFalse(WENZHEN_FLOW_FIXTURE["canonical_calendar_truth"])
        for witness in WENZHEN_FLOW_FIXTURE["months"]:
            longitude = witness["longitude_degrees"]
            with self.subTest(longitude=longitude):
                target = self.chart_engine.time_calendar.solar_terms.term(2026, longitude).utc_instant
                context = self._resolve(target, temporal=self.wenzhen).candidates[0].context
                self.assertEqual(WENZHEN_FLOW_FIXTURE["annual"]["ganzhi"], context.annual_frame.ganzhi)
                self.assertEqual(witness["start_term"], context.monthly_frame.start_jie_name)
                self.assertEqual(witness["ganzhi"], context.monthly_frame.ganzhi)
                self.assertEqual(
                    "BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1",
                    context.temporal_profile_id,
                )

    def test_continuous_and_wenzhen_profiles_share_annual_month_truth(self):
        target = datetime(2026, 6, 1, tzinfo=timezone.utc)
        continuous = self._resolve(target).candidates[0].context
        wenzhen = self._resolve(target, temporal=self.wenzhen).candidates[0].context
        self.assertEqual(continuous.annual_frame, wenzhen.annual_frame)
        self.assertEqual(continuous.monthly_frame, wenzhen.monthly_frame)
        self.assertNotEqual(
            continuous.upstream_temporal_fact_hash,
            wenzhen.upstream_temporal_fact_hash,
        )

    def test_frame_identity_depends_on_instant_not_display_timezone(self):
        utc_target = datetime(2026, 6, 1, tzinfo=timezone.utc)
        china_target = utc_target.astimezone(timezone(timedelta(hours=8)))
        utc_context = self._resolve(utc_target).candidates[0].context
        china_context = self._resolve(china_target).candidates[0].context
        self.assertEqual(utc_context.target_utc, china_context.target_utc)
        self.assertEqual(utc_context.annual_frame.frame_id, china_context.annual_frame.frame_id)
        self.assertEqual(utc_context.monthly_frame.frame_id, china_context.monthly_frame.frame_id)
        self.assertEqual(
            self._resolve(utc_target).candidates[0].hashes.fact_hash,
            self._resolve(china_target).candidates[0].hashes.fact_hash,
        )

    def test_multiple_temporal_candidates_replay_without_collapsing(self):
        natal = self._natal(datetime(2025, 2, 7, 10, 10), uncertainty_seconds=120)
        temporal = self.temporal_engine.resolve_typed(
            BaziTemporalRequest(
                natal,
                BaziSex.MALE,
                bazi_temporal_v1_continuous_profile(),
                dayun_count=3,
            )
        )
        self.assertEqual("MULTI_CANDIDATE", temporal.status)
        target = datetime(2026, 1, 1, tzinfo=timezone.utc)
        result = self._resolve(target, temporal=temporal, natal=natal)
        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(len(temporal.candidates), len(result.candidates))
        self.assertEqual(1, len({row.context.annual_frame.frame_id for row in result.candidates}))
        self.assertEqual(1, len({row.context.monthly_frame.frame_id for row in result.candidates}))
        self.assertEqual(
            len(result.candidates),
            len({row.context.upstream_temporal_fact_hash for row in result.candidates}),
        )

    def test_only_identical_complete_flow_payload_deduplicates(self):
        target = datetime(2026, 1, 1, tzinfo=timezone.utc)
        temporal = self.continuous.candidates[0]
        result = self.flow_engine.resolve_typed(
            BaziFlowRequest(
                self.natal,
                (temporal, temporal),
                target,
                self.chart_profile,
            )
        )
        self.assertEqual("RESOLVED", result.status)
        self.assertEqual(1, len(result.candidates))
        self.assertEqual((0, 1), result.candidates[0].source_temporal_candidate_indices)

    def test_flow_hashes_are_deterministic_and_upstream_hashes_do_not_mutate(self):
        target = datetime(2026, 6, 1, tzinfo=timezone.utc)
        natal_hashes = self.natal.hashes
        temporal_hashes = self.continuous.candidates[0].hashes
        first = self._resolve(target)
        second = self._resolve(target)
        self.assertEqual(first, second)
        self.assertEqual(first.candidates[0].hashes, second.candidates[0].hashes)
        self.assertEqual(natal_hashes, self.natal.hashes)
        self.assertEqual(temporal_hashes, self.continuous.candidates[0].hashes)

    def test_integrity_replay_detects_tampered_month_and_hash(self):
        result = self._resolve(datetime(2026, 6, 1, tzinfo=timezone.utc))
        row = result.candidates[0]
        tampered = replace(
            row.context,
            monthly_frame=replace(row.context.monthly_frame, ganzhi="甲子"),
        )
        report = validate_flow_context(
            tampered,
            self.natal,
            self.continuous.candidates[0],
            self.chart_profile,
            self.flow_engine.bazi_time,
        )
        self.assertEqual("FAIL", report.status)
        self.assertIn("MONTHLY_GANZHI_REPLAY_MISMATCH", {item.code for item in report.diagnostics})
        self.assertNotEqual(
            row.hashes.fact_hash,
            flow_hash_bundle(
                tampered,
                self.natal,
                self.continuous.candidates[0],
                self.chart_profile,
            ).fact_hash,
        )

        wrong_upstream = replace(tampered, upstream_temporal_fact_hash="0" * 64)
        upstream_report = validate_flow_context(
            wrong_upstream,
            self.natal,
            self.continuous.candidates[0],
            self.chart_profile,
            self.flow_engine.bazi_time,
        )
        self.assertIn(
            "UPSTREAM_TEMPORAL_HASH_MISMATCH",
            {item.code for item in upstream_report.diagnostics},
        )

    def test_target_before_birth_and_after_schedule_fail_closed(self):
        birth = self.continuous.candidates[0].state.jiaoyun.birth_utc
        before = self._resolve(birth - timedelta(microseconds=1))
        self.assertEqual("FAILED", before.status)
        self.assertTrue(before.diagnostics[0].startswith("TARGET_BEFORE_BIRTH:"))

        end = self.continuous.candidates[0].state.dayun_frames[-1].end_utc
        after = self._resolve(end)
        self.assertEqual("FAILED", after.status)
        self.assertTrue(
            after.diagnostics[0].startswith("TARGET_OUT_OF_MATERIALIZED_DAYUN_RANGE:")
        )


if __name__ == "__main__":
    unittest.main()
