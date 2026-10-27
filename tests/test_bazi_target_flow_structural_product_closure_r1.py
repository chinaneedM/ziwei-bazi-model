from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.target_flow_assets import TARGET_FLOW_JS


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"
STRUCTURAL_PROJECTION_PATH = (
    ROOT
    / "src"
    / "fortune_training"
    / "bazi_application"
    / "structural_projection.py"
)
SUPPORT_PROJECTION_PATH = (
    ROOT
    / "src"
    / "fortune_training"
    / "bazi_application"
    / "structural_support_projection.py"
)
FLOW_LOCAL_APP_PATH = (
    ROOT
    / "src"
    / "fortune_training"
    / "combined_chart_application"
    / "flow_local_app.py"
)


class BaziTargetFlowStructuralProductClosureR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.rows = {row["field_id"]: row for row in matrix["fields"]}
        cls.structural_source = STRUCTURAL_PROJECTION_PATH.read_text(encoding="utf-8")
        cls.support_source = SUPPORT_PROJECTION_PATH.read_text(encoding="utf-8")
        cls.flow_local_app_source = FLOW_LOCAL_APP_PATH.read_text(encoding="utf-8")

    def test_both_released_structural_surfaces_are_registered_visible(self) -> None:
        expected = {
            "BAZI_TARGET_FLOW_STRUCTURAL_PROJECTION": (
                "src/fortune_training/bazi_application/structural_projection.py",
                "structural_projection",
                "renderStructural",
            ),
            "BAZI_TARGET_FLOW_STRUCTURAL_SUPPORT_PROJECTION": (
                "src/fortune_training/bazi_application/structural_support_projection.py",
                "structural_support_projection",
                "renderStructuralSupport",
            ),
        }
        for field_id, (backend_path, backend_symbol, workbench_symbol) in expected.items():
            with self.subTest(field_id=field_id):
                row = self.rows[field_id]
                self.assertEqual(row["system"], "BAZI")
                self.assertEqual(row["status"], "ALREADY_VISIBLE")
                self.assertEqual(row["priority"], "REFERENCE")
                self.assertEqual(row["backend_evidence"]["path"], backend_path)
                self.assertEqual(row["backend_evidence"]["symbol"], backend_symbol)
                self.assertEqual(
                    row["api_evidence"]["path"],
                    "src/fortune_training/combined_chart_application/flow_local_app.py",
                )
                self.assertEqual(
                    row["workbench_evidence"]["path"],
                    "src/fortune_training/combined_chart_application/target_flow_assets.py",
                )
                self.assertEqual(
                    row["workbench_evidence"]["symbol"], workbench_symbol
                )
                for evidence_key in (
                    "backend_evidence",
                    "api_evidence",
                    "workbench_evidence",
                ):
                    self.assertTrue((ROOT / row[evidence_key]["path"]).exists())

    def test_structural_projection_contract_keeps_exact_neutral_coverage(self) -> None:
        for expected in (
            '"BAZI-TARGET-FLOW-STRUCTURAL-PROJECTION-R1"',
            'STRUCTURAL_SUPPORTED_LAYERS = ("DAYUN", "ANNUAL", "MONTHLY")',
            'STRUCTURAL_EXCLUDED_LAYERS = ("XIAOYUN", "DAILY", "HOURLY")',
            '"NEUTRAL_STRUCTURAL_OCCURRENCES_ONLY_NO_EFFECT_STRENGTH_OR_TRANSFORMATION_SUCCESS"',
            '"dynamic_exposures"',
            '"dynamic_affinities"',
            '"relations"',
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.structural_source)

    def test_support_projection_contract_preserves_roles_and_candidates(self) -> None:
        for expected in (
            '"BAZI-TARGET-FLOW-STRUCTURAL-SUPPORT-PROJECTION-R1"',
            '"NEUTRAL_SUPPORT_EVIDENCE_CANDIDATES_ONLY_NO_ROOT_STRENGTH_OR_WEIGHT"',
            'NATAL_MONTH_COMMAND = "NATAL_MONTH_COMMAND"',
            'ACTIVE_FLOW_SOLAR_MONTH = "ACTIVE_FLOW_SOLAR_MONTH"',
            'EXACT_HIDDEN_STEM_MATCH = "EXACT_HIDDEN_STEM_MATCH"',
            'SAME_ELEMENT_HIDDEN_SUPPORT = "SAME_ELEMENT_HIDDEN_SUPPORT"',
            '"support_evidence_candidates"',
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.support_source)

    def test_flow_endpoint_releases_the_exact_containing_bundle(self) -> None:
        self.assertIn(
            '"bazi_target_flow_bundle": json_value(bazi_flow),',
            self.flow_local_app_source,
        )
        self.assertIn(
            'urlsplit(self.path).path != "/api/resolve-flow"',
            self.flow_local_app_source,
        )

    def test_workbench_consumes_structural_and_support_objects_separately(self) -> None:
        for expected in (
            "renderStructural(view.structural)",
            "structural.active_temporal_stems.forEach",
            "structural.temporal_hidden_stems.filter",
            "structural.dynamic_exposures.forEach",
            "structural.dynamic_affinities.forEach",
            "structural.relations.forEach",
            "renderStructuralSupport(view.structural_support)",
            "support.natal_month_command",
            "support.active_flow_solar_month",
            "support.support_evidence_candidates.forEach",
            "candidate.source_affinity_fact_id",
            "candidate.source_exposure_link_ids.join",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, TARGET_FLOW_JS)

    def test_inventory_boundary_adds_no_effect_or_root_verdict(self) -> None:
        structural_notes = self.rows[
            "BAZI_TARGET_FLOW_STRUCTURAL_PROJECTION"
        ]["notes"]
        support_notes = self.rows[
            "BAZI_TARGET_FLOW_STRUCTURAL_SUPPORT_PROJECTION"
        ]["notes"]
        for expected in (
            "Xiaoyun/Daily/Hourly",
            "Nominal transformation element is metadata only",
            "no effect",
            "strength",
            "winner",
            "transformation-success",
            "prediction",
        ):
            with self.subTest(surface="structural", expected=expected):
                self.assertIn(expected, structural_notes)
        for expected in (
            "not ROOT/NO_ROOT",
            "得令",
            "strength",
            "weight",
            "score",
            "rank",
            "winner",
            "prediction",
        ):
            with self.subTest(surface="support", expected=expected):
                self.assertIn(expected, support_notes)
        for forbidden in (
            "generate_raw_relations",
            "BaziStructuralEngine",
            "BaziStructuralSupportEngine",
            "HIDDEN_STEMS",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, TARGET_FLOW_JS)


if __name__ == "__main__":
    unittest.main()
