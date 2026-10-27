import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13fh-book-distinctness.py"
s=importlib.util.spec_from_file_location("v13fh",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test13FH(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.x=v.get(v.P);cls.s=v.get(v.S);cls.l=v.get(v.L)
 def test_pass(self):self.assertTrue(v.check(self.x,self.s,self.l))
 def deny(self,fn):
  c=copy.deepcopy(self.x);fn(c)
  with self.assertRaises(AssertionError):v.check(c,self.s,self.l)
 def test_false_book_mapping(self):self.deny(lambda x:x["first_party_target_catalog"].update(exact_physical_book_containing_work_juan_52=20))
 def test_false_impression_year(self):self.deny(lambda x:x["first_party_target_catalog"].update(edition_impression_year=1451))
 def test_wrong_same_physical_book(self):self.deny(lambda x:x["distinct_independent_comparator"].update(this_is_SNU_GK05553_00=True))
 def test_false_runner_html(self):self.deny(lambda x:x["exact_actions_13fh_access_snapshot"].update(source_http=200))
 def test_fake_ancient_copy_cert(self):self.deny(lambda x:x["previous_13fg_snapshot_scope_reinterpretation"].update(distinct_physically_authenticated_book_leaf_bindings_observed=1))
 def test_fake_historic_D5(self):self.deny(lambda x:x["previous_13fg_snapshot_scope_reinterpretation"].update(day5_historical_numeric_value=5.5172))
 def test_fake_algorithm_reopen(self):self.deny(lambda x:x["no_reopen"].update(algorithm_reopens=1))
if __name__=="__main__":unittest.main()
