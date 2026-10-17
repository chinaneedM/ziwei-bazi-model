import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-mingshi-cadal-12yl-bibliography.py"
spec=importlib.util.spec_from_file_location("tianwen_12yl",p); v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class SourceLocator(unittest.TestCase):
 def setUp(self):self.d=list(v.load())
 def rejects(self):
  with self.assertRaises(ValueError):v.verify(*self.d)
 def test_valid(self):self.assertEqual(v.verify(*self.d)["original_glyphs_verified"],0)
 def test_fake_full_sha(self):self.d[0]["source_cadal"]["full_bytes_local_sha_verified"]=True;self.rejects()
 def test_assume_copy_year(self):self.d[0]["source_cadal"]["physical_copy_impression_date"]="1739";self.rejects()
 def test_fake_original_read(self):self.d[0]["source_cadal"]["original_target_glyph_read"]=True;self.rejects()
 def test_fake_original_glyph(self):self.d[0]["research_target"]["verified_imprint_glyph_1"]="一秒八十六微";self.rejects()
 def test_two_digital_surfaces_not_two_physical(self):self.d[0]["independence"]["ctext_vs_commons_same_cadal_id"]="TWO_ORIGINALS";self.rejects()
 def test_unchecked_ssid_not_same_copy(self):self.d[0]["source_ssid"]["physical_relation_to_cadal"]="SAME";self.rejects()
 def test_secondary_site_is_not_original(self):self.d[0]["secondary_editorial_control"]["modern_received_not_independent_original"]=False;self.rejects()
 def test_no_added_source_registry(self):self.d[0]["safeguards"]["new_source_registry_entries"]=1;self.rejects()
 def test_no_genealogy(self):self.d[0]["safeguards"]["new_genealogy_edges"]=1;self.rejects()
 def test_no_chart_reopen(self):self.d[0]["safeguards"]["algorithm_reopens"]=1;self.rejects()
 def test_issue_preserved(self):next(x for x in self.d[1]["issues"] if x["id"]=="TW-OPEN-0005")["status"]="RESOLVED_WITH_EVIDENCE";self.rejects()
 def test_no_old_state(self):self.d[2]["schema_version"]="1.625.0";self.rejects()
if __name__=="__main__":unittest.main()
