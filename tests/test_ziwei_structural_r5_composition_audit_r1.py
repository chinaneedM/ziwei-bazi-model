from __future__ import annotations

import json
import unittest
from collections import Counter
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_chart import Sex, ZiweiChartFoundation, ZiweiChartRequest, ziwei_chart_engine_v1_profile
from fortune_training.ziwei_structural import ZiweiStructuralRuntime, ziwei_structural_v2_r1_profile
from fortune_training.ziwei_structural.r2 import ZiweiRelativePalaceFrameRuntime, ziwei_structural_v2_r2_profile
from fortune_training.ziwei_structural.r3 import ZiweiBorrowProjectionRuntime, ziwei_structural_v2_r3_profile
from fortune_training.ziwei_structural.r4 import ZiweiNamedStructuralSemanticRuntime, ziwei_structural_v2_r4_profile
from fortune_training.ziwei_structural.r5 import ZiweiResolvedStructuralRuntime, ziwei_structural_v2_r5_profile
from fortune_training.ziwei_structural.r5.composition import ResolvedStructuralComposer

ROOT = Path(__file__).resolve().parents[1]


def build_states(month: int, hour_branch: int, sex: Sex):
    registry = PolicyRegistry.from_file(ROOT / "config/time-calendar-policies.json")
    request = ZiweiChartRequest(
        birth=BirthInput(
            reported_local_datetime=datetime(1994, month, 17, hour_branch * 2, 30),
            birth_place="Beijing", latitude=39.9042, longitude=116.4074,
            timezone_id="Asia/Shanghai",
        ),
        sex=sex, profile=ziwei_chart_engine_v1_profile(registry),
    )
    typed = ZiweiChartFoundation(TimeCalendarFoundation(registry)).resolve_typed(request)
    if typed.status != "RESOLVED" or len(typed.candidates) != 1:
        raise AssertionError(f"unexpected sample resolution: {typed.status}")
    candidate = typed.candidates[0]
    r1 = ZiweiStructuralRuntime().generate_from_candidate(candidate, ziwei_structural_v2_r1_profile())
    r2 = ZiweiRelativePalaceFrameRuntime().generate_from_candidate(candidate, r1, ziwei_structural_v2_r2_profile())
    r3 = ZiweiBorrowProjectionRuntime().generate_from_candidate(candidate, r1, r2, ziwei_structural_v2_r3_profile())
    r4 = ZiweiNamedStructuralSemanticRuntime().generate(r2, ziwei_structural_v2_r4_profile())
    return r3, r4


def check_composition(r3, r4):
    """Compare the join with independent coordinate and reference expectations."""
    before = (json_value(r3), json_value(r4))
    state = ZiweiResolvedStructuralRuntime().generate(r3, r4, ziwei_structural_v2_r5_profile())
    assert len(state.frames) == 12
    r3_index = {(m.evaluation_origin_designation_id, m.member_offset): m for m in r3.member_facts}
    r4_index = {f.origin_designation_id: f for f in r4.sanfang_sizheng_frames}
    statuses = Counter()
    for frame in state.frames:
        semantic = r4_index[frame.origin_designation_id]
        assert frame.trine_group_key == semantic.trine_group_key
        assert frame.opposition_axis_key == semantic.opposition_axis_key
        assert [(m.member_offset, m.semantic_role) for m in frame.members] == [
            (0, "SELF"), (4, "TRINE_PLUS_4"), (6, "OPPOSITION"), (8, "TRINE_PLUS_8"),
        ]
        for member in frame.members:
            source = r3_index[(frame.origin_designation_id, member.member_offset)]
            assert member.target_raw_address.index == (frame.origin_address.index + member.member_offset) % 12
            assert member.target_designation_id == source.target_designation_id
            assert member.target_raw_address == source.target_raw_address
            assert member.structure_physical_key == source.structure_physical_key
            assert member.closure_status == source.closure_status
            assert member.borrowed_from_raw_address == source.borrowed_from_raw_address
            assert member.r3_member_key == f"R3_MEMBER:{frame.origin_designation_id}:{member.member_offset}"
            expected_source = {
                "DIRECT_PHYSICAL": member.target_raw_address,
                "BORROWED_DIRECT": member.borrowed_from_raw_address,
                "BORROW_SOURCE_EMPTY_OR_UNKNOWN": None,
            }[source.closure_status]
            assert member.physical_source_address == expected_source
            statuses[source.closure_status] += 1
    rendered = json_value(state)
    assert "projected_placements" not in json.dumps(rendered)
    assert "projected_transformations" not in json.dumps(rendered)
    assert before == (json_value(r3), json_value(r4))
    assert state.integrity.status == "PASS"
    return statuses, state


class ZiweiStructuralR5CompositionAuditR1Tests(unittest.TestCase):
    def test_season_hour_sex_samples_preserve_coordinates_and_two_identity_domains(self):
        counts = Counter()
        for month in range(1, 13):
            for sex in (Sex.MALE, Sex.FEMALE):
                with self.subTest(month=month, sex=sex):
                    statuses, _ = check_composition(*build_states(month, month - 1, sex))
                    counts.update(statuses)
        self.assertEqual(24 * 48, sum(counts.values()))
        self.assertGreater(counts["DIRECT_PHYSICAL"], 0)
        self.assertGreater(counts["BORROWED_DIRECT"], 0)

    def test_unresolved_borrow_reference_remains_null_without_second_borrow(self):
        # Composer-unit fixture only: not a valid independently generated natal chart.
        r3, r4 = build_states(5, 7, Sex.MALE)
        original = r3.member_facts[0]
        unresolved = replace(original, closure_status="BORROW_SOURCE_EMPTY_OR_UNKNOWN",
                             borrowed_from_raw_address=None, projected_placements=(),
                             projected_transformations=())
        frames = ResolvedStructuralComposer().compose(
            replace(r3, member_facts=(unresolved, *r3.member_facts[1:])), r4,
        )
        member = frames[0].members[0]
        self.assertEqual("BORROW_SOURCE_EMPTY_OR_UNKNOWN", member.closure_status)
        self.assertIsNone(member.physical_source_address)
        self.assertIsNone(member.borrowed_from_raw_address)
        self.assertEqual(original.structure_physical_key, member.structure_physical_key)

    def test_composition_audit_does_not_certify_unreviewed_r4_history(self):
        matrix = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text())
        row = next(r for r in matrix["rows"] if r["rule_id"] == "HPA-STRUCT-005")
        self.assertEqual("MODERN_COMPATIBILITY_ONLY", row["audit_status"])
        self.assertFalse(row["component_firewall"]["r4_historical_authority_certified_by_composition"])
        self.assertFalse(row["component_firewall"]["new_independent_evidence_cause"])
        self.assertFalse(row["algorithm_reopen_authorized"])


if __name__ == "__main__":
    unittest.main()
