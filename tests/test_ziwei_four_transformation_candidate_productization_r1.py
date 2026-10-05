from __future__ import annotations

import unittest
from pathlib import Path

from fortune_training.combined_chart_application.ziwei_four_transformation_historical_candidate_assets import (
    ZIWEI_FOUR_TRANSFORMATION_CANDIDATE_JS,
    ziwei_four_transformation_candidate_index_html,
)
from fortune_training.combined_chart_application.local_app import INDEX_HTML
from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
    _WorkbenchHandler,
)
from fortune_training.ziwei_chart import (
    FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_API_ID,
    FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_API_VERSION,
    FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_IDS,
    FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_ID,
    FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_VERSION,
    FOUR_TRANSFORMATION_HISTORICAL_RESOLVER_ID,
    FOUR_TRANSFORMATION_HISTORICAL_RESOLVER_VERSION,
    FOUR_TRANSFORMATION_HISTORICAL_SELECTION_STATUS,
)


ROOT = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return {
        "birth_datetime": "1994-05-17T14:30:00",
        "birth_place": "Beijing",
        "latitude": 39.9042,
        "longitude": 116.4074,
        "timezone_id": "Asia/Shanghai",
        "location_selection_id": None,
        "sex": "MALE",
        "precision": "EXACT_SECOND",
        "uncertainty_seconds": 0,
        "ziwei_daxian_count": 12,
        "ziwei_daxian_frame_id": None,
        "ziwei_annual_year": 2025,
        "ziwei_lunar_month": 4,
        "ziwei_minor_limit_age": None,
        "bazi_natal_profile_id": "BAZI-FOUNDATION-V1-R1",
        "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
        "bazi_dayun_count": 12,
        "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
    }


class ZiweiFourTransformationCandidateProductizationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = CombinedChartWorkbenchApplication(ROOT)
        cls.base = cls.app.resolve_payload(_payload())
        cls.sidecar = cls.app.resolve_ziwei_four_transformation_candidate_payload(
            _payload()
        )

    def test_profile_metadata_advertises_read_only_whole_table_api(self) -> None:
        rows = self.app.profile_metadata()["ziwei_historical_candidates"]
        row = next(
            item
            for item in rows
            if item["candidate_api_id"]
            == FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_API_ID
        )
        self.assertEqual(
            FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_API_VERSION,
            row["candidate_api_version"],
        )
        self.assertEqual(
            FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_ID,
            row["rule_set_id"],
        )
        self.assertEqual(
            FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_VERSION,
            row["rule_set_version"],
        )
        self.assertEqual(
            FOUR_TRANSFORMATION_HISTORICAL_SELECTION_STATUS,
            row["selection_status"],
        )
        self.assertEqual(
            FOUR_TRANSFORMATION_HISTORICAL_RESOLVER_ID,
            row["runtime_resolver_id"],
        )
        self.assertEqual(
            FOUR_TRANSFORMATION_HISTORICAL_RESOLVER_VERSION,
            row["runtime_resolver_version"],
        )
        self.assertEqual(
            FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_IDS,
            tuple(row["candidate_ids"]),
        )
        self.assertTrue(row["whole_table_only"])
        self.assertFalse(row["cell_level_hybridization_allowed"])
        self.assertEqual(
            "/api/ziwei-four-transformation-candidates",
            row["workbench_api_endpoint"],
        )
        self.assertFalse(row["production_winner_selected"])
        self.assertFalse(row["production_profile_changed"])
        self.assertEqual(64, len(row["registry_hash"]))

    def test_sidecar_is_bound_to_exact_source_chart_and_returns_both_families(self) -> None:
        resolution = self.base["combined_resolution"]
        self.assertEqual(
            resolution["manifest_hash"],
            self.sidecar["source_combined_manifest_hash"],
        )
        self.assertEqual(
            resolution["ziwei_bundle"]["bundle_hash"],
            self.sidecar["source_ziwei_bundle_hash"],
        )
        self.assertEqual(64, len(self.sidecar["source_natal_fact_hash"]))
        self.assertEqual(64, len(self.sidecar["source_natal_computation_hash"]))
        self.assertIn(
            self.sidecar["input_snapshot"]["source_stem"],
            tuple("甲乙丙丁戊己庚辛壬癸"),
        )
        rows = self.sidecar["candidate_tables"]
        self.assertEqual(
            FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_IDS,
            tuple(row["candidate_id"] for row in rows),
        )
        for row in rows:
            self.assertEqual("PRESERVED_NOT_SELECTED", row["selection_status"])
            self.assertTrue(row["whole_table_only"])
            self.assertEqual(4, len(row["assignments"]))
            self.assertEqual(64, len(row["registry_hash"]))
            self.assertEqual(64, len(row["runtime_hash"]))

    def test_product_profile_forbids_hybridization_and_winner_selection(self) -> None:
        profile = self.sidecar["candidate_profile"]
        self.assertEqual(
            FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_API_ID,
            profile["candidate_api_id"],
        )
        self.assertEqual("PRESERVED_NOT_SELECTED", profile["selection_status"])
        self.assertTrue(profile["whole_table_only"])
        self.assertFalse(profile["cell_level_hybridization_allowed"])
        self.assertFalse(profile["production_winner_selected"])
        self.assertFalse(profile["production_profile_changed"])
        self.assertEqual(
            FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_IDS,
            tuple(profile["candidate_ids"]),
        )

    def test_browser_renders_backend_assignments_without_table_formulas(self) -> None:
        for token in (
            "/api/ziwei-four-transformation-candidates",
            "candidate_tables",
            "assignment.transformation_type",
            "assignment.target_display_name",
            "whole_table_only",
            "cell_level_hybridization_allowed",
            "production_winner_selected",
            "production_profile_changed",
        ):
            with self.subTest(token=token):
                self.assertIn(token, ZIWEI_FOUR_TRANSFORMATION_CANDIDATE_JS)
        for forbidden in (
            "FULLBOOK_SHIDIAN_TABLE",
            "ZHONGZHOU_WANGTINGZHI_TABLE",
            "庚化科",
            "庚化忌",
            "壬化科",
            "戊化科",
            "天同",
            "天府",
            "左辅",
            "右弼",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, ZIWEI_FOUR_TRANSFORMATION_CANDIDATE_JS)

    def test_assets_are_additive_and_idempotence_guarded(self) -> None:
        html = ziwei_four_transformation_candidate_index_html(INDEX_HTML)
        self.assertIn("/ziwei-four-transformation-candidates.css", html)
        self.assertIn("/ziwei-four-transformation-candidates.js", html)
        with self.assertRaises(ValueError):
            ziwei_four_transformation_candidate_index_html(html)

    def test_workbench_version_bumped_without_legacy_health_change(self) -> None:
        self.assertEqual(
            "CombinedChartWorkbenchLocalApp/1.15",
            _WorkbenchHandler.server_version,
        )
        health = self.app.health()
        self.assertEqual("ZIWEI-BAZI-COMBINED-LOCAL-APP-HEALTH-V1", health["schema"])
        self.assertEqual("1.1.0", health["application_version"])


if __name__ == "__main__":
    unittest.main()
