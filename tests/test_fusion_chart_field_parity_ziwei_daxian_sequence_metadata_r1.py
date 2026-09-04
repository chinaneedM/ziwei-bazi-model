from __future__ import annotations

import json
import unittest
from dataclasses import fields
from pathlib import Path

from fortune_training.ziwei_application.svg import SVG_RENDERER_VERSION
from fortune_training.ziwei_chart.view import (
    VIEW_PROJECTION_ALGORITHM_VERSION,
    ViewDaxianSequenceMetadata,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiDaxianSequenceMetadataParityR1Tests(unittest.TestCase):
    def test_parity_matrix_registers_released_surface(self) -> None:
        matrix = json.loads((ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json").read_text(encoding="utf-8"))
        rows = {row["field_id"]: row for row in matrix["fields"]}
        row = rows["ZIWEI_DAXIAN_SEQUENCE_METADATA"]
        self.assertEqual("ZIWEI", row["system"])
        self.assertEqual("ALREADY_VISIBLE", row["status"])
        self.assertEqual("src/fortune_training/ziwei_chart/temporal.py", row["backend_evidence"]["path"])
        self.assertEqual("src/fortune_training/ziwei_chart/view.py", row["api_evidence"]["path"])
        self.assertEqual("src/fortune_training/ziwei_application/svg.py", row["workbench_evidence"]["path"])

    def test_view_contract_is_exact_and_versioned(self) -> None:
        self.assertEqual("1.2.0", VIEW_PROJECTION_ALGORITHM_VERSION)
        self.assertEqual(
            ["daxian_direction", "first_daxian_nominal_age"],
            [field.name for field in fields(ViewDaxianSequenceMetadata)],
        )

    def test_strict_schema_has_no_extra_sequence_fields(self) -> None:
        schema = json.loads((ROOT / "schemas" / "ziwei-chart-view-v1.schema.json").read_text(encoding="utf-8"))
        self.assertIn("daxian_sequence_metadata", schema["required"])
        definition = schema["$defs"]["daxianSequenceMetadata"]
        self.assertFalse(definition["additionalProperties"])
        self.assertEqual(
            {"daxian_direction", "first_daxian_nominal_age"},
            set(definition["properties"]),
        )
        self.assertEqual(["FORWARD", "REVERSE"], definition["properties"]["daxian_direction"]["enum"])

    def test_svg_is_server_side_and_workbench_does_not_derive_metadata(self) -> None:
        self.assertEqual("1.4.0", SVG_RENDERER_VERSION)
        svg_source = (ROOT / "src" / "fortune_training" / "ziwei_application" / "svg.py").read_text(encoding="utf-8")
        self.assertIn("view.daxian_sequence_metadata", svg_source)
        self.assertIn("大限序列:", svg_source)

        workbench_source = (
            ROOT / "src" / "fortune_training" / "combined_chart_application" / "local_app_assets.py"
        ).read_text(encoding="utf-8")
        self.assertIn("zroot.innerHTML=d.ziwei_svg", workbench_source)
        self.assertNotIn("daxian_sequence_metadata", workbench_source)


if __name__ == "__main__":
    unittest.main()
