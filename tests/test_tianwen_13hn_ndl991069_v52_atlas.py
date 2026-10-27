import importlib.util, unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts/probe-tianwen-13hn-ndl991069-v52-atlas.py"
S=importlib.util.spec_from_file_location("thirteen_hn",P);m=importlib.util.module_from_spec(S);S.loader.exec_module(m)
class BoundedAtlas(unittest.TestCase):
 def d(self):
  ids=[f"https://dl.ndl.go.jp/api/iiif/991069/canvas/{j}" for j in range(1,9)]
  cs=[{"@id":u,"images":[{"resource":{"service":{"@id":f"https://dl.ndl.go.jp/api/iiif/991069/image/{j}"}}}]} for j,u in enumerate(ids,1)]
  return {"@id":m.URL,"sequences":[{"canvases":cs}],"structures":[{"label":"第六　高麗史五十二","canvases":[ids[1]]},{"label":"第七　高麗史五十三","canvases":[ids[5]]}]}
 def test_manifest_canvas_and_source_toc(self):
  d=self.d();cs,ids=m.canvases(d);self.assertEqual(m.toc_scope(d,ids),(2,6))
 def test_source_issued_service(self):
  self.assertEqual(m.image_service(self.d()["sequences"][0]["canvases"][1]),"https://dl.ndl.go.jp/api/iiif/991069/image/2")
 def test_ssrf_host_blocked(self):
  c=self.d()["sequences"][0]["canvases"][1];c["images"][0]["resource"]["service"]["@id"]="https://evil.example/api/iiif/991069/image/2"
  with self.assertRaises(ValueError):m.image_service(c)
 def test_no_guess_when_next_heading_absent(self):
  d=self.d();d["structures"]=d["structures"][:1];_,ids=m.canvases(d)
  with self.assertRaises(ValueError):m.toc_scope(d,ids)
 def test_ambiguous_foreign_pid(self):
  d=self.d();d["@id"]="https://dl.ndl.go.jp/api/iiif/991068/manifest.json"
  with self.assertRaises(ValueError):m.canvases(d)
