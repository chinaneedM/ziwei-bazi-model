import importlib.util, unittest
from copy import deepcopy
from pathlib import Path
S=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13jr-goryeosa-modern-holdings.py"
spec=importlib.util.spec_from_file_location("tw13jr",S)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
class TestModernGoryeosaHoldingsGate(unittest.TestCase):
 def setUp(self): self.x=list(mod.load())
 def rejects(self):
  with self.assertRaises(AssertionError):mod.verify(*self.x)
 def test_valid(self):self.assertEqual(mod.verify(*self.x)["status"],"PASS")
 def test_series_not_ancient_recension(self):
  self.x[0]["bibliographic_adjudication"]["two_asia_1972_catalog_entries_are_proven_distinct_textual_editions"]=True
  self.rejects()
 def test_preface_1983_cannot_certify_1972_impression(self):
  self.x[0]["bibliographic_adjudication"]["bb04922175_1972_9_plus_1983_2_preface_is_sufficient_to_identify_each_1972_physical_impression"]=True
  self.rejects()
 def test_unauthorized_original_claim(self):
  self.x[0]["catalogs"][0]["original_colophon_seen"]=True
  self.rejects()
 def test_gk5554_source_not_minted(self):
  self.x[0]["catalogs"][1]["ancient_gk5554_folio_bound"]=True
  self.rejects()
 def test_g893_not_closed_from_catalog(self):
  self.x[0]["bibliographic_adjudication"]["g893_six_numeric_targets_closed_this_batch"]=1
  self.rejects()
 def test_issue_remains_open(self):
  next(x for x in self.x[2]["issues"] if x["id"]=="TW-OPEN-0005")["status"]="CLOSED"
  self.rejects()
 def test_historical_13jr_revision_preserved(self):
  issue=next(x for x in self.x[2]["issues"] if x["id"]=="TW-OPEN-0005")
  issue["history"]=[rev for rev in issue["history"] if not rev.get("revision_id","").startswith("TW-OPEN-0005-13JR-")]
  self.rejects()
 def test_future_history_append_not_rejected(self):
  issue=next(x for x in self.x[2]["issues"] if x["id"]=="TW-OPEN-0005")
  issue["history"].append({"event":"ISSUE_REVISION","revision_id":"TW-OPEN-0005-13JS-FUTURE","evidence_refs":[],"changed_fields":["next_action"]})
  self.assertEqual(mod.verify(*self.x)["status"],"PASS")
 def test_future_append_only_state(self):
  self.x[1]["historical_audit"]["current_focus"].append("13JS later")
  self.x[2]["binding"]["latest_research_focus_prefix"]="13JS"
  self.x[2]["binding"]["source_focus_count"]+=1
  self.assertEqual(mod.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
