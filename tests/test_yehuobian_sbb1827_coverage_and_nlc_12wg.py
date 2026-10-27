import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("wg",ROOT/"scripts/probe-yehuobian-sbb1827-coverage-and-nlc-12wg.py")
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class SourceScope(unittest.TestCase):
 def test_exact_provider_endpoints(self):
  for k,x in (("manifest",p.MANIFEST),("mets",p.METS),("nlc",p.NLC)):
   self.assertEqual(p.checked_source(x,k),x)
 def test_id_guess_forbidden(self):
  with self.assertRaisesRegex(ValueError,"wrong exact"):p.checked_source("https://content.staatsbibliothek-berlin.de/dc/PPN334378186X-0000003/full/max/0/default.jpg","manifest")
 def test_crosshost_forbidden(self):
  with self.assertRaisesRegex(ValueError,"wrong exact"):p.checked_source("https://evil.example/x","manifest")
 def test_nlc_web_scraping_endpoint_guess_forbidden(self):
  with self.assertRaisesRegex(ValueError,"first-party landing"):p.checked_source("https://gjpc.nlc.cn/xlsworkbench/private-search","nlc")
 def test_budgets(self):
  self.assertEqual(p.MAX_BYTES,12_000_000);self.assertEqual(p.MAX_NLC_BYTES,500_000)
 def test_v2_synthetic_manifest_label_only_not_glyph(self):
  src={"@type":"sc:Manifest","label":"Preview",
   "sequences":[{"canvases":[{"@id":"id1","label":"封面","images":[]},{"@id":"id2","label":"卷二十","images":[{"resource":{"@id":"https://source.test/image1"}}]}]}],
   "structures":[{"label":"全册"}]}
  result=p.iiif_analysis(json.dumps(src).encode())
  self.assertEqual(result["canvas_count"],2)
  self.assertEqual(len(result["target_keyword_canvas_label_hits"]),1)
  self.assertFalse(result["declared_target_folio_image_human_verified"])
 def test_mets_physical_div_label_is_not_ancient_original(self):
  raw='<mets:mets xmlns:mets="http://www.loc.gov/METS/"><mets:structMap TYPE="PHYSICAL"><mets:div LABEL="卷二十" TYPE="page"/></mets:structMap></mets:mets>'.encode("utf-8")
  z=p.mets_analysis(raw)
  self.assertEqual(z["structmap_count"],1)
  self.assertEqual(len(z["target_keyword_div_hits"]),1)
  self.assertFalse(z["target_article_original_page_human_verified"])
 def test_nonmanifest_fails(self):
  with self.assertRaisesRegex(ValueError,"not a IIIF manifest"):p.iiif_analysis(b'{"type":"Collection","items":[]}')
if __name__=="__main__":unittest.main()
