import copy
import importlib.util
import unittest
from pathlib import Path
p = Path(__file__).resolve().parents[1] / "scripts" / "verify-tianwen-13fl-gk05553-repair-ordinal-scope.py"
spec = importlib.util.spec_from_file_location("v13fl", p)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
class Test13FL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = v.load(v.E)
        cls.p = v.load(v.P)
        cls.s = v.load(v.S)
        cls.l = v.load(v.L)
    def test_valid(self):
        self.assertTrue(v.check(self.e,self.p,self.s,self.l))
    def reject(self, fn):
        e = copy.deepcopy(self.e)
        fn(e)
        with self.assertRaises(AssertionError):
            v.check(e,self.p,self.s,self.l)
    def test_erase_official_29(self):
        self.reject(lambda e:e["first_party_catalog"].update(replacement_book_ordinals=[8,26,28]))
    def test_erase_secondary_28(self):
        self.reject(lambda e:e["secondary_scholarship"].update(replacement_book_ordinals_from_republished_text=[8,26,29]))
    def test_conflate_edition_impression(self):
        self.reject(lambda e:e["first_party_catalog"].update(edition_impression_date=1454))
    def test_forge_book52_binding(self):
        self.reject(lambda e:e["relation_to_active_rule"].update(work_juan_52_to_physical_book=17))
    def test_forge_original_d9(self):
        self.reject(lambda e:e["relation_to_active_rule"].update(NLC_D9_original="四分五八二〇"))
    def test_erase_original_d5_disagreement(self):
        self.reject(lambda e:e["relation_to_active_rule"].update(NLC_D5_original="四分五一七二"))
    def test_claim_scholarly_pdf_direct(self):
        self.reject(lambda e:e["secondary_scholarship"].update(original_article_pdf_direct_page_collation=True))
    def test_unauthorized_witness_inflation(self):
        self.reject(lambda e:e["impact"].update(new_independent_physical_witnesses=1))
if __name__ == "__main__":
    unittest.main()
