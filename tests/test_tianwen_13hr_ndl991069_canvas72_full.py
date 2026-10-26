import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "tianwen_13hr", ROOT / "scripts/probe-tianwen-13hr-ndl991069-canvas72-full.py"
)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

class Ndl1909Canvas72Capture(unittest.TestCase):
    def test_bad_external_manifest_fails(self):
        fake = {"@id": M.MANIFEST, "sequences": [{"canvases": [{"@id": "https://wrong.invalid"}]*395}]}
        with self.assertRaises(ValueError): M.source_canvas(fake)

    def test_source_emitted_canvas_and_service_binding(self):
        ids = [f"https://dl.ndl.go.jp/api/iiif/991069/canvas/{i}" for i in range(1, 92)]
        cs = [{"width":5893,"height":4597} for _ in ids]
        with patch.object(M.HN, "canvases", return_value=(cs, ids)), patch.object(M.HN, "toc_scope", return_value=(68,91)), patch.object(M.HN, "image_service", return_value="https://dl.ndl.go.jp/api/iiif/991069/R0000072"):
            self.assertEqual(M.source_canvas({})[1], "https://dl.ndl.go.jp/api/iiif/991069/R0000072")
        ids[71] = ids[72]
        with patch.object(M.HN, "canvases", return_value=(cs, ids)), patch.object(M.HN, "toc_scope", return_value=(68,91)), patch.object(M.HN, "image_service", return_value="https://dl.ndl.go.jp/api/iiif/991069/R0000072"):
            with self.assertRaises(ValueError): M.source_canvas({})

    def test_wrong_service_or_toc_fails_closed(self):
        ids = [f"https://dl.ndl.go.jp/api/iiif/991069/canvas/{i}" for i in range(1,92)]
        cs = [{"width":5893,"height":4597} for _ in ids]
        with patch.object(M.HN, "canvases", return_value=(cs,ids)), patch.object(M.HN, "toc_scope", return_value=(68,91)), patch.object(M.HN, "image_service", return_value="https://dl.ndl.go.jp/api/iiif/991069/R0000073"):
            with self.assertRaises(ValueError): M.source_canvas({})
        with patch.object(M.HN, "canvases", return_value=(cs,ids)), patch.object(M.HN, "toc_scope", return_value=(69,91)), patch.object(M.HN, "image_service", return_value=M.CANVAS):
            with self.assertRaises(ValueError): M.source_canvas({})

    def test_bounded_context_crops_and_non_decisive_scope(self):
        self.assertEqual(M.HEADINGS["winter-heading-context"], (115,130,780,650))
        self.assertEqual(M.HEADINGS["initial-days-context"], (105,540,775,995))
        for roi in M.HEADINGS.values():
            a,b,c,d = M.scaled_box(roi, (3773,2943))
            self.assertTrue(0<=a<c<=3773 and 0<=b<d<=2943)
        for dims in ((6000,4680),(800,624),(4000,0)):
            with self.assertRaises(ValueError): M.scaled_box((115,130,780,650),dims)
        with self.assertRaises(ValueError): M.scaled_box((115,130,1800,650),(3773,2943))
        self.assertEqual(M.EXPECTED_MANIFEST_SHA, "5ef67e4f84917ffd1eafee2b2da1d22f1aeb68f8d7f2ac441b7d398be19bf674")

    def test_report_schema_matches_canvas72_source(self):
        source = (ROOT / "scripts/probe-tianwen-13hr-ndl991069-canvas72-full.py").read_text(encoding="utf-8")
        self.assertIn("TIANWEN-13HR-NDL991069-CANVAS72-ONE-PAGE-SOURCE-CAPTURE-R1", source)
        self.assertNotIn("CANVAS73-ONE-PAGE-SOURCE-CAPTURE", source)
