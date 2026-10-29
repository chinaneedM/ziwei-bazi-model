import copy,importlib.util,unittest
from pathlib import Path
path=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13ky-harvard-mingshi-p7-p9-original.py"
spec=importlib.util.spec_from_file_location("tw13ky",path);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class HarvardTwoOriginalPages(unittest.TestCase):
 def setUp(self):self.args=copy.deepcopy(list(v.read()))
 def rejects(self):
  with self.assertRaises(ValueError):v.verify(*self.args)
 def test_valid(self):self.assertEqual(v.verify(*self.args)["native_original_pages"],[7,9])
 def test_false_p7_glyph(self):self.args[0]["source_native_page_collations"][0]["positive_glyph"]="有閏加二十八萬八九七七○九";self.rejects()
 def test_receipt_ordinary_zero_variant(self):self.args[0]["comparison"]["ordinary_received_quote_number"]="有閏加二十三萬八九七七○九";self.rejects()
 def test_false_p9_glyph(self):self.args[0]["source_native_page_collations"][1]["positive_glyph"]="推遲疾限各置遲次歷";self.rejects()
 def test_false_page_sha(self):self.args[0]["source_native_page_collations"][1]["full_page_rgb_sha256"]="0"*64;self.rejects()
 def test_false_roi_sha(self):self.args[0]["source_native_page_collations"][0]["roi_rgb_sha256"]="1"*64;self.rejects()
 def test_fake_siku_original(self):self.args[0]["comparison"]["original_siku_288977_original_image_confirmed"]=True;self.rejects()
 def test_fake_historical_index(self):self.args[0]["adjudication"]["historical_83_84_limit_index_selected"]=True;self.rejects()
 def test_fake_independent_copy(self):self.args[0]["source"]["distinct_original_physical_impressions_new"]=1;self.rejects()
 def test_fake_algorithm(self):self.args[0]["adjudication"]["chart_algorithm_reopens"]=1;self.rejects()
if __name__=="__main__":unittest.main()
