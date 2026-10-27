from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from types import SimpleNamespace

from fortune_training.ziwei_chart.registries import address
from fortune_training.ziwei_structural.r6.projection import project_qishu_positions

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research/ZIWEI-R6-QISHU-SOURCE-PHILOLOGY-SCOPE-AUDIT-R1.json"
REPLAY = ROOT / "docs/research/evidence/batch-12mx/r6-qishu-geometry-replay.json"
S04_RUNTIME = ROOT / "sources/canonical-runtime/S04/segment-0001.txt"
S04_ATOMS = ROOT / "sources/canonical-runtime/S04/segment-0003.txt"

IDS = "LIFE SIBLINGS SPOUSE CHILDREN WEALTH HEALTH TRAVEL SERVANTS_FRIENDS CAREER PROPERTY FORTUNE PARENTS".split()
TARGETS = {
    "LIFE": "CAREER", "SIBLINGS": "PROPERTY", "SPOUSE": "FORTUNE", "CHILDREN": "PARENTS",
    "WEALTH": "LIFE", "HEALTH": "SIBLINGS", "TRAVEL": "SPOUSE", "SERVANTS_FRIENDS": "CHILDREN",
    "CAREER": "WEALTH", "PROPERTY": "HEALTH", "FORTUNE": "TRAVEL", "PARENTS": "SERVANTS_FRIENDS",
}


def synthetic_r2(life_index: int):
    facts = []
    for origin_pos, origin_id in enumerate(IDS):
        origin_index = (life_index - origin_pos) % 12
        for role_offset, role_id in enumerate(IDS):
            target_id = IDS[(origin_pos + role_offset) % 12]
            facts.append(SimpleNamespace(
                origin_designation_id=origin_id, origin_address=address(origin_index),
                relative_ordinal=role_offset + 1, relative_role_designation_id=role_id,
                target_designation_id=target_id, target_address=address((origin_index - role_offset) % 12),
                clockwise_offset=(-role_offset) % 12,
            ))
    return SimpleNamespace(frame_facts=tuple(facts))


def replay_records():
    records = []
    for life_index in range(12):
        projected = project_qishu_positions(synthetic_r2(life_index))
        assert len(projected) == 12
        for fact in projected:
            records.append({
                "life_index": life_index, "origin_designation_id": fact.origin_designation_id,
                "target_designation_id": fact.target_designation_id, "origin_address_index": fact.origin_address.index,
                "target_address_index": fact.target_address.index, "relative_ordinal": fact.relative_ordinal,
                "clockwise_offset": fact.clockwise_offset,
            })
    return records


class ZiweiR6QiShuSourcePhilologyScopeAuditR1Tests(unittest.TestCase):
    def test_inverse_ninth_is_relative_career_and_clockwise_plus_four(self):
        for life_index in range(12):
            for fact in project_qishu_positions(synthetic_r2(life_index)):
                self.assertEqual(TARGETS[fact.origin_designation_id], fact.target_designation_id)
                self.assertEqual(9, fact.relative_ordinal)
                self.assertEqual(4, fact.clockwise_offset)
                self.assertEqual((fact.origin_address.index + 4) % 12, fact.target_address.index)

    def test_all_named_palace_rotations_match_independent_oracle(self):
        records = replay_records()
        self.assertEqual(144, len(records))
        for row in records:
            origin_pos = IDS.index(row["origin_designation_id"])
            self.assertEqual(IDS[(origin_pos + 8) % 12], row["target_designation_id"])
            self.assertEqual((row["life_index"] - origin_pos) % 12, row["origin_address_index"])
            self.assertEqual((row["origin_address_index"] + 4) % 12, row["target_address_index"])

    def test_replay_artifact_is_reproducible(self):
        replay = json.loads(REPLAY.read_text(encoding="utf-8"))
        records = replay_records()
        self.assertEqual(records, replay["records"])
        digest = hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(replay["records_sha256"], digest)

    def test_s04_anchor_and_semantic_firewall_are_explicit(self):
        runtime = S04_RUNTIME.read_text(encoding="utf-8")
        atoms = S04_ATOMS.read_text(encoding="utf-8")
        self.assertIn("气数位是当前主题宫在其主题太极中的官禄位，只表示现实承接", runtime)
        self.assertIn("气数位见禄=成功", runtime)
        self.assertIn("气数位见忌=失败", runtime)
        self.assertIn("由命宫逆数九位，为官禄宫。此宫位在河洛法中称为“气数位”", atoms)
        self.assertIn("各宫之第九位（本宫逆数九位）为其官禄宫，亦称“气数位”", atoms)

    def test_historical_and_engineering_scope_remain_separate_and_frozen(self):
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        self.assertEqual("SUPPORTED_BUT_SCHOOL_SPECIFIC", audit["coordinate_status"])
        self.assertEqual("MODERN_COMPATIBILITY_ONLY", audit["semantic_closure_status"])
        self.assertFalse(audit["historical_scope"]["premodern_qishu_attestation_closed"])
        self.assertFalse(audit["historical_scope"]["earliest_qishu_definition_closed"])
        self.assertFalse(audit["historical_scope"]["exact_physical_edition_bound"])
        self.assertFalse(audit["semantic_firewall"]["project_fixed_support_meanings_are_verbatim_historical_text"])
        self.assertFalse(audit["algorithm_reopen_authorized"])
        self.assertEqual("NONE", audit["transmission_impact"]["status"])
        for obj in audit["frozen_files"]:
            raw = (ROOT / obj["path"]).read_bytes()
            blob_sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            self.assertEqual(obj["blob_sha"], blob_sha)


if __name__ == "__main__":
    unittest.main()
