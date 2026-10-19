import copy
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-utokyo-dual-holding-13ad.py"
spec=importlib.util.spec_from_file_location("goryeosa13ad",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class ManuscriptPrintCatalogBoundary(unittest.TestCase):
 def test_verification(self):self.assertTrue(m.verify())
 def test_do_not_promote_union_catalog_to_glyph(self):
  x=copy.deepcopy(m.load(m.S))
  self.assertFalse(x["sources"][0]["physical_glyph_authority"])
  self.assertEqual(x["sources"][0]["verification_status"],"BIBLIOGRAPHIC_METADATA_ONLY")
 def test_distinct_holding_no_copy_date(self):
  e=m.load(m.E);a=e["new_manuscript_holding"];b=e["known_print_holding"]
  self.assertNotEqual(a["ncid"],b["ncid"])
  self.assertNotEqual(a["individual_registration"],b["individual_registration"])
  self.assertIsNone(a["source_image_sha256"])
  self.assertEqual(a["copy_date"],"UNKNOWN")
 def test_forward_compatibility_with_future_shards(self):
  from unittest.mock import patch
  old=m.load
  st=copy.deepcopy(old("docs/PROJECT-CURRENT-STATE-R1.json"))
  le=copy.deepcopy(old("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
  ma=copy.deepcopy(old(m.M))
  st["schema_version"]="1.690.0";st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.690.0"
  st["historical_audit"]["current_focus"].append("13AE TEST_FUTURE")
  st["historical_audit"]["external_source_registry_extension_count"]+=1
  st["historical_audit"]["external_source_registry_total_unique_count"]+=1
  le["binding"]["reviewed_state_version"]="1.690.0"
  le["binding"]["latest_research_focus_prefix"]="13AE"
  le["binding"]["source_focus_count"]+=1
  le["checkpoint_log"].append({"id":"TEST_FUTURE","state_version":"1.690.0"})
  ma["extension_source_count"]+=1;ma["combined_source_count"]+=1
  ma["shards"].append({"path":"docs/research/future.json","schema":"TEST_FUTURE","source_count":1})
  def load(name):
   if name=="docs/PROJECT-CURRENT-STATE-R1.json":return st
   if name=="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json":return le
   if name==m.M:return ma
   return old(name)
  with patch.object(m,"load",side_effect=load):self.assertTrue(m.verify())
if __name__=="__main__":unittest.main()
