import copy,hashlib,importlib.util,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("xd",P/"scripts/verify-yehuobian-original-folio-intake-12xd.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class OfficialFormAndIntake(unittest.TestCase):
 def setUp(self):
  self.r=m.read(m.REC);self.x=m.read(m.XC);self.s=m.read(m.STATE);self.man=m.read(m.MANIFEST)
  self.binary=b"\x89PNG\r\n\x1a\n"+b"synthetic-test-only"*5
  self.receipt={"physical_item_barcode":"6403767830","catalog_detail":"9927","ncid":"BC0492354X","source_shelfmark":"大木;子部:雜家類:16-20","juan":20,"chapter":"改造漏刻","provider":"TOKYO_IOC","capture_channel":"INSTITUTION_FULFILLED_COPY","custody_document":"provider issued document Oki 6403767830","original_leaf_ref":"卷二十第十八葉假定測試用","source_image_url":"https://www.ioc.u-tokyo.ac.jp/~library/placeholder-synthetic-test.png","capture_date":"2026-10-15","research_use_authorization_ref":"synthetic fixture approval only; no real permission","personal_identifying_data_included":False,"claims_ancient_glyph_votes":0,"claims_independent_print_witnesses":0,"format":"PNG","image_bytes":len(self.binary),"image_sha256":hashlib.sha256(self.binary).hexdigest(),"human_glyph_review_completed":False,"print_plate_identity_adjudicated":False}
 def badledger(self,pattern):
  with self.assertRaisesRegex(ValueError,pattern):m.check_ledger(self.r,self.x,self.s,self.man)
 def badreceipt(self,pattern):
  with self.assertRaisesRegex(ValueError,pattern):m.check_receipt(self.receipt,self.binary,self.r)
 def test_ledger(self):self.assertEqual(m.verify()["new_original_source_images"],0)
 def test_synthetic_receipt_never_historical_vote(self):
  self.assertEqual(m.check_receipt(self.receipt,self.binary,self.r)["historical_glyph_votes_awarded"],0)
 def test_wrong_edition_barcode(self):
  self.receipt["physical_item_barcode"]="6403148395";self.badreceipt("catalog item scope")
 def test_wrong_chapter(self):
  self.receipt["chapter"]="釐正歷法";self.badreceipt("catalog item scope")
 def test_noncatalog_image(self):
  self.receipt["source_image_url"]="http://unbound.example.com/foo";self.badreceipt("official source URL")
 def test_modern_source_cross_binding(self):
  self.receipt["source_image_url"]="https://www.ioc.u-tokyo.ac.jp/ttsweb/hb_new/B/B17/B1765700-1,2_photo.html";self.badreceipt("modern 1959")
 def test_missing_folio(self):
  self.receipt["original_leaf_ref"]="";self.badreceipt("folio coordinate")
 def test_no_custody_receipt(self):
  self.receipt["custody_document"]="";self.badreceipt("custody")
 def test_digest_tampering(self):
  self.receipt["image_sha256"]="0"*64;self.badreceipt("binary digest")
 def test_no_permission(self):
  self.receipt["research_use_authorization_ref"]=None;self.badreceipt("written scope")
 def test_physical_print_claims_not_machine_set(self):
  self.receipt["claims_independent_print_witnesses"]=1;self.badreceipt("no automatic")
 def test_human_review_false_attestation(self):
  self.receipt["human_glyph_review_completed"]=True;self.badreceipt("human review")
 def test_claimed_filled_form(self):
  self.r["official_copy_form"]["filled"]=True;self.badledger("not an application")
 def test_dated_example_not_original(self):
  self.r["official_example_pdf"]["is_original_target"]=True;self.badledger("not an application")
 def test_1827_not_1869_shelfmark(self):
  self.r["primary_catalogs"][0]["request_shelfmark"]="倉石文庫:20128:11";self.badledger("distinct physical")
 def test_false_image_proven(self):
  self.r["invariants"]["ancient_print_page_images"]=1;self.badledger("no false progress")
 def test_reservation_limit(self):
  self.r["reservation"]["maximum_stitched_cases_per_booking"]=100;self.badledger("reservation constraints")
if __name__=="__main__":unittest.main()
