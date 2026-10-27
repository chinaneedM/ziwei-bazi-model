"""12RE cross-batch checks must fail closed on fake continuity, hashes and evidence promotion."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/verify_yehuobian_nlc_f1_crossbatch_native_12re.py"
SPEC = importlib.util.spec_from_file_location("tianwen_12re_gate", SCRIPT)
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


class TestNlcOld20F1CrossBatch12RE(unittest.TestCase):
    def test_real_f1_cross_batch_partition(self):
        result = GATE.verify()
        self.assertEqual(result["fascicle1_native_visual_pages"], 117)
        self.assertEqual((result["crossbatch_gaps"], result["crossbatch_overlaps"]), (0, 0))
        self.assertEqual(result["remaining_native_body_screen_queue"], 882)
        self.assertEqual(result["remaining_full_text_body_collation"], 1027)
        self.assertEqual(result["next_fascicle2_native_pages"], 72)

    def _mutate_manifest(self, change):
        value = copy.deepcopy(GATE._read(GATE.RECORD))
        change(value)
        with tempfile.TemporaryDirectory() as dirname:
            fp = Path(dirname) / "manifest.json"
            fp.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                GATE.verify(record_path=fp)

    def test_overlapping_scope_fails(self):
        self._mutate_manifest(lambda x: x["windows"][1].__setitem__("first_page", 22))

    def test_aggregate_source_pages_alias_is_exact(self):
        self._mutate_manifest(lambda x: x["source_identity"].__setitem__("source_pages", 120))

    def test_wrong_archive_does_not_merge_holding(self):
        self._mutate_manifest(lambda x: x["source_identity"].__setitem__("artifact_id", 0))

    def test_rehashed_pdf_claim_disallowed(self):
        self._mutate_manifest(lambda x: x["claims"].__setitem__("source_pdf_binary_rehashed_in_12re", True))

    def test_whole_work_absence_promotion_disallowed(self):
        self._mutate_manifest(lambda x: x["claims"].__setitem__("whole_work_target_absence_proven", True))

    def test_false_full_text_completion_disallowed(self):
        self._mutate_manifest(lambda x: x["review_accounting"].__setitem__("whole_body_full_text_collation_backlog", 0))

    def test_second_fascicle_unverified_advance_disallowed(self):
        self._mutate_manifest(lambda x: x["review_accounting"].__setitem__("second_fascicle_native_target_review_pages_pending", 0))

    def test_changed_page_jpeg_hash_fails(self):
        source = copy.deepcopy(GATE._read(GATE.ROOT / GATE._read(GATE.RECORD)["windows"][2]["path"]))
        source["review"]["source_image_sha256_by_pdf_page"][5] = "0" * 64
        with tempfile.TemporaryDirectory() as dirname:
            fp = Path(dirname) / "source.json"
            fp.write_text(json.dumps(source, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                GATE.verify(replacement_sources={"12RB": fp})

    def test_transmission_witness_inflation_disallowed(self):
        self._mutate_manifest(lambda x: x["claims"].__setitem__("new_physical_copies", 1))


if __name__ == "__main__":
    unittest.main()
