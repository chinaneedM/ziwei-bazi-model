"""12QK remainder files 4-9 do not inflate independent copies or attested glyphs."""
import ast,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QK-NLC-OLD20-FASC4-9-ATLAS-STAGING-R1.json"
SCRIPT=ROOT/"scripts/probe-yehuobian-nlc-old20-fascicles-wave1-12qi.py"
class Old20Wave2Stage(unittest.TestCase):
 def test_counts_and_duplicate_manuscript_control(self):
  x=json.loads(S.read_text(encoding="utf8"))
  self.assertEqual([s["fascicle"] for s in x["source_digital_files"]],[4,5,6,7,8,9])
  self.assertEqual([s["expected_pdf_pages"] for s in x["source_digital_files"]],[56,63,116,110,87,141])
  self.assertEqual(x["expected_pdf_images"],573)
  self.assertEqual(x["expected_total_if_success_10_fascicles"],1030)
  self.assertEqual(x["physical_copy_count_increment"],0)
  self.assertEqual(x["source_registry_increment"],0)
  self.assertFalse(x["manual_target_passage_search_completed"])
  self.assertFalse(x["historical_text_absence_proven"])
  self.assertEqual(x["source_copy_authorial_original_equivalence"],"UNPROVEN")
 def test_script_remains_source_bounded_and_no_ocr(self):
  src=SCRIPT.read_text(encoding="utf8")
  ast.parse(src)
  for n,token in [(4,'383062'),(5,'383066'),(6,'383071'),(7,'383070'),(8,'383069'),(9,'383063')]:
   self.assertIn(f'{n}: ("{token}"',src)
  self.assertIn("ocr_performed",src)
  self.assertIn("exact_target_heading_manually_verified",src)
  self.assertIn("SOURCE_PAGE_COUNT_MISMATCH",src)
if __name__=="__main__":unittest.main()
