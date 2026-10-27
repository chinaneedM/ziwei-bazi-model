import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-utokyo-agawa-collection-13ag.py"
s=importlib.util.spec_from_file_location("verify13ag",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class TestAgawaEvidenceScope(unittest.TestCase):
 def test_scope(self):self.assertTrue(m.verify())
 def test_one_list_two_paginations(self):
  e=m.load(m.E);self.assertTrue(e["original_1998_special_list"]["same_work_one_list_not_two"])
 def test_two_G23_not_attributed(self):
  e=m.load(m.E);self.assertTrue(all(x["agawa_membership"]=="UNVERIFIED" for x in e["checked_items"]))
 def test_no_manuscript_num_values(self):
  e=m.load(m.E);self.assertTrue(e["no_new_numeric_witnesses"])
if __name__=="__main__":unittest.main()
