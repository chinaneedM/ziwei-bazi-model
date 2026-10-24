import copy, importlib.util, unittest
from pathlib import Path
q=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-solar-taiyin-erratum-13dx.py"
sp=importlib.util.spec_from_file_location("erratum13dx",q);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class Test13DX(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
 def test_valid(self):self.assertTrue(m.check(self.e,self.s,self.l))
 def bad(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):m.check(e,self.s,self.l)
 def test_fake_solar_d28(self):self.bad(lambda e:e["p86_source_native_limit28"].update(ordinal_type="SOLAR_XIAZHI_DAY"))
 def test_fake_solarglyph(self):self.bad(lambda e:e["adjudication"].update(solar_D28_numeric="0.994549"))
 def test_old_error_revived(self):self.bad(lambda e:e["adjudication"].update(p86_prior_solar_D28_target="UNRESOLVED"))
 def test_fake_physical_copy_vote(self):self.bad(lambda e:e["adjudication"].update(solar_D28_0_994549_physical_vote="ATTESTED"))
 def test_unproven_solar_page(self):self.bad(lambda e:e["next_page_search"].update(p76_is_confirmed_solar_D28=True))
 def test_wrong_lunar_dayrate(self):self.bad(lambda e:e["p86_source_native_limit28"].update(source_original_literal="初度九十九四五四九"))
 def test_wrong_original_sha(self):self.bad(lambda e:e["acquired_original_evidence"][5].update(source_png_sha256="0"*64))
 def test_source_mirror_promoted(self):self.bad(lambda e:e["source_object"].update(physical_copy_identity="PROVEN_QING_ORIGINAL"))

 def test_later_focus_does_not_erase_13dx_original_erratum(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="FUTURE_R"
  s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="FUTURE_R"
  s["historical_audit"]["current_focus"].append("13EA FOLLOWUP ORIGINAL FOLIO")
  l["binding"].update(reviewed_state_version="FUTURE_R",
      latest_research_focus_prefix="13EA",source_focus_count=len(s["historical_audit"]["current_focus"]))
  l["checkpoint_log"].append({"state_version":"FUTURE_R","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(m.check(self.e,s,l))
 def test_fake_future_latest_focus_rejected(self):
  l=copy.deepcopy(self.l);l["binding"]["latest_research_focus_prefix"]=l["binding"]["latest_research_focus_prefix"]+"_FORGED"
  with self.assertRaises(AssertionError):m.check(self.e,self.s,l)
 def test_13dx_history_missing_rejected(self):
  l=copy.deepcopy(self.l)
  i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  i["history"]=[x for x in i["history"] if x.get("revision_id")!="TW-OPEN-0005-13DX-SOLAR-TAIYIN-ERRATUM"]
  with self.assertRaises(AssertionError):m.check(self.e,self.s,l)
if __name__=="__main__":unittest.main()
