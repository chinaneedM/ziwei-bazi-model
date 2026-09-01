from __future__ import annotations

import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from fortune_training.combined_chart_application.local_app import (
    LocalCombinedAppRequestError,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
)
from fortune_training.ziwei_application.star_provenance import (
    STAR_PROVENANCE_CLASSIFICATION_POLICY,
    STAR_PROVENANCE_SCHEMA,
    STAR_PROVENANCE_SEMANTIC_SCOPE,
    validate_star_provenance,
)


ROOT = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return {
        "birth_datetime": "1994-05-17T14:30:00",
        "birth_place": "Beijing",
        "latitude": 39.9042,
        "longitude": 116.4074,
        "timezone_id": "Asia/Shanghai",
        "sex": "MALE",
        "precision": "EXACT_SECOND",
        "uncertainty_seconds": 0,
        "ziwei_daxian_count": 12,
        "ziwei_daxian_frame_id": None,
        "ziwei_annual_year": 2025,
        "ziwei_lunar_month": 4,
        "ziwei_minor_limit_age": None,
        "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
        "bazi_dayun_count": 12,
        "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
    }


class ZiweiStarPlacementProvenanceR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = CombinedChartWorkbenchApplication(ROOT)
        cls.payload = _payload()
        combined, expected_hash, bundle = cls.app._resolve_ziwei_sidecar_source(
            dict(cls.payload)
        )
        cls.combined = combined
        cls.expected_hash = expected_hash
        cls.bundle = bundle
        cls.resolution = cls.app.ziwei_star_provenance_service.resolve(bundle)
        cls.response = cls.app.resolve_ziwei_star_provenance_payload(dict(cls.payload))
        cls.provenance = cls.response["ziwei_star_placement_provenance"]

    def test_sidecar_is_bound_to_exact_released_application_bundle(self) -> None:
        self.assertEqual(self.bundle.bundle_hash, self.expected_hash)
        self.assertEqual(self.response["source_ziwei_bundle_hash"], self.expected_hash)
        self.assertEqual(
            self.provenance["source_application_bundle_hash"],
            self.expected_hash,
        )
        self.assertEqual(
            self.response["source_combined_manifest_hash"],
            self.combined["manifest_hash"],
        )

    def test_rows_are_one_to_one_with_released_natal_placements(self) -> None:
        self.assertEqual(self.provenance["schema"], STAR_PROVENANCE_SCHEMA)
        self.assertEqual(self.provenance["status"], "COMPLETE")
        self.assertEqual(self.provenance["integrity"]["status"], "PASS")
        self.assertEqual(
            self.provenance["classification_policy"],
            STAR_PROVENANCE_CLASSIFICATION_POLICY,
        )
        self.assertEqual(
            self.provenance["semantic_scope"],
            STAR_PROVENANCE_SEMANTIC_SCOPE,
        )
        self.assertEqual(
            len(self.provenance["rows"]),
            len(self.bundle.candidate.chart.placements),
        )
        self.assertEqual(
            {row["entity_id"] for row in self.provenance["rows"]},
            {row.entity_id for row in self.bundle.candidate.chart.placements},
        )

    def test_generator_families_are_backend_provenance_not_star_nature(self) -> None:
        rows = self.provenance["rows"]
        self.assertEqual(
            {row["generator_family_id"] for row in rows},
            {
                "FOURTEEN_MAIN_STARS",
                "CORE_AUXILIARY",
                "DERIVED_AUXILIARY",
                "OPERATIONAL_MINOR_STARS",
            },
        )
        main_rows = [
            row for row in rows if row["generator_family_id"] == "FOURTEEN_MAIN_STARS"
        ]
        self.assertEqual(len(main_rows), 14)
        by_system = {}
        for row in main_rows:
            by_system.setdefault(row["main_star_system_id"], []).append(row)
        self.assertEqual(len(by_system["ZIWEI_SYSTEM"]), 6)
        self.assertEqual(len(by_system["TIANFU_SYSTEM"]), 8)
        for row in rows:
            self.assertTrue(row["generator_id"])
            self.assertTrue(row["algorithm_version"])
            self.assertTrue(row["source_refs"])
            self.assertEqual(len(row["fact_hash"]), 64)
            self.assertEqual(len(row["computation_hash"]), 64)
            self.assertNotIn("auspiciousness", row)
            self.assertNotIn("benefic_malefic", row)
            if row["generator_family_id"] != "FOURTEEN_MAIN_STARS":
                self.assertIsNone(row["main_star_system_id"])
                self.assertIsNone(row["main_star_system_label"])

    def test_top_level_hash_chain_is_tamper_evident(self) -> None:
        genuine = validate_star_provenance(self.resolution)
        self.assertEqual(genuine.status, "PASS")
        for field_name, diagnostic in (
            ("fact_hash", "FACT_HASH_MISMATCH"),
            ("computation_hash", "COMPUTATION_HASH_MISMATCH"),
            ("bundle_hash", "BUNDLE_HASH_MISMATCH"),
        ):
            with self.subTest(field_name=field_name):
                tampered = replace(self.resolution, **{field_name: "0" * 64})
                report = validate_star_provenance(tampered)
                self.assertEqual(report.status, "FAIL")
                self.assertIn(diagnostic, report.diagnostics)

    def test_source_bundle_rebinding_breaks_computation_chain(self) -> None:
        tampered = replace(
            self.resolution,
            source_application_bundle_hash="1" * 64,
        )
        report = validate_star_provenance(tampered)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("COMPUTATION_HASH_MISMATCH", report.diagnostics)
        self.assertIn("BUNDLE_HASH_MISMATCH", report.diagnostics)

    def test_star_provenance_source_unavailable_has_dedicated_diagnostic(self) -> None:
        combined = {
            "combined_resolution": {
                "ziwei_bundle": None,
                "ziwei_error": {"detail": "fixture source unavailable"},
            }
        }
        with patch.object(self.app, "resolve_payload", return_value=combined):
            with self.assertRaises(LocalCombinedAppRequestError) as raised:
                self.app.resolve_ziwei_star_provenance_payload(dict(self.payload))
        self.assertEqual(
            raised.exception.code,
            "LOCAL_APP_ZIWEI_STAR_PROVENANCE_SOURCE_UNAVAILABLE",
        )
        self.assertEqual(raised.exception.status, 422)

    def test_full_replay_is_stable(self) -> None:
        replay = self.app.resolve_ziwei_star_provenance_payload(dict(self.payload))
        self.assertEqual(replay, self.response)


if __name__ == "__main__":
    unittest.main()
