import copy,importlib.util,unittest
from pathlib import Path
path=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13ks-mingshi-v35-rounding.py"
spec=importlib.util.spec_from_file_location("tw13ks",path)
v=importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
class ReceivedThreeConstantReplay(unittest.TestCase):
    def setUp(self):
        self.values=copy.deepcopy(list(v.read()))
    def fails(self):
        with self.assertRaises(ValueError):
            v.verify(*self.values)
    def test_valid(self):
        self.assertEqual(v.verify(*self.values)["verified_received_constants"],3)
    def test_wrong_transcribed_mid_turn(self):
        self.values[0]["controls"][0]["source_value"]="168.01585366"
        self.fails()
    def test_wrong_solar_half_input(self):
        self.values[0]["controls"][0]["input_base_units"]="137772"
        self.fails()
    def test_wrong_new_moon_result(self):
        self.values[0]["controls"][1]["source_value"]="24.1071145"
        self.fails()
    def test_wrong_quarter_phase_result(self):
        self.values[0]["controls"][2]["source_value"]="90.06830866"
        self.fails()
    def test_fake_original_folio(self):
        self.values[0]["source"]["dated_original_folio_image_checked_this_batch"]=True
        self.fails()
    def test_fake_historical_index(self):
        self.values[0]["adjudication"]["source_specific_index_base_selected"]=True
        self.fails()
    def test_false_lineage(self):
        self.values[0]["transmission_impact"]["edges_supported"].append("DIRECT_COPIED")
        self.fails()
    def test_false_six_winners(self):
        self.values[0]["adjudication"]["original_g893_six_numeric_winners"]=6
        self.fails()
    def test_missing_source_ref(self):
        self.values[2]["issues"][4]["source_refs"].remove("docs/research/TIANWEN-13KS-MINGSHI-V35-ROUNDED-LIMIT-THREE-CONSTANT-REPLAY-R1.json")
        self.fails()
if __name__=="__main__":
    unittest.main()
