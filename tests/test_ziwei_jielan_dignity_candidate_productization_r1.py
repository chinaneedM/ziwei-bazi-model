from __future__ import annotations

import unittest
from pathlib import Path

from fortune_training.combined_chart_application.ziwei_jielan_dignity_historical_candidate_assets import (
    ZIWEI_JIELAN_DIGNITY_CANDIDATE_JS,
    ziwei_jielan_dignity_candidate_index_html,
)
from fortune_training.combined_chart_application.local_app import INDEX_HTML
from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
    _WorkbenchHandler,
)
from fortune_training.ziwei_chart import (
    JIELAN_1581_DIGNITY_CANDIDATE_API_ID,
    JIELAN_1581_DIGNITY_CANDIDATE_API_VERSION,
    JIELAN_1581_DIGNITY_CROSS_COLLATION_ID,
    JIELAN_1581_DIGNITY_CROSS_COLLATION_STATUS,
    JIELAN_1581_DIGNITY_CROSS_COLLATION_VERSION,
    JIELAN_1581_DIGNITY_LEXEME_CANDIDATE_ID,
    JIELAN_1581_DIGNITY_LEXEME_REGISTRY_ID,
    JIELAN_1581_DIGNITY_LEXEME_REGISTRY_VERSION,
    JIELAN_1581_DIGNITY_LEXEME_RESOLVER_ID,
    JIELAN_1581_DIGNITY_LEXEME_RESOLVER_VERSION,
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


class ZiweiJielanDignityCandidateProductizationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = CombinedChartWorkbenchApplication(ROOT)
        cls.base = cls.app.resolve_payload(_payload())
        cls.sidecar = cls.app.resolve_ziwei_jielan_dignity_candidate_payload(
            _payload()
        )

    def test_profile_metadata_advertises_read_only_raw_lexeme_api(self) -> None:
        rows = self.app.profile_metadata()["ziwei_historical_candidates"]
        row = next(
            item
            for item in rows
            if item["candidate_api_id"] == JIELAN_1581_DIGNITY_CANDIDATE_API_ID
        )
        self.assertEqual(
            JIELAN_1581_DIGNITY_CANDIDATE_API_VERSION,
            row["candidate_api_version"],
        )
        self.assertEqual(JIELAN_1581_DIGNITY_LEXEME_REGISTRY_ID, row["rule_set_id"])
        self.assertEqual(
            JIELAN_1581_DIGNITY_LEXEME_REGISTRY_VERSION,
            row["rule_set_version"],
        )
        self.assertEqual(
            JIELAN_1581_DIGNITY_LEXEME_CANDIDATE_ID,
            row["candidate_id"],
        )
        self.assertEqual("PRESERVED_NOT_SELECTED", row["selection_status"])
        self.assertEqual(
            JIELAN_1581_DIGNITY_LEXEME_RESOLVER_ID,
            row["runtime_resolver_id"],
        )
        self.assertEqual(
            JIELAN_1581_DIGNITY_LEXEME_RESOLVER_VERSION,
            row["runtime_resolver_version"],
        )
        self.assertEqual(
            JIELAN_1581_DIGNITY_CROSS_COLLATION_ID,
            row["cross_collation_id"],
        )
        self.assertEqual(
            JIELAN_1581_DIGNITY_CROSS_COLLATION_VERSION,
            row["cross_collation_version"],
        )
        self.assertEqual(
            JIELAN_1581_DIGNITY_CROSS_COLLATION_STATUS,
            row["cross_collation_status"],
        )
        self.assertEqual(
            "/api/ziwei-jielan-1581-dignity-candidate",
            row["workbench_api_endpoint"],
        )
        self.assertFalse(row["production_grade_mapping_present"])
        self.assertFalse(row["ch69_used_to_fill_ch70"])
        self.assertFalse(row["production_winner_selected"])
        self.assertFalse(row["production_profile_changed"])
        self.assertEqual(64, len(row["registry_hash"]))
        self.assertEqual(64, len(row["cross_collation_hash"]))

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

    def test_sidecar_exposes_raw_source_rows_and_frozen_cross_collation_only(self) -> None:
        profile = self.sidecar["candidate_profile"]
        self.assertEqual(
            JIELAN_1581_DIGNITY_CANDIDATE_API_ID,
            profile["candidate_api_id"],
        )
        self.assertEqual("PRESERVED_NOT_SELECTED", profile["selection_status"])
        self.assertEqual(300, len(self.sidecar["source_lexeme_rows"]))
        self.assertEqual(300, len(self.sidecar["cross_collation_rows"]))
        self.assertEqual(
            {
                "EXACT_LEXEME_OVERLAP": 97,
                "SOURCE_EXPLICIT_EQUIVALENT": 37,
                "SOURCE_LOCAL_POLARITY_CONFLICT": 54,
                "ATTESTED_NON_EQUIVALENT_NO_DIRECT_GLOSS": 21,
                "CH69_UNSTATED": 82,
                "CH69_TEXT_UNRESOLVED": 8,
                "CH70_UNSTATED": 1,
            },
            self.sidecar["relation_counts"],
        )
        self.assertFalse(profile["production_grade_mapping_present"])
        self.assertFalse(profile["ch69_used_to_fill_ch70"])
        self.assertFalse(profile["ch70_used_to_overwrite_ch69"])
        self.assertFalse(profile["production_winner_selected"])
        self.assertFalse(profile["production_profile_changed"])
        self.assertEqual(64, len(profile["candidate_runtime_hash"]))
        self.assertEqual(64, len(profile["cross_collation_hash"]))

    def test_browser_renders_backend_rows_without_source_tables_or_grade_formula(self) -> None:
        for token in (
            "/api/ziwei-jielan-1581-dignity-candidate",
            "cross_collation_rows",
            "row.ch70_source_lexemes",
            "row.ch69_source_lexemes",
            "row.relation",
            "production_grade_mapping_present",
            "ch69_used_to_fill_ch70",
            "production_winner_selected",
        ):
            with self.subTest(token=token):
                self.assertIn(token, ZIWEI_JIELAN_DIGNITY_CANDIDATE_JS)
        for forbidden in (
            "_CH69_GROUPS",
            "_GROUPS",
            "SOURCE_LOCAL_POLARITY",
            "JIELAN_1581_DIGNITY_EXPLICIT_GLOSSES",
            "卯酉巳亥",
            "局陷",
            "OPERATIONAL-ZIWEI-DIGNITY-R4",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, ZIWEI_JIELAN_DIGNITY_CANDIDATE_JS)

    def test_assets_are_additive_and_idempotence_guarded(self) -> None:
        html = ziwei_jielan_dignity_candidate_index_html(INDEX_HTML)
        self.assertIn("/ziwei-jielan-dignity-candidate.css", html)
        self.assertIn("/ziwei-jielan-dignity-candidate.js", html)
        with self.assertRaises(ValueError):
            ziwei_jielan_dignity_candidate_index_html(html)

    def test_workbench_bumps_without_changing_legacy_health_contract(self) -> None:
        self.assertEqual(
            "CombinedChartWorkbenchLocalApp/1.15",
            _WorkbenchHandler.server_version,
        )
        health = self.app.health()
        self.assertEqual("ZIWEI-BAZI-COMBINED-LOCAL-APP-HEALTH-V1", health["schema"])
        self.assertEqual("1.1.0", health["application_version"])


if __name__ == "__main__":
    unittest.main()
