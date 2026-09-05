from __future__ import annotations

import json
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs" / "research" / "MING-DATONG-1569-TIME-COORDINATE-R1.json"


class MingDatong1569TimeCoordinateR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_internal_day_and_ke_coordinate_is_source_closed(self) -> None:
        self.assertEqual(self.data["schema"], "MING-DATONG-1569-TIME-COORDINATE-R1")
        internal = self.data["internal_coordinate"]
        self.assertEqual(internal["day_cycle_source_units"], 10000)
        self.assertEqual(internal["ke_per_day"], 100)
        self.assertEqual(internal["fen_per_ke"], 100)
        self.assertEqual(internal["miao_per_fen"], 100)
        self.assertEqual(internal["computational_day_boundary"], "ZI_ZHENG")
        self.assertEqual(internal["computational_zero_label"], "子正")
        self.assertEqual(internal["ke_per_day"] * internal["fen_per_ke"], internal["day_cycle_source_units"])

    def test_ming_worked_example_replays_source_shortcut_arithmetic(self) -> None:
        replay = self.data["ming_worked_replay"]
        scaled = Decimal(replay["small_remainder_source_units"]) * Decimal(replay["normalized_shortcut_multiplier"])
        self.assertEqual(scaled, Decimal(replay["expected_scaled_value"]))
        self.assertEqual(replay["recorded_clock_label"], "乙丑日午正初刻")

    def test_calendar_day_boundary_cannot_select_bazi_or_ziwei_policy(self) -> None:
        boundary = self.data["boundary_semantics"]
        firewalls = self.data["scope_firewalls"]
        self.assertEqual(boundary["boundary"], "ZI_ZHENG")
        self.assertTrue(firewalls["astrological_day_boundary_inference_forbidden"])
        self.assertTrue(firewalls["bazi_day_boundary_selection_forbidden"])
        self.assertTrue(firewalls["ziwei_day_boundary_selection_forbidden"])

    def test_geographic_qishuo_reference_remains_fail_closed(self) -> None:
        geography = self.data["geographic_realization"]
        self.assertEqual(geography["qishuo_meridian_reference_status"], "UNRESOLVED")
        self.assertTrue(geography["implicit_utc_mapping_forbidden"])
        self.assertTrue(geography["implicit_modern_timezone_mapping_forbidden"])
        self.assertTrue(geography["inherit_sunrise_sunset_table_location_forbidden"])
        self.assertFalse(self.data["runtime_calendar_adapter_authorized"])


if __name__ == "__main__":
    unittest.main()
