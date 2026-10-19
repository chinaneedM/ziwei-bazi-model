import importlib.util,copy,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"acquire-waseda-goryeosa-0033-13w.py"
s=importlib.util.spec_from_file_location("w13",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class WasedaWork52Book0033(unittest.TestCase):
 def test_direct_book34_positive_control(self):m.validate(m.load())
 def test_group33_work52_not_prematurely_promoted(self):
  d=copy.deepcopy(m.load());d["candidate_book_0033"]["internal_work52_verified"]=True
  with self.assertRaises(AssertionError):m.validate(d)
 def test_book34_not_assumed_work52(self):
  d=copy.deepcopy(m.load());d["original_book_0034"]["volume52_target_present"]=True
  with self.assertRaises(AssertionError):m.validate(d)
 def test_no_automatic_independent_glyph_vote(self):
  d=copy.deepcopy(m.load());d["safety"]["independent_source_numeric_votes_added"]=1
  with self.assertRaises(AssertionError):m.validate(d)
if __name__=="__main__":unittest.main()
