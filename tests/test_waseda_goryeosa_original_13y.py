import importlib.util,copy,unittest,json
from decimal import Decimal
from pathlib import Path
P=Path(__file__).resolve().parents[1]
p=P/'scripts'/'verify-waseda-goryeosa-13y.py'
spec=importlib.util.spec_from_file_location('waseda13y',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class WasedaOriginalDay12To20(unittest.TestCase):
 def test_static_contract(self):self.assertTrue(m.check(m.read()))
 def test_source_day16_not_normalized_silently(self):
  d=copy.deepcopy(m.read());d['original_short_day_series'][4]['original_glyph']='五分二三六二'
  with self.assertRaises(AssertionError):m.check(d)
 def test_independent_vote_not_promoted(self):
  d=copy.deepcopy(m.read());d['restrictions']['physical_independent_vote_added']=1
  with self.assertRaises(AssertionError):m.check(d)
 def test_neighbor_anomaly(self):
  d=copy.deepcopy(m.read());d['arithmetic']['exception_d15_to_d16']='0.0186'
  with self.assertRaises(AssertionError):m.check(d)
if __name__=='__main__':unittest.main()
