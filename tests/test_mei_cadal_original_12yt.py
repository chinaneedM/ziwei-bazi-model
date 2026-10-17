import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-mei-cadal-original-12yt.py"
s=importlib.util.spec_from_file_location("mei_12yt",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class TestMeiOriginal(unittest.TestCase):
 def setUp(self):self.d=list(v.load())
 def fails(self):
  with self.assertRaises(ValueError):v.verify(*self.d)
 def test_valid(self):self.assertEqual(v.verify(*self.d)["direct_original_Mei_glyphs"],3)
 def test_fake_source_sha(self):self.d[0]["source"]["sha256"]="fake";self.fails()
 def test_wrong_v3_printed(self):self.d[0]["verified_original"][0]["printed"]="一秒三十六微";self.fails()
 def test_wrong_v4_printed(self):self.d[0]["verified_original"][2]["printed"]="○一八五";self.fails()
 def test_wrong_crop_hash(self):self.d[0]["verified_original"][1]["crop_rgb_sha"]="false";self.fails()
 def test_wrong_location(self):self.d[0]["verified_original"][0]["page"]=28;self.fails()
 def test_false_edition_date(self):self.d[0]["source"]["source_impression_year"]="1706";self.fails()
 def test_fake_same_CText_copy(self):self.d[0]["source"]["CText_251951_same_physical_copy"]="TRUE";self.fails()
 def test_false_stemmatic_root(self):self.d[0]["boundary"]["distinct_ancient_physical_witnesses_proven"]=1;self.fails()
 def test_close_issue(self):next(x for x in self.d[1]["issues"] if x["id"]=="TW-OPEN-0005")["status"]="RESOLVED";self.fails()
 def test_stale_state(self):self.d[2]["schema_version"]="1.631.0";self.fails()
 def test_future_focus_allowed(self):self.d[2]["historical_audit"]["current_focus"].append("12YU NEXT");self.assertEqual(v.verify(*self.d)["status"],"PASS")
 def test_missing_12yt_disallowed(self):self.d[2]["historical_audit"]["current_focus"]=[x for x in self.d[2]["historical_audit"]["current_focus"] if not x.startswith("12YT ")];self.fails()
if __name__=="__main__":unittest.main()
