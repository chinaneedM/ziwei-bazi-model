import importlib.util,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts"/"probe-tianwen-13iy-khs-2114-1-firstparty.py"
sp=importlib.util.spec_from_file_location("probe13iy",P)
M=importlib.util.module_from_spec(sp);sp.loader.exec_module(M)
def fake(title="고려사",id="보물 2114-1",n=600):
 return ("<response><item><ccbaMnm1>"+title+"</ccbaMnm1><ccbaAsno>"+id+"</ccbaAsno><content>"+("가"*n)+"</content></item></response>").encode()
class FirstpartyProbe(unittest.TestCase):
 def test_good_firstparty_identity_is_only_modern(self):
  p=M.assess(fake());self.assertTrue(p["direct_official_2114_1"]);self.assertFalse(p["ancient_original_page"]);self.assertIsNone(p["physical_book29_juan_map"])
 def test_2114_2_must_not_be_2114_1(self):self.assertFalse(M.assess(fake(id="보물 2114-2"))["direct_official_2114_1"])
 def test_short_detail_rejected(self):self.assertFalse(M.assess(fake(n=100))["direct_official_2114_1"])
 def test_title_missing_rejected(self):self.assertFalse(M.assess(fake(title="다른 책"))["direct_official_2114_1"])
 def test_wrong_2114_x_rejected(self):self.assertFalse(M.assess(fake(id="2114-3"))["direct_official_2114_1"])
 def test_truncated_xml_rejected(self):self.assertFalse(M.assess(b"<bad")["direct_official_2114_1"])
 def test_html_is_not_xml(self):self.assertFalse(M.assess(b"<html>oops</html>")["direct_official_2114_1"])
 def test_empty_body_rejected(self):self.assertFalse(M.assess(b"")["direct_official_2114_1"])
 def test_cross_designation_control_is_separate(self):
  v=M.assess(fake(id="보물 2114-2"),"2114-2");self.assertFalse(v["direct_official_2114_1"]);self.assertTrue(v["identity_matched"])
 def test_exact_bytes_have_sha(self):
  import hashlib
  b=fake();self.assertEqual(M.assess(b)["body_sha256"],hashlib.sha256(b).hexdigest())
if __name__=="__main__":unittest.main()
