"""12SE regression of F8 87 page original-JPEG evidence-scoped bounded review."""
import json,tempfile,unittest
from pathlib import Path
from scripts.verify_yehuobian_nlc_f8_all87_native_12se import RECORD,verify
class F8All87Native12SE(unittest.TestCase):
    def test_good(self):
        self.assertEqual(verify()["native_bounded_source_pages"],751)
    def mutation(self,fn):
        d=json.loads(RECORD.read_text(encoding="utf-8"));fn(d)
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/"mutated.json";p.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):verify(p)
    def test_changed_image_hash(self):
        self.mutation(lambda d:d["review"]["original_jpeg_sha256_by_pdf_page"].__setitem__(0,"0"*64))
    def test_reordered_pages(self):
        self.mutation(lambda d:d["review"]["original_jpeg_sha256_by_pdf_page"].reverse())
    def test_unjustified_target_absence(self):
        self.mutation(lambda d:d["review"].__setitem__("whole_old20_work_target_absence_proven",True))
    def test_unjustified_positive_attestation(self):
        self.mutation(lambda d:d["review"].__setitem__("positive_old20_gaizao_louke_original_target_folio_attestation",True))
    def test_false_independent_copy(self):
        self.mutation(lambda d:d["grade_union"].__setitem__("independent_physical_holding_increment",1))
    def test_broken_archive_identity(self):
        self.mutation(lambda d:d["source"].__setitem__("archived_artifact_id",0))
if __name__=="__main__":unittest.main()
