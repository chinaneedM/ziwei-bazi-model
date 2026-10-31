"""13MM received conflict and original numeric nonpromotion tests."""
import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("gate13mm",R/"scripts/verify-tianwen-13mm-goryeosa-d16-received-print-gate.py")
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class ReceivedD16(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=json.loads(v.E.read_text(encoding="utf-8"))
  cls.s=json.loads(v.S.read_text(encoding="utf-8"))
  cls.l=json.loads(v.L.read_text(encoding="utf-8"))
 def test_original_received_grade(self):
  self.assertEqual(v.check(self.e,self.s,self.l)["status"],"PASS")
 def test_silent_correction_of_received_witness_fails(self):
  e=copy.deepcopy(self.e)
  e["source_layers"]["official_korean_received"]["received_day_difference"][2]="5.2362"
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_false_G893_numeric_winner_fails(self):
  e=copy.deepcopy(self.e);e["safeguards"]["cross_original_G893_six_historical_winners"]=1
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_false_independent_physical_vote_fails(self):
  e=copy.deepcopy(self.e);e["safeguards"]["online_transcriptions_are_independent_print_votes"]=True
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_print_image_sha_tamper_fails(self):
  e=copy.deepcopy(self.e);e["source_layers"]["zhouxiang_1569_original"]["pdf_sha256"]="0"*64
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_archive_survives_forward_research(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["historical_audit"]["current_focus"].append("13MN successor source study")
  l["binding"]["source_focus_count"]+=1
  l["binding"]["latest_research_focus_prefix"]="13MN"
  self.assertEqual(v.check(self.e,s,l)["status"],"PASS")
 def test_removed_archive_fails(self):
  l=copy.deepcopy(self.l)
  l["checkpoint_log"]=[x for x in l["checkpoint_log"] if x.get("id")!="OMISSIONS-13MM-RECEIVED-D16-PRINT-GATE-20261031"]
  with self.assertRaises(AssertionError):v.check(self.e,self.s,l)
if __name__=="__main__":unittest.main()
