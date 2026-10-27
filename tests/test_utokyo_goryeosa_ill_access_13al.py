import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-utokyo-goryeosa-ill-access-13al.py"
spec=importlib.util.spec_from_file_location("g13al",p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class TestUTokyoILLAccess(unittest.TestCase):
 def test_replay(self):self.assertTrue(mod.verify())
 def test_unobserved_originals(self):
  d=mod.load(mod.E)
  self.assertTrue(all(x["original_D16"] is None and not x["direct_original_target_image"] for x in d["targets"]))
 def test_ill_is_not_permission(self):
  d=mod.load(mod.E)
  self.assertEqual(d["access_routes"]["remote_individual_direct_request"],"NOT_ACCEPTED_BY_PROVIDER")
  self.assertFalse(d["access_routes"]["approval_received"])
  self.assertFalse(d["provenance_fences"]["foreign_ill_exemption_established"])
if __name__=="__main__":unittest.main()
