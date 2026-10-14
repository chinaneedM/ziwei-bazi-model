"""12VR — synthetic byte-level tests, never historical attestation."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("yehuobian12vr",ROOT/"scripts/verify-yehuobian-original-leaf-intake-r1.py")
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
QUEUE=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12UK-ORIGINAL-LEAF-INTAKE-QUEUE-R1.json"
CONTROL=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12UF-SOURCE-READING-CONTROL-AND-IMPRESSION-GATES-R1.json"

class ActualBytes(unittest.TestCase):
 def setUp(self):
  self.q=json.loads(QUEUE.read_text())
  self.control=json.loads(CONTROL.read_text())
  self.tmp=tempfile.TemporaryDirectory()
  self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name)
  self.source=b"SYNTHETIC_12VR_SOURCE_A"
  self.page=b"SYNTHETIC_12VR_PAGE_A"
  self.prepare(0)
 def prepare(self,index,source=None,page=None):
  source=source if source is not None else self.source
  page=page if page is not None else self.page
  src=f"source{index}.pdf"; img=f"image{index}.jpg"
  (self.root/src).write_bytes(source)
  (self.root/img).write_bytes(page)
  row=self.q["candidates"][index]
  row.update(stage="IMAGE_CAPTURED",
   source_issued_image_url="https://example.invalid/synthetic-only",
   source_binary_sha256=hashlib.sha256(source).hexdigest(),
   source_local_file=src,
   pages=[{"page_label":f"image{index}","sha256":hashlib.sha256(page).hexdigest(),"local_file":img}],
   target_original_folio="SYNTHETIC_UNIT_TEST_NOT_A_REAL_FOLIO",
   relationship_to_prior_surfaces="DISTINCT_BYTES_RELATION_UNRESOLVED")
  return row
 def invalid(self,needle):
  with self.assertRaisesRegex(ValueError,needle):
   gate.validate(self.q,self.control,artifact_root=self.root)
 def test_positive_actual_bytes_still_zero_votes(self):
  a=gate.validate(self.q,self.control,artifact_root=self.root)
  self.assertEqual((a["captured_images"],a["binary_verified_image_captures"],a["independent_ancient_glyph_votes"]),(1,1,0))
 def test_positive_without_root_rejected(self):
  with self.assertRaisesRegex(ValueError,"actual artifact root"):
   gate.validate(self.q,self.control)
 def test_source_mutation_rejected(self):
  (self.root/"source0.pdf").write_bytes(b"CHANGED");self.invalid("actual source/page file bytes")
 def test_page_mutation_rejected(self):
  (self.root/"image0.jpg").write_bytes(b"CHANGED");self.invalid("actual source/page file bytes")
 def test_forged_64hex_rejected(self):
  self.q["candidates"][0]["pages"][0]["sha256"]="f"*64;self.invalid("actual source/page file bytes")
 def test_source_missing_rejected(self):
  (self.root/"source0.pdf").unlink();self.invalid("file missing")
 def test_parent_escape_rejected(self):
  self.q["candidates"][0]["source_local_file"]="../elsewhere.pdf";self.invalid("unsafe image artifact")
 def test_absolute_path_rejected(self):
  self.q["candidates"][0]["pages"][0]["local_file"]=str(self.root/"image0.jpg");self.invalid("unsafe image artifact")
 def test_symlink_outside_root_rejected(self):
  with tempfile.TemporaryDirectory() as outside:
   f=Path(outside)/"a.pdf";f.write_bytes(self.source)
   (self.root/"source0.pdf").unlink();(self.root/"source0.pdf").symlink_to(f)
   self.invalid("escapes root")
 def test_duplicate_source_across_copies_rejected(self):
  self.prepare(1,source=self.source,page=b"OTHER SYNTHETIC PAGE");self.invalid("duplicate original source bytes")
 def test_duplicate_page_across_copies_rejected(self):
  self.prepare(1,source=b"OTHER SYNTHETIC SOURCE",page=self.page);self.invalid("duplicate original page bytes")
 def test_two_distinct_binary_copies_remain_zero_vote(self):
  self.prepare(1,source=b"OTHER SYNTHETIC SOURCE",page=b"OTHER SYNTHETIC PAGE")
  a=gate.validate(self.q,self.control,artifact_root=self.root)
  self.assertEqual((a["binary_verified_image_captures"],a["independent_ancient_glyph_votes"]),(2,0))
 def test_print_state_wrong_page_digest_rejected(self):
  row=self.q["candidates"][0];row["stage"]="PRINT_STATE_CANDIDATE"
  row["printing_state_evidence"]={"source_page_label":"image0","source_page_sha256":"f"*64,"adjudication":"MANUAL_REVIEW_PENDING","dated_paratext_quotation":"SYNTHETIC 1827"}
  self.invalid("print-state paratext")
 def test_print_state_wrong_page_label_rejected(self):
  row=self.q["candidates"][0];row["stage"]="PRINT_STATE_CANDIDATE"
  row["printing_state_evidence"]={"source_page_label":"other","source_page_sha256":row["pages"][0]["sha256"],"adjudication":"MANUAL_REVIEW_PENDING","dated_paratext_quotation":"SYNTHETIC 1827"}
  self.invalid("print-state paratext")
 def test_print_state_matching_image_still_pending(self):
  row=self.q["candidates"][0];row["stage"]="PRINT_STATE_CANDIDATE"
  row["printing_state_evidence"]={"source_page_label":"image0","source_page_sha256":row["pages"][0]["sha256"],"adjudication":"MANUAL_REVIEW_PENDING","dated_paratext_quotation":"SYNTHETIC PARATEXT UNIT TEST"}
  a=gate.validate(self.q,self.control,artifact_root=self.root)
  self.assertEqual((a["print_state_candidates"],a["independent_ancient_glyph_votes"]),(1,0))
 def test_null_catalogue_live_queue_unchanged(self):
  self.assertEqual(gate.verify()["captured_images"],0) # live historical JSON untouched
if __name__=="__main__":unittest.main()
