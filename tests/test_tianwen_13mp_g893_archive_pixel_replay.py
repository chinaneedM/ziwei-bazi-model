"""13MP original archive replay scope: no fabricated source PASS when bytes absent."""
import copy,importlib.util,json,os,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("gate13mp",R/"scripts/verify-tianwen-13mp-g893-archive-pixel-replay.py")
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class OriginalArchiveGate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e,cls.p,cls.s,cls.l=[json.loads(f.read_text(encoding="utf-8")) for f in (v.E,v.P,v.S,v.L)]
 def test_metadata_does_not_claim_source_replay(self):
  got=v.check(self.e,self.p,self.s,self.l)
  self.assertEqual(got["status"],"PASS")
  self.assertEqual(got["source_image_hash_replay"],"NOT_EXECUTED_WITHOUT_ARCHIVE")
 def test_historical_nonrevision_events_are_valid(self):
  # Earlier history legitimately includes original admission/nonrevision entries.
  l=copy.deepcopy(self.l)
  issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  issue["history"].insert(0,{"event":"LEGACY_ADMISSION","date":"2026-10-15"})
  self.assertEqual(v.check(self.e,self.p,self.s,l)["status"],"PASS")
 def test_missing_specific_13mp_revision_is_rejected(self):
  l=copy.deepcopy(self.l)
  issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  issue["history"]=[x for x in issue["history"] if x.get("revision_id")!="TW-OPEN-0005-13MP-PIXEL-REPLAY-20261031"]
  with self.assertRaises(AssertionError):v.check(self.e,self.p,self.s,l)
 def test_source_sublane_tamper_rejected(self):
  e=copy.deepcopy(self.e)
  e["paired_column_transcriptions"][1]["short"]="5.1362"
  with self.assertRaises(AssertionError):v.check(e,self.p,self.s,self.l)
 def test_false_cross_source_long_identity_rejected(self):
  p=copy.deepcopy(self.p)
  p["source_field_scope"]["zhou1569_other_column_normalized_values_claimed_equal_to_g893_long"]=True
  with self.assertRaises(AssertionError):v.check(self.e,p,self.s,self.l)
 def test_false_original_historical_winner_rejected(self):
  p=copy.deepcopy(self.p);p["invariants"]["historical_cross_original_six_winners"]=1
  with self.assertRaises(AssertionError):v.check(self.e,p,self.s,self.l)
 def test_missing_13mp_focus_rejected(self):
  s=copy.deepcopy(self.s)
  s["historical_audit"]["current_focus"]=[x for x in s["historical_audit"]["current_focus"] if not x.startswith("13MP ")]
  with self.assertRaises(AssertionError):v.check(self.e,self.p,s,self.l)
 def test_next_batch_allowed(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="1.979.0"
  s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.979.0"
  s["historical_audit"]["current_focus"].append("13MQ successor")
  l["binding"]["reviewed_state_version"]="1.979.0"
  l["binding"]["latest_research_focus_prefix"]="13MQ"
  l["binding"]["source_focus_count"]+=1
  self.assertEqual(v.check(self.e,self.p,s,l)["status"],"PASS")
 def test_optional_real_archive_only_if_available(self):
  path=os.environ.get("TIANWEN_13MP_SOURCE_ARCHIVE")
  if not path:self.skipTest("Source ZIP not supplied; do not claim pixel replay in CI")
  self.assertEqual(v.replay(self.e,path)["source_image_hash_replay"],"PASS")
if __name__=="__main__":unittest.main()
