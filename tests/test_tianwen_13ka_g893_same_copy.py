import copy
import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "scripts/verify-tianwen-13ka-g893-same-copy.py"
spec = importlib.util.spec_from_file_location("g893_collation", path)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class SourceEvidenceBoundaries(unittest.TestCase):
    def setUp(self):
        self.data = copy.deepcopy(v.load())

    def rejects(self):
        with self.assertRaises(ValueError):
            v.verify(self.data)

    def test_original_record_and_handoff(self):
        self.assertEqual(v.verify(self.data)["same_copy_rows"], 9)
        v.verify_handoff()

    def test_source_hash_cannot_be_substituted(self):
        self.data["pages"][1]["sha256"] = "0" * 64
        self.rejects()

    def test_received_value_cannot_replace_original(self):
        self.data["cases"][1]["rows"][1]["displayed_magnitude_decimal_candidate"] = "1.0821"
        self.rejects()

    def test_original_zero_cannot_be_dropped(self):
        self.data["cases"][2]["rows"][1]["field_literal"] = "損七分八八六七五"
        self.rejects()

    def test_incorrect_difference(self):
        self.data["cases"][0]["second_difference"] = "0"
        self.rejects()

    def test_sign_cannot_be_collapsed(self):
        self.data["cases"][2]["rows"][0]["sign_glyph"] = "益"
        self.rejects()

    def test_heading_cannot_point_to_value_lane(self):
        row = self.data["cases"][1]["rows"][1]
        row["heading_roi"] = row["value_roi"]
        self.rejects()

    def test_out_of_source_crop(self):
        self.data["regions"][0]["rect_px"][2] = 1200
        self.rejects()

    def test_string_or_bool_coordinates(self):
        for bad in ["700", True]:
            self.data = copy.deepcopy(v.load())
            self.data["regions"][0]["rect_px"][0] = bad
            self.rejects()

    def test_tiny_stripe_is_not_original_field_evidence(self):
        self.data["regions"][0]["rect_px"][2] = 701
        self.rejects()

    def test_hash_replay_cannot_promote_blank_old_roi(self):
        self.data["forward_only_roi_semantic_errata"][0]["semantic_sufficiency"] = "COMPLETE_HEADING"
        self.rejects()

    def test_historical_roi_cannot_be_rewritten(self):
        self.data["forward_only_roi_semantic_errata"][0]["prior_rect_px"][0] += 1
        self.rejects()

    def test_three_rows_are_not_five(self):
        self.data["boundaries"]["full_five_row_same_copy_comparison_completed"] = True
        self.rejects()

    def test_same_copy_is_not_new_witness(self):
        self.data["boundaries"]["new_physical_witnesses"] = 1
        self.rejects()

    def test_smooth_arithmetic_is_not_historical_winner(self):
        self.data["boundaries"]["cross_witness_numeric_winners"] = 1
        self.rejects()

    def test_other_witness_unit_not_automatically_equivalent(self):
        self.data["boundaries"]["unit_equivalence_to_ming_or_goryeosa"] = True
        self.rejects()


if __name__ == "__main__":
    unittest.main()
