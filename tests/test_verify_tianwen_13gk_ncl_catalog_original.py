import copy
import importlib.util
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('ncl_original',Path(__file__).resolve().parents[1]/'scripts/verify-tianwen-13gk-ncl-catalog-original.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class TestNclOriginal(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E)
 def reject(self,mutate):
  e=copy.deepcopy(self.e);mutate(e)
  with self.assertRaises(AssertionError):m.check(e)
 def test_sealed_source_record(self):self.assertTrue(m.check(self.e))
 def test_logical_row_cannot_be_physical_line(self):self.reject(lambda e:e['target_record'].update(physical_start_line=3541,physical_end_line=3541))
 def test_catalog_date_must_not_be_normalized(self):self.reject(lambda e:e['target_record']['fields'].update(版本='清初舊鈔光緒補鈔本'))
 def test_unverified_leaf_cannot_be_promoted(self):self.reject(lambda e:e['unresolved'].update(physical_target_leaf='74a'))
 def test_1909_glyph_cannot_fill_old_day30(self):self.reject(lambda e:e['unresolved'].update(old_d30='四分九二二二'))
 def test_changed_fragment_rejected(self):self.reject(lambda e:e['target_record']['raw_record'].update(sha256='0'*64))
 def test_report_only_cannot_claim_full_replay(self):self.reject(lambda e:e['independent_replay'].update(full_csv_sha_recomputed=False))
 def test_wrong_whole_source_bytes_rejected(self):
  with self.assertRaises(AssertionError):m.check(self.e,b'partial CSV')

if __name__=='__main__':unittest.main()
