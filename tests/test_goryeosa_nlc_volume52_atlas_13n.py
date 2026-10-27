import copy
import importlib.util
import unittest
from pathlib import Path
F=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-nlc-volume52-atlas-13n.py"
sp=importlib.util.spec_from_file_location("atlas13n",F)
m=importlib.util.module_from_spec(sp)
sp.loader.exec_module(m)
class ScanAtlas13N(unittest.TestCase):
 def test_gate(self):self.assertEqual(m.verify()["status"],"PASS")
 def test_hypothetical_work52_not_prelabelled(self):
  e=m.read(m.E);e["scan_atlas"]["records"][5]["contains_target_work_volume52"]=True
  with self.assertRaises(AssertionError):m.check(e)
 def test_nlc_numeric_vote_requires_original(self):
  e=m.read(m.E);e["adjudication"]["independent_copy_numeric_votes_added"]=1
  with self.assertRaises(AssertionError):m.check(e)
 def test_cadal52_not_same_as_work52(self):
  e=m.read(m.E);e["cadal_misleading_title_control"]["may_vote_on_work52"]=True
  with self.assertRaises(AssertionError):m.check(e)
 def test_original_sha_not_fabricated(self):
  e=m.read(m.E);e["scan_atlas"]["records"][2]["source_pdf_sha256"]="f"*64
  with self.assertRaises(AssertionError):m.check(e)
 def test_omit_boundary_control_fails(self):
  e=m.read(m.E);e["scan_atlas"]["boundary_control_groups"].remove(44)
  with self.assertRaises(AssertionError):m.check(e)
if __name__=="__main__":unittest.main()
