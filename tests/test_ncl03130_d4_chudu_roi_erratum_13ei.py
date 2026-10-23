import copy,importlib.util,unittest
from pathlib import Path
path=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-d4-chudu-roi-erratum-13ei.py"
spec=importlib.util.spec_from_file_location("v13ei",path);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Test13EI(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=v.read(v.E);cls.s=v.read(v.STATE);cls.l=v.read(v.LEDGER);cls.eh=v.read(v.EH);cls.eg=v.read(v.EG);cls.ed=v.read(v.ED)
 def check(self,e=None,l=None):
  return v.check(self.e if e is None else e,self.s,self.l if l is None else l,self.eh,self.eg,self.ed)
 def reject(self,edit):
  e=copy.deepcopy(self.e);edit(e)
  with self.assertRaises(AssertionError):self.check(e)
 def test_positive_erratum(self):self.assertTrue(self.check())
 def test_reject_reborn_13eh_claim(self):self.reject(lambda e:e["error"].update(adjudication="HISTORICALLY_PROVEN"))
 def test_reject_original_wrong_glyph(self):self.reject(lambda e:e["error"].update(actual_visible_opening="初度"))
 def test_reject_false_chudu_roi(self):self.reject(lambda e:next(x for x in e["rois"] if x["name"]=="p74_invalid_claimed_chudu_strip").update(rgb_sha256="0"*64))
 def test_reject_new_chudu_roi_tamper(self):self.reject(lambda e:next(x for x in e["rois"] if x["name"]=="p74_nearby_chudu_candidate_strip").update(bbox=[958,397,982,785]))
 def test_reject_old_one_pixel_concordance(self):self.reject(lambda e:e["replacement"].update(normalized_pair_geometry="PROVEN"))
 def test_reject_invented_day30_decimal(self):self.reject(lambda e:e["replacement"].update(original_p76_day30_numeric="0.965038"))
 def test_reject_fake_source_vote(self):self.reject(lambda e:e["impact"].update(independent_physical_copy_votes=1))
 def test_reject_stale_issue_action(self):
  l=copy.deepcopy(self.l);q=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
  q["next_action"]=q["history"][-1]["previous_next_action"]
  with self.assertRaises(AssertionError):self.check(l=l)
if __name__=="__main__":unittest.main()
