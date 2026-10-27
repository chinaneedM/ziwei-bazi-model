import copy,importlib.util,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("ver13im",root/"scripts/verify-tianwen-13im-sysu-journal-pdf.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class JournalPdf(unittest.TestCase):
    def test_source(self):self.assertTrue(m.check(m.read()))
    def test_no_raw_byte_claim(self):
        for key,value in (("binary_downloaded_to_project",True),("raw_pdf_bytes_sha256","fabricated"),("visual_page_100_chinese_glyphs_exhaustive",True)):
            x=copy.deepcopy(m.read());x["journal_original"][key]=value
            with self.assertRaises(AssertionError):m.check(x,False)
    def test_not_ancient_original(self):
        x=copy.deepcopy(m.read());x["scope_boundaries"]["gk3467_original_d1_to_d7_recovered"]=True
        with self.assertRaises(AssertionError):m.check(x,False)
    def test_no_fabricated_copy(self):
        x=copy.deepcopy(m.read());x["scope_boundaries"]["physical_copy_missing_leaf_count"]=6
        with self.assertRaises(AssertionError):m.check(x,False)
if __name__=="__main__":unittest.main()
