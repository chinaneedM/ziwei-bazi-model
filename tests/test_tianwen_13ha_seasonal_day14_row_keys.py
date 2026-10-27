import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("ha",ROOT/"scripts/verify-tianwen-13ha-seasonal-day14-row-keys.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SeasonFirewalls(unittest.TestCase):
 def setUp(self):self.e=json.loads(m.E.read_text(encoding="utf8"))
 def test_source_scoped_two_tables(self):self.assertTrue(m.check(self.e))
 def test_winter_day14_swapped_into_summer(self):
  self.e["seasonal_tables"][1]["day14"]["first_field"]="五分一九九〇"
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_summer_day14_swapped_into_winter(self):
  self.e["seasonal_tables"][0]["day14"]["first_field"]="四分六六三〇"
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_missing_season_key_rejected(self):
  self.e["normalized_selector"]["key_fields"].remove("seasonal_heading")
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_received_not_original(self):
  self.e["original_evidence_firewall"]["NCL_p74_source_original_D14_complete_field"]="四分六六三〇"
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_source_sha_cannot_change(self):
  self.e["source_snapshots"][0]["git_blob_sha"]="0"*40
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_artifact_reused_not_new_witness(self):
  self.e["original_evidence_firewall"]["physical_copies_added"]=1
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_modern_gallery_index4_not_already_collated(self):
  self.e["first_party_received"]["gallery_index4_d14_original_glyph_review_done"]=True
  with self.assertRaises(AssertionError):m.check(self.e)
if __name__=="__main__":unittest.main()
