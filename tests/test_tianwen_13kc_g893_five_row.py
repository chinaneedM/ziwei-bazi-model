"""13KC provenance, five-row arithmetic and negative scope gates."""
import importlib.util
import json
import copy
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"scripts/verify-tianwen-13kc-g893-five-row.py"
spec=importlib.util.spec_from_file_location("research13kc",PATH)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestFiveRow(unittest.TestCase):
    def setUp(self):
        self.e=json.loads((ROOT/mod.EVIDENCE).read_text(encoding="utf-8"))

    def test_exact_same_copy_windows(self):
        self.assertEqual(mod.verify(self.e)["same_copy_rows"],15)

    def test_no_silent_received_copy_substitution(self):
        bad=copy.deepcopy(self.e)
        bad["five_row_same_copy_windows"][0]["same_copy_display_magnitude"][2]="10.5601775"
        with self.assertRaisesRegex(ValueError,"borrowed mixed-witness"):
            mod.verify(bad)

    def test_no_historical_winner_from_smoothness(self):
        bad=copy.deepcopy(self.e)
        bad["boundaries"]["cross_witness_numeric_winners"]=1
        with self.assertRaisesRegex(ValueError,"historical winner"):
            mod.verify(bad)

    def test_source_bound_image_and_box(self):
        bad=copy.deepcopy(self.e)
        bad["perimeter_original_rows"][0]["heading_rect_px"]=[0,0,2,3]
        with self.assertRaises(ValueError):
            mod.verify(bad)

    def test_no_fake_036b_l130(self):
        bad=copy.deepcopy(self.e)
        bad["perimeter_original_rows"][4]["page_id"]="036b"
        with self.assertRaisesRegex(ValueError,"original glyph/value"):
            mod.verify(bad)

    def test_unit_date_not_awarded(self):
        for field in ("unit_equivalence_to_ming_or_goryeosa","exact_impression_year"):
            bad=copy.deepcopy(self.e)
            bad["boundaries"][field]="confirmed"
            with self.assertRaisesRegex(ValueError,"units/date"):
                mod.verify(bad)


if __name__=="__main__":
    unittest.main()
