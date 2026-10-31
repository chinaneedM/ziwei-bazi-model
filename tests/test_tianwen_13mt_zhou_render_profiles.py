"""13MT exact source render fingerprint constants and incompatible versions."""
import importlib.util,unittest
from pathlib import Path
r=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("v13mt",r/"scripts/replay-tianwen-13mt-zhou-render-profiles.py")
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class Profiles(unittest.TestCase):
 def test_same_source_two_different_render_pixel_hashes(self):
  self.assertNotEqual(v.RECORDS["1.26.7"]["full"],v.RECORDS["1.28.2"]["full"])
  self.assertNotEqual(v.RECORDS["1.26.7"]["roi"],v.RECORDS["1.28.2"]["roi"])
 def test_both_use_same_crop_geometry(self):
  self.assertEqual(v.BOX,(1295,70,1353,1370))
  self.assertEqual(len(v.SHA),64)
if __name__=="__main__":unittest.main()
