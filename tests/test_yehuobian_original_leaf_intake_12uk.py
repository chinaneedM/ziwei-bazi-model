"""12UK: test original-folio intake without certifying catalog leads as witnesses."""
from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/verify-yehuobian-original-leaf-intake-r1.py"
QUEUE = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12UK-ORIGINAL-LEAF-INTAKE-QUEUE-R1.json"
CONTROL = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12UF-SOURCE-READING-CONTROL-AND-IMPRESSION-GATES-R1.json"
spec = importlib.util.spec_from_file_location("yehuobian_12uk", SCRIPT)
ingest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ingest)

def fixtures():
    return json.loads(QUEUE.read_text(encoding="utf-8")), json.loads(CONTROL.read_text(encoding="utf-8"))

class Intake12UK(unittest.TestCase):
    def test_live_queue_has_six_unverified_objects_and_no_votes(self):
        q, control = fixtures()
        result = ingest.validate(q, control)
        self.assertEqual((result["candidate_count"], result["captured_images"], result["independent_ancient_glyph_votes"]), (6, 0, 0))
        self.assertEqual(result["historical_control_surfaces"], 3)
        self.assertEqual({x["id"] for x in q["candidates"]}, {
            "KYOTO_1827_188987L", "HOKKAIDO_1827_0181427762",
            "TOKYO_1869_6403148395", "TSUKUBA_V20_10076865665",
            "NDL_18465", "NAJ_3080212"})
        st = json.loads((ROOT / "docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))
        self.assertTrue(any(x.startswith("12UK ") for x in st["historical_audit"]["current_focus"]))
        self.assertEqual(st["invariants"]["deterministic_fusion_chart_product_r1"], "CLOSED")
        self.assertEqual(st["invariants"]["algorithm_reopen_count"], 0)

    def test_no_vote_without_adjudication(self):
        q, c = fixtures()
        q["candidates"][0]["historical_vote"] = True
        with self.assertRaisesRegex(ValueError, "cannot claim"):
            ingest.validate(q, c)

    def test_plan_cannot_prepopulate_glyph(self):
        q, c = fixtures()
        q["candidates"][-1]["four_locus_readings"]["GONGJIN"] = "宮禁"
        with self.assertRaisesRegex(ValueError, "catalog/plan"):
            ingest.validate(q, c)

    def test_bad_image_hash(self):
        q, c = fixtures()
        item = q["candidates"][0]
        item.update(stage="IMAGE_CAPTURED", source_binary_sha256="bad", source_issued_image_url="https://example.org/scan",
                    pages=[{"page_label": "p10", "sha256": "1" * 64}],
                    target_original_folio="卷20第10葉", relationship_to_prior_surfaces="DISTINCT_BYTES_RELATION_UNRESOLVED")
        with self.assertRaisesRegex(ValueError, "source-issued URL"):
            ingest.validate(q, c)

    def test_duplicate_prior_binary_not_independent_witness(self):
        q, c = fixtures()
        item = q["candidates"][0]
        item.update(stage="IMAGE_CAPTURED", source_binary_sha256=c["source_surfaces"][0]["sha256"],
                    source_issued_image_url="https://example.org/scan", pages=[{"page_label": "p10", "sha256": "1" * 64}],
                    target_original_folio="卷20第10葉", relationship_to_prior_surfaces="DISTINCT_BYTES_RELATION_UNRESOLVED")
        with self.assertRaisesRegex(ValueError, "known control binary"):
            ingest.validate(q, c)

    def test_capture_remains_zero_vote(self):
        q, c = fixtures()
        item = q["candidates"][0]
        item.update(stage="IMAGE_CAPTURED", source_binary_sha256="d" * 64,
                    source_issued_image_url="https://example.org/scan", pages=[{"page_label": "p10", "sha256": "1" * 64}],
                    target_original_folio="卷20第10葉", relationship_to_prior_surfaces="DISTINCT_BYTES_RELATION_UNRESOLVED")
        outcome = ingest.validate(q, c)
        self.assertEqual(outcome["captured_images"], 1)
        self.assertEqual(outcome["independent_ancient_glyph_votes"], 0)

    def test_print_claim_needs_image_bound_paratext(self):
        q, c = fixtures()
        item = q["candidates"][0]
        item.update(stage="PRINT_STATE_CANDIDATE", source_binary_sha256="d" * 64,
                    source_issued_image_url="https://example.org/scan", pages=[{"page_label": "p10", "sha256": "1" * 64}],
                    target_original_folio="卷20第10葉", relationship_to_prior_surfaces="DISTINCT_BYTES_RELATION_UNRESOLVED",
                    printing_state_evidence={"source_page_sha256": "e" * 64, "adjudication": "MANUAL_REVIEW_PENDING",
                                             "dated_paratext_quotation": ""})
        with self.assertRaisesRegex(ValueError, "paratext"):
            ingest.validate(q, c)

    def test_early_chronological20_not_the_same_juan20(self):
        q, c = fixtures()
        q["candidates"][0]["historical_volume_arrangement"] = "CHRONOLOGICAL_20"
        with self.assertRaisesRegex(ValueError, "cannot be equated"):
            ingest.validate(q, c)

    def test_duplicate_object_identifiers(self):
        q, c = fixtures()
        q["candidates"][1]["id"] = q["candidates"][0]["id"]
        with self.assertRaisesRegex(ValueError, "duplicate"):
            ingest.validate(q, c)

if __name__ == "__main__":
    unittest.main()
