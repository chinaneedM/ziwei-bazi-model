import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-naj-d17-d18-canvas-seam-13cc.py"
spec=importlib.util.spec_from_file_location("naj13cc",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Naj13CC(unittest.TestCase):
 def setUp(self):self.e=m.load(m.E);self.s=m.load(m.S);self.l=m.load(m.L)
 def go(self,e=None,s=None,l=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l)
 def test_positive(self):self.assertTrue(self.go())
 def test_original_day_header_forgery(self):
  e=copy.deepcopy(self.e);e["original_rois"][0]["reading"]="十八日"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_original_numeric_roi_mutated(self):
  e=copy.deepcopy(self.e);e["original_rois"][1]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_same_day_long(self):
  e=copy.deepcopy(self.e);e["firstparty_comparison"]["ten_thousandths_int"]["long_D17"]=4296073
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_global_shift(self):
  e=copy.deepcopy(self.e);e["firstparty_comparison"]["proves_whole_table_day_shift"]=True
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_fabricated_D16_C(self):
  e=copy.deepcopy(self.e);e["firstparty_comparison"]["independent_original_printed_D16_cumulative_value"]="7570.6624"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_copy_vote(self):
  e=copy.deepcopy(self.e);e["scope_firewall"]["new_independent_stemmatic_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_future_batch_retains_13cc(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="1.999.0";s["historical_audit"]["current_focus"].append("13CD later")
  l["binding"]["reviewed_state_version"]="1.999.0";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  self.assertTrue(self.go(s=s,l=l))
if __name__=="__main__":unittest.main()
