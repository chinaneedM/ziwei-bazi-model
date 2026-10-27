import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def get(name,path):
 spec=importlib.util.spec_from_file_location(name,ROOT/path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
V=get("v13iv","scripts/verify-tianwen-13iv-khs-source-scope.py")
P=get("p13iv","scripts/probe-tianwen-13iv-khs-heritage-xml.py")
class Scope(unittest.TestCase):
 def setUp(self):self.r=V.load()
 def denied(self):
  with self.assertRaises(AssertionError):V.check(self.r)
 def test_original(self):self.assertTrue(V.check(self.r))
 def test_false_government_full_text(self):self.r["official_api"]["returned_official_long_text_confirmed"]=True;self.denied()
 def test_unverified_ancient_six(self):self.r["pending"]["g893_six_original_numbers"]=[1]*6;self.denied()
 def test_no_13io_resurrection(self):self.r["pending"]["gk5553_book29_to_juan81_83"]="CONFIRMED";self.denied()
 def test_no_specific_1482_impression(self):self.r["hypothesis_fence"]["physical_copy_impression_year"]="1482";self.denied()
 def test_no_glyph_vote(self):self.r["counts"]["new_numerical_winners"]=1;self.denied()
 def test_no_enumeration(self):self.r["official_api"]["target_code_variants"].append("21140201");self.denied()
 def test_snu_conjecture_preserved(self):self.r["hypothesis_fence"]["snu_conjecture_not_government_error_proof"]=False;self.denied()
 def test_old_13ei_retired(self):self.r["pending"]["older_13EI"]="PROVEN";self.denied()
class Parser(unittest.TestCase):
 def test_no_unlisted_ids(self):
  self.assertIn("ccbaAsno=21140200",P.request_url("21140200"))
  with self.assertRaises(AssertionError):P.request_url("21140201")
 def test_reject_html(self):self.assertFalse(P.parse_xml(b"<html>blocked</html>")["official_description_verified"])
 def test_reject_plain(self):self.assertFalse(P.parse_xml(b"not xml")["official_description_verified"])
 def test_title_and_id_and_detail_required(self):
  yes=b"<data><name>Goryeosa</name><code>21140200</code><content>"+b"x"*500+b"</content></data>"
  self.assertTrue(P.parse_xml(yes)["official_description_verified"])
  no=b"<data><name>Goryeosa</name><content>"+b"x"*500+b"</content></data>"
  self.assertFalse(P.parse_xml(no)["official_description_verified"])
 def test_not_original_ancient_leaf(self):
  yes=b"<data><name>Goryeosa</name><code>21140200</code><content>"+b"x"*500+b"</content></data>"
  self.assertFalse(P.parse_xml(yes)["original_ancient_folio_verified"])
if __name__=="__main__":unittest.main()
