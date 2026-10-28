import copy,importlib.util,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13iz-snu-firstparty-reel-boundary.py"
spec=importlib.util.spec_from_file_location("v13iz",P);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
class FirstpartyVolList(unittest.TestCase):
 def setUp(self):self.e=M.get(M.E)
 def deny(self):
  with self.assertRaises(AssertionError):M.check(self.e)
 def test_snapshot(self):self.assertTrue(M.check(self.e))
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
