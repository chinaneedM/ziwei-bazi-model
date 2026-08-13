from __future__ import annotations

import copy
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from fortune_training.bazi_application import (
    BaziApplicationRequest,
    BaziChartService,
    bazi_local_application_v1_profile,
)
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_temporal import (
    BaziSex,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.combined_chart_application import (
    CombinedChartApplicationRequest,
    CombinedChartService,
    combined_chart_application_v1_profile,
    combined_manifest_hash,
    combined_manifest_payload,
    validate_combined_resolution,
)
from fortune_training.ziwei_application import (
    ApplicationBirthRequest,
    ZiweiChartService,
    ziwei_application_default_presentation_profile,
    ziwei_application_v1_profile,
)
from fortune_training.ziwei_chart import Sex, ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class CombinedChartApplicationV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        cls.birth = BirthInput(
            reported_local_datetime=datetime(1994, 5, 17, 14, 30),
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
        )
        cls.ziwei_calculation_profile = ziwei_chart_engine_v1_profile(registry)
        cls.ziwei_application_profile = ziwei_application_v1_profile()
        cls.ziwei_presentation_profile = (
            ziwei_application_default_presentation_profile()
        )
        cls.bazi_natal_profile = bazi_foundation_v1_profile(registry)
        cls.bazi_temporal_profile = bazi_temporal_v1_continuous_profile()
        cls.bazi_application_profile = bazi_local_application_v1_profile()
        cls.combined_profile = combined_chart_application_v1_profile()
        cls.request = CombinedChartApplicationRequest(
            birth=cls.birth,
            sex="MALE",
            ziwei_calculation_profile=cls.ziwei_calculation_profile,
            bazi_natal_profile=cls.bazi_natal_profile,
            bazi_temporal_profile=cls.bazi_temporal_profile,
            combined_profile=cls.combined_profile,
            ziwei_application_profile=cls.ziwei_application_profile,
            ziwei_presentation_profile=cls.ziwei_presentation_profile,
            bazi_application_profile=cls.bazi_application_profile,
            ziwei_daxian_count=12,
            bazi_dayun_count=12,
        )
        cls.combined_service = CombinedChartService.from_repository(ROOT)
        cls.ziwei_service = ZiweiChartService.from_repository(ROOT)
        cls.bazi_service = BaziChartService.from_repository(ROOT)
        cls.standalone_ziwei = cls.ziwei_service.resolve(
            ApplicationBirthRequest(
                birth=cls.birth,
                sex=Sex.MALE,
                calculation_profile=cls.ziwei_calculation_profile,
                presentation_profile=cls.ziwei_presentation_profile,
                daxian_count=12,
            )
        )
        cls.standalone_bazi = cls.bazi_service.resolve(
            BaziApplicationRequest(
                birth=cls.birth,
                sex=BaziSex.MALE,
                natal_profile=cls.bazi_natal_profile,
                temporal_profile=cls.bazi_temporal_profile,
                application_profile=cls.bazi_application_profile,
                dayun_count=12,
            )
        )
        cls.combined = cls.combined_service.resolve(cls.request)

    def test_valid_shared_birth_resolves_both_independently(self):
        self.assertEqual("RESOLVED_BOTH", self.combined.status)
        self.assertEqual("PASS", self.combined.integrity.status)
        self.assertIsNotNone(self.combined.ziwei_bundle)
        self.assertIsNotNone(self.combined.bazi_bundle)
        self.assertIsNone(self.combined.ziwei_error)
        self.assertIsNone(self.combined.bazi_error)

    def test_combined_reproduces_exact_standalone_bundle_hashes(self):
        self.assertEqual(
            self.standalone_ziwei.bundle_hash,
            self.combined.ziwei_bundle.bundle_hash,
        )
        self.assertEqual(
            self.standalone_bazi.bundle_hash,
            self.combined.bazi_bundle.bundle_hash,
        )

    def test_same_birth_object_is_passed_to_both_subsystem_requests(self):
        seen: dict[str, BirthInput] = {}
        real_ziwei_resolve = ZiweiChartService.resolve
        real_bazi_resolve = self.combined_service.bazi_service.resolve

        def ziwei_spy(service, request):
            seen["ziwei"] = request.birth
            return real_ziwei_resolve(service, request)

        def bazi_spy(request):
            seen["bazi"] = request.birth
            return real_bazi_resolve(request)

        with patch.object(ZiweiChartService, "resolve", new=ziwei_spy), patch.object(
            self.combined_service.bazi_service,
            "resolve",
            new=bazi_spy,
        ):
            result = self.combined_service.resolve(self.request)
        self.assertEqual("RESOLVED_BOTH", result.status)
        self.assertIs(self.birth, seen["ziwei"])
        self.assertIs(self.birth, seen["bazi"])
        self.assertIs(seen["ziwei"], seen["bazi"])

    def test_manifest_identity_changes_if_either_subsystem_hash_changes(self):
        base_hash = self.combined.manifest_hash
        changed_ziwei = replace(
            self.combined.ziwei_bundle,
            bundle_hash="TAMPERED-ZIWEI-BUNDLE-HASH",
        )
        changed = replace(
            self.combined,
            ziwei_bundle=changed_ziwei,
            manifest_hash="PENDING",
        )
        changed = replace(changed, manifest_hash=combined_manifest_hash(changed))
        self.assertNotEqual(base_hash, changed.manifest_hash)

        changed_bazi = replace(
            self.combined.bazi_bundle,
            bundle_hash="TAMPERED-BAZI-BUNDLE-HASH",
        )
        changed = replace(
            self.combined,
            bazi_bundle=changed_bazi,
            manifest_hash="PENDING",
        )
        changed = replace(changed, manifest_hash=combined_manifest_hash(changed))
        self.assertNotEqual(base_hash, changed.manifest_hash)

    def test_shell_export_does_not_mutate_subsystem_bundle_hashes(self):
        ziwei_hash = self.combined.ziwei_bundle.bundle_hash
        bazi_hash = self.combined.bazi_bundle.bundle_hash
        exported = self.combined_service.export(self.combined)
        self.assertEqual(ziwei_hash, self.combined.ziwei_bundle.bundle_hash)
        self.assertEqual(bazi_hash, self.combined.bazi_bundle.bundle_hash)
        self.assertEqual(
            ziwei_hash,
            exported["manifest"]["subsystems"]["ziwei"]["bundle_hash"],
        )
        self.assertEqual(
            bazi_hash,
            exported["manifest"]["subsystems"]["bazi"]["bundle_hash"],
        )

    def test_tampered_ziwei_bundle_fails_combined_replay(self):
        changed_bundle = replace(
            self.combined.ziwei_bundle,
            bundle_hash="TAMPERED-ZIWEI-BUNDLE-HASH",
        )
        changed = replace(self.combined, ziwei_bundle=changed_bundle)
        report = validate_combined_resolution(changed)
        self.assertEqual("FAIL", report.status)
        self.assertTrue(
            any(row.startswith("ZIWEI_BUNDLE_REPLAY_FAILED:") for row in report.diagnostics)
        )

    def test_tampered_bazi_bundle_fails_combined_replay(self):
        changed_view = copy.deepcopy(self.combined.bazi_bundle.candidates[0].view)
        changed_view["day_master_stem"] = "TAMPERED"
        changed_candidate = replace(
            self.combined.bazi_bundle.candidates[0],
            view=changed_view,
        )
        changed_bundle = replace(
            self.combined.bazi_bundle,
            candidates=(changed_candidate,),
        )
        changed = replace(self.combined, bazi_bundle=changed_bundle)
        report = validate_combined_resolution(changed)
        self.assertEqual("FAIL", report.status)
        self.assertTrue(
            any(row.startswith("BAZI_BUNDLE_REPLAY_FAILED:") for row in report.diagnostics)
        )

    def test_subsystem_failure_remains_explicit_partial(self):
        result = self.combined_service.resolve(
            replace(
                self.request,
                ziwei_annual_year=1900,
            )
        )
        self.assertEqual("PARTIAL", result.status)
        self.assertIsNone(result.ziwei_bundle)
        self.assertIsNotNone(result.ziwei_error)
        self.assertIsNotNone(result.bazi_bundle)
        self.assertIsNone(result.bazi_error)

    def test_bazi_uncertainty_is_not_cross_collapsed_by_ziwei(self):
        uncertain_birth = replace(self.birth, uncertainty_seconds=7200)
        result = self.combined_service.resolve(
            replace(self.request, birth=uncertain_birth)
        )
        self.assertIn(result.status, {"UNCERTAINTY_PRESENT", "PARTIAL"})
        if result.bazi_bundle is not None:
            self.assertNotEqual("RESOLVED", result.bazi_bundle.status)

    def test_manifest_contains_only_identity_composition_semantics(self):
        payload = combined_manifest_payload(self.combined)
        forbidden_fragments = {
            "prediction",
            "conclusion",
            "confirmation",
            "contradiction",
            "confidence",
            "score",
            "weight",
            "winner",
            "synthesis",
            "auspicious",
            "inauspicious",
        }

        def keys(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    yield str(key).lower()
                    yield from keys(item)
            elif isinstance(value, (list, tuple)):
                for item in value:
                    yield from keys(item)

        present = tuple(keys(payload))
        for fragment in forbidden_fragments:
            self.assertFalse(
                any(fragment in key for key in present),
                fragment,
            )
        self.assertEqual(
            "INDEPENDENT_BUNDLE_IDENTITY_COMPOSITION_ONLY",
            payload["combined_profile"]["composition_semantics"],
        )

    def test_native_exports_retain_exact_subsystem_identities(self):
        exported = self.combined_service.export(self.combined)
        self.assertEqual(
            self.combined.ziwei_bundle.bundle_hash,
            exported["ziwei_export"]["bundle_hash"],
        )
        self.assertEqual(
            self.combined.bazi_bundle.bundle_hash,
            exported["bazi_export"]["bundle_hash"],
        )
        self.assertEqual(self.combined.manifest_hash, exported["manifest"]["manifest_hash"])


if __name__ == "__main__":
    unittest.main()
