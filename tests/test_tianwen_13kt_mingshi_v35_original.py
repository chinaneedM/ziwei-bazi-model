import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13kt-mingshi-v35-original.py"
spec=importlib.util.spec_from_file_location("tw13kt",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class MingOriginal(unittest.TestCase):
 def setUp(self):self.args=copy.deepcopy(list(v.read()))
 def fails(self):
  with self.assertRaises(ValueError):v.verify(*self.args)
 def test_valid(self):self.assertEqual(v.verify(*self.args)["original_limit_constants"],3)
 def test_fake_source_digest(self):self.args[0]["provenance"]["source_sha256"]="0"*64;self.fails()
 def test_fake_target_page(self):self.args[0]["witness"]["manually_collated_pages"][2]["sha256"]="1"*64;self.fails()
 def test_fake_168_number(self):self.args[0]["arithmetic_controls"][0]["exact_received_limit"]="167.083060";self.fails()
 def test_fake_朔(self):self.args[0]["arithmetic_controls"][1]["exact_received_limit"]="24.1071145";self.fails()
 def test_fake_弦(self):self.args[0]["arithmetic_controls"][2]["exact_received_limit"]="90.06830866";self.fails()
 def test_fake_1739_impression(self):self.args[0]["provenance"]["edition_impression_date_bound"]=True;self.fails()
 def test_fake_index(self):self.args[0]["adjudication"]["ancient_0_1_index_base_selected"]=True;self.fails()
 def test_fake_independent_copy(self):self.args[0]["provenance"]["new_independent_physical_witnesses"]=1;self.fails()
 def test_fake_algorithm(self):self.args[0]["adjudication"]["chart_algorithm_reopens"]=1;self.fails()
if __name__=="__main__":unittest.main()
