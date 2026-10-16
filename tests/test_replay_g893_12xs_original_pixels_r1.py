import hashlib
import importlib.util
import unittest
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("g893source",ROOT/"scripts/replay-g893-12xs-original-pixels-r1.py")
m=importlib.util.module_from_spec(sp)
sp.loader.exec_module(m)
class G893OriginalPixelsTest(unittest.TestCase):
 def test_rgb_digest_matches_exact_bytes(self):
  im=Image.new("RGB",(32,40),(12,42,51))
  self.assertEqual(m.rgb_crop_digest(im,[2,4,28,37]),hashlib.sha256(im.crop((2,4,28,37)).tobytes()).hexdigest())
 def test_geometry_cannot_leave_original_pixels(self):
  with self.assertRaisesRegex(ValueError,"ROI beyond original image"):
   m.rgb_crop_digest(Image.new("RGB",(32,40)),[0,0,300,40])
 def test_boolean_coordinate_cannot_fake_integer(self):
  with self.assertRaisesRegex(ValueError,"invalid ROI geometry"):
   m.rgb_crop_digest(Image.new("RGB",(32,40)),[0,True,20,20])
 def test_one_pixel_change_changes_digest(self):
  a=Image.new("RGB",(20,20),(8,15,30))
  b=Image.new("RGB",(20,20),(9,15,30))
  self.assertNotEqual(m.rgb_crop_digest(a,[2,2,18,18]),m.rgb_crop_digest(b,[2,2,18,18]))
 def test_real_original_archive_not_available_in_ci_does_not_falsely_pass(self):
  with self.assertRaises((FileNotFoundError,ValueError)):
   m.replay(ROOT/"tests/FAKE-NONEXISTENT-G893-ORIGINAL-ARCHIVE.zip")
if __name__=="__main__":
 unittest.main()
