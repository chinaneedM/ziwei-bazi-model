import copy, importlib.util, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-three-lane-12yz.py"
spec=importlib.util.spec_from_file_location("tianwen12yz",p)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class GoryeosaTripleColumn(unittest.TestCase):
    def setUp(self):self.x=list(v.load())
    def bad(self):
        with self.assertRaises(ValueError):v.verify(*self.x)
    def test_valid(self):self.assertEqual(v.verify(*self.x)["mismatch_day"],16)
    def test_cannot_silently_correct_modern_literal(self):self.x[0]["modern_received_rows"][2]["short_raw"]="五分二三六二";self.bad()
    def test_cannot_change_d16_number(self):self.x[0]["modern_received_rows"][2]["short"]="5.2362";self.bad()
    def test_cross_column_long_tamper(self):self.x[0]["modern_received_rows"][3]["long"]="424.3712";self.bad()
    def test_cumulative_tamper(self):self.x[0]["modern_received_rows"][4]["cumulative"]="8424.6409";self.bad()
    def test_false_original_claim(self):self.x[0]["scope_firewall"]["official_original_image_pixels_or_hash_acquired"]=True;self.bad()
    def test_false_causation(self):self.x[0]["scope_firewall"]["digital_transcription_error_cause_proven"]=True;self.bad()
    def test_false_independent_vote(self):self.x[0]["scope_firewall"]["independently_attested_new_physical_originals"]=1;self.bad()
    def test_no_close_to_six(self):self.x[0]["scope_firewall"]["G893_six_controls_fully_adjudicated"]="6/6";self.bad()
    def test_future_focus_growth(self):
        self.x[4]["historical_audit"]["current_focus"].append("12ZA future")
        self.x[3]["binding"]["source_focus_count"]+=1
        self.x[3]["binding"]["latest_research_focus_prefix"]="12ZA"
        self.assertEqual(v.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
