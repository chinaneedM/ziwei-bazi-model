import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("wz",ROOT/"scripts/verify-yehuobian-12wz-tokyo-seven-firstparty-catalog.py")
p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
class CatalogNotPaperPrint(unittest.TestCase):
 def setUp(self):self.r=p.load(p.REC);self.s=p.load(p.SHARD);self.st=p.load(p.STATE);self.m=p.load(p.MAN)
 def bad(self,msg):
  with self.assertRaisesRegex(ValueError,msg):p.validate(self.r,self.s,self.st,self.m)
 def test_real_evidence(self):self.assertEqual(p.verify()["historic_print_votes"],0)
 def test_seven_not_seven_originals(self):
  self.r["limits"]["all_7_records_are_seven_independent_historical_print_witnesses"]=True;self.bad("inference gate")
 def test_imabori_missing_21_22_doesnt_certify_juan20(self):
  self.r["imabori"]["juan20_physically_present_and_usable"]=True;self.bad("Imabori physical")
 def test_false_print_page(self):
  self.r["target_physical_impressions"]["1827"]["source_issued_image_uri"]="invented";self.bad("no original folio")
 def test_1827_crosswalk_preserved(self):
  self.r["items"][0]["ciNiiItem"]="invented";self.bad("Oki catalog")
 def test_wrong_1869_shelfmark(self):
  self.r["items"][3]["shelfmark"]="no";self.bad("Kuraishi catalog")
 def test_seven_single_metadata_registration(self):
  self.r["limits"]["registered_metadata_sources"]=7;self.bad("one source")
 def test_new_source_status_cannot_be_glyph(self):
  self.s["sources"][0]["physical_glyph_authority"]=True;self.bad("catalogue evidence")
 def test_source_union_monotone(self):
  self.m["combined_source_count"]=705;self.bad("registered evidence growth")
 def test_no_algorithm_reopen(self):
  self.r["counts"]["algorithm_reopen_count"]=1;self.bad("product")
if __name__=="__main__":unittest.main()
