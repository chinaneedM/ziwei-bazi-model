from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.target_flow_assets import TARGET_FLOW_JS


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"
ANNOTATION_PATH = (
    ROOT
    / "src"
    / "fortune_training"
    / "bazi_application"
    / "temporal_annotations.py"
)
FLOW_SERVICE_PATH = (
    ROOT / "src" / "fortune_training" / "bazi_application" / "flow_service.py"
)
FLOW_LOCAL_APP_PATH = (
    ROOT
    / "src"
    / "fortune_training"
    / "combined_chart_application"
    / "flow_local_app.py"
)


class BaziTargetFlowClassicalAnnotationsProductClosureR1Tests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.rows = {row["field_id"]: row for row in matrix["fields"]}
        cls.annotation_source = ANNOTATION_PATH.read_text(encoding="utf-8")
        cls.flow_service_source = FLOW_SERVICE_PATH.read_text(encoding="utf-8")
        cls.flow_local_app_source = FLOW_LOCAL_APP_PATH.read_text(encoding="utf-8")

    def test_annotation_surface_is_registered_as_already_visible(self) -> None:
        row = self.rows["BAZI_TARGET_FLOW_CLASSICAL_ANNOTATIONS"]
        self.assertEqual(row["system"], "BAZI")
        self.assertEqual(row["status"], "ALREADY_VISIBLE")
        self.assertEqual(row["priority"], "REFERENCE")
        self.assertEqual(
            row["backend_evidence"]["path"],
            "src/fortune_training/bazi_application/temporal_annotations.py",
        )
        self.assertEqual(
            row["backend_evidence"]["symbol"],
            "temporal_classical_annotation_projection",
        )
        self.assertEqual(
            row["api_evidence"]["path"],
            "src/fortune_training/combined_chart_application/flow_local_app.py",
        )
        self.assertEqual(
            row["workbench_evidence"]["path"],
            "src/fortune_training/combined_chart_application/target_flow_assets.py",
        )
        self.assertEqual(
            row["workbench_evidence"]["symbol"],
            "frameCard + renderCandidate",
        )
        for evidence_key in (
            "backend_evidence",
            "api_evidence",
            "workbench_evidence",
        ):
            self.assertTrue((ROOT / row[evidence_key]["path"]).exists())

    def test_projection_covers_every_released_annotation_identity(self) -> None:
        for expected in (
            '"visible_ten_god"',
            '"hidden_stems"',
            '"nayin"',
            '"xunkong"',
            '"day_master_twelve_growth"',
            '"self_twelve_growth"',
            '"DAYUN"',
            '"XIAOYUN"',
            '"ANNUAL"',
            '"MONTHLY"',
            '"DAILY"',
            '"HOURLY"',
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.annotation_source)

    def test_candidate_and_predayun_boundaries_remain_explicit(self) -> None:
        for expected in (
            '"XIAOYUN_CANDIDATES_PRESERVED_NO_WINNER"',
            'unresolved_status="PRE_DAYUN_NO_GANZHI_ANNOTATION"',
            '"IDENTITY_ANNOTATIONS_ONLY_NO_STRENGTH_PATTERN_OR_INTERPRETATION"',
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.annotation_source)

    def test_application_and_endpoint_release_the_exact_projection(self) -> None:
        self.assertIn(
            'timeline["classical_annotations"] = temporal_classical_annotation_projection(',
            self.flow_service_source,
        )
        self.assertIn(
            '"bazi_target_flow_bundle": json_value(bazi_flow),',
            self.flow_local_app_source,
        )
        self.assertIn(
            'urlsplit(self.path).path != "/api/resolve-flow"',
            self.flow_local_app_source,
        )

    def test_workbench_directly_renders_released_annotation_fields(self) -> None:
        for expected in (
            "const annotations = view.timeline.classical_annotations;",
            "annotation.visible_ten_god.display_name",
            "annotation.hidden_stems.map",
            "annotation.nayin.display_name",
            "annotation.xunkong.display_name",
            "annotation.day_master_twelve_growth.phase",
            "annotation.self_twelve_growth.phase",
            "annotation_fact=${annotation.fact_hash}",
            "注释状态 ${annotationSlot.status}",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, TARGET_FLOW_JS)

    def test_inventory_boundary_adds_no_interpretive_semantics(self) -> None:
        notes = self.rows["BAZI_TARGET_FLOW_CLASSICAL_ANNOTATIONS"]["notes"]
        for expected in (
            "no browser annotation calculation",
            "XIAOYUN_CANDIDATES_PRESERVED_NO_WINNER",
            "PRE_DAYUN_NO_GANZHI_ANNOTATION",
            "No strength",
            "pattern",
            "useful/favorable element",
            "transformation-success",
            "auspiciousness",
            "interpretation",
            "prediction",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, notes)
        for forbidden in (
            "HIDDEN_STEMS",
            "ten_god(",
            "entry_for_ganzhi",
            "xunkong_for_ganzhi",
            "twelve_growth_for",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, TARGET_FLOW_JS)


if __name__ == "__main__":
    unittest.main()
