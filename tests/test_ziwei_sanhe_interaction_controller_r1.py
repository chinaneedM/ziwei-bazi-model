from __future__ import annotations

import copy
import json
import unittest
from dataclasses import fields, replace
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_application import (
    ApplicationBirthRequest,
    SanheInteractionRequest,
    SanheInteractionResolutionError,
    ZiweiChartService,
    ZiweiSanheInteractionService,
    sanhe_interaction_bundle_hash,
    sanhe_interaction_source_fact_hash,
    sanhe_interaction_view_hash,
    validate_sanhe_interaction_full_replay,
    validate_sanhe_interaction_resolution,
    ziwei_application_default_presentation_profile,
)
from fortune_training.ziwei_chart import Sex, ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class ZiweiSanheInteractionControllerR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        cls.calculation_profile = ziwei_chart_engine_v1_profile(registry)
        cls.application_request = ApplicationBirthRequest(
            birth=BirthInput(
                reported_local_datetime=datetime(1994, 5, 17, 14, 30),
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            sex=Sex.MALE,
            calculation_profile=cls.calculation_profile,
            presentation_profile=ziwei_application_default_presentation_profile(),
            daxian_frame_id="DAXIAN:index=1",
            annual_year=2001,
            minor_limit_age=8,
        )
        cls.base_service = ZiweiChartService.from_repository(ROOT)
        cls.service = ZiweiSanheInteractionService(cls.base_service)
        cls.base_bundle = cls.base_service.resolve(cls.application_request)
        cls.origin_ids = tuple(
            dict.fromkeys(
                row.origin_designation_id
                for row in cls.base_bundle.r2_state.frame_facts
            )
        )
        if len(cls.origin_ids) != 12:
            raise AssertionError(f"expected 12 R2 origins, found {len(cls.origin_ids)}")
        cls.origin = cls.origin_ids[0]
        cls.schema = json.loads(
            (
                ROOT / "schemas" / "ziwei-sanhe-interaction-controller-r1.schema.json"
            ).read_text(encoding="utf-8")
        )

    @classmethod
    def _request(cls, *, application_request=None, origin=None):
        return SanheInteractionRequest(
            application_request=application_request or cls.application_request,
            origin_designation_id=origin or cls.origin,
        )

    def test_application_v1_is_unchanged_by_controller_resolution(self) -> None:
        before = self.base_service.resolve(self.application_request)
        before_export = self.base_service.export(before)
        self.service.resolve(self._request())
        after = self.base_service.resolve(self.application_request)
        self.assertEqual(before, after)
        self.assertEqual(before.bundle_hash, after.bundle_hash)
        self.assertEqual(before_export, self.base_service.export(after))

    def test_deterministic_projection_is_schema_valid_and_closed(self) -> None:
        request = self._request()
        bundle1, first = self.service.resolve_with_bundle(request)
        bundle2, second = self.service.resolve_with_bundle(request)
        self.assertEqual(bundle1, bundle2)
        self.assertEqual(first, second)
        self.assertEqual("RESOLVED", first.status)
        self.assertEqual("SANHE", first.interaction_mode)
        self.assertEqual("PASS", first.integrity.status)
        self.assertEqual(bundle1.bundle_hash, first.source_application_bundle_hash)
        self.assertEqual(12, len(first.relative_roles))
        self.assertEqual(4, len(first.sanfang_sizheng_frame.members))
        Draft202012Validator(self.schema).validate(json_value(first))

        injected = copy.deepcopy(json_value(first))
        injected["prediction"] = "FORBIDDEN"
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.schema).validate(injected)

    def test_all_twelve_origins_select_exact_r2_and_r5_subsets(self) -> None:
        for origin in self.origin_ids:
            with self.subTest(origin=origin):
                bundle, result = self.service.resolve_with_bundle(
                    self._request(origin=origin)
                )
                expected_r2 = tuple(
                    row
                    for row in bundle.r2_state.frame_facts
                    if row.origin_designation_id == origin
                )
                expected_r5 = tuple(
                    row
                    for row in bundle.r5_state.frames
                    if row.origin_designation_id == origin
                )
                self.assertEqual(12, len(expected_r2))
                self.assertEqual(1, len(expected_r5))
                self.assertEqual(expected_r2, result.relative_roles)
                self.assertEqual(expected_r5[0], result.sanfang_sizheng_frame)
                self.assertEqual(
                    [0, 4, 6, 8],
                    [row.member_offset for row in result.sanfang_sizheng_frame.members],
                )
                self.assertEqual(
                    ["SELF", "TRINE_PLUS_4", "OPPOSITION", "TRINE_PLUS_8"],
                    [row.semantic_role for row in result.sanfang_sizheng_frame.members],
                )

    def test_unknown_origin_fails_closed_without_fallback(self) -> None:
        with self.assertRaises(SanheInteractionResolutionError) as caught:
            self.service.resolve(self._request(origin="NOT-A-REAL-PALACE"))
        self.assertEqual(
            "SANHE_INTERACTION_R2_ORIGIN_NOT_UNIQUE",
            caught.exception.code,
        )
        self.assertIn("rows=0", caught.exception.detail)

    def test_temporal_selection_is_explicit_and_does_not_change_origin_contract(self) -> None:
        request_2001 = self._request()
        request_2002 = self._request(
            application_request=replace(self.application_request, annual_year=2002)
        )
        bundle_2001, result_2001 = self.service.resolve_with_bundle(request_2001)
        bundle_2002, result_2002 = self.service.resolve_with_bundle(request_2002)
        self.assertNotEqual(bundle_2001.bundle_hash, bundle_2002.bundle_hash)
        self.assertEqual(2001, result_2001.selected_annual_year)
        self.assertEqual(2002, result_2002.selected_annual_year)
        self.assertEqual(
            result_2001.selected_origin_designation_id,
            result_2002.selected_origin_designation_id,
        )
        self.assertEqual(result_2001.relative_roles, result_2002.relative_roles)
        self.assertEqual(
            result_2001.sanfang_sizheng_frame,
            result_2002.sanfang_sizheng_frame,
        )
        self.assertNotEqual(result_2001.bundle_hash, result_2002.bundle_hash)

    def test_controller_contract_has_no_bazi_target_time_input(self) -> None:
        names = {field.name for field in fields(SanheInteractionRequest)}
        self.assertEqual({"application_request", "origin_designation_id"}, names)
        self.assertFalse(any("bazi" in name or "target" in name for name in names))

    def test_borrow_provenance_is_exact_when_present(self) -> None:
        borrowed_origin = None
        for frame in self.base_bundle.r5_state.frames:
            if any(
                member.borrowed_from_raw_address is not None
                or member.physical_source_address != member.target_raw_address
                for member in frame.members
            ):
                borrowed_origin = frame.origin_designation_id
                break
        if borrowed_origin is None:
            self.skipTest("fixture has no R5 borrowed member")
        bundle, result = self.service.resolve_with_bundle(
            self._request(origin=borrowed_origin)
        )
        source_frame = next(
            row
            for row in bundle.r5_state.frames
            if row.origin_designation_id == borrowed_origin
        )
        self.assertEqual(source_frame, result.sanfang_sizheng_frame)
        self.assertEqual(source_frame.members, result.sanfang_sizheng_frame.members)

    def test_structural_tamper_fails_controller_integrity(self) -> None:
        bundle, result = self.service.resolve_with_bundle(self._request())
        first_role = result.relative_roles[0]
        tampered_role = replace(
            first_role,
            relative_role_designation_id=first_role.relative_role_designation_id + ":TAMPER",
        )
        tampered = replace(
            result,
            relative_roles=(tampered_role, *result.relative_roles[1:]),
        )
        report = validate_sanhe_interaction_resolution(bundle, tampered)
        self.assertEqual("FAIL", report.status)
        self.assertIn("R2_RELATIVE_ROLE_SUBSET_MISMATCH", report.diagnostics)
        self.assertIn("VIEW_HASH_MISMATCH", report.diagnostics)

    def test_self_consistent_local_rewrite_still_fails_full_replay(self) -> None:
        request = self._request()
        bundle, result = self.service.resolve_with_bundle(request)
        rewritten = replace(result, selected_annual_year=9999)
        rewritten = replace(
            rewritten,
            source_fact_hash=sanhe_interaction_source_fact_hash(rewritten),
        )
        rewritten = replace(
            rewritten,
            view_hash=sanhe_interaction_view_hash(rewritten),
        )
        rewritten = replace(
            rewritten,
            bundle_hash=sanhe_interaction_bundle_hash(rewritten),
        )
        structural = validate_sanhe_interaction_resolution(bundle, rewritten)
        self.assertEqual("FAIL", structural.status)
        self.assertIn("ANNUAL_SELECTION_MISMATCH", structural.diagnostics)
        replay = validate_sanhe_interaction_full_replay(
            self.service,
            request,
            bundle,
            rewritten,
        )
        self.assertEqual("FAIL", replay.status)
        self.assertIn("SANHE_INTERACTION_FULL_REPLAY_MISMATCH", replay.diagnostics)

    def test_full_replay_passes_for_exact_application_and_origin(self) -> None:
        request = self._request()
        bundle, result = self.service.resolve_with_bundle(request)
        report = validate_sanhe_interaction_full_replay(
            self.service,
            request,
            bundle,
            result,
        )
        self.assertEqual("PASS", report.status)
        self.assertEqual((), report.diagnostics)


if __name__ == "__main__":
    unittest.main()
