"""12RI protects F2 p41–60 native bounded visual evidence without target absence proof."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("tw12ri", ROOT/"scripts/verify_yehuobian_nlc_f2_p41_60_native_12ri.py")
G=importlib.util.module_from_spec(S)
S.loader.exec_module(G)

class TestNlcF2P41To60(unittest.TestCase):
    def mutation(self,f):
        rec=copy.deepcopy(G.read(G.RECORD))
        f(rec)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"changed.json"
            p.write_text(json.dumps(rec,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):
                G.verify(record_path=p)

    def test_positive_source_chain(self):
        result=G.verify()
        self.assertEqual(result["fascicle2_native_screened"],60)
        self.assertEqual(result["fascicle2_native_remaining"],12)
        self.assertEqual(result["native_source_bounded_screens"],206)
        self.assertEqual(result["preview_only_remaining"],822)
        self.assertEqual(result["whole_body_full_text_collation_remaining"],1027)
        self.assertFalse(result["new_target_glyph_or_absence_proof"])
    def test_page_source_sha_pin(self):
        self.mutation(lambda r:r["review"]["source_jpeg_sha256_in_pdf_order"].__setitem__(7,"0"*64))
    def test_source_pdf_hash_pin(self):
        self.mutation(lambda r:r["source"].__setitem__("source_pdf_sha256","0"*64))
    def test_scope_start(self):
        self.mutation(lambda r:r["review"].__setitem__("first_pdf_page",40))
    def test_chain_digest(self):
        self.mutation(lambda r:r["review"].__setitem__("sha256_fascicle2_pages1_60_chain","0"*64))
    def test_absence_claim(self):
        self.mutation(lambda r:r["review"].__setitem__("whole_manuscript_absence_proven",True))
    def test_no_full_text_promotion(self):
        self.mutation(lambda r:r["review"].__setitem__("complete_text_transcription_performed",True))
    def test_pending_native_backlog(self):
        self.mutation(lambda r:r["queue"].__setitem__("fascicle2_remaining_native_target_screens",0))
    def test_no_extra_witness(self):
        self.mutation(lambda r:r["queue"].__setitem__("new_physical_copy_count",1))
if __name__=="__main__":
    unittest.main()
