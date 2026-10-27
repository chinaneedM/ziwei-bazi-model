import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("thirteen_hm",ROOT/"scripts/probe-tianwen-13hm-ndl991069-iiif.py")
m=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(m)
class NdlIiifManifestBoundaries(unittest.TestCase):
 def test_iiif2_range_locator_only(self):
  a={"@id":m.URL,"label":"高麗史","sequences":[{"canvases":[{"@id":"canvas/a"},{"@id":"canvas/b"}]}],
     "structures":[{"label":"高麗史五十二","canvases":["canvas/b"]}]}
  o=m.analyze(a)
  self.assertEqual(o["canvas_count"],2)
  self.assertEqual(o["toc_range_hints"][0]["bound_canvas_positions"],[2])
  self.assertFalse(o["target_d14_glyph_obtained"])
 def test_iiif3_supported_without_original_glyph(self):
  a={"id":m.URL,"label":{"ja":["高麗史"]},"items":[{"id":"canvas/a"},{"id":"canvas/b"}]}
  o=m.analyze(a)
  self.assertEqual(o["canvas_count"],2)
  self.assertEqual(o["toc_range_hints"],[])
 def test_unrelated_manifest_rejected(self):
  with self.assertRaises(ValueError):m.analyze({"@id":"https://dl.ndl.go.jp/api/iiif/991068/manifest.json","sequences":[{"canvases":[{"@id":"x"}]}]})
 def test_duplicate_canvas_rejected(self):
  with self.assertRaises(ValueError):m.analyze({"@id":m.URL,"sequences":[{"canvases":[{"@id":"x"},{"@id":"x"}]}]})
 def test_no_inferred_target_without_canvas(self):
  with self.assertRaises(ValueError):m.analyze({"@id":m.URL,"sequences":[{"canvases":[]}]})
