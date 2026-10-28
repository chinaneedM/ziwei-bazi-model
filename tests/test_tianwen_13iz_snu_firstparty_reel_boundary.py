import copy,importlib.util,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13iz-snu-firstparty-reel-boundary.py"
spec=importlib.util.spec_from_file_location("v13iz",P);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
class FirstpartyVolList(unittest.TestCase):
 def setUp(self):self.e=M.get(M.E)
 def deny(self):
  with self.assertRaises(AssertionError):M.check(self.e)
 def test_snapshot(self):self.assertTrue(M.check(self.e))
 def test_13iz_persists_as_prior_batch_not_latest(self):
  current=M.get(M.S);self.assertNotEqual(current["historical_audit"]["current_focus"][-1].split()[0],"13IZ")
  self.assertTrue(any(f.startswith("13IZ ") for f in current["historical_audit"]["current_focus"]))
  self.assertTrue(M.check(self.e))
 def test_missing_archived_focus_rejected(self):
  s=copy.deepcopy(M.get(M.S));s["historical_audit"]["current_focus"]=[x for x in s["historical_audit"]["current_focus"] if not x.startswith("13IZ ")]
  with self.assertRaises(AssertionError):M.check(self.e,state=s)
 def test_live_action_prefix_mutation_rejected(self):
  l=copy.deepcopy(M.get(M.L));issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  issue["next_action"]="13IZ CURRENT ACTION: forged older focus"
  with self.assertRaises(AssertionError):M.check(self.e,ledger=l)

 def test_fake_pdf_yes(self):self.e["official_5554"]["all_is_pdf"]="Y";self.deny()
 def test_fake_source_copy(self):self.e["official_5554"]["provider_books"]=["GK05553_00"];self.deny()
 def test_fake_raw_digest(self):self.e["official_5554"]["raw_json_sha256"]="0"*64;self.deny()
 def test_fake_32_independent_images(self):self.e["official_5554"]["all_32_volumes_printed_original_images_acquired"]=True;self.deny()
 def test_forged_original_folio(self):self.e["official_5553"]["physical_book29_folio"]="卷81";self.deny()
 def test_no_negative_snu_holding_proof(self):self.e["official_5553"]["negative_original_absence_proven"]=True;self.deny()
 def test_no_original_juan_from_17_18(self):self.e["official_5554"]["gk5554_books17_18_juan81_82_physical_titles"]={"81":17};self.deny()
 def test_no_book12_29_winner(self):self.e["prior_13iy"]["book12_29_winner"]=[8,12,26];self.deny()
 def test_no_13io_revival(self):self.e["evidence_boundary"]["previous_13IO_book29_to_juan81_83"]="CONFIRMED";self.deny()
 def test_reject_extra_ancient_votes(self):self.e["impact"]["new_ancient_numeric_winners"]=1;self.deny()
 def test_source_registry_growth_does_not_change_old_snapshot(self):self.e["impact"]["total_sources"]=765;self.deny()
if __name__=="__main__":unittest.main()
