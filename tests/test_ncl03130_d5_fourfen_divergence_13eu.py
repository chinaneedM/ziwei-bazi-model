import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-d5-fourfen-krdb-divergence-13eu.py"
s=importlib.util.spec_from_file_location("q13eu",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test13EU(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=v.load(v.P);cls.en=v.load(v.EN);cls.et=v.load(v.ET);cls.st=v.load(v.S);cls.l=v.load(v.L)
    def good(self,x=None):return v.verify(self.a if x is None else x,self.en,self.et,self.st,self.l)
    def reject(self,f):
        x=copy.deepcopy(self.a);f(x)
        with self.assertRaises(AssertionError):self.good(x)
    def test_valid(self):self.assertTrue(self.good())
    def test_rolling_next_action_may_abbreviate_13eu_glyphs(self):
        l=copy.deepcopy(self.l)
        issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
        issue["next_action"]=issue["next_action"].replace("四分〇一七二","D5_NCL_ROI").replace("四分五一七二","D5_KRDB_TEXT")
        self.assertNotIn("四分〇一七二",issue["next_action"])
        self.assertNotIn("四分五一七二",issue["next_action"])
        self.assertTrue(v.verify(self.a,self.en,self.et,self.st,l))
    def test_prior_glyph_record_cannot_disappear(self):
        l=copy.deepcopy(self.l);issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
        issue["history"]=[z for z in issue["history"] if z.get("revision_id")!="TW-OPEN-0005-13EU-LEGACY-D1D6-GUARD-20261024"]
        with self.assertRaises((AssertionError,StopIteration)):
            v.verify(self.a,self.en,self.et,self.st,l)
    def test_prior_glyph_record_cannot_be_corrupted(self):
        l=copy.deepcopy(self.l);issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
        archival=next(z for z in issue["history"] if z.get("revision_id")=="TW-OPEN-0005-13EU-LEGACY-D1D6-GUARD-20261024")
        archival["previous_next_action"]=archival["previous_next_action"].replace("四分〇一七二","四分五一七二")
        with self.assertRaises(AssertionError):
            v.verify(self.a,self.en,self.et,self.st,l)
    def test_primary_character_crop(self):self.reject(lambda x:x["ncl_original"]["positive_d5_digit_roi"].update(rgb_sha256="0"*64))
    def test_rewrite_source_original(self):self.reject(lambda x:x["ncl_original"].update(previous_image_reading="四分五一七二"))
    def test_reverse_db_reading(self):self.reject(lambda x:x["krdb_original_text"]["adjacent_daily_original_text_transcriptions"][1].update(original_transcription="四分〇一七二"))
    def test_fake_independent_witness(self):self.reject(lambda x:x["limits"].update(krdb_o_not_second_original_witness=False))
    def test_fake_edition_variant(self):self.reject(lambda x:x["alignment_candidate"].update(confirmed_historical_edition_variant=True))
    def test_fake_krdb_error(self):self.reject(lambda x:x["alignment_candidate"].update(confirmed_krdb_transcription_error=True))
    def test_silent_decimal(self):self.reject(lambda x:x["alignment_candidate"].update(normalized_digit_for_algorithm=5))
    def test_reopen_algorithm(self):self.reject(lambda x:x["impact"].update(algorithm_reopened=1))
    def test_wrong_field(self):self.reject(lambda x:x["krdb_original_text"].update(column_label="行度"))
    def test_retired_claim_restored(self):self.reject(lambda x:x["limits"].update(retired_claim_restored=True))
if __name__=="__main__":unittest.main()
