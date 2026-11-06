import json
from pathlib import Path
import unittest


RESEARCH = Path(__file__).resolve().parents[1] / "docs" / "research"
EVIDENCE = RESEARCH / "TIANWEN-13SG-G893-SOLAR-INTERIOR-DAILY-DIFFERENCE-PRECISION-R1.json"
PRIOR_MODEL = RESEARCH / "TIANWEN-13SD-G893-PER-DAY-M-QUANTIZATION-STAGE-FIREWALL-R1.json"


class G893InteriorDailyDifferenceTests(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.prior = json.loads(PRIOR_MODEL.read_text(encoding="utf-8"))["integer_model"]
        self.pages = self.doc["original_pages"]

    def test_short_field_discriminates_only_end_only_propagation(self):
        replay = self.doc["exact_replay"]
        matches = dict.fromkeys(replay["matches_out_of_55"], 0)
        expected_windows = {
            "winter": [(31, 41), (53, 74)],
            "summer": [(27, 37), (60, 70)],
        }
        for season, windows in expected_windows.items():
            with self.subTest(season=season):
                rows = [
                    (page["first_day"] + offset, value)
                    for page in self.pages.values()
                    if page["season"] == season
                    for offset, value in enumerate(page["S4_right_to_left"])
                ]
                self.assertEqual([day for day, _ in rows], [
                    day for start, end in windows for day in range(start, end + 1)
                ])
                model = replay["season_models"][season]
                prior = self.prior["initial_" + season]
                origin = model["day_0_S4"]
                display_step = model["displayed_step_S4"]
                hypothesis = model["hypothetical_step_microfen"]
                self.assertEqual((origin, hypothesis), (prior["S4"], prior["d_micro"]))
                self.assertEqual(len(rows), model["sample_count"])
                for day, observed in rows:
                    exact_microfen = origin * 100 + day * hypothesis
                    matches["displayed_model"] += observed == origin + day * display_step
                    for mode, offset in (("FLOOR", 0), ("HALF_UP", 50)):
                        end_only = (exact_microfen + offset) // 100
                        daily_step = (hypothesis + offset) // 100
                        matches["end_only_" + mode] += observed == end_only
                        matches["daily_S_" + mode] += observed == origin + day * daily_step

        self.assertEqual(matches, replay["matches_out_of_55"])
        self.assertEqual(list(matches.values()), [55, 0, 0, 55, 55])

    def test_whole_fen_carry_and_historical_evidence_boundary(self):
        for carry in self.doc["observed_whole_fen_carries"]:
            with self.subTest(season=carry["season"]):
                for side in ("from", "to"):
                    page = self.pages[carry[side + "_page"]]
                    value = page["S4_right_to_left"][carry[side + "_day"] - page["first_day"]]
                    self.assertEqual(value, carry[side + "_S4"])
                before, after = carry["from_S4"], carry["to_S4"]
                self.assertEqual(after // 10_000 - before // 10_000, 1)
                self.assertEqual(after - before, {"winter": 186, "summer": 162}[carry["season"]])

        scope = self.doc["adjudication"]
        self.assertEqual(scope["TW_OPEN_0005"], "OPEN")
        self.assertEqual(scope["historic_numeric_finals"], "0/6")
        self.assertEqual(scope["new_physical_witnesses"], 0)
        self.assertEqual(scope["algorithm_reopens"], 0)
