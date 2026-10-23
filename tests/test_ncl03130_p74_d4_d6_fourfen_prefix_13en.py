import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-p74-d4-d6-fourfen-prefix-13en.py"
spec=importlib.util.spec_from_file_location("v13en",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13EN(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.E);cls.el=m.read(m.EL);cls.em=m.read(m.EM);cls.ei=m.read(m.EI);cls.ed=m.read(m.ED);cls.s=m.read(m.S);cls.l=m.read(m.L)
 def go(self,e=None):return m.check(self.e if e is None else e,self.el,self.em,self.ei,self.ed,self.s,self.l)
 def reject(self,f):
  e=copy.deepcopy(self.e);f(e)
  with self.assertRaises(AssertionError):self.go(e)
 def test_source_and_handoff(self):self.assertTrue(self.go())
 def test_reject_fake_d6_prefix(self):self.reject(lambda x:x["findings"].update(fourfen_d6_clear_prefix="四分五三三五"))
 def test_reject_forged_pixel_hash(self):self.reject(lambda x:x["rois"][0].update(rgb_sha256="0"*64))
 def test_reject_full_literal_inference(self):self.reject(lambda x:x["findings"].update(fourfen_prefix_is_complete_column=[True,True,True]))
 def test_reject_forged_decimal(self):self.reject(lambda x:x["findings"].update(d4_d5_d6_fourfen_exact_decimals=["0.501",None,None]))
 def test_reject_independent_copy(self):self.reject(lambda x:x["source"].update(independent_original_witnesses_added=1))
 def test_reject_p73_heading_bridge(self):self.reject(lambda x:x["findings"].update(p73_technical_heading_lane_assignment="PROVEN"))
 def test_reject_d30_emendation(self):self.reject(lambda x:x["findings"].update(day30_missing_character_proved=True))
if __name__=="__main__": unittest.main()
