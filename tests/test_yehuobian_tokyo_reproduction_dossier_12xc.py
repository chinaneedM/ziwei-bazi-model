import copy,importlib.util,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("xc",P/"scripts/verify-yehuobian-tokyo-reproduction-dossier-12xc.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TokyoReproDossier(unittest.TestCase):
 def setUp(self):
  self.r=m.read(m.REC);self.wz=m.read(m.WZ);self.xa=m.read(m.XA);self.sn=m.read(m.SN);self.s=m.read(m.STATE);self.man=m.read(m.MANIFEST)
 def bad(self,needle):
  with self.assertRaisesRegex(ValueError,needle):m.validate(self.r,self.wz,self.xa,self.sn,self.s,self.man)
 def test_actual_current_ledger(self):
  self.assertEqual(m.verify()["source_issued_printed_folios"],0)
 def test_no_fake_1827_identifier(self):
  self.r["target_items"][0]["item"]="6403148395";self.bad("Oki exact")
 def test_no_fake_1869_identifier(self):
  self.r["target_items"][1]["item"]="6403767830";self.bad("Kuraishi exact")
 def test_no_misreading_imabori_lacuna(self):
  self.r["target_items"][2]["physical"]="COMPLETE_VOLUME20";self.bad("never promote")
 def test_original_folio_claim_not_allowed(self):
  self.r["evidence_gates"]["source_issued_original_juan20_page_image_count"]=1;self.bad("original printed folio absent")
 def test_claimed_reply_not_allowed(self):
  self.r["request_package"]["staff_reply_received"]=True;self.bad("external action")
 def test_claimed_sent_application_not_allowed(self):
  self.r["request_package"]["formal_copy_application_submitted"]=True;self.bad("external action")
 def test_no_personal_info_fake(self):
  self.r["request_package"]["applicant_phone"]="000-0000";self.bad("personal information")
 def test_no_modern_image_promotion(self):
  self.r["evidence_gates"]["modern_1959_image_link_not_ancient_original"]=False;self.bad("evidence scope")
 def test_source_registry_count_not_faked(self):
  self.r["accounting"]["registry_union"]=707;self.bad("frozen current source")
 def test_policy_duplicate(self):
  self.r["official_service_pages"][0]["url"]="https://example.org/form";self.bad("duplicate policy parent")
 def test_genealogy_not_promoted(self):
  self.r["transmission_impact"]["edges_supported"]=["9927->90972"];self.bad("not a lineage claim")
if __name__=="__main__":unittest.main()
