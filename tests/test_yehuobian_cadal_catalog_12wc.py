import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(path,name):
    s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
v=load("scripts/verify-yehuobian-wenzhou-cadal-series-12wc.py","wcver")
p=load("scripts/probe-yehuobian-cadal-duplicate-alias-12wc.py","wcprobe")
class PublicationAndAlias(unittest.TestCase):
    def setUp(self):
        self.r=json.loads((ROOT/v.REC).read_text());self.s=json.loads((ROOT/v.SHARD).read_text())
        self.m=json.loads((ROOT/v.MAN).read_text());self.st=json.loads((ROOT/v.STATE).read_text())
    def bad(self,msg):
        with self.assertRaisesRegex(ValueError,msg):v.validate(self.r,self.s,self.m,self.st)
    def test_live_registry(self):self.assertEqual(v.verify()["ancient_1827_1869_target_glyph_votes"],0)
    def test_census_number_not_invented(self):
        self.r["official_catalogue"]["yehuobian_official_census_id"]="330000-1704-0000002";self.bad("false assigned census identifier")
    def test_legacy_book_cannot_be_firstparty_title_item(self):
        self.r["official_catalogue"]["exact_yehuobian_entry_verified"]=True;self.bad("official item firewall")
    def test_27_pairs_are_not_paper_copies(self):
        self.r["cadal_inventory"]["independent_historical_print_votes_from_uploads"]=27;self.bad("digital alias lineage")
    def test_research_cannot_preclaim_old_binary(self):
        self.r["cadal_inventory"]["old_file_original_bytes_obtained_at_research_commit"]=True;self.bad("premature source-byte assertion")
    def test_2017_official_publication_is_not_historical_glyph(self):
        self.s["sources"][0]["physical_glyph_authority"]=True;self.bad("two bibliographic-only source records")
    def test_probe_limits_and_explicit_names(self):
        self.assertEqual(p.MAX_SOURCE_BYTES,8_000_000);self.assertEqual([x["label"] for x in p.ITEMS],["old","new"])
    def test_probe_disallows_url_host_escape(self):
        with self.assertRaisesRegex(ValueError,"unexpected source host"):p.check_url("https://evil.example/x","upload.wikimedia.org","/wikipedia/commons/")
        with self.assertRaisesRegex(ValueError,"unexpected source host"):p.check_url("http://upload.wikimedia.org/wikipedia/commons/a","upload.wikimedia.org","/wikipedia/commons/")
    def test_scoped_ocr_free_pixel_relation_only(self):
        a={"preview_256x384":[1,2,3],"raw_grayscale_pixel_sha256":"a","dimensions":[2,1]}
        b={"preview_256x384":[1,2,3],"raw_grayscale_pixel_sha256":"a","dimensions":[2,1]}
        result=p.compare_pages(a,b)
        self.assertTrue(result["same_exact_decoded_grayscale_pixels"])
        self.assertEqual(result["historical_original_paper_or_impression_identity"],"UNBOUND")
    def test_old_original_not_missing_when_no_matching_page(self):
        self.assertEqual(p.compare_pages(None,None)["comparison"],"PAGE_OUT_OF_RANGE_NO_ABSENCE_CLAIM")
if __name__=="__main__":unittest.main()
