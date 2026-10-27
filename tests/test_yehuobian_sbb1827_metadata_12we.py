import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("sbb12we",ROOT/"scripts/probe-yehuobian-sbb1827-metadata-12we.py")
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class ProviderRoutes(unittest.TestCase):
 def test_exact_object_and_only_two_documented_routes(self):
  self.assertEqual(p.PPN,"PPN334378186X")
  self.assertEqual(set(p.URLS),{"manifest","mets"})
  self.assertTrue(all(p.sanctioned(u) for u in p.URLS.values()))
 def test_page_address_guess_rejected(self):
  with self.assertRaisesRegex(ValueError,"not a provider-documented"):p.sanctioned("https://content.staatsbibliothek-berlin.de/dc/PPN334378186X-00000011/full/1200,/0/default.jpg")
 def test_cross_host_rejected(self):
  with self.assertRaisesRegex(ValueError,"unauthorized provider"):p.sanctioned("https://evil.example/dc/PPN334378186X/manifest")
 def test_v3_synthetic_manifest_positive_label_is_not_original_article_proof(self):
  a={"type":"Manifest","label":{"en":["Example sample"]},"items":[{"id":"canvas1","label":{"none":["卷二十"]}}],"structures":[]}
  result=p.parse_manifest(json.dumps(a).encode())
  self.assertEqual(result["canvas_count"],1)
  self.assertTrue(result["has_source_issued_juan20_canvas_label"])
  self.assertFalse(result["target_article_original_folio_confirmed"])
 def test_v2_synthetic_manifest(self):
  a={"@type":"sc:Manifest","label":"Example","sequences":[{"canvases":[{"@id":"canvas2","label":"第七叶"}]}]}
  self.assertEqual(p.parse_manifest(json.dumps(a).encode())["canvas_count"],1)
 def test_nonmanifest_rejected(self):
  with self.assertRaisesRegex(ValueError,"not an IIIF"):p.parse_manifest(b'{"type":"Collection"}')
 def test_mets_synthetic_struct_div(self):
  x='<mets:mets xmlns:mets="http://www.loc.gov/METS/"><mets:structMap><mets:div LABEL="卷二十"/></mets:structMap></mets:mets>'.encode("utf-8")
  z=p.parse_mets(x)
  self.assertEqual(len(z["label_matched_divs"]),1)
  self.assertFalse(z["target_article_original_folio_confirmed"])
 def test_nonmets_rejected(self):
  with self.assertRaisesRegex(ValueError,"not METS"):p.parse_mets(b"<html/>")
if __name__=="__main__":unittest.main()
