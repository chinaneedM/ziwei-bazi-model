import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13kx-exact-head-ci-repair.py"
s=importlib.util.spec_from_file_location("tw13kx",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Repair(unittest.TestCase):
 def setUp(self):self.args=copy.deepcopy(list(v.read()))
 def reject(self):
  with self.assertRaises(ValueError):v.verify(*self.args)
 def test_valid(self):self.assertEqual(v.verify(*self.args)["verified_exact_daily_unit"],"10000")
 def test_corrupt_daily_base(self):self.args[1]["exact_arithmetic"]["daily_base_units"]="9999";self.reject()
 def test_false_ci_prefix(self):self.args[0]["defects"][1]["new_prefix"]="13KX AD HOC:";self.reject()
 def test_wrong_issue_action(self):self.args[4]["issues"][4]["next_action"]="13KX FORWARD ERRATUM FIRST:";self.reject()
 def test_fake_original(self):self.args[0]["preserved_boundaries"]["independent_physical_witnesses_added"]=1;self.reject()
 def test_fake_chart_reopen(self):self.args[0]["preserved_boundaries"]["algorithm_reopens"]=1;self.reject()
if __name__=="__main__":unittest.main()
