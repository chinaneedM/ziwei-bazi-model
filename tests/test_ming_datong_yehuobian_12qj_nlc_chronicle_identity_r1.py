"""12QJ chronological index is a manuscript-source reading, not authorial equivalence."""
import json,unittest
from pathlib import Path
E=Path(__file__).resolve().parents[1]/"docs/research/MING-DATONG-YEHUOBIAN-12QJ-NLC411999003250-CHRONOLOGICAL-MANUSCRIPT-IDENTITY-CHECK-R1.json"
class Source12QJChronicleIdentity(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.d=json.loads(E.read_text(encoding="utf8"))
 def test_source_pages_digest_and_manual_review_boundary(self):
  c=self.d["capture"]
  self.assertEqual([x["pages"] for x in c["source_pdfs"]],[119,72,121])
  self.assertEqual([x["sheets"] for x in c["source_pdfs"]],[15,9,16])
  self.assertEqual(c["rendered_pdf_pages"],312)
  self.assertEqual(c["manually_inspected_pages"],3)
  self.assertFalse(c["all_312_pages_manually_read"])
  self.assertFalse(c["ocr_performed"])
  self.assertEqual(len({x["source_pdf_sha256"] for x in c["source_pdfs"]}),3)
 def test_exact_20_volume_year_labels_from_source_image(self):
  d=self.d["direct_glyph_readings"]
  self.assertEqual(d["printed_index_title"],"萬曆野獲編紀目")
  self.assertEqual(len(d["sexagenary_year_by_volume"]),20)
  self.assertEqual([x["volume"] for x in d["sexagenary_year_by_volume"]],list(range(1,21)))
  self.assertEqual([x["sexagenary_year"] for x in d["sexagenary_year_by_volume"]],["戊戌","己亥","庚子","辛丑","壬寅","癸卯","甲辰","乙巳","丙午","丁未","戊申","己酉","庚戌","辛亥","壬子","癸丑","甲寅","乙卯","丙辰","丁巳"])
  self.assertEqual(d["independent_volume5_heading"]["reading"],"萬曆三十年壬寅卷五")
 def test_source_does_not_promote_original_authorial_claim(self):
  self.assertEqual(self.d["physical_copy_count_delta"],0)
  self.assertTrue(all(v is False for v in self.d["source_scope_firewall"].values()))
  self.assertEqual(self.d["invariants"]["algorithm_reopens"],0)
  self.assertEqual(self.d["invariants"]["product_r1"],"CLOSED")
if __name__=="__main__":unittest.main()
