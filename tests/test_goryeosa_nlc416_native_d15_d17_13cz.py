import copy
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-nlc416-native-d15-d17-13cz.py"
spec=importlib.util.spec_from_file_location("tw13cz",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13CZ(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
 def check(self,e=None,l=None):
  return m.check(self.e if e is None else e,self.s,self.l if l is None else l)
 def test_pass(self):self.assertTrue(self.check())
 def bad(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_sha_is_stable(self):self.bad(lambda e:e["provenance"].update(sha256="0"*64))
 def test_numeric_page(self):self.bad(lambda e:e["page_binding"].update(numeric_pdf=142))
 def test_header(self):self.bad(lambda e:e["page_binding"].update(field="日差"))
 def test_printed_not_derived(self):self.bad(lambda e:e["native_original_rois"][1].update(value="5.2362"))
 def test_roi_hash(self):self.bad(lambda e:e["native_original_rois"][1].update(rgb_sha256="0"*64))
 def test_no_witness_inflation(self):self.bad(lambda e:e["lineage"].update(independent_early_physical_witnesses_added=1))
 def test_no_emendation(self):self.bad(lambda e:e["numerical_scope"].update(emend_original_text=True))
 def test_d17_literal(self):self.bad(lambda e:e["native_original_rois"][2].update(literal="五分二三六二"))
 def test_ledger(self):
  l=copy.deepcopy(self.l);l["binding"]["source_focus_count"]-=1
  with self.assertRaises(AssertionError):self.check(l=l)
if __name__=="__main__":unittest.main()
