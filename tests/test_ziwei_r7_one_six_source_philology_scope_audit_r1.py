from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from types import SimpleNamespace

from fortune_training.ziwei_chart.registries import address
from fortune_training.ziwei_structural.r7.projection import project_one_six_common_roots

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research/ZIWEI-R7-ONE-SIX-SOURCE-PHILOLOGY-SCOPE-AUDIT-R1.json"
REPLAY = ROOT / "docs/research/evidence/batch-12my/r7-one-six-geometry-replay.json"
S04 = ROOT / "sources/canonical-runtime/S04/segment-0001.txt"

IDS = "LIFE SIBLINGS SPOUSE CHILDREN WEALTH HEALTH TRAVEL SERVANTS_FRIENDS CAREER PROPERTY FORTUNE PARENTS".split()
TARGETS = {
    "LIFE": "HEALTH", "SIBLINGS": "TRAVEL", "SPOUSE": "SERVANTS_FRIENDS",
    "CHILDREN": "CAREER", "WEALTH": "PROPERTY", "HEALTH": "FORTUNE",
    "TRAVEL": "PARENTS", "SERVANTS_FRIENDS": "LIFE", "CAREER": "SIBLINGS",
    "PROPERTY": "SPOUSE", "FORTUNE": "CHILDREN", "PARENTS": "WEALTH",
}


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
    records = []
    for life_index in range(12):
        projected = project_one_six_common_roots(synthetic_r2(life_index))
        assert len(projected) == 12
        for fact in projected:
            records.append({
                "life_index": life_index,
                "origin_designation_id": fact.origin_designation_id,
                "target_designation_id": fact.target_designation_id,
                "origin_address_index": fact.origin_address.index,
                "target_address_index": fact.target_address.index,
                "relative_ordinal": fact.relative_ordinal,
                "clockwise_offset": fact.clockwise_offset,
            })
    return records


class ZiweiR7OneSixSourcePhilologyScopeAuditR1Tests(unittest.TestCase):
    def test_relative_sixth_is_health_role_and_clockwise_plus_seven(self):
        for life_index in range(12):
            for fact in project_one_six_common_roots(synthetic_r2(life_index)):
                self.assertEqual(TARGETS[fact.origin_designation_id], fact.target_designation_id)
                self.assertEqual("HEALTH", fact.relative_role_designation_id)
                self.assertEqual(6, fact.relative_ordinal)
                self.assertEqual(7, fact.clockwise_offset)
                self.assertEqual((fact.origin_address.index + 7) % 12, fact.target_address.index)

    def test_all_named_palace_rotations_match_independent_oracle(self):
        records = replay_records()
        self.assertEqual(144, len(records))
        for row in records:
            origin_pos = IDS.index(row["origin_designation_id"])
            self.assertEqual(IDS[(origin_pos + 5) % 12], row["target_designation_id"])
            self.assertEqual((row["life_index"] - origin_pos) % 12, row["origin_address_index"])
            self.assertEqual((row["origin_address_index"] + 7) % 12, row["target_address_index"])

    def test_replay_artifact_is_reproducible(self):
        replay = json.loads(REPLAY.read_text(encoding="utf-8"))
        records = replay_records()
        self.assertEqual(records, replay["records"])
        digest = hashlib.sha256(
            json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        self.assertEqual(replay["records_sha256"], digest)

    def test_s04_contains_relation_but_runtime_forbids_direct_results(self):
        text = S04.read_text(encoding="utf-8")
        self.assertIn("由命宫逆数六位，为疾厄宫。", text)
        self.assertIn("此关系称为“一六共宗”。", text)
        self.assertIn("以财帛为本宫，田宅为第六位", text)
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        self.assertFalse(audit["engineering_firewall"]["direct_event_permission"])
        self.assertFalse(audit["engineering_firewall"]["direct_endpoint_permission"])
        self.assertFalse(audit["engineering_firewall"]["modern_same_fortune_semantics_imported"])

    def test_premodern_term_and_modern_ziwei_coordinate_are_not_conflated(self):
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        self.assertTrue(audit["historical_scope"]["premodern_hetu_term_attested"])
        self.assertFalse(audit["historical_scope"]["premodern_ziwei_palace_projection_attested"])
        self.assertFalse(audit["historical_scope"]["direct_term_to_ziwei_transmission_closed"])
        self.assertEqual("SUPPORTED_BUT_SCHOOL_SPECIFIC", audit["coordinate_status"])
        self.assertEqual("MODERN_COMPATIBILITY_ONLY", audit["engineering_status"])
        self.assertFalse(audit["algorithm_reopen_authorized"])
        self.assertEqual("NONE", audit["transmission_impact"]["status"])
        for obj in audit["frozen_files"]:
            raw = (ROOT / obj["path"]).read_bytes()
            blob_sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            self.assertEqual(obj["blob_sha"], blob_sha)


if __name__ == "__main__":
    unittest.main()
