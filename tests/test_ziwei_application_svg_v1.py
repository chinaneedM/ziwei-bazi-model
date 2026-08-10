from __future__ import annotations

import json
import unittest
import xml.etree.ElementTree as ET
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_application import (
    ApplicationBirthRequest,
    SvgRendererProfile,
    ZiweiChartService,
    ZiweiTwelvePalaceSvgRenderer,
    ziwei_application_default_presentation_profile,
)
from fortune_training.ziwei_chart import LexemeOverride, Sex, ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]
SVG_NS = "http://www.w3.org/2000/svg"


class ZiweiApplicationSvgV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.calculation_profile = ziwei_chart_engine_v1_profile(registry)
        cls.service = ZiweiChartService.from_repository(ROOT)
        cls.presentation = ziwei_application_default_presentation_profile()
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
            presentation_profile=cls.presentation,
            daxian_frame_id="DAXIAN:index=1",
            annual_year=2001,
            minor_limit_age=8,
        )
        cls.bundle = cls.service.resolve(cls.request)
        cls.renderer = ZiweiTwelvePalaceSvgRenderer()
        cls.artifact = cls.renderer.render(cls.bundle.view_model)

    def test_one_bundle_renders_valid_standalone_svg(self) -> None:
        artifact = self.artifact
        self.assertEqual("ZIWEI-TWELVE-PALACE-SVG-ARTIFACT-V1", artifact.schema)
        self.assertEqual(self.bundle.view_model.view_hash, artifact.source_view_hash)
        self.assertRegex(artifact.render_hash, r"^[0-9a-f]{64}$")
        self.assertTrue(artifact.svg.startswith('<?xml version="1.0" encoding="UTF-8"?>'))
        root = ET.fromstring(artifact.svg)
        self.assertEqual(f"{{{SVG_NS}}}svg", root.tag)
        self.assertNotIn("<script", artifact.svg.lower())
        self.assertNotIn("http://", artifact.svg.replace("http://www.w3.org/2000/svg", ""))
        self.assertNotIn("https://", artifact.svg)

    def test_exactly_twelve_unique_palace_groups_exist(self) -> None:
        root = ET.fromstring(self.artifact.svg)
        groups = [
            row
            for row in root.findall(f".//{{{SVG_NS}}}g")
            if row.attrib.get("id", "").startswith("palace-")
        ]
        self.assertEqual(12, len(groups))
        self.assertEqual(set(range(12)), {int(row.attrib["data-address-index"]) for row in groups})
        self.assertEqual(12, len({row.attrib["data-branch"] for row in groups}))

    def test_temporal_dignity_and_transformation_content_are_visible(self) -> None:
        svg = self.artifact.svg
        self.assertIn("DAXIAN:", svg)
        self.assertIn("ANNUAL:", svg)
        self.assertIn("小限:", svg)
        self.assertTrue(any(token in svg for token in ("[庙]", "[旺]", "[得]", "[利]", "[平]", "[不]", "[陷]", "[未评级]")))
        self.assertTrue(any(token in svg for token in ("化禄", "化权", "化科", "化忌")))

    def test_repeated_render_is_byte_and_hash_identical(self) -> None:
        replay = self.renderer.render(self.bundle.view_model)
        self.assertEqual(self.artifact.svg, replay.svg)
        self.assertEqual(self.artifact.render_hash, replay.render_hash)
        self.assertEqual(self.artifact, replay)

    def test_input_cell_order_does_not_change_canonical_svg(self) -> None:
        reordered = replace(
            self.bundle.view_model,
            cells=tuple(reversed(self.bundle.view_model.cells)),
        )
        artifact = self.renderer.render(reordered)
        self.assertEqual(self.artifact.svg, artifact.svg)
        self.assertEqual(self.artifact.render_hash, artifact.render_hash)

    def test_presentation_lexeme_change_changes_view_and_render_hashes(self) -> None:
        changed_presentation = replace(
            self.presentation,
            lexeme_overrides=(
                LexemeOverride(namespace="DESIGNATION", object_id="LIFE", label="命宫·校验"),
            ),
        )
        changed_bundle = self.service.resolve(
            replace(self.request, presentation_profile=changed_presentation)
        )
        changed_artifact = self.renderer.render(changed_bundle.view_model)
        self.assertNotEqual(self.bundle.view_model.view_hash, changed_bundle.view_model.view_hash)
        self.assertNotEqual(self.artifact.render_hash, changed_artifact.render_hash)
        self.assertIn("命宫·校验", changed_artifact.svg)

    def test_renderer_only_geometry_changes_render_hash_not_view_hash(self) -> None:
        profile = replace(SvgRendererProfile(), width=1280)
        changed = self.renderer.render(self.bundle.view_model, profile)
        self.assertEqual(self.bundle.view_model.view_hash, changed.source_view_hash)
        self.assertEqual(self.artifact.source_view_hash, changed.source_view_hash)
        self.assertNotEqual(self.artifact.render_hash, changed.render_hash)
        self.assertNotEqual(self.artifact.svg, changed.svg)

    def test_unsafe_xml_text_is_escaped(self) -> None:
        first = self.bundle.view_model.cells[0]
        unsafe = replace(first, natal_designation_label='<script>alert("x")</script>&')
        unsafe_view = replace(
            self.bundle.view_model,
            cells=(unsafe, *self.bundle.view_model.cells[1:]),
        )
        artifact = self.renderer.render(unsafe_view)
        ET.fromstring(artifact.svg)
        self.assertNotIn('<script>alert("x")</script>', artifact.svg)
        self.assertIn("&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;&amp;", artifact.svg)

    def test_svg_artifact_validates_against_independent_schema(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "ziwei-twelve-palace-svg-artifact-v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        Draft202012Validator.check_schema(schema)
        errors = list(Draft202012Validator(schema).iter_errors(json_value(self.artifact)))
        if errors:
            self.fail("SVG artifact schema failed: " + "; ".join(row.message for row in errors))

    def test_render_does_not_mutate_source_view(self) -> None:
        before = json_value(self.bundle.view_model)
        self.renderer.render(self.bundle.view_model)
        self.assertEqual(before, json_value(self.bundle.view_model))


if __name__ == "__main__":
    unittest.main()
