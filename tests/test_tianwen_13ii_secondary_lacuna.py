import copy
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("scope13ii",ROOT/"scripts/verify-tianwen-13ii-secondary-lacuna.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestScope(unittest.TestCase):
    def test_evidence(self): self.assertTrue(m.check(m.load()))
    def test_no_secondary_negative_proof(self):
        for k in ("secondary_silence_proves_juan52_complete","other_juan_lacunae_prove_juan52_loss","six_folio_residual_proves_six_missing_leaves","original_journal_pdf_target_lacuna_text_verified"):
            x=copy.deepcopy(m.load());x["adjudication"][k]=True
            with self.assertRaises(AssertionError):m.check(x,False)
if __name__=="__main__":unittest.main()
