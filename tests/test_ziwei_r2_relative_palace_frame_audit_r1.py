from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from types import SimpleNamespace

from fortune_training.ziwei_chart.registries import address
from fortune_training.ziwei_structural.r2.frame import RelativePalaceFrameGenerator, canonical_designation_ids

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research/ZIWEI-R2-RELATIVE-PALACE-FRAME-AUDIT-R1.json"
REPLAY = ROOT / "docs/research/evidence/batch-12nb/r2-relative-palace-frame-replay.json"
MATRIX = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"

IDS = "LIFE SIBLINGS SPOUSE CHILDREN WEALTH HEALTH TRAVEL SERVANTS_FRIENDS CAREER PROPERTY FORTUNE PARENTS".split()


def synthetic_natal(life_index: int):
    bindings = []
    for i, designation_id in enumerate(IDS):
        bindings.append(SimpleNamespace(
            designation_id=designation_id,
            address=address((life_index - i) % 12),
        ))
    return SimpleNamespace(structure=SimpleNamespace(designation_bindings=tuple(bindings)))


def replay_records():
    generator = RelativePalaceFrameGenerator()
    rows = []
    for life_index in range(12):
        facts = generator.generate(synthetic_natal(life_index))
        assert len(facts) == 144
        for fact in facts:
            rows.append({
                "life_index": life_index,
                "origin_designation_id": fact.origin_designation_id,
                "origin_address_index": fact.origin_address.index,
                "relative_ordinal": fact.relative_ordinal,
                "relative_role_designation_id": fact.relative_role_designation_id,
                "target_designation_id": fact.target_designation_id,
                "target_address_index": fact.target_address.index,
                "clockwise_offset": fact.clockwise_offset,
            })
    return rows


class ZiweiR2RelativePalaceFrameAuditR1Tests(unittest.TestCase):
    def test_frozen_designation_order_matches_historical_upstream_row(self):
        self.assertEqual(tuple(IDS), canonical_designation_ids())
        matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        upstream = next(row for row in matrix["rows"] if row["rule_id"] == "HPA-ZIWEI-003")
        self.assertEqual("HISTORICALLY_SUPPORTED", upstream["audit_status"])
        self.assertIn("一命宫 二兄弟 三妻妾 四子女 五财帛 六疾厄 七迁移 八奴仆 九官禄 十田宅 十一福德 十二父母", upstream["source_quote"])

    def test_all_12_physical_rotations_produce_complete_144_fact_frames(self):
        generator = RelativePalaceFrameGenerator()
        for life_index in range(12):
            facts = generator.generate(synthetic_natal(life_index))
            self.assertEqual(144, len(facts))
            self.assertEqual(144, len({(x.origin_designation_id, x.relative_ordinal) for x in facts}))

    def test_all_1728_rows_match_independent_rotation_oracle(self):
        rows = replay_records()
        self.assertEqual(1728, len(rows))
        for row in rows:
            i = IDS.index(row["origin_designation_id"])
            j = row["relative_ordinal"] - 1
            self.assertEqual(IDS[j], row["relative_role_designation_id"])
            self.assertEqual(IDS[(i + j) % 12], row["target_designation_id"])
            self.assertEqual((row["life_index"] - i) % 12, row["origin_address_index"])
            self.assertEqual((row["life_index"] - i - j) % 12, row["target_address_index"])
            self.assertEqual((-j) % 12, row["clockwise_offset"])

    def test_replay_artifact_is_reproducible(self):
        replay = json.loads(REPLAY.read_text(encoding="utf-8"))
        rows = replay_records()
        self.assertEqual(rows, replay["records"])
        digest = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(replay["records_sha256"], digest)

    def test_modern_frame_scope_keeps_named_semantics_disabled(self):
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        self.assertEqual("MODERN_COMPATIBILITY_ONLY", audit["audit_status"])
        self.assertFalse(audit["historical_scope"]["r2_144_fact_matrix_claimed_as_classical"])
        self.assertFalse(audit["semantic_firewall"]["named_traditional_semantics_enabled"])
        self.assertFalse(audit["algorithm_reopen_authorized"])
        self.assertEqual("NONE", audit["transmission_impact"]["status"])
        for obj in audit["frozen_files"]:
            raw = (ROOT / obj["path"]).read_bytes()
            blob_sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            self.assertEqual(obj["blob_sha"], blob_sha)


if __name__ == "__main__":
    unittest.main()
