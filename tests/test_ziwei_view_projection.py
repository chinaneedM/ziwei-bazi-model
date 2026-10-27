from __future__ import annotations

import unittest
from datetime import datetime

from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_chart.integrity import HashBundle
from fortune_training.ziwei_chart.main_stars import MainStarGenerator
from fortune_training.ziwei_chart.models import NatalChartState
from fortune_training.ziwei_chart.natal import NatalStructureGenerator, NatalStructureInput
from fortune_training.ziwei_chart.temporal import ZiweiTemporalState
from fortune_training.ziwei_chart.view import (
    LexemeOverride,
    PlainTextZiweiRenderer,
    PresentationProfile,
    ViewProjectionError,
    ZiweiViewProjectionCompiler,
)


class ZiweiViewProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        structure = NatalStructureGenerator().generate(
            NatalStructureInput(
                lunar_year=2001,
                lunar_month=11,
                lunar_day=1,
                is_leap_month=False,
                lunar_month_length_days=30,
                local_apparent_solar_datetime=datetime(2001, 12, 15, 11, 50),
                life_body_leap_month_policy="CURRENT_MONTH",
            )
        )
        placements = MainStarGenerator().generate(structure.lunar_birth_day, structure.bureau.number)
        self.chart = NatalChartState(
            structure=structure,
            placements=placements,
            profile_id="TEST.CALC",
            profile_version="1.0.0",
            algorithm_versions={"natal_structure": "1.0.0", "main_stars": "1.0.1"},
        )
        self.hashes = HashBundle(fact_hash="a" * 64, computation_hash="b" * 64)
        self.compiler = ZiweiViewProjectionCompiler()

    def test_projection_is_deterministic_and_does_not_mutate_canonical_state(self) -> None:
        before = json_value(self.chart)
        profile = PresentationProfile("VIEW.DEFAULT", "1.0.0")
        first = self.compiler.compile(self.chart, self.hashes, profile)
        second = self.compiler.compile(self.chart, self.hashes, profile)

        self.assertEqual(first, second)
        self.assertEqual(first.view_hash, second.view_hash)
        self.assertEqual(len(first.cells), 12)
        self.assertEqual(json_value(self.chart), before)
        self.assertEqual(first.source_fact_hash, self.hashes.fact_hash)
        self.assertEqual(first.source_computation_hash, self.hashes.computation_hash)

    def test_lexeme_override_changes_only_view_surface_and_view_hash(self) -> None:
        before = json_value(self.chart)
        base = self.compiler.compile(
            self.chart,
            self.hashes,
            PresentationProfile("VIEW.DEFAULT", "1.0.0"),
        )
        renamed = self.compiler.compile(
            self.chart,
            self.hashes,
            PresentationProfile(
                "VIEW.ALIAS",
                "1.0.0",
                lexeme_overrides=(LexemeOverride("ENTITY", "STAR.ZIWEI", "帝星"),),
            ),
        )

        def star_label(view, entity_id: str) -> str:
            for cell in view.cells:
                for star in cell.placements:
                    if star.entity_id == entity_id:
                        return star.label
            raise AssertionError(entity_id)

        self.assertEqual(star_label(base, "STAR.ZIWEI"), "紫微")
        self.assertEqual(star_label(renamed, "STAR.ZIWEI"), "帝星")
        self.assertNotEqual(base.view_hash, renamed.view_hash)
        self.assertEqual(base.source_fact_hash, renamed.source_fact_hash)
        self.assertEqual(base.source_computation_hash, renamed.source_computation_hash)
        self.assertEqual(json_value(self.chart), before)

    def test_life_first_order_is_presentation_only(self) -> None:
        view = self.compiler.compile(
            self.chart,
            self.hashes,
            PresentationProfile("VIEW.LIFE_FIRST", "1.0.0", address_order="LIFE_FIRST_FORWARD"),
        )
        self.assertEqual(view.cells[0].address_index, self.chart.structure.life_address.index)
        self.assertEqual(view.cells[0].natal_designation_id, "LIFE")

    def test_plain_text_renderer_consumes_view_model(self) -> None:
        view = self.compiler.compile(
            self.chart,
            self.hashes,
            PresentationProfile("VIEW.TEXT", "1.0.0"),
        )
        rendered = PlainTextZiweiRenderer().render(view)
        self.assertIn("view=VIEW.TEXT@1.0.0", rendered)
        self.assertIn("fact_hash=" + "a" * 64, rendered)
        self.assertIn("紫微", rendered)

    def test_temporal_projection_requires_explicit_context(self) -> None:
        temporal = ZiweiTemporalState(
            rule_set_id="TEST",
            rule_set_version="1",
            algorithm_id="TEST",
            algorithm_version="1",
            daxian_direction="FORWARD",
            first_daxian_nominal_age=4,
            daxian_frames=(),
            annual_frames=(),
            minor_limit_frames=(),
        )
        with self.assertRaisesRegex(ViewProjectionError, "VIEW_TEMPORAL_CONTEXT_REQUIRED"):
            self.compiler.compile(
                self.chart,
                self.hashes,
                PresentationProfile("VIEW.TEMPORAL", "1.0.0"),
                temporal_state=temporal,
            )

    def test_duplicate_lexeme_override_fails_closed(self) -> None:
        profile = PresentationProfile(
            "VIEW.BAD",
            "1.0.0",
            lexeme_overrides=(
                LexemeOverride("ENTITY", "STAR.ZIWEI", "A"),
                LexemeOverride("ENTITY", "STAR.ZIWEI", "B"),
            ),
        )
        with self.assertRaisesRegex(ViewProjectionError, "VIEW_DUPLICATE_LEXEME_OVERRIDE"):
            self.compiler.compile(self.chart, self.hashes, profile)


if __name__ == "__main__":
    unittest.main()
