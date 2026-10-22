import copy
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-nlc416-three-columns-13da.py"
s=importlib.util.spec_from_file_location("tw13da",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Test13DA(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.state=m.load(m.S);cls.ledger=m.load(m.L)
 def check(self,e=None,l=None):return m.check(self.e if e is None else e,self.state,self.ledger if l is None else l)
 def bad(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_pass(self):self.assertTrue(self.check())
 def test_field_swap(self):self.bad(lambda e:e["source_native_lanes"][1].update(field="CUMULATIVE"))
 def test_roi_sha(self):self.bad(lambda e:e["source_native_lanes"][1].update(rgb_sha256="0"*64))
 def test_wrong_cumulative(self):self.bad(lambda e:e["source_native_lanes"][4].update(value="7570.7624"))
 def test_wrong_short(self):self.bad(lambda e:e["source_short_prior_13cz"][1].update(value="5.2362"))
 def test_no_emend(self):self.bad(lambda e:e["arithmetic"].update(emend_original_text=True))
 def test_no_early_witness(self):self.bad(lambda e:e["impact"].update(new_early_independent_witnesses=1))
 def test_erratum_retained(self):self.bad(lambda e:e["forward_only_erratum"].update(previous_data_qualified_not_deleted=False))
 def test_ledger_binding(self):
  l=copy.deepcopy(self.ledger);l["binding"]["source_focus_count"]-=1
  with self.assertRaises(AssertionError):self.check(l=l)
if __name__=="__main__":unittest.main()
