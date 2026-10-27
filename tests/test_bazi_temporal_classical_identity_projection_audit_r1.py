from __future__ import annotations

import unittest

from fortune_training.bazi_application.classical_annotations import (
    twelve_growth_for,
    xunkong_for_ganzhi,
)
from fortune_training.bazi_application.temporal_annotations import (
    TEMPORAL_CLASSICAL_ANNOTATION_PROFILE_VERSION,
    TEMPORAL_CLASSICAL_ANNOTATION_SOURCE_REFS,
    temporal_classical_annotation,
    temporal_classical_annotation_projection,
)
from fortune_training.bazi_chart.registries import (
    EARTHLY_BRANCHES,
    HEAVENLY_STEMS,
    SEXAGENARY_CYCLE,
)
from fortune_training.bazi_nayin_annotation.registry import entry_for_ganzhi


class BaziTemporalClassicalIdentityProjectionAuditR1Tests(unittest.TestCase):
    def _assert_components(self, annotation, day_master: str, ganzhi: str) -> None:
        parent_nayin = entry_for_ganzhi(ganzhi)
        self.assertEqual(parent_nayin.semantic_id, annotation["nayin"]["semantic_id"])
        self.assertEqual(parent_nayin.display_name, annotation["nayin"]["display_name"])
        self.assertEqual(parent_nayin.element, annotation["nayin"]["element"])
        self.assertEqual(xunkong_for_ganzhi(ganzhi), annotation["xunkong"])
        self.assertEqual(twelve_growth_for(day_master, ganzhi[1]), annotation["day_master_twelve_growth"])
        self.assertEqual(twelve_growth_for(ganzhi[0], ganzhi[1]), annotation["self_twelve_growth"])
        self.assertEqual(
            "IDENTITY_ANNOTATIONS_ONLY_NO_STRENGTH_PATTERN_OR_INTERPRETATION",
            annotation["semantic_scope"],
        )
        self.assertTrue(
            {"strength", "pattern", "useful_god", "auspiciousness", "prediction", "winner"}.isdisjoint(annotation)
        )

    def test_600_day_master_ganzhi_annotations_reuse_all_three_parent_apis(self) -> None:
        seen = 0
        for day_master in HEAVENLY_STEMS:
            for ganzhi in SEXAGENARY_CYCLE:
                annotation = temporal_classical_annotation(
                    ganzhi,
                    day_master,
                    source_layer="AUDIT",
                    context_id=f"AUDIT:{day_master}:{ganzhi}",
                )
                self._assert_components(annotation, day_master, ganzhi)
                seen += 1
        self.assertEqual(600, seen)

    def test_4200_resolved_layer_slots_preserve_component_identities_and_candidates(self) -> None:
        annotation_count = 0
        for day_master in HEAVENLY_STEMS:
            for ganzhi in SEXAGENARY_CYCLE:
                frames = {
                    layer: {"ganzhi": ganzhi, "frame_id": f"AUDIT:{layer}:{day_master}:{ganzhi}"}
                    for layer in ("DAYUN", "XIAOYUN_A", "XIAOYUN_B", "ANNUAL", "MONTHLY", "DAILY", "HOURLY")
                }
                projection = temporal_classical_annotation_projection(
                    day_master,
                    dayun_kind="DAYUN",
                    dayun_frame=frames["DAYUN"],
                    xiaoyun_candidates=[
                        {"profile_id": "AUDIT:XIAOYUN:A", "direction": "FORWARD", "active_frame": frames["XIAOYUN_A"]},
                        {"profile_id": "AUDIT:XIAOYUN:B", "direction": "REVERSE", "active_frame": frames["XIAOYUN_B"]},
                    ],
                    annual_frame=frames["ANNUAL"],
                    monthly_frame=frames["MONTHLY"],
                    daily_frame=frames["DAILY"],
                    hourly_frame=frames["HOURLY"],
                )
                slots = [projection[key] for key in ("dayun", "annual", "monthly", "daily", "hourly")]
                slots += projection["xiaoyun_candidates"]
                self.assertEqual(7, len(slots))
                for slot in slots:
                    self.assertEqual("RESOLVED", slot["status"])
                    self._assert_components(slot["annotation"], day_master, ganzhi)
                    annotation_count += 1
                self.assertEqual("XIAOYUN_CANDIDATES_PRESERVED_NO_WINNER", projection["selection_semantics"])
                self.assertEqual(
                    projection["xiaoyun_candidates"][0]["annotation"]["nayin"],
                    projection["xiaoyun_candidates"][1]["annotation"]["nayin"],
                )
                self.assertNotEqual(
                    projection["xiaoyun_candidates"][0]["annotation"]["fact_hash"],
                    projection["xiaoyun_candidates"][1]["annotation"]["fact_hash"],
                )
        self.assertEqual(4200, annotation_count)

    def test_600_illegal_ganzhi_day_master_coordinates_are_rejected_before_projection(self) -> None:
        illegal = {
            stem + branch
            for stem in HEAVENLY_STEMS
            for branch in EARTHLY_BRANCHES
        } - set(SEXAGENARY_CYCLE)
        self.assertEqual(60, len(illegal))
        rejected = 0
        for day_master in HEAVENLY_STEMS:
            for ganzhi in illegal:
                with self.assertRaises(ValueError):
                    temporal_classical_annotation(
                        ganzhi,
                        day_master,
                        source_layer="AUDIT",
                        context_id="ILLEGAL",
                    )
                rejected += 1
        self.assertEqual(600, rejected)

    def test_pre_dayun_absence_and_xiaoyun_candidate_preservation_are_unchanged(self) -> None:
        ganzhi = "庚申"
        frame = {"ganzhi": ganzhi, "frame_id": "AUDIT:TARGET"}
        projection = temporal_classical_annotation_projection(
            "辛",
            dayun_kind="PRE_DAYUN",
            dayun_frame=frame,
            xiaoyun_candidates=[
                {"profile_id": "AUDIT:XIAOYUN:A", "direction": "FORWARD", "active_frame": frame},
                {"profile_id": "AUDIT:XIAOYUN:B", "direction": "REVERSE", "active_frame": frame},
            ],
            annual_frame=frame,
            monthly_frame=frame,
            daily_frame=frame,
            hourly_frame=frame,
        )
        self.assertEqual("PRE_DAYUN_NO_GANZHI_ANNOTATION", projection["dayun"]["status"])
        self.assertIsNone(projection["dayun"]["annotation"])
        self.assertEqual(2, len(projection["xiaoyun_candidates"]))
        self.assertTrue(all(row["status"] == "RESOLVED" for row in projection["xiaoyun_candidates"]))
        self.assertEqual("XIAOYUN_CANDIDATES_PRESERVED_NO_WINNER", projection["selection_semantics"])

    def test_profile_and_component_source_lineage_match_live_release(self) -> None:
        self.assertEqual("1.0.2", TEMPORAL_CLASSICAL_ANNOTATION_PROFILE_VERSION)
        self.assertIn("S11:YHZP-CH-014", TEMPORAL_CLASSICAL_ANNOTATION_SOURCE_REFS)
        self.assertIn("S14:YHZP-CH-047", TEMPORAL_CLASSICAL_ANNOTATION_SOURCE_REFS)
        self.assertIn("S11:YHZP-CH-015", TEMPORAL_CLASSICAL_ANNOTATION_SOURCE_REFS)
        self.assertNotIn("S01:ZZZA-PR-010", TEMPORAL_CLASSICAL_ANNOTATION_SOURCE_REFS)
        self.assertNotIn("S01:ZZZA-PR-011", TEMPORAL_CLASSICAL_ANNOTATION_SOURCE_REFS)
        self.assertNotIn("S12:YHZP-CH-016", TEMPORAL_CLASSICAL_ANNOTATION_SOURCE_REFS)


if __name__ == "__main__":
    unittest.main()
