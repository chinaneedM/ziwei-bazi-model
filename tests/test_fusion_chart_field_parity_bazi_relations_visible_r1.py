from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.bazi_branch_relation_assets import (
    BAZI_BRANCH_RELATION_JS,
)
from fortune_training.combined_chart_application.bazi_stem_relation_assets import (
    BAZI_STEM_RELATION_JS,
)


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"
RELATIONS_PATH = ROOT / "src" / "fortune_training" / "bazi_chart" / "relations.py"
BRANCH_LOCAL_PATH = (
    ROOT
    / "src"
    / "fortune_training"
    / "combined_chart_application"
    / "bazi_branch_relation_local_app.py"
)
STEM_LOCAL_PATH = (
    ROOT
    / "src"
    / "fortune_training"
    / "combined_chart_application"
    / "bazi_stem_relation_local_app.py"
)


class FusionChartFieldParityBaziRelationsVisibleR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.rows = {row["field_id"]: row for row in matrix["fields"]}
        cls.relations_source = RELATIONS_PATH.read_text(encoding="utf-8")
        cls.branch_local_source = BRANCH_LOCAL_PATH.read_text(encoding="utf-8")
        cls.stem_local_source = STEM_LOCAL_PATH.read_text(encoding="utf-8")

    def test_natal_relation_rows_are_registered_visible(self) -> None:
        expected = {
            "BAZI_NATAL_BRANCH_RELATIONS": (
                "src/fortune_training/combined_chart_application/bazi_branch_relation_local_app.py",
                "src/fortune_training/combined_chart_application/bazi_branch_relation_assets.py",
            ),
            "BAZI_NATAL_STEM_FIVE_COMBINATIONS": (
                "src/fortune_training/combined_chart_application/bazi_stem_relation_local_app.py",
                "src/fortune_training/combined_chart_application/bazi_stem_relation_assets.py",
            ),
        }
        for field_id, (api_path, workbench_path) in expected.items():
            with self.subTest(field_id=field_id):
                row = self.rows[field_id]
                self.assertEqual("BAZI", row["system"])
                self.assertEqual("ALREADY_VISIBLE", row["status"])
                self.assertEqual("REFERENCE", row["priority"])
                self.assertEqual(
                    "src/fortune_training/bazi_chart/relations.py",
                    row["backend_evidence"]["path"],
                )
                self.assertEqual(api_path, row["api_evidence"]["path"])
                self.assertEqual(workbench_path, row["workbench_evidence"]["path"])

    def test_relation_sidecars_are_exact_natal_hash_bound(self) -> None:
        for name, source in (
            ("branch", self.branch_local_source),
            ("stem", self.stem_local_source),
        ):
            with self.subTest(sidecar=name):
                self.assertIn("natal_candidate_index", source)
                self.assertIn("source_natal_fact_hash", source)
                self.assertIn("source_natal_computation_hash", source)
                self.assertIn("natal_candidate.hashes.fact_hash", source)
                self.assertIn("natal_candidate.hashes.computation_hash", source)
                self.assertIn("NATAL_FACT_HASH_MISMATCH", source)
                self.assertIn("NATAL_COMPUTATION_HASH_MISMATCH", source)

        self.assertIn('_BRANCH_RELATION_PREFIX = "BRANCH_"', self.branch_local_source)
        self.assertIn(
            '_STEM_RELATION_FAMILY = "STEM_COMBINATION"',
            self.stem_local_source,
        )

    def test_backend_relations_are_reused_not_reimplemented_in_browser(self) -> None:
        for token in (
            "_STEM_COMBINATIONS",
            "_BRANCH_SIX_HARMONY",
            "_BRANCH_TRINES",
            "_BRANCH_CLASH",
            "_BRANCH_CHUAN",
            "_DIRECTED_PUNISHMENTS",
            'source_refs=("S14",)',
        ):
            with self.subTest(token=token):
                self.assertIn(token, self.relations_source)

        for browser_source in (BAZI_BRANCH_RELATION_JS, BAZI_STEM_RELATION_JS):
            self.assertNotIn("_STEM_COMBINATIONS", browser_source)
            self.assertNotIn("_BRANCH_SIX_HARMONY", browser_source)
            self.assertNotIn("generate_raw_relations", browser_source)

    def test_browser_contract_is_relation_identity_only(self) -> None:
        self.assertIn("RELATION_IDENTITY_ONLY", BAZI_BRANCH_RELATION_JS)
        self.assertIn("RELATION_IDENTITY_ONLY", BAZI_STEM_RELATION_JS)
        for family in (
            "BRANCH_SIX_HARMONY",
            "BRANCH_TRINE",
            "BRANCH_CLASH",
            "BRANCH_CHUAN",
            "BRANCH_PUNISHMENT",
        ):
            with self.subTest(family=family):
                self.assertIn(family, BAZI_BRANCH_RELATION_JS)
        self.assertIn("STEM_COMBINATION", BAZI_STEM_RELATION_JS)
        self.assertIn("不判合化", BAZI_BRANCH_RELATION_JS)
        self.assertIn("不判合化", BAZI_STEM_RELATION_JS)

        for forbidden in (
            "nominal_transformation_element",
            "winner",
            "喜用神",
            "五行强弱",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, BAZI_BRANCH_RELATION_JS)
                self.assertNotIn(forbidden, BAZI_STEM_RELATION_JS)

    def test_relation_rows_leave_no_stale_released_but_hidden_gap(self) -> None:
        for field_id in (
            "BAZI_NATAL_BRANCH_RELATIONS",
            "BAZI_NATAL_STEM_FIVE_COMBINATIONS",
        ):
            self.assertNotEqual(
                "ALREADY_RELEASED_NOT_YET_VISIBLE",
                self.rows[field_id]["status"],
            )


if __name__ == "__main__":
    unittest.main()
