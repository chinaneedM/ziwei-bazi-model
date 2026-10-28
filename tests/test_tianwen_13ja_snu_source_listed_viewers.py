import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-tianwen-13ja-snu-source-listed-viewers.py"
spec=importlib.util.spec_from_file_location("v13ja",p);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
class SourceLimited(unittest.TestCase):
 def test_allow_two_provider_listed(self):self.assertEqual(M.PROVIDER_LISTED,("0017","0018"))
 def test_reject_unguarded_child(self):
  with self.assertRaises(ValueError):M.get("9999")
 def test_reject_other_volume(self):
  with self.assertRaises(ValueError):M.get("0016")
 def test_viewer_html_not_ancient_folio(self):
  x=M.audit_html(b'<html>GK05554_00 vol_no=0017 viewImgList</html>',"0017")
  self.assertFalse(x["original_ancient_folio_captured"])
 def test_ancient_juan_not_inferred(self):
  x=M.audit_html(b'<html>GK05554_00 vol_no=0018</html>',"0018")
  self.assertFalse(x["printed_juan81_or_82_bound"] or x["physical_book17_or_18_identity_bound"])
 def test_mismatched_child_detected(self):self.assertFalse(M.audit_html(b'<html>GK05554_00 0001</html>',"0017")["provider_volume_token_in_response"])
 def test_no_viewer_marker_cannot_be_positive(self):
  x=M.audit_html(b'<html>GK05554_00 0017</html>',"0017")
  self.assertEqual(x["url_marker_counts"]["viewImgList"],0)
if __name__=="__main__":unittest.main()
