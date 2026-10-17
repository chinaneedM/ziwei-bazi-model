#!/usr/bin/env python3
import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-g893-dual-column-erratum-12yf.py"
s=importlib.util.spec_from_file_location("t12yf",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class TwoColumnErratum(unittest.TestCase):
 def setUp(self):self.p=list(m.load())
 def reject(self):
  with self.assertRaises(ValueError):m.verify(*self.p)
 def test_pass(self):self.assertEqual(m.verify(*self.p)["status"],"PASS")
 def test_removed_erratum(self):self.p[0]["prior_evidence_status"]="CONFIRMED_EIGHT_PLACE_FIELD";self.reject()
 def test_reactivate_false_second_difference(self):self.p[0]["prior_false_claims"]["historical_numeric_evidence_validity"]="CONFIRMED";self.reject()
 def test_long_column_tamper(self):self.p[0]["direct_original_readings"][2]["long_decimal"]="434.3712";self.reject()
 def test_long_roi_tamper(self):self.p[0]["native_rgb_rois"]["per_column"][2]["sha256"]="0"*64;self.reject()
 def test_overlap_columns(self):self.p[0]["native_rgb_rois"]["per_column"][1]["rect_px"][0]=660;self.reject()
 def test_wrong_recurrence(self):self.p[0]["source_scoped_replay"]["long_next_minus_long_current"][1]="4.7639";self.reject()
 def test_solar_header_unjustified(self):self.p[0]["scope_guard"]["header_to_column_unit_identity"]="CONFIRMED";self.reject()
 def test_false_independent_witness(self):self.p[0]["original_copy"]["new_independent_physical_witnesses"]=1;self.reject()
 def test_closed_issue(self):next(z for z in self.p[1]["issues"] if z["id"]=="TW-OPEN-0005")["status"]="RESOLVED_WITH_EVIDENCE";self.reject()
 def test_state_mismatch(self):self.p[2]["schema_version"]="1.618.0";self.reject()
if __name__=="__main__":unittest.main()
