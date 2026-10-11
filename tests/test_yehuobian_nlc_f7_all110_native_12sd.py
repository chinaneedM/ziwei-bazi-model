"""12SD regression: source chain continuity and evidence-scope firewalls."""
import json,tempfile,unittest
from pathlib import Path
from scripts.verify_yehuobian_nlc_f7_all110_native_12sd import verify,RECORD
class F7All110Native12SD(unittest.TestCase):
    def test_success(self):
        self.assertEqual(verify()["global_native_source_pages"],664)
    def mutate_and_reject(self,mutator):
        data=json.loads(RECORD.read_text(encoding="utf-8"));mutator(data)
        with tempfile.TemporaryDirectory() as x:
            p=Path(x)/"candidate.json"
            p.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):verify(p)
    def test_modify_sha(self):
        self.mutate_and_reject(lambda x:x["review"]["page_sha256_in_order"].__setitem__(0,"0"*64))
    def test_duplicate_page(self):
        self.mutate_and_reject(lambda x:x["review"]["page_sha256_in_order"].__setitem__(1,x["review"]["page_sha256_in_order"][0]))
    def test_bad_window(self):
        self.mutate_and_reject(lambda x:x["review"]["montage_page_windows"].append([109,110]))
    def test_false_absence(self):
        self.mutate_and_reject(lambda x:x["review"].__setitem__("entire_old20_target_absence_proven",True))
    def test_miscount(self):
        self.mutate_and_reject(lambda x:x["grade_union"].__setitem__("global_not_real",12))
    def test_archive_mismatch(self):
        self.mutate_and_reject(lambda x:x["source"].__setitem__("archived_artifact_id",0))
if __name__=="__main__":unittest.main()
