from __future__ import annotations

import unittest

from fortune_training.bazi_chart import (
    BaziNatalState,
    BranchInstance,
    StemInstance,
    historical_relation_candidate_registry_hash,
    historical_relation_candidate_registry_payload,
    resolve_bazi_historical_relation_candidates,
)
from fortune_training.bazi_chart.hidden_stems import generate_hidden_stems
from fortune_training.bazi_chart.registries import (
    BRANCH_ELEMENTS,
    STEM_ELEMENTS,
    STEM_POLARITY,
)
from fortune_training.bazi_chart.relations import generate_raw_relations


POSITIONS = ("YEAR", "MONTH", "DAY", "HOUR")


def _chart(branches: tuple[str, ...], stems: tuple[str, ...]) -> BaziNatalState:
    if len(branches) != len(stems):
        raise ValueError("test chart branches/stems length mismatch")
    if not 1 <= len(branches) <= len(POSITIONS):
        raise ValueError("test chart must contain between one and four pillar fragments")
    positions = POSITIONS[: len(branches)]
    branch_rows = tuple(
        BranchInstance(
            instance_id=f"{position}.BRANCH",
            position=position,
            branch=branch,
            element_affiliation=BRANCH_ELEMENTS[branch],
        )
        for position, branch in zip(positions, branches, strict=True)
    )
    stem_rows = tuple(
        StemInstance(
            instance_id=f"{position}.STEM",
            position=position,
            stem=stem,
            element=STEM_ELEMENTS[stem],
            polarity=STEM_POLARITY[stem],
        )
        for position, stem in zip(positions, stems, strict=True)
    )
    hidden = generate_hidden_stems(branch_rows)
    raw = generate_raw_relations(stem_rows, branch_rows)
    return BaziNatalState(
        pillars=(),
        stems=stem_rows,
        branches=branch_rows,
        hidden_stems=hidden,
        ten_gods=(),
        exposures=(),
        affinities=(),
        raw_relations=raw,
        day_master_stem=stems[min(2, len(stems) - 1)],
        profile_id="TEST-BAZI-HISTORICAL-RELATION-CANDIDATES",
        profile_version="1.0.0",
        algorithm_versions={},
        trace=(),
    )


class BaziHistoricalRelationCandidateR1Tests(unittest.TestCase):
    def test_registry_is_hash_stable_and_never_selected(self) -> None:
        payload = historical_relation_candidate_registry_payload()
        self.assertEqual("PRESERVED_NOT_SELECTED", payload["selection_status"])
        self.assertEqual(
            historical_relation_candidate_registry_hash(),
            historical_relation_candidate_registry_hash(),
        )

    def test_four_earth_bureau_is_arity_four_and_not_raw_trine(self) -> None:
        chart = _chart(("辰", "戌", "丑", "未"), ("乙", "乙", "乙", "乙"))
        runtime = resolve_bazi_historical_relation_candidates(chart)
        rows = [row for row in runtime["candidates"] if row["relation_family"] == "FOUR_EARTH_BUREAU"]
        self.assertEqual(1, len(rows))
        self.assertEqual(4, rows[0]["arity"])
        self.assertEqual("土", rows[0]["nominal_transformation_element"])
        self.assertFalse(any(row.relation_family == "BRANCH_TRINE" for row in chart.raw_relations))

    def test_directional_triads_are_separate_from_standard_trines(self) -> None:
        chart = _chart(("寅", "卯", "辰"), ("乙", "乙", "乙"))
        runtime = resolve_bazi_historical_relation_candidates(chart)
        rows = [row for row in runtime["candidates"] if row["relation_family"] == "DIRECTIONAL_TRIAD"]
        self.assertEqual(1, len(rows))
        self.assertEqual("BRANCH.DIRECTIONAL_TRIAD.EAST.WOOD", rows[0]["semantic_relation_id"])
        self.assertFalse(any(row.relation_family == "BRANCH_TRINE" for row in chart.raw_relations))

    def test_early_break_preserves_four_pair_source_and_excludes_later_harmony_pairs(self) -> None:
        early = _chart(("卯", "午"), ("乙", "乙"))
        runtime = resolve_bazi_historical_relation_candidates(early)
        breaks = [row for row in runtime["candidates"] if row["relation_family"] == "BRANCH_BREAK_EARLY_FOUR"]
        self.assertEqual(1, len(breaks))
        self.assertEqual("BRANCH.BREAK.EARLY.MAO_WU", breaks[0]["semantic_relation_id"])

        later_pair = _chart(("寅", "亥"), ("乙", "乙"))
        later_runtime = resolve_bazi_historical_relation_candidates(later_pair)
        self.assertFalse(
            any(row["relation_family"] == "BRANCH_BREAK_EARLY_FOUR" for row in later_runtime["candidates"])
        )
        self.assertTrue(
            any(row.relation_family == "BRANCH_SIX_HARMONY" for row in later_pair.raw_relations)
        )

    def test_same_pillar_hidden_stem_combination_is_occurrence_only(self) -> None:
        chart = _chart(("午",), ("壬",))
        runtime = resolve_bazi_historical_relation_candidates(chart)
        rows = [row for row in runtime["candidates"] if row["relation_family"] == "STEM_HIDDEN_COMBINATION"]
        self.assertEqual(1, len(rows))
        self.assertEqual(
            ("YEAR.STEM", "YEAR.BRANCH.HIDDEN:丁"),
            tuple(rows[0]["participant_instance_ids"]),
        )
        self.assertEqual("木", rows[0]["nominal_transformation_element"])
        self.assertEqual("WITHIN_PILLAR", rows[0]["orientation"])
        self.assertNotIn("TRANSFORMATION_ESTABLISHED", str(rows[0]))

    def test_cross_pillar_hidden_stem_is_not_promoted_to_same_pillar_candidate(self) -> None:
        chart = _chart(("子", "午"), ("壬", "乙"))
        runtime = resolve_bazi_historical_relation_candidates(chart)
        self.assertFalse(
            any(row["relation_family"] == "STEM_HIDDEN_COMBINATION" for row in runtime["candidates"])
        )

    def test_sidecar_does_not_mutate_raw_relation_core_or_hash_by_call_order(self) -> None:
        chart = _chart(("辰", "戌", "丑", "未"), ("乙", "乙", "乙", "乙"))
        before = chart.raw_relations
        first = resolve_bazi_historical_relation_candidates(chart)
        second = resolve_bazi_historical_relation_candidates(chart)
        self.assertEqual(before, chart.raw_relations)
        self.assertEqual(first["runtime_hash"], second["runtime_hash"])
        self.assertEqual("PRESERVED_NOT_SELECTED", first["selection_status"])
        self.assertEqual(3, first["candidate_count"])
        self.assertEqual(
            {"FOUR_EARTH_BUREAU", "BRANCH_BREAK_EARLY_FOUR"},
            {row["relation_family"] for row in first["candidates"]},
        )


if __name__ == "__main__":
    unittest.main()
