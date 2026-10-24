"""Direct digital identity must not silently upgrade numeric or edition evidence."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = "docs/research/TIANWEN-13FP-GK03467-04-BOOK6-JUAN52-DIRECT-SURROGATE-BINDING-R1.json"


class DirectBook6Binding(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = json.loads((ROOT / EVIDENCE).read_text())

    def test_archived_null_evidence_preserved(self):
        self.assertEqual(hashlib.sha256((ROOT / self.e["prior_record"]).read_bytes()).hexdigest(), self.e["prior_record_sha256"])

    def test_source_emitted_subgroup_volume_lists(self):
        files = {f["name"]: f for f in self.e["source_archive"]["files"]}
        for code, count in (("GK03467_02", 5), ("GK03467_04", 1)):
            name = code + "-volumes.json"
            raw = (ROOT / "docs/research/evidence/tianwen-13fp" / name).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), files[name]["sha256"])
            data = json.loads(raw)
            self.assertEqual(data["RESULT"], "SUCCESS")
            self.assertEqual([v["VOL_NO"] for v in data["volList"]], [f"{i:04d}" for i in range(1, count + 1)])
            self.assertTrue(all(v["IS_PDF"] == "Y" and v["BOOK_CD"] == code for v in data["volList"]))

    def test_cover_and_inner_title_bind_same_item(self):
        d = self.e["direct_visual_observations"]
        self.assertEqual(d["color_cover"]["label_shelfmark"], "3467의4")
        self.assertEqual(d["color_cover"]["label_within_set_book_number"], 6)
        self.assertEqual(d["microfilm_pdf"]["page1_cover_label_book"], 6)
        self.assertEqual(d["microfilm_pdf"]["page2_inner_title"], "高麗史五十二")
        self.assertEqual(d["microfilm_pdf"]["pages"], 53)
        self.assertEqual(d["control_pdf"]["page1_cover_label_book"], 26)
        self.assertFalse(d["complete_line_by_line_collation"])
        self.assertFalse(d["target_D5_numeric_lane_read"])

    def test_original_archive_identity(self):
        archive = self.e["source_archive"]
        self.assertEqual(archive["library_file_id"], "libfile_7fc9b9153f2c819197120d2599298d57")
        pdf = next(f for f in archive["files"] if f["name"] == "GK03467_04_0001.pdf")
        self.assertEqual(pdf["bytes"], 12898627)
        self.assertEqual(pdf["sha256"], "b75009805dae9ccc22797c005bd5f32c7870a192945b503f6b3af3fbf14e1386")

    def test_no_numeric_winner_or_unproved_copy_identity(self):
        a = self.e["adjudication"]
        for key in ("authenticated_impression_date", "independence_from_NIKH_GK5553_physical_copy", "NIKH_GK5553_juan52_book_and_folio", "D5_winner", "NLC_D9", "historic_D1_D2_D3_D4_D5_D6_D30_units"):
            self.assertIsNone(a[key])
        self.assertEqual(a["G893_six_original_controls"], "OPEN")
        self.assertEqual(a["fourfen_to_chudu_bridge"], "UNPROVEN")
        self.assertEqual(a["13EI"], "RETRACTED")
        for key in ("new_source_registry_records", "new_numeric_target_glyphs", "new_independent_ancient_witness_votes", "algorithm_reopens", "candidate_collapses"):
            self.assertEqual(self.e["impact"][key], 0)

    def test_forward_revision_and_continuity(self):
        state = json.loads((ROOT / "docs/PROJECT-CURRENT-STATE-R1.json").read_text())
        ledger = json.loads((ROOT / "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text())
        self.assertEqual(state["schema_version"], ledger["binding"]["reviewed_state_version"])
        issue = next(i for i in ledger["issues"] if i["id"] == "TW-OPEN-0005")
        self.assertEqual(issue["status"], "OPEN")
        self.assertIn(EVIDENCE, issue["source_refs"])
        self.assertTrue(any(h.get("revision_id") == "TW-OPEN-0005-13FP-DIRECT-GK03467-04-BOOK6-JUAN52-20261024" for h in issue["history"]))


if __name__ == "__main__":
    unittest.main()
