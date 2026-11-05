"""Replay two-season G893 printed precision without assuming an ancient rounding rule."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/research/TIANWEN-13RS-G893-ORIGINAL-TWO-SEASON-SOLAR-DEGREE-PRECISION-R1.json"
FINDING = ROOT / "docs/research/TIANWEN-13SB-G893-TWO-SEASON-SHORT-INCREMENT-PRECISION-GATE-R1.json"
LANES = {
    "winter": (5108569, 49386, 18600, 18625, 1),
    "summer": (4848473, 44362, 16200, 16225, -1),
}

def four_place_increment(micro_units, mode):
    if mode == "FLOOR":
        return micro_units // 100
    if mode == "HALF_UP":
        return (micro_units + 50) // 100
    raise ValueError(mode)

def replay_quantized(season, day, daily_micro_increment, mode):
    base_m, base_s, _, _, sign = LANES[season]
    m, s = base_m, base_s
    for _ in range(day):
        m -= s
        s += four_place_increment(daily_micro_increment, mode)
    j = 1_000_000 + sign * (m // 100)
    return m, j

def exact_carry_terminal_half_up(season, day, daily_micro_increment):
    base_m, base_s, _, _, _ = LANES[season]
    micro = 100 * base_m - day * 100 * base_s - (day * (day - 1) // 2) * daily_micro_increment
    return (micro + 50) // 100

class G893TwoSeasonPrecisionGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.finding = json.loads(FINDING.read_text(encoding="utf-8"))

    def test_28_physical_original_pairs_match_all_quantized_hypotheses(self):
        rows = self.source["paired_rows"]
        self.assertEqual(len(rows), 28)
        self.assertEqual([sum(r["season"] == s for r in rows) for s in LANES], [11, 17])
        for row in rows:
            m_read = int(row["original_M_fen"].replace(".", ""))
            j_read = int(row["original_J_degree"].replace(".", ""))
            _, _, printed_delta, hypothetical_quarter, _ = LANES[row["season"]]
            for mode in ("FLOOR", "HALF_UP"):
                for delta in (printed_delta, hypothetical_quarter):
                    with self.subTest(season=row["season"], day=row["day"], mode=mode, delta=delta):
                        self.assertEqual(
                            replay_quantized(row["season"], row["day"], delta, mode),
                            (m_read, j_read),
                        )

    def test_unquantized_quarter_terminal_mismatch_is_conditional(self):
        checks = [
            ("winter", 15, 4348249, 4348223),
            ("winter", 88, 50593, 49636),
            ("summer", 4, 4670053, 4670052),
            ("summer", 93, 29771, 28702),
        ]
        for season, day, source_m, unquantized_m in checks:
            _, _, _, hypothesis, _ = LANES[season]
            with self.subTest(season=season, day=day):
                self.assertEqual(replay_quantized(season, day, hypothesis, "FLOOR")[0], source_m)
                self.assertEqual(exact_carry_terminal_half_up(season, day, hypothesis), unquantized_m)
                self.assertNotEqual(source_m, unquantized_m)

    def test_research_firewall(self):
        self.assertEqual(
            self.finding["source_grade"], "PREVIOUSLY_AUTHENTICATED_ORIGINAL_13RS_NO_NEW_IMAGE"
        )
        self.assertEqual(self.finding["historical_g893_six_final_winners"], 0)
        self.assertFalse(self.finding["ancient_unit_or_rounding_instruction_proven"])
        self.assertEqual(self.finding["new_original_source_count"], 0)
        self.assertEqual(self.finding["algorithm_reopens"], 0)
        self.assertEqual(self.finding["verification"]["source_rows"], 28)

if __name__ == "__main__":
    unittest.main()
