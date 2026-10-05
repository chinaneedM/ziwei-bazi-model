from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from fortune_training.ziwei_structural import NeutralZ12Topology, canonical_addresses, shift

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research/ZIWEI-R1-NEUTRAL-Z12-TOPOLOGY-AUDIT-R1.json"
REPLAY = ROOT / "docs/research/evidence/batch-12na/r1-neutral-z12-topology-replay.json"


def runtime_records():
    return [
        {
            "source_index": row.source.index,
            "source_branch": row.source.branch,
            "target_index": row.target.index,
            "target_branch": row.target.branch,
            "clockwise_offset": row.clockwise_offset,
        }
        for row in NeutralZ12Topology().generate()
    ]


class ZiweiR1NeutralZ12TopologyAuditR1Tests(unittest.TestCase):
    def test_complete_ordered_pair_matrix_matches_modular_oracle(self):
        rows = runtime_records()
        self.assertEqual(144, len(rows))
        self.assertEqual(144, len({(r["source_index"], r["target_index"]) for r in rows}))
        for row in rows:
            self.assertEqual((row["target_index"] - row["source_index"]) % 12, row["clockwise_offset"])

    def test_each_source_covers_all_targets_and_shift_is_invertible(self):
        addresses = canonical_addresses()
        for source in addresses:
            source_rows = [row for row in NeutralZ12Topology().generate() if row.source == source]
            self.assertEqual(set(range(12)), {row.target.index for row in source_rows})
            for offset in range(12):
                self.assertEqual(source, shift(shift(source, offset), -offset))
            self.assertEqual(source, shift(shift(source, 6), 6))

    def test_replay_artifact_is_reproducible(self):
        replay = json.loads(REPLAY.read_text(encoding="utf-8"))
        rows = runtime_records()
        self.assertEqual(rows, replay["records"])
        digest = hashlib.sha256(
            json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        ).hexdigest()
        self.assertEqual(replay["records_sha256"], digest)

    def test_audit_explicitly_disclaims_historical_doctrine_and_named_semantics(self):
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        self.assertEqual("MODERN_COMPATIBILITY_ONLY", audit["audit_status"])
        self.assertTrue(audit["scope"]["modern_computational_substrate"])
        self.assertFalse(audit["scope"]["historical_doctrine_claim"])
        self.assertFalse(audit["scope"]["named_traditional_semantics_enabled"])
        self.assertFalse(audit["algorithm_reopen_authorized"])
        self.assertEqual("NONE", audit["transmission_impact"]["status"])

    def test_frozen_files_remain_byte_identical(self):
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        for obj in audit["frozen_files"]:
            raw = (ROOT / obj["path"]).read_bytes()
            blob_sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            self.assertEqual(obj["blob_sha"], blob_sha)


if __name__ == "__main__":
    unittest.main()
