import copy, importlib.util, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13kk-shanghai-p71-seam.py"
spec=importlib.util.spec_from_file_location("tw13kk",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class ShanghaiP71Seam(unittest.TestCase):
 def setUp(self): self.data=copy.deepcopy(list(v.load()))
 def fails(self):
  with self.assertRaises(ValueError):v.verify(*self.data)
 def test_source_scoped_seam(self):self.assertEqual(v.verify(*self.data)["status"],"PASS")
 def test_roi_hash_mutation(self):self.data[0]["direct_visual_collation"]["pixel_roi_reviews"][0]["roi_rgb_sha256"]="0"*64;self.fails()
 def test_false_glyph_award(self):self.data[0]["revised_source_scope"]["huang_益加損減_original_glyph_proven"]=True;self.fails()
 def test_false_physical_edition(self):self.data[0]["source_identity"]["original_physical_copy_identity_bound"]=True;self.fails()
 def test_rename_prior_work(self):self.data[0]["direct_visual_collation"]["pixel_roi_reviews"][0]["literal"]="授時曆故卷三終";self.fails()
 def test_future_append_only(self):
  self.data[1]["historical_audit"]["current_focus"].append("13KL next")
  self.data[2]["binding"]["source_focus_count"]+=1
  self.data[2]["binding"]["latest_research_focus_prefix"]="13KL"
  self.assertEqual(v.verify(*self.data)["status"],"PASS")
if __name__=="__main__":unittest.main()
