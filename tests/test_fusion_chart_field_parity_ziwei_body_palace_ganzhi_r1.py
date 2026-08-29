from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.ziwei_basic_info_assets import ZIWEI_BASIC_INFO_JS


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"


class FusionChartFieldParityZiweiBodyPalaceGanzhiR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.rows = {row["field_id"]: row for row in matrix["fields"]}

    def test_body_palace_ganzhi_has_its_own_visible_inventory_row(self) -> None:
        row = self.rows["ZIWEI_BODY_PALACE_GANZHI"]
        self.assertEqual(row["system"], "ZIWEI")
        self.assertEqual(row["status"], "ALREADY_VISIBLE")
        self.assertEqual(row["priority"], "REFERENCE")
        self.assertIn("body_address", row["backend_evidence"]["symbol"])
        self.assertIn("address_attributes", row["backend_evidence"]["symbol"])
        self.assertEqual(
            row["workbench_evidence"]["path"],
            "src/fortune_training/combined_chart_application/ziwei_basic_info_assets.py",
        )
        self.assertIn("palaceGanzhi", row["workbench_evidence"]["symbol"])

    def test_branch_inventory_remains_branch_only(self) -> None:
        row = self.rows["ZIWEI_LIFE_BODY_PALACE_BRANCHES"]
        self.assertEqual(row["display_name"], "命宫支 / 身宫支")
        self.assertEqual(row["status"], "ALREADY_VISIBLE")
        self.assertIn("palace branches only", row["notes"])

    def test_workbench_body_ganzhi_is_released_data_identity_join(self) -> None:
        self.assertIn("function palaceGanzhi(structure, palaceAddress)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("structure.address_attributes", ZIWEI_BASIC_INFO_JS)
        self.assertIn("row?.address?.index === palaceAddress.index", ZIWEI_BASIC_INFO_JS)
        self.assertIn("row?.address?.branch === palaceAddress.branch", ZIWEI_BASIC_INFO_JS)
        self.assertIn("matches.length !== 1", ZIWEI_BASIC_INFO_JS)
        self.assertIn("item('身宫干支', palaceGanzhi(structure, structure.body_address))", ZIWEI_BASIC_INFO_JS)


if __name__ == "__main__":
    unittest.main()
