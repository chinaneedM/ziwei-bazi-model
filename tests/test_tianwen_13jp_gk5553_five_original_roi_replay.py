"""13JP manifest and source-byte strictness; all historical bounds stay fail-closed."""
import importlib.util
import json
import unittest
from copy import deepcopy
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13JP-GK5553-13JI-FIVE-ORIGINAL-JPEG-PIXEL-ROI-REPLAY-R1.json"
P=ROOT/"docs/research/TIANWEN-13JJ-SNU-GK5553-ORIGINAL-12-29-PHOTO-COLLATION-R1.json"
S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
SPEC=importlib.util.spec_from_file_location("thirteen_jp",ROOT/"scripts/verify-tianwen-13jp-gk5553-five-source-rois.py")
V=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)

class OriginalFivePixelReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=json.loads(E.read_text(encoding="utf-8"))
        cls.p=json.loads(P.read_text(encoding="utf-8"))
        cls.s=json.loads(S.read_text(encoding="utf-8"))
        cls.l=json.loads(L.read_text(encoding="utf-8"))
    def test_manifest_original_sha_and_ten_rois(self):
        V.verify_manifest(self.e,self.p)
        self.assertEqual(self.e["replay"]["original_jpeg_sha256_verified"],5)
        self.assertEqual(self.e["replay"]["decoded_rgb_sha256_verified"],5)
        self.assertEqual(self.e["replay"]["verified_native_pixel_roi_sha256"],10)
    def test_mutation_rejects_fake_geometry_and_witnesses(self):
        for mode in ("noninteger","hash_missing","forged_source","physical_vote"):
            x=deepcopy(self.e)
            y=x["original_images"][0]
            if mode=="noninteger":y["original_rgb_rois"][0]["xyxy"][0]="721"
            if mode=="hash_missing":y["original_rgb_rois"][0]["rgb_sha256"]="!"
            if mode=="forged_source":y["jpeg_sha256"]="a"*64
            if mode=="physical_vote":x["replay"]["new_independent_physical_witness_count"]=1
            with self.subTest(mode=mode):
                with self.assertRaises(AssertionError): V.verify_manifest(x,self.p)
    def test_forward_state(self):
        self.assertEqual(self.s["schema_version"],self.l["binding"]["reviewed_state_version"])
        self.assertEqual(self.l["binding"]["reviewed_state_version"],self.s["historical_audit"]["research_omission_guard"]["reviewed_state_version"])
        self.assertEqual(self.l["binding"]["latest_research_focus_prefix"],self.s["historical_audit"]["current_focus"][-1].split(" ",1)[0])
        self.assertTrue(any(x.startswith("13JP ") for x in self.s["historical_audit"]["current_focus"]))
        self.assertEqual(self.l["binding"]["source_focus_count"],len(self.s["historical_audit"]["current_focus"]))
        issue=next(q for q in self.l["issues"] if q["id"]=="TW-OPEN-0005")
        self.assertIn(E.relative_to(ROOT).as_posix(),issue["source_refs"])
        self.assertEqual((issue["priority"],issue["status"]),("P0","OPEN"))
        for prev in ("13JJ CURRENT ACTION:","13JN CURRENT ACTION:","13JO CURRENT ACTION:"):
            self.assertIn(prev,issue["next_action"])
        self.assertTrue(any(x.get("revision_id","").startswith("TW-OPEN-0005-13JP") for x in issue["history"]))
        self.assertEqual(self.l["checkpoint_log"][-1]["state_version"],self.s["schema_version"])
        self.assertEqual(self.s["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
if __name__=="__main__":unittest.main()
