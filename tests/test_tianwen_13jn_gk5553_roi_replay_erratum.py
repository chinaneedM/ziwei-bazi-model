"""13JN: preserve bad 13JM ROI metadata and fail closed on replay authority."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / "docs/research/TIANWEN-13JM-GK5553-8-26-MANUSCRIPT-NEIGHBOR-SIX-ORIGINAL-IMAGE-SCOPE-R1.json"
ERRATUM = ROOT / "docs/research/TIANWEN-13JN-GK5553-13JM-ROI-REPLAY-ERRATUM-R1.json"
STATE = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER = ROOT / "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"

class ForwardOnlyRoiReplayErratum(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        prior_bytes = PRIOR.read_bytes()
        cls.prior_sha1 = hashlib.sha1(
            ("blob %d" % len(prior_bytes)).encode("ascii") + bytes([0]) + prior_bytes
        ).hexdigest()
        cls.prior = json.loads(prior_bytes)
        cls.erratum = json.loads(ERRATUM.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE.read_text(encoding="utf-8"))
        cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

    @staticmethod
    def valid_crop(crop, dims):
        xy = crop.get("xyxy")
        h = crop.get("sha256")
        return (isinstance(xy, list) and len(xy) == 4
                and all(type(v) is int for v in xy)
                and 0 <= xy[0] < xy[2] <= dims[0]
                and 0 <= xy[1] < xy[3] <= dims[1]
                and isinstance(h, str) and len(h) == 64
                and all(ch in "0123456789abcdef" for ch in h))

    def test_immutable_prior_image_manifest(self):
        self.assertEqual(self.prior_sha1, "40d242fcffc8c45b66961b71d85fb0a8f306ada0")
        self.assertEqual(self.erratum["prior_evidence_git_blob_sha1"], self.prior_sha1)

    def test_prior_twelve_crops_not_replayable(self):
        bad = [(p["digital_volume"], roi["name"]) for p in self.prior["pages"]
               for roi in p["native_rgb_rois"] if not self.valid_crop(roi, p["pixel_dimensions"])]
        self.assertEqual(len(self.prior["pages"]), 6)
        self.assertEqual(len(bad), 12)
        self.assertEqual(len(self.erratum["invalid_roi_details"]), 12)
        self.assertEqual({v for v, _ in bad},
                         {"0008", "0026", "0011", "0013", "0025", "0027"})
        self.assertTrue(all(not x["geometry_well_typed_and_bounded"] or not x["sha256_well_formed"]
                            for x in self.erratum["invalid_roi_details"]))

    def test_evidence_grade_firewall(self):
        scope = self.erratum["scope"]
        self.assertEqual(scope["new_recomputed_crop_digest_awards"], 0)
        self.assertEqual(scope["independent_physical_copy_votes_added"], 0)
        self.assertEqual(scope["algorithm_reopens"], 0)
        self.assertEqual(scope["chart_product"], "CLOSED")
        self.assertEqual(self.erratum["transmission_impact"], "NONE_EVIDENCE_REPLAY_GRADE_CORRECTION_ONLY")

    def test_state_and_issue_forward_only(self):
        self.assertEqual(self.state["schema_version"], "1.913.0")
        self.assertEqual(self.ledger["binding"]["reviewed_state_version"], self.state["schema_version"])
        self.assertEqual(self.ledger["binding"]["latest_research_focus_prefix"], "13JP")
        self.assertTrue(any(x.startswith("13JN ") for x in self.state["historical_audit"]["current_focus"]))
        self.assertTrue(any(x.startswith("13JO ") for x in self.state["historical_audit"]["current_focus"]))
        self.assertTrue(self.state["historical_audit"]["current_focus"][-1].startswith("13JP "))
        self.assertEqual(self.ledger["binding"]["source_focus_count"],
                         len(self.state["historical_audit"]["current_focus"]))
        issue = next(x for x in self.ledger["issues"] if x["id"] == "TW-OPEN-0005")
        self.assertEqual((issue["status"], issue["priority"]), ("OPEN", "P0"))
        self.assertIn("docs/research/TIANWEN-13JN-GK5553-13JM-ROI-REPLAY-ERRATUM-R1.json", issue["source_refs"])
        self.assertIn("13JM CURRENT ACTION:", issue["next_action"])
        self.assertIn("13JN CURRENT ACTION:", issue["next_action"])
        self.assertTrue(any(x.get("revision_id", "").startswith("TW-OPEN-0005-13JN")
                            for x in issue["history"]))
        self.assertEqual(self.ledger["checkpoint_log"][-1]["state_version"], "1.913.0")

if __name__ == "__main__":
    unittest.main()
