import copy,unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"acquire-waseda-goryeosa-0034-13v.py"
spec=importlib.util.spec_from_file_location("src13v",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SampleAtlas13V(unittest.TestCase):
 def test_route_immutable(self):m.check_static(m.evidence())
 def test_cannot_assume_group34_work52(self):
  a=copy.deepcopy(m.evidence());a["book34_candidate"]["book_contains_work52"]=True
  with self.assertRaises(AssertionError):m.check_static(a)
 def test_cannot_recast_creation_1451_as_imprint(self):
  a=copy.deepcopy(m.evidence());a["book34_candidate"]["impression_year"]=1451
  with self.assertRaises(AssertionError):m.check_static(a)
 def test_no_extra_original_numeric_witness(self):
  a=copy.deepcopy(m.evidence());a["safety"]["numeric_glyph_votes_added"]=1
  with self.assertRaises(AssertionError):m.check_static(a)
if __name__=="__main__":unittest.main()
