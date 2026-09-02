from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.palace_stem_topology_assets import (
    PALACE_STEM_TOPOLOGY_JS,
)
from fortune_training.ziwei_application.structural_relations import (
    STRUCTURAL_RELATION_PROJECTIONS_SEMANTIC_SCOPE,
)


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"
CLOSURE_AUDIT_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-CLOSURE-AUDIT-R1.md"


class ZiweiStructuralR6R8ProductClosureR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.rows = {row["field_id"]: row for row in matrix["fields"]}
        cls.audit = CLOSURE_AUDIT_PATH.read_text(encoding="utf-8")

    def test_r6_r7_r8_are_registered_as_visible_product_fields(self) -> None:
        expected = {
            "ZIWEI_QISHU_POSITION": (
                "src/fortune_training/ziwei_structural/r6/engine.py",
                "ZiweiQiShuPositionRuntime",
            ),
            "ZIWEI_ONE_SIX_COMMON_ROOT": (
                "src/fortune_training/ziwei_structural/r7/engine.py",
                "ZiweiOneSixCommonRootRuntime",
            ),
            "ZIWEI_ADJACENT_PALACE_PAIR": (
                "src/fortune_training/ziwei_structural/r8/engine.py",
                "ZiweiAdjacentPalaceRuntime",
            ),
        }
        for field_id, (backend_path, symbol) in expected.items():
            with self.subTest(field_id=field_id):
                row = self.rows[field_id]
                self.assertEqual(row["system"], "ZIWEI")
                self.assertEqual(row["status"], "ALREADY_VISIBLE")
                self.assertEqual(row["priority"], "REFERENCE")
                self.assertEqual(row["backend_evidence"]["path"], backend_path)
                self.assertEqual(row["backend_evidence"]["symbol"], symbol)
                self.assertEqual(
                    row["api_evidence"]["path"],
                    "src/fortune_training/ziwei_application/structural_relations.py",
                )
                self.assertEqual(
                    row["workbench_evidence"]["path"],
                    "src/fortune_training/combined_chart_application/palace_stem_topology_assets.py",
                )
                for evidence_key in (
                    "backend_evidence",
                    "api_evidence",
                    "workbench_evidence",
                ):
                    self.assertTrue((ROOT / row[evidence_key]["path"]).exists())

    def test_workbench_consumes_the_released_sidecar_without_recomputing_geometry(self) -> None:
        for expected in (
            "/api/ziwei-structural-relations",
            "ziwei_structural_relation_projections",
            "renderStructuralRelations",
            "qishu_facts",
            "one_six_facts",
            "adjacent_palace_pairs",
            "source_application_bundle_hash",
            "source_r2_fact_hash",
            "source_r2_computation_hash",
            "这里不成立夹宫/夹格",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, PALACE_STEM_TOPOLOGY_JS)

        for forbidden in (
            "project_qishu_positions",
            "project_one_six_common_roots",
            "project_adjacent_palace_pairs",
            "QISHU_RELATIVE_ORDINAL",
            "QISHU_CLOCKWISE_OFFSET",
            "OUTWARD_DISSIPATION",
            "INWARD_RECEPTION",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, PALACE_STEM_TOPOLOGY_JS)

    def test_r8_visibility_does_not_promote_flank_or_judgment_semantics(self) -> None:
        row = self.rows["ZIWEI_ADJACENT_PALACE_PAIR"]
        self.assertIn("flank_semantics_permission remains false", row["notes"])
        self.assertIn("no 夹宫/夹格成立判断", row["notes"])
        self.assertIn("NO_EVENT_ENDPOINT_SCORE_OR_FLANK_JUDGMENT", STRUCTURAL_RELATION_PROJECTIONS_SEMANTIC_SCOPE)
        self.assertIn("R8 adjacent-palace pair geometry", self.audit)
        self.assertIn("夹宫 / 夹格成立判断", self.audit)
        self.assertIn("pair-geometry strength", self.audit)

    def test_self_inward_direction_remains_not_formalized(self) -> None:
        direction = self.rows["ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION"]
        self.assertEqual(direction["status"], "NOT_YET_FORMALIZED")
        self.assertIn("must not be promoted", direction["notes"])
        self.assertIn(
            "`ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION` remains `NOT_YET_FORMALIZED`",
            self.audit,
        )

    def test_closure_audit_tracks_the_actual_r1_r8_release_chain(self) -> None:
        self.assertIn("CURRENT_STRUCTURAL_CLOSURE=R1-R8", self.audit)
        self.assertIn("Ziwei structural relations — CLOSED FOR RELEASED R1-R8", self.audit)
        for expected in (
            "R6 Qishu position projection",
            "R7 One-Six Common-Root projection",
            "R8 adjacent-palace pair geometry",
            "/api/ziwei-structural-relations",
            "field parity and product closure",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.audit)


if __name__ == "__main__":
    unittest.main()
