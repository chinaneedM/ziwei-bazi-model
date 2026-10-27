import copy,importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("f13iu",ROOT/"scripts"/"verify-tianwen-13iu-microfilm-identity-firewall.py")
M=importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
class Tests(unittest.TestCase):
 def setUp(self): self.e=M.load()
 def test_genuine(self): self.assertTrue(M.check(self.e))
 def test_other_holding_mf_label_not_promoted(self):
  self.e["firstparty_records"]["GK05554_00"]["microfilm_list"][3]["displayed_subject"]="GK05554"
  with self.assertRaises(AssertionError): M.check(self.e)
 def test_false_own_mf_flag_rejected(self):
  self.e["firstparty_records"]["GK05554_00"]["independently_labeled_gk5554_microfilm_entry_present"]=True
  with self.assertRaises(AssertionError): M.check(self.e)
 def test_no_physical_juan81_82_promotion(self):
  self.e["firstparty_records"]["GK05554_00"]["physical_juan81_82_original_leaf_obtained"]=True
  with self.assertRaises(AssertionError): M.check(self.e)
 def test_book29_retraction_immutable(self):
  self.e["comparison"]["source_5553_volume29_to_juan81_83"]="CONFIRMED"
  with self.assertRaises(AssertionError): M.check(self.e)
 def test_heritage_catalog_date_not_copy_exact_impression(self):
  self.e["official_heritage_index"]["physical_impression_exact_year_proven"]=True
  with self.assertRaises(AssertionError): M.check(self.e)
 def test_source_original_numeric_stays_unread(self):
  self.e["active_unresolved_targets"]["NLC03130_SOLAR_D30"]=1234
  with self.assertRaises(AssertionError): M.check(self.e)
 def test_old_13it_git_identity_frozen(self):
  self.e["predecessor"]["immutable_blob_sha"]="0"*40
  with self.assertRaises(AssertionError): M.check(self.e)
 def test_not_claim_every_photo_is_other_holding(self):
  self.e["comparison"]["no_claim_that_every_shown_image_is_gk5553"]=False
  with self.assertRaises(AssertionError): M.check(self.e)
 def test_transmission_not_upgraded(self):
  self.e["transmission_impact"]["edges_supported"].append("fake")
  with self.assertRaises(AssertionError): M.check(self.e)
if __name__=="__main__": unittest.main()
