from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.target_flow_assets import TARGET_FLOW_JS


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"
BAZI_FLOW_SERVICE_PATH = (
    ROOT / "src" / "fortune_training" / "bazi_application" / "flow_service.py"
)
FLOW_LOCAL_APP_PATH = (
    ROOT
    / "src"
    / "fortune_training"
    / "combined_chart_application"
    / "flow_local_app.py"
)
TARGET_FLOW_ASSETS_PATH = (
    ROOT
    / "src"
    / "fortune_training"
    / "combined_chart_application"
    / "target_flow_assets.py"
)


class BaziTargetFlowTimelineProductClosureR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.rows = {row["field_id"]: row for row in matrix["fields"]}
        cls.application_flow_source = BAZI_FLOW_SERVICE_PATH.read_text(
            encoding="utf-8"
        )
        cls.flow_local_app_source = FLOW_LOCAL_APP_PATH.read_text(encoding="utf-8")
        render_tail = TARGET_FLOW_JS.split("function renderCandidate", 1)[1]
        cls.render_candidate = render_tail.split("async function resolveFlow", 1)[0]

    def test_target_flow_timeline_is_registered_as_already_visible(self) -> None:
        row = self.rows["BAZI_TARGET_FLOW_TIMELINE"]
        self.assertEqual(row["system"], "BAZI")
        self.assertEqual(row["status"], "ALREADY_VISIBLE")
        self.assertEqual(row["priority"], "REFERENCE")
        self.assertEqual(
            row["backend_evidence"]["path"],
            "src/fortune_training/bazi_application/flow_service.py",
        )
        self.assertEqual(
            row["backend_evidence"]["symbol"],
            "BaziApplicationFlowService._build_view",
        )
        self.assertEqual(
            row["api_evidence"]["path"],
            "src/fortune_training/combined_chart_application/flow_local_app.py",
        )
        self.assertEqual(
            row["workbench_evidence"]["path"],
            "src/fortune_training/combined_chart_application/target_flow_assets.py",
        )
        self.assertEqual(row["workbench_evidence"]["symbol"], "renderCandidate")
        for evidence_key in (
            "backend_evidence",
            "api_evidence",
            "workbench_evidence",
        ):
            with self.subTest(evidence_key=evidence_key):
                self.assertTrue((ROOT / row[evidence_key]["path"]).exists())

    def test_application_releases_unified_target_timeline_without_interpretation(self) -> None:
        for expected in (
            '"schema": "BAZI-UNIFIED-TARGET-TIMELINE-R1"',
            '"NATAL"',
            '"DAYUN"',
            '"XIAOYUN"',
            '"ANNUAL"',
            '"MONTHLY"',
            '"DAILY"',
            '"HOURLY"',
            '"selection_status": "UNRESOLVED_CLASSICAL_METHOD_ALTERNATIVES"',
            '"semantic_scope": "TEMPORAL_COORDINATES_ONLY_NO_INTERPRETATION"',
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.application_flow_source)

    def test_flow_endpoint_releases_exact_bazi_target_flow_bundle(self) -> None:
        self.assertIn('"bazi_target_flow_bundle": json_value(bazi_flow),', self.flow_local_app_source)
        self.assertIn('urlsplit(self.path).path != "/api/resolve-flow"', self.flow_local_app_source)

    def test_workbench_directly_consumes_released_target_layers(self) -> None:
        for expected in (
            "const flow = view.flow;",
            "const annotations = view.timeline.classical_annotations;",
            "view.timeline.xiaoyun.candidates.forEach",
            "'大运', dayun, flow.active_dayun_kind",
            "frameCard('流年', flow.annual",
            "frameCard('流月', flow.monthly",
            "frameCard('流日', view.daily",
            "frameCard('流时', view.hourly",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.render_candidate)

    def test_inventory_boundary_remains_non_interpretive(self) -> None:
        notes = self.rows["BAZI_TARGET_FLOW_TIMELINE"]["notes"]
        for expected in (
            "no browser recomputation",
            "Candidate-preserved Xiaoyun",
            "strength",
            "favorable-element",
            "auspiciousness",
            "prediction",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, notes)
        self.assertNotIn("winner", self.render_candidate.lower())


if __name__ == "__main__":
    unittest.main()
