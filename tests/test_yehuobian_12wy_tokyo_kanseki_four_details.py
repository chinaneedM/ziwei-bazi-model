import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("wy",ROOT/"scripts/probe-yehuobian-12wy-tokyo-kanseki-four-details.py")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class SourceEmittedFour(unittest.TestCase):
 def test_four_exact_provider_ids(self):
  self.assertEqual([x["dno"] for x in m.RECORDS],["9927","90972","103841","104379"])
  self.assertEqual(len(m.RECORDS),4)
 def test_verified_ftlink_source(self):
  for x in m.RECORDS:self.assertTrue(m.guard(x,m.url_for(x)))
 def test_no_guessed_detail_id(self):
  x=dict(m.RECORDS[0]);x["dno"]="6403767830"
  with self.assertRaisesRegex(ValueError,"source-verified"):m.guard(x,m.url_for(x))
 def test_no_modified_detail_url(self):
  x=m.RECORDS[0]
  with self.assertRaisesRegex(ValueError,"source-emitted"):m.guard(x,m.url_for(x)+"&leaf=1")
 def test_catalog_text_does_not_date_paper(self):
  x=m.inspect("野獲編 道光七年刊本".encode(),m.RECORDS[0])
  self.assertFalse(x["original_juan20_leaf_image_acquired"])
  self.assertFalse(x["independently_printed_1827_paper_proven"])
  self.assertEqual(x["new_historical_glyph_votes"],0)
 def test_no_original_identity_from_barcode_mention(self):
  x=m.inspect("6403767830".encode(),m.RECORDS[1])
  self.assertTrue(x["page_contains_Oki_barcode_literal"])
  self.assertFalse(x["independently_revised_1869_paper_proven"])
 def test_html_sha_is_deterministic(self):
  b="漢籍".encode();x=m.inspect(b,m.RECORDS[0])
  self.assertEqual(x["raw_provider_html_sha256"],m.hashlib.sha256(b).hexdigest())
 def test_max_source_bytes(self):
  with self.assertRaisesRegex(ValueError,"oversized"):m.inspect(b"a"*(m.MAX_BYTES+1),m.RECORDS[0])
if __name__=="__main__":unittest.main()
