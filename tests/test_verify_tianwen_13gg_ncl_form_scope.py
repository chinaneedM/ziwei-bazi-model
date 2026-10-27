import copy, importlib.util, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("v13gg",R/"scripts/verify-tianwen-13gg-ncl-form-scope.py")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class Test13GG(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L);cls.gf=m.load(m.GF)
 def check(self,e):return m.check(e,self.s,self.l,self.gf)
 def reject(self,edit):
  e=copy.deepcopy(self.e);edit(e)
  with self.assertRaises(AssertionError):self.check(e)
 def test_positive(self):self.assertTrue(self.check(self.e))
 def test_no_remote_order_inferred(self):self.reject(lambda x:x["request_channel"].update(remote_digital_copy_form_confirmed=True))
 def test_no_submission(self):self.reject(lambda x:x["request_channel"].update(request_submitted=True))
 def test_no_approval(self):self.reject(lambda x:x["request_channel"].update(target_approved=True))
 def test_no_unread_glyph(self):self.reject(lambda x:x["historical_boundaries"].update(old_copy_day30="四分九二二二"))
 def test_no_old_scan_upgraded(self):self.reject(lambda x:x["original_replay"]["p74"].update(sha256="fabricated"))
 def test_no_historical_award(self):self.reject(lambda x:x["counts"].update(new_historical_physical_witnesses=1))
if __name__=="__main__":unittest.main()
