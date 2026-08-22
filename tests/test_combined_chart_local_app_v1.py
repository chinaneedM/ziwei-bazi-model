from __future__ import annotations

import unittest
from pathlib import Path

from fortune_training.combined_chart_application.local_app import (
    LocalCombinedAppRequestError,
    LocalCombinedChartApplication,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedChartLocalAppV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = LocalCombinedChartApplication(ROOT)
        cls.payload = {
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

    def test_local_api_returns_independent_native_exports_and_svg(self):
        response = self.app.resolve_payload(dict(self.payload))
        self.assertEqual(
            "ZIWEI-BAZI-COMBINED-LOCAL-APP-RESOLVE-V1",
            response["schema"],
        )
        resolution = response["combined_resolution"]
        exported = response["combined_export"]
        self.assertEqual("RESOLVED_BOTH", resolution["status"])
        self.assertEqual("PASS", resolution["integrity"]["status"])
        self.assertEqual(
            resolution["manifest_hash"],
            exported["manifest"]["manifest_hash"],
        )
        self.assertEqual(
            resolution["ziwei_bundle"]["bundle_hash"],
            exported["ziwei_export"]["bundle_hash"],
        )
        self.assertEqual(
            resolution["bazi_bundle"]["bundle_hash"],
            exported["bazi_export"]["bundle_hash"],
        )
        self.assertTrue(response["ziwei_svg"].startswith('<?xml version="1.0" encoding="UTF-8"?>'))
        self.assertIn('<svg xmlns="http://www.w3.org/2000/svg"', response["ziwei_svg"])

    def test_profile_metadata_is_explicit_and_independent(self):
        metadata = self.app.profile_metadata()
        profiles = metadata["profiles"]
        self.assertEqual(
            "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
            profiles["combined"],
        )
        self.assertEqual(
            self.app.ziwei_calculation_profile.profile_id,
            profiles["ziwei_calculation"],
        )
        self.assertEqual(
            self.app.bazi_natal_profile.profile_id,
            profiles["bazi_natal"],
        )
        self.assertIn(
            "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
            profiles["bazi_temporal_options"],
        )

    def test_invalid_timezone_profile_and_counts_fail_at_shell_boundary(self):
        cases = (
            ("timezone_id", "Mars/Olympus"),
            ("combined_profile_id", "IMPLICIT-DEFAULT"),
            ("bazi_temporal_profile_id", "IMPLICIT-DEFAULT"),
            ("ziwei_daxian_count", 0),
            ("bazi_dayun_count", 21),
        )
        for key, value in cases:
            with self.subTest(key=key):
                payload = dict(self.payload)
                payload[key] = value
                with self.assertRaises(LocalCombinedAppRequestError):
                    self.app.resolve_payload(payload)

    def test_partial_subsystem_failure_remains_visible_in_local_response(self):
        payload = dict(self.payload)
        payload["ziwei_annual_year"] = 1900
        response = self.app.resolve_payload(payload)
        resolution = response["combined_resolution"]
        self.assertEqual("PARTIAL", resolution["status"])
        self.assertIsNone(resolution["ziwei_bundle"])
        self.assertIsNotNone(resolution["ziwei_error"])
        self.assertIsNotNone(resolution["bazi_bundle"])
        self.assertIsNone(response["ziwei_svg"])
        self.assertIsNone(response["combined_export"]["ziwei_export"])
        self.assertIsNotNone(response["combined_export"]["bazi_export"])

    def test_regular_lunar_month_selection_reaches_ziwei_without_changing_bazi(self):
        payload = dict(self.payload)
        payload["ziwei_annual_year"] = 2001
        payload["ziwei_lunar_month"] = 5
        response = self.app.resolve_payload(payload)
        resolution = response["combined_resolution"]
        self.assertEqual("RESOLVED_BOTH", resolution["status"])
        self.assertEqual(5, resolution["ziwei_bundle"]["selected_lunar_month"])
        self.assertIn(
            "MONTH:2001:5",
            resolution["ziwei_bundle"]["view_model"]["selected_temporal_frame_ids"],
        )
        self.assertIsNotNone(resolution["bazi_bundle"])

    def test_month_without_parent_year_fails_at_local_boundary(self):
        payload = dict(self.payload)
        payload["ziwei_lunar_month"] = 5
        with self.assertRaisesRegex(LocalCombinedAppRequestError, "requires ziwei_annual_year"):
            self.app.resolve_payload(payload)


if __name__ == "__main__":
    unittest.main()
