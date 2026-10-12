import json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RECORD="docs/research/MING-DATONG-YEHUOBIAN-12TA-CROSS-IMAGE-THREE-KE-FOUR-LOCUS-MATRIX-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"

def load(name): return json.loads((ROOT/name).read_text(encoding="utf-8"))

class ThreeKeCrossImageMatrix12TA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=load(RECORD)
        cls.state=load(STATE)
        cls.cadal=load(cls.r["exact_sources"]["cadal"])
        cls.xuxiu=load(cls.r["exact_sources"]["xuxiu"])

    def test_cadal_three_ke_inherited_from_direct_record(self):
        source={x["field"]:x["reading"] for x in self.cadal["target"]["field_collation"]}
        self.assertEqual(source["BEIJING_WINTER_SUNRISE"],"辰初二刻")
        self.assertEqual(source["BEIJING_SUMMER_SUNSET"],"戌初三刻")
        row=next(x for x in self.r["witnessed_readings"] if x["id"]=="CADAL02096915")
        self.assertEqual(row["loci"],["宮禁","宮漏","辰初二刻","戌初三刻"])
        self.assertFalse(row["proven_1827_unrepaired"])

    def test_1174_direct_read_not_overwritten(self):
        target={x["id"]:x["reading"] for x in self.xuxiu["directly_read_four_loci"]}
        row=next(x for x in self.r["witnessed_readings"] if x["id"]=="XUXIU1174_2002")
        self.assertEqual(row["loci"],[
            target["GONGJIN_WORD"],target["PALACE_CLOCK_NOUN"],
            target["BEIJING_WINTER_SUNRISE_KE"],target["BEIJING_SUMMER_SUNSET_KE"]])
        self.assertEqual(row["loci"][-1],"戌初二刻")

    def test_all_three_summer_values_remain_distinct(self):
        direct=[x for x in self.r["witnessed_readings"] if x["class"].startswith("DIRECT_DIGITAL")]
        self.assertEqual(len(direct),3)
        self.assertEqual({x["loci"][-1] for x in direct},{"戌初一刻","戌初二刻","戌初三刻"})
        self.assertEqual(self.r["derived"]["image_witnesses_without_bounded_original_print_state"],3)
        self.assertEqual(self.r["derived"]["new_independent_source_count"],0)
        self.assertEqual(self.r["derived"]["direct_stemma_edges_added"],0)

    def test_handoff_and_product_invariants(self):
        a=self.state["historical_audit"]
        self.assertTrue(any(x.startswith("12TA CROSS-IMAGE") for x in a["current_focus"]))
        self.assertEqual(a["external_source_registry_total_unique_count"],660)
        self.assertEqual(len(a["completed_batches"]),487)
        self.assertEqual(a["row_count"],222)
        self.assertEqual(a["repaired_provenance_metadata_defect_count"],45)
        self.assertEqual(self.state["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(self.state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")

if __name__=="__main__":unittest.main()
