import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-solar-folio-boundaries-13eg.py"
spec=importlib.util.spec_from_file_location("v13eg",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13EG(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.E);cls.s=m.read(m.S);cls.l=m.read(m.L);cls.dz=m.read(m.DZ);cls.ef=m.read(m.EF);cls.ee=m.read(m.EE)
 def go(self,e=None,l=None):return m.check(self.e if e is None else e,self.s,self.l if l is None else l,self.dz,self.ef,self.ee)
 def reject(self,edit):
  e=copy.deepcopy(self.e);edit(e)
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_metadata(self):self.assertTrue(self.go())
 def test_reject_fake_day_jump(self):self.reject(lambda e:e["boundary_pairs"][0].update(to_day=5))
 def test_reject_folio_order(self):self.reject(lambda e:e["pages"][2].update(pdf_page=76))
 def test_reject_changed_heading(self):self.reject(lambda e:e["pages"][3]["boundaries"][1].update(source_literal="三十五日"))
 def test_reject_wrong_cropped_sha(self):self.reject(lambda e:e["pages"][1]["boundaries"][0].update(roi_rgb_sha256="0"*64))
 def test_reject_new_global_day_law(self):self.reject(lambda e:e["conclusion"].update(source_local_any_global_day_offset_rule="PROVEN"))
 def test_reject_full_day_transcription_claim(self):self.reject(lambda e:e["conclusion"].update(all_intermediate_day_headings_exhaustively_read=True))
 def test_reject_fabricated_d30_decimal(self):self.reject(lambda e:e["conclusion"].update(d30_exact_numeric="0.965038"))
 def test_reject_fabricated_independent_copy(self):self.reject(lambda e:e["impact"].update(new_independent_physical_witnesses=1))
 def test_reject_stale_action(self):
  l=copy.deepcopy(self.l);q=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005");q["next_action"]=next(h for h in q["history"] if h.get("revision_id")=="TW-OPEN-0005-13EG-FIVE-FOLIO-BOUNDARY-CONTINUITY-20261023")["previous_next_action"]
  with self.assertRaises(AssertionError):self.go(l=l)
 def test_reject_missing_current_evidence(self):
  l=copy.deepcopy(self.l);q=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005");q["history"][-1]["evidence_refs"]=[]
  with self.assertRaises(AssertionError):self.go(l=l)
if __name__=="__main__":unittest.main()
