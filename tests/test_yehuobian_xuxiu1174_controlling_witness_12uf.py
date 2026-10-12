"""12UF: fail closed against repeated same-image glyph votes and 1827 catalogue inference."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LEDGER="docs/research/MING-DATONG-YEHUOBIAN-12UF-SOURCE-READING-CONTROL-AND-IMPRESSION-GATES-R1.json"
def read(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
class SourcePrecedence12UF(unittest.TestCase):
    def setUp(self):
        self.x=read(LEDGER)
        self.tb=read(self.x["controlling_records"]["printed_images"])
        self.ue=read(self.x["controlling_records"]["forward_correction"])
    def test_image_locus_control_and_no_same_pdf_vote(self):
        controls={r["id"]:r["loci"] for r in self.tb["corrected_direct_image_loci"]}
        surfaces=self.x["source_surfaces"]
        self.assertEqual(len(surfaces),3)
        self.assertEqual(len({r["sha256"] for r in surfaces}),3)
        for r in surfaces:
            self.assertEqual(r["loci"],controls[r["id"]])
            self.assertFalse(r["unrepaired_1827_original"])
        self.assertEqual(self.ue["corrected_same_source_loci"],controls["XUXIU1174_2002"])
        self.assertNotEqual(self.ue["corrected_same_source_loci"],self.ue["erroneous_12ud_loci"])
        self.assertEqual(self.x["copy_independence"]["distinct_original_printing_states_positively_verified"],0)
        self.assertFalse(self.x["copy_independence"]["xuxiu_cadal_strong_image_registration"]["independent_physical_copy_proven"])
    def test_three_catalog_items_without_unrepaired_copy_vote(self):
        holdings={h["ncid"]:h for h in self.x["catalog_holding_candidates"]}
        self.assertEqual(set(holdings),{"BB18578034","BB10385966","BB23196128"})
        self.assertEqual(holdings["BB18578034"]["holding"],"B||VIb||9-1 188987L")
        self.assertEqual(holdings["BB10385966"]["holding"],"史6-2/YA/2 0181427762")
        self.assertEqual(holdings["BB23196128"]["holding"],"倉石文庫:20128:11 6403148395")
        self.assertTrue(all(not h["target_leaf_directly_examined"] and not h["unrepaired_1827_first_impression_proven"] for h in holdings.values()))
        self.assertTrue(self.x["institutional_access_check"]["kyoto_archive_is_general_portal_not_bound_target_iiif"])
    def test_no_count_or_runtime_change(self):
        st=read("docs/PROJECT-CURRENT-STATE-R1.json")
        self.assertTrue(any(t.startswith("12UF ") for t in st["historical_audit"]["current_focus"]))
        self.assertEqual(self.x["accounting"]["new_source_records"],0)
        self.assertEqual(st["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(st["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertGreaterEqual(st["historical_audit"]["external_source_registry_total_unique_count"],678)
if __name__=="__main__":unittest.main()
