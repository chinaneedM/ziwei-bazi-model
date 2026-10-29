import copy,importlib.util,unittest
from pathlib import Path
path=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13ku-mingshi-four-phase-return.py"
spec=importlib.util.spec_from_file_location("tw13ku",path);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class FourPhaseReturn(unittest.TestCase):
 def setUp(self):self.args=copy.deepcopy(list(v.read()))
 def reject(self):
  with self.assertRaises(ValueError):v.verify(*self.args)
 def test_valid(self):self.assertEqual(v.verify(*self.args)["phase_cases"],5)
 def test_false_synodic(self):self.args[0]["rational_basis"]["synodic_turn_limit"]="24.1071147";self.reject()
 def test_false_half_turn(self):self.args[0]["rational_basis"]["middle_turn_limit"]="168";self.reject()
 def test_false_residual(self):self.args[0]["conditional_four_phase_replay"][2]["residual_limit"]="12.05355731";self.reject()
 def test_false_parity(self):self.args[0]["conditional_four_phase_replay"][3]["parity"]="EVEN";self.reject()
 def test_fake_original_p7(self):self.args[0]["original_source"]["source_page_p7_to_p12_native_operator_collation_this_batch"]=True;self.reject()
 def test_fake_original_operator(self):self.args[0]["received_operator"]["independent_source_native_page_confirmation_of_this_full_phrase"]=True;self.reject()
 def test_fake_168_identity(self):self.args[0]["boundaries"]["historical_168_integer_is_identical_to_168_083060_middle_period"]=True;self.reject()
 def test_fake_83_84_selection(self):self.args[0]["boundaries"]["historic_zero_or_one_base_selected"]=True;self.reject()
 def test_fake_algorithm(self):self.args[0]["boundaries"]["chart_algorithm_reopens"]=1;self.reject()
if __name__=="__main__":unittest.main()
