import importlib.util
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-national-heritage-impressions-12zt.py"
spec=importlib.util.spec_from_file_location("tw12zt",P)
v=importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

class Test(unittest.TestCase):
    def setUp(self):
        self.a=list(v.load())
    def bad(self):
        with self.assertRaises(ValueError):
            v.verify(*self.a)
    def test_baseline(self):
        self.assertEqual(v.verify(*self.a)["status"],"PASS")
    def test_donga_later_17_18_not_first_1613(self):
        self.a[0]["heritage_items"][2]["impression_grade"]="FIRST_IMPRESSION_1613"
        self.bad()
    def test_snu_first_not_unproven_later(self):
        self.a[0]["heritage_items"][0]["impression_grade"]="LATER_IMPRESSION"
        self.bad()
    def test_no_manual_heritage_item_binding(self):
        self.a[0]["heritage_items"][0]["exact_SNU_item_id"]="GK03539_00"
        self.bad()
    def test_no_heritage_order_guess(self):
        self.a[0]["hypotheses_to_preserve"]["assign_KHS_2021_3_to_GK03539_and_2021_4_to_GK03579_proven"]=True
        self.bad()
    def test_no_target_52_folio_hash(self):
        self.a[0]["unresolved"]["snu_3539_original_work52_page_image_sha256"]="0"*64
        self.bad()
    def test_no_early_print_value_award(self):
        self.a[0]["hypotheses_to_preserve"]["first_impression_more_correct_numeric_without_collation_proven"]=True
        self.bad()
    def test_no_woodblock_ancestral_duplicate_votes(self):
        self.a[0]["unresolved"]["new_independent_plate_ancestry_votes"]=2
        self.bad()
    def test_no_promote_heritage_metadata_to_ancient_glyph(self):
        self.a[1]["sources"][0]["physical_glyph_authority"]=True
        self.bad()
    def test_source_count_forward_growth(self):
        self.a[4]["extension_source_count"]+=2
        self.a[4]["combined_source_count"]+=2
        self.a[2]["historical_audit"]["external_source_registry_extension_count"]+=2
        self.a[2]["historical_audit"]["external_source_registry_total_unique_count"]+=2
        self.assertEqual(v.verify(*self.a)["status"],"PASS")
    def test_focus_forward_compatible(self):
        self.a[2]["historical_audit"]["current_focus"].append("12ZU next")
        self.a[3]["binding"]["source_focus_count"]+=1
        self.a[3]["binding"]["latest_research_focus_prefix"]="12ZU"
        self.assertEqual(v.verify(*self.a)["status"],"PASS")

if __name__=="__main__":
    unittest.main()
