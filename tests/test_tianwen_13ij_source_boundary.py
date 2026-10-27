import copy,importlib.util,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("ver13ij",root/"scripts/verify-tianwen-13ij-source-boundary.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class Boundaries(unittest.TestCase):
 def test_real_images(self):self.assertTrue(m.check(m.read()))
 def test_no_unproven_loss(self):
  for field,val in (("original_physical_leaf_loss_proven",True),("number_of_physically_missing_leaves",6),("own_table_title_obtained",True)):
   obj=copy.deepcopy(m.read());obj["adjudication"][field]=val
   with self.assertRaises(AssertionError):m.check(obj,False)
 def test_no_fake_pdf(self):
  obj=copy.deepcopy(m.read());obj["article_probe"]["original_target_page_seen"]=True
  with self.assertRaises(AssertionError):m.check(obj,False)
if __name__=="__main__":unittest.main()
