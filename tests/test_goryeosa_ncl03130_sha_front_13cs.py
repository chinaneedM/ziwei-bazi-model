import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-ncl03130-sha-front-13cs.py"
spec=importlib.util.spec_from_file_location("ncl13cs",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.read(m.E);cls.s=m.read('docs/PROJECT-CURRENT-STATE-R1.json');cls.l=m.read('docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json')
 def test_pass(self):self.assertTrue(m.check(self.e,self.s,self.l))
 def test_uncertainty(self):
  e=copy.deepcopy(self.e);e['original_front_preview_observation']['red_marks_identified_as_missing_juan_register']=True
  with self.assertRaises(AssertionError):m.check(e,self.s,self.l)
 def test_digest(self):
  e=copy.deepcopy(self.e);e['verified_capture']['pdf_sha256']='0'*64
  with self.assertRaises(AssertionError):m.check(e,self.s,self.l)
 def test_no_copy_inflation(self):
  e=copy.deepcopy(self.e);e['source_firewall']['third_original_copy_d16_count']=1
  with self.assertRaises(AssertionError):m.check(e,self.s,self.l)
if __name__=='__main__':unittest.main()
