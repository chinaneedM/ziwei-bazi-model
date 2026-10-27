from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_application import (
    ApplicationBirthRequest,
    ApplicationResolutionError,
    SvgRendererProfile,
    ZiweiChartService,
    ZiweiTwelvePalaceSvgRenderer,
    ziwei_application_default_presentation_profile,
)
from fortune_training.ziwei_chart import Sex, ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class ZiweiSelectedTemporalFrameSummaryR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        calculation_profile = ziwei_chart_engine_v1_profile(registry)
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
            calculation_profile=calculation_profile,
            presentation_profile=ziwei_application_default_presentation_profile(),
            daxian_frame_id="DAXIAN:index=1",
            annual_year=2001,
            lunar_month=5,
            minor_limit_age=8,
        )
        cls.bundle = cls.service.resolve(cls.request)

    def test_selected_summary_is_exact_copy_of_canonical_frames(self) -> None:
        state = self.bundle.temporal_state
        summary = self.bundle.view_model.selected_temporal_frame_summary
        daxian = next(row for row in state.daxian_frames if row.frame_id == "DAXIAN:index=1")
        annual = next(row for row in state.annual_frames if row.absolute_year == 2001)
        monthly = next(
            row
            for row in state.monthly_frames
            if row.absolute_year == 2001 and row.lunar_month == 5
        )
        minor = next(row for row in state.minor_limit_frames if row.nominal_age == 8)

        self.assertEqual(
            {
                "frame_id": daxian.frame_id,
                "index": daxian.index,
                "nominal_age_start": daxian.nominal_age_start,
                "nominal_age_end": daxian.nominal_age_end,
                "absolute_year_start": daxian.absolute_year_start,
                "absolute_year_end": daxian.absolute_year_end,
                "active_address_index": daxian.active_address.index,
                "active_branch": daxian.active_address.branch,
                "active_palace_ganzhi": daxian.active_palace_ganzhi,
            },
            json_value(summary.daxian),
        )
        self.assertEqual(
            {
                "frame_id": annual.frame_id,
                "absolute_year": annual.absolute_year,
                "nominal_age": annual.nominal_age,
                "year_stem": annual.year_stem,
                "year_branch": annual.year_branch,
                "active_address_index": annual.active_address.index,
                "active_branch": annual.active_address.branch,
                "active_palace_ganzhi": annual.active_palace_ganzhi,
            },
            json_value(summary.annual),
        )
        self.assertEqual(
            {
                "frame_id": monthly.frame_id,
                "absolute_year": monthly.absolute_year,
                "lunar_month": monthly.lunar_month,
                "month_stem": monthly.month_stem,
                "month_branch": monthly.month_branch,
                "month_ganzhi": monthly.month_ganzhi,
                "active_address_index": monthly.active_address.index,
                "active_branch": monthly.active_address.branch,
                "calendar_scope": monthly.calendar_scope,
                "leap_month_policy_status": monthly.leap_month_policy_status,
            },
            json_value(summary.monthly),
        )
        self.assertEqual(
            {
                "frame_id": minor.frame_id,
                "nominal_age": minor.nominal_age,
                "active_address_index": minor.active_address.index,
                "active_branch": minor.active_address.branch,
            },
            json_value(summary.minor_limit),
        )

    def test_summary_is_exported_and_replay_bound(self) -> None:
        view_payload = json_value(self.bundle.view_model)
        self.assertIn("selected_temporal_frame_summary", view_payload)
        exported = self.service.export(self.bundle)
        self.assertEqual(
            view_payload["selected_temporal_frame_summary"],
            exported["view_model"]["selected_temporal_frame_summary"],
        )

        summary = self.bundle.view_model.selected_temporal_frame_summary
        self.assertIsNotNone(summary.daxian)
        tampered_daxian = replace(summary.daxian, active_branch="子")
        if tampered_daxian == summary.daxian:
            tampered_daxian = replace(summary.daxian, active_branch="丑")
        tampered_view = replace(
            self.bundle.view_model,
            selected_temporal_frame_summary=replace(summary, daxian=tampered_daxian),
        )
        with self.assertRaises(ApplicationResolutionError) as caught:
            self.service.export(replace(self.bundle, view_model=tampered_view))
        self.assertEqual("APPLICATION_VIEW_REPLAY_MISMATCH", caught.exception.diagnostic_code)

    def test_svg_renders_only_released_summary_fields(self) -> None:
        renderer = ZiweiTwelvePalaceSvgRenderer()
        svg = renderer.render(self.bundle.view_model).svg
        summary = self.bundle.view_model.selected_temporal_frame_summary
        self.assertIsNotNone(summary.daxian)
        self.assertIsNotNone(summary.annual)
        self.assertIsNotNone(summary.monthly)
        self.assertIsNotNone(summary.minor_limit)

        self.assertIn("大限:", svg)
        self.assertIn(f"虚岁{summary.daxian.nominal_age_start}-{summary.daxian.nominal_age_end}", svg)
        self.assertIn(f"宫干支{summary.daxian.active_palace_ganzhi}", svg)
        self.assertIn("流年:", svg)
        self.assertIn(f"年干{summary.annual.year_stem}", svg)
        self.assertIn(f"年支{summary.annual.year_branch}", svg)
        self.assertIn("流月:", svg)
        self.assertIn(f"月干支{summary.monthly.month_ganzhi}", svg)
        self.assertIn(f"月历: {summary.monthly.calendar_scope}", svg)
        self.assertIn(f"闰月策略: {summary.monthly.leap_month_policy_status}", svg)
        self.assertIn("小限:", svg)

        hidden = renderer.render(
            self.bundle.view_model,
            SvgRendererProfile(show_temporal=False),
        ).svg
        for token in ("大限:", "流年:", "流月:", "月历:", "闰月策略:"):
            self.assertNotIn(token, hidden)


if __name__ == "__main__":
    unittest.main()
