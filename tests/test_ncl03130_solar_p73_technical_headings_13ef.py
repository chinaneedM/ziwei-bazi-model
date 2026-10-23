import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-solar-p73-technical-headings-13ef.py"
spec=importlib.util.spec_from_file_location("v13ef",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13EF(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.E);cls.s=m.read(m.STATE);cls.l=m.read(m.LEDGER);cls.dz=m.read(m.DZ);cls.ee=m.read(m.EE)
 def go(self,e=None,l=None):return m.check(self.e if e is None else e,self.s,self.l if l is None else l,self.dz,self.ee)
 def bad(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_real_original_metadata(self):self.assertTrue(self.go())
 def test_wrong_original_page_sha(self):self.bad(lambda e:e["source"]["original_page"].update(png_sha256="0"*64))
 def test_wrong_solar_title(self):self.bad(lambda e:e["positive_source_facts"].update(full_table_title="太陰夏至"))
 def test_wrong_xingdu_glyph(self):self.bad(lambda e:e["original_rois"][2].update(original_literal="星度"))
 def test_yingsuoji_roi_integrity(self):self.bad(lambda e:e["original_rois"][3].update(rgb_sha256="0"*64))
 def test_unproved_cross_page_numeric_relation(self):self.bad(lambda e:e["limits"].update(source_p73_day0_to_p75_p77_numeric_rule="PROVEN"))
 def test_fake_d30_numeric(self):self.bad(lambda e:e["limits"].update(original_d30_exact_numeric="0.965038"))
 def test_fake_stemmatic_votes(self):self.bad(lambda e:e["impact"].update(new_stemmatic_independent_votes=1))
 def test_stale_13ee_task_cannot_resurrect(self):
  l=copy.deepcopy(self.l);z=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  z["next_action"]=z["history"][-1]["previous_next_action"]
  with self.assertRaises(AssertionError):self.go(l=l)
 def test_missing_evidence_links_rejected(self):
  l=copy.deepcopy(self.l);l["issues"][4]["history"][-1]["evidence_refs"]=[]
  with self.assertRaises(AssertionError):self.go(l=l)
if __name__=="__main__":unittest.main()
