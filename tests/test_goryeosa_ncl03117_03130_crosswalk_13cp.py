import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-ncl03117-03130-crosswalk-13cp.py"
spec=importlib.util.spec_from_file_location("tianwen13cp",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13CP(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
 def check(self,e=None,s=None,l=None):
  return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l)
 def test_positive(self):self.assertTrue(self.check())
 def test_cannot_conflate_03117_shelf(self):
  e=copy.deepcopy(self.e);e["authority"]["03117"]["title"]="高麗史"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_cannot_promote_alias_to_physical(self):
  e=copy.deepcopy(self.e);e["interpretation"]["upload_comment_source_filename_is_not_catalog_number"]="PROVEN_SAME_ITEM"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_spurious_copy_vote(self):
  e=copy.deepcopy(self.e);e["interpretation"]["physical_copy_new_votes"]=1
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_unverified_direct_glyph(self):
  e=copy.deepcopy(self.e);e["interpretation"]["third_original_D16_glyphs_added"]=1
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_future_continuity(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="1.753.0";s["historical_audit"]["current_focus"].append("13CQ future")
  l["binding"]["reviewed_state_version"]="1.753.0"
  l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  self.assertTrue(self.check(s=s,l=l))
if __name__=="__main__":unittest.main()
