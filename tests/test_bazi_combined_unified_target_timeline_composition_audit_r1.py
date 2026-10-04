from __future__ import annotations

import copy
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_application import (
    BaziApplicationFlowRequest,
    BaziApplicationFlowService,
    BaziApplicationRequest,
    BaziChartService,
    bazi_local_application_v1_profile,
    validate_application_flow_full_replay,
)
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_target_temporal import (
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.combined_chart_application import (
    CombinedChartApplicationRequest,
    CombinedTargetFlowRequest,
    CombinedTargetFlowService,
    combined_chart_application_v1_profile,
    validate_combined_target_flow_full_replay,
)
from fortune_training.ziwei_application import (
    ziwei_application_default_presentation_profile,
    ziwei_application_v1_profile,
)
from fortune_training.ziwei_chart import ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class BaziCombinedUnifiedTargetTimelineCompositionAuditR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bazi_base_service = BaziChartService.from_repository(ROOT)
        cls.bazi_flow_service = BaziApplicationFlowService(cls.bazi_base_service)
        cls.bazi_registry = cls.bazi_base_service.chart_foundation.time_calendar.policy_registry
        cls.target_profile = bazi_target_temporal_coordinate_r1_profile()
        cls.bazi_birth = BirthInput(
            reported_local_datetime=datetime(2025, 2, 7, 10, 10),
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
        )
        cls.bazi_base_request = BaziApplicationRequest(
            birth=cls.bazi_birth,
            sex=BaziSex.MALE,
            natal_profile=bazi_foundation_v1_profile(cls.bazi_registry),
            temporal_profile=bazi_temporal_v1_continuous_profile(),
            application_profile=bazi_local_application_v1_profile(),
            dayun_count=6,
        )

        registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        cls.combined_request = CombinedChartApplicationRequest(
            birth=BirthInput(
                reported_local_datetime=datetime(1994, 5, 17, 14, 30),
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            sex="MALE",
            ziwei_calculation_profile=ziwei_chart_engine_v1_profile(registry),
            ziwei_application_profile=ziwei_application_v1_profile(),
            ziwei_presentation_profile=ziwei_application_default_presentation_profile(),
            bazi_natal_profile=bazi_foundation_v1_profile(registry),
            bazi_temporal_profile=bazi_temporal_v1_continuous_profile(),
            bazi_application_profile=bazi_local_application_v1_profile(),
            combined_profile=combined_chart_application_v1_profile(),
            ziwei_annual_year=2025,
            ziwei_daxian_count=12,
            bazi_dayun_count=12,
        )
        cls.combined_service = CombinedTargetFlowService.from_repository(ROOT)

    @staticmethod
    def _target(local: datetime, *, uncertainty_seconds: int = 0) -> TargetTemporalInput:
        return TargetTemporalInput(
            reported_local_datetime=local,
            target_place="Greenwich",
            latitude=51.4769,
            longitude=0.0,
            timezone_id="Etc/UTC",
            uncertainty_seconds=uncertainty_seconds,
        )

    @classmethod
    def _bazi_request(cls, local: datetime, *, uncertainty_seconds: int = 0):
        return BaziApplicationFlowRequest(
            application_request=cls.bazi_base_request,
            target_input=cls._target(local, uncertainty_seconds=uncertainty_seconds),
            target_coordinate_profile=cls.target_profile,
        )

    @classmethod
    def _combined_request(cls, local: datetime, *, uncertainty_seconds: int = 0, combined_request=None):
        return CombinedTargetFlowRequest(
            combined_request=combined_request or cls.combined_request,
            target_input=cls._target(local, uncertainty_seconds=uncertainty_seconds),
            target_coordinate_profile=cls.target_profile,
        )

    def test_bazi_timeline_reuses_released_layer_objects_and_full_replays(self) -> None:
        request = self._bazi_request(datetime(2026, 6, 1, 12, 0))
        result = self.bazi_flow_service.resolve(request)
        self.assertEqual("RESOLVED", result.status)
        row = result.candidates[0]
        timeline = row.view["timeline"]
        self.assertEqual(
            ["NATAL", "DAYUN", "XIAOYUN", "ANNUAL", "MONTHLY", "DAILY", "HOURLY"],
            timeline["layer_order"],
        )
        self.assertEqual("TEMPORAL_COORDINATES_ONLY_NO_INTERPRETATION", timeline["semantic_scope"])
        self.assertEqual(row.target_coordinate_candidate_id, timeline["target_coordinate_candidate_id"])
        self.assertEqual(list(row.source_application_candidate_ids), timeline["natal"]["source_application_candidate_ids"])
        self.assertEqual(row.natal_fact_hash, timeline["natal"]["natal_fact_hash"])
        self.assertEqual(row.view["flow"]["active_dayun_kind"], timeline["dayun"]["kind"])
        self.assertEqual(row.view["flow"]["active_dayun_frame"], timeline["dayun"]["frame"])
        self.assertEqual(row.view["flow"]["annual"], timeline["annual"])
        self.assertEqual(row.view["flow"]["monthly"], timeline["monthly"])
        self.assertEqual(row.view["daily"], timeline["daily"])
        self.assertEqual(row.view["hourly"], timeline["hourly"])
        self.assertEqual(
            "PASS",
            validate_application_flow_full_replay(
                self.bazi_flow_service,
                request,
                result,
            ).status,
        )

    def test_pre_dayun_and_xiaoyun_engineering_linkage_remain_explicit(self) -> None:
        result = self.bazi_flow_service.resolve(
            self._bazi_request(datetime(2025, 6, 1, 12, 0))
        )
        timeline = result.candidates[0].view["timeline"]
        self.assertEqual("PRE_DAYUN", timeline["dayun"]["kind"])
        self.assertIsNotNone(timeline["dayun"]["frame"])
        self.assertTrue(timeline["dayun"]["frame"]["frame_id"].startswith("PRE_DAYUN:"))
        self.assertNotIn("ganzhi", timeline["dayun"]["frame"])
        self.assertNotIn("sexagenary_index", timeline["dayun"]["frame"])
        xiaoyun = timeline["xiaoyun"]
        self.assertEqual("UNRESOLVED_CLASSICAL_METHOD_ALTERNATIVES", xiaoyun["selection_status"])
        self.assertEqual(2, len(xiaoyun["candidates"]))
        self.assertEqual("TARGET-CIVIL-YEAR-NOMINAL-AGE-R1", xiaoyun["age_coordinate"]["profile_id"])
        self.assertEqual("ENGINEERING_LINKAGE_COORDINATE", xiaoyun["age_coordinate"]["source_class"])
        self.assertEqual("NOT_ARBITRATED", xiaoyun["age_coordinate"]["classical_age_boundary_status"])
        self.assertFalse(any("winner" in row for row in xiaoyun["candidates"]))

    def test_target_uncertainty_preserves_bazi_candidate_lineage_and_combined_uncertainty(self) -> None:
        _, bazi_flow, combined = self.combined_service.resolve_with_bundles(
            self._combined_request(
                datetime(2026, 6, 1, 12, 0),
                uncertainty_seconds=120,
            )
        )
        self.assertEqual("MULTI_CANDIDATE", bazi_flow.status)
        self.assertGreater(len(bazi_flow.candidates), 1)
        self.assertEqual("UNCERTAINTY_PRESENT", combined.status)
        self.assertEqual(bazi_flow.bundle_hash, combined.bazi_target_flow_bundle_hash)
        source_keys = {
            (
                row.natal_candidate_index,
                row.source_temporal_candidate_indices,
                row.source_flow_candidate_index,
                row.source_target_coordinate_candidate_index,
                row.target_coordinate_candidate_id,
            )
            for row in bazi_flow.candidates
        }
        self.assertEqual(len(bazi_flow.candidates), len(source_keys))

    def test_ziwei_selected_annual_change_does_not_recompute_bazi_target_flow(self) -> None:
        target = datetime(2026, 6, 1, 12, 0)
        base1, flow1, combined1 = self.combined_service.resolve_with_bundles(
            self._combined_request(target)
        )
        altered = replace(self.combined_request, ziwei_annual_year=2026)
        base2, flow2, combined2 = self.combined_service.resolve_with_bundles(
            self._combined_request(target, combined_request=altered)
        )
        self.assertNotEqual(base1.ziwei_bundle.bundle_hash, base2.ziwei_bundle.bundle_hash)
        self.assertEqual(flow1.bundle_hash, flow2.bundle_hash)
        self.assertEqual(
            combined1.bazi_target_flow_bundle_hash,
            combined2.bazi_target_flow_bundle_hash,
        )
        self.assertNotEqual(combined1.bundle_hash, combined2.bundle_hash)

    def test_combined_composition_is_identity_only_and_full_replay_rejects_bazi_rewrite(self) -> None:
        request = self._combined_request(datetime(2026, 6, 1, 12, 0))
        base, bazi_flow, combined = self.combined_service.resolve_with_bundles(request)
        self.assertEqual("INDEPENDENT_BUNDLE_IDENTITY_COMPOSITION_ONLY", combined.composition_semantics)
        self.assertEqual(base.manifest_hash, combined.base_combined_manifest_hash)
        self.assertEqual(base.ziwei_bundle.bundle_hash, combined.ziwei_bundle_hash)
        self.assertEqual(base.bazi_bundle.bundle_hash, combined.bazi_base_bundle_hash)
        self.assertEqual(bazi_flow.bundle_hash, combined.bazi_target_flow_bundle_hash)
        self.assertEqual(self.target_profile.profile_id, combined.target_coordinate_profile_id)
        self.assertEqual(self.target_profile.profile_version, combined.target_coordinate_profile_version)

        rewritten_flow = replace(
            bazi_flow,
            events=(*bazi_flow.events, "SYNTHETIC_12MR_REWRITE"),
        )
        replay = validate_combined_target_flow_full_replay(
            self.combined_service,
            request,
            base,
            rewritten_flow,
            combined,
        )
        self.assertEqual("FAIL", replay.status)
        self.assertIn("BAZI_TARGET_FLOW_FULL_REPLAY_MISMATCH", replay.diagnostics)


if __name__ == "__main__":
    unittest.main()
