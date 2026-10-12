import ast
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/replay-yehuobian-image-registration-12tc.py"
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12TB-PRINT-IMAGE-MISREAD-CORRECTION-R1.json"
STATE=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
class ImageRegistrationReplayContract12TC(unittest.TestCase):
 def test_replay_script_syntax_source_hash_and_fails_closed(self):
  content=SCRIPT.read_text(encoding="utf-8")
  ast.parse(content)
  self.assertIn("SOURCE_JPEG_SHA256_MISMATCH_FAIL_CLOSED",content)
  self.assertIn("SOURCE_PAGE_DIMENSION_MISMATCH_FAIL_CLOSED",content)
  self.assertIn("cv2.SIFT_create(nfeatures=4500)",content)
  self.assertIn("cv2.findHomography(p, q, cv2.RANSAC, 3.5)",content)
  self.assertIn("same_physical_copy_proven",content)
  r=json.loads(RECORD.read_text(encoding="utf-8"))
  self.assertIn(r["original_images"]["cadal"]["jpeg_sha256"],content)
  self.assertIn(r["original_images"]["xuxiu"]["jpeg_sha256"],content)
 def test_state_keeps_evidence_uncertainty(self):
  s=json.loads(STATE.read_text(encoding="utf-8"))
  self.assertTrue(any(x.startswith("12TC IMAGE-REGISTRATION") for x in s["historical_audit"]["current_focus"]))
  self.assertEqual(s["historical_audit"]["external_source_registry_total_unique_count"],660)
  self.assertEqual(len(s["historical_audit"]["completed_batches"]),487)
  self.assertEqual(s["invariants"]["algorithm_reopen_count"],0)
  self.assertEqual(s["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
if __name__=="__main__":unittest.main()
