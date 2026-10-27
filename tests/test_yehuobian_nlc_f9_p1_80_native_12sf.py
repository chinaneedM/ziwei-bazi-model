"""12SF: prevent hash order drift, evidence-grade overclaim and count corruption."""
import json,tempfile,unittest
from pathlib import Path
from scripts.verify_yehuobian_nlc_f9_p1_80_native_12sf import verify,RECORD
class F9Native12SF(unittest.TestCase):
    def test_valid(self):
        r=verify()
        self.assertEqual((r["global_native_source_pages"],r["f9_pending"]),(831,61))
    def mutate(self,fn):
        d=json.loads(RECORD.read_text(encoding="utf-8"));fn(d)
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/"bad.json";f.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):verify(f)
    def test_hash_change(self):
        self.mutate(lambda d:d["review"]["individual_source_page_sha256_in_pdf_order"].__setitem__(0,"0"*64))
    def test_page_reordering(self):
        self.mutate(lambda d:d["review"]["individual_source_page_sha256_in_pdf_order"].reverse())
    def test_negative_absence_claim(self):
        self.mutate(lambda d:d["review"].__setitem__("whole_f9_target_absence_proven",True))
    def test_physical_copies_overcount(self):
        self.mutate(lambda d:d["grade_union"].__setitem__("new_physical_copy_count",1))
    def test_volume17_unsupported_upgrade(self):
        self.mutate(lambda d:d["review"].__setitem__("f9_original_volume17_boundary_native_reviewed_this_batch",True))
    def test_archived_zip_identity_drift(self):
        self.mutate(lambda d:d["source"].__setitem__("artifact_zip_sha256","0"*64))
if __name__=="__main__":unittest.main()
