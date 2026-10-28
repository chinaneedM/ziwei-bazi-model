import importlib.util,tempfile,unittest
from pathlib import Path
sp=Path(__file__).resolve().parents[1]/"scripts"/"audit-tianwen-live-source-count-guards-r1.py"
spec=importlib.util.spec_from_file_location("scan",sp);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
class SourceGuardTriage(unittest.TestCase):
 def test_flags_live_count_assert(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"scripts";p.mkdir()
   (p/"one.py").write_text(" assert s['external_source_registry_total_unique_count']==761\n")
   self.assertEqual(len(M.scan(Path(td))),1)
 def test_ignores_frozen_source_snapshot(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"scripts";p.mkdir()
   (p/"one.py").write_text(" assert im['source_registry_total_unique_count']==761\n")
   self.assertEqual(len(M.scan(Path(td))),0)
 def test_ignores_unrelated_digit(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"scripts";p.mkdir()
   (p/"one.py").write_text(" assert x['rows']==761\n")
   self.assertEqual(M.scan(Path(td)),[])
if __name__=="__main__":unittest.main()
