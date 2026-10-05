from __future__ import annotations

import hashlib
import json
import unittest
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.ziwei_chart import Sex, ZiweiChartFoundation, ZiweiChartRequest, ziwei_chart_engine_v1_profile
from fortune_training.ziwei_chart.registries import address
from fortune_training.ziwei_chart.rings import WenmoDefaultRingGenerator

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "docs/research/ZIWEI-THREE-RING-SOURCE-SCOPE-AUDIT-R1.json"
REPLAY_PATH = ROOT / "docs/research/evidence/batch-12mv/three-ring-replay.json"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
STEMS = "甲乙丙丁戊己庚辛壬癸"
# Independent S01 PR-058..060 / received-text tables, not runtime constants.
ORDERS = {
    "RING.TAISUI12": "岁建 晦气 丧门 贯索 官符 小耗 岁破 龙德 白虎 天德 吊客 病符".split(),
    "RING.JIANGQIAN12": "将星 攀鞍 岁驿 息神 华盖 劫煞 灾煞 天煞 指背 咸池 月煞 亡神".split(),
    "RING.BOSHI12": "博士 力士 青龙 小耗 将军 奏书 飞廉 喜神 病符 大耗 伏兵 官符".split(),
}
WANG_ANCHORS = "子酉午卯子酉午卯子酉午卯"
LUCUN_BY_STEM = "寅卯巳午巳午申酉亥子"


def replay_records():
    records = []
    generator = WenmoDefaultRingGenerator()
    for cycle in range(60):
        stem, branch = STEMS[cycle % 10], BRANCHES[cycle % 12]
        lucun = BRANCHES.index(LUCUN_BY_STEM[cycle % 10])
        for sex in (Sex.MALE, Sex.FEMALE):
            direction = 1 if (cycle % 2 == 0) == (sex is Sex.MALE) else -1
            rings = (generator.taisui(branch), generator.jiangqian(branch), generator.boshi(address(lucun), stem, sex))
            anchors = (cycle % 12, BRANCHES.index(WANG_ANCHORS[cycle % 12]), lucun)
            member_ids = set()
            outputs = []
            for ring, anchor, step in zip(rings, anchors, (1, 1, direction)):
                assert ring.anchor_address.index == anchor
                assert ring.direction == ("FORWARD" if step == 1 else "REVERSE")
                assert len(ring.members) == 12
                assert [m.display_name for m in ring.members] == ORDERS[ring.ring_id]
                assert [m.ordinal for m in ring.members] == list(range(12))
                indices = [(anchor + step * i) % 12 for i in range(12)]
                assert [m.address.index for m in ring.members] == indices
                for member in ring.members:
                    assert member.member_id.startswith(ring.ring_id + ".")
                    assert member.member_id not in member_ids
                    member_ids.add(member.member_id)
                outputs.append({"ring_id": ring.ring_id, "anchor_index": anchor, "direction": ring.direction, "member_indices": indices})
            records.append({"ganzhi": stem + branch, "sex": sex.value, "lucun_index": lucun, "rings": outputs})
    return records


class ZiweiThreeRingSourceScopeAuditR1Tests(unittest.TestCase):
    def test_all_legal_ganzhi_and_sexes_match_separate_source_tables(self):
        records = replay_records()
        self.assertEqual(120, len(records))
        self.assertEqual(60, len({r["ganzhi"] for r in records}))
        self.assertEqual(4320, sum(len(g["member_indices"]) for r in records for g in r["rings"]))

    def test_replay_artifact_is_reproducible(self):
        replay = json.loads(REPLAY_PATH.read_text())
        records = replay_records()
        self.assertEqual(records, replay["records"])
        digest = hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(digest, replay["records_sha256"])

    def test_natal_pipeline_consumes_birth_branch_and_lucun(self):
        registry = PolicyRegistry.from_file(ROOT / "config/time-calendar-policies.json")
        profile = ziwei_chart_engine_v1_profile(registry)
        result = ZiweiChartFoundation(TimeCalendarFoundation(registry)).resolve_typed(ZiweiChartRequest(
            birth=BirthInput(reported_local_datetime=datetime(2001, 6, 17, 12, 30), birth_place="Beijing", latitude=39.9042, longitude=116.4, timezone_id="Asia/Shanghai"),
            sex=Sex.MALE, profile=profile,
        ))
        self.assertEqual("RESOLVED", result.status)
        chart = result.candidates[0].chart
        rings = {r.ring_id: r for r in chart.rings}
        birth_branch = chart.structure.ziwei_birth_year_branch
        self.assertEqual("巳", birth_branch)
        self.assertEqual(birth_branch, rings["RING.TAISUI12"].anchor_address.branch)
        self.assertEqual("酉", rings["RING.JIANGQIAN12"].anchor_address.branch)
        lucun = next(p.address for p in chart.placements if p.entity_id == "STAR.LUCUN")
        self.assertEqual(lucun, rings["RING.BOSHI12"].anchor_address)
        physical_ids = {p.entity_id for p in chart.placements}
        self.assertTrue(all(m.member_id not in physical_ids for r in rings.values() for m in r.members))

    def test_four_taisui_label_variants_are_not_silently_aliased(self):
        audit = json.loads(AUDIT_PATH.read_text())
        variants = audit["taisui"]["label_variants"]
        self.assertEqual([1, 3, 5, 9], [v["ordinal"] for v in variants])
        self.assertTrue(all(v["alias_equivalence_established"] is False for v in variants))
        self.assertEqual("DISPUTED_MULTIPLE_CANDIDATES", audit["taisui"]["status"])

    def test_source_and_time_layer_firewalls_survive_parent_decomposition(self):
        audit = json.loads(AUDIT_PATH.read_text())
        self.assertEqual("SOURCE_INSUFFICIENT", audit["jiangqian"]["status"])
        self.assertFalse(audit["jiangqian"]["received_fullbook_attribution_verified"])
        self.assertFalse(audit["runtime_contract"]["annual_target_ring_materialization_claimed"])
        self.assertFalse(audit["runtime_contract"]["normalized_pr_atom_is_classical_authority"])
        self.assertEqual(["HPA-ZIWEI-019", "HPA-ZIWEI-024"], audit["reused_audited_rows"])
        self.assertEqual(["HPA-ZIWEI-025", "HPA-ZIWEI-026"], audit["new_child_rows"])

    def test_same_label_across_rings_preserves_distinct_member_identities(self):
        g = WenmoDefaultRingGenerator()
        a, b = g.taisui("子"), g.boshi(address(0), "甲", Sex.MALE)
        for name in ("官符", "小耗", "病符"):
            x = next(m for m in a.members if m.display_name == name)
            y = next(m for m in b.members if m.display_name == name)
            self.assertNotEqual(x.member_id, y.member_id)
            self.assertNotEqual(x.ordinal, y.ordinal)


if __name__ == "__main__":
    unittest.main()
