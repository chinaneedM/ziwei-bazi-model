"""12QQ provenance-safe queue regression tests for source-bound manuscript review."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/yehuobian_nlc_scoped_manual_review_queue_12qq.py"
spec = importlib.util.spec_from_file_location("nlc_review_12qq", SCRIPT)
queue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(queue)

class Test12QQScopedReviewQueue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = queue.build_rows()
        cls.pages = {(r["fascicle"], r["pdf_page"]): r for r in cls.rows}

    def test_complete_queue_and_no_global_negative_claims(self):
        summary = queue.summary(self.rows)
        self.assertEqual(summary["source_pages"], 1030)
        self.assertEqual(summary["remaining_target_body_review_queue"], 1019)
        self.assertEqual(summary["prior_nine_page_bounded_target_checks"], 9)
        self.assertEqual(summary["eligible_prior_bounded_checked_pages"], 8)
        self.assertFalse(summary["entire_manuscript_target_absence_proven"])
        for r in self.rows:
            self.assertFalse(r["entire_manuscript_target_absence_proven"])
            self.assertEqual(r["physical_witness_increment"], 0)

    def test_context_page136_not_target_checked_and_colophon_not_body(self):
        self.assertTrue(self.pages[10,136]["needs_target_image_review"])
        for p in range(137, 146):
            r = self.pages[10,p]
            self.assertEqual(r["target_review_status"], "PRIOR_NINE_PAGE_BOUNDED_CHECK")
            self.assertEqual(len(r["page_jpeg_sha256_if_known"]), 64)
        self.assertFalse(self.pages[10,145]["body_search_eligible"])
        self.assertFalse(self.pages[1,1]["body_search_eligible"])
        self.assertFalse(self.pages[1,2]["body_search_eligible"])
        self.assertTrue(self.pages[1,3]["needs_target_image_review"])
        self.assertEqual(self.pages[10,137]["page_scope"], "TWO_LEAF_CROSS_VOLUME_BOUNDARY")

    def test_mixed_leaves_retained_on_all_eight_original_volume_transitions(self):
        examples = [(1,35,1,2), (1,88,3,4), (3,83,6,7), (4,35,8,9),
                    (7,68,13,14), (9,84,16,17), (10,81,18,19), (10,137,19,20)]
        for f,p,right,left in examples:
            with self.subTest(f=f,p=p):
                r = self.pages[f,p]
                self.assertEqual(r["original_volume_candidates"], [right,left])
                self.assertEqual(r["cross_volume_leaf_ownership"], {"right":right, "left":left})
                self.assertEqual(len(r["source_pdf_sha256"]), 64)

    def test_mutated_manual_source_scope_fails_closed(self):
        loc = queue.load_locator()
        sources, spans = loc.load_index()
        original = json.loads(queue.REVIEW.read_text(encoding="utf-8"))
        mutations = [
            ("source", "source_pdf_sha256", "0"*64),
            ("direct_page_review", "target_not_in_any_other_old20_volume", "ABSENT"),
            ("direct_page_review", "entire_original_20_volume_work_negatively_searched", True),
            ("direct_page_review", "preceding_context_pdf_page", 137),
        ]
        for section,key,value in mutations:
            with self.subTest(key=key), tempfile.TemporaryDirectory() as d:
                modified = copy.deepcopy(original)
                modified[section][key] = value
                path = Path(d) / "changed.json"
                path.write_text(json.dumps(modified, ensure_ascii=False), encoding="utf-8")
                with self.assertRaises(ValueError):
                    queue.bounded_review(sources, spans, path)

    def test_machine_evidence_matches_replay(self):
        file = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12QQ-NLC411999003250-REVIEW-QUEUE-R1.json"
        record = json.loads(file.read_text(encoding="utf-8"))
        self.assertEqual(queue.summary(self.rows), record["computed_review_queue"])
        self.assertFalse(record["scope"]["new_original_target_folio_seen"])
        self.assertFalse(record["scope"]["entire_work_absence_proven"])

if __name__ == "__main__":
    unittest.main()
