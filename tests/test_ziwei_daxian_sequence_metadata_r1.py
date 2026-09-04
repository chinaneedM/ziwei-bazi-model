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


class ZiweiDaxianSequenceMetadataR1Tests(unittest.TestCase):
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

    def test_metadata_copy_projects_only_canonical_state_fields(self) -> None:
        state = self.bundle.temporal_state
        metadata = self.bundle.view_model.daxian_sequence_metadata
        self.assertIsNotNone(metadata)
        self.assertEqual(
            {
                "daxian_direction": state.daxian_direction,
                "first_daxian_nominal_age": state.first_daxian_nominal_age,
            },
            json_value(metadata),
        )

    def test_metadata_is_exported_and_replay_bound(self) -> None:
        view_payload = json_value(self.bundle.view_model)
        self.assertIn("daxian_sequence_metadata", view_payload)
        exported = self.service.export(self.bundle)
        self.assertEqual(
            view_payload["daxian_sequence_metadata"],
            exported["view_model"]["daxian_sequence_metadata"],
        )

        metadata = self.bundle.view_model.daxian_sequence_metadata
        self.assertIsNotNone(metadata)
        alternate = "REVERSE" if metadata.daxian_direction == "FORWARD" else "FORWARD"
        tampered_view = replace(
            self.bundle.view_model,
            daxian_sequence_metadata=replace(metadata, daxian_direction=alternate),
        )
        with self.assertRaises(ApplicationResolutionError) as caught:
            self.service.export(replace(self.bundle, view_model=tampered_view))
        self.assertEqual("APPLICATION_VIEW_REPLAY_MISMATCH", caught.exception.diagnostic_code)

    def test_svg_renders_sequence_metadata_only_when_temporal_is_enabled(self) -> None:
        metadata = self.bundle.view_model.daxian_sequence_metadata
        self.assertIsNotNone(metadata)
        renderer = ZiweiTwelvePalaceSvgRenderer()
        svg = renderer.render(self.bundle.view_model).svg
        self.assertIn("大限序列:", svg)
        self.assertIn(metadata.daxian_direction, svg)
        self.assertIn(f"起限虚岁{metadata.first_daxian_nominal_age}", svg)

        hidden = renderer.render(
            self.bundle.view_model,
            SvgRendererProfile(show_temporal=False),
        ).svg
        self.assertNotIn("大限序列:", hidden)
        self.assertNotIn(f"起限虚岁{metadata.first_daxian_nominal_age}", hidden)


if __name__ == "__main__":
    unittest.main()
