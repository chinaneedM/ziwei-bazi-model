import copy,importlib.util,unittest
from pathlib import Path
q=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-solar-d28-d29-original-13ea.py"
spec=importlib.util.spec_from_file_location("e13ea",q);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SourceOriginal13EA(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L);cls.w=m.load(m.W);cls.n=m.load(m.N);cls.p=m.load(m.P1909)
 def go(self,e=None,l=None,s=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.w,self.n,self.p)
 def bad(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_positive(self):self.assertTrue(self.go())
 def test_wrong_d28_original_glyph(self):self.bad(lambda e:e["original_source_rows"][0].update(original_literal="初度九十九四五四九"))
 def test_wrong_d29_original_glyph(self):self.bad(lambda e:e["original_source_rows"][1].update(source_value="0.964549"))
 def test_wrong_source_original_pixel(self):self.bad(lambda e:e["original_source_rows"][1].update(field_rgb_sha256="0"*64))
 def test_wrong_day_heading_pixel(self):self.bad(lambda e:e["original_source_rows"][0].update(day_heading_rgb_sha256="0"*64))
 def test_fake_folio(self):self.bad(lambda e:e["capture"].update(source_page=86))
 def test_fake_stemmatic_vote(self):self.bad(lambda e:e["scope"].update(new_stemmatic_independence_votes=1))
 def test_false_full_solar_reindexing(self):self.bad(lambda e:e["comparison"].update(global_solar_date_reindexing_proven=True))
 def test_false_earlier_candidate_original(self):self.bad(lambda e:e["comparison"].update(derived_0_964549="PROVEN_ORIGINAL"))
 def test_wrong_physical_binding(self):self.bad(lambda e:e["source"].update(physical_item_firstparty_binding="PROVEN_QING_ORIGINAL"))
 def test_future_handoff_focus_without_13ea_loss(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="FUTURE_R";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="FUTURE_R"
  s["historical_audit"]["current_focus"].append("13EB TEST NEXT")
  l["binding"].update(reviewed_state_version="FUTURE_R",latest_research_focus_prefix="13EB",source_focus_count=len(s["historical_audit"]["current_focus"]))
  l["checkpoint_log"].append({"state_version":"FUTURE_R","reviewed_issue_ids":[z["id"] for z in l["issues"]]})
  self.assertTrue(self.go(s=s,l=l))
 def test_spoof_latest_rejected(self):
  l=copy.deepcopy(self.l);l["binding"]["latest_research_focus_prefix"]="13FA"
  with self.assertRaises(AssertionError):self.go(l=l)
if __name__=="__main__":unittest.main()
