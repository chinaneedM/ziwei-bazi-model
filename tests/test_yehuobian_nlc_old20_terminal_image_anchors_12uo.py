"""12UO: direct JPEG evidence is two scoped anchors, not target glyph evidence."""
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12UO-NLC-OLD20-TERMINAL-FOLIO-IMAGE-ANCHORS-R1.json"
PARENT=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QD-SHLIB-FIRSTPARTY-AND-NLC-OLD20-ATLAS-R1.json"
STATE=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"

class Old20Terminal12UO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(DOC.read_text(encoding="utf-8"))
        cls.p=json.loads(PARENT.read_text(encoding="utf-8"))
        cls.s=json.loads(STATE.read_text(encoding="utf-8"))

    def test_exact_artifact_source_binding(self):
        item=self.a["source_object"]
        other=self.p["nlc_old20_direct_raster_atlas"]
        self.assertEqual(item["registered_source_id"],other["source_id"])
        self.assertEqual(item["original_source_pdf_sha256_from_12qd"],other["original_pdf_sha256"])
        self.assertEqual(item["upstream_artifact_id"],other["artifact_id"])
        self.assertEqual(item["upstream_workflow_id"],other["upstream_run"])
        self.assertEqual(item["upstream_artifact_name"],other["artifact_name"])
        self.assertEqual(self.a["archive_check"]["upstream_artifact_page_atlas_entries"],145)

    def test_jpeg_hashes_64_hex_and_exact_anchor_bindings(self):
        rec={x["page"]:x["sha256"] for x in self.a["archive_check"]["rehashed_jpeg_pages"]}
        self.assertEqual(len(rec),7)
        self.assertTrue(all(isinstance(v,str) and len(v)==64 and all(k in "0123456789abcdef" for k in v) for v in rec.values()))
        self.assertEqual([x["pdf_page"] for x in self.a["direct_image_anchors"]],[1,145])
        for anchor in self.a["direct_image_anchors"]:
            self.assertEqual(anchor["page_image_sha256"],rec[anchor["pdf_page"]])

    def test_manually_scoped_exact_readings_no_old20_new30_merge(self):
        self.assertEqual(self.a["direct_image_anchors"][0]["manual_visible_text"],"萬曆野獲編卷十八")
        self.assertEqual(self.a["direct_image_anchors"][1]["manual_visible_text"],"萬曆野獲編二十卷紀事畢")
        bounds=self.a["negative_inference_firewall"]
        self.assertFalse(bounds["old_20_juan20_equal_1827_new_30_juan20"])
        self.assertFalse(bounds["gaizao_louke_target_heading_located"])
        self.assertFalse(bounds["gaizao_louke_not_present_in_this_book"])
        self.assertEqual(bounds["new_variant_locus_reads"],0)
        self.assertEqual(bounds["new_physically_distinct_source_objects"],0)

    def test_no_false_original_binary_or_entire_codex_claim(self):
        self.assertFalse(self.a["archive_check"]["full_145_page_manual_transcription"])
        self.assertFalse(self.a["archive_check"]["ocr_performed"])
        self.assertFalse(self.a["source_object"]["original_pdf_sha256_independently_rehashed_this_batch"])
        self.assertFalse(self.a["negative_inference_firewall"]["entire_145_pages_checked_for_target"])
        self.assertFalse(self.a["negative_inference_firewall"]["image_dates_original_physical_impression"])

    def test_project_counts_and_reopen_firewall(self):
        x=self.a["accounting"];h=self.s["historical_audit"]
        # 12UO source total is an immutable historical snapshot, not the live registry count.
        self.assertEqual(x["source_registry_unique"],x["source_registry_root"]+x["source_registry_extension"])
        self.assertGreaterEqual(h["external_source_registry_total_unique_count"],x["source_registry_unique"])
        self.assertEqual(x["formal_batches"],len(h["completed_batches"]))
        self.assertEqual(x["matrix_rows"],h["row_count"])
        self.assertEqual(x["matrix_audited"],h["audited_row_count"])
        self.assertEqual(x["new_external_source_records"],0)
        self.assertEqual(x["new_target_glyph_votes"],0)
        self.assertEqual(self.s["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(x["product"],"CLOSED")
        self.assertTrue(any(z.startswith("12UO ") for z in h["current_focus"]))

if __name__=="__main__":
    unittest.main()
