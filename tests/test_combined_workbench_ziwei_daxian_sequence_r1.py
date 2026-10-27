from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.local_app import LocalCombinedChartApplication
from fortune_training.combined_chart_application.ziwei_basic_info_assets import ZIWEI_BASIC_INFO_JS


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"


class CombinedWorkbenchZiweiDaxianSequenceR1Tests(unittest.TestCase):
    @staticmethod
    def _resolve_temporal_state() -> dict[str, object]:
        app = LocalCombinedChartApplication(ROOT)
        response = app.resolve_payload(
            {
                "birth_datetime": "1994-05-17T14:30",
                "birth_place": "Beijing",
                "latitude": 39.9042,
                "longitude": 116.4074,
                "timezone_id": "Asia/Shanghai",
                "sex": "MALE",
                "precision": "EXACT_SECOND",
                "uncertainty_seconds": 0,
                "ziwei_daxian_count": 12,
                "ziwei_daxian_frame_id": None,
                "ziwei_annual_year": None,
                "ziwei_lunar_month": None,
                "ziwei_minor_limit_age": None,
                "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
                "bazi_dayun_count": 12,
                "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
            }
        )
        return response["combined_resolution"]["ziwei_bundle"]["temporal_state"]

    def test_released_daxian_sequence_exposes_full_frame_identity(self) -> None:
        temporal_state = self._resolve_temporal_state()
        rows = temporal_state["daxian_frames"]
        self.assertEqual(12, len(rows))
        self.assertEqual(12, len({row["frame_id"] for row in rows}))
        self.assertEqual(12, len({row["index"] for row in rows}))
        self.assertEqual("DAXIAN:index=1", rows[0]["frame_id"])
        self.assertEqual("DAXIAN:index=12", rows[-1]["frame_id"])
        for row in rows:
            with self.subTest(frame_id=row["frame_id"]):
                self.assertIsInstance(row["index"], int)
                self.assertIsInstance(row["nominal_age_start"], int)
                self.assertIsInstance(row["nominal_age_end"], int)
                self.assertLessEqual(row["nominal_age_start"], row["nominal_age_end"])
                self.assertIsInstance(row["absolute_year_start"], int)
                self.assertIsInstance(row["absolute_year_end"], int)
                self.assertLessEqual(row["absolute_year_start"], row["absolute_year_end"])
                self.assertIsInstance(row["active_address"]["index"], int)
                self.assertTrue(row["active_address"]["branch"])
                self.assertTrue(row["active_palace_ganzhi"])
                self.assertTrue(row["active_palace_ganzhi"].endswith(row["active_address"]["branch"]))

    def test_browser_copy_projects_released_daxian_sequence_only(self) -> None:
        self.assertIn("function daxianSequence(temporalState)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("temporalState?.daxian_frames", ZIWEI_BASIC_INFO_JS)
        for released_field in (
            "row?.frame_id",
            "row?.index",
            "row?.nominal_age_start",
            "row?.nominal_age_end",
            "row?.absolute_year_start",
            "row?.absolute_year_end",
            "row?.active_address?.index",
            "row?.active_address?.branch",
            "row?.active_palace_ganzhi",
        ):
            with self.subTest(released_field=released_field):
                self.assertIn(released_field, ZIWEI_BASIC_INFO_JS)
        self.assertIn("frameIds.has(row.frame_id)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("indexes.has(row.index)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("function renderDaxianSequence(temporalState)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("renderDaxianSequence(ziweiBundle?.temporal_state)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("完整大限序列", ZIWEI_BASIC_INFO_JS)

    def test_browser_does_not_reimplement_daxian_generation_formula(self) -> None:
        for forbidden in (
            "context.life_address.index + direction * index",
            "context.bureau_number + index * 10",
            "nominal_age_start + 9",
            "context.ziwei_birth_year + nominal_age_start - 1",
            "frame_index = index + 1",
            "_daxian_direction",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, ZIWEI_BASIC_INFO_JS)

    def test_field_parity_separates_full_frames_from_sequence_metadata(self) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        rows = {row["field_id"]: row for row in matrix["fields"]}
        metadata = rows["ZIWEI_DAXIAN_SEQUENCE_METADATA"]
        frames = rows["ZIWEI_DAXIAN_SEQUENCE_FRAMES"]
        self.assertEqual("ALREADY_VISIBLE", metadata["status"])
        self.assertEqual("ALREADY_VISIBLE", frames["status"])
        self.assertEqual("ZIWEI", frames["system"])
        self.assertEqual("REFERENCE", frames["priority"])
        self.assertIn("ZiweiTemporalState.daxian_frames", frames["backend_evidence"]["symbol"])
        self.assertIn("ApplicationChartBundle.temporal_state", frames["api_evidence"]["symbol"])
        self.assertIn("daxianSequence", frames["workbench_evidence"]["symbol"])
        self.assertIn("does not derive", frames["notes"])
        self.assertNotEqual(metadata["display_name"], frames["display_name"])


if __name__ == "__main__":
    unittest.main()
