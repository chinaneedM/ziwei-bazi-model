from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.palace_stem_topology_assets import (
    PALACE_STEM_TOPOLOGY_JS,
)
from fortune_training.ziwei_application.palace_stem_topology import (
    PALACE_STEM_TOPOLOGY_CLASSIFICATION_POLICY,
    PALACE_STEM_TOPOLOGY_PROFILE_ID,
    PALACE_STEM_TOPOLOGY_SCHEMA,
    PALACE_STEM_TOPOLOGY_SELECTION_SEMANTICS,
    PALACE_STEM_TOPOLOGY_SEMANTIC_SCOPE,
    TOPOLOGY_RELATIONS,
)


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "ZIWEI-PALACE-STEM-TRANSFORMATION-TOPOLOGY-R1.md"
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"


class ZiweiPalaceStemTopologyReleaseContractR1Tests(unittest.TestCase):
    def test_runtime_semantics_are_geometry_only(self) -> None:
        self.assertEqual(
            PALACE_STEM_TOPOLOGY_SCHEMA,
            "ZIWEI-PALACE-STEM-TRANSFORMATION-TOPOLOGY-SIDECAR-R1",
        )
        self.assertEqual(
            PALACE_STEM_TOPOLOGY_PROFILE_ID,
            "ZIWEI-PALACE-STEM-TRANSFORMATION-TOPOLOGY-R1",
        )
        self.assertEqual(
            PALACE_STEM_TOPOLOGY_CLASSIFICATION_POLICY,
            "GEOMETRIC_SAME_OPPOSITE_OTHER_ONLY",
        )
        self.assertEqual(
            PALACE_STEM_TOPOLOGY_SELECTION_SEMANTICS,
            "NO_SELF_OR_INWARD_DIRECTION_CLASSIFICATION_NO_WINNER",
        )
        self.assertEqual(
            PALACE_STEM_TOPOLOGY_SEMANTIC_SCOPE,
            "PALACE_STEM_TARGET_TOPOLOGY_ONLY_NO_SELF_TRANSFORMATION_DIRECTION_OR_INTERPRETATION",
        )
        self.assertEqual(
            set(TOPOLOGY_RELATIONS),
            {"SAME_PALACE", "OPPOSITE_PALACE", "OTHER_PALACE"},
        )

    def test_release_doc_records_product_and_direction_boundaries(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")
        for expected in (
            PALACE_STEM_TOPOLOGY_SCHEMA,
            PALACE_STEM_TOPOLOGY_PROFILE_ID,
            PALACE_STEM_TOPOLOGY_CLASSIFICATION_POLICY,
            PALACE_STEM_TOPOLOGY_SELECTION_SEMANTICS,
            PALACE_STEM_TOPOLOGY_SEMANTIC_SCOPE,
            "12 × 4 = 48",
            "POST /api/ziwei-palace-stem-topology",
            "ZIWEI_PALACE_STEM_TRANSFORMATION_TOPOLOGY = ALREADY_VISIBLE",
            "ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION = NOT_YET_FORMALIZED",
            "SAME_PALACE -> OUTWARD_DISSIPATION",
            "OPPOSITE_PALACE -> INWARD_RECEPTION",
            "候选",
            "不自动选 winner",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_field_parity_matrix_keeps_visibility_separate_from_direction(self) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        rows = {row["field_id"]: row for row in matrix["fields"]}

        topology = rows["ZIWEI_PALACE_STEM_TRANSFORMATION_TOPOLOGY"]
        self.assertEqual(topology["status"], "ALREADY_VISIBLE")
        self.assertEqual(
            topology["backend_evidence"]["path"],
            "src/fortune_training/ziwei_application/palace_stem_topology.py",
        )
        self.assertIn("Topology only", topology["notes"])
        self.assertIn("must not be promoted", topology["notes"])

        direction = rows["ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION"]
        self.assertEqual(direction["status"], "NOT_YET_FORMALIZED")
        self.assertEqual(
            direction["backend_evidence"]["path"],
            "sources/canonical/S08_十干四化自化与禄忌线库.txt",
        )
        self.assertIn("mechanical selector", direction["backend_evidence"]["claim"])
        self.assertIn("must not be promoted by geometry alone", direction["notes"])

    def test_workbench_does_not_smuggle_direction_semantics_into_geometry(self) -> None:
        for backend_field in (
            "topology.classification_policy",
            "topology.selection_semantics",
            "topology.semantic_scope",
            "topology.source_transformation_rule_set_id",
            "topology.source_application_bundle_hash",
            "row.topology_relation",
        ):
            with self.subTest(backend_field=backend_field):
                self.assertIn(backend_field, PALACE_STEM_TOPOLOGY_JS)

        self.assertIn(
            "同宫 / 对宫 / 其他宫不等于离心 / 向心自化",
            PALACE_STEM_TOPOLOGY_JS,
        )
        for forbidden in (
            "OUTWARD_DISSIPATION",
            "INWARD_RECEPTION",
            "SELF_LU",
            "SELF_QUAN",
            "SELF_KE",
            "SELF_JI",
            "OPPOSITE_LU",
            "OPPOSITE_QUAN",
            "OPPOSITE_KE",
            "OPPOSITE_JI",
            "S08-ASG-",
            "TransformationGenerator",
            "+ 6",
            "% 12",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, PALACE_STEM_TOPOLOGY_JS)


if __name__ == "__main__":
    unittest.main()
