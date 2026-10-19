import importlib.util,copy,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-utokyo-hanseki1995-13ae.py"
s=importlib.util.spec_from_file_location("catalog13ae",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class HansekiBibliographyFirewall(unittest.TestCase):
 def test_scope_gate(self):self.assertTrue(m.verify())
 def test_metadata_not_folio(self):
  e=m.load(m.E);self.assertFalse(e["observed_access"]["fulltext_page_level_entry_read"])
  self.assertIsNone(e["observed_access"]["source_pdf_sha256"])
  self.assertFalse(m.load(m.S)["sources"][0]["physical_glyph_authority"])
 def test_nonpromotion_preserves_dates(self):
  x=m.load(m.E);self.assertLess(x["source"]["edition_main_year"],x["source"]["repository_deposit_year"])
  self.assertEqual(len({z["url"] for z in x["source"]["repository_section_files"]}),3)
 def test_forward_compatible_beyond_13ae(self):
  from unittest.mock import patch
  old=m.load;st=copy.deepcopy(old("docs/PROJECT-CURRENT-STATE-R1.json"));l=copy.deepcopy(old("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"));ma=copy.deepcopy(old(m.M))
  st["schema_version"]="1.691.0";st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.691.0"
  st["historical_audit"]["current_focus"].append("13AF simulated")
  st["historical_audit"]["external_source_registry_extension_count"]+=1
  st["historical_audit"]["external_source_registry_total_unique_count"]+=1
  l["binding"]["reviewed_state_version"]="1.691.0";l["binding"]["latest_research_focus_prefix"]="13AF";l["binding"]["source_focus_count"]+=1
  l["checkpoint_log"].append({"id":"SIMULATED","state_version":"1.691.0"})
  ma["extension_source_count"]+=1;ma["combined_source_count"]+=1;ma["shards"].append({"path":"docs/research/future.json","schema":"TEST","source_count":1})
  def load(path):
   if path=="docs/PROJECT-CURRENT-STATE-R1.json":return st
   if path=="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json":return l
   if path==m.M:return ma
   return old(path)
  with patch.object(m,"load",side_effect=load):self.assertTrue(m.verify())
if __name__=="__main__":unittest.main()
