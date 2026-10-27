import importlib.util
import unittest
from pathlib import Path
F=Path(__file__).resolve().parents[1]/'scripts'/'verify-goryeosa-nlc99-13j.py'
spec=importlib.util.spec_from_file_location('nlc99_13j',F)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class CopyFirewall13J(unittest.TestCase):
 def test_integrity(self): self.assertEqual(m.verify()['status'],'PASS')
 def test_colophon_is_not_print_date(self):
  e=m.read(m.E);e['waseda']['impression_year']=1848
  with self.assertRaises(AssertionError):m.validate(e)
 def test_digital_99_not_physical_99(self):
  e=m.read(m.E);e['nlc']['physical_books_verified']=99
  with self.assertRaises(AssertionError):m.validate(e)
 def test_work1451_not_copy1451(self):
  e=m.read(m.E);e['wul_mirror']['official_imprint_year']=1451
  with self.assertRaises(AssertionError):m.validate(e)
 def test_surrogate_not_new_witness(self):
  e=m.read(m.E);e['wul_mirror']['new_independent_copy']=True
  with self.assertRaises(AssertionError):m.validate(e)
 def test_unread_glyph_does_not_vote(self):
  e=m.read(m.E);e['nlc']['d16_glyph']='五二三六二'
  with self.assertRaises(AssertionError):m.validate(e)
if __name__=='__main__':unittest.main()
