import copy,importlib.util,unittest
from pathlib import Path
path=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13kw-mingshi-source-attribution-erratum.py"
spec=importlib.util.spec_from_file_location("tw13kw",path);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class AttributionErratum(unittest.TestCase):
 def setUp(self):self.a=copy.deepcopy(list(v.read()))
 def rejects(self):
  with self.assertRaises(ValueError):v.verify(*self.a)
 def test_valid(self):self.assertEqual(v.verify(*self.a)["corrected_source_subject"],"遲次歷")
 def test_erase_old_claim(self):self.a[0]["prior_published_quote_preserved"]="corrected silently";self.rejects()
 def test_false_regular_text(self):self.a[0]["correction"]["ordinary_received_exact_subject"]="推遲疾限　各置遲疾歷";self.rejects()
 def test_false_siku(self):self.a[0]["correction"]["siku_received_exact_subject"]="推遲疾限　各置遲次歷";self.rejects()
 def test_fake_original_operator(self):self.a[0]["correction"]["full_original_harvard_p7_to_p12_operator_native_glyph_verified"]=True;self.rejects()
 def test_fake_physical_copy(self):self.a[0]["correction"]["two_website_transcriptions_not_two_ancient_physical_copies"]=False;self.rejects()
 def test_wrong_arithmetic(self):self.a[0]["arithmetic_invariance"]["prior_13ku_exact_four_quarters_minus_two_half_turns"]="24.1071147";self.rejects()
 def test_fake_algorithm(self):self.a[0]["bounded_consequence"]["algorithm_reopens"]=1;self.rejects()
if __name__=="__main__":unittest.main()
