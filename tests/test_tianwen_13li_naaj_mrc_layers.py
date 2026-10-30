import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13li-naaj-mrc-layers.py"
spec=importlib.util.spec_from_file_location("tw13li",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class MRCFirewall(unittest.TestCase):
 def setUp(self):self.a=copy.deepcopy(list(v.load()))
 def bad(self):
  with self.assertRaises(AssertionError):v.check(*self.a)
 def test_base(self):self.assertEqual(v.check(*self.a)["mrc_composite_sources"],2)
 def test_fake_unprocessed(self):self.a[0]["interpretation"]["decoded_jbig2_mask_is_unprocessed_camera_original"]=True;self.bad()
 def test_fake_compression_error(self):self.a[0]["interpretation"]["lossy_symbol_substitution_proven_in_these_files"]=True;self.bad()
 def test_fake_physical_plate(self):self.a[0]["interpretation"]["same_woodblocks_historically_proven"]=True;self.bad()
 def test_fake_impression_date(self):self.a[0]["interpretation"]["pdf_creation_dates_prove_ancient_printing"]=True;self.bad()
 def test_forged_mask_hash(self):self.a[0]["source_originals"][0]["layers"][1]["decoded_pixmap_sha256"]="0"*64;self.bad()
 def test_forged_crop_hash(self):self.a[0]["source_originals"][0]["target_mask_crop_gray_sha256"]="0"*64;self.bad()
 def test_forged_crop_coordinates(self):self.a[0]["source_originals"][1]["target_mask_crop_xyxy"]=[0,0,100,100];self.bad()
 def test_forged_original(self):self.a[0]["source_originals"][1]["pdf_sha256"]="0"*64;self.bad()
 def test_restore_preceding_actions(self):self.a[2]["issues"][4]["next_action"]="13LI CURRENT ACTION: nothing archived";self.bad()
 def test_forward(self):
  self.a[1]["historical_audit"]["current_focus"].append("13LJ next research")
  self.a[2]["binding"]["source_focus_count"]+=1
  self.a[2]["binding"]["latest_research_focus_prefix"]="13LJ"
  self.a[2]["issues"][4]["next_action"]="13LJ CURRENT ACTION: next\n"+self.a[2]["issues"][4]["next_action"]
  self.assertEqual(v.check(*self.a)["status"],"PASS")
if __name__=="__main__":unittest.main()
