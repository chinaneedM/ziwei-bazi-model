from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = json.loads((ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json").read_text(encoding="utf-8"))
TEMPORAL = (ROOT / "src" / "fortune_training" / "ziwei_chart" / "temporal.py").read_text(encoding="utf-8")
VIEW = (ROOT / "src" / "fortune_training" / "ziwei_chart" / "view.py").read_text(encoding="utf-8")
SVG = (ROOT / "src" / "fortune_training" / "ziwei_application" / "svg.py").read_text(encoding="utf-8")


class FusionChartFieldParityZiweiTemporalReleasedSurfaceR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = {row["field_id"]: row for row in MATRIX["fields"]}

    def _visible_row(self, field_id: str, backend_symbol: str, api_symbol: str) -> dict:
        row = self.rows[field_id]
        self.assertEqual("ZIWEI", row["system"])
        self.assertEqual("ALREADY_VISIBLE", row["status"])
        self.assertEqual("src/fortune_training/ziwei_chart/temporal.py", row["backend_evidence"]["path"])
        self.assertIn(backend_symbol, row["backend_evidence"]["symbol"])
        self.assertEqual("src/fortune_training/ziwei_chart/view.py", row["api_evidence"]["path"])
        self.assertIn(api_symbol, row["api_evidence"]["symbol"])
        self.assertEqual("src/fortune_training/ziwei_application/svg.py", row["workbench_evidence"]["path"])
        return row

    def test_temporal_designations_are_registered_as_released_visible_view_data(self) -> None:
        row = self._visible_row(
            "ZIWEI_TEMPORAL_DESIGNATIONS",
            "designation_overlay",
            "ViewDesignationOverlay",
        )
        for field_name in ("frame_type", "frame_id", "designation_id", "label"):
            self.assertIn(field_name, row["api_evidence"]["claim"])
        self.assertIn("designation_overlay: tuple[DesignationBinding, ...]", TEMPORAL)
        self.assertIn("class ViewDesignationOverlay:", VIEW)
        self.assertIn("temporal_designations: tuple[ViewDesignationOverlay, ...]", VIEW)
        self.assertIn('lines.extend("时: "', SVG)

    def test_selected_temporal_transformations_are_registered_without_browser_recalculation(self) -> None:
        row = self._visible_row(
            "ZIWEI_TEMPORAL_TRANSFORMATION_BADGES",
            "transformations",
            "ViewPlacement.transformation_badges",
        )
        self.assertIn("selected DAXIAN/ANNUAL/MONTH", row["api_evidence"]["claim"])
        self.assertIn("transformations: tuple[TransformationActivation, ...]", TEMPORAL)
        self.assertIn("activation_sets.append(daxian.transformations)", VIEW)
        self.assertIn("activation_sets.append(annual.transformations)", VIEW)
        self.assertIn("activation_sets.append(monthly.transformations)", VIEW)
        self.assertIn("transformation_badges=tuple(sorted(transformation_by_entity.get(row.entity_id, ())))", VIEW)
        self.assertIn("row.transformation_badges", SVG)

    def test_non_candidate_temporal_auxiliaries_are_registered_with_exact_released_fields(self) -> None:
        row = self._visible_row(
            "ZIWEI_TEMPORAL_AUXILIARIES",
            "auxiliary_activations",
            "ViewTemporalAuxiliary",
        )
        for field_name in ("frame_type", "frame_id", "entity_id", "label"):
            self.assertIn(field_name, row["api_evidence"]["claim"])
        self.assertNotIn("candidate_fact_hash", row["api_evidence"]["claim"])
        self.assertIn("auxiliary_activations: tuple[TemporalAuxiliaryActivation, ...]", TEMPORAL)
        self.assertIn("class ViewTemporalAuxiliary:", VIEW)
        self.assertIn("temporal_auxiliaries: tuple[ViewTemporalAuxiliary, ...]", VIEW)
        self.assertIn('lines.extend("流曜: "', SVG)

    def test_minor_limit_and_doujun_palace_markers_are_registered_as_view_projection_only(self) -> None:
        minor = self._visible_row(
            "ZIWEI_MINOR_LIMIT_PALACE",
            "MinorLimitFrame.active_address",
            "PalaceViewCell.minor_limit_frame_ids",
        )
        doujun = self._visible_row(
            "ZIWEI_DOUJUN_PALACE",
            "AnnualFrame.doujun_address",
            "PalaceViewCell.doujun_frame_ids",
        )
        self.assertIn("frame_id", minor["api_evidence"]["claim"])
        self.assertIn("frame_id", doujun["api_evidence"]["claim"])
        self.assertIn("class MinorLimitFrame:", TEMPORAL)
        self.assertIn("doujun_address: Address", TEMPORAL)
        self.assertIn("minor_by_address[minor.active_address.index].append(minor.frame_id)", VIEW)
        self.assertIn("doujun_by_address[annual.doujun_address.index].append(annual.frame_id)", VIEW)
        self.assertIn('"小限: " + row', SVG)
        self.assertIn('"斗君: " + row', SVG)

    def test_candidate_only_contract_remains_separate(self) -> None:
        row = self.rows["ZIWEI_TEMPORAL_AUXILIARY_CANDIDATES"]
        self.assertEqual("DISPUTED_CANDIDATE_ONLY", row["status"])
        self.assertNotEqual("ZIWEI_TEMPORAL_AUXILIARIES", row["field_id"])


if __name__ == "__main__":
    unittest.main()
