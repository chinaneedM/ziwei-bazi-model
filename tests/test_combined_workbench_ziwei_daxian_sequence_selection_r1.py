from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.local_app import LocalCombinedChartApplication
from fortune_training.combined_chart_application.local_app_assets import INDEX_HTML
from fortune_training.combined_chart_application.ziwei_basic_info_assets import ZIWEI_BASIC_INFO_JS


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"


class CombinedWorkbenchZiweiDaxianSequenceSelectionR1Tests(unittest.TestCase):
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

    def test_core_released_frame_identity_is_the_selection_value(self) -> None:
        temporal_state = self._resolve_temporal_state()
        rows = temporal_state["daxian_frames"]
        self.assertEqual("DAXIAN:index=1", rows[0]["frame_id"])
        self.assertEqual("DAXIAN:index=12", rows[-1]["frame_id"])
        self.assertEqual(12, len({row["frame_id"] for row in rows}))

    def test_workbench_has_existing_daxian_target_input(self) -> None:
        self.assertIn('id="ziwei-daxian-frame-id"', INDEX_HTML)
        self.assertIn('placeholder="DAXIAN:index=1"', INDEX_HTML)

    def test_sequence_click_copies_released_frame_id_into_existing_target(self) -> None:
        self.assertIn("function fillDaxianTarget(frameId)", ZIWEI_BASIC_INFO_JS)
        self.assertIn("const target = $('ziwei-daxian-frame-id')", ZIWEI_BASIC_INFO_JS)
        self.assertIn("target.value = frameId", ZIWEI_BASIC_INFO_JS)
        self.assertIn("target.dispatchEvent(new Event('input', { bubbles: true }))", ZIWEI_BASIC_INFO_JS)
        self.assertIn("target.dispatchEvent(new Event('change', { bubbles: true }))", ZIWEI_BASIC_INFO_JS)
        self.assertIn("document.createElement('button')", ZIWEI_BASIC_INFO_JS)
        self.assertIn("box.type = 'button'", ZIWEI_BASIC_INFO_JS)
        self.assertIn("box.addEventListener('click', () => fillDaxianTarget(row.frameId))", ZIWEI_BASIC_INFO_JS)
        self.assertIn("released 大限帧 · 点击填入目标", ZIWEI_BASIC_INFO_JS)

    def test_browser_does_not_construct_frame_identity_or_auto_submit(self) -> None:
        start = ZIWEI_BASIC_INFO_JS.index("function daxianSequence(temporalState)")
        end = ZIWEI_BASIC_INFO_JS.index("function annualSequence", start)
        daxian_projection = ZIWEI_BASIC_INFO_JS[start:end]
        for forbidden in (
            "DAXIAN:index=${",
            '"DAXIAN:index=" +',
            "'DAXIAN:index=' +",
            "requestSubmit(",
            ".submit(",
            "DaxianFrame",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, daxian_projection)

    def test_field_parity_remains_the_existing_full_sequence_field(self) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        rows = {row["field_id"]: row for row in matrix["fields"]}
        frames = rows["ZIWEI_DAXIAN_SEQUENCE_FRAMES"]
        self.assertEqual("ALREADY_VISIBLE", frames["status"])
        self.assertEqual("ZIWEI", frames["system"])
        self.assertIn("ZiweiTemporalState.daxian_frames", frames["backend_evidence"]["symbol"])
        self.assertIn("daxianSequence", frames["workbench_evidence"]["symbol"])
        self.assertIn("does not derive", frames["notes"])
        self.assertNotIn("ZIWEI_DAXIAN_SEQUENCE_SELECTION", rows)


if __name__ == "__main__":
    unittest.main()
