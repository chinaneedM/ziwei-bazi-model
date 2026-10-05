from __future__ import annotations

import unittest
from pathlib import Path

from fortune_training.combined_chart_application.ziwei_jielan_historical_candidate_assets import (
    ZIWEI_JIELAN_1581_CANDIDATE_JS,
    ziwei_jielan_1581_candidate_index_html,
)
from fortune_training.combined_chart_application.local_app import INDEX_HTML
from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
    _WorkbenchHandler,
)
from fortune_training.ziwei_chart import (
    JIELAN_1581_CANDIDATE_API_ID,
    JIELAN_1581_CANDIDATE_API_VERSION,
    JIELAN_1581_PRODUCT_FACT_KEYS,
    JIELAN_1581_RULE_SET_ID,
    JIELAN_1581_RULE_SET_VERSION,
    JIELAN_1581_RUNTIME_RESOLVER_ID,
    JIELAN_1581_RUNTIME_RESOLVER_VERSION,
    JIELAN_1581_SELECTION_STATUS,
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


class ZiweiJielan1581CandidateProductizationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = CombinedChartWorkbenchApplication(ROOT)
        cls.base = cls.app.resolve_payload(_payload())
        cls.sidecar = cls.app.resolve_ziwei_jielan_1581_candidate_payload(_payload())

    def test_profile_metadata_advertises_unselected_candidate_api(self) -> None:
        metadata = self.app.profile_metadata()
        rows = metadata["ziwei_historical_candidates"]
        self.assertEqual(1, len(rows))
        row = rows[0]
        self.assertEqual(JIELAN_1581_CANDIDATE_API_ID, row["candidate_api_id"])
        self.assertEqual(JIELAN_1581_CANDIDATE_API_VERSION, row["candidate_api_version"])
        self.assertEqual(JIELAN_1581_RULE_SET_ID, row["rule_set_id"])
        self.assertEqual(JIELAN_1581_RULE_SET_VERSION, row["rule_set_version"])
        self.assertEqual(JIELAN_1581_SELECTION_STATUS, row["selection_status"])
        self.assertEqual(JIELAN_1581_RUNTIME_RESOLVER_ID, row["runtime_resolver_id"])
        self.assertEqual(
            JIELAN_1581_RUNTIME_RESOLVER_VERSION,
            row["runtime_resolver_version"],
        )
        self.assertEqual(JIELAN_1581_PRODUCT_FACT_KEYS, tuple(row["released_fact_keys"]))
        self.assertEqual(
            "/api/ziwei-jielan-1581-candidate",
            row["workbench_api_endpoint"],
        )
        self.assertFalse(row["production_winner_selected"])
        self.assertFalse(row["production_profile_changed"])
        self.assertEqual(64, len(row["registry_hash"]))

    def test_sidecar_is_bound_to_exact_combined_and_ziwei_resolution(self) -> None:
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

    def test_only_three_source_closed_natal_facts_are_released(self) -> None:
        self.assertEqual(
            JIELAN_1581_PRODUCT_FACT_KEYS,
            tuple(self.sidecar["released_facts"]),
        )
        self.assertEqual(
            {"kui_yue", "fire_bell", "mingzhu"},
            set(self.sidecar["released_facts"]),
        )
        for forbidden in (
            "dignity",
            "shenzhu",
            "four_transformations",
            "tianshang_tianshi",
            "changsheng",
            "daxian",
            "minor_limit",
            "boshi",
        ):
            self.assertNotIn(forbidden, self.sidecar["released_facts"])

    def test_candidate_profile_is_preserved_not_selected(self) -> None:
        profile = self.sidecar["candidate_profile"]
        self.assertEqual(JIELAN_1581_CANDIDATE_API_ID, profile["candidate_api_id"])
        self.assertEqual(JIELAN_1581_RULE_SET_ID, profile["rule_set_id"])
        self.assertEqual("PRESERVED_NOT_SELECTED", profile["selection_status"])
        self.assertEqual(
            JIELAN_1581_RUNTIME_RESOLVER_ID,
            profile["runtime_resolver_id"],
        )
        self.assertEqual(JIELAN_1581_PRODUCT_FACT_KEYS, tuple(profile["released_fact_keys"]))
        self.assertFalse(profile["production_winner_selected"])
        self.assertFalse(profile["production_profile_changed"])
        self.assertEqual(64, len(profile["registry_hash"]))
        self.assertEqual(64, len(profile["candidate_runtime_hash"]))

    def test_browser_is_read_only_and_contains_no_candidate_formulas(self) -> None:
        for token in (
            "/api/ziwei-jielan-1581-candidate",
            "released_facts",
            "kui_yue",
            "fire_bell",
            "mingzhu",
            "selection_status=PRESERVED_NOT_SELECTED",
            "production_winner_selected",
            "production_profile_changed",
            "source_natal_fact_hash",
            "source_natal_computation_hash",
        ):
            with self.subTest(token=token):
                self.assertIn(token, ZIWEI_JIELAN_1581_CANDIDATE_JS)
        for forbidden in (
            "branch_index",
            "% 12",
            "JIELAN_1581_KUI_YUE_BY_STEM",
            "JIELAN_1581_FIRE_BELL_START_BY_YEAR_BRANCH",
            "JIELAN_1581_MINGZHU_BY_BIRTH_YEAR_BRANCH",
            "午寅",
            "戌火",
            "铃卯",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, ZIWEI_JIELAN_1581_CANDIDATE_JS)

    def test_assets_are_additive_and_idempotence_guarded(self) -> None:
        html = ziwei_jielan_1581_candidate_index_html(INDEX_HTML)
        self.assertIn("/ziwei-jielan-1581-candidate.css", html)
        self.assertIn("/ziwei-jielan-1581-candidate.js", html)
        with self.assertRaises(ValueError):
            ziwei_jielan_1581_candidate_index_html(html)

    def test_workbench_bumps_without_changing_legacy_health_contract(self) -> None:
        self.assertEqual(
            "CombinedChartWorkbenchLocalApp/1.13",
            _WorkbenchHandler.server_version,
        )
        health = self.app.health()
        self.assertEqual(
            "ZIWEI-BAZI-COMBINED-LOCAL-APP-HEALTH-V1",
            health["schema"],
        )
        self.assertEqual("1.1.0", health["application_version"])


if __name__ == "__main__":
    unittest.main()
