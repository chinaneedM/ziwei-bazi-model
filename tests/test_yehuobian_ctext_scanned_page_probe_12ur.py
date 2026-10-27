"""12UR tests for source-bound OCR vs historical printed folio."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/"scripts/probe-yehuobian-ctext-scanned-book-12ur.py"
s=importlib.util.spec_from_file_location("probe12ur",path)
mod=importlib.util.module_from_spec(s);s.loader.exec_module(mod)
DOC=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12UR-CTEXT-SCAN-PAGE-IDENTITY-PROBE-R1.json"
class CText12UR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=json.loads(DOC.read_text(encoding="utf-8"))
    def test_exact_public_known_urls_not_scanned_pages(self):
        self.assertEqual(mod.validate_ledger(self.doc)["known_urls"],2)
        self.assertEqual(self.doc["chapter_image_page_locator"],"UNBOUND")
        self.assertIsNone(self.doc["first_party_original_image_page_sha256"])
    def test_ocr_does_not_authorize_glyph_vote(self):
        self.assertFalse(self.doc["historical_glyph_vote"])
        self.assertFalse(self.doc["algorithm_reopen_authorized"])
        self.assertEqual(self.doc["outcome"]["new_target_page_glyph_votes"],0)
    def test_parser_allows_only_exact_first_party_host(self):
        html='<a href="/wiki.pl?if=en&file=123">Image</a><a href="https://evil.example/scan/xx">bad</a><a href="/wiki.pl?chapter=42">unrelated</a>'
        result=mod.extract_links(html,"https://ctext.org/wiki.pl?res=1")
        self.assertEqual(result,["https://ctext.org/wiki.pl?if=en&file=123"])
    def test_no_unrelated_image_destination_accepted(self):
        self.assertIsNone(mod.public_image_link("http://ctext.org/images/foo.png","https://ctext.org"))
        self.assertIsNone(mod.public_image_link("https://ctext.org.evil.example/scan","https://ctext.org"))
    def test_distinct_endpoints_with_identical_html_are_not_verified(self):
        a={"requested_url":"https://ctext.org/wiki.pl?if=en&res=1946940","outcome":"PUBLIC_HTML_NO_IMAGE_LINKS","http_status":200,"body_sha256":"4f323319db2cfd81d5d8106ab0f3cdbf21aaf8a17f2d187347961c569bbc1d73","found_source_emitted_links":[]}
        b={"requested_url":"https://ctext.org/wiki.pl?chapter=418967&if=gb","outcome":"PUBLIC_HTML_NO_IMAGE_LINKS","http_status":200,"body_sha256":a["body_sha256"],"found_source_emitted_links":[]}
        rows=mod.crosscheck_distinct_urls([a,b])
        self.assertEqual([x["outcome"] for x in rows],["AMBIGUOUS_IDENTICAL_HTML_SHELL"]*2)
        self.assertTrue(all(x["source_item_identity_proven"] is False for x in rows))
    def test_different_html_hashes_do_not_prove_a_scanned_folio_either(self):
        a={"requested_url":"https://ctext.org/wiki.pl?if=en&res=1946940","outcome":"PUBLIC_HTML_NO_IMAGE_LINKS","http_status":200,"body_sha256":"1"*64}
        b={"requested_url":"https://ctext.org/wiki.pl?chapter=418967&if=gb","outcome":"PUBLIC_HTML_NO_IMAGE_LINKS","http_status":200,"body_sha256":"2"*64}
        self.assertTrue(all(x["source_item_identity_proven"] is False for x in mod.crosscheck_distinct_urls([a,b])))
    def test_berlin_sample_already_accounted_for(self):
        b=self.doc["prior_exhausted_german_example_source"]
        self.assertEqual(b["total_public_sample_canvases"],38)
        self.assertTrue(b["historical_12pz_38_of_38_image_examined"])
        self.assertFalse(b["entire_1827_print_juan20_excluded"])
    def test_project_counters_unchanged(self):
        s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))
        self.assertEqual(self.doc["accounting"]["total_sources"],687)
        self.assertEqual(self.doc["accounting"]["root_sources"]+self.doc["accounting"]["extension_sources"],687)
        self.assertGreaterEqual(s["historical_audit"]["external_source_registry_total_unique_count"],self.doc["accounting"]["total_sources"])
        self.assertEqual(len(s["historical_audit"]["completed_batches"]),487)
        self.assertEqual(s["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(s["invariants"]["algorithm_reopen_count"],0)
        self.assertTrue(any(v.startswith("12UR ") for v in s["historical_audit"]["current_focus"]))
if __name__=="__main__":
    unittest.main()
