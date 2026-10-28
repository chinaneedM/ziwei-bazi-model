"""13JO static replay manifest gate plus mutation rejection; real archive replay uses CLI."""
import importlib.util,json,unittest
from copy import deepcopy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13JO-GK5553-13JL-ORIGINAL-JPEG-PIXEL-ROI-REPLAY-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
V=R/"scripts/verify-tianwen-13jo-gk5553-original-roi-replay.py"
spec=importlib.util.spec_from_file_location("tianwen_13jo",V)
v=importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
class OriginalRoiReplay(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=json.loads(E.read_text(encoding="utf-8"))
  cls.s=json.loads(S.read_text(encoding="utf-8"))
  cls.l=json.loads(L.read_text(encoding="utf-8"))
 def test_six_jpegs_twelve_crops(self):
  v.verify_manifest(self.e)
  self.assertEqual(self.e["source"]["official_original_image_artifact_id"],12809334156)
  self.assertEqual(self.e["replay_result"]["source_original_jpeg_sha256_verified"],6)
  self.assertEqual(self.e["replay_result"]["source_original_rgb_sha256_verified"],6)
  self.assertEqual(self.e["replay_result"]["large_integer_roi_digests_recalculated"],12)
 def test_negative_mutations_fail_closed(self):
  for kind in ("noninteger","bad_hash","false_independent_copy"):
   row=deepcopy(self.e)
   if kind=="noninteger":row["original_images"][0]["original_rgb_rois"][0]["xyxy"][0]="724"
   if kind=="bad_hash":row["original_images"][0]["original_rgb_rois"][0]["rgb_sha256"]="z"*64
   if kind=="false_independent_copy":row["replay_result"]["new_independent_physical_witness_votes"]=1
   with self.subTest(kind=kind):
    with self.assertRaises(AssertionError):v.verify_manifest(row)
 def test_state_and_ledger_forward_only(self):
  self.assertEqual(self.s["schema_version"],"1.913.0")
  self.assertEqual(self.l["binding"]["reviewed_state_version"],"1.913.0")
  self.assertEqual(self.s["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"1.913.0")
  self.assertEqual(self.l["binding"]["source_focus_count"],len(self.s["historical_audit"]["current_focus"]))
  self.assertEqual(self.l["binding"]["latest_research_focus_prefix"],"13JP")
  self.assertTrue(any(x.startswith("13JO ") for x in self.s["historical_audit"]["current_focus"]))
  self.assertTrue(self.s["historical_audit"]["current_focus"][-1].startswith("13JP "))
  i=next(x for x in self.l["issues"] if x["id"]=="TW-OPEN-0005")
  self.assertEqual((i["status"],i["priority"]),("OPEN","P0"))
  self.assertIn(E.relative_to(R).as_posix(),i["source_refs"])
  self.assertIn("13JN CURRENT ACTION:",i["next_action"])
  self.assertIn("13JM CURRENT ACTION:",i["next_action"])
  self.assertTrue(any(x.get("revision_id","").startswith("TW-OPEN-0005-13JO") for x in i["history"]))
  self.assertEqual(self.l["checkpoint_log"][-1]["state_version"],"1.913.0")
  self.assertEqual(self.s["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
if __name__=="__main__":unittest.main()
