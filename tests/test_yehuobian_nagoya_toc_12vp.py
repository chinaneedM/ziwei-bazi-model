import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("toc12vp",ROOT/"scripts/verify-yehuobian-nagoya-toc-12vp.py")
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class TocScope(unittest.TestCase):
    def setUp(self):
        self.r=json.loads((ROOT/v.RECORD).read_text())
        self.s=json.loads((ROOT/v.SHARD).read_text())
        self.m=json.loads((ROOT/v.MANIFEST).read_text())
        self.st=json.loads((ROOT/v.STATE).read_text())
    def check_invalid(self, word):
        with self.assertRaisesRegex(ValueError, word):
            v.validate(self.r,self.s,self.m,self.st)
    def test_real_record_and_blob(self):
        self.assertEqual(v.verify()["new_ancient_glyph_votes"],0)
    def test_toc_absence_not_worldwide_absence(self):
        self.r["negative_claim"]["worldwide_no_further_publication"]=True;self.check_invalid("overbroad")
    def test_other_venues_not_checked(self):
        self.r["negative_claim"]["other_journals_checked"]=True;self.check_invalid("overbroad")
    def test_no_fulltext_universal_negative(self):
        self.r["negative_claim"]["fulltext_juan20_exhaustively_searched"]=True;self.check_invalid("overbroad")
    def test_third_installment_not_listed(self):
        self.r["searched_continuation"][2]["listed_inoue_yehuobian_koki_continuation"]=True;self.check_invalid("later TOC")
    def test_issue_range(self):
        self.r["searched_continuation"][-1]["issue"]=51;self.check_invalid("issue-year")
    def test_gloss_not_ancient_folio(self):
        self.s["sources"][0]["physical_glyph_authority"]=True;self.check_invalid("source glyph")
    def test_no_genealogy_upgrade(self):
        self.r["accounting"]["graph_edges"]=1;self.check_invalid("glyph/graph")
    def test_future_source_growth_allowed(self):
        self.m["combined_source_count"]+=1;self.m["extension_source_count"]+=1;self.st["historical_audit"]["external_source_registry_total_unique_count"]+=1
        self.assertEqual(v.validate(self.r,self.s,self.m,self.st)["status"],"PASS")
    def test_current_source_count_not_backdated(self):
        self.m["combined_source_count"]=694;self.check_invalid("must not regress")
if __name__=="__main__":unittest.main()
