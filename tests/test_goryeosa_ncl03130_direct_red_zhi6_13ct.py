import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-ncl03130-direct-red-zhi6-13ct.py"
spec=importlib.util.spec_from_file_location("goryeosa13ct",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13CT(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
 def check(self,e=None,s=None,l=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l)
 def test_positive(self):self.assertTrue(self.check())
 def test_no_fabricated_zhi6(self):
  e=copy.deepcopy(self.e);e["scope_gates"]["is_genre_zhi_six_missing"]="YES"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_image_sha_stable(self):
  e=copy.deepcopy(self.e);e["primary_image"]["png_sha256"]="fake"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_automated_read_claim(self):
  e=copy.deepcopy(self.e);e["primary_image"]["ocr_used"]=True
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_extra_original_vote(self):
  e=copy.deepcopy(self.e);e["scope_gates"]["third_independent_d16_historical_votes_added"]=1
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_mapping_scope(self):
  e=copy.deepcopy(self.e);e["first_party_text_structure_crosswalk"]["genre_juan"]=52
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_old_copy_date_inference(self):
  e=copy.deepcopy(self.e);e["scope_gates"]["whether_juan52_qing_old_hand"]="CONFIRMED"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_historical_13ct_issue_revision_not_removed(self):
  l=copy.deepcopy(self.l)
  issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  issue["history"]=[x for x in issue["history"] if x.get("revision_id")!="TW-OPEN-0005-13CT-RED-ZHI6"]
  with self.assertRaises(AssertionError):self.check(l=l)
 def test_historical_13ct_checkpoint_not_removed(self):
  l=copy.deepcopy(self.l)
  l["checkpoint_log"]=[x for x in l["checkpoint_log"] if x.get("id")!="OMISSIONS-13CT-DIRECT-RED-ZHI6-20261022"]
  with self.assertRaises(AssertionError):self.check(l=l)
if __name__=="__main__":unittest.main()
