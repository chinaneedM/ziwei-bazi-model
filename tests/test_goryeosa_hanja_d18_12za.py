import copy, importlib.util, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-hanja-d18-12za.py"
spec=importlib.util.spec_from_file_location("tianwen12za",p)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class GoryeosaHanjaD18ForwardErratum(unittest.TestCase):
    def setUp(self):self.x=list(v.load())
    def failcase(self):
        with self.assertRaises(ValueError):v.verify(*self.x)
    def test_valid(self):self.assertEqual(v.verify(*self.x)["received_hanja_cumulative_exact"],"4/6")
    def test_no_old_source_rewrite(self):self.x[1]["modern_received_rows"][4]["cumulative"]="8424.64083";self.failcase()
    def test_new_hanja_must_keep_three(self):self.x[0]["replay"]["rows"][4]["cumulative_raw"]="八千四百二十四六四〇八";self.failcase()
    def test_not_silently_round_off(self):self.x[0]["replay"]["rows"][4]["cumulative"]="8424.6408";self.failcase()
    def test_no_invented_pdf(self):self.x[0]["qualifications"]["physical_goryeosa_original_image_acquired"]=True;self.failcase()
    def test_no_arbitrary_cause(self):self.x[0]["qualifications"]["cause_of_extra_three"]="PRINTING_ERROR_PROVED";self.failcase()
    def test_avoid_modern_copies_physical_votes(self):self.x[0]["qualifications"]["new_physical_witness_votes"]=1;self.failcase()
    def test_bad_residual(self):self.x[0]["replay"]["edges"][3]["cumulative_minus_long_residual"]="0.00000";self.failcase()
    def test_previous_claim_retracted(self):self.x[0]["replay"]["claimed_12yz_cumulative_6_of_6_exact_retracted"]=False;self.failcase()
    def test_future_focus_growth_ok(self):
        self.x[2]["historical_audit"]["current_focus"].append("12ZB future")
        self.x[3]["binding"]["source_focus_count"]+=1
        self.x[3]["binding"]["latest_research_focus_prefix"]="12ZB"
        self.assertEqual(v.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
