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
    _WorkbenchHandler,
)
from fortune_training.combined_chart_application.ziwei_dignity_provenance_assets import (
    ZIWEI_DIGNITY_PROVENANCE_JS,
)
from fortune_training.ziwei_application.dignity_provenance import (
    DIGNITY_PROVENANCE_AUTHORITY_CLASS,
    DIGNITY_PROVENANCE_S01_BRIGHTNESS_AUTHORITY,
    DIGNITY_PROVENANCE_SCHEMA,
    DIGNITY_PROVENANCE_SEMANTIC_SCOPE,
    validate_dignity_provenance,
)
from fortune_training.ziwei_chart.dignity_r4 import (
    OPERATIONAL_R4_DIGNITY_RULE_SET_ID,
    OPERATIONAL_R4_DIGNITY_RULE_SET_VERSION,
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


class ZiweiDignityAnnotationProvenanceR1Tests(unittest.TestCase):
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
        cls.resolution = cls.app.ziwei_dignity_provenance_service.resolve(bundle)
        cls.response = cls.app.resolve_ziwei_dignity_provenance_payload(dict(cls.payload))
        cls.provenance = cls.response["ziwei_dignity_annotation_provenance"]

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

    def test_rows_are_one_to_one_with_released_dignity_annotations(self) -> None:
        annotations = [
            row
            for row in self.bundle.candidate.chart.annotations
            if row.annotation_type == "DIGNITY"
        ]
        self.assertEqual(self.provenance["schema"], DIGNITY_PROVENANCE_SCHEMA)
        self.assertEqual(self.provenance["status"], "COMPLETE")
        self.assertEqual(self.provenance["integrity"]["status"], "PASS")
        self.assertEqual(len(self.provenance["rows"]), len(annotations))
        self.assertEqual(len(annotations), 70)
        self.assertEqual(
            {row["annotation_id"] for row in self.provenance["rows"]},
            {row.annotation_id for row in annotations},
        )

    def test_current_production_r4_identity_is_copied_not_recomputed(self) -> None:
        self.assertEqual(
            self.provenance["source_dignity_rule_set_id"],
            OPERATIONAL_R4_DIGNITY_RULE_SET_ID,
        )
        self.assertEqual(
            self.provenance["source_dignity_rule_set_version"],
            OPERATIONAL_R4_DIGNITY_RULE_SET_VERSION,
        )
        self.assertEqual(
            self.provenance["source_dignity_rule_set_id"],
            self.bundle.calculation_profile.dignity_rule_set_id,
        )
        self.assertEqual(
            self.provenance["source_dignity_algorithm_id"],
            self.bundle.calculation_profile.dignity_algorithm_id,
        )
        annotation_by_id = {
            row.annotation_id: row for row in self.bundle.candidate.chart.annotations
        }
        placement_by_id = {
            row.entity_id: row for row in self.bundle.candidate.chart.placements
        }
        for row in self.provenance["rows"]:
            source = annotation_by_id[row["annotation_id"]]
            placement = placement_by_id[row["target_entity_id"]]
            self.assertEqual(row["target_display_name"], placement.display_name)
            self.assertEqual(row["address_index"], source.target_address.index)
            self.assertEqual(row["branch"], source.target_address.branch)
            self.assertEqual(row["status"], source.status)
            self.assertEqual(row["grade"], source.grade)
            self.assertEqual(row["scale_id"], source.scale_id)
            self.assertEqual(row["scale_version"], source.scale_version)
            self.assertEqual(row["rule_set_id"], source.rule_set_id)
            self.assertEqual(row["rule_set_version"], source.rule_set_version)
            self.assertEqual(row["generator_id"], source.generator_id)
            self.assertEqual(row["algorithm_version"], source.algorithm_version)
            self.assertEqual(row["source_refs"], list(source.source_refs))
            self.assertEqual(len(row["fact_hash"]), 64)
            self.assertEqual(len(row["computation_hash"]), 64)

    def test_authority_boundary_is_explicit_and_non_interpretive(self) -> None:
        self.assertEqual(
            self.provenance["authority_class"],
            DIGNITY_PROVENANCE_AUTHORITY_CLASS,
        )
        self.assertEqual(
            self.provenance["s01_brightness_authority"],
            DIGNITY_PROVENANCE_S01_BRIGHTNESS_AUTHORITY,
        )
        self.assertEqual(
            self.provenance["semantic_scope"],
            DIGNITY_PROVENANCE_SEMANTIC_SCOPE,
        )
        self.assertEqual(self.provenance["s01_brightness_authority"], "NOT_CLAIMED")
        forbidden = {
            "auspiciousness",
            "benefic_malefic",
            "strength_score",
            "prediction",
            "s01_frozen_brightness_value",
        }
        for row in self.provenance["rows"]:
            self.assertTrue(forbidden.isdisjoint(row))

    def test_top_level_hash_chain_is_tamper_evident(self) -> None:
        self.assertEqual(validate_dignity_provenance(self.resolution).status, "PASS")
        for field_name, diagnostic in (
            ("fact_hash", "FACT_HASH_MISMATCH"),
            ("computation_hash", "COMPUTATION_HASH_MISMATCH"),
            ("bundle_hash", "BUNDLE_HASH_MISMATCH"),
        ):
            with self.subTest(field_name=field_name):
                tampered = replace(self.resolution, **{field_name: "0" * 64})
                report = validate_dignity_provenance(tampered)
                self.assertEqual(report.status, "FAIL")
                self.assertIn(diagnostic, report.diagnostics)

    def test_rule_set_tampering_fails_closed(self) -> None:
        tampered = replace(
            self.resolution,
            source_dignity_rule_set_id="UNKNOWN-DIGNITY-RULE-SET",
        )
        report = validate_dignity_provenance(tampered)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SOURCE_RULE_SET_UNSUPPORTED", report.diagnostics)
        self.assertIn("FACT_HASH_MISMATCH", report.diagnostics)

    def test_source_unavailable_has_dedicated_diagnostic(self) -> None:
        combined = {
            "combined_resolution": {
                "ziwei_bundle": None,
                "ziwei_error": {"detail": "fixture source unavailable"},
            }
        }
        with patch.object(self.app, "resolve_payload", return_value=combined):
            with self.assertRaises(LocalCombinedAppRequestError) as raised:
                self.app.resolve_ziwei_dignity_provenance_payload(dict(self.payload))
        self.assertEqual(
            raised.exception.code,
            "LOCAL_APP_ZIWEI_DIGNITY_PROVENANCE_SOURCE_UNAVAILABLE",
        )
        self.assertEqual(raised.exception.status, 422)

    def test_full_replay_is_stable(self) -> None:
        replay = self.app.resolve_ziwei_dignity_provenance_payload(dict(self.payload))
        self.assertEqual(replay, self.response)

    def test_workbench_contract_is_read_only_and_s01_boundary_is_visible(self) -> None:
        self.assertEqual(_WorkbenchHandler.server_version, "CombinedChartWorkbenchLocalApp/1.12")
        self.assertIn("/api/ziwei-dignity-provenance", ZIWEI_DIGNITY_PROVENANCE_JS)
        self.assertIn("s01_brightness_authority", ZIWEI_DIGNITY_PROVENANCE_JS)
        self.assertIn("不是 S01 冻结原盘亮度权威", ZIWEI_DIGNITY_PROVENANCE_JS)
        for forbidden in (
            "OPERATIONAL_R4_ADDED_DIGNITY_BY_BRANCH",
            "OPERATIONAL_MAIN_STAR_DIGNITY_BY_ADDRESS",
            "STAR.ZIWEI",
            "DIGNITY_GRADES",
        ):
            self.assertNotIn(forbidden, ZIWEI_DIGNITY_PROVENANCE_JS)


if __name__ == "__main__":
    unittest.main()
