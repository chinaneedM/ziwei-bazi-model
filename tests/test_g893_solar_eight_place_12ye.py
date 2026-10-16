#!/usr/bin/env python3
import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-g893-solar-eight-place-12ye.py"
spec=importlib.util.spec_from_file_location("t12ye",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class EightPlace(unittest.TestCase):
 def setUp(self):self.args=list(m.load())
 def fails(self):
  with self.assertRaises(ValueError):m.verify(*self.args)
 def test_ok(self):self.assertEqual(m.verify(*self.args)["status"],"PASS")
 def test_glyph_tail_tamper(self):self.args[0]["readings"][0]["original_glyphs"]="五分二一七六八二四八";self.fails()
 def test_step_tamper(self):self.args[0]["arithmetic"]["delta_16_17"]="0.0186";self.fails()
 def test_second_difference_flip(self):self.args[0]["arithmetic"]["second_difference"]="0.00000186";self.fails()
 def test_same_copy_double_vote(self):self.args[0]["boundaries"]["new_physical_copies"]=1;self.fails()
 def test_unproved_unit_forced(self):self.args[0]["boundaries"]["source_header_unit_to_lane"]="PROVEN";self.fails()
 def test_source_hash_tamper(self):self.args[0]["rois"][1]["sha256"]="0"*64;self.fails()
 def test_closed_issue(self):next(x for x in self.args[1]["issues"] if x["id"]=="TW-OPEN-0005")["status"]="RESOLVED_WITH_EVIDENCE";self.fails()
 def test_state_desync(self):self.args[2]["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.617.0";self.fails()
if __name__=="__main__":unittest.main()
