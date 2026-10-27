"""12QI physical witness de-duplication and no-OCR atlas stage contract."""
import ast
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STAGE=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QI-NLC-OLD20-FASC1-3-ATLAS-STAGING-R1.json"
SCRIPT=ROOT/"scripts/probe-yehuobian-nlc-old20-fascicles-wave1-12qi.py"
class NLC12QIWave1BoundaryTest(unittest.TestCase):
    def setUp(self):
        self.stage=json.loads(STAGE.read_text(encoding="utf-8"))
        self.script=SCRIPT.read_text(encoding="utf-8")
    def test_exact_three_fascicles_not_three_copies(self):
        self.assertEqual([x["number"] for x in self.stage["fascicles_to_capture"]],[1,2,3])
        self.assertEqual(sum(x["expected_pages"] for x in self.stage["fascicles_to_capture"]),312)
        self.assertEqual(self.stage["physical_copy_count_delta"],0)
        self.assertFalse(self.stage["old20_target_found"])
        self.assertFalse(self.stage["old20_whole_work_absence_proven"])
    def test_source_capture_does_not_make_manual_glyph_claims(self):
        self.assertTrue(self.stage["derived_page_images_are_not_direct_manually_verified_glyphs"])
        self.assertFalse(self.stage["ocr_performed"])
        self.assertFalse(self.stage["runtime_or_algorithm_changes"])
        self.assertEqual(self.stage["chart_r1"],"CLOSED")
        tree=ast.parse(self.script)
        self.assertGreater(len(tree.body),2)
        self.assertIn("ALL_SOURCE_PAGES_CAPTURED_MANUAL_TARGET_SEARCH_PENDING",self.script)
        self.assertIn("physical_copy_count_increment",self.script)
        self.assertIn("ocr_performed",self.script)
if __name__=="__main__":unittest.main()
