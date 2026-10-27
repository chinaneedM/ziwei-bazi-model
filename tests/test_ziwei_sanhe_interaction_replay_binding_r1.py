from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.ziwei_application import (
    ApplicationBirthRequest,
    SanheInteractionRequest,
    ZiweiChartService,
    ZiweiSanheInteractionService,
    sanhe_interaction_bundle_hash,
    sanhe_interaction_source_fact_hash,
    sanhe_interaction_view_hash,
    validate_sanhe_interaction_full_replay,
    validate_sanhe_interaction_resolution,
    ziwei_application_default_presentation_profile,
)
from fortune_training.ziwei_chart import Sex, ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class ZiweiSanheInteractionReplayBindingR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        application_request = ApplicationBirthRequest(
            birth=BirthInput(
                reported_local_datetime=datetime(1994, 5, 17, 14, 30),
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            sex=Sex.MALE,
            calculation_profile=ziwei_chart_engine_v1_profile(registry),
            presentation_profile=ziwei_application_default_presentation_profile(),
            daxian_frame_id="DAXIAN:index=1",
            annual_year=2001,
            minor_limit_age=8,
        )
        cls.service = ZiweiSanheInteractionService(
            ZiweiChartService.from_repository(ROOT)
        )
        bundle = cls.service.base_service.resolve(application_request)
        origins = tuple(
            dict.fromkeys(row.origin_designation_id for row in bundle.r2_state.frame_facts)
        )
        if len(origins) < 2:
            raise AssertionError("fixture requires at least two valid origins")
        cls.request_a = SanheInteractionRequest(application_request, origins[0])
        cls.request_b = SanheInteractionRequest(application_request, origins[1])

    def test_structurally_valid_other_origin_still_fails_original_request_full_replay(self) -> None:
        bundle_a, result_a = self.service.resolve_with_bundle(self.request_a)
        bundle_b, result_b = self.service.resolve_with_bundle(self.request_b)
        self.assertEqual(bundle_a, bundle_b)

        rewritten = replace(
            result_a,
            selected_origin_designation_id=result_b.selected_origin_designation_id,
            selected_origin_address=result_b.selected_origin_address,
            relative_roles=result_b.relative_roles,
            sanfang_sizheng_frame=result_b.sanfang_sizheng_frame,
        )
        rewritten = replace(
            rewritten,
            source_fact_hash=sanhe_interaction_source_fact_hash(rewritten),
        )
        rewritten = replace(
            rewritten,
            view_hash=sanhe_interaction_view_hash(rewritten),
        )
        rewritten = replace(
            rewritten,
            bundle_hash=sanhe_interaction_bundle_hash(rewritten),
        )

        structural = validate_sanhe_interaction_resolution(bundle_a, rewritten)
        self.assertEqual("PASS", structural.status)
        replay = validate_sanhe_interaction_full_replay(
            self.service,
            self.request_a,
            bundle_a,
            rewritten,
        )
        self.assertEqual("FAIL", replay.status)
        self.assertIn("SANHE_INTERACTION_FULL_REPLAY_MISMATCH", replay.diagnostics)


if __name__ == "__main__":
    unittest.main()
