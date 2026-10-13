#!/usr/bin/env python3
"""12VK: verify actual image bytes before allowing future Tokyo 1827/1869 leaf votes."""
import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "physical_12vk", ROOT / "scripts/verify-yehuobian-physical-leaf-attestation-r1.py"
)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
QUEUE = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12SM-TOKYO-TARGET-LEAF-ATTESTATION-QUEUE-R1.json"
STATE = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"


class ByteBoundLeafIntake(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = json.loads(QUEUE.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE.read_text(encoding="utf-8"))

    def positive(self, root, count=1):
        rec = copy.deepcopy(self.queue)
        for i in range(count):
            item = rec["entries"][i]
            item["digital_access"] = "ITEM_ORIGINAL_LEAF_VERIFIED"
            item["copy_image_identity_bound"] = True
            item["independent_target_glyph_vote"] = 1
            item["collated_loci"] = {
                "WINTER_BEIJING_SUNRISE": "synthetic unverified unit-test winter",
                "SUMMER_BEIJING_SUNSET": "synthetic unverified unit-test summer",
                "PRECINCT_TERM": "synthetic unit-test precinct",
                "CLOCK_TERM": "synthetic unit-test clock",
            }
            source = ("TEST SOURCE PDF " + str(i)).encode()
            page = ("TEST PAGE JPEG " + str(i)).encode()
            src_name, page_name = f"source{i}.pdf", f"page{i}.jpg"
            (root / src_name).write_bytes(source)
            (root / page_name).write_bytes(page)
            item["original_target_leaf"] = {
                "source_url": "https://example.invalid/synthetic-not-historical",
                "page": i + 1,
                "source_sha256": hashlib.sha256(source).hexdigest(),
                "page_sha256": hashlib.sha256(page).hexdigest(),
                "source_local_file": src_name,
                "page_local_file": page_name,
                "human_reviewer": "SYNTHETIC_UNIT_TEST_ONLY",
                "edition_control": "SYNTHETIC_UNIT_TEST_NO_HISTORICAL_AUTHORITY",
            }
        rec["independent_target_glyph_votes"] = count
        return rec

    def test_live_queue_zero_votes_still_passes(self):
        self.assertEqual(gate.verify(self.queue)["admitted_target_glyph_votes"], 0)
        self.assertEqual(self.state["invariants"]["algorithm_reopen_count"], 0)

    def test_positive_without_real_bytes_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            rec = self.positive(Path(td))
            with self.assertRaisesRegex(ValueError, "actual artifact root"):
                gate.verify(rec)

    def test_positive_with_actual_bytes_passes_syntactic_gate(self):
        with tempfile.TemporaryDirectory() as td:
            rec = self.positive(Path(td))
            self.assertEqual(gate.verify(rec, Path(td))["admitted_target_glyph_votes"], 1)

    def test_changed_source_bytes_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rec = self.positive(root)
            (root / "source0.pdf").write_bytes(b"FORGED DIFFERENT CONTENT")
            with self.assertRaisesRegex(ValueError, "actual file bytes sha256 mismatch"):
                gate.verify(rec, root)

    def test_changed_page_bytes_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rec = self.positive(root)
            (root / "page0.jpg").write_bytes(b"FORGED PAGE")
            with self.assertRaisesRegex(ValueError, "actual file bytes sha256 mismatch"):
                gate.verify(rec, root)

    def test_forged_well_formed_digest_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rec = self.positive(root)
            rec["entries"][0]["original_target_leaf"]["page_sha256"] = "a" * 64
            with self.assertRaisesRegex(ValueError, "actual file bytes sha256 mismatch"):
                gate.verify(rec, root)

    def test_missing_file_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rec = self.positive(root)
            (root / "page0.jpg").unlink()
            with self.assertRaises((ValueError, FileNotFoundError)):
                gate.verify(rec, root)

    def test_parent_escape_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rec = self.positive(root)
            rec["entries"][0]["original_target_leaf"]["source_local_file"] = "../other.pdf"
            with self.assertRaisesRegex(ValueError, "unsafe source/page artifact path"):
                gate.verify(rec, root)

    def test_absolute_path_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rec = self.positive(root)
            rec["entries"][0]["original_target_leaf"]["page_local_file"] = str(root / "page0.jpg")
            with self.assertRaisesRegex(ValueError, "unsafe source/page artifact path"):
                gate.verify(rec, root)

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as external:
            root = Path(td)
            rec = self.positive(root)
            file = Path(external) / "outside.pdf"
            file.write_bytes((root / "source0.pdf").read_bytes())
            (root / "source0.pdf").unlink()
            (root / "source0.pdf").symlink_to(file)
            with self.assertRaisesRegex(ValueError, "artifact path escapes root"):
                gate.verify(rec, root)

    def test_separately_hashed_two_synthetic_images(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rec = self.positive(root, 2)
            self.assertEqual(gate.verify(rec, root)["admitted_target_glyph_votes"], 2)

    def test_same_page_image_not_two_independent_votes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rec = self.positive(root, 2)
            leaf1 = rec["entries"][1]["original_target_leaf"]
            leaf0 = rec["entries"][0]["original_target_leaf"]
            (root / "page1.jpg").write_bytes((root / "page0.jpg").read_bytes())
            leaf1["page_sha256"] = leaf0["page_sha256"]
            with self.assertRaisesRegex(ValueError, "same digitized bytes"):
                gate.verify(rec, root)

    def test_same_source_binary_not_two_independent_votes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rec = self.positive(root, 2)
            leaf1 = rec["entries"][1]["original_target_leaf"]
            leaf0 = rec["entries"][0]["original_target_leaf"]
            (root / "source1.pdf").write_bytes((root / "source0.pdf").read_bytes())
            leaf1["source_sha256"] = leaf0["source_sha256"]
            with self.assertRaisesRegex(ValueError, "same digitized bytes"):
                gate.verify(rec, root)


if __name__ == "__main__":
    unittest.main()
