from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.bazi_application.temporal_annotations import (
    temporal_classical_annotation,
    temporal_classical_annotation_projection,
)
from fortune_training.bazi_chart.registries import (
    EARTHLY_BRANCHES,
    HEAVENLY_STEMS,
    HIDDEN_STEMS,
    SEXAGENARY_CYCLE,
)
from fortune_training.bazi_chart.ten_gods import TEN_GOD_DISPLAY, ten_god


ROOT = Path(__file__).resolve().parents[1]
ORACLE = json.loads(
    (ROOT / "tests/fixtures/bazi-temporal-ten-god-physical-table-oracle-r1.json")
    .read_text(encoding="utf-8")
)["roles"]


class BaziTemporalTenGodProjectionAuditR1Tests(unittest.TestCase):
    def test_all_100_natal_pairs_match_visually_collated_table(self):
        for day_master, targets in ORACLE.items():
            self.assertEqual(10, len(targets))
            for stem, role in targets.items():
                with self.subTest(day_master=day_master, target=stem):
                    self.assertEqual((role, TEN_GOD_DISPLAY[role]), ten_god(day_master, stem))

    def test_600_projections_preserve_4200_layer_anchors_and_equal_candidates(self):
        for day_master in HEAVENLY_STEMS:
            for ganzhi in SEXAGENARY_CYCLE:
                frames = {
                    layer: {"ganzhi": ganzhi, "frame_id": f"AUDIT:{layer}:{ganzhi}"}
                    for layer in ("DAYUN", "XIAOYUN_A", "XIAOYUN_B", "ANNUAL", "MONTHLY", "DAILY", "HOURLY")
                }
                projection = temporal_classical_annotation_projection(
                    day_master,
                    dayun_kind="DAYUN", dayun_frame=frames["DAYUN"],
                    xiaoyun_candidates=[
                        {"profile_id": f"AUDIT:{name}", "direction": "FORWARD", "active_frame": frames[name]}
                        for name in ("XIAOYUN_A", "XIAOYUN_B")
                    ],
                    annual_frame=frames["ANNUAL"], monthly_frame=frames["MONTHLY"],
                    daily_frame=frames["DAILY"], hourly_frame=frames["HOURLY"],
                )
                slots = [projection[key] for key in ("dayun", "annual", "monthly", "daily", "hourly")]
                slots += projection["xiaoyun_candidates"]
                self.assertEqual(7, len(slots))
                contexts = set()
                for slot in slots:
                    self.assertEqual("RESOLVED", slot["status"])
                    a = slot["annotation"]
                    contexts.add(a["context_id"])
                    self.assertEqual(day_master, a["day_master_stem"])
                    role = ORACLE[day_master][ganzhi[0]]
                    self.assertEqual({"semantic_role_id": role, "display_name": TEN_GOD_DISPLAY[role]}, a["visible_ten_god"])
                    self.assertEqual(list(HIDDEN_STEMS[ganzhi[1]]), [h["stem"] for h in a["hidden_stems"]])
                    for hidden in a["hidden_stems"]:
                        self.assertEqual(ORACLE[day_master][hidden["stem"]], hidden["ten_god_semantic_role_id"])
                    self.assertEqual("IDENTITY_ANNOTATIONS_ONLY_NO_STRENGTH_PATTERN_OR_INTERPRETATION", a["semantic_scope"])
                    self.assertTrue({"strength", "pattern", "useful_god", "prediction", "winner"}.isdisjoint(a))
                self.assertEqual(7, len(contexts))
                twins = projection["xiaoyun_candidates"]
                self.assertEqual(twins[0]["annotation"]["visible_ten_god"], twins[1]["annotation"]["visible_ten_god"])
                self.assertNotEqual(twins[0]["annotation"]["fact_hash"], twins[1]["annotation"]["fact_hash"])
                self.assertEqual("XIAOYUN_CANDIDATES_PRESERVED_NO_WINNER", projection["selection_semantics"])

    def test_600_illegal_ganzhi_coordinates_are_rejected(self):
        illegal = {s + b for s in HEAVENLY_STEMS for b in EARTHLY_BRANCHES} - set(SEXAGENARY_CYCLE)
        self.assertEqual(60, len(illegal))
        for day_master in HEAVENLY_STEMS:
            for ganzhi in illegal:
                with self.assertRaises(ValueError):
                    temporal_classical_annotation(ganzhi, day_master, source_layer="DAILY", context_id="ILLEGAL")

    def test_invalid_day_master_is_rejected(self):
        for day_master in ("", "子", "甲子", "A", "甲 "):
            with self.assertRaises(ValueError):
                temporal_classical_annotation("庚申", day_master, source_layer="DAILY", context_id="BAD_ANCHOR")


if __name__ == "__main__":
    unittest.main()
