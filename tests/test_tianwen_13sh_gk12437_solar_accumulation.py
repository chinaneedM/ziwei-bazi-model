from decimal import Decimal
import json
from pathlib import Path
import unittest


RESEARCH = Path(__file__).resolve().parents[1] / "docs" / "research"
EVIDENCE = RESEARCH / "TIANWEN-13SH-GK12437-G893-SOLAR-ACCUMULATION-TERMINAL-COLLATION-R1.json"
PRIOR_ENDS = RESEARCH / "TIANWEN-13SF-G893-SOLAR-ENDPOINT-SHORT-LANE-AND-GORYEOSA-PRINT-VARIANTS-R1.json"


class GK12437SolarAccumulationTests(unittest.TestCase):
    def test_cross_copy_matches_and_full_ordinary_terminal_addend(self):
        doc = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        prior = json.loads(PRIOR_ENDS.read_text(encoding="utf-8"))
        g893_ends = {
            row["season"]: row for row in prior["original_rows"] if row["copy"] == "G893"
        }
        matched_m = matched_c = 0
        for season in ("winter", "summer"):
            with self.subTest(season=season):
                start = doc["season_start"][season]
                end = doc["season_end"][season]
                self.assertEqual(start["GK12437"]["M4"], start["G893"]["M4"])
                self.assertEqual(start["GK12437"]["C4"], start["G893"]["C4"])
                for witness in ("GK12437", "G893"):
                    m4, c4 = start[witness]["M4"], start[witness]["C4"]
                    self.assertEqual(c4, [None, m4[0], m4[0] + m4[1]])
                    regular, terminal = end[witness]["ordinary"], end[witness]["terminal"]
                    delta = terminal["C4"] - regular["C4"]
                    self.assertEqual(delta, regular["M4"])
                    self.assertEqual(
                        Decimal(delta) / 10_000,
                        Decimal(doc["adjudication"][season + "_terminal_delta_fen"]),
                    )
                self.assertEqual(end["GK12437"]["ordinary"], end["G893"]["ordinary"])
                self.assertEqual(end["GK12437"]["terminal"]["C4"], end["G893"]["terminal"]["C4"])
                self.assertEqual(end["G893"]["terminal"]["C4"], g893_ends[season]["terminal"]["C4"])
                self.assertNotEqual(
                    end["GK12437"]["terminal"]["header_literal"],
                    end["G893"]["terminal"]["header_literal"],
                )
                matched_m += len(start["G893"]["M4"]) + 1
                matched_c += sum(value is not None for value in start["G893"]["C4"]) + 2
        self.assertEqual((matched_m, matched_c), (8, 8))

    def test_field_inventory_and_terminal_inscription_are_scoped(self):
        doc = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        headers = doc["headers"]["GK12437"]
        self.assertEqual(headers["winter"]["data_fields"], ["盈縮加分", "盈縮積度"])
        self.assertEqual(headers["summer"]["data_fields"], ["盈縮加分", "盈縮積"])
        terminal = doc["season_end"]["summer"]["GK12437"]["terminal"]
        self.assertEqual(terminal["header_literal"], "九十四日")
        self.assertEqual(terminal["M_position_literal"], "五七十一分")
        self.assertIsNone(terminal["M_position_numeric"])
        self.assertEqual(doc["adjudication"]["historic_numeric_finals"], "0/6")
        self.assertEqual(doc["adjudication"]["TW_OPEN_0005"], "OPEN")
