from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from types import SimpleNamespace

from fortune_training.ziwei_chart.registries import address
from fortune_training.ziwei_structural.r8.projection import project_adjacent_palace_pairs

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research/ZIWEI-R8-ADJACENT-PALACE-SOURCE-PHILOLOGY-SCOPE-AUDIT-R1.json"
REPLAY = ROOT / "docs/research/evidence/batch-12mz/r8-adjacent-palace-geometry-replay.json"
S04 = ROOT / "sources/canonical-runtime/S04/segment-0001.txt"
S05 = ROOT / "sources/canonical-runtime/S05/segment-0015.txt"

IDS = "LIFE SIBLINGS SPOUSE CHILDREN WEALTH HEALTH TRAVEL SERVANTS_FRIENDS CAREER PROPERTY FORTUNE PARENTS".split()


def synthetic_r2(life_index: int):
    facts = []
    for origin_pos, origin_id in enumerate(IDS):
        origin_index = (life_index - origin_pos) % 12
        for role_offset, role_id in enumerate(IDS):
            target_id = IDS[(origin_pos + role_offset) % 12]
            facts.append(SimpleNamespace(
                origin_designation_id=origin_id,
                origin_address=address(origin_index),
                relative_ordinal=role_offset + 1,
                relative_role_designation_id=role_id,
                target_designation_id=target_id,
                target_address=address((origin_index - role_offset) % 12),
                clockwise_offset=(-role_offset) % 12,
            ))
    return SimpleNamespace(frame_facts=tuple(facts))


def replay_records():
    rows = []
    for life_index in range(12):
        projected = project_adjacent_palace_pairs(synthetic_r2(life_index))
        assert len(projected) == 12
        for fact in projected:
            rows.append({
                "life_index": life_index,
                "origin_designation_id": fact.origin_designation_id,
                "counterclockwise_designation_id": fact.counterclockwise_designation_id,
                "clockwise_designation_id": fact.clockwise_designation_id,
                "origin_address_index": fact.origin_address.index,
                "counterclockwise_address_index": fact.counterclockwise_address.index,
                "clockwise_address_index": fact.clockwise_address.index,
                "counterclockwise_relative_ordinal": fact.counterclockwise_relative_ordinal,
                "counterclockwise_clockwise_offset": fact.counterclockwise_clockwise_offset,
                "clockwise_relative_ordinal": fact.clockwise_relative_ordinal,
                "clockwise_clockwise_offset": fact.clockwise_clockwise_offset,
            })
    return rows


class ZiweiR8AdjacentPalaceSourcePhilologyScopeAuditR1Tests(unittest.TestCase):
    def test_bilateral_geometry_matches_relative_two_and_twelve(self):
        for life_index in range(12):
            for fact in project_adjacent_palace_pairs(synthetic_r2(life_index)):
                i = IDS.index(fact.origin_designation_id)
                self.assertEqual(IDS[(i + 1) % 12], fact.counterclockwise_designation_id)
                self.assertEqual(IDS[(i - 1) % 12], fact.clockwise_designation_id)
                self.assertEqual(2, fact.counterclockwise_relative_ordinal)
                self.assertEqual(11, fact.counterclockwise_clockwise_offset)
                self.assertEqual(12, fact.clockwise_relative_ordinal)
                self.assertEqual(1, fact.clockwise_clockwise_offset)
                self.assertEqual((fact.origin_address.index + 11) % 12, fact.counterclockwise_address.index)
                self.assertEqual((fact.origin_address.index + 1) % 12, fact.clockwise_address.index)

    def test_all_named_palace_rotations_match_independent_oracle(self):
        rows = replay_records()
        self.assertEqual(144, len(rows))
        for row in rows:
            i = IDS.index(row["origin_designation_id"])
            self.assertEqual(IDS[(i + 1) % 12], row["counterclockwise_designation_id"])
            self.assertEqual(IDS[(i - 1) % 12], row["clockwise_designation_id"])
            self.assertEqual((row["life_index"] - i) % 12, row["origin_address_index"])

    def test_replay_artifact_is_reproducible(self):
        replay = json.loads(REPLAY.read_text(encoding="utf-8"))
        rows = replay_records()
        self.assertEqual(rows, replay["records"])
        digest = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(replay["records_sha256"], digest)

    def test_source_term_and_flank_semantics_are_distinct(self):
        s04 = S04.read_text(encoding="utf-8")
        s05 = S05.read_text(encoding="utf-8")
        self.assertIn("本宫两侧相邻之两个宫垣。如子宫为本宫，则丑宫与亥宫即为其邻宫。", s04)
        self.assertIn("十五、邻宫", s05)
        self.assertIn("两星曜位于本宫之邻宫，称为相夹", s05)
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        fw = audit["engineering_firewall"]
        self.assertFalse(fw["flank_semantics_permission"])
        self.assertFalse(fw["direct_event_permission"])
        self.assertFalse(fw["direct_endpoint_permission"])
        self.assertFalse(fw["direct_score_permission"])
        self.assertFalse(fw["premodern_flank_patterns_imported"])

    def test_historical_scope_and_metadata_correction_are_explicit(self):
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        hs = audit["historical_scope"]
        self.assertTrue(hs["premodern_specific_flank_patterns_attested"])
        self.assertFalse(hs["premodern_generic_adjacent_term_definition_attested"])
        self.assertFalse(hs["direct_fullbook_to_zhongzhou_term_transmission_closed"])
        self.assertEqual("PROV-DEFECT-019", audit["provenance_correction"]["defect_id"])
        self.assertTrue(audit["provenance_correction"]["repaired"])
        self.assertFalse(audit["algorithm_reopen_authorized"])
        self.assertEqual("NONE", audit["transmission_impact"]["status"])
        for obj in audit["frozen_files"]:
            raw = (ROOT / obj["path"]).read_bytes()
            blob_sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            self.assertEqual(obj["blob_sha"], blob_sha)


if __name__ == "__main__":
    unittest.main()
