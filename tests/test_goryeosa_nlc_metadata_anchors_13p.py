import copy
import importlib.util
import unittest
from pathlib import Path
F=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-nlc-metadata-anchors-13p.py"
spec=importlib.util.spec_from_file_location("anchors13p",F)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class NonVotingMetadataAnchors13P(unittest.TestCase):
 def test_exact_gate(self):self.assertEqual(m.verify()["status"],"PASS")
 def test_uploader_description_not_direct_image(self):
  e=copy.deepcopy(m.read(m.E));e["documented_anchors"][0]["original_leaf_juan_directly_inspected"]=True
  with self.assertRaises(AssertionError):m.check(e)
 def test_unverified_target_stays_unknown(self):
  e=copy.deepcopy(m.read(m.E));e["documented_anchors"][1]["target_work52_in_this_digital_group"]=False
  with self.assertRaises(AssertionError):m.check(e)
 def test_independent_numeric_vote_forbidden(self):
  e=copy.deepcopy(m.read(m.E));e["adjudication"]["independent_original_numeric_votes_added"]=1
  with self.assertRaises(AssertionError):m.check(e)
 def test_no_guess_for_internal_juan(self):
  e=copy.deepcopy(m.read(m.E));e["documented_anchors"][0]["uploader_description_internal_zhi_juan"]=[6]
  with self.assertRaises(AssertionError):m.check(e)
if __name__=="__main__":unittest.main()
