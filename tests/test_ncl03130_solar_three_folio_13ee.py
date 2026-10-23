import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-solar-three-folio-13ee.py"
spec=importlib.util.spec_from_file_location("t13ee",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13EE(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.E);cls.s=m.read(m.S);cls.l=m.read(m.L);cls.ed=m.read(m.ED);cls.dz=m.read(m.DZ)
 def runcheck(self,e=None,l=None):return m.check(self.e if e is None else e,self.s,self.l if l is None else l,self.ed,self.dz)
 def reject(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.runcheck(e=e)
 def test_valid_metadata(self):self.assertTrue(self.runcheck())
 def test_wrong_middle_day(self):self.reject(lambda e:e["pages"][1].update(source_printed_day=28))
 def test_wrong_glyph_day41(self):self.reject(lambda e:e["pages"][2].update(printed_heading="四十日"))
 def test_wrong_original_p75_sha(self):self.reject(lambda e:e["pages"][0].update(png_sha256="0"*64))
 def test_swapped_original_p77_roi(self):self.reject(lambda e:e["pages"][2]["rois"]["narrow_original_column"].update(rgb_sha256="0"*64))
 def test_fake_d30_value(self):self.reject(lambda e:e["observation"].update(numeric_d30="0.965038"))
 def test_false_three_independent_copies(self):self.reject(lambda e:e["impact"].update(new_independent_votes=3))
 def test_false_global_day_offset(self):self.reject(lambda e:e["observation"].update(global_day_offset="PROVEN"))
 def test_fake_full_folio(self):self.reject(lambda e:e["observation"].update(full_folio_numerical_transcription=True))
 def test_stale_action_cannot_reopen(self):
  l=copy.deepcopy(self.l);item=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005");item["next_action"]=item["history"][-1]["previous_next_action"]
  with self.assertRaises(AssertionError):self.runcheck(l=l)
if __name__=="__main__":unittest.main()
