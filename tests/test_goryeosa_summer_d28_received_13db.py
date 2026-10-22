import copy
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-summer-d28-received-13db.py"
s=importlib.util.spec_from_file_location("tw13db",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Test13DB(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.state=m.load(m.S);cls.ledger=m.load(m.L)
 def check(self,e=None,l=None):return m.check(self.e if e is None else e,self.state,self.ledger if l is None else l)
 def bad(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_pass(self):self.assertTrue(self.check())
 def test_wrong_printed_D28(self):self.bad(lambda e:e["received_summer_rows"][1].update(xingdu_literal="初度九十六四五四九"))
 def test_false_original_authority(self):self.bad(lambda e:e["witness_scope"].update(original_glyph_authority=True))
 def test_false_print_error(self):self.bad(lambda e:e["local_arithmetic"].update(alleged_ancient_printing_defect_proven=True))
 def test_false_independent_witness(self):self.bad(lambda e:e["adjudication"].update(new_independent_original_witnesses=1))
 def test_false_original_emendation(self):self.bad(lambda e:e["local_arithmetic"].update(original_emendation_authorized=True))
 def test_wrong_long(self):self.bad(lambda e:e["received_summer_rows"][1].update(long="354.6101"))
 def test_wrong_cumulative(self):self.bad(lambda e:e["received_summer_rows"][2].update(cumulative="12200.2798"))
 def test_scope_confusion(self):self.bad(lambda e:e["adjudication"].update(differentiated_from_13DA="SAME_TABLE"))
 def test_ledger_binding(self):
  l=copy.deepcopy(self.ledger);l["binding"]["source_focus_count"]-=1
  with self.assertRaises(AssertionError):self.check(l=l)
if __name__=="__main__":unittest.main()
