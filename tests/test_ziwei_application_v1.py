from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.ziwei_application import (
    ApplicationBirthRequest,
    ApplicationResolutionError,
    ZiweiChartService,
    ziwei_application_default_presentation_profile,
)
from fortune_training.ziwei_chart import Sex, ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class ZiweiApplicationV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.calculation_profile = ziwei_chart_engine_v1_profile(cls.registry)
        cls.service = ZiweiChartService.from_repository(ROOT)
        cls.request = ApplicationBirthRequest(
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
            lunar_month=5,
            minor_limit_age=8,
        )
        cls.bundle = cls.service.resolve(cls.request)

    def test_one_call_produces_complete_application_bundle(self) -> None:
        bundle = self.bundle
        self.assertEqual("ZIWEI-APPLICATION-CHART-BUNDLE-V1", bundle.schema)
        self.assertEqual("ZIWEI-APPLICATION-V1", bundle.application_profile.profile_id)
        self.assertEqual("PASS", bundle.candidate.integrity.status)
        self.assertEqual("PASS", bundle.r1_state.integrity.status)
        self.assertEqual("PASS", bundle.r2_state.integrity.status)
        self.assertEqual("PASS", bundle.r3_state.integrity.status)
        self.assertEqual("PASS", bundle.r4_state.integrity.status)
        self.assertEqual("PASS", bundle.r5_state.integrity.status)
        self.assertEqual(12, len(bundle.r5_state.frames))
        self.assertEqual(48, sum(len(row.members) for row in bundle.r5_state.frames))
        self.assertEqual(64, len(bundle.bundle_hash))

    def test_bundle_references_exact_upstream_hashes(self) -> None:
        bundle = self.bundle
        self.assertEqual(bundle.candidate.hashes.fact_hash, bundle.r1_state.upstream_natal_fact_hash)
        self.assertEqual(
            bundle.candidate.hashes.computation_hash,
            bundle.r1_state.upstream_natal_computation_hash,
        )
        self.assertEqual(
            bundle.r2_state.hashes.fact_hash,
            bundle.r3_state.upstream_relative_frame_fact_hash,
        )
        self.assertEqual(
            bundle.r2_state.hashes.fact_hash,
            bundle.r4_state.upstream_r2_fact_hash,
        )
        self.assertEqual(bundle.r3_state.hashes.fact_hash, bundle.r5_state.upstream_r3_fact_hash)
        self.assertEqual(bundle.r4_state.hashes.fact_hash, bundle.r5_state.upstream_r4_fact_hash)

    def test_temporal_selection_is_reflected_in_view(self) -> None:
        self.assertEqual(
            ("DAXIAN:index=1", "ANNUAL:2001", "MONTH:2001:5", "MINOR:age=8"),
            self.bundle.view_model.selected_temporal_frame_ids,
        )
        self.assertEqual(self.bundle.candidate.hashes.fact_hash, self.bundle.view_model.source_fact_hash)
        self.assertEqual(
            self.bundle.candidate.hashes.computation_hash,
            self.bundle.view_model.source_computation_hash,
        )
        doujun_cells = [
            cell for cell in self.bundle.view_model.cells if cell.doujun_frame_ids
        ]
        self.assertEqual(1, len(doujun_cells))
        self.assertEqual(("ANNUAL:2001",), doujun_cells[0].doujun_frame_ids)
        month_overlays = [
            row
            for cell in self.bundle.view_model.cells
            for row in cell.temporal_designations
            if row.frame_type == "MONTH" and row.designation_id == "LIFE"
        ]
        self.assertEqual(1, len(month_overlays))
        self.assertEqual("MONTH:2001:5", month_overlays[0].frame_id)

    def test_month_selection_requires_parent_annual_year(self) -> None:
        with self.assertRaisesRegex(ValueError, "lunar_month requires annual_year"):
            replace(self.request, annual_year=None, lunar_month=5)

    def test_plain_text_renderer_is_immediately_usable(self) -> None:
        rendered = self.service.render_plain_text(self.bundle)
        self.assertIn("view=ZIWEI-APPLICATION-V1-DEFAULT-VIEW@1.0.0", rendered)
        self.assertIn("fact_hash=", rendered)
        self.assertIn("temporal=", rendered)
        self.assertGreaterEqual(len(rendered.splitlines()), 16)

    def test_application_export_and_view_model_schemas(self) -> None:
        payload = self.service.export(self.bundle)
        application_schema = json.loads(
            (ROOT / "schemas" / "ziwei-application-chart-export-v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        view_schema = json.loads(
            (ROOT / "schemas" / "ziwei-chart-view-v1.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(application_schema)
        Draft202012Validator.check_schema(view_schema)
        application_errors = list(Draft202012Validator(application_schema).iter_errors(payload))
        if application_errors:
            self.fail("application export schema failed: " + "; ".join(row.message for row in application_errors))
        view_errors = list(Draft202012Validator(view_schema).iter_errors(payload["view_model"]))
        if view_errors:
            self.fail("view schema failed: " + "; ".join(row.message for row in view_errors))

    def test_repeated_execution_is_deterministic(self) -> None:
        replay = self.service.resolve(self.request)
        self.assertEqual(self.bundle.bundle_hash, replay.bundle_hash)
        self.assertEqual(self.bundle.temporal_hashes, replay.temporal_hashes)
        self.assertEqual(self.bundle.r1_state.hashes, replay.r1_state.hashes)
        self.assertEqual(self.bundle.r2_state.hashes, replay.r2_state.hashes)
        self.assertEqual(self.bundle.r3_state.hashes, replay.r3_state.hashes)
        self.assertEqual(self.bundle.r4_state.hashes, replay.r4_state.hashes)
        self.assertEqual(self.bundle.r5_state.hashes, replay.r5_state.hashes)
        self.assertEqual(self.bundle.view_model, replay.view_model)
        self.assertEqual(self.service.export(self.bundle), self.service.export(replay))

    def test_stale_natal_pass_and_hashes_cannot_hide_lineage_tamper(self) -> None:
        placement = self.bundle.candidate.chart.placements[0]
        tampered_placement = replace(placement, source_refs=("TAMPERED:SOURCE",))
        tampered_chart = replace(
            self.bundle.candidate.chart,
            placements=(tampered_placement, *self.bundle.candidate.chart.placements[1:]),
        )
        tampered_candidate = replace(self.bundle.candidate, chart=tampered_chart)
        self.assertEqual("PASS", tampered_candidate.integrity.status)
        self.assertEqual(self.bundle.candidate.hashes, tampered_candidate.hashes)
        tampered_bundle = replace(self.bundle, candidate=tampered_candidate)
        with self.assertRaises(ApplicationResolutionError) as caught:
            self.service.export(tampered_bundle)
        self.assertEqual("APPLICATION_NATAL_HASH_MISMATCH", caught.exception.diagnostic_code)

    def test_temporal_context_must_reproduce_from_candidate(self) -> None:
        tampered_context = replace(
            self.bundle.temporal_context,
            bureau_number=(self.bundle.temporal_context.bureau_number % 5) + 2,
        )
        if tampered_context.bureau_number == self.bundle.temporal_context.bureau_number:
            tampered_context = replace(
                self.bundle.temporal_context,
                bureau_number=2 if self.bundle.temporal_context.bureau_number != 2 else 3,
            )
        tampered_bundle = replace(self.bundle, temporal_context=tampered_context)
        with self.assertRaises(ApplicationResolutionError) as caught:
            self.service.export(tampered_bundle)
        self.assertEqual("APPLICATION_TEMPORAL_CONTEXT_MISMATCH", caught.exception.diagnostic_code)

    def test_tampered_r5_substitution_fails_closed_before_export(self) -> None:
        tampered_r5 = replace(
            self.bundle.r5_state,
            hashes=replace(self.bundle.r5_state.hashes, fact_hash="0" * 64),
        )
        tampered_bundle = replace(self.bundle, r5_state=tampered_r5)
        with self.assertRaises(ApplicationResolutionError):
            self.service.export(tampered_bundle)

    def test_tampered_view_fails_closed_before_render(self) -> None:
        tampered_view = replace(self.bundle.view_model, view_hash="0" * 64)
        tampered_bundle = replace(self.bundle, view_model=tampered_view)
        with self.assertRaises(ApplicationResolutionError) as caught:
            self.service.render_plain_text(tampered_bundle)
        self.assertEqual("APPLICATION_VIEW_REPLAY_MISMATCH", caught.exception.diagnostic_code)

    def test_requested_temporal_range_must_cover_selection(self) -> None:
        request = replace(self.request, annual_year=2030, max_nominal_age=10)
        with self.assertRaises(ApplicationResolutionError) as caught:
            self.service.resolve(request)
        self.assertEqual("APPLICATION_TEMPORAL_RANGE_TOO_SHORT", caught.exception.diagnostic_code)


if __name__ == "__main__":
    unittest.main()
