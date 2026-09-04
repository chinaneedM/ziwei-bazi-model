from __future__ import annotations

import unittest
from dataclasses import fields

from fortune_training.bazi_application.flow_models import BaziApplicationFlowCandidate
from fortune_training.combined_chart_application.target_flow_assets import (
    TARGET_FLOW_CSS,
    TARGET_FLOW_JS,
)


class CombinedBrowserBaziTemporalShenshaSidecarR1Tests(unittest.TestCase):
    def test_released_flow_candidate_shape_is_not_extended_for_shensha(self) -> None:
        names = {row.name for row in fields(BaziApplicationFlowCandidate)}
        self.assertNotIn("temporal_shensha", names)
        self.assertNotIn("temporal_shensha_projection", names)
        self.assertNotIn("shensha_projection", names)

    def test_browser_binds_sidecar_by_exact_flow_candidate_identity(self) -> None:
        self.assertIn("bazi_temporal_shensha_projection_bundle", TARGET_FLOW_JS)
        self.assertIn("source_bazi_target_flow_candidate_id", TARGET_FLOW_JS)
        self.assertIn("candidate.candidate_id", TARGET_FLOW_JS)
        self.assertIn("matches.length === 1 ? matches[0] : null", TARGET_FLOW_JS)
        self.assertNotIn("bundle.candidates[0]", TARGET_FLOW_JS)

    def test_all_dynamic_frame_cards_receive_separate_projection_slots(self) -> None:
        for expression in (
            "shenshaProjection?.dayun",
            "shenshaProjection?.xiaoyun_candidates?.[rowIndex]",
            "shenshaProjection?.annual",
            "shenshaProjection?.monthly",
            "shenshaProjection?.daily",
            "shenshaProjection?.hourly",
        ):
            with self.subTest(expression=expression):
                self.assertIn(expression, TARGET_FLOW_JS)

    def test_ui_wording_is_target_match_only_and_not_temporal_adjudication(self) -> None:
        self.assertIn("神煞候选目标命中", TARGET_FLOW_JS)
        self.assertIn(
            "仅为目标身份匹配；岁运神煞适用性尚未作古法/流派裁决。",
            TARGET_FLOW_JS,
        )
        self.assertIn(".bazi-flow-shensha-hit", TARGET_FLOW_CSS)
        self.assertIn(".bazi-flow-shensha-note", TARGET_FLOW_CSS)
        for forbidden in (
            "流年神煞",
            "流月神煞",
            "流日神煞",
            "流时神煞",
            "大运神煞",
            "小运神煞",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, TARGET_FLOW_JS)


if __name__ == "__main__":
    unittest.main()
