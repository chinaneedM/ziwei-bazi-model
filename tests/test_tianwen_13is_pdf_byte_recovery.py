import copy
import importlib.util
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT/"scripts"/filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


M = load_module("recovery13is", "verify-tianwen-13is-pdf-byte-recovery.py")
IR = load_module("active13ir", "verify-tianwen-13ir-active-field-control.py")


class JournalByteRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.e = M.read()

    def test_source_recovery_preserves_old_null_snapshot(self):
        self.assertTrue(M.check(self.e))

    def test_hash_is_exact_source_binding(self):
        self.e["journal_byte_recovery"]["raw_pdf_sha256"] = "0"*64
        with self.assertRaises(AssertionError):
            M.check(self.e)

    def test_missing_font_program_cannot_become_full_glyph_proof(self):
        self.e["page100_replay"]["original_CJK_glyphs_exhaustively_verified"] = True
        with self.assertRaises(AssertionError):
            M.check(self.e)

    def test_modern_article_does_not_restore_ancient_table(self):
        self.e["scope"]["GK3467_table_start_recovered"] = True
        with self.assertRaises(AssertionError):
            M.check(self.e)

    def test_failed_page_response_is_not_new_original_image(self):
        self.e["gk3467_front_retry"]["new_original_images"] = 1
        with self.assertRaises(AssertionError):
            M.check(self.e)

    def test_missing_history_is_rejected(self):
        ledger = M.read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
        issue = next(i for i in ledger["issues"] if i["id"] == "TW-OPEN-0005")
        issue["history"] = [h for h in issue["history"] if not h.get("revision_id", "").startswith("TW-OPEN-0005-13IS-")]
        with self.assertRaises(AssertionError):
            M.check(self.e, ledger=ledger)

    def test_wrong_file_cannot_satisfy_pdf_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"wrong.pdf"
            path.write_bytes(b"%PDF-fabricated")
            with self.assertRaises(AssertionError):
                M.replay_pdf(path,self.e)

    def test_content_stream_tampering_fails(self):
        self.e["page100_replay"]["content_streams"][0]["sha256"] = "0"*64
        with self.assertRaises(AssertionError):
            M.check(self.e)

    def future_handoff(self):
        state = M.read("docs/PROJECT-CURRENT-STATE-R1.json")
        ledger = M.read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
        state["schema_version"] = "1.999.0"
        state["historical_audit"]["current_focus"].append("FUTURE genuine original page review")
        state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] = "1.999.0"
        ledger["binding"].update(reviewed_state_version="1.999.0", source_focus_count=len(state["historical_audit"]["current_focus"]),latest_research_focus_prefix="FUTURE")
        ledger["checkpoint_log"][-1]["state_version"] = "1.999.0"
        issue = next(i for i in ledger["issues"] if i["id"] == "TW-OPEN-0005")
        issue["next_action"] = "FUTURE CURRENT ACTION: " + issue["next_action"].split(": ",1)[1]
        return state, ledger, issue

    def test_active_controls_accept_a_later_batch_prefix(self):
        state, ledger, issue = self.future_handoff()
        e = IR.load()
        with patch.object(IR,"load", side_effect=lambda path: state if path.endswith("PROJECT-CURRENT-STATE-R1.json") else ledger):
            self.assertTrue(IR.check(e))

    def test_later_prefix_does_not_relax_live_original_controls(self):
        state, ledger, issue = self.future_handoff()
        e = IR.load()
        e["source_controls"][0]["value"] = "FABRICATED_ANCIENT_D30"
        with patch.object(IR,"load", side_effect=lambda path: state if path.endswith("PROJECT-CURRENT-STATE-R1.json") else ledger):
            with self.assertRaises(AssertionError):
                IR.check(e)


if __name__ == "__main__":
    unittest.main()
