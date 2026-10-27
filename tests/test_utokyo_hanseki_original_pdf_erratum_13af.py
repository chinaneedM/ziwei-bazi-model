import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-utokyo-hanseki-original-pdf-erratum-13af.py"
spec=importlib.util.spec_from_file_location("hanseki13af",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SourceFamilyHomographCorrection(unittest.TestCase):
 def test_state(self):self.assertTrue(m.verify())
 def test_original_pdf_not_original_historical_goryeosa(self):
  x=m.load(m.E);self.assertTrue(x["acquisition"]["original_binaries_retrieved"])
  self.assertFalse(x["scope"]["historical_goryeosa_work52_original_image_acquired"])
 def test_separate_romanized_shibu_concepts(self):
  x=m.load(m.E);self.assertNotEqual(x["pdfs"][0]["part"],x["pdfs"][1]["part"])
  self.assertTrue(x["correction"]["prior_record_preserved_without_silent_rewrite"])
 def test_independent_catalogue_not_numeric_vote(self):
  x=m.load(m.E);self.assertEqual(x["scope"]["direct_Historical_Goryeosa_numeric_votes_added"],0)
  self.assertFalse(x["scope"]["whole_History_catalog_negative_search_proven"])
if __name__=="__main__":unittest.main()
