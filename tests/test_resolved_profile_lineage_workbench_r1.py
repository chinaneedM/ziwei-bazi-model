from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.resolved_profile_lineage_assets import (
    RESOLVED_PROFILE_LINEAGE_JS,
    resolved_profile_lineage_index_html,
)
from fortune_training.combined_chart_application.local_app import INDEX_HTML
from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
    _WorkbenchHandler,
)


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"


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


class ResolvedProfileLineageWorkbenchR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = CombinedChartWorkbenchApplication(ROOT)
        cls.response = cls.app.resolve_payload(_payload())
        cls.resolution = cls.response["combined_resolution"]
        cls.manifest = cls.response["combined_export"]["manifest"]

    def test_backend_resolution_exposes_exact_profile_versions_bound_by_manifest(self) -> None:
        self.assertEqual(self.resolution["integrity"]["status"], "PASS")
        self.assertEqual(self.resolution["manifest_hash"], self.manifest["manifest_hash"])
        for key in (
            "ziwei_calculation",
            "ziwei_application",
            "ziwei_presentation",
            "bazi_natal",
            "bazi_temporal",
            "bazi_application",
        ):
            resolution_key = f"{key}_profile"
            profile = self.resolution[resolution_key]
            manifest_profile = self.manifest["profiles"][key]
            self.assertEqual(profile["profile_id"], manifest_profile["profile_id"])
            self.assertEqual(profile["profile_version"], manifest_profile["profile_version"])

    def test_resolved_profiles_carry_rule_and_algorithm_lineage(self) -> None:
        z = self.resolution["ziwei_calculation_profile"]
        for key in (
            "natal_structure_algorithm_id",
            "main_star_algorithm_id",
            "auxiliary_rule_set_id",
            "auxiliary_algorithm_id",
            "minor_rule_set_id",
            "minor_algorithm_id",
            "dignity_rule_set_id",
            "dignity_algorithm_id",
            "transformation_rule_set_id",
            "transformation_algorithm_id",
            "temporal_rule_set_id",
            "temporal_algorithm_id",
            "ring_rule_set_id",
            "ring_algorithm_id",
            "role_rule_set_id",
            "role_algorithm_id",
        ):
            self.assertTrue(z.get(key), key)

        bn = self.resolution["bazi_natal_profile"]
        for key in (
            "sexagenary_registry_id",
            "hidden_stem_rule_set_id",
            "hidden_stem_algorithm_id",
            "ten_god_rule_set_id",
            "ten_god_algorithm_id",
            "affinity_rule_set_id",
            "affinity_algorithm_id",
            "raw_relation_rule_set_id",
            "raw_relation_algorithm_id",
            "natal_algorithm_id",
        ):
            self.assertTrue(bn.get(key), key)

        bt = self.resolution["bazi_temporal_profile"]
        for key in (
            "direction_rule_set_id",
            "anchor_rule_set_id",
            "symbolic_age_rule_set_id",
            "dayun_sequence_rule_set_id",
            "calendar_realization_rule_set",
            "dayun_boundary_rule_set",
            "algorithm_id",
        ):
            self.assertTrue(bt.get(key), key)

    def test_browser_asset_consumes_backend_snapshot_without_hardcoded_profile_values(self) -> None:
        for key in (
            "combined_profile",
            "ziwei_calculation_profile",
            "ziwei_application_profile",
            "ziwei_presentation_profile",
            "bazi_natal_profile",
            "bazi_temporal_profile",
            "bazi_application_profile",
            "manifest_hash",
            "integrity",
        ):
            self.assertIn(key, RESOLVED_PROFILE_LINEAGE_JS)
        for forbidden in (
            "ZIWEI-PRODUCTION-R1",
            "BAZI-FOUNDATION-V1-R1",
            "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
            "WENZHEN",
            "OPERATIONAL-ZIWEI-DIGNITY",
            "S08-",
        ):
            self.assertNotIn(forbidden, RESOLVED_PROFILE_LINEAGE_JS)

    def test_browser_contract_is_read_only_non_arbitrating_and_manifest_precise(self) -> None:
        self.assertIn("response.clone().json()", RESOLVED_PROFILE_LINEAGE_JS)
        self.assertNotIn("fetch('/api/", RESOLVED_PROFILE_LINEAGE_JS)
        self.assertIn("RuleSet / Algorithm 来自同一已验证后端快照", RESOLVED_PROFILE_LINEAGE_JS)
        self.assertIn("Profile identity 本身不表示 doctrine winner", RESOLVED_PROFILE_LINEAGE_JS)
        html = resolved_profile_lineage_index_html(INDEX_HTML)
        self.assertIn("已解析计算身份 / 规则版本", html)
        self.assertIn("/resolved-profile-lineage.css", html)
        self.assertIn("/resolved-profile-lineage.js", html)

    def test_self_inward_direction_remains_not_yet_formalized(self) -> None:
        payload = json.loads(MATRIX.read_text(encoding="utf-8"))
        rows = {row["field_id"]: row for row in payload["fields"]}
        row = rows["ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION"]
        self.assertEqual(row["status"], "NOT_YET_FORMALIZED")
        self.assertIn("must not be promoted", row["notes"])

    def test_workbench_version_bumps_without_changing_legacy_health_contract(self) -> None:
        self.assertEqual(_WorkbenchHandler.server_version, "CombinedChartWorkbenchLocalApp/1.12")
        health = self.app.health()
        self.assertEqual(health["schema"], "ZIWEI-BAZI-COMBINED-LOCAL-APP-HEALTH-V1")
        self.assertEqual(health["application_version"], "1.1.0")


if __name__ == "__main__":
    unittest.main()
