from __future__ import annotations

import unittest
from pathlib import Path

from fortune_training.combined_chart_application.local_app import (
    APP_JS,
    CSP,
    INDEX_HTML,
    LocalCombinedAppRequestError,
    LocalCombinedChartApplication,
)
from fortune_training.combined_chart_application.location_catalog import (
    OfflineLocationCatalog,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedChartLocationCatalogR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = OfflineLocationCatalog()

    def test_chinese_alias_prefers_deterministic_beijing_preset(self) -> None:
        rows = self.catalog.search("北京", limit=10)
        self.assertTrue(rows)
        row = rows[0]
        self.assertEqual("PRESET:BEIJING", row.selection_id)
        self.assertEqual(39.9042, row.latitude)
        self.assertEqual(116.4074, row.longitude)
        self.assertEqual("Asia/Shanghai", row.timezone_id)

    def test_greenwich_calibration_preset_preserves_exact_vector(self) -> None:
        rows = self.catalog.search("Greenwich Observatory", limit=10)
        row = next(item for item in rows if item.selection_id == "PRESET:GREENWICH_OBSERVATORY")
        self.assertEqual(51.4769, row.latitude)
        self.assertEqual(0.0, row.longitude)
        self.assertEqual("Europe/London", row.timezone_id)

    def test_global_city_lookup_is_offline_and_supplies_timezone(self) -> None:
        rows = self.catalog.search("Tokyo", limit=20)
        tokyo = next(
            item
            for item in rows
            if item.source_kind == "GEONAMESCACHE_OFFLINE_R1"
            and item.birth_place == "Tokyo"
        )
        self.assertEqual("Asia/Tokyo", tokyo.timezone_id)
        self.assertEqual("JP", tokyo.country_code)
        metadata = self.catalog.metadata()
        self.assertFalse(metadata["network_access"])


class CombinedChartLocationLinkageR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = LocalCombinedChartApplication(ROOT)
        cls.payload = {
            "birth_datetime": "1994-05-17T14:30",
            "birth_place": "Beijing",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone_id": "Asia/Shanghai",
            "location_selection_id": "PRESET:BEIJING",
            "sex": "MALE",
            "precision": "EXACT_SECOND",
            "uncertainty_seconds": 0,
            "ziwei_daxian_count": 12,
            "ziwei_daxian_frame_id": None,
            "ziwei_annual_year": None,
            "ziwei_minor_limit_age": None,
            "bazi_natal_profile_id": "BAZI-FOUNDATION-V1-R1",
            "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
            "bazi_dayun_count": 12,
            "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
        }

    def test_linked_selection_is_validated_and_reported_without_changing_native_export(self) -> None:
        response = self.app.resolve_payload(dict(self.payload))
        linked = response["location_selection"]
        self.assertEqual("LINKED", linked["mode"])
        self.assertEqual("PRESET:BEIJING", linked["selection_id"])
        self.assertEqual("PRESET:BEIJING", linked["record"]["selection_id"])
        self.assertNotIn("location_selection", response["combined_export"])
        self.assertEqual("RESOLVED_BOTH", response["combined_resolution"]["status"])

    def test_stale_linked_coordinates_fail_closed(self) -> None:
        payload = dict(self.payload)
        payload["longitude"] = 121.4737
        with self.assertRaises(LocalCombinedAppRequestError) as raised:
            self.app.resolve_payload(payload)
        self.assertEqual("LOCAL_APP_LOCATION_SELECTION_MISMATCH", raised.exception.code)

    def test_manual_mode_remains_backward_compatible(self) -> None:
        payload = dict(self.payload)
        payload["location_selection_id"] = None
        payload["birth_place"] = "Manual Test Point"
        payload["latitude"] = 0.0
        payload["longitude"] = 0.0
        payload["timezone_id"] = "Etc/UTC"
        response = self.app.resolve_payload(payload)
        self.assertEqual("MANUAL", response["location_selection"]["mode"])
        self.assertIsNone(response["location_selection"]["selection_id"])

    def test_location_search_api_shape_and_network_policy(self) -> None:
        response = self.app.search_locations("纽约", limit=10)
        self.assertEqual("ZIWEI-BAZI-COMBINED-LOCAL-LOCATION-SEARCH-V1", response["schema"])
        self.assertFalse(response["catalog"]["network_access"])
        self.assertTrue(any(row["selection_id"] == "PRESET:NEW_YORK" for row in response["results"]))

    def test_ui_requires_explicit_link_or_manual_override(self) -> None:
        self.assertIn('id="location-results"', INDEX_HTML)
        self.assertIn('id="location-manual"', INDEX_HTML)
        self.assertIn("readonly required", INDEX_HTML)
        self.assertIn("location_selection_id:$('location-manual').checked?null:locationSelection.selection_id", APP_JS)
        self.assertIn("LOCAL_APP_LOCATION_SELECTION_REQUIRED", APP_JS)
        self.assertIn("/api/locations?q=", APP_JS)
        self.assertIn("connect-src 'self'", CSP)
        self.assertNotIn("http://", APP_JS)
        self.assertNotIn("https://", APP_JS)


if __name__ == "__main__":
    unittest.main()
