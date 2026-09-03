from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.combined_chart_application.resolved_profile_lineage_assets import (
    RESOLVED_PROFILE_LINEAGE_JS,
)


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"
SERVICE_PATH = (
    ROOT / "src" / "fortune_training" / "combined_chart_application" / "service.py"
)
LOCAL_APP_PATH = (
    ROOT / "src" / "fortune_training" / "combined_chart_application" / "local_app.py"
)


class CombinedResolvedProfileLineageProductClosureR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.rows = {row["field_id"]: row for row in matrix["fields"]}
        cls.service_source = SERVICE_PATH.read_text(encoding="utf-8")
        cls.local_app_source = LOCAL_APP_PATH.read_text(encoding="utf-8")

    def test_lineage_surface_is_registered_as_shared_and_visible(self) -> None:
        row = self.rows["COMBINED_RESOLVED_PROFILE_LINEAGE"]
        self.assertEqual(row["system"], "SHARED")
        self.assertEqual(row["status"], "ALREADY_VISIBLE")
        self.assertEqual(row["priority"], "REFERENCE")
        self.assertEqual(
            row["backend_evidence"]["path"],
            "src/fortune_training/combined_chart_application/service.py",
        )
        self.assertEqual(
            row["api_evidence"]["path"],
            "src/fortune_training/combined_chart_application/local_app.py",
        )
        self.assertEqual(
            row["workbench_evidence"]["path"],
            "src/fortune_training/combined_chart_application/resolved_profile_lineage_assets.py",
        )
        self.assertEqual(row["workbench_evidence"]["symbol"], "render")
        for evidence_key in (
            "backend_evidence",
            "api_evidence",
            "workbench_evidence",
        ):
            self.assertTrue((ROOT / row[evidence_key]["path"]).exists())

    def test_backend_binds_exact_profiles_and_manifest_identity(self) -> None:
        for expected in (
            '"combined_profile"',
            '"ziwei_calculation"',
            '"ziwei_application"',
            '"ziwei_presentation"',
            '"bazi_natal"',
            '"bazi_temporal"',
            '"bazi_application"',
            'if resolution.manifest_hash != combined_manifest_hash(resolution):',
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.service_source)

    def test_resolve_endpoint_releases_validated_combined_resolution(self) -> None:
        for expected in (
            '"combined_resolution": json_value(resolution)',
            '"combined_export": export',
            'if urlsplit(self.path).path != "/api/resolve":',
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.local_app_source)

    def test_workbench_consumes_exact_snapshot_only_after_integrity_pass(self) -> None:
        for expected in (
            "payload?.combined_resolution",
            "resolution.integrity?.status !== 'PASS'",
            "!resolution.manifest_hash",
            "resolution.combined_profile",
            "resolution.ziwei_calculation_profile",
            "resolution.bazi_natal_profile",
            "resolution.bazi_temporal_profile",
            "response.clone().json()",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, RESOLVED_PROFILE_LINEAGE_JS)

    def test_browser_has_no_parallel_profile_registry_or_winner_selection(self) -> None:
        self.assertNotIn("fetch('/api/", RESOLVED_PROFILE_LINEAGE_JS)
        for forbidden in (
            "ZIWEI-PRODUCTION-R1",
            "BAZI-FOUNDATION-V1-R1",
            "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
            "WENZHEN",
            "OPERATIONAL-ZIWEI-DIGNITY",
            "S08-",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, RESOLVED_PROFILE_LINEAGE_JS)
        self.assertIn(
            "Profile identity 本身不表示 doctrine winner",
            RESOLVED_PROFILE_LINEAGE_JS,
        )

    def test_inventory_boundary_remains_non_interpretive(self) -> None:
        notes = self.rows["COMBINED_RESOLVED_PROFILE_LINEAGE"]["notes"]
        for expected in (
            "Inventory closure only",
            "not a canonical doctrine winner",
            "compatibility promotion",
            "cross-system rule unification",
            "strength/auspiciousness judgment",
            "interpretation",
            "prediction",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, notes)
        self.assertEqual(
            self.rows["ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION"]["status"],
            "NOT_YET_FORMALIZED",
        )


if __name__ == "__main__":
    unittest.main()
