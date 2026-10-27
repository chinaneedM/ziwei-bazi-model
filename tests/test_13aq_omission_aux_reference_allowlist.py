import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-research-omission-risk-ledger-r1.py"
s=importlib.util.spec_from_file_location("issue13aq",p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class TestStrictAuxPaths(unittest.TestCase):
 def test_exact_three_only(self):
  expected={"scripts/probe-najda-goryeosa-13ap.py",".github/workflows/probe-najda-goryeosa-13ap.yml","tests/test_probe_najda_goryeosa_13ap.py"}
  self.assertEqual(m.ALLOWED_13AP_AUX_REFS,expected)
  for p in expected:
   self.assertTrue(m.valid_issue_source_ref("TW-OPEN-0005",p))
   self.assertFalse(m.valid_issue_source_ref("TW-OPEN-0006",p))
 def test_no_escape_or_general_code_paths(self):
  for p in ["scripts/not-whitelisted.py","../docs/test.json","docs/../secrets.txt","tests/random.py","https://random.example/"]:
   self.assertFalse(m.valid_issue_source_ref("TW-OPEN-0005",p))
  self.assertTrue(m.valid_issue_source_ref("TW-OPEN-0005","docs/research/TIANWEN-13AP-NAJDA-SOURCE-EMITTED-BOOK52-LINK-PROBE-R1.json"))
if __name__=="__main__":unittest.main()
