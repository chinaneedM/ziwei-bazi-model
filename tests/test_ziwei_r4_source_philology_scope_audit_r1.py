from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from types import SimpleNamespace

from fortune_training.ziwei_chart.registries import address
from fortune_training.ziwei_structural.r4.semantics import NamedStructuralSemanticCompiler

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research/ZIWEI-R4-SOURCE-PHILOLOGY-SCOPE-AUDIT-R1.json"
REPLAY = ROOT / "docs/research/evidence/batch-12mw/r4-geometry-replay.json"
# Independent explicit named-palace oracle; not imported from R4/R2 tables.
IDS = "LIFE SIBLINGS SPOUSE CHILDREN WEALTH HEALTH TRAVEL SERVANTS_FRIENDS CAREER PROPERTY FORTUNE PARENTS".split()
TABLE = [
    ("WEALTH CAREER", "TRAVEL"), ("HEALTH PROPERTY", "SERVANTS_FRIENDS"),
    ("TRAVEL FORTUNE", "CAREER"), ("SERVANTS_FRIENDS PARENTS", "PROPERTY"),
    ("LIFE CAREER", "FORTUNE"), ("SIBLINGS PROPERTY", "PARENTS"),
    ("SPOUSE FORTUNE", "LIFE"), ("CHILDREN PARENTS", "SIBLINGS"),
    ("LIFE WEALTH", "SPOUSE"), ("SIBLINGS HEALTH", "CHILDREN"),
    ("SPOUSE TRAVEL", "WEALTH"), ("CHILDREN SERVANTS_FRIENDS", "HEALTH"),
]


def replay_records():
    records = []
    for life_index in range(12):
        rows = []
        for i, origin in enumerate(IDS):
            for offset in range(12):
                rows.append(SimpleNamespace(
                    origin_designation_id=origin, origin_address=address((life_index - i) % 12),
                    clockwise_offset=offset, target_designation_id=IDS[(i - offset) % 12],
                    target_address=address((life_index - i + offset) % 12),
                ))
        axes, groups, frames = NamedStructuralSemanticCompiler().compile(SimpleNamespace(frame_facts=rows))
        assert (len(axes), len(groups), len(frames)) == (6, 4, 12)
        for i, frame in enumerate(frames):
            partners, opposite = TABLE[i]
            assert frame.origin_designation_id == IDS[i]
            assert set(frame.trine_partner_designation_ids) == set(partners.split())
            assert frame.opposition_designation_id == opposite
            origin = (life_index - i) % 12
            assert frame.origin_address.index == origin
            assert tuple(a.index for a in frame.trine_partner_addresses) == ((origin + 4) % 12, (origin + 8) % 12)
            assert frame.opposition_address.index == (origin + 6) % 12
            assert frame.trine_offsets == (4, 8) and frame.opposition_offset == 6
            group = next(g for g in groups if g.group_key == frame.trine_group_key)
            assert set(group.member_designation_ids) == {IDS[i], *partners.split()}
            records.append({"life_index": life_index, "origin": IDS[i], "origin_index": origin,
                            "trine_ids": list(frame.trine_partner_designation_ids),
                            "trine_indices": [a.index for a in frame.trine_partner_addresses],
                            "opposition_id": opposite, "opposition_index": frame.opposition_address.index})
    return records


class ZiweiR4SourcePhilologyScopeAuditR1Tests(unittest.TestCase):
    def test_all_rotations_and_named_origins_match_independent_table(self):
        self.assertEqual(144, len(replay_records()))

    def test_source_zi_example_preserves_trines_opposition_and_origin(self):
        record = next(r for r in replay_records() if r["life_index"] == 0 and r["origin"] == "LIFE")
        self.assertEqual([4, 8], record["trine_indices"])
        self.assertEqual(6, record["opposition_index"])
        self.assertEqual({0, 4, 6, 8}, {record["origin_index"], *record["trine_indices"], record["opposition_index"]})

    def test_replay_artifact_is_reproducible(self):
        replay = json.loads(REPLAY.read_text())
        records = replay_records()
        self.assertEqual(records, replay["records"])
        digest = hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(digest, replay["records_sha256"])

    def test_early_term_attestation_does_not_certify_modern_definition(self):
        audit = json.loads(AUDIT.read_text())
        self.assertFalse(audit["historical_scope"]["early_exact_four_palace_definition_closed"])
        self.assertFalse(audit["historical_scope"]["modern_manual_exact_impression_bound"])
        self.assertEqual("MODERN_COMPATIBILITY_ONLY", audit["parent_status"])
        self.assertEqual("SUPPORTED_BUT_SCHOOL_SPECIFIC", audit["geometry_status"])

    def test_frozen_source_and_runtime_blobs_are_unchanged(self):
        audit = json.loads(AUDIT.read_text())
        for obj in audit["frozen_files"]:
            raw = (ROOT / obj["path"]).read_bytes()
            self.assertEqual(obj["blob_sha"], hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest())
        self.assertFalse(audit["algorithm_reopen_authorized"])


if __name__ == "__main__":
    unittest.main()
