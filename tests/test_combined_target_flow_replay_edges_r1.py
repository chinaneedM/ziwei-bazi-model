from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_application import bazi_local_application_v1_profile
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_target_temporal import (
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
)
from fortune_training.bazi_temporal import bazi_temporal_v1_continuous_profile
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


class CombinedTargetFlowReplayEdgesR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
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
            ziwei_presentation_profile=(
                ziwei_application_default_presentation_profile()
            ),
            bazi_natal_profile=bazi_foundation_v1_profile(registry),
            bazi_temporal_profile=bazi_temporal_v1_continuous_profile(),
            bazi_application_profile=bazi_local_application_v1_profile(),
            combined_profile=combined_chart_application_v1_profile(),
            ziwei_annual_year=2025,
            ziwei_daxian_count=12,
            bazi_dayun_count=12,
        )
        cls.target_profile = bazi_target_temporal_coordinate_r1_profile()
        cls.service = CombinedTargetFlowService.from_repository(ROOT)

    @classmethod
    def _request(cls, *, uncertainty_seconds: int = 0):
        return CombinedTargetFlowRequest(
            combined_request=cls.combined_request,
            target_input=TargetTemporalInput(
                reported_local_datetime=datetime(2026, 6, 1, 12, 0),
                target_place="Greenwich",
                latitude=51.4769,
                longitude=0.0,
                timezone_id="Etc/UTC",
                uncertainty_seconds=uncertainty_seconds,
            ),
            target_coordinate_profile=cls.target_profile,
        )

    def test_target_uncertainty_preserves_upstream_bazi_flow_multiplicity(self) -> None:
        _, bazi_flow, combined_flow = self.service.resolve_with_bundles(
            self._request(uncertainty_seconds=120)
        )
        self.assertEqual("MULTI_CANDIDATE", bazi_flow.status)
        self.assertGreater(len(bazi_flow.candidates), 1)
        self.assertEqual("UNCERTAINTY_PRESENT", combined_flow.status)
        self.assertEqual(
            bazi_flow.bundle_hash,
            combined_flow.bazi_target_flow_bundle_hash,
        )

    def test_bazi_target_flow_object_rewrite_fails_combined_full_replay(self) -> None:
        request = self._request()
        base, bazi_flow, combined_flow = self.service.resolve_with_bundles(request)
        rewritten_flow = replace(
            bazi_flow,
            events=(*bazi_flow.events, "SYNTHETIC_COMBINED_REPLAY_TAMPER"),
        )
        report = validate_combined_target_flow_full_replay(
            self.service,
            request,
            base,
            rewritten_flow,
            combined_flow,
        )
        self.assertEqual("FAIL", report.status)
        self.assertIn("BAZI_TARGET_FLOW_FULL_REPLAY_MISMATCH", report.diagnostics)


if __name__ == "__main__":
    unittest.main()
