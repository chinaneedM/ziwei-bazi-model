import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13lb-cadal-siku-native.py"
s=importlib.util.spec_from_file_location("tw13lb",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Native(unittest.TestCase):
 def setUp(self):self.a=copy.deepcopy(list(v.load()))
 def fails(self):
  with self.assertRaises(ValueError):v.verify(*self.a)
 def test_valid(self):self.assertEqual(v.verify(*self.a)["delta_units"],50000)
 def test_fake_source(self):self.a[0]["source"]["sha256"]="0"*64;self.fails()
 def test_fake_p11_glyph(self):self.a[0]["original_pages"][1]["original_literal"]="有閏加二十三萬八九七七○九";self.fails()
 def test_fake_p16_glyph(self):self.a[0]["original_pages"][2]["original_literal"]="推遲疾限各置遲次歷";self.fails()
 def test_fake_page_hash(self):self.a[0]["original_pages"][1]["full_rgb_sha256"]="0"*64;self.fails()
 def test_fake_roi_hash(self):self.a[0]["original_pages"][2]["roi_rgb_sha256"]="a"*64;self.fails()
 def test_fake_1739(self):self.a[0]["boundaries"]["source_original_1739_impression_proven"]=True;self.fails()
 def test_fake_copying(self):self.a[0]["cross_witness"]["historical_copying_lineage_proven"]=True;self.fails()
 def test_fake_chart(self):self.a[0]["boundaries"]["algorithm_reopens"]=1;self.fails()
if __name__=="__main__":unittest.main()
