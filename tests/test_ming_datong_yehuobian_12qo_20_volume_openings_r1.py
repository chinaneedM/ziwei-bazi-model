import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=json.loads((R/"docs/research/MING-DATONG-YEHUOBIAN-12QO-NLC411999003250-ALL20-CHRONICLE-VOLUME-OPENINGS-R1.json").read_text(encoding="utf8"))
Q=json.loads((R/"docs/research/MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json").read_text(encoding="utf8"))
S=json.loads((R/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
class Test12QO(unittest.TestCase):
 def test_twenty(self):
  a=E["original_juan_openings"]
  self.assertEqual([x["volume"] for x in a],list(range(1,21)))
  self.assertEqual([(x["digital_fascicle"],x["pdf_page"]) for x in a],[(1,3),(1,35),(1,62),(1,88),(2,1),(3,1),(3,83),(4,1),(4,35),(5,1),(6,1),(7,1),(7,48),(7,68),(8,1),(9,1),(9,84),(10,1),(10,81),(10,137)])
  self.assertEqual([x["volume"] for x in a if x["new_location_12qo"]],[2,3,4,7,9])
  self.assertEqual([x["volume"] for x in a if x["right_leaf_has_previous_volume"]],[2,4,7,9,14,17,19,20])
  for x in a:
   self.assertEqual(len(x["page_jpeg_sha256"]),64)
   self.assertTrue(1<=x["pdf_page"]<=Q["sources"][x["digital_fascicle"]-1]["source_pdf_pages"])
   self.assertEqual(x["witness_copy_increment"],0)
  self.assertIn("PARTLY_CLIPPED",a[5]["glyph_caveat"])
 def test_scope(self):
  c=E["image_reverification"]
  self.assertEqual((c["source_page_jpegs_verified"],c["contact_jpegs_verified"],c["digest_mismatches"]),(1030,132,0))
  self.assertEqual(sum(x["pdf_pages"] for x in E["source_fascicles"]),1030)
  self.assertEqual(sum(x["contact_sheets"] for x in E["source_fascicles"]),132)
  for x in E["source_fascicles"]:
   self.assertEqual(x["source_pdf_sha256_previously_verified"],Q["sources"][x["fascicle"]-1]["source_pdf_sha256"])
  for flag in ("source_pdf_hash_recomputed_this_batch","ocr_used"):
   self.assertFalse(c[flag])
  for flag in E["unresolved"]:
   self.assertFalse(E["unresolved"][flag])
  self.assertEqual(E["invariants"]["algorithm_reopens"],0)
  self.assertEqual(S["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
if __name__=="__main__":unittest.main()
