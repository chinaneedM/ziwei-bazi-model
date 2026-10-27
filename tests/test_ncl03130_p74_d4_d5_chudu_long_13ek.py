import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-p74-d4-d5-chudu-long-13ek.py"
spec=importlib.util.spec_from_file_location("v13ek",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13EK(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.E);cls.s=m.read(m.S);cls.l=m.read(m.L);cls.ej=m.read(m.EJ);cls.ei=m.read(m.EI);cls.ed=m.read(m.ED)
 def go(self,e=None,l=None):return m.check(self.e if e is None else e,self.s,self.l if l is None else l,self.ej,self.ei,self.ed)
 def reject(self,fn):
  x=copy.deepcopy(self.e);fn(x)
  with self.assertRaises(AssertionError):self.go(e=x)
 def test_source_and_ledger(self):self.assertTrue(self.go())
 def test_reject_false_original_byte(self):self.reject(lambda e:e["rois"][0].update(rgb_sha256="0"*64))
 def test_reject_edited_d5_literal(self):self.reject(lambda e:e["rois"][1].update(visible_literal="初度九十五三三〇一"))
 def test_reject_fake_source_original_decimal(self):self.reject(lambda e:e["findings"].update(D30_exact_numeric_decimal="0.965038"))
 def test_reject_fake_digit_precision(self):self.reject(lambda e:e["findings"].update(source_literal_count_not_historical_decimal_precision=False))
 def test_reject_old_erroneous_column(self):self.reject(lambda e:e["findings"].update(legacy_13eh_misread_reinstated=True))
 def test_reject_rebranded_copy_count(self):self.reject(lambda e:e["source"].update(independent_original_witnesses_added=1))
 def test_reject_auto_field_map(self):self.reject(lambda e:e["findings"].update(technical_heading_map_to_p73="PROVEN"))
if __name__=="__main__":unittest.main()
