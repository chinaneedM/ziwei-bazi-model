import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("seller12vt",ROOT/"scripts/verify-yehuobian-rinrokaku-object-crosswalk-12vt.py")
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
class ItemCrosswalk(unittest.TestCase):
 def setUp(self):
  self.rec=json.loads((ROOT/gate.DATA).read_text())
  self.parent=json.loads((ROOT/gate.PARENT).read_text())
  self.shard=json.loads((ROOT/gate.SHARD).read_text())
  self.state=json.loads((ROOT/gate.STATE).read_text())
 def bad(self,part):
  with self.assertRaisesRegex(ValueError,part):gate.validate(self.rec,self.parent,self.shard,self.state)
 def test_verified_permalink_and_no_votes(self):self.assertEqual(gate.verify()["new_sources"],0)
 def test_wrong_seller_sku_fails(self):self.rec["first_party_product"]["sku"]="UNVERIFIED";self.bad("item identity")
 def test_wrong_catalogue_crosswalk_fails(self):self.rec["first_party_product"]["catalogue_numbers"][1]="WRONG";self.bad("item identity")
 def test_false_inventory_claim_fails(self):self.rec["first_party_product"]["available_to_purchase_or_in_stock"]="IN_STOCK_CONFIRMED";self.bad("stock")
 def test_false_1827_first_impression_fails(self):self.rec["first_party_product"]["printed_year_attests_this_copy_first_impression"]=True;self.bad("impression")
 def test_same_item_as_three_print_witnesses_fails(self):self.rec["identity_bridge"]["one_commercial_exemplar_not_three_independent_witnesses"]=False;self.bad("original folio")
 def test_image_promotion_fails(self):self.rec["identity_bridge"]["site_page_is_original_folio_scan"]=True;self.bad("original folio")
 def test_unsupported_original_glyph_fails(self):self.rec["future_image_intake"]["loci"]["GONGJIN"]="宮禁";self.bad("unsupported original glyph")
 def test_no_external_outreach(self):self.rec["contact_or_purchase"]["seller_contacted"]=True;self.bad("external request")
 def test_no_source_count_growth_for_same_seller_item(self):self.rec["source_registration"]["extensions_after"]=52;self.bad("source snapshot")
 def test_no_genealogy_upgrade(self):self.rec["transmission_impact"]["edges_supported"].append("CLAIM");self.bad("genealogy")
if __name__=="__main__":unittest.main()
