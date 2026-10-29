"""13KG: fail closed for altered Harvard printed glyph and imaginary antiquity."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
src=ROOT/"scripts/verify-tianwen-13kg-harvard-original.py"
sp=importlib.util.spec_from_file_location("v13kg",src)
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class TestHarvardOriginal(unittest.TestCase):
 def setUp(self):
  self.e=json.loads((ROOT/v.E).read_text())
  self.shard=json.loads((ROOT/v.SHARD).read_text())
 def test_positive_printed_loci(self):self.assertEqual(v.verify(self.e,self.shard)["visually_attested_printed_loci"],2)
 def test_no_altered_polarity(self):
  e=copy.deepcopy(self.e);e["witness"]["manually_collated_pages"][1]["literal"]=e["witness"]["manually_collated_pages"][1]["literal"].replace("益減損加","益加損減")
  with self.assertRaises(ValueError):v.verify(e,self.shard)
 def test_no_false_printed_tail(self):
  e=copy.deepcopy(self.e);e["observed_original_readings"]["after_81_wei_50_xian_explicit"]=True
  with self.assertRaises(ValueError):v.verify(e,self.shard)
 def test_no_huang_original(self):
  e=copy.deepcopy(self.e);e["remaining_boundaries"]["huang_printed_original_observed"]=True
  with self.assertRaises(ValueError):v.verify(e,self.shard)
 def test_no_new_physical_impression(self):
  e=copy.deepcopy(self.e);e["witness"]["edition_impression_date_bound"]=True
  with self.assertRaises(ValueError):v.verify(e,self.shard)
 def test_reject_bad_image_binding(self):
  s=copy.deepcopy(self.shard);s["sources"][0]["direct_image_attestation"]["page_sha256"]["12"]="0"*64
  with self.assertRaises(ValueError):v.verify(self.e,s)
 def test_no_cross_witness_numeric_winner(self):
  e=copy.deepcopy(self.e);e["remaining_boundaries"]["G893_cross_witness_numeric_winners"]=1
  with self.assertRaises(ValueError):v.verify(e,self.shard)
if __name__=="__main__":unittest.main()
