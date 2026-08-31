from __future__ import annotations

import unittest
from pathlib import Path

from fortune_training.combined_chart_application.target_flow_assets import TARGET_FLOW_JS


ROOT = Path(__file__).resolve().parents[1]
SMOKE_PATH = ROOT / "scripts" / "combined-workbench-smoke.py"
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"


class BaziTemporalShenshaWorkbenchContractR1Tests(unittest.TestCase):
    def test_workbench_consumes_sidecar_lineage_without_recomputing_shensha(self) -> None:
        for released_field in (
            "bazi_temporal_shensha_projection_bundle",
            "source_bazi_target_flow_candidate_id",
            "target_coordinate_candidate_id",
            "source_application_candidate_ids",
            "source_application_view_hashes",
            "source_shensha_hash",
            "projection_profile_id",
            "base_application_bundle_hash",
            "bazi_target_flow_bundle_hash",
            "temporal_shensha_projection_fact",
            "temporal_shensha_projection_computation",
            "temporal_shensha_integrity",
        ):
            with self.subTest(released_field=released_field):
                self.assertIn(released_field, TARGET_FLOW_JS)

        self.assertIn(
            "row.source_bazi_target_flow_candidate_id === candidate.candidate_id",
            TARGET_FLOW_JS,
        )
        self.assertIn("row.temporal_applicability_status", TARGET_FLOW_JS)
        self.assertIn("row.source_refs", TARGET_FLOW_JS)
        for forbidden in (
            "temporal_shensha_target_projection(",
            "project_temporal_shensha(",
            "SEXAGENARY_INDEX",
            "matched_value not in",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, TARGET_FLOW_JS)

    def test_smoke_validates_temporal_shensha_sidecar_at_workbench_boundary(self) -> None:
        source = SMOKE_PATH.read_text(encoding="utf-8")
        for expected in (
            "BAZI-TEMPORAL-SHENSHA-PROJECTION-SIDECAR-R1",
            "SOURCE_CANDIDATES_PRESERVED_NO_WINNER",
            "TARGET_IDENTITY_MATCH_ONLY_NO_AUSPICIOUSNESS_OR_TEMPORAL_RULE_ADJUDICATION",
            "bazi_temporal_shensha_candidate_count",
            "bazi_temporal_shensha_projection_slot_count",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, source)
        for forbidden in (
            "temporal_shensha_target_projection",
            "validate_temporal_shensha_target_projection",
            "SEXAGENARY_INDEX",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)

    def test_field_parity_matrix_registers_temporal_shensha_product_surface(self) -> None:
        text = MATRIX_PATH.read_text(encoding="utf-8")
        self.assertIn('"field_id":"BAZI_TARGET_TEMPORAL_SHENSHA_PROJECTION"', text)
        self.assertIn('"status":"ALREADY_VISIBLE"', text)
        self.assertIn("TARGET_IDENTITY_MATCH_ONLY", text)
        self.assertIn("no winner", text.lower())


if __name__ == "__main__":
    unittest.main()
