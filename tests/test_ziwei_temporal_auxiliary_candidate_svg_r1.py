from __future__ import annotations

import unittest
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.ziwei_application import ApplicationBirthRequest, ZiweiChartService, ZiweiTwelvePalaceSvgRenderer, ziwei_application_default_presentation_profile
from fortune_training.ziwei_chart import Sex, ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]
SVG_NS = "http://www.w3.org/2000/svg"


class ZiweiTemporalAuxiliaryCandidateSvgR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        calculation_profile = ziwei_chart_engine_v1_profile(registry)
        service = ZiweiChartService.from_repository(ROOT)
        request = ApplicationBirthRequest(
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
            minor_limit_age=8,
        )
        cls.bundle = service.resolve(request)
        cls.artifact = ZiweiTwelvePalaceSvgRenderer().render(cls.bundle.view_model)
        cls.expected = tuple(
            candidate
            for cell in sorted(cls.bundle.view_model.cells, key=lambda row: row.address_index)
            for candidate in cell.temporal_auxiliary_candidates
        )

    def test_candidate_identity_is_exposed_without_selection(self) -> None:
        self.assertTrue(self.expected)
        root = ET.fromstring(self.artifact.svg)
        groups = [
            row
            for row in root.findall(f".//{{{SVG_NS}}}g")
            if row.attrib.get("class") == "temporal-auxiliary-candidate"
        ]
        self.assertEqual(len(self.expected), len(groups))
        actual = tuple(
            (
                row.attrib["data-candidate-set-id"],
                row.attrib["data-candidate-set-hash"],
                row.attrib["data-candidate-id"],
                row.attrib["data-candidate-fact-hash"],
                row.attrib["data-frame-type"],
                row.attrib["data-star-id"],
                row.attrib["data-method-id"],
                row.attrib["data-authority-status"],
            )
            for row in groups
        )
        expected = tuple(
            (
                row.candidate_set_id,
                row.candidate_set_hash,
                row.candidate_id,
                row.candidate_fact_hash,
                row.frame_type,
                row.star_id,
                row.method_id,
                row.authority_status,
            )
            for row in self.expected
        )
        self.assertEqual(expected, actual)
        self.assertNotIn("data-selected", self.artifact.svg)
        self.assertNotIn("data-winner", self.artifact.svg)
        self.assertNotIn("data-rank", self.artifact.svg)

    def test_disputed_method_identity_is_visible_side_by_side(self) -> None:
        methods = {row.method_id for row in self.expected}
        self.assertIn("ZIWEI-QS-STRICT-S01-R1", methods)
        self.assertIn("ZIWEI-QS-WENMO-COMPAT-S01-R1", methods)
        self.assertIn("候选流曜:", self.artifact.svg)
        for row in self.expected:
            self.assertIn(row.method_id, self.artifact.svg)

    def test_candidate_metadata_disappears_when_temporal_rendering_is_disabled(self) -> None:
        from fortune_training.ziwei_application import SvgRendererProfile

        hidden = ZiweiTwelvePalaceSvgRenderer().render(
            self.bundle.view_model,
            SvgRendererProfile(show_temporal=False),
        )
        self.assertNotIn("temporal-auxiliary-candidate", hidden.svg)
        self.assertNotIn("候选流曜:", hidden.svg)


if __name__ == "__main__":
    unittest.main()
